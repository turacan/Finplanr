#!/usr/bin/env bash
# Finplanr deploy helper (WSL/Linux). Mirrors the built site (dist/) into the server's project folder through a mounted
# share, optionally recreates the web container over SSH, and checks the live site.
#
#   tools/deploy.sh release [--yes] [--no-build] [--no-ssh]   EVERYTHING: mount if needed, build, mirror site + config + updater files,
#                                                              recreate the web container over SSH, wait, live check
#   tools/deploy.sh site    [--yes] [--dry-run] [--no-build]   build + mirror dist/ -> <project>/site only (stale files are deleted)
#   tools/deploy.sh all     [--yes] [--dry-run] [--no-build]   site + config/default.conf + updater scripts (no container restart)
#   tools/deploy.sh check                                       live check of the public site (all lines must say ok)
#   tools/deploy.sh mount                                       only mount the share
#
# Setup (once): copy config/deploy.env.example to config/deploy.env (git-ignored) and fill it in.
# Never touched on the server: docker-compose.yaml, tunnel.env, instruments-data/, instruments-cache/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ENV_FILE="${DEPLOY_ENV:-$ROOT/config/deploy.env}"
[ -f "$ENV_FILE" ] && . "$ENV_FILE"
NAS_PROJECT_DIR="${NAS_PROJECT_DIR:-}"      # mounted project folder (contains site/, config/, docker-compose.yaml)
NAS_MOUNT_SPEC="${NAS_MOUNT_SPEC:-}"        # optional: what to mount automatically (drive like Z: or a share path)
NAS_MOUNT_POINT="${NAS_MOUNT_POINT:-}"      # optional: where it is mounted in WSL
NAS_SSH="${NAS_SSH:-}"                      # optional: user@host for the container recreate
NAS_REMOTE_DIR="${NAS_REMOTE_DIR:-}"        # optional: project folder path ON the server (for docker compose -f)
SITE_URL="${SITE_URL:-https://finplanr.net}"

die() { echo "ERROR: $*" >&2; exit 1; }
info() { echo "== $*"; }

cmd="${1:-}"; [ $# -gt 0 ] && shift || true
YES=0; DRY=0; BUILD=1; SSH=1
for a in "$@"; do
  case "$a" in
    --yes) YES=1 ;; --dry-run) DRY=1 ;; --no-build) BUILD=0 ;; --no-ssh) SSH=0 ;;
    *) die "unknown option: $a" ;;
  esac
done

# ------------------------------------------------------------------------------------------------ live check
live_check() {
  command -v curl >/dev/null || die "curl is required"
  local H="$SITE_URL" bad=0 e c
  for e in 200:/ 200:/de/ 200:/anleitung.html 200:/en/datenschutz.html 200:/style.css 200:/robots.txt 200:/sitemap.xml \
           200:/data/instruments.v1.json 301:/de 404:/.env 404:/.env.php/ 404:/.env.backup 404:/application/config/.env \
           404:/.git/config 404:/db.sql 404:/site.zip 404:/notes.md 404:/docker-compose.yaml 404:/default.conf \
           404:/tunnel.env 404:/operator.json 404:/index.html.bak 404:/LICENSE 404:/data/instruments.status.json 404:/data/ 404:/logos/; do
    c=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 --path-as-is "$H${e#*:}" || true)
    if [ "$c" = "${e%%:*}" ]; then echo "ok   $c ${e#*:}"; else echo "FAIL $c ${e#*:} (expected ${e%%:*})"; bad=$((bad+1)); fi
  done
  if [ "$bad" -eq 0 ]; then info "live check: all ok"; else info "live check: $bad line(s) FAILED"; return 1; fi
}

