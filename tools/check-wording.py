#!/usr/bin/env python3
"""Wording guard: Finplanr only CALCULATES from values the user enters. It must never read like investment advice.

    python3 -I tools/check-wording.py                 # scans the built site in dist/
    python3 -I tools/check-wording.py --src           # additionally scans the sources (site/, README, privacy texts, og-image)
    python3 -I tools/check-wording.py --dist DIR      # scan another build directory
    python3 -I tools/check-wording.py --no-dist --src # sources only

What is scanned (only text a visitor can read; HTML/JS comments are ignored):
  * every .html file: text nodes plus the attributes title, alt, aria-label, placeholder, value and content
    (meta description, og:/twitter: texts), plus the JSON-LD description,
  * inside the <script> of the app pages: every string literal (this covers the STR table with BOTH languages
    as well as texts that app code builds at run time),
  * with --src: README.md, parked-for-later/datenschutz-text.*.md and tools/og-image.html.

The build (tools/build.py) calls the same check and fails when it finds a banned term; .githooks/pre-commit runs it too.

Exit codes: 0 clean, 1 banned term found, 2 usage error. Stdlib only.
"""
import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------- BANNED TERMS (readable list; regexes, case-insensitive)
# Whole-word matching at the START of a word (so "advice" is caught, "Anlageberatung" only through its own entry).
BANNED_EN = [
    r"suggest\w*",        # suggest, suggestion, suggested
    r"recommend\w*",      # recommend, recommendation
    r"advis\w*",          # advise, advisable, advisor
    r"advice",            # only allowed inside the negating disclaimers below
    r"should",
    r"must",
    r"best",
    r"optimal\w*", r"optimi[sz]\w*",
    r"ideal\w*",
    r"better",
    r"ensure\w*",
    r"guarantee\w*",
    r"safe\b", r"safer\b", r"safest\b",          # "safeguards"/"safety" (data protection) are not banned
    r"risk-free",
    r"outperform\w*",
    r"beat the market",
    r"you need",
    r"you have to",
]
BANNED_DE = [
    r"vorschlag\w*", r"vorschläge\w*", r"vorgeschlagen\w*", r"vorschlagen", r"schlägt\w* \w+ vor", r"schlagen \w+ vor",
    r"empfehl\w*", r"empfiehl\w*", r"empfohlen\w*", r"empfehlung\w*",
    r"ratsam\w*", r"rät\b", r"raten\b", r"ratschlag\w*",
    r"sollte\w*", r"sollst\b", r"soll\b", r"sollen\b", r"muss\b", r"musst\b", r"müssen\b",
    r"am besten", r"beste[nmrs]?\b", r"bestens",   # (not "besteht"/"bestehen")
    r"optimal\w*", r"optimier\w*",
    r"ideal\w*",
    r"besser\w*",
    r"garantier\w*",
    r"sicher(?:e[mnrs]?)?\b",                      # "sicher", "sichere(n)"; plain "Sicherheit" (data protection) is not banned
    r"risikolos\w*", r"risikofrei\w*",
    r"unbedingt",
    r"du brauchst", r"brauchst du", r"du bräuchtest",
    r"anlageberatung", r"anlageempfehlung", r"kaufempfehlung", r"finanzberatung",
]

# --------------------------------------------------------------------------- ALLOWLIST (keep it minimal and explicit)
# Exact phrases that contain a banned word but NEGATE advice or are a plain technical statement. The phrase is cut out of the
# text before the banned terms are searched (case-insensitive). Anything not listed here fails.
ALLOWLIST = [
    # --- disclaimers that NEGATE advice (footer, guides, FAQ, privacy pages, README)
    "not investment advice",                 # "Planning tool, not investment advice."
    "no investment advice",
    "give investment advice",                # FAQ: "Does Finplanr give investment advice?" / "... does not give investment advice"
    "not provide investment or tax advice",  # guide, risk note
    "keine anlageberatung",                  # DE footer "Planungswerkzeug, keine Anlageberatung."
    "gibt finplanr anlageberatung",          # DE FAQ question
    "no recommendation",                     # negations: "no recommendation(s)"
    "keine empfehlung",                      # negations: "keine Empfehlung(en)"; also covers the DE example chip "Beispielplan – keine Empfehlung"
    "not a recommendation",                  # EN example chip "Example plan – not a recommendation": it NEGATES a recommendation (the preset plan is only an example)
    # --- input validation (UI error messages, not about investments)
    "at least one category must remain",
    "mindestens eine kategorie muss bleiben",
    # --- statutory term of art in the privacy text (section 25(2) TDDDG: "unbedingt erforderlich")
    "unbedingt erforderlich",
]
# (path suffix, exact phrase): allowed only in that file, e.g. the README sentence that names the guard itself.
FILE_ALLOWLIST = [
    ("README.md", "advice-like words"),
]

ATTRS = {"title", "alt", "aria-label", "placeholder", "value", "content", "aria-description"}
SKIP_META_CONTENT = {"viewport", "theme-color", "color-scheme", "robots", "referrer", "format-detection"}

BANNED_RE = re.compile(r"(?<![\w-])(?:" + "|".join(BANNED_EN + BANNED_DE) + r")\b", re.I)
ALLOW_RE = re.compile("|".join(re.escape(p) for p in sorted(ALLOWLIST, key=len, reverse=True)), re.I)

STRING_RE = re.compile(r"""'((?:[^'\\\n]|\\.)*)'|"((?:[^"\\\n]|\\.)*)"|`((?:[^`\\]|\\.)*)`""", re.S)


