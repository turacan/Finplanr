#!/usr/bin/env python3
"""Build the deployable Finplanr site into dist/ and inject the local operator configuration.

    cp config/operator.example.json config/operator.json     # once, then fill in your own values
    python3 -I tools/build.py

Nothing personal is committed: the sources (site/, parked-for-later/datenschutz-text.*.md) only contain
{{PLACEHOLDERS}}; the real values live in config/operator.json (git-ignored) and are injected here.

Result (dist/ is deleted and rebuilt on every run, so the output is reproducible):
  * a copy of site/ with all placeholders replaced (text files only; images and other binaries are copied as-is),
  * dist/de/index.html: the German page generated from site/index.html (static markup localized from the STR table,
    German SEO head block),
  * dist/datenschutz.html and dist/en/datenschutz.html: the privacy policy pages rendered from
    parked-for-later/datenschutz-text.de.md / .en.md,
  * private/datenschutz-text.de.md and .en.md: the same texts with your values filled in (for pasting into an
    Impressum service; git-ignored folder).
The build then verifies the result (no placeholder left, every sitemap URL exists, real values present).

Options:
  --config PATH        operator config (default: config/operator.json)
  --out DIR            output directory (default: dist/; must not exist yet or be empty, unless it is the default one)
  --private-out DIR    where the filled markdown texts go (default: private/ for the default --out, else <out>-private)
  --update-source      also refresh the English SEO head block inside site/index.html from the STR table

Exit codes: 0 ok, 1 build/verification error, 2 missing or invalid configuration.
Stdlib only.
"""
import argparse
import html
import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "site"
INDEX_SRC = SRC_DIR / "index.html"
DEFAULT_CONFIG = ROOT / "config" / "operator.json"
DEFAULT_OUT = ROOT / "dist"
DEFAULT_PRIVATE = ROOT / "private"
MD_SRC = {"de": ROOT / "parked-for-later" / "datenschutz-text.de.md", "en": ROOT / "parked-for-later" / "datenschutz-text.en.md"}

BASE = "https://finplanr.net"
OG_IMAGE = BASE + "/og-image.png"

TEXT_EXT = {".html", ".htm", ".md", ".xml", ".txt", ".svg", ".js", ".css", ".json", ".webmanifest"}
ESCAPE_EXT = {".html", ".htm", ".xml", ".svg"}  # values are HTML-escaped when injected into these
SKIP_NAMES = {".DS_Store", "Thumbs.db"}

REQUIRED_STR = ["operator_name", "country_de", "country_en", "email", "impressum_url", "impressum_provider_name",
                "copyright_holder", "mailbox_provider_name", "mailbox_provider_address_de", "mailbox_provider_address_en",
                "mailbox_recipient_de", "mailbox_recipient_en", "mailbox_transfer_de", "mailbox_transfer_en"]
PLACEHOLDER_RE = re.compile(r"\{\{([A-Z_]+)\}\}")


class ConfigError(Exception):
    pass


# --------------------------------------------------------------------------- configuration and placeholders

def load_config(path):
    path = Path(path)
    if not path.is_file():
        raise ConfigError("operator configuration not found: %s\n"
                          "Copy config/operator.example.json to config/operator.json and fill it in." % path)
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise ConfigError("cannot read %s: %s" % (path, e))
    if not isinstance(cfg, dict):
        raise ConfigError("%s must contain a JSON object" % path)
    for k in REQUIRED_STR:
        if not isinstance(cfg.get(k), str) or not cfg[k].strip():
            raise ConfigError("%s: key '%s' is missing or empty" % (path.name, k))
        if "{{" in cfg[k] or "\n" in cfg[k]:
            raise ConfigError("%s: key '%s' must be a single line without '{{'" % (path.name, k))
    lines = cfg.get("address_lines")
    if not isinstance(lines, list) or not lines or not all(isinstance(x, str) and x.strip() and "{{" not in x for x in lines):
        raise ConfigError("%s: 'address_lines' must be a non-empty array of strings" % path.name)
    if not re.fullmatch(r"https?://[^\s'\"<>\\&{}]+", cfg["impressum_url"]):
        raise ConfigError("%s: 'impressum_url' must be a plain http(s) URL without spaces, quotes, '&', '<', '>' or backslashes" % path.name)
    return cfg