# ------------------------------------------------------------------------------------------------ mount
project_ok() { [ -n "$NAS_PROJECT_DIR" ] && [ -d "$NAS_PROJECT_DIR" ] && { [ -f "$NAS_PROJECT_DIR/docker-compose.yaml" ] || [ -f "$NAS_PROJECT_DIR/tunnel.env" ]; }; }
ensure_mount() {
  if project_ok; then return 0; fi
  if [ -n "$NAS_MOUNT_SPEC" ] && [ -n "$NAS_MOUNT_POINT" ]; then
    info "share not mounted: mounting $NAS_MOUNT_SPEC on $NAS_MOUNT_POINT (sudo may ask for your WSL password)"
    sudo mkdir -p "$NAS_MOUNT_POINT"
    sudo mount -t drvfs "$NAS_MOUNT_SPEC" "$NAS_MOUNT_POINT" || die "mount failed (is the share reachable from Windows?)"
  fi
  project_ok || die "project folder not found or no marker files (docker-compose.yaml / tunnel.env) in: ${NAS_PROJECT_DIR:-<NAS_PROJECT_DIR not set>}"
}

[ "$cmd" = "check" ] && { live_check; exit $?; }
[ "$cmd" = "mount" ] && { [ -n "$NAS_PROJECT_DIR" ] || die "NAS_PROJECT_DIR is not set"; ensure_mount; info "mounted: $NAS_PROJECT_DIR"; exit 0; }
case "$cmd" in release|site|all) ;; *) die "usage: tools/deploy.sh release|site|all|check|mount [--yes] [--dry-run] [--no-build] [--no-ssh]" ;; esac

# ------------------------------------------------------------------------------------------------ safety checks
[ -n "$NAS_PROJECT_DIR" ] || die "NAS_PROJECT_DIR is not set (create config/deploy.env from config/deploy.env.example)"
NAS_PROJECT_DIR="${NAS_PROJECT_DIR%/}"
case "$NAS_PROJECT_DIR" in ""|"/"|"/mnt"|"/home"|"$HOME") die "refusing to use $NAS_PROJECT_DIR as the project folder" ;; esac
ensure_mount
TARGET="$NAS_PROJECT_DIR/site"
mkdir -p "$TARGET"
command -v rsync >/dev/null || die "rsync is required (sudo apt install rsync)"

if [ "$BUILD" -eq 1 ]; then
  info "build"
  python3 -I tools/build.py | tail -n 3
fi
[ -f dist/index.html ] && [ -f dist/de/index.html ] || die "dist/ is missing or incomplete: run python3 -I tools/build.py"
if grep -rIl --include='*.html' '{{' dist >/dev/null 2>&1; then die "unfilled {{placeholder}} in dist/ (config/operator.json missing?)"; fi
python3 -I tools/check-wording.py >/dev/null || die "wording guard failed on dist/"
python3 -I tools/check-repo.py >/dev/null || die "check-repo failed"

# compose files: this script does not deploy them, but warn if the server folder copy differs from the local one
if [ -f docker-compose.yaml ] && [ -f "$NAS_PROJECT_DIR/docker-compose.yaml" ] && ! cmp -s docker-compose.yaml "$NAS_PROJECT_DIR/docker-compose.yaml"; then
  echo "WARNING: docker-compose.yaml on the server differs from your local one. This script does not change it: update the UGOS project text (and the folder copy) yourself."
fi

# ------------------------------------------------------------------------------------------------ site mirror
# data/ is not deployed through site/ (the instrument file comes from instruments-data/ via the updater).
RS_OPTS=(-rc --delete --delete-excluded --no-perms --no-owner --no-group --omit-dir-times
         --exclude='data/' --exclude='.*' --exclude='Thumbs.db' --exclude='desktop.ini' --exclude='*:Zone.Identifier' --exclude='*~')
info "changes for $TARGET:"
CHANGES="$(rsync "${RS_OPTS[@]}" -n -i dist/ "$TARGET/" | grep -v '^\.' || true)"
if [ -z "$CHANGES" ]; then echo "(nothing to change)"; else echo "$CHANGES"; fi
NDEL=$(printf '%s\n' "$CHANGES" | grep -c '^\*deleting' || true)
NADD=$(printf '%s\n' "$CHANGES" | grep -c -E '^[<>c]' || true)
info "$NADD file(s) to add/update, $NDEL stale file(s) to delete"

