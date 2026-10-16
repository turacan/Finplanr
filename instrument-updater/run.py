#!/usr/bin/env python3
"""Daily refresh of the instrument index (instruments.v1.json) inside the instrument-updater container.

    python3 -I -B run.py [daemon|once]

  daemon (default)  Wait for the next UPDATE_AT (local time of TZ), run the update, repeat. At start the index is built
                    once, but only if DATA_DIR/instruments.v1.json does not exist yet (seed). At most one successful
                    run per calendar day. A failed run is retried once after RETRY_DELAY seconds, then it waits for
                    the next day.
  once              Run one update now (manual run, ignores the one-per-day rule) and exit 0 (ok) / 1 (failed).

One update = `python3 -I TOOLS_DIR/fetch-instruments.py --refresh --out DATA_DIR/instruments.v1.json.tmp [FETCH_ARGS]`,
then checks (size, JSON, "v":1, row count at least MIN_ROWS_RATIO of the current file, tools/validate-instruments.py),
then an atomic os.replace onto the live file. On any failure the live file stays untouched.

Environment (all optional):
  TZ              time zone for UPDATE_AT, default Europe/Berlin (falls back to UTC with a warning if tz data is missing)
  UPDATE_AT       HH:MM, default 00:30
  FETCH_ARGS      extra arguments for the fetch script (shell-style quoting), default empty
  DATA_DIR        default /data (live index, status file, lock file)
  TOOLS_DIR       default /app/tools
  RUN_TIMEOUT     seconds per fetch run, default 3600 (the very first run needs ~30 min: OpenFIGI rate limit; later runs 1-5 min)
  RETRY_DELAY     seconds before the single retry, default 1800
  MIN_ROWS_RATIO  new index must have at least this share of the current row count, default 0.7 (0 disables the check)
  HEARTBEAT_FILE  touched at least every minute (container health check), default <tmp dir>/updater.alive

Status file DATA_DIR/instruments.status.json: lastRun, lastSuccess, built, rows, error, nextRun (UTC ISO strings).
Stdlib only, Python 3.9+ (zoneinfo).
"""
import fcntl
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import tempfile
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path

LIVE_NAME = "instruments.v1.json"
STATUS_NAME = "instruments.status.json"
LOCK_NAME = ".updater.lock"
MIN_BYTES = 100 * 1024
TICK = 60  # re-check the wall clock at least this often (survives clock jumps)


def parse_hhmm(text):
    m = re.fullmatch(r"\s*([01]?\d|2[0-3]):([0-5]\d)\s*", text or "")
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def load_tz(name):
    """Return (tzinfo, warning or None)."""
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name), None
    except Exception as e:  # missing tz database, unknown name, old Python
        return timezone.utc, "time zone %r not available (%s): using UTC" % (name, e.__class__.__name__)


def slot_on(day, hh, mm, tz):
    """The instant (UTC) of hh:mm local time on `day`. A wall time inside a DST gap resolves to the instant just after it."""
    return datetime(day.year, day.month, day.day, hh, mm, tzinfo=tz).astimezone(timezone.utc)


def next_slot(now, hh, mm, tz):
    """First slot strictly after `now` (aware datetime)."""
    today = now.astimezone(tz).date()
    for add in range(0, 3):
        cand = slot_on(today + timedelta(days=add), hh, mm, tz)
        if cand > now:
            return cand
    raise RuntimeError("no next slot found")  # unreachable


def iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