def placeholder_values(cfg, lang=None):
    """Mapping placeholder name -> raw value. Language specific entries only exist when lang is given."""
    v = {
        "OPERATOR_NAME": cfg["operator_name"],
        "COPYRIGHT_HOLDER": cfg["copyright_holder"],
        "EMAIL": cfg["email"],
        "IMPRESSUM_URL": cfg["impressum_url"],
        "IMPRESSUM_PROVIDER": cfg["impressum_provider_name"],
    }
    if lang:
        v["COUNTRY"] = cfg["country_" + lang]
        v["ADDRESS_BLOCK"] = "  \n".join(list(cfg["address_lines"]) + [cfg["country_" + lang]])
        v["MAILBOX_PROVIDER"] = cfg["mailbox_provider_name"] + ", " + cfg["mailbox_provider_address_" + lang]
        v["MAILBOX_RECIPIENT"] = cfg["mailbox_recipient_" + lang]
        v["MAILBOX_TRANSFER"] = cfg["mailbox_transfer_" + lang]
    return v


def fill(text, values, escape):
    """Replace {{KEY}} placeholders. Unknown keys are left in place (the final verification reports them)."""
    def sub(m):
        k = m.group(1)
        if k not in values:
            return m.group(0)
        return html.escape(values[k], quote=True) if escape else values[k]
    return PLACEHOLDER_RE.sub(sub, text)


# --------------------------------------------------------------------------- German page and SEO head (from the former build-de.py)

PAGES = {
    "en": {"path": "/", "locale": "en_US", "alt_locale": "de_DE", "guide": "/en/anleitung.html", "privacy": "/en/datenschutz.html"},
    "de": {"path": "/de/", "locale": "de_DE", "alt_locale": "en_US", "guide": "/anleitung.html", "privacy": "/datenschutz.html"},
}
# Elements whose text is set by app code (not by data-i18n) but should be localized in the static HTML too.
EXTRA_TEXT_BY_ID = {"editToggle": "tb.edit"}
OG_ALT = {"en": "Finplanr: savings plan calculator", "de": "Finplanr: Sparplan-Rechner"}
COPYRIGHT_MARKERS = ("© 2026 {{COPYRIGHT_HOLDER}}. All rights reserved.",
                     '<meta name="author" content="{{OPERATOR_NAME}}">',
                     '<meta name="copyright" content="© 2026 {{COPYRIGHT_HOLDER}}">',
                     "const IMPRESSUM_URL='{{IMPRESSUM_URL}}';")


def unescape_js(s):
    return re.sub(r"\\(u[0-9a-fA-F]{4}|.)", lambda m: chr(int(m.group(1)[1:], 16)) if len(m.group(1)) == 5 else {"n": "\n", "t": "\t"}.get(m.group(1), m.group(1)), s)


def parse_str(text):
    """Return {'en': {...}, 'de': {...}} with the plain string entries of the STR table."""
    start = text.index("const STR={")
    de_at = text.index("\n    de:{", start)
    end = text.index("\n  };", de_at)
    pair = re.compile(r"'([\w.]+)':'((?:[^'\\\n]|\\.)*)'")
    return {
        "en": {k: unescape_js(v) for k, v in pair.findall(text[start:de_at])},
        "de": {k: unescape_js(v) for k, v in pair.findall(text[de_at:end])},
    }


