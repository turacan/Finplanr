#!/usr/bin/env python3
"""Build the local instrument search index (ETFs, ETCs/ETNs, stocks, funds) from official, openly reusable reference data.

    python3 -I tools/fetch-instruments.py [--refresh] [--offline] [--out PATH] [--with-xetra] [--no-openfigi] [--no-wikidata] [--verify]

Sources used by DEFAULT (all of them reusable without asking anybody; see private/INSTRUMENT-DATA-NOTES.md for URLs, quotes and the
residual uncertainty):
  esma      ESMA FIRDS full files FULINS_C (collective investment vehicles), FULINS_E (equities), FULINS_D (debt, only
            ETC/ETN/ETP products are taken from it). ISIN, full name, CFI code, trading venues (MIC). Weekly, XML in zip.
            Reuse: ESMA legal notice (reproduction authorised if the source is acknowledged and changes are stated);
            the EU Open Data Portal lists FIRDS under the Commission reuse notice (Decision 2011/833/EU: commercial use allowed).
  openfigi  OpenFIGI (Bloomberg L.P.) mapping API, ISIN -> ticker on Xetra (MIC XETR). Fills the "ticker" column for instruments
            that ESMA reports on Xetra. Free API, no key; FIGI identifiers are dedicated to the public domain.
  wikidata  Wikidata SPARQL (CC0): ticker of US stocks on NYSE / Nasdaq (only US ISINs, only unambiguous cases). Fills "ticker" and adds
            the venue XNYS / XNAS for stocks that are not on Xetra.
  WKN       derived arithmetically from German ISINs (DE000 + 6 characters + check digit); no other WKN source is used.

Optional, NOT part of the default (private use / only with a written licence from Deutsche Boerse):
  --with-xetra   also read the Deutsche Boerse "All tradable instruments" files for Xetra (CSV) and Boerse Frankfurt (zip/CSV):
                 WKN, mnemonic (= Xetra ticker), instrument type, trading currency, Xetra-only rows. The resulting index must NOT be
                 published unless Deutsche Boerse has granted a licence (no explicit reuse licence exists; database-right question open).

Output: build-cache/instruments.v1.json (compact index, contract "v":1, see validate-instruments.py), raw downloads in
build-cache/raw/ (git-ignored). The script is idempotent: a second run reuses the cached raw files (ESMA files are identified
by their dated file names; the OpenFIGI answers are cached for 30 days, the Wikidata answer for 7 days). It needs no API key and
sends no personal data (User-Agent identifies the tool generically). The ticker convention of the index: the ticker belongs to Xetra
when "XETR" is among the venues, otherwise to Nasdaq / NYSE (then "XNAS" / "XNYS" is among the venues); rows with no known ticker
are searchable by name, ISIN and (German ISINs) WKN.

Options:
  --refresh      download the ESMA / Wikidata data again, ignoring the cache (OpenFIGI answers are kept until they are 30 days old)
  --offline      no network access at all: build from the newest cached raw files
  --out PATH     index file to write (default build-cache/instruments.v1.json)
  --with-xetra   opt-in described above (private builds only)
  --no-openfigi  do not look up Xetra tickers (index without most tickers)
  --no-wikidata  do not add Nasdaq / NYSE tickers
  --no-xetra-fields  accepted for compatibility; it is the default now
  --verify       do not fetch or build: run the lookup verification report against the existing index (--out)

Memory: the ESMA XML files (up to ~1 GB uncompressed) are read as a stream (iterparse); peak memory stays well below
1 GB. Runtime: about 1 to 2 minutes for ESMA, plus about 20 minutes for the first OpenFIGI run (25 requests per minute, 10 ISINs each,
cached afterwards: later runs only look up new ISINs). Exit codes: 0 ok, 1 error. Stdlib only, Python 3.8+.
"""
import argparse
import csv
import gzip
import importlib.util
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "build-cache"
RAW = CACHE / "raw"
DEFAULT_OUT = CACHE / "instruments.v1.json"

USER_AGENT = "finplanr-build/1.0 (static-site build tool; reads public reference data once per build)"
TIMEOUT = 60
RETRIES = 3
SIZE_BUDGET_GZ = 4 * 1024 * 1024
XETRA_MAX_AGE_S = 12 * 3600
FIGI_URL = "https://api.openfigi.com/v3/mapping"
FIGI_BATCH = 10            # jobs per request without an API key
FIGI_GAP_S = 2.6           # 25 requests per minute without an API key
FIGI_TTL_DAYS = 30
FIGI_CACHE = "openfigi-xetr-tickers.json"
FIGI_US_CACHE = "openfigi-us-composite.json"
WD_SPARQL = "https://query.wikidata.org/sparql"
WD_CACHE = "wikidata-us-tickers.csv"
WD_TTL_S = 7 * 24 * 3600
WD_EXCHANGES = {"Q82059": "XNAS", "Q13677": "XNYS"}  # Wikidata items "Nasdaq", "New York Stock Exchange"
TICKER_RE = re.compile(r"[A-Z0-9.\-]{1,12}")
XETRA_TICKER_RE = re.compile(r"[A-Z0-9]{3,4}")  # Xetra mnemonics are always 3 or 4 characters; longer Bloomberg tickers (ETFDAX, CG1GR ...) are not Xetra symbols

ESMA_SOLR = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select"
ESMA_TYPES = ("C", "D", "E")
ESMA_HOST = "firds.esma.europa.eu"
DB_HOST = "www.cashmarket.deutsche-boerse.com"
DB_PAGE_XETRA = "https://www.cashmarket.deutsche-boerse.com/cash-en/trading/Tradable-Instruments-Xetra/Downloads/xetra-downloads"
DB_PAGE_FRA = "https://www.cashmarket.deutsche-boerse.com/cash-en/trading/Tradable-Instruments-Xetra/Downloads/frankfurt-downloads"
DB_LINK_XETRA = re.compile(r"(?:https://www\.cashmarket\.deutsche-boerse\.com)?/resource/blob/\d+/[0-9a-f]+/data/t7-xetr-allTradableInstruments\.csv")
DB_LINK_FRA = re.compile(r"(?:https://www\.cashmarket\.deutsche-boerse\.com)?/resource/blob/\d+/[0-9a-f]+/data/t7-xfra-BF-allTradableInstruments\.zip")

# ---------------------------------------------------------------------------- venues
# ESMA reports segment MICs (e.g. FRAA, FRAB, STUB, XETA). They are rolled up to one code per exchange / platform that
# a German retail user can reach. Anything not listed here is dropped (dark pools, RFQ platforms, systematic
# internalisers, derivatives venues ...); an instrument without any kept venue is not indexed from ESMA.
ROLLUP = {}


def _roll(code, *mics):
    for m in (code,) + mics:
        ROLLUP[m] = code