def unescape_js(s):
    return re.sub(r"\\(u[0-9a-fA-F]{4}|.)",
                  lambda m: chr(int(m.group(1)[1:], 16)) if len(m.group(1)) == 5 else {"n": "\n", "t": "\t"}.get(m.group(1), m.group(1)), s)


def scan_text(text):
    """Return the banned terms found in text after cutting out the allowlisted phrases."""
    cleaned = ALLOW_RE.sub(lambda m: " " * len(m.group(0)), text)
    return [m.group(0) for m in BANNED_RE.finditer(cleaned)]


class Extractor(HTMLParser):
    """Collect (line, kind, text) for everything a visitor can read in an HTML file."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items = []
        self.skip = 0          # inside <style>
        self.script = None     # None, or the type of the open <script>
        self.script_start = 0

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        a = dict(attrs)
        if tag == "style":
            self.skip += 1
        elif tag == "script":
            self.script = (a.get("type") or "text/javascript").lower()
            self.script_start = line
        elif tag == "meta" and (a.get("name") or "").lower() in SKIP_META_CONTENT:
            return
        for k, v in attrs:
            if k in ATTRS and v and not (tag == "input" and k == "value" and (a.get("type") or "").lower() in ("radio", "checkbox", "number", "hidden")):
                self.items.append((line, "attr %s" % k, v))

    def handle_endtag(self, tag):
        if tag == "style" and self.skip:
            self.skip -= 1
        elif tag == "script":
            self.script = None

    def handle_data(self, data):
        if self.skip or not data.strip():
            return
        line = self.getpos()[0]
        if self.script is not None:
            if "json" in self.script:
                for i, l in enumerate(data.split("\n")):
                    for m in re.finditer(r'"description"\s*:\s*"((?:[^"\\]|\\.)*)"', l):
                        self.items.append((line + i, "json-ld", unescape_js(m.group(1))))
            else:
                self.items.extend(js_strings(data, line))
            return
        for i, l in enumerate(data.split("\n")):
            if l.strip():
                self.items.append((line + i, "text", l.strip()))


def strip_js_comments(src):
    """Blank out // and /* */ comments while leaving string literals alone."""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c in "'\"`":
            q, j = c, i + 1
            while j < n and src[j] != q:
                j += 2 if src[j] == "\\" else 1
                if q != "`" and j < n and src[j] == "\n":
                    break
            out.append(src[i:j + 1]); i = j + 1
        elif src.startswith("//", i) and (i == 0 or src[i - 1] != ":"):
            j = src.find("\n", i)
            j = n if j == -1 else j
            out.append(" " * (j - i)); i = j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j == -1 else j + 2
            out.append("".join(ch if ch == "\n" else " " for ch in src[i:j])); i = j
        else:
            out.append(c); i += 1
    return "".join(out)


def js_strings(data, first_line):
    items = []
    code = strip_js_comments(data)
    for m in STRING_RE.finditer(code):
        s = next(g for g in m.groups() if g is not None)
        if not re.search(r"[A-Za-zÄÖÜäöüß]{3}", s):
            continue
        line = first_line + code.count("\n", 0, m.start())
        items.append((line, "script string", unescape_js(s)))
    return items


def scan_html(path):
    p = Extractor()
    p.feed(path.read_text(encoding="utf-8"))
    return p.items


def scan_md(path):
    items = []
    for i, l in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if l.strip():
            items.append((i, "text", l))
    return items


def collect(dist, src):
    files = []
    if dist:
        for p in sorted(Path(dist).rglob("*.html")):
            files.append((p, scan_html))
    if src:
        site = ROOT / "site"
        for p in sorted(site.rglob("*.html")):
            if "logos" not in p.relative_to(site).parts:
                files.append((p, scan_html))
        files.append((ROOT / "tools" / "og-image.html", scan_html))
        files.append((ROOT / "README.md", scan_md))
        for p in sorted((ROOT / "parked-for-later").glob("datenschutz-text.*.md")):
            files.append((p, scan_md))
    return [(p, f) for p, f in files if p.is_file()]


def check(dist=None, src=False):
    """Return a list of (file, line, kind, term, excerpt). Also used by tools/build.py."""
    hits = []
    for path, fn in collect(dist, src):
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            rel = path
        for line, kind, text in fn(path):
            if any(str(path).endswith(sfx) and ph.lower() in text.lower() for sfx, ph in FILE_ALLOWLIST):
                continue
            for term in scan_text(text):
                at = text.lower().find(term.lower())
                excerpt = text[max(0, at - 30):at + len(term) + 30].replace("\n", " ")
                hits.append((str(rel), line, kind, term, excerpt))
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fail when advice-like wording appears in the built site (or the sources).")
    ap.add_argument("--dist", default=str(ROOT / "dist"), help="build directory to scan (default: dist/)")
    ap.add_argument("--no-dist", action="store_true", help="do not scan the build directory")
    ap.add_argument("--src", action="store_true", help="also scan site/, README.md, privacy texts and og-image source")
    args = ap.parse_args(argv)
    dist = None if args.no_dist else Path(args.dist)
    if dist is not None and not dist.is_dir():
        print("error: %s is not a directory (run tools/build.py first, or use --no-dist --src)" % dist, file=sys.stderr)
        return 2
    hits = check(dist, args.src)
    if hits:
        print("wording guard FAILED: %d advice-like term(s) found" % len(hits), file=sys.stderr)
        for f, line, kind, term, ex in hits:
            print("  %s:%d [%s] '%s' ... %s" % (f, line, kind, term, ex), file=sys.stderr)
        print("Finplanr must only calculate from entered values. Reword the text (see BANNED_* / ALLOWLIST at the top of tools/check-wording.py).", file=sys.stderr)
        return 1
    print("wording guard ok (no advice-like terms)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