def head_block(lang, STR):
    p = PAGES[lang]
    title, desc = STR[lang]["meta.title"], STR[lang]["meta.desc"]
    url = BASE + p["path"]
    jsonld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Finplanr",
        "url": url,
        "description": desc,
        "applicationCategory": "FinanceApplication",
        "operatingSystem": "Web",
        "inLanguage": lang,
        "browserRequirements": "Requires JavaScript",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
    }
    ld = json.dumps(jsonld, ensure_ascii=False, indent=2).replace("</", "<\\/")
    a = lambda v: html.escape(v, quote=True)
    lines = [
        f"<title>{html.escape(title, quote=False)}</title>",
        f'<meta name="description" content="{a(desc)}">',
        f'<link rel="canonical" href="{url}">',
        f'<link rel="alternate" hreflang="en" href="{BASE}/">',
        f'<link rel="alternate" hreflang="de" href="{BASE}/de/">',
        f'<link rel="alternate" hreflang="x-default" href="{BASE}/">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Finplanr">',
        f'<meta property="og:title" content="{a(title)}">',
        f'<meta property="og:description" content="{a(desc)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:locale" content="{p["locale"]}">',
        f'<meta property="og:locale:alternate" content="{p["alt_locale"]}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        '<meta property="og:image:type" content="image/png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{a(OG_ALT[lang])}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{a(title)}">',
        f'<meta name="twitter:description" content="{a(desc)}">',
        f'<meta name="twitter:image" content="{OG_IMAGE}">',
        f'<script type="application/ld+json">\n{ld}\n</script>',
    ]
    return "\n".join("  " + l.replace("\n", "\n  ") for l in lines)


SEO_RE = re.compile(r"(  <!-- seo:begin[^\n]*-->\n)(?:.*?\n)?(  <!-- seo:end -->)", re.S)


def with_head(text, lang, STR):
    new, n = SEO_RE.subn(lambda m: m.group(1) + head_block(lang, STR) + "\n" + m.group(2), text, count=1)
    if n != 1:
        raise RuntimeError("seo markers not found in site/index.html")
    return new


TAG_RE = re.compile(r"<([a-zA-Z][\w-]*)((?:\s+[\w:-]+(?:=(?:\"[^\"]*\"|'[^']*'|[^\s>]+))?)*)\s*/?>")
ATTR_RE = re.compile(r"([\w:-]+)(?:=(\"[^\"]*\"|'[^']*'|[^\s>]+))?")


def localize_body(body, T):
    """Fill data-i18n text and data-i18n-attr attributes of the static markup from the table T."""
    stats = {"text": 0, "attr": 0, "skipped": []}
    out, pos = [], 0
    for m in TAG_RE.finditer(body):
        tag, attrs_s = m.group(1), m.group(2)
        attrs = {k: (v[1:-1] if v and v[0] in "\"'" else v) for k, v in ATTR_RE.findall(attrs_s)}
        key = attrs.get("data-i18n") or EXTRA_TEXT_BY_ID.get(attrs.get("id", ""))
        spec = attrs.get("data-i18n-attr")
        if not key and not spec:
            continue
        start_tag = m.group(0)
        if spec:
            for pair in spec.split(","):
                name, _, k = pair.partition(":")
                name, k = name.strip(), k.strip()
                val = html.escape(T[k], quote=True)
                if re.search(r'\s%s="[^"]*"' % re.escape(name), start_tag):
                    start_tag = re.sub(r'(\s%s=)"[^"]*"' % re.escape(name), lambda mm: mm.group(1) + '"' + val + '"', start_tag, count=1)
                else:
                    start_tag = start_tag[:-1].rstrip("/ ") + f' {name}="{val}">'
                stats["attr"] += 1
        out.append(body[pos:m.start()])
        out.append(start_tag)
        pos = m.end()
        if key:
            close = f"</{tag}>"
            end = body.find("<", pos)
            if end != -1 and body.startswith(close, end):
                out.append(html.escape(T[key], quote=False))
                pos = end
                stats["text"] += 1
            else:
                stats["skipped"].append(key)
    out.append(body[pos:])
    return "".join(out), stats


