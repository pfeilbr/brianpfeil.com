#!/usr/bin/env python3
"""Refresh data/subscriptions.yaml (the YouTube tab of /subscriptions/).

Which channels I subscribe to needs my sign-in, so that one list comes from
the browser: on https://www.youtube.com/feed/channels, scroll to the bottom
and run this in the console, then save the output to a file:

    [...document.querySelectorAll('ytd-channel-renderer')]
      .map(r => r.data.channelId).join('\\n')

Everything else is public and fetched here, per channel, from its own page:
name, @handle, subscriber count and, for a newly listed channel, its avatar
(downscaled to 96px and copied into static/subscriptions/avatars/, never
hotlinked).

config.json:
  exclude  id -> why it is not listed (topic channels, people who didn't
           ask to be on my website)
  cat      id -> category key, for channels added after the first listing.
           A subscribed channel that is neither listed, excluded nor given
           a category stops the run, so nothing is published unreviewed.

Channels stay grouped by category (in the file's category order) and sorted
by subscribers within each. A channel I unsubscribed from drops off.

  python3 tools/subscriptions/youtube.py --ids ids.txt            # write
  python3 tools/subscriptions/youtube.py --ids ids.txt --dry-run  # print only

Standard library only.
"""
import argparse
import html
import json
import pathlib
import re
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "subscriptions.yaml"
AVATARS = ROOT / "static" / "subscriptions" / "avatars"
CONFIG = pathlib.Path(__file__).with_name("config.json")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140 Safari/537.36"

ENTRY = re.compile(
    r'  - name: "(?P<name>.*)"\n'
    r'    handle: "(?P<handle>.*)"\n'
    r'    cat: (?P<cat>\w+)\n'
    r'    subs: "(?P<subs>.*)"\n'
    r'    uploads: "(?P<uploads>.*)"\n'
    r'    avatar: "(?P<avatar>.*)"\n'
)


def parse_count(s):
    mult = {"K": 1e3, "M": 1e6, "B": 1e9}
    s = s.strip()
    return float(s[:-1]) * mult[s[-1]] if s[-1] in mult else float(s)


def fmt_combined(n):
    return f"{round(n / 1e6)}M"


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def yaml_str(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def parse(text):
    head, _, body = text.partition("\nchannels:\n")
    channels = [m.groupdict() for m in ENTRY.finditer(body)]
    for c in channels:
        c["name"] = c["name"].replace('\\"', '"').replace("\\\\", "\\")
    if len(ENTRY.sub("", body).strip()) != 0:
        raise SystemExit("subscriptions.yaml: unexpected text in channels block")
    cats = re.findall(r"  - key: (\w+)\n    count: \d+\n", head)
    return head, cats, channels


def render(head, cats, channels):
    counts = {k: sum(1 for c in channels if c["cat"] == k) for k in cats}
    head = re.sub(r"^total: \d+$", f"total: {len(channels)}", head, flags=re.M)
    combined = fmt_combined(sum(parse_count(c["subs"]) for c in channels))
    head = re.sub(r'^combined_subscribers: ".*"$', f'combined_subscribers: "{combined}"', head, flags=re.M)
    for k in cats:
        head = re.sub(rf"(  - key: {k}\n    count: )\d+", rf"\g<1>{counts[k]}", head)
    out = [head, "\nchannels:\n"]
    for c in channels:
        out.append(
            f'  - name: "{yaml_str(c["name"])}"\n'
            f'    handle: "{c["handle"]}"\n'
            f'    cat: {c["cat"]}\n'
            f'    subs: "{c["subs"]}"\n'
            f'    uploads: "{c["uploads"]}"\n'
            f'    avatar: "{c["avatar"]}"\n'
        )
    return "".join(out)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))


def channel_info(cid):
    """Name, handle, subscriber count and avatar URL from the public channel page."""
    page = get(f"https://www.youtube.com/channel/{cid}").decode("utf-8", "replace")
    return parse_channel_page(page, cid)


def parse_channel_page(page, cid):
    name = re.search(r'<meta property="og:title" content="([^"]*)"', page)
    handle = re.search(r'"canonicalBaseUrl":"/(@[^"]+)"', page)
    # The header's metadata row ("4.29M subscribers"); other subscriberCountText
    # values on the page belong to featured channels.
    subs = re.search(r'"content":"([\d.]+[KMB]?) subscribers?"', page)
    avatar = re.search(r'<meta property="og:image" content="([^"]*)"', page)
    if not (name and subs and avatar):
        raise ValueError(f"{cid}: could not read the channel page")
    return {
        "name": html.unescape(name.group(1)).strip(),
        "handle": handle.group(1) if handle else "",
        "subs": subs.group(1),
        "avatar_url": re.sub(r"=s\d+.*$", "=s96-c-k-c0x00ffffff-no-rj", avatar.group(1)),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ids", required=True, help="file of subscribed channel ids (UC...), one per line")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    config = json.loads(CONFIG.read_text())
    ids = [i for i in re.split(r"\s+", pathlib.Path(args.ids).read_text()) if i]
    ids = [i if i.startswith("UC") else "UC" + i for i in ids]
    if len(ids) < 20:
        raise SystemExit(f"only {len(ids)} ids -- is the list complete?")

    head, cats, channels = parse(DATA.read_text())
    listed = {"UC" + c["uploads"][2:]: c for c in channels}
    unknown = [i for i in ids if i not in listed and i not in config["exclude"] and i not in config["cat"]]
    if unknown:
        for i in unknown:
            info = channel_info(i)
            print(f"unreviewed: {i} {info['name']} {info['handle']} {info['subs']}", file=sys.stderr)
        raise SystemExit("add each to config.json 'cat' or 'exclude', then re-run")

    keep = []
    for cid in ids:
        if cid in config["exclude"]:
            continue
        info = channel_info(cid)
        old = listed.get(cid)
        c = {
            "name": info["name"],
            "handle": info["handle"] or (old or {}).get("handle", ""),
            "cat": old["cat"] if old else config["cat"][cid],
            "subs": info["subs"],
            "uploads": "UU" + cid[2:],
            "avatar": old["avatar"] if old else f"/subscriptions/avatars/{slug(info['name'])}.jpg",
            "_avatar_url": info["avatar_url"],
        }
        tag = "new " if not old else ("    " if old["subs"] == c["subs"] else "subs")
        print(f"{tag} {c['name']:<40} {(old or {}).get('subs', ''):>6} -> {c['subs']}")
        keep.append(c)
    for cid, c in listed.items():
        if cid not in ids:
            print(f"gone {c['name']} (unsubscribed)")

    keep.sort(key=lambda c: (cats.index(c["cat"]), -parse_count(c["subs"])))
    text = render(head, cats, keep)
    if args.dry_run:
        return 0
    for c in keep:
        dest = ROOT / "static" / c["avatar"].lstrip("/")
        url = c.pop("_avatar_url")
        if not dest.exists():  # Google re-encodes on every fetch; keep the copy we have
            dest.write_bytes(get(url))
    DATA.write_text(text)
    print(f"wrote {DATA.relative_to(ROOT)}: {len(keep)} channels")
    return 0


if __name__ == "__main__":
    sys.exit(main())