_roll("XETR", "XETA", "XEMA", "XETU", "XETB", "XETV", "XETS", "XETW", "XEMI", "XEMB")
_roll("XFRA", "FRAA", "FRAB", "FRAU", "FRAV", "FRAS", "FRAW")
_roll("XSTU", "STUA", "STUB", "STUC", "STUD", "STUE", "STUF", "STUH", "STUJ", "EUWX", "XSTP", "XSTF", "XCTS")
_roll("XBER", "BERA", "BERB", "BERC", "EQTA", "EQTB", "EQTC", "XEQT")
_roll("XDUS", "DUSA", "DUSB", "DUSC", "DUSD", "XQTX")
_roll("XHAM", "HAMA", "HAMB", "HAMO", "HAMP", "HAMQ", "HAMX", "HAMY", "HAMZ")
_roll("HAMN", "HAMM")
_roll("XHAN", "HANA", "HANB", "HANC", "HAND", "HANE")
_roll("XMUN", "MUNA", "MUNB")
_roll("MUND", "MUNC")
_roll("XGAT", "TGAT", "XGRM")
_roll("XAMS", "XAMC")
_roll("XPAR")
_roll("XBRU")
_roll("XLIS")
_roll("XMIL", "ETFP", "MTAA", "MTAH", "BGEM", "EXGM", "MIVX")
_roll("XMAD")
_roll("XWBO", "XVIE", "WBAH", "WBDM")
_roll("XMSM", "XDUB")
_roll("XLUX", "EMTF")
_roll("XSTO")
_roll("XHEL")
_roll("XCSE")
_roll("XOSL")
_roll("XSWX")
_roll("XLON")

VENUE_NAMES = {
    "XETR": "Xetra", "XFRA": "Börse Frankfurt", "XSTU": "Börse Stuttgart", "XBER": "Börse Berlin",
    "XDUS": "Börse Düsseldorf", "XHAM": "Börse Hamburg", "HAMN": "Lang & Schwarz Exchange", "XHAN": "Börse Hannover",
    "XMUN": "Börse München", "MUND": "gettex", "XGAT": "Tradegate", "XAMS": "Euronext Amsterdam",
    "XPAR": "Euronext Paris", "XBRU": "Euronext Brussels", "XLIS": "Euronext Lisbon", "XMIL": "Borsa Italiana",
    "XMAD": "Bolsa de Madrid", "XWBO": "Wiener Börse", "XMSM": "Euronext Dublin", "XLUX": "Luxembourg Stock Exchange",
    "XSTO": "Nasdaq Stockholm", "XHEL": "Nasdaq Helsinki", "XCSE": "Nasdaq Copenhagen", "XOSL": "Oslo Børs",
    "XSWX": "SIX Swiss Exchange", "XLON": "London Stock Exchange", "XNAS": "Nasdaq", "XNYS": "NYSE",
}
VENUE_ORDER = list(VENUE_NAMES)  # German venues first, Xetra first of all

# ---------------------------------------------------------------------------- types
TYPE_PRIO = {"E": 0, "C": 1, "S": 2, "F": 3, "O": 4}
XTYPE = {"ETF": "E", "ETC": "C", "ETN": "C", "CS": "S", "FUN": "F"}  # Deutsche Boerse "Instrument Type" -> our type
ETP_NAME_RE = re.compile(r"\bET[CNP]s?\b|\bETC\s?S\b|Exchange[- ]Traded (?:Note|Commodit|Product)", re.I)
ETP_CFI2 = {"DA", "DE", "DT", "DM", "DS"}  # asset-backed, structured (with/without capital protection), medium-term notes, other
STOCK_CFI2 = {"ES", "EP", "EC", "ER", "ED", "EU", "EL"}  # shares, preferred, convertible, depositary receipts, units, LP interests


def is_etp_candidate(cfi, name):
    """Debt-file record that looks like an ETC/ETN/ETP: structured/asset-backed CFI (not plain bonds, which can carry
    a ticker such as 'ETN' in their name) and an ETC/ETN/ETP word in the name."""
    return (cfi or "")[:2] in ETP_CFI2 and bool(ETP_NAME_RE.search(name or ""))


def type_from_cfi(file_letter, cfi, name):
    """ESMA classification (CFI code, ISO 10962) -> index type, or None when the instrument is not indexed."""
    c2 = (cfi or "")[:2]
    if file_letter == "C":
        if c2 == "CE":
            return "E"  # exchange-traded funds
        if c2 == "CB":
            return "S"  # real estate investment trusts: traded like shares
        return "F"
    if file_letter == "E":
        return "S" if c2 in STOCK_CFI2 else None  # EY (structured participation certificates) etc. are not indexed
    if file_letter == "D":
        return "C" if is_etp_candidate(cfi, name) else None
    return None


# ---------------------------------------------------------------------------- small helpers
def log(msg=""):
    print(msg, flush=True)


def fmt_mb(n):
    return "%.1f MB" % (n / 1048576.0)


def isin_ok(s):
    """ISO 6166 check digit (Luhn over the letter-expanded digits)."""
    if not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}[0-9]", s or ""):
        return False
    digits = "".join(str(int(ch, 36)) for ch in s)
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def clean_name(s):
    s = re.sub(r"[\u200b-\u200f\u2060\ufeff]", "", s or "")  # zero-width characters
    s = re.sub(r"[\s\xa0]+", " ", s).strip()
    return s[:120].rstrip()


TIDY_SUFFIX = re.compile(r"\s+(?:(?:Registered|Reg\.?)\s?(?:Shares?|Shs\.?)|Inhaber-?(?:Aktien|Anteile)|Namens-?(?:Aktien|Anteile)|Bearer Shares?|Stammaktien)?\s*\bo\.?N\.?$", re.I)


def tidy_name(n):
    """Drop the German exchange boilerplate at the very end ('... Registered Shares o.N.'); legal suffixes stay."""
    t = TIDY_SUFFIX.sub("", n).strip()
    return t if len(t) >= 3 else n


def norm_wkn(w):
    w = (w or "").strip().upper()
    if len(w) == 9 and w.startswith("000"):
        w = w[3:]  # Deutsche Boerse pads the 6-character WKN with three zeros
    return w if re.fullmatch(r"[A-Z0-9]{6}", w) else ""


def derive_wkn(isin):
    # German ISIN: DE + 000 + 6-character WKN + check digit
    return isin[5:11] if isin.startswith("DE000") and re.fullmatch(r"[A-Z0-9]{6}", isin[5:11]) else ""