def build_app_pages(src_text):
    """Return (english_text, german_text, stats) from the source index.html (placeholders still in place)."""
    for marker in COPYRIGHT_MARKERS:
        if src_text.count(marker) < 1:
            raise RuntimeError("expected placeholder text missing in site/index.html: " + marker)
    STR = parse_str(src_text)
    missing = sorted(set(STR["en"]) ^ set(STR["de"]))
    if missing:
        raise RuntimeError("STR keys not present in both languages: " + ", ".join(missing))
    en_text = with_head(src_text, "en", STR)
    de = with_head(en_text, "de", STR)
    de = de.replace('<html lang="en">', '<html lang="de">', 1)
    b0 = de.index("<body>")
    b1 = de.index("<script>", b0)
    body, stats = localize_body(de[b0:b1], STR["de"])
    if stats["skipped"]:
        raise RuntimeError("data-i18n elements with child markup (cannot be localized statically): " + ", ".join(stats["skipped"]))
    de = de[:b0] + body + de[b1:]
    de = de.replace('data-lang="de" aria-pressed="false"', 'data-lang="de" aria-pressed="true"', 1)
    de = de.replace('data-lang="en" aria-pressed="true"', 'data-lang="en" aria-pressed="false"', 1)
    de = de.replace('id="guideLink" href="%s"' % PAGES["en"]["guide"], 'id="guideLink" href="%s"' % PAGES["de"]["guide"], 1)
    de = de.replace('data-privacy-link href="%s"' % PAGES["en"]["privacy"], 'data-privacy-link href="%s"' % PAGES["de"]["privacy"])
    return en_text, de, stats


# --------------------------------------------------------------------------- privacy pages (from the former build-datenschutz-pages.py)

PRIVACY = {
    "de": dict(
        lang="de", title="Datenschutzerklärung | Finplanr",
        desc="Datenschutzerklärung von Finplanr",
        nav_label="Hauptnavigation", app="App öffnen", lang_label="Sprache",
        toc="Inhalt", impressum="Impressum", guide="Anleitung", guide_href="/anleitung.html",
        footnote="Planungswerkzeug, keine Anlageberatung.",
        de_href="/datenschutz.html", en_href="/en/datenschutz.html", de_cur=True,
        privacy="Datenschutz", app_href="/de/", out="datenschutz.html", prefix="abschnitt",
    ),
    "en": dict(
        lang="en", title="Privacy policy | Finplanr",
        desc="Privacy policy of Finplanr",
        nav_label="Main navigation", app="Open app", lang_label="Language",
        toc="Contents", impressum="Legal notice (Impressum)", guide="User guide", guide_href="/en/anleitung.html",
        footnote="Planning tool, not investment advice.",
        de_href="/datenschutz.html", en_href="/en/datenschutz.html", de_cur=False,
        app_href="/", privacy="Privacy policy", out="en/datenschutz.html", prefix="section",
    ),
}

URL_RE = re.compile(r'https?://[^\s<>()"“”„]+')
EMAIL_RE = re.compile(r'(?<![\w@/.=-])[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}')
# Cloudflare "Email Address Obfuscation" (Scrape Shield) rewrites e-mail addresses in HTML into JS-decoded links; without JavaScript the
# visitor sees "[email protected]". Documented exemption (developers.cloudflare.com/waf/tools/scrape-shield/email-address-obfuscation/):
# wrap the address in <!--email_off--> ... <!--/email_off-->. The href of an <a> is obfuscated too, so the WHOLE link is wrapped.
EMAIL_OFF = ("<!--email_off-->", "<!--/email_off-->")
EMAIL_OFF_RE = re.compile(re.escape(EMAIL_OFF[0]) + r".*?" + re.escape(EMAIL_OFF[1]), re.S)