class Updater:
    def __init__(self, environ=None, clock=None, sleeper=None, out=None):
        e = os.environ if environ is None else environ
        self.out = out or sys.stdout
        self.data = Path(e.get("DATA_DIR") or "/data")
        self.tools = Path(e.get("TOOLS_DIR") or "/app/tools")
        self.timeout = self._num(e.get("RUN_TIMEOUT"), 3600, int)
        self.retry_delay = self._num(e.get("RETRY_DELAY"), 1800, int)
        self.min_ratio = self._num(e.get("MIN_ROWS_RATIO"), 0.7, float)
        try:
            self.fetch_args = shlex.split(e.get("FETCH_ARGS") or "")
        except ValueError:
            self.fetch_args = []
            self.warn_later = "FETCH_ARGS ignored (invalid quoting)"
        self.tmp_dir = Path(tempfile.gettempdir())
        self.heartbeat_file = Path(e.get("HEARTBEAT_FILE") or (self.tmp_dir / "updater.alive"))
        self.stop = threading.Event()
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.sleeper = sleeper or self.stop.wait
        self.live = self.data / LIVE_NAME
        self.tmp = self.data / (LIVE_NAME + ".tmp")
        self.status_path = self.data / STATUS_NAME
        self.status = {"lastRun": None, "lastSuccess": None, "built": None, "rows": None, "error": None, "nextRun": None}
        self.tz, tzwarn = load_tz(e.get("TZ") or "Europe/Berlin")
        self.tzname = e.get("TZ") or "Europe/Berlin"
        hm = parse_hhmm(e.get("UPDATE_AT") or "00:30")
        self.hhmm_warn = None
        if hm is None:
            self.hhmm_warn = "UPDATE_AT %r is not HH:MM: using 00:30" % e.get("UPDATE_AT")
            hm = (0, 30)
        self.hh, self.mm = hm
        self.pending_warnings = [w for w in (tzwarn, self.hhmm_warn, getattr(self, "warn_later", None)) if w]
        self.child = None

    @staticmethod
    def _num(v, default, cast):
        try:
            return cast(v) if v not in (None, "") else default
        except ValueError:
            return default

    # ------------------------------------------------------------------ small helpers
    def log(self, msg):
        ts = self.clock().astimezone(self.tz).strftime("%Y-%m-%dT%H:%M:%S%z")
        print("%s %s" % (ts, msg), file=self.out, flush=True)

    def beat(self):
        try:
            self.heartbeat_file.touch()
        except OSError:
            pass

    def write_status(self, **upd):
        self.status.update(upd)
        try:
            tmp = self.status_path.with_name(STATUS_NAME + ".tmp")
            tmp.write_text(json.dumps(self.status, indent=1) + "\n", encoding="utf-8")
            os.chmod(tmp, 0o644)
            os.replace(tmp, self.status_path)
        except OSError as ex:
            self.log("warning: cannot write status file: %s" % ex)

    def load_status(self):
        try:
            old = json.loads(self.status_path.read_text(encoding="utf-8"))
            if isinstance(old, dict):
                for k in self.status:
                    if k in old:
                        self.status[k] = old[k]
        except (OSError, ValueError):
            pass

    def live_info(self):
        """(built, rows) of the live file, or (None, None)."""
        try:
            idx = json.loads(self.live.read_text(encoding="utf-8"))
            return idx.get("built"), len(idx.get("rows") or [])
        except (OSError, ValueError, AttributeError):
            return None, None

    def done_today(self):
        last = parse_iso(self.status.get("lastSuccess"))
        if last is None:
            return False
        return last.astimezone(self.tz).date() == self.clock().astimezone(self.tz).date()

    # ------------------------------------------------------------------ waiting
    def wait_until(self, target, slot=False):
        """Sleep until `target` (aware datetime). Re-reads the wall clock at least every TICK seconds, so a clock jump
        forward fires immediately and a jump backward just waits longer (for a slot target a nearer slot is adopted).
        Returns False if a stop was requested."""
        while not self.stop.is_set():
            self.beat()
            now = self.clock()
            if now >= target:
                return True
            if slot:
                nxt = next_slot(now, self.hh, self.mm, self.tz)
                if nxt < target:
                    target = nxt
            self.sleeper(max(0.05, min(TICK, (target - now).total_seconds())))
        return False

    def wait_slot(self):
        target = next_slot(self.clock(), self.hh, self.mm, self.tz)
        self.write_status(nextRun=iso(target))
        self.log("next update at %s (%s)" % (target.astimezone(self.tz).strftime("%Y-%m-%d %H:%M %Z"), self.tzname))
        return self.wait_until(target, slot=True)

    def wait_delay(self, seconds):
        return self.wait_until(self.clock() + timedelta(seconds=seconds))

    # ------------------------------------------------------------------ one update
    def run_update(self):
        """Returns (ok, error text)."""
        try:
            self.data.mkdir(parents=True, exist_ok=True)
            lock = open(self.data / LOCK_NAME, "a")
        except OSError as ex:
            return self._fail("cannot open data dir %s: %s" % (self.data, ex))
        try:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                return self._fail("another update is already running (lock held)")
            return self._locked_update()
        finally:
            lock.close()

    def _fail(self, err):
        self.log("update FAILED: %s" % err)
        self.write_status(error=err)
        return False, err

    def _cleanup(self):
        for p in (self.tmp, self.tmp.with_name(self.tmp.name + ".tmp")):
            try:
                p.unlink()
            except OSError:
                pass

    def _locked_update(self):
        t0 = self.clock()
        self.write_status(lastRun=iso(t0), error=None)
        fetch = self.tools / "fetch-instruments.py"
        if not fetch.is_file():
            return self._fail("%s not found (is ./tools mounted?)" % fetch)
        self._cleanup()
        old_built, old_rows = self.live_info()
        cmd = [sys.executable, "-I", "-B", str(fetch), "--refresh", "--out", str(self.tmp)] + self.fetch_args
        self.log("update started: %s" % " ".join(shlex.quote(c) for c in cmd[3:]))
        logf = tempfile.NamedTemporaryFile("w+b", dir=str(self.tmp_dir), prefix="fetch-", suffix=".log", delete=False)
        try:
            ok, err = self._run_child(cmd, logf)
            tail = self._tail(logf.name)
        finally:
            logf.close()
            try:
                os.unlink(logf.name)
            except OSError:
                pass
        if not ok:
            self._cleanup()
            if tail:
                self.log("fetch output (last lines):\n  " + "\n  ".join(tail))
            return self._fail(err)
        try:
            idx = self._verify(self.tmp, old_rows)
        except ValueError as ex:
            self._cleanup()
            return self._fail("rejected new index, kept the old one: %s" % ex)
        try:
            os.chmod(self.tmp, 0o644)
            os.replace(self.tmp, self.live)
        except OSError as ex:
            self._cleanup()
            return self._fail("cannot install the new index: %s" % ex)
        rows = len(idx["rows"])
        secs = int((self.clock() - t0).total_seconds())
        self.log("update OK: %d rows (was %s), built %s, %d s" % (rows, old_rows if old_rows is not None else "-", idx.get("built"), secs))
        self.write_status(lastSuccess=iso(self.clock()), built=idx.get("built"), rows=rows, error=None)
        return True, None

    def _run_child(self, cmd, logf):
        try:
            self.child = subprocess.Popen(cmd, stdout=logf, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                          cwd=str(self.tmp_dir), start_new_session=True)
        except OSError as ex:
            return False, "cannot start the fetch script: %s" % ex
        proc = self.child
        waited = 0.0
        try:
            while True:
                try:
                    rc = proc.wait(timeout=1)
                    break
                except subprocess.TimeoutExpired:
                    waited += 1
                    if waited % 20 == 0 or waited < 2:
                        self.beat()
                    if self.stop.is_set():
                        self._kill(proc)
                        return False, "interrupted by shutdown"
                    if waited >= self.timeout:
                        self._kill(proc)
                        return False, "timeout after %d s (killed)" % self.timeout
        finally:
            self.child = None
        if rc != 0:
            return False, "fetch script exited with code %s" % rc
        if not self.tmp.is_file():
            return False, "fetch script reported success but wrote no file"
        return True, None

    @staticmethod
    def _kill(proc):
        for sig, grace in ((signal.SIGTERM, 5), (signal.SIGKILL, 5)):
            try:
                os.killpg(proc.pid, sig)
            except (ProcessLookupError, PermissionError, OSError):
                pass
            try:
                proc.wait(timeout=grace)
                return
            except subprocess.TimeoutExpired:
                continue

    @staticmethod
    def _tail(path, n=10):
        try:
            data = Path(path).read_bytes()[-4000:].decode("utf-8", "replace")
        except OSError:
            return []
        return [l.rstrip() for l in data.splitlines() if l.strip()][-n:]

    def _verify(self, path, old_rows):
        """Sanity checks on the freshly built file. Returns the parsed index; raises ValueError with the reason."""
        size = path.stat().st_size
        if size < MIN_BYTES:
            raise ValueError("file too small (%d bytes)" % size)
        try:
            idx = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as ex:
            raise ValueError("not valid JSON (%s)" % ex)
        if not isinstance(idx, dict) or idx.get("v") != 1:
            raise ValueError('contract version is not "v":1')
        rows = idx.get("rows")
        if not isinstance(rows, list) or not rows:
            raise ValueError("no rows")
        if old_rows and self.min_ratio > 0 and len(rows) < self.min_ratio * old_rows:
            raise ValueError("only %d rows, the current index has %d (minimum %.0f%%; set MIN_ROWS_RATIO=0 for a deliberate "
                             "reduction)" % (len(rows), old_rows, self.min_ratio * 100))
        validator = self.tools / "validate-instruments.py"
        if validator.is_file():
            try:
                r = subprocess.run([sys.executable, "-I", "-B", str(validator), str(path)], capture_output=True,
                                   timeout=300, cwd=str(self.tmp_dir))
            except (OSError, subprocess.TimeoutExpired) as ex:
                raise ValueError("validate-instruments.py did not run (%s)" % ex.__class__.__name__)
            if r.returncode != 0:
                lines = [l for l in r.stdout.decode("utf-8", "replace").splitlines() if l.strip()][:4]
                raise ValueError("validate-instruments.py: " + " | ".join(lines))
        return idx

    # ------------------------------------------------------------------ modes
    def attempt(self):
        """One update plus the single delayed retry. Returns True on success."""
        ok, err = self.run_update()
        if not ok and not self.stop.is_set() and "lock held" not in (err or ""):
            self.log("retry in %d min" % (self.retry_delay // 60))
            if self.wait_delay(self.retry_delay):
                ok, err = self.run_update()
        if not ok and not self.stop.is_set():
            self.log("giving up until the next scheduled run; the previous index stays in place")
        return ok

    def start(self):
        for w in self.pending_warnings:
            self.log("warning: " + w)
        self.pending_warnings = []
        self.load_status()
        try:
            self.data.mkdir(parents=True, exist_ok=True)
        except OSError as ex:
            self.log("warning: cannot create %s: %s" % (self.data, ex))
        built, rows = self.live_info()
        if built is not None:
            self.write_status(built=built, rows=rows)

    def daemon(self):
        self.start()
        self.log("instrument updater started: daily at %02d:%02d (%s), data dir %s" % (self.hh, self.mm, self.tzname, self.data))
        if not self.live.exists():
            self.log("no %s yet: seeding now" % LIVE_NAME)
            self.attempt()
        while not self.stop.is_set():
            if not self.wait_slot():
                break
            if self.done_today():
                self.log("already updated successfully today: skipping")
                continue
            self.attempt()
        self.log("stopped")
        return 0

    def once(self):
        self.start()
        ok, _ = self.run_update()
        return 0 if ok else 1


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    mode = argv[0] if argv else "daemon"
    if mode not in ("daemon", "once"):
        print("usage: run.py [daemon|once]", file=sys.stderr)
        return 2
    u = Updater()

    def on_signal(signum, frame):
        u.stop.set()

    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    return u.daemon() if mode == "daemon" else u.once()


if __name__ == "__main__":
    sys.exit(main())
