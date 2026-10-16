#!/usr/bin/env python3
"""Validate the instrument index contract "v":1 (build-cache/instruments.v1.json, written by fetch-instruments.py).

    python3 -I tools/validate-instruments.py [PATH] [--fix]

Checks: JSON shape, columns, sources (id, name, date, attr, attr_de), venue codes defined and used rows only reference
defined venues, ISIN format and check digit, unique ISINs, type codes, WKN / ticker / currency shape, ticker convention
(a ticker needs XETR, XNAS or XNYS among the venues: it belongs to Xetra when XETR is listed, otherwise to Nasdaq / NYSE), sort order
(type priority E, C, S, F, O, then name case-insensitive, then ISIN) and the gzip size budget (4 MB).
--fix rewrites the file without rows that have an invalid ISIN (the only fixable problem) and reports what was dropped.
Exit codes: 0 valid, 1 problems found. Importable: validate_file(path) -> list of problem strings. Stdlib only.
"""
import gzip
import json
import re
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / "build-cache" / "instruments.v1.json"
COLS = ["isin", "name", "wkn", "ticker", "type", "ccy", "venues"]
PRIO = {"E": 0, "C": 1, "S": 2, "F": 3, "O": 4}
BUDGET_GZ = 4 * 1024 * 1024


def isin_ok(s):
    if not isinstance(s, str) or not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}[0-9]", s):
        return False
    digits = "".join(str(int(c, 36)) for c in s)
    t = 0
    for i, c in enumerate(reversed(digits)):
        d = int(c)
        if i % 2:
            d = d * 2 - 9 if d > 4 else d * 2
        t += d
    return t % 10 == 0


def validate(idx, gz_size=None, max_report=25):
    P = []
    if not isinstance(idx, dict):
        return ["top level is not an object"]
    if idx.get("v") != 1:
        P.append('"v" must be 1')
    if not re.fullmatch(r"\d{4}-\d\d-\d\d", str(idx.get("built", ""))):
        P.append('"built" must be YYYY-MM-DD')
    src = idx.get("sources")
    if not isinstance(src, list) or not src:
        P.append('"sources" must be a non-empty list')
    else:
        for s in src:
            if not isinstance(s, dict) or any(not isinstance(s.get(k), str) or not s.get(k) for k in ("id", "name", "date", "attr", "attr_de")):
                P.append("source entry incomplete: %r" % (s.get("id") if isinstance(s, dict) else s))
    ven = idx.get("venues")
    if not isinstance(ven, dict) or not ven or any(not re.fullmatch(r"[A-Z0-9]{4}", k) or not isinstance(v, str) or not v for k, v in ven.items()):
        P.append('"venues" must map 4-character MIC codes to names')
        ven = ven if isinstance(ven, dict) else {}
    if idx.get("cols") != COLS:
        P.append('"cols" must be %s' % COLS)
    rows = idx.get("rows")
    if not isinstance(rows, list) or not rows:
        P.append('"rows" must be a non-empty list')
        return P
    seen, prev, bad = set(), None, []
    for n, r in enumerate(rows):
        def bad_row(msg):
            bad.append("row %d %s: %s" % (n, r[0] if isinstance(r, list) and r else "?", msg))
        if not isinstance(r, list) or len(r) != 7 or any(not isinstance(x, str) for x in r):
            bad_row("not a list of 7 strings")
            continue
        isin, name, wkn, tick, typ, ccy, vs = r
        if not isin_ok(isin):
            bad_row("invalid ISIN")
        if isin in seen:
            bad_row("duplicate ISIN")
        seen.add(isin)
        if not name or name != re.sub(r"\s+", " ", name).strip():
            bad_row("name empty or not whitespace-normalised")
        if wkn and not re.fullmatch(r"[A-Z0-9]{6}", wkn):
            bad_row("bad WKN %r" % wkn)
        if tick and not re.fullmatch(r"[A-Z0-9.\-]{1,12}", tick):
            bad_row("bad ticker %r" % tick)
        if typ not in PRIO:
            bad_row("bad type %r" % typ)
        if ccy and not re.fullmatch(r"[A-Z]{3}", ccy):
            bad_row("bad currency %r" % ccy)
        toks = vs.split(" ")
        if not vs or any(t not in ven for t in toks):
            bad_row("venues missing or undefined: %r" % vs)
        if tick and not ({"XETR", "XNAS", "XNYS"} & set(toks)):
            bad_row("ticker %r without a venue it belongs to (XETR, XNAS or XNYS)" % tick)
        if typ in PRIO:
            key = (PRIO[typ], name.casefold(), isin)
            if prev is not None and key < prev:
                bad_row("sort order violated")
            prev = key
    P.extend(bad[:max_report])
    if len(bad) > max_report:
        P.append("... and %d more row problems" % (len(bad) - max_report))
    used = {t for r in rows if isinstance(r, list) and len(r) == 7 and isinstance(r[6], str) for t in r[6].split(" ")}
    if set(ven) - used:
        P.append("venues defined but unused: %s" % " ".join(sorted(set(ven) - used)))
    if gz_size is not None and gz_size > BUDGET_GZ:
        P.append("gzip size %d exceeds the budget of %d bytes" % (gz_size, BUDGET_GZ))
    return P


def validate_file(path):
    try:
        raw = Path(path).read_bytes()
        idx = json.loads(raw.decode("utf-8"))
    except (OSError, ValueError) as e:
        return ["cannot read %s: %s" % (path, e)]
    return validate(idx, len(gzip.compress(raw, 9, mtime=0)))


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    path = Path(args[0]) if args else DEFAULT
    if "--fix" in argv:
        idx = json.loads(path.read_text(encoding="utf-8"))
        keep = [r for r in idx["rows"] if isin_ok(r[0])]
        if len(keep) != len(idx["rows"]):
            print("dropped %d rows with invalid ISIN" % (len(idx["rows"]) - len(keep)))
            idx["rows"] = keep
            head = json.dumps({k: v for k, v in idx.items() if k != "rows"}, ensure_ascii=False, separators=(",", ":"))
            body = ",\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in keep)
            path.write_text(head[:-1] + ',"rows":[\n' + body + "\n]}", encoding="utf-8")
    problems = validate_file(path)
    if problems:
        print("INVALID: %s" % path)
        for p in problems:
            print("  - " + p)
        return 1
    n = len(json.loads(path.read_text(encoding="utf-8"))["rows"])
    print("valid: %s (%d rows)" % (path, n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