def inline(text):
    # protect code spans
    codes = []

    def code_sub(m):
        codes.append(m.group(1))
        return "\x00C%d\x00" % (len(codes) - 1)
    text = re.sub(r'`([^`]+)`', code_sub, text)
    text = html.escape(text, quote=False)

    def link_sub(m):
        url = m.group(0)
        trail = ""
        while url and url[-1] in ".,;:":
            trail = url[-1] + trail
            url = url[:-1]
        return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>%s' % (url, url, trail)
    text = URL_RE.sub(link_sub, text)
    text = EMAIL_RE.sub(lambda m: '%s<a href="mailto:%s">%s</a>%s' % (EMAIL_OFF[0], m.group(0), m.group(0), EMAIL_OFF[1]), text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # the single owner placeholder
    text = re.sub(r'\[([^\]]*(?:bitte ergänzen|please add)[^\]]*)\]', r'<mark class="todo">[\1]</mark>', text)
    text = re.sub(r'\x00C(\d+)\x00', lambda m: '<code>%s</code>' % html.escape(codes[int(m.group(1))], quote=False), text)
    return text


def convert(md, prefix="abschnitt"):
    lines = md.split("\n")
    out, toc = [], []
    i, n = 0, len(lines)
    h1 = ""
    para = []
    ul = False
    sec = 0

    def flush_para():
        nonlocal para
        if para:
            out.append("<p>" + "<br>\n".join(inline(p) for p in para) + "</p>")
            para = []

    def close_ul():
        nonlocal ul
        if ul:
            out.append("</ul>")
            ul = False

    while i < n:
        line = lines[i].rstrip("\n")
        if not line.strip():
            flush_para(); close_ul(); i += 1; continue
        if line.startswith("# "):
            flush_para(); close_ul(); h1 = line[2:].strip(); i += 1; continue
        m = re.match(r'^## (.+?)(?:\s*\{#([\w-]+)\})?\s*$', line)
        if m:
            flush_para(); close_ul()
            sec += 1
            title = m.group(1).strip()
            sid = m.group(2) or ("%s-%d" % (prefix, sec))
            toc.append((sid, title))
            out.append('<h2 id="%s">%s</h2>' % (sid, inline(title)))
            i += 1; continue
        if line.startswith("- "):
            flush_para()
            if not ul:
                out.append("<ul>"); ul = True
            out.append("<li>" + inline(line[2:].strip()) + "</li>")
            i += 1; continue
        # paragraph line: lines of one block are joined with <br> (the address block uses hard breaks)
        para.append(line.strip())
        i += 1
    flush_para(); close_ul()
    return h1, toc, "\n".join(out)


def render_privacy_page(lang, md_filled):
    """Render one privacy page from the already filled markdown text. The footer carries {{IMPRESSUM_URL}}
    for the caller's fill() pass."""
    c = PRIVACY[lang]
    h1, toc, body = convert(md_filled, c["prefix"])
    toc_html = "\n".join('<li><a href="#%s">%s</a></li>' % (sid, inline(t)) for sid, t in toc)
    de_cur = ' aria-current="page"' if c["de_cur"] else ""
    en_cur = "" if c["de_cur"] else ' aria-current="page"'
    m = re.search(r'<p><strong>[^<]*(?:Stand|Last updated)[^<]*</strong></p>\n?', body)
    if not m:
        raise RuntimeError("'Stand' / 'Last updated' line missing in the %s privacy text" % lang)
    stand = m.group(0).strip()
    body = body.replace(m.group(0), "", 1)
    return f"""<!doctype html>
<html lang="{c['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(c['desc'])}">
<title>{html.escape(c['title'])}</title>
<link rel="stylesheet" href="/style.css">
<style>
main{{max-width:820px}}
main h2{{scroll-margin-top:12px;font-size:1.25rem}}
.toc{{border:1px solid #d8e2ed;border-radius:10px;padding:6px 20px 6px 8px;background:#fff}}
.toc ol{{margin:8px 0;padding-left:12px;list-style:none;columns:2;column-gap:28px}}
.toc li{{margin-bottom:4px;break-inside:avoid}}
.toc strong{{display:block;padding:8px 0 0 12px}}
code{{background:#eaf0f7;padding:1px 5px;border-radius:4px;font-size:.92em;word-break:break-all}}
mark.todo{{background:#fff3b0;color:#4a3b00;padding:1px 4px;border-radius:4px}}
main a{{overflow-wrap:anywhere}}
footer .links{{display:flex;gap:16px;flex-wrap:wrap}}
@media(max-width:680px){{.toc ol{{columns:1}}}}
@media(prefers-color-scheme:dark){{
:root{{color:#dbe6f2;background:#0f1a26}}
a{{color:#7fb8ee}}
.brand{{color:#eaf2fb}}
.toc{{background:#14212f;border-color:#2b3d51}}
code{{background:#1d2e40}}
mark.todo{{background:#5a4a00;color:#fff3b0}}
footer,.language-switch a{{border-color:#2b3d51;color:#a9bbcf}}
.language-switch a[aria-current="page"]{{color:#fff}}
}}
</style>
</head>
<body>
<header>
<a class="brand" href="{c['app_href']}">Finplanr</a>
<nav aria-label="{c['nav_label']}"><a href="{c['app_href']}">{c['app']}</a></nav>
<div class="language-switch" aria-label="{c['lang_label']}"><a lang="de"{de_cur} href="{c['de_href']}">DE</a><a lang="en"{en_cur} href="{c['en_href']}">EN</a></div>
</header>
<main>
<h1>{html.escape(h1)}</h1>
{stand}
<nav class="toc" aria-label="{c['toc']}"><strong>{c['toc']}</strong>
<ol>
{toc_html}
</ol></nav>
{body}
</main>
<footer>
<div class="links"><a href="{c['app_href']}">{c['app']}</a><a href="{c['guide_href']}">{c['guide']}</a><a href="{{{{IMPRESSUM_URL}}}}" target="_blank" rel="noopener noreferrer">{c['impressum']}</a></div>
<p>{c['footnote']}</p>
</footer>
</body>
</html>
""", len(toc)


# --------------------------------------------------------------------------- build

def is_text(path):
    return path.suffix.lower() in TEXT_EXT


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    path.chmod(0o644)


def copy_site(out, cfg):
    """Copy site/ to out, filling placeholders in text files. Returns the number of files."""
    values = placeholder_values(cfg)
    n = 0
    for p in sorted(SRC_DIR.rglob("*")):
        rel = p.relative_to(SRC_DIR)
        if p.is_dir() or p.name in SKIP_NAMES or p.name.endswith(":Zone.Identifier") or any(part.startswith(".") for part in rel.parts):
            continue
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if is_text(p):
            text = p.read_text(encoding="utf-8")
            write_text(dest, fill(text, values, p.suffix.lower() in ESCAPE_EXT))
        else:
            shutil.copyfile(p, dest)
            dest.chmod(0o644)
        n += 1
    return n


def verify(out, cfg):
    errors = []
    # 1) no placeholder left
    for p in sorted(out.rglob("*")):
        if p.is_file() and is_text(p) and "{{" in p.read_text(encoding="utf-8"):
            errors.append("unreplaced '{{' in %s" % p.relative_to(out))
    # 2) every sitemap URL exists
    sm = out / "sitemap.xml"
    if not sm.is_file():
        errors.append("sitemap.xml missing")
    else:
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
        root = ET.parse(sm).getroot()
        urls = [e.text.strip() for e in root.iterfind(".//s:loc", ns)]
        urls += [e.get("href") for e in root.iterfind(".//x:link", ns)]
        for u in sorted(set(urls)):
            if not u.startswith(BASE + "/"):
                errors.append("sitemap URL outside %s: %s" % (BASE, u))
                continue
            rel = u[len(BASE) + 1:]
            target = out / (rel + "index.html" if rel == "" or rel.endswith("/") else rel)
            if not target.is_file():
                errors.append("sitemap URL has no file in the output: %s" % u)
    # 3) real values where expected
    def has(rel, *needles):
        f = out / rel
        if not f.is_file():
            errors.append("missing output file: " + rel)
            return
        t = f.read_text(encoding="utf-8")
        for needle in needles:
            if not (html.escape(needle, quote=True) in t or html.escape(needle, quote=False) in t):
                errors.append("%s does not contain the configured value %r" % (rel, needle if len(needle) < 40 else needle[:37] + "..."))
    name, mail, url = cfg["operator_name"], cfg["email"], cfg["impressum_url"]
    for rel in ("datenschutz.html", "en/datenschutz.html"):
        has(rel, name, mail, url, *cfg["address_lines"])
    for rel in ("index.html", "de/index.html", "anleitung.html", "en/anleitung.html"):
        has(rel, cfg["copyright_holder"], url)
    for rel in ("index.html", "de/index.html"):
        f = out / rel
        if f.is_file() and ('<meta name="author" content="%s">' % html.escape(name, quote=True)) not in f.read_text(encoding="utf-8"):
            errors.append("%s: meta author not set" % rel)
    # 4) the contact address must be shielded from Cloudflare's e-mail obfuscation in EVERY html page that shows it
    mail_html = html.escape(mail, quote=False)
    for p in sorted(out.rglob("*.html")):
        t = p.read_text(encoding="utf-8")
        if mail_html in EMAIL_OFF_RE.sub("", t) or mail in EMAIL_OFF_RE.sub("", t):
            errors.append("%s shows the contact address outside <!--email_off-->...<!--/email_off-->" % p.relative_to(out))
    for rel in ("datenschutz.html", "en/datenschutz.html"):
        f = out / rel
        if f.is_file():
            t = f.read_text(encoding="utf-8")
            wrapped = "".join(EMAIL_OFF_RE.findall(t))
            if mail_html not in re.sub(r"<[^>]+>", "", wrapped):
                errors.append("%s: no wrapped, visible contact address" % rel)
    return errors


def prepare_out(out):
    out = out.resolve()
    if out == DEFAULT_OUT.resolve():
        if out.exists():
            shutil.rmtree(out)
    else:
        if out in ROOT.parents or out == ROOT or out == SRC_DIR.resolve() or SRC_DIR.resolve() in out.parents:
            raise RuntimeError("refusing to use %s as output directory" % out)
        if out.exists() and (not out.is_dir() or any(out.iterdir())):
            raise RuntimeError("output directory %s exists and is not empty; remove it first" % out)
    out.mkdir(parents=True, exist_ok=True)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build dist/ from site/ and the local operator configuration.")
    ap.add_argument("--config", default=str(DEFAULT_CONFIG))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--private-out", default=None)
    ap.add_argument("--update-source", action="store_true")
    args = ap.parse_args(argv)

    try:
        cfg = load_config(args.config)
    except ConfigError as e:
        print("error: " + str(e), file=sys.stderr)
        return 2

    try:
        out_arg = Path(args.out).resolve()
        if args.private_out:
            private = Path(args.private_out)
        elif out_arg == DEFAULT_OUT.resolve():
            private = DEFAULT_PRIVATE
        else:
            private = out_arg.parent / (out_arg.name + "-private")

        for stale in ("de/index.html", "datenschutz.html", "en/datenschutz.html"):
            if (SRC_DIR / stale).exists():
                print("warning: site/%s is a generated file now; it is ignored and replaced in the output - delete it from the source" % stale, file=sys.stderr)

        src_text = INDEX_SRC.read_text(encoding="utf-8")
        en_text, de_text, stats = build_app_pages(src_text)
        if en_text != src_text:
            if args.update_source:
                INDEX_SRC.write_text(en_text, encoding="utf-8", newline="\n")
                print("updated the SEO head block in site/index.html")
            else:
                print("note: the SEO head block in site/index.html differs from the STR table; the output uses the generated one "
                      "(run with --update-source to refresh the source)", file=sys.stderr)

        out = prepare_out(out_arg)
        n_files = copy_site(out, cfg)

        # app pages: the generated English head replaces the source block, the German page is new
        base_values = placeholder_values(cfg)
        write_text(out / "index.html", fill(en_text, base_values, True))
        write_text(out / "de" / "index.html", fill(de_text, base_values, True))

        # privacy pages + filled markdown for the Impressum service
        private.mkdir(parents=True, exist_ok=True)
        for lang in ("de", "en"):
            md = fill(MD_SRC[lang].read_text(encoding="utf-8"), placeholder_values(cfg, lang), False)
            left = PLACEHOLDER_RE.findall(md)
            if left:
                raise RuntimeError("unknown placeholders in %s: %s" % (MD_SRC[lang].name, ", ".join(sorted(set(left)))))
            (private / ("datenschutz-text.%s.md" % lang)).write_text(md, encoding="utf-8", newline="\n")
            page, n_sec = render_privacy_page(lang, md)
            write_text(out / PRIVACY[lang]["out"], fill(page, base_values, True))
            print("rendered %s (%d sections)" % (PRIVACY[lang]["out"], n_sec))

        errors = verify(out, cfg)
    except (RuntimeError, OSError, ValueError) as e:
        print("error: " + str(e), file=sys.stderr)
        return 1
    if errors:
        print("verification FAILED:", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        return 1
    n_all = sum(1 for p in out.rglob("*") if p.is_file())
    print("localized %d texts and %d attributes in /de/; copied %d source files; %d files in %s; verification ok"
          % (stats["text"], stats["attr"], n_files, n_all, out))
    print("filled privacy texts: %s" % private)
    return 0


if __name__ == "__main__":
    sys.exit(main())
