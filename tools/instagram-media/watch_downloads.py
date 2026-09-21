#!/usr/bin/env python3
"""Watch ~/Downloads for an Instagram export and publish its stories.

Runs from a launchd agent: whenever ~/Downloads changes (and every 30 minutes
as a fallback) it looks for a finished Instagram export, and if it finds one it
hasn't seen, runs `pull.py sync --export …` and posts a macOS notification.

sync publishes: B asked for everything to be on /media/, and the account is
public. Posts and reels still come from the archive; the export adds its
stories, minus reshares (see igmedia/stories.py), each silent clip given
music. Set WATCH_ACTION = "stage" to go back to staging for review.

    watch_downloads.py            one check (what launchd runs)
    watch_downloads.py --install  install and start the launchd agent
    watch_downloads.py --uninstall
    watch_downloads.py --status

Standard library only; it shells out to the tool's own venv for staging.
"""

import json
import os
import plistlib
import subprocess
import sys
import time
import zipfile
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
PYTHON = TOOL_DIR / ".venv" / "bin" / "python"
PULL = TOOL_DIR / "pull.py"
STATE = TOOL_DIR / "build" / "watch-state.json"

WATCH_DIR = Path.home() / "Downloads"
LOG = Path.home() / "Library" / "Logs" / "brianpfeil-instagram-watch.log"

LABEL = "com.brianpfeil.instagram-watch"
PLIST = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"

# "sync" publishes (stage, approve all, encode, upload, commit, push);
# "stage" only prepares the approve list and review sheet.
WATCH_ACTION = "sync"

# Browsers write a download under a temporary name and rename it when done.
IN_PROGRESS_SUFFIXES = (".crdownload", ".download", ".part", ".partial", ".tmp")
# A finished file can still be flushing; leave anything touched this recently.
SETTLE_SECONDS = 120


def log(message: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")


def notify(title: str, message: str) -> None:
    # osascript strings are double-quoted; keep ours free of quotes.
    safe = message.replace('"', "'")
    subprocess.run(
        ["osascript", "-e", f'display notification "{safe}" with title "{title}"'],
        capture_output=True,
    )


def looks_like_export(path: Path) -> bool:
    """True for a ZIP Instagram produced.

    The name usually says "instagram", but a part-2-of-3 can hold nothing but
    media, so the contents are checked too rather than relying on either.
    """
    if path.suffix.lower() != ".zip" or path.name.lower().endswith(IN_PROGRESS_SUFFIXES):
        return False
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
    except (zipfile.BadZipFile, OSError):
        return False  # unreadable, or still being written
    if "instagram" in path.name.lower():
        return True
    return any("your_instagram_activity/" in n for n in names)


def settled(path: Path, now: float | None = None) -> bool:
    now = time.time() if now is None else now
    return now - path.stat().st_mtime >= SETTLE_SECONDS


def find_exports(directory: Path, now: float | None = None) -> list[Path]:
    """Finished Instagram export ZIPs in directory, sorted by name."""
    if not directory.is_dir():
        return []
    found = []
    for path in directory.iterdir():
        if not path.is_file() or path.name.startswith("."):
            continue
        if path.name.lower().endswith(IN_PROGRESS_SUFFIXES):
            continue
        if not settled(path, now):
            continue
        if looks_like_export(path):
            found.append(path)
    return sorted(found, key=lambda p: p.name)


def fingerprint(paths: list[Path]) -> list[list]:
    return [[p.name, p.stat().st_size] for p in paths]


def load_state(state_file: Path) -> dict:
    try:
        return json.loads(state_file.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state_file: Path, state: dict) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def check(directory: Path = WATCH_DIR, state_file: Path = STATE, stage=None) -> str:
    """One pass. Returns what happened, for the log and for tests."""
    exports = find_exports(directory)
    if not exports:
        return "no export"

    fp = fingerprint(exports)
    state = load_state(state_file)
    if state.get("staged") == fp:
        return "already staged"

    stage = stage or run_stage
    ok, output = stage(exports)
    if not ok:
        state["last_error"] = output[-500:]
        save_state(state_file, state)
        return f"stage failed: {output[-300:]}"

    save_state(state_file, {"staged": fp, "at": time.strftime("%Y-%m-%d %H:%M:%S")})
    return f"staged {len(exports)} archive(s): {output.strip().splitlines()[0] if output.strip() else ''}"


def run_stage(exports: list[Path]) -> tuple[bool, str]:
    proc = subprocess.run(
        [str(PYTHON), str(PULL), WATCH_ACTION, "--export", *map(str, exports)],
        capture_output=True, text=True, cwd=TOOL_DIR,
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr)


# --- launchd -------------------------------------------------------------

def plist_body() -> dict:
    return {
        "Label": LABEL,
        "ProgramArguments": [str(PYTHON), str(Path(__file__).resolve())],
        # Fires when ~/Downloads changes, i.e. when a browser renames a
        # finished download into place; the interval catches anything missed,
        # such as a file that was still settling on the first trigger.
        "WatchPaths": [str(WATCH_DIR)],
        "StartInterval": 1800,
        "RunAtLoad": True,
        "StandardOutPath": str(LOG),
        "StandardErrorPath": str(LOG),
        # A burst of Downloads activity shouldn't spawn a burst of checks.
        "ThrottleInterval": 60,
    }


def install() -> int:
    if not PYTHON.exists():
        print(f"no venv at {PYTHON}; run `make media-deps` first", file=sys.stderr)
        return 1
    PLIST.parent.mkdir(parents=True, exist_ok=True)
    with PLIST.open("wb") as fh:
        plistlib.dump(plist_body(), fh)
    domain = f"gui/{os.getuid()}"
    subprocess.run(["launchctl", "bootout", f"{domain}/{LABEL}"], capture_output=True)
    proc = subprocess.run(["launchctl", "bootstrap", domain, str(PLIST)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"launchctl bootstrap failed: {proc.stderr.strip()}", file=sys.stderr)
        return 1
    print(f"installed {PLIST}\nlog: {LOG}")
    return 0


def uninstall() -> int:
    subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}/{LABEL}"], capture_output=True)
    PLIST.unlink(missing_ok=True)
    print(f"removed {LABEL}")
    return 0


def status() -> int:
    proc = subprocess.run(["launchctl", "print", f"gui/{os.getuid()}/{LABEL}"],
                          capture_output=True, text=True)
    print("agent: loaded" if proc.returncode == 0 else "agent: not loaded")
    state = load_state(STATE)
    print(f"last staged: {state.get('at', 'never')}")
    if LOG.exists():
        print("recent log:")
        for line in LOG.read_text(encoding="utf-8").splitlines()[-5:]:
            print(f"  {line}")
    return 0


def main() -> int:
    args = sys.argv[1:]
    if "--install" in args:
        return install()
    if "--uninstall" in args:
        return uninstall()
    if "--status" in args:
        return status()

    try:
        result = check()
    except PermissionError as exc:
        # macOS protects ~/Downloads; a background agent needs the Python
        # binary to have been granted access to it.
        result = f"no permission to read {WATCH_DIR}: {exc}"
        log(result)
        notify("Instagram watcher", "Cannot read Downloads. See the log for the fix.")
        return 1

    log(result)
    if result.startswith("staged") and WATCH_ACTION == "sync":
        notify("Instagram export published", "Its stories are on brianpfeil.com/media.")
    elif result.startswith("staged"):
        notify("Instagram export staged",
               "Open tools/instagram-media/build/review.html and tick what to publish.")
    elif result.startswith("stage failed"):
        notify("Instagram export found, staging failed", "See ~/Library/Logs for details.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