if [ "$DRY" -eq 1 ]; then info "dry run only: nothing written"; exit 0; fi
if [ "$YES" -ne 1 ]; then
  read -r -p "Apply to the server folder (and restart the web container if this is a release)? [y/N] " ans
  [ "$ans" = "y" ] || [ "$ans" = "Y" ] || die "aborted"
fi
rsync "${RS_OPTS[@]}" dist/ "$TARGET/"
info "site mirrored"

# ------------------------------------------------------------------------------------------------ config + updater files
UPDATER_CHANGED=0
if [ "$cmd" = "all" ] || [ "$cmd" = "release" ]; then
  if grep -q $'\r' config/default.conf; then die "config/default.conf contains CRLF line endings"; fi
  mkdir -p "$NAS_PROJECT_DIR/config" "$NAS_PROJECT_DIR/tools" "$NAS_PROJECT_DIR/instrument-updater"
  for pair in "config/default.conf:config/default.conf" "tools/fetch-instruments.py:tools/fetch-instruments.py" \
              "tools/validate-instruments.py:tools/validate-instruments.py" "instrument-updater/run.py:instrument-updater/run.py"; do
    src="${pair%%:*}"; dst="$NAS_PROJECT_DIR/${pair##*:}"
    if ! cmp -s "$src" "$dst" 2>/dev/null; then
      cp "$src" "$dst"; echo "updated ${pair##*:}"
      case "$src" in tools/*|instrument-updater/*) UPDATER_CHANGED=1 ;; esac
    fi
  done
  info "config/updater files are current on the server"
fi

# ------------------------------------------------------------------------------------------------ audit
info "audit of $TARGET (anything listed here will not be served or is unexpected):"
UNEXPECTED="$(cd "$TARGET" && find . -type f \
  \( -name '.*' -o -name '*:Zone.Identifier' -o -name 'Thumbs.db' -o -name 'desktop.ini' -o -name '*[A-Z]*' \
     -o ! -regex '.*\.\(html\|css\|xml\|svg\|png\|jpg\|jpeg\|webp\|ico\|txt\)$' \) -print)"
if [ -z "$UNEXPECTED" ]; then echo "(clean)"; else echo "$UNEXPECTED"; fi

# ------------------------------------------------------------------------------------------------ container recreate + live check
REMOTE_CMD="cd '$NAS_REMOTE_DIR' && sudo docker compose -f '$NAS_REMOTE_DIR/docker-compose.yaml' up -d --force-recreate finplanr"
[ "$UPDATER_CHANGED" -eq 1 ] && REMOTE_CMD="$REMOTE_CMD && sudo docker restart finplanr-instrument-updater"
if [ "$cmd" = "release" ]; then
  if [ "$SSH" -eq 1 ] && [ -n "$NAS_SSH" ] && [ -n "$NAS_REMOTE_DIR" ]; then
    info "recreating the web container on the server (ssh asks for your password; sudo may ask again)"
    ssh -t "$NAS_SSH" "$REMOTE_CMD" || die "remote command failed"
    info "waiting for the site to come back"
    for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
      c=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$SITE_URL/" || true); [ "$c" = "200" ] && break; sleep 5
    done
    live_check
    exit $?
  fi
  echo
  echo "NEXT STEP (run on the server): $REMOTE_CMD"
  echo "Then: tools/deploy.sh check"
else
  echo
  echo "NEXT STEPS: recreate the web container on the server: sudo docker compose -f ${NAS_REMOTE_DIR:-<project>}/docker-compose.yaml up -d --force-recreate finplanr"
  [ "$UPDATER_CHANGED" -eq 1 ] && echo "            and restart the updater:  sudo docker restart finplanr-instrument-updater"
  echo "            then verify:              tools/deploy.sh check"
fi