# ---------------------------------------------------------------------------- download
def http_get(url, dest=None, timeout=TIMEOUT, retries=RETRIES, label=None):
    """GET with retries; bytes or, with dest, streamed to that file (via a .part file). https only."""
    if urllib.parse.urlsplit(url).scheme != "https":
        raise ValueError("refusing non-https URL: " + url)
    last = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if dest is None:
                    return r.read()
                total = int(r.headers.get("Content-Length") or 0)
                part = Path(str(dest) + ".part")
                got, shown = 0, 0
                with open(part, "wb") as f:
                    while True:
                        chunk = r.read(1 << 20)
                        if not chunk:
                            break
                        f.write(chunk)
                        got += len(chunk)
                        if total and got * 5 // total > shown and got < total:
                            shown = got * 5 // total
                            log("    %s %d%%" % (label or Path(dest).name, shown * 20))
                if total and got != total:
                    raise IOError("short read %d of %d bytes" % (got, total))
                part.replace(dest)
                return got
        except (urllib.error.URLError, OSError, ValueError) as e:
            last = e
            if attempt < retries:
                log("    retry %d/%d after error: %s" % (attempt, retries - 1, e))
                time.sleep(2 * attempt)
    raise RuntimeError("download failed: %s (%s)" % (url, last))


# ---------------------------------------------------------------------------- ESMA FIRDS
FNAME_RE = re.compile(r"^FULINS_([A-Z])_(\d{8})_(\d+)of(\d+)\.zip$")


def esma_remote_sets():
    since = (date.today() - timedelta(days=28)).isoformat()
    params = {"q": "file_type:FULINS", "fq": "publication_date:[%sT00:00:00Z TO NOW]" % since, "wt": "json",
              "rows": "1000", "sort": "publication_date desc", "fl": "file_name,download_link"}
    data = json.loads(http_get(ESMA_SOLR + "?" + urllib.parse.urlencode(params)).decode("utf-8"))
    parts = defaultdict(dict)  # (letter, yyyymmdd) -> {file_name: url}
    for d in data["response"]["docs"]:
        m = FNAME_RE.match(d.get("file_name", ""))
        url = d.get("download_link", "")
        if not m or urllib.parse.urlsplit(url).hostname != ESMA_HOST or not url.startswith("https://"):
            continue
        parts[(m.group(1), m.group(2))][d["file_name"]] = (url, int(m.group(4)))
    chosen = {}
    for letter in ESMA_TYPES:
        days = sorted((k[1] for k in parts if k[0] == letter and len(parts[k]) == next(iter(parts[k].values()))[1]), reverse=True)
        if not days:
            raise RuntimeError("no complete FULINS_%s file set in the ESMA listing" % letter)
        chosen[letter] = (days[0], {n: v[0] for n, v in sorted(parts[(letter, days[0])].items())})
    return chosen


def esma_cached_sets():
    found = defaultdict(dict)
    for p in RAW.glob("FULINS_*.zip"):
        m = FNAME_RE.match(p.name)
        if m:
            found[(m.group(1), m.group(2))][p.name] = (p, int(m.group(4)))
    chosen = {}
    for letter in ESMA_TYPES:
        days = sorted((k[1] for k in found if k[0] == letter and len(found[k]) == next(iter(found[k].values()))[1]), reverse=True)
        if not days:
            raise RuntimeError("offline: no complete cached FULINS_%s file set in %s" % (letter, RAW))
        chosen[letter] = (days[0], {n: v[0] for n, v in sorted(found[(letter, days[0])].items())})
    return chosen


def esma_get(refresh, offline):
    """Return {letter: (yyyymmdd, [zip paths])} for the newest complete FULINS sets, downloading what is missing."""
    RAW.mkdir(parents=True, exist_ok=True)
    if offline:
        sets = esma_cached_sets()
        return {k: (v[0], list(v[1].values())) for k, v in sets.items()}
    try:
        sets = esma_remote_sets()
    except Exception as e:  # listing unavailable: fall back to the cache if it is complete
        log("  ESMA listing failed (%s); trying the cache" % e)
        sets = esma_cached_sets()
        return {k: (v[0], list(v[1].values())) for k, v in sets.items()}
    result = {}
    for letter, (day, files) in sets.items():
        paths = []
        for name, url in files.items():
            dest = RAW / name
            if dest.exists() and not refresh and zipfile.is_zipfile(dest):
                log("  cached   %s" % name)
            else:
                t0 = time.time()
                log("  download %s" % name)
                n = http_get(url, dest)
                log("    %s in %.1fs" % (fmt_mb(n), time.time() - t0))
            paths.append(dest)
        result[letter] = (day, paths)
    keep = {p.name for v in result.values() for p in v[1]}
    for p in RAW.glob("FULINS_*.zip"):
        if p.name not in keep:
            p.unlink()
            log("  removed old cache file %s" % p.name)
    return result


def iter_firds(path, today_iso):
    """Stream (isin, full_name, cfi, notional_ccy, venue_mic) of the instrument/venue records that are not terminated."""
    with zipfile.ZipFile(path) as z, z.open(z.namelist()[0]) as f:
        holder = None
        n = 0
        for ev, el in ET.iterparse(f, events=("start", "end")):
            if ev == "start":
                if holder is None and el.tag.endswith("}FinInstrmRptgRefDataRpt"):
                    holder = el  # parent of the records: emptied periodically so processed records are freed
                continue
            if not el.tag.endswith("}RefData"):
                continue
            ns = el.tag[: el.tag.index("}") + 1]
            g = el.find(ns + "FinInstrmGnlAttrbts")
            v = el.find(ns + "TradgVnRltdAttrbts")
            if g is not None and v is not None:
                term = v.findtext(ns + "TermntnDt")
                if not term or term[:4] == "9999" or term[:10] >= today_iso:
                    yield (g.findtext(ns + "Id") or "", g.findtext(ns + "FullNm") or "", g.findtext(ns + "ClssfctnTp") or "",
                           g.findtext(ns + "NtnlCcy") or "", v.findtext(ns + "Id") or "")
            el.clear()
            n += 1
            if holder is not None and n % 20000 == 0:
                del holder[:]


# ---------------------------------------------------------------------------- Deutsche Boerse files
def parse_db_csv(raw_bytes):
    """-> (date_iso, [row dict]) for a Deutsche Boerse 'All tradable instruments' CSV (';' separated, 2 header lines)."""
    text = io.TextIOWrapper(io.BytesIO(raw_bytes), encoding="utf-8", errors="replace", newline="")
    lines = text.read().splitlines()
    d = ""
    for ln in lines[:3]:
        m = re.search(r"Date Last Update:;(\d\d)\.(\d\d)\.(\d{4})", ln)
        if m:
            d = "%s-%s-%s" % (m.group(3), m.group(2), m.group(1))
    start = next((i for i, ln in enumerate(lines[:6]) if ln.startswith("Product Status;")), None)
    if start is None:
        raise ValueError("unexpected CSV layout (header row not found)")
    rd = csv.reader(lines[start:], delimiter=";")
    head = next(rd)
    want = ["Instrument Status", "Instrument", "ISIN", "WKN", "Mnemonic", "Instrument Type", "Settlement Currency"]
    idx = {k: head.index(k) for k in want}
    rows = []
    for r in rd:
        if len(r) >= len(head) - 1 and r:
            rows.append({k: (r[i] if i < len(r) else "") for k, i in idx.items()})
    return d, rows


