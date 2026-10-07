#!/usr/bin/env python3
"""Switch the site's TikTok links to @pfeilbr once that username is B's.

B's TikTok account (user id ACCOUNT_ID) shows "pfeilbr" as its display
name, but its username -- the part of the URL -- is still the one TikTok
generated, so the site links that. When B changes the username in the app,
https://www.tiktok.com/@pfeilbr starts answering with the same user id.
This checks for that and, with --apply, rewrites every link to the new
handle. It never switches to an @pfeilbr that belongs to someone else.

    python3 tools/profiles/tiktok_handle.py           # report only
    python3 tools/profiles/tiktok_handle.py --apply   # rewrite the files

Once the site links @pfeilbr, it instead confirms @pfeilbr is still B's
account and exits 1 if not, so the weekly Action shows red. Otherwise exit
status 0 whether or not anything changed (the Action commits only when
files did). Standard library only.
"""

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ACCOUNT_ID = "7321531911816938539"
CURRENT = "user8768514322831"
WANTED = "pfeilbr"
FILES = (
    "config.yaml",
    "data/home.yaml",
    "tools/profiles/check_profiles.py",
    *(f"content/about{s}.md" for s in ("", ".zh", ".es", ".pt", ".fr", ".de", ".it", ".ja", ".ko")),
)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
DATA = re.compile(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', re.S)


def owner(html: str) -> str | None:
    """The user id behind a TikTok profile page, or None if it has none."""
    m = DATA.search(html)
    if not m:
        return None
    try:
        detail = json.loads(m.group(1))["__DEFAULT_SCOPE__"]["webapp.user-detail"]
        return detail["userInfo"]["user"]["id"] or None
    except (ValueError, KeyError, TypeError):
        return None


def fetch(handle: str) -> str:
    req = urllib.request.Request(f"https://www.tiktok.com/@{handle}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def rewrite(root: Path) -> list[str]:
    """Replace the generated handle with WANTED; return the files changed."""
    changed = []
    for name in FILES:
        p = root / name
        s = p.read_text()
        new = s.replace(f"@{CURRENT}", f"@{WANTED}").replace(f'tiktok: "{CURRENT}"', f'tiktok: "{WANTED}"')
        if new != s:
            p.write_text(new)
            changed.append(name)
    return changed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true", help="rewrite the files when @pfeilbr is B's")
    args = ap.parse_args()
    switched = f'tiktok: "{CURRENT}"' not in (REPO / "config.yaml").read_text()
    try:
        who = owner(fetch(WANTED))
    except OSError as e:
        print(f"could not check @{WANTED}: {e}")
        return 0
    if switched:
        # B renamed the account on 2026-10-07 and the site links @pfeilbr.
        # Fail (so the weekly run shows red) if that stops being B's.
        if who == ACCOUNT_ID:
            print(f"ok: the site links @{WANTED}, and it is B's account")
            return 0
        print(f"error: the site links @{WANTED}, but it is {'someone else' if who else 'not found'}")
        return 1
    if who != ACCOUNT_ID:
        print(f"@{WANTED} is {'someone else' if who else 'not taken'}; keeping @{CURRENT}")
        return 0
    if not args.apply:
        print(f"@{WANTED} is now B's account; run with --apply to switch")
        return 0
    for name in rewrite(REPO):
        print(f"switched: {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
