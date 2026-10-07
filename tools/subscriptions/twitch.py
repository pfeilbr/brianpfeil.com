#!/usr/bin/env python3
"""Refresh follower counts and display names in data/twitch.yaml.

Which channels I follow (and which I once subscribed to) needs my Twitch
sign-in, so the lists themselves are edited by hand; this re-reads every
listed channel's public numbers from Twitch's own GraphQL endpoint (the
anonymous client id twitch.tv uses before you sign in) and keeps each list
sorted by followers. A channel that no longer exists is reported and left
alone.

  python3 tools/subscriptions/twitch.py            # fetch and write
  python3 tools/subscriptions/twitch.py --dry-run  # fetch and print

Standard library only.
"""
import argparse
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "twitch.yaml"
GQL = "https://gql.twitch.tv/gql"
CLIENT_ID = "kimne78kx3ncx6brgo4mv6wki5h1ko"  # public, anonymous web client

ENTRY = re.compile(
    r'  - login: "(?P<login>[^"]*)"\n'
    r'    name: "(?P<name>[^"]*)"\n'
    r'    followers: "(?P<followers>[^"]*)"\n'
    r'    avatar: "(?P<avatar>[^"]*)"\n'
)


def fmt(n):
    """Twitch-style short count: 11.2M, 6M, 709K, 7K, 950."""
    if n >= 1e6:
        return f"{n / 1e6:.1f}".rstrip("0").rstrip(".") + "M"
    if n >= 1e3:
        return f"{round(n / 1e3)}K"
    return str(n)


def parse_count(s):
    mult = {"K": 1e3, "M": 1e6}
    return float(s[:-1]) * mult[s[-1]] if s[-1] in mult else float(s)


def fetch(logins):
    out = {}
    for i in range(0, len(logins), 50):
        query = "query($l:[String!]){users(logins:$l){login displayName followers{totalCount}}}"
        body = json.dumps({"query": query, "variables": {"l": logins[i:i + 50]}}).encode()
        req = urllib.request.Request(GQL, data=body, headers={"Client-Id": CLIENT_ID, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        for u in data["data"]["users"]:
            if u:
                out[u["login"]] = {"name": u["displayName"], "followers": u["followers"]["totalCount"]}
    return out


def update_block(block, live):
    entries = [m.groupdict() for m in ENTRY.finditer(block)]
    for e in entries:
        u = live.get(e["login"])
        if not u:
            print(f"missing on Twitch: {e['login']} (left as is)", file=sys.stderr)
            continue
        new = fmt(u["followers"])
        if new != e["followers"]:
            print(f"{e['login']:<20} {e['followers']:>6} -> {new}")
        e["followers"], e["name"] = new, u["name"]
    entries.sort(key=lambda e: -parse_count(e["followers"]))
    return "".join(
        f'  - login: "{e["login"]}"\n    name: "{e["name"]}"\n'
        f'    followers: "{e["followers"]}"\n    avatar: "{e["avatar"]}"\n'
        for e in entries
    )


def refresh(text, live):
    def repl(m):
        return m.group(1) + update_block(m.group(2), live)
    return re.sub(r"(^(?:following|past):\n)((?:  - login:.*\n(?:    .*\n)+)+)", repl, text, flags=re.M)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    text = DATA.read_text()
    logins = re.findall(r'login: "([^"]+)"', text)
    live = fetch(logins)
    if len(live) < len(logins) * 0.75:
        raise SystemExit(f"only {len(live)} of {len(logins)} channels answered; not writing")
    new = refresh(text, live)
    if not args.dry_run and new != text:
        DATA.write_text(new)
        print(f"wrote {DATA.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