def read_db_file(path):
    b = Path(path).read_bytes()
    if b[:2] == b"PK":
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            b = z.read(z.namelist()[0])
    return parse_db_csv(b)


def db_get(label, page_url, link_re, prefix, suffix, refresh, offline):
    """Newest cached or freshly downloaded Deutsche Boerse file -> (date_iso, rows) or (None, None)."""
    RAW.mkdir(parents=True, exist_ok=True)
    cached = sorted(RAW.glob("%s_????-??-??%s" % (prefix, suffix)))
    fresh = cached and (time.time() - cached[-1].stat().st_mtime) < XETRA_MAX_AGE_S
    if offline or (fresh and not refresh):
        if not cached:
            log("  %s: no cached file (offline); skipped" % label)
            return None, None
        log("  cached   %s" % cached[-1].name)
        return read_db_file(cached[-1])
    try:
        html = http_get(page_url).decode("utf-8", "replace")
        links = sorted({urllib.parse.urljoin("https://" + DB_HOST + "/", u) for u in link_re.findall(html)})  # the page serves absolute or relative links
        if not links:
            raise RuntimeError("download link not found on %s" % page_url)
        tmp = RAW / (prefix + "_download" + suffix)
        t0 = time.time()
        log("  download %s" % links[0].rsplit("/", 1)[1])
        n = http_get(links[0], tmp)
        d, rows = read_db_file(tmp)
        if not d or len(rows) < 1000:
            raise RuntimeError("file looks incomplete (%d rows)" % len(rows))
        dest = RAW / ("%s_%s%s" % (prefix, d, suffix))
        tmp.replace(dest)
        for old in RAW.glob("%s_????-??-??%s" % (prefix, suffix)):
            if old != dest:
                old.unlink()
        log("    %s in %.1fs, data date %s, %d rows" % (fmt_mb(n), time.time() - t0, d, len(rows)))
        return d, rows
    except Exception as e:
        if cached:
            log("  %s: download failed (%s); using cached %s" % (label, e, cached[-1].name))
            return read_db_file(cached[-1])
        log("  %s: download failed (%s); skipped" % (label, e))
        return None, None


