#!/usr/bin/env python3
"""Safety net: make sure nothing personal or infrastructure-specific is about to be committed.

    python3 -I tools/check-repo.py            # run this before EVERY commit (the git hook .githooks/pre-commit does it for you)

It reads the local, git-ignored config/operator.json and scans, case-insensitively,
  * every file known to git (git ls-files: the staged version via `git show :path`, and the working-tree version),
  * every file named by `git diff --cached --name-only`,
  * every untracked file that is not ignored (a plain `git add -A` would stage it),
and the file names themselves, for
  * every operator value of the config (name, each address line, e-mail, Impressum URL incl. host/path, Impressum provider,
    mailbox provider strings, "forbidden_extra" entries),
  * a built-in list of infrastructure / personal markers (hardware brand, mount paths, user name, host and home-directory names),
  * token-like strings (JWT-style tokens, API keys, private keys, TUNNEL_TOKEN assignments).
Offenders are listed with file, line and WHICH rule matched (the matched value itself is never printed).

Exit codes: 0 clean, 1 offenders found, 2 usage/git error. Stdlib only.
Options: --repo DIR (check another git repository, default: this one), --config FILE (default: config/operator.json).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Built-in markers. They are assembled from pieces so that this very file does not trigger itself.
BUILTIN = {
    "hardware brand": "UGRE" + "EN",
    "NAS mount path": "/vol" + "ume1",
    "user name": "tura" + "can",
    "workstation host name": "DESK" + "TOP-",
    "home directory": "/home/" + "dev" + "user",
}

TOKEN_PATTERNS = [
    ("JWT/base64 token (eyJ...)", re.compile(r"eyJ[A-Za-z0-9_-]{30,}")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("TUNNEL_TOKEN assignment", re.compile(r"TUNNEL_TOKEN\s*[=:]\s*(?!replace_me\b)[\"']?[A-Za-z0-9_+/=.-]{16,}")),
    ("generic secret assignment", re.compile(r"(?i)\b(?:api[_-]?key|secret|passw(?:or)?d|token)\b\s*[=:]\s*[\"'][A-Za-z0-9_+/=.-]{24,}[\"']")),
    ("long random-looking string", re.compile(r"(?<![A-Za-z0-9+/=_.-])(?=[A-Za-z0-9+/_-]*[A-Z])(?=[A-Za-z0-9+/_-]*[a-z])(?=[A-Za-z0-9+/_-]*[0-9])[A-Za-z0-9+/_-]{56,}(?![A-Za-z0-9+/=_.-])")),
]


def git(repo, *args, text=True):
    r = subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8", "replace") if text else r.stdout


def needles_from_config(cfg):
    """Return list of (label, lowercase needle)."""
    out = []

    def add(label, v):
        if isinstance(v, str) and len(v.strip()) >= 4:
            out.append((label, v.strip().lower()))

    for k in ("operator_name", "email", "impressum_provider_name", "copyright_holder", "mailbox_provider_name",
              "mailbox_provider_address_de", "mailbox_provider_address_en", "mailbox_recipient_de", "mailbox_recipient_en",
              "mailbox_transfer_de", "mailbox_transfer_en"):
        add("config:" + k, cfg.get(k))
    for i, line in enumerate(cfg.get("address_lines") or []):
        add("config:address_lines[%d]" % i, line)
    url = cfg.get("impressum_url")
    if isinstance(url, str) and url:
        add("config:impressum_url", url)
        no_scheme = re.sub(r"^[a-z]+://", "", url.strip().lower()).rstrip("/")
        add("config:impressum_url(host+path)", no_scheme)
        add("config:impressum_url(host)", no_scheme.split("/")[0])
    for i, v in enumerate(cfg.get("forbidden_extra") or []):
        add("config:forbidden_extra[%d]" % i, v)
    seen, uniq = set(), []
    for label, n in out:
        if (label, n) not in seen:
            seen.add((label, n))
            uniq.append((label, n))
    return uniq


# The operator's NAME (only the name, never address, email or infrastructure) may appear in the
# copyright notice of these files, as is conventional for a licence/README.
NAME_LABELS = {"builtin:user name", "config:operator_name", "config:copyright_holder"}
NAME_ALLOWED_FILES = {"README.md", "LICENSE"}


def scan_text(where, text, needles, findings, skip_labels=frozenset()):
    low = text.lower()
    for label, n in needles:
        if label in skip_labels:
            continue
        start = 0
        while True:
            i = low.find(n, start)
            if i == -1:
                break
            findings.append((where, low.count("\n", 0, i) + 1, label))
            start = i + len(n)
            break  # one report per rule and file is enough
    for label, rx in TOKEN_PATTERNS:
        m = rx.search(text)
        if m:
            findings.append((where, text.count("\n", 0, m.start()) + 1, "token-like: " + label))


def is_binary(b):
    return b"\0" in b[:8000]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Scan git-tracked/staged files for personal data and secrets.")
    ap.add_argument("--repo", default=str(ROOT))
    ap.add_argument("--config", default=None)
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    cfg_path = Path(args.config) if args.config else repo / "config" / "operator.json"
    if git(repo, "rev-parse", "--git-dir") is None:
        print("check-repo: %s is not a git repository" % repo, file=sys.stderr)
        return 2

    needles = [(("builtin:" + k), v.lower()) for k, v in BUILTIN.items()]
    if cfg_path.is_file():
        try:
            needles += needles_from_config(json.loads(cfg_path.read_text(encoding="utf-8")))
        except (OSError, ValueError) as e:
            print("check-repo: cannot read %s: %s" % (cfg_path, e), file=sys.stderr)
            return 2
    else:
        print("check-repo: WARNING: %s not found - operator values are NOT checked (built-in markers and tokens only)" % cfg_path, file=sys.stderr)

    names = set()
    for cmd in (("ls-files", "-z"), ("diff", "--cached", "--name-only", "-z"), ("ls-files", "-z", "--others", "--exclude-standard")):
        raw = git(repo, *cmd, text=False)
        if raw is None:
            print("check-repo: git %s failed" % " ".join(cmd), file=sys.stderr)
            return 2
        names.update(x.decode("utf-8", "replace") for x in raw.split(b"\0") if x)

    findings, checked = [], 0
    for name in sorted(names):
        # file name itself
        scan_text(name + " (file name)", name, [n for n in needles], findings)
        # staged / committed-to-be version
        staged = git(repo, "show", ":" + name, text=False)
        versions = []
        if staged is not None:
            versions.append(("staged", staged))
        wt = repo / name
        if wt.is_file():
            try:
                versions.append(("worktree", wt.read_bytes()))
            except OSError:
                pass
        for kind, data in versions:
            if is_binary(data):
                continue
            skip = NAME_LABELS if name in NAME_ALLOWED_FILES else frozenset()
            scan_text("%s [%s]" % (name, kind), data.decode("utf-8", "replace"), needles, findings, skip)
        if versions:
            checked += 1

    if findings:
        print("check-repo: FOUND personal/infrastructure data or secrets in files that would be committed:", file=sys.stderr)
        for where, line, label in sorted(set(findings)):
            print("  %s: line %d: %s" % (where, line, label), file=sys.stderr)
        print("Move the value into config/operator.json (placeholder {{KEY}}) or remove it, then run this check again.", file=sys.stderr)
        return 1
    print("check-repo: clean (%d files checked, %d operator/built-in rules)" % (checked, len(needles)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
