#!/usr/bin/env python3
"""Bring the instagram-archive project up to date, ahead of `make media-sync`.

The archive (~/projects/instagram-archive, the parent of `archive_dir` in
tools/instagram-media/config.yaml) learns about new posts only from a harvest
in the signed-in instagram.com tab, which no script here can run. So:

  1. if the clipboard holds a capture (the page's COPY CAPTURE button), file it
     into the archive's harvest/ (`make paste` there);
  2. say how old the last harvest is, and how to take a new one when it is
     older than a day;
  3. `make update` there: ingest, download new media in committed chunks,
     restore parked oversized reels, save.

The harvest itself:  make -C ~/projects/instagram-archive harvest-snippet
puts the collector and its run lines on the clipboard; paste it into the
console on https://www.instagram.com/pfeilbr/, click COPY CAPTURE, then run
`make refresh STEPS="instagram media"`.

Standard library only.
"""
import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
STALE_DAYS = 1


def archive_root():
    """The instagram-archive project, or None when it is not on this machine."""
    cfg = (ROOT / "tools/instagram-media/config.yaml").read_text()
    line = next((l for l in cfg.splitlines() if l.startswith("archive_dir:")), "")
    path = pathlib.Path(line.partition(":")[2].strip().strip('"\'')).expanduser()
    return path.parent if path.is_dir() and (path.parent / "Makefile").is_file() else None


def harvest_age_days(root):
    """Days since the newest posts capture landed in harvest/, or None."""
    caps = sorted((root / "harvest").glob("posts-*.json"), key=lambda p: p.stat().st_mtime)
    return (time.time() - caps[-1].stat().st_mtime) / 86400 if caps else None


def stale_note(root):
    age = harvest_age_days(root)
    if age is not None and age < STALE_DAYS:
        return ""
    when = "never" if age is None else f"{age:.0f} day(s) ago"
    return (f"Instagram was last harvested {when}; posts since then are not on /media/. "
            f"Run `make -C {root} harvest-snippet`, paste it into the console on "
            "instagram.com/pfeilbr, click COPY CAPTURE, then "
            "`make refresh STEPS=\"instagram media\"`.")


def clipboard_capture():
    try:
        text = subprocess.run(["pbpaste"], capture_output=True, text=True).stdout
        cap = json.loads(text)
    except (OSError, json.JSONDecodeError):
        return False
    return isinstance(cap, dict) and bool(cap.get("kind")) and "pages" in cap


def main():
    root = archive_root()
    if not root:
        print("the instagram-archive project is not on this machine", file=sys.stderr)
        return 1
    if clipboard_capture():
        print("a capture is on the clipboard; filing it into harvest/", flush=True)
        if subprocess.run(["make", "-C", str(root), "paste"]).returncode != 0:
            return 1
    note = stale_note(root)
    if note:
        print(f"\n!! {note}\n", flush=True)
    return subprocess.run(["make", "-C", str(root), "update"]).returncode


if __name__ == "__main__":
    sys.exit(main())