# ---------------------------------------------------------------------------- open ticker sources (default)
def figi_post(jobs):
    """One OpenFIGI mapping request (list of jobs) -> list of results. Waits and retries on rate limits / server errors."""
    body = json.dumps(jobs).encode("utf-8")
    last = None
    for attempt in range(1, 6):
        try:
            req = urllib.request.Request(FIGI_URL, data=body, headers={
                "User-Agent": USER_AGENT, "Content-Type": "application/json", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last = e
            wait = 65 if e.code == 429 else 5 * attempt
            if e.code == 429:
                try:
                    wait = int(e.headers.get("ratelimit-reset") or e.headers.get("Retry-After") or 65) + 2
                except ValueError:
                    pass
            if e.code not in (429, 500, 502, 503, 504):
                raise RuntimeError("OpenFIGI HTTP %d" % e.code)
            log("    OpenFIGI HTTP %d, waiting %d s" % (e.code, wait))
            time.sleep(wait)
        except (urllib.error.URLError, OSError, ValueError) as e:
            last = e
            time.sleep(5 * attempt)
    raise RuntimeError("OpenFIGI request failed: %s" % last)


def figi_cached_lookup(isins, job_for, cache_name, refresh, offline, today_iso, label):
    """Run OpenFIGI mapping jobs for the ISINs that are not in the cache (or older than FIGI_TTL_DAYS) and return
    ({isin: sorted list of tickers}, newest answer date). Answers (also "nothing found") are cached in build-cache/raw."""
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / cache_name
    cache = {}
    if path.is_file():
        try:
            cache = json.loads(path.read_text(encoding="utf-8")).get("t", {})
            for k, v in list(cache.items()):  # format 1 stored one ticker string, format 2 a list
                if isinstance(v[0], str):
                    cache[k] = [[v[0]] if v[0] else [], v[1]]
        except (OSError, ValueError, TypeError, IndexError):
            cache = {}
    limit = (date.today() - timedelta(days=FIGI_TTL_DAYS)).isoformat()
    todo = [i for i in isins if i not in cache or cache[i][1] < limit]
    log("  OpenFIGI %s: %d ISINs wanted, %d cached and fresh, %d to look up%s" % (
        label, len(isins), len(isins) - len(todo), len(todo), " (offline: skipped)" if offline and todo else ""))

    def save():
        tmp = Path(str(path) + ".tmp")
        tmp.write_text(json.dumps({"v": 2, "t": cache}, separators=(",", ":")), encoding="utf-8")
        tmp.replace(path)

    if todo and not offline:
        t0 = time.time()
        reqs = (len(todo) + FIGI_BATCH - 1) // FIGI_BATCH
        log("    about %d requests, roughly %d minutes (free API without key: 25 requests per minute)" % (reqs, int(reqs * FIGI_GAP_S / 60) + 1))
        try:
            for n in range(reqs):
                chunk = todo[n * FIGI_BATCH:(n + 1) * FIGI_BATCH]
                res = figi_post([job_for(i) for i in chunk])
                if not isinstance(res, list) or len(res) != len(chunk):
                    raise RuntimeError("OpenFIGI answered with an unexpected shape")
                for isin, r in zip(chunk, res):
                    ticks = sorted({str(d.get("ticker") or "").strip().upper() for d in r.get("data", []) if isinstance(d, dict)} - {""})
                    cache[isin] = [ticks, today_iso]
                if (n + 1) % 25 == 0 or n + 1 == reqs:
                    save()
                    log("    %d/%d requests, %d min elapsed" % (n + 1, reqs, (time.time() - t0) / 60))
                time.sleep(FIGI_GAP_S)
        except RuntimeError as e:
            log("  OpenFIGI stopped early (%s); using what is cached" % e)
            save()
    got = {i: cache[i][0] for i in isins if i in cache}
    return got, max([cache[i][1] for i in got] or [None])


def figi_tickers(isins, refresh, offline, today_iso):
    """({isin: ticker or ""}, newest answer date): the ticker on Xetra (MIC XETR); "" when there is none or it is ambiguous."""
    got, d = figi_cached_lookup(isins, lambda i: {"idType": "ID_ISIN", "idValue": i, "micCode": "XETR"},
                                FIGI_CACHE, refresh, offline, today_iso, "Xetra tickers")
    return {i: (t[0] if len(t) == 1 else "") for i, t in got.items()}, d


def figi_us_composite(isins, refresh, offline, today_iso):
    """{isin: [tickers]} on the US composite listing: used to confirm Wikidata tickers (Wikidata statements can be stale)."""
    return figi_cached_lookup(isins, lambda i: {"idType": "ID_ISIN", "idValue": i, "exchCode": "US"},
                              FIGI_US_CACHE, refresh, offline, today_iso, "US tickers (check of Wikidata)")[0]


WD_QUERY = """SELECT ?isin ?ex ?t (COUNT(DISTINCT ?isin2) AS ?nisin) WHERE {
  VALUES ?ex { %s }
  ?i p:P946 ?is. ?is ps:P946 ?isin. FILTER NOT EXISTS { ?is wikibase:rank wikibase:DeprecatedRank } FILTER(STRSTARTS(?isin, "US"))
  ?i wdt:P946 ?isin2.
  ?i p:P414 ?e. ?e ps:P414 ?ex. ?e pq:P249 ?t. ?e wikibase:rank ?rk. FILTER(?rk != wikibase:DeprecatedRank)
  FILTER NOT EXISTS { ?e pq:P582 [] }
} GROUP BY ?isin ?ex ?t""" % " ".join("wd:" + q for q in WD_EXCHANGES)


def wikidata_tickers(refresh, offline):
    """{isin: (ticker, MIC)} for US ISINs listed on NYSE or Nasdaq according to Wikidata (CC0). Only unambiguous cases: one
    ticker per ISIN, and the Wikidata item carries exactly one ISIN (so the ticker cannot belong to another share class)."""
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / WD_CACHE
    fresh = path.is_file() and time.time() - path.stat().st_mtime < WD_TTL_S
    if not offline and (refresh or not fresh):
        try:
            url = WD_SPARQL + "?" + urllib.parse.urlencode({"query": WD_QUERY})
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/csv"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            if data.count(b"\n") < 500:
                raise RuntimeError("Wikidata answer too small (%d lines)" % data.count(b"\n"))
            tmp = Path(str(path) + ".tmp")
            tmp.write_bytes(data)
            tmp.replace(path)
        except Exception as e:
            log("  Wikidata query failed (%s); %s" % (e, "using the cached answer" if path.is_file() else "no Wikidata tickers"))
    if not path.is_file():
        return {}
    cand = defaultdict(set)
    for r in csv.DictReader(io.StringIO(path.read_text(encoding="utf-8"))):
        mic = WD_EXCHANGES.get((r.get("ex") or "").rsplit("/", 1)[-1])
        t = (r.get("t") or "").strip().upper()
        if mic and TICKER_RE.fullmatch(t) and r.get("nisin") == "1" and isin_ok(r.get("isin") or ""):
            cand[r["isin"]].add((t, mic))
    return {i: next(iter(v)) for i, v in cand.items() if len(v) == 1}


# ---------------------------------------------------------------------------- name choice
BAD_NAME = re.compile(r"\b(?:o\.?N\.?|oN)\b|Reg\.?\s?Shs|Registered Shs|\(unl|O\.?END|\bZ ?\d\d\b|\bCMN\b|CLASS ETF|PUBLIC LIMITED|\bPLC\s*[-\u2013]|SHS CL|/|\bNAMENS|\bINH\.?\b|Inhaber", re.I)
SHARE_BOILERPLATE = re.compile(r"Registered|\bReg\.? ?Sh|Inhaber|Namens|Stamm|Vorzug|\bAktien\b|\bDL\b|\bEO\b|\bDL ?-|\bEO ?-|\bCl\.|\bClass\b|\bShares?\b|\bo\.?N\b|\bNew\b|\bUnits?\b|\bOrd\b", re.I)
ODD_CASE = re.compile(r"Ucits|\bEtf\b|\bEtc\b|\bEtn\b")
ABBREV = re.compile(r"\b[A-Za-z]{1,4}\.[A-Za-z]")
VENUE_NAME_BONUS = {"STUB": 2, "STUD": 2, "STUF": 2, "XAMS": 1, "XPAR": 1, "ETFP": 1, "XETA": 0.5, "XETR": 0.5}


def name_score(n, cnt, bonus, typ="E"):
    letters = [c for c in n if c.isalpha()]
    if not letters:
        return -999.0
    s = 0.0
    if sum(c.isupper() for c in letters) / len(letters) > 0.9:
        s -= 25  # ALL CAPS
    if BAD_NAME.search(n):
        s -= 30  # German exchange abbreviation style ("o.N.", "Reg.Shs", "O.END Z 24(unl.)")
    if ODD_CASE.search(n):
        s -= 15
    if ABBREV.search(n):
        s -= 8
    L = len(n)
    if typ == "S":
        if SHARE_BOILERPLATE.search(n):
            s -= 20  # "Registered Shares DL-,001", "Inhaber-Aktien o.N.": share class details instead of the company name
        s -= L / 15.0  # for companies the plain name is the best one
    else:
        s += min(L, 70) / 5.0  # for funds/ETPs the more descriptive name wins (acc/dist, hedging ...)
    if L > 85:
        s -= (L - 85) / 2.0
    return s + cnt * 1.5 + bonus


def best_name(cands, typ="E"):
    """cands: {name: [count, bonus]} -> most descriptive well-formed name."""
    best, best_s = "", -1e9
    for n, (cnt, bonus) in cands.items():
        s = name_score(n, cnt, bonus, typ)
        if s > best_s or (s == best_s and (len(n), n) > (len(best), best)):
            best, best_s = n, s
    return best


# ---------------------------------------------------------------------------- build
def build(args):
    today = date.today()
    today_iso = today.isoformat()
    t_start = time.time()
    if not args.with_xetra:
        # nothing from the Deutsche Boerse files is used: do not keep old copies of them around either
        for old in list(RAW.glob("xetra_????-??-??.csv")) + list(RAW.glob("xfra-bf_????-??-??.zip")):
            old.unlink()
            log("  removed %s (Deutsche Boerse files are only used with --with-xetra)" % old.name)
    log("== ESMA FIRDS full files")
    esma = esma_get(args.refresh, args.offline)
    esma_day = min(v[0] for v in esma.values())
    esma_date = "%s-%s-%s" % (esma_day[:4], esma_day[4:6], esma_day[6:])

    x_date = bf_date = None
    xrows = bfrows = None
    if args.with_xetra:
        log("== Deutsche Boerse tradable instruments (--with-xetra: PRIVATE build, do not publish without a licence)")
        x_date, xrows = db_get("Xetra", DB_PAGE_XETRA, DB_LINK_XETRA, "xetra", ".csv", args.refresh, args.offline)
        bf_date, bfrows = db_get("Frankfurt", DB_PAGE_FRA, DB_LINK_FRA, "xfra-bf", ".zip", args.refresh, args.offline)

    # --- Deutsche Boerse side: type, WKN, ticker, trading currency, listing flags
    xt = {}      # isin -> dict(type, wkn, ticker, ccy, name, xetra, fra)
    skipped_status = Counter()
    for venue, rows in (("XETR", xrows), ("XFRA", bfrows)):
        for r in rows or []:
            isin = r["ISIN"].strip().upper()
            t = XTYPE.get(r["Instrument Type"].strip().upper())
            if t is None:
                continue
            if r["Instrument Status"] != "Active":
                skipped_status[r["Instrument Status"]] += 1
                continue
            e = xt.setdefault(isin, {"type": t, "wkn": "", "ticker": "", "ccy": "", "name": "", "XETR": False, "XFRA": False})
            e[venue] = True
            if venue == "XETR" or not e["name"]:
                e["name"] = clean_name(r["Instrument"])
            if not e["wkn"]:
                e["wkn"] = norm_wkn(r["WKN"])
            if venue == "XETR":
                e["type"] = t  # Xetra classification wins over Frankfurt
                e["ticker"] = re.sub(r"[^A-Z0-9.\-]", "", r["Mnemonic"].strip().upper())
                e["ccy"] = r["Settlement Currency"].strip().upper()
            elif not e["ccy"]:
                e["ccy"] = r["Settlement Currency"].strip().upper()
    log("  Deutsche Boerse side: %d ISINs (Xetra %d, Frankfurt %d)" % (
        len(xt), sum(1 for e in xt.values() if e["XETR"]), sum(1 for e in xt.values() if e["XFRA"])))

    # --- ESMA side
    info = {}  # isin -> {"type","ccy","venues":set,"names":{n:[cnt,bonus]}}
    stats = Counter()

    def add(isin, name, mic, typ, ccy):
        v = ROLLUP.get(mic)
        if v is None:
            stats["venue_dropped"] += 1
            return
        e = info.get(isin)
        if e is None:
            e = info[isin] = {"type": typ, "ccy": ccy, "venues": set(), "names": {}}
        e["venues"].add(v)
        nm = clean_name(name)
        if nm:
            c = e["names"].get(nm)
            if c:
                c[0] += 1
            elif len(e["names"]) < 12:
                e["names"][nm] = [1, VENUE_NAME_BONUS.get(mic, 0)]

    def isin_type(letter, isin, cfi, name):
        if isin in xt:
            return xt[isin]["type"]
        return type_from_cfi(letter, cfi, name)

    log("== Parsing ESMA files (streaming)")
    for letter in ESMA_TYPES:
        day, paths = esma[letter]
        etp_isins = set()
        if letter in ("D", "E"):
            # pass 1: which debt-file ISINs are ETC/ETN/ETP products (decided per ISIN, because venue names differ).
            # In the equity file the crypto/commodity ETPs sit under CFI "EY" (structured participation certificates).
            t0 = time.time()
            for p in paths:
                for isin, name, cfi, ccy, mic in iter_firds(p, today_iso):
                    if letter == "D":
                        if isin in xt or is_etp_candidate(cfi, name):
                            etp_isins.add(isin)
                    elif cfi[:2] == "EY" and ETP_NAME_RE.search(name):
                        etp_isins.add(isin)
            log("  FULINS_%s pass 1: %d ETC/ETN/ETP candidate ISINs (%.0fs)" % (letter, len(etp_isins), time.time() - t0))
        t0 = time.time()
        n = 0
        for p in paths:
            for isin, name, cfi, ccy, mic in iter_firds(p, today_iso):
                n += 1
                if letter == "D":
                    if isin not in etp_isins:
                        continue
                    typ = xt[isin]["type"] if isin in xt else "C"
                else:
                    typ = isin_type(letter, isin, cfi, name)
                    if typ is None and isin in etp_isins:
                        typ = "C"
                    if typ is None:
                        continue
                add(isin, name, mic, typ, ccy)
        log("  FULINS_%s %s: %d venue records read, %d ISINs kept so far (%.0fs)" % (letter, day, n, len(info), time.time() - t0))

    # --- merge into rows
    rows, dropped_invalid = [], 0
    ids = set(info) | set(xt)
    for isin in ids:
        if not isin_ok(isin):
            dropped_invalid += 1
            continue
        e = info.get(isin)
        x = xt.get(isin)
        if e is None and x is None:
            continue
        typ = x["type"] if x else e["type"]
        venues = set(e["venues"]) if e else set()
        if x:
            for k in ("XETR", "XFRA"):
                if x[k]:
                    venues.add(k)
        if not venues:
            continue
        name = best_name(e["names"], typ) if e and e["names"] else ""
        if not name and x:
            name = x["name"]
        if not name:
            continue
        ccy = (x["ccy"] if x and x["ccy"] else "") or (e["ccy"] if e and typ == "S" else "")
        if not re.fullmatch(r"[A-Z]{3}", ccy or ""):
            ccy = ""
        wkn = (x["wkn"] if x else "") or derive_wkn(isin)
        ticker = x["ticker"] if x and x["XETR"] else ""
        rows.append([isin, tidy_name(name), wkn, ticker, typ, ccy, venues])
    log("  %d rows (%d ISINs with invalid check digit dropped)" % (len(rows), dropped_invalid))

    # --- open ticker sources: OpenFIGI (Xetra) and Wikidata (US stocks on NYSE / Nasdaq)
    used = {"openfigi": 0, "wikidata": 0}
    skipped_long = 0
    fig_date = wd_date = None
    if not args.no_openfigi:
        log("== OpenFIGI: Xetra tickers")
        skipped_long = 0
        want = sorted(r[0] for r in rows if "XETR" in r[6] and not r[3])
        got, fig_date = figi_tickers(want, args.refresh, args.offline, today_iso)
        byi = {r[0]: r for r in rows}
        for isin, t in got.items():
            if XETRA_TICKER_RE.fullmatch(t):
                byi[isin][3] = t
                used["openfigi"] += 1
            elif t:
                skipped_long += 1
    if not args.no_wikidata:
        log("== Wikidata (CC0): ticker of US stocks on NYSE / Nasdaq")
        wd = wikidata_tickers(args.refresh, args.offline)
        cand = [r for r in rows if r[4] == "S" and not r[3] and "XETR" not in r[6] and r[0] in wd]
        if args.no_openfigi:
            confirmed = None
        else:
            confirmed = figi_us_composite(sorted(r[0] for r in cand), args.refresh, args.offline, today_iso)
        dropped_stale = 0
        for r in cand:
            t, mic = wd[r[0]]
            if confirmed is not None and t not in confirmed.get(r[0], []):
                dropped_stale += 1  # Wikidata ticker not (or no longer) the US ticker of this ISIN at OpenFIGI: stale, not used
                continue
            r[3] = t
            r[6] = r[6] | {mic}
            used["wikidata"] += 1
        log("  Wikidata candidates %d, %d dropped because OpenFIGI does not confirm the ticker" % (len(cand), dropped_stale))
        if used["wikidata"]:
            wd_date = datetime.fromtimestamp((RAW / WD_CACHE).stat().st_mtime).date().isoformat()  # local date, like "built"
    log("  tickers added: OpenFIGI %d (%d longer than 4 characters ignored), Wikidata %d" % (used["openfigi"], skipped_long, used["wikidata"]))
    for r in rows:
        r[6] = " ".join(sorted(r[6], key=VENUE_ORDER.index))
    rows.sort(key=lambda r: (TYPE_PRIO[r[4]], r[1].casefold(), r[0]))

    # --- size budget: drop stocks that only trade on small venues if the gzip size is over budget
    extra = {"xetra": max([d for d in (x_date, bf_date) if d] or [None]), "openfigi": fig_date if used["openfigi"] else None,
             "wikidata": wd_date if used["wikidata"] else None}
    index = make_index(rows, esma_date, extra, today_iso)
    plain, gz = encode(index)
    if len(gz) > SIZE_BUDGET_GZ:
        log("  over the size budget (%s gz): dropping stocks without a German-venue listing" % fmt_mb(len(gz)))
        german = {"XETR", "XFRA", "XSTU", "XBER", "XDUS", "XHAM", "HAMN", "XHAN", "XMUN", "MUND", "XGAT"}
        rows = [r for r in rows if r[4] != "S" or german & set(r[6].split())]
        index = make_index(rows, esma_date, extra, today_iso)
        plain, gz = encode(index)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(out) + ".tmp")
    tmp.write_bytes(plain)
    tmp.replace(out)

    # --- summary
    cnt = Counter(r[4] for r in rows)
    raw_total = sum(p.stat().st_size for p in RAW.glob("*") if p.is_file())
    log("")
    log("== Summary")
    log("  index         %s" % out)
    log("  rows          %d  (ETF %d, ETC/ETN %d, stocks %d, other funds %d, other %d)" % (
        len(rows), cnt["E"], cnt["C"], cnt["S"], cnt["F"], cnt["O"]))
    log("  size          %s plain, %s gzip (budget %s)" % (fmt_mb(len(plain)), fmt_mb(len(gz)), fmt_mb(SIZE_BUDGET_GZ)))
    log("  raw cache     %s in %s" % (fmt_mb(raw_total), RAW))
    log("  data dates    ESMA FIRDS %s; OpenFIGI %s; Wikidata %s; Deutsche Boerse (--with-xetra) %s" % (
        esma_date, extra["openfigi"] or "-", extra["wikidata"] or "-", extra["xetra"] or "-"))
    log("  with WKN %d, with ticker %d" % (sum(1 for r in rows if r[2]), sum(1 for r in rows if r[3])))
    log("  runtime       %.0f s" % (time.time() - t_start))
    validate_with_tool(out)
    return 0


def de_date(d):
    return "%s.%s.%s" % (d[8:10], d[5:7], d[:4])


def make_index(rows, esma_date, extra, built):
    """extra: {"xetra": date or None, "openfigi": date or None, "wikidata": date or None}; a source is listed only when it was used."""
    sources = [{
        "id": "esma", "name": "ESMA FIRDS", "date": esma_date,
        # LEGAL CONDITION (ESMA legal notice): keep this credit clearly SEPARATE from any advertising area wherever it is
        # shown (search dialog footer, guides, privacy text). If ads are ever added, never place them in or next to it.
        "attr": "Source: ESMA Financial Instruments Reference Data System (FIRDS), registers.esma.europa.eu, data as of %s. "
                "Names, venues and classification were condensed and transformed by Finplanr. Not endorsed by ESMA." % esma_date,
        "attr_de": "Quelle: ESMA Financial Instruments Reference Data System (FIRDS), registers.esma.europa.eu, Stand %s. "
                   "Namen, Handelsplätze und Klassifizierung wurden von Finplanr verdichtet und bearbeitet. Keine Empfehlung durch die ESMA." % de_date(esma_date),
    }]
    if extra.get("openfigi"):
        d = extra["openfigi"]
        sources.append({
            "id": "openfigi", "name": "OpenFIGI", "date": d,
            "attr": "Xetra tickers: OpenFIGI (Bloomberg L.P.), open symbology, FIGI identifiers dedicated to the public domain, queried %s. "
                    "Not endorsed by Bloomberg." % d,
            "attr_de": "Xetra-Kürzel: OpenFIGI (Bloomberg L.P.), offene Symbologie, FIGI-Kennungen gemeinfrei gestellt, abgefragt am %s. "
                       "Keine Empfehlung durch Bloomberg." % de_date(d),
        })
    if extra.get("wikidata"):
        d = extra["wikidata"]
        sources.append({
            "id": "wikidata", "name": "Wikidata", "date": d,
            "attr": "Tickers of US stocks (Nasdaq, NYSE): Wikidata, structured data under CC0, queried %s." % d,
            "attr_de": "Kürzel von US-Aktien (Nasdaq, NYSE): Wikidata, strukturierte Daten unter CC0, abgefragt am %s." % de_date(d),
        })
    if extra.get("xetra"):
        d = extra["xetra"]
        sources.append({
            "id": "xetra", "name": "Deutsche Börse Xetra / Börse Frankfurt", "date": d,
            "attr": "WKN, Xetra ticker and Xetra/Börse Frankfurt listings: Deutsche Börse AG, \"All tradable instruments\" "
                    "(Xetra, Börse Frankfurt), data as of %s. PRIVATE BUILD: not licensed for publication." % d,
            "attr_de": "WKN, Xetra-Kürzel sowie Xetra-/Börse-Frankfurt-Listings: Deutsche Börse AG, \"Alle handelbaren Instrumente\" "
                       "(Xetra, Börse Frankfurt), Stand %s. PRIVATER BUILD: nicht zur Veröffentlichung lizenziert." % de_date(d),
        })
    used = {v for r in rows for v in r[6].split()}
    venues = {k: VENUE_NAMES[k] for k in VENUE_ORDER if k in used}
    return {"v": 1, "built": built, "sources": sources, "venues": venues,
            "cols": ["isin", "name", "wkn", "ticker", "type", "ccy", "venues"], "rows": rows}


def encode(index):
    head = {k: v for k, v in index.items() if k != "rows"}
    h = json.dumps(head, ensure_ascii=False, separators=(",", ":"))
    body = ",\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in index["rows"])
    plain = (h[:-1] + ',"rows":[\n' + body + "\n]}").encode("utf-8")
    json.loads(plain)  # self-check: valid JSON
    return plain, gzip.compress(plain, 9, mtime=0)


def load_validator():
    p = ROOT / "tools" / "validate-instruments.py"
    if not p.is_file():
        return None
    spec = importlib.util.spec_from_file_location("validate_instruments", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def validate_with_tool(path):
    mod = load_validator()
    if mod is None:
        log("  (tools/validate-instruments.py not found: contract check skipped)")
        return
    problems = mod.validate_file(path)
    if problems:
        log("  CONTRACT CHECK FAILED:")
        for p in problems[:20]:
            log("    - " + p)
        raise SystemExit(1)
    log("  contract check  OK")


# ---------------------------------------------------------------------------- verification report
DEFAULT_HOLDINGS = ["IE00BF4RFH31", "IE00BKM4GZ66", "IE00BK5BQT80", "JE00BN2CJ301", "JE00BQRFDY49"]
CATALOG_STOCKS = ["US0378331005", "US5949181045", "US67066G1040", "US88160R1014", "US0231351067", "US02079K3059",
                  "US30303M1027", "US0846707026", "DE0007164600", "DE0007236101", "DE0008404005", "DE0005557508",
                  "DE0007664039", "DE0007100000", "DE0005190003", "DE000BASF111"]
POPULAR_ETFS = ["IE00B4L5Y983", "IE00B5BMR087", "IE00BJ0KDQ92", "IE00BFMXXD54", "LU0274208692", "DE0005933931",
                "IE00B3RBWM25", "IE00B4ND3602", "LU1681043599", "IE00B3XXRP09", "IE00BKX55T58", "IE00B0M62Q58",
                "IE00B1XNHC34", "IE00B3F81R35", "IE00BTJRMP35", "IE00B4K48X80", "LU0908500753", "IE00B53SZB19",
                "IE00B3YLTY66", "IE00B6YX5C33", "IE00B8GKDB10", "LU0290358497", "IE00BYX2JD69", "IE00B4WXJJ64",
                "IE00BK5BQT80"]
TICKER_SAMPLES = {"VWCE": "IE00BK5BQT80", "EUNL": "IE00B4L5Y983", "SXR8": "IE00B5BMR087", "WGLD": "JE00BN2CJ301", "SAP": "DE0007164600"}


def verify(args):
    path = Path(args.out)
    if not path.is_file():
        log("index not found: %s (run without --verify first)" % path)
        return 1
    idx = json.loads(path.read_text(encoding="utf-8"))
    rows = idx["rows"]
    by_isin = {r[0]: r for r in rows}
    by_wkn = {r[2]: r for r in rows if r[2]}
    by_tick = {r[3]: r for r in rows if r[3]}
    names = {k: i for i, k in enumerate(idx["cols"])}

    def show(isin):
        r = by_isin.get(isin)
        if not r:
            return None
        return "%s | %s | WKN %s | %s | type %s | %s | %s" % (r[0], r[1], r[2] or "-", r[3] or "-", r[4], r[5] or "-", r[6])

    log("index built %s, sources: %s" % (idx["built"], ", ".join("%s %s" % (s["id"], s["date"]) for s in idx["sources"])))
    cnt = Counter(r[4] for r in rows)
    log("rows %d: ETF %d, ETC/ETN %d, stocks %d, other funds %d, other %d" % (len(rows), cnt["E"], cnt["C"], cnt["S"], cnt["F"], cnt["O"]))
    etf_de = sum(1 for r in rows if r[4] == "E" and set(r[6].split()) & {"XETR", "XFRA", "XSTU", "XGAT", "MUND", "HAMN"})
    log("ETFs on at least one of Xetra/Frankfurt/Stuttgart/Tradegate/gettex/L&S: %d (public claim: about 3,500+ UCITS ETFs tradable in Germany)" % etf_de)
    bad = 0
    log("\n-- the instrument the owner could not find")
    log("IE000JHYO4T6: " + (show("IE000JHYO4T6") or "NOT FOUND"))
    for title, lst in (("default holdings", DEFAULT_HOLDINGS), ("catalog stocks", CATALOG_STOCKS), ("further popular ETFs", POPULAR_ETFS)):
        found, missing = [], []
        for i in lst:
            (found if i in by_isin else missing).append(i)
        log("\n-- %s: %d/%d found" % (title, len(found), len(lst)))
        for i in found:
            log("   ok   " + show(i))
        for i in missing:
            log("   MISSING %s" % i)
        bad += len(missing)
    log("\n-- search by ticker / WKN")
    for t, isin in TICKER_SAMPLES.items():
        r = by_tick.get(t)
        log("   ticker %-5s -> %s %s" % (t, r[0] if r else "NOT FOUND", "(as expected)" if r and r[0] == isin else "(UNEXPECTED)"))
        if not r or r[0] != isin:
            bad += 1
    with_xetra = any(x["id"] == "xetra" for x in idx["sources"])
    for w in ("716460", "A2PKXG", "A0RPWH", "A3DE9T"):
        r = by_wkn.get(w)
        derived = w == "716460"  # German ISIN: the WKN is part of the ISIN
        if r:
            log("   WKN    %-6s -> %s %s" % (w, r[0], r[1]))
        elif derived or with_xetra:
            log("   WKN    %-6s -> NOT FOUND" % w)
            bad += 1
        else:
            log("   WKN    %-6s -> not in the index (expected: foreign ISINs get no WKN without --with-xetra)" % w)
    log("\nverification: %s" % ("all lookups succeeded" if not bad else "%d lookup(s) failed" % bad))
    return 0 if not bad else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the local instrument search index from ESMA FIRDS, OpenFIGI and Wikidata (open data).")
    ap.add_argument("--refresh", action="store_true", help="download everything again, ignoring the cache")
    ap.add_argument("--offline", action="store_true", help="no network access: build from the newest cached raw files")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="index file to write (default build-cache/instruments.v1.json)")
    ap.add_argument("--with-xetra", action="store_true",
                    help="PRIVATE builds only: also use the Deutsche Boerse 'All tradable instruments' files (WKN, Xetra ticker). Not licensed for publication.")
    ap.add_argument("--no-xetra-fields", action="store_true", help="accepted for compatibility; this is the default now")
    ap.add_argument("--no-openfigi", action="store_true", help="do not look up Xetra tickers at OpenFIGI")
    ap.add_argument("--no-wikidata", action="store_true", help="do not add Nasdaq / NYSE tickers from Wikidata")
    ap.add_argument("--verify", action="store_true", help="only run the lookup verification report on the existing index")
    args = ap.parse_args(argv)
    if args.with_xetra and args.no_xetra_fields:
        ap.error("--with-xetra and --no-xetra-fields exclude each other")
    if args.verify:
        return verify(args)
    try:
        return build(args)
    except (RuntimeError, OSError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
