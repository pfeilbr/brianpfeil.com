#!/usr/bin/env python3
"""Post the next item from the social kit to Bluesky and Mastodon.

    python3 tools/social/post.py              # dry run: show what would post
    python3 tools/social/post.py --post       # post it (the weekday Action does this)
    python3 tools/social/post.py --post --channel mastodon

The queue is the kit's order (kit.py: the people-I-follow path first, then
the rest of /learn/, the guides, the courses). Each channel posts the first
item it hasn't posted yet, so a missed day just shifts the queue, a channel
added later catches up at its own pace, and a new course or guide joins the
end of the queue by itself. tools/social/posted.json records what went out
where; the Action commits it after each run.

A channel without its credentials is skipped, so the Action is harmless
until they're set:

    Bluesky   BLUESKY_HANDLE, BLUESKY_APP_PASSWORD (an app password, not the
              account password), optional BLUESKY_PDS (default bsky.social)
    Mastodon  MASTODON_INSTANCE (e.g. https://hachyderm.io), MASTODON_TOKEN
              (an application token with write:statuses only)

Before posting, the page itself is fetched: an item whose page doesn't load
is skipped for that run (it isn't deployed yet), and its og: title,
description and share card become the Bluesky link card. Mastodon builds
its own card from the same tags. Mastodon also gets an Idempotency-Key, so a
retried request can never post twice.

Standard library only.
"""

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit  # noqa: E402

LEDGER = Path(__file__).resolve().parent / "posted.json"
CHANNELS = ("bluesky", "mastodon")
UA = "brianpfeil.com social poster (+https://brianpfeil.com/)"
THUMB_MAX = 1_000_000  # Bluesky's blob limit for an external embed thumb


class PostError(Exception):
    pass


# ---------------------------------------------------------------- http

def http(method, url, *, headers=None, data=None, timeout=30):
    """(status, headers, body bytes). Never raises on an HTTP status."""
    req = urllib.request.Request(url, data=data, method=method, headers={"User-Agent": UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read()


def json_call(send, method, url, body=None, headers=None):
    data = None if body is None else json.dumps(body).encode()
    h = {"Content-Type": "application/json", **(headers or {})} if body is not None else dict(headers or {})
    status, _, raw = send(method, url, headers=h, data=data)
    if status >= 300:
        raise PostError(f"{method} {url.split('?')[0]} -> HTTP {status}: {raw[:300].decode('utf-8', 'replace')}")
    return json.loads(raw or b"{}")


# ---------------------------------------------------------------- page

def page_meta(send, url):
    """og: title/description/image of a live page, or None if it doesn't load."""
    status, _, raw = send("GET", url)
    if status != 200:
        return None
    text = raw.decode("utf-8", "replace")

    def og(prop):
        # Production HTML is minified, so attributes may be unquoted.
        m = re.search(r'<meta\s+property="?og:%s"?\s+content=("([^"]*)"|[^\s>]+)' % prop, text)
        if not m:
            return ""
        return html.unescape(m.group(2) if m.group(2) is not None else m.group(1))

    return {"title": og("title"), "description": og("description"), "image": og("image")}


# ---------------------------------------------------------------- ledger

def load_ledger(path=LEDGER):
    if path.exists():
        return json.loads(path.read_text())
    return {c: {} for c in CHANNELS}


def save_ledger(ledger, path=LEDGER):
    path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")


def next_item(items, ledger, channel):
    done = ledger.get(channel, {})
    return next((i for i in items if i["id"] not in done), None)


# ---------------------------------------------------------------- bluesky

def bluesky_record(item, meta, thumb_blob, now):
    external = {"uri": kit.link(item, "bluesky"),
                "title": meta.get("title") or item["title"],
                "description": meta.get("description") or item["blurb"]}
    if thumb_blob:
        external["thumb"] = thumb_blob
    return {
        "$type": "app.bsky.feed.post",
        "text": item["posts"]["bluesky_card"],
        "createdAt": now.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "langs": ["en"],
        "embed": {"$type": "app.bsky.embed.external", "external": external},
    }


def post_bluesky(send, item, meta, env, now):
    pds = env.get("BLUESKY_PDS", "https://bsky.social").rstrip("/")
    s = json_call(send, "POST", f"{pds}/xrpc/com.atproto.server.createSession",
                  {"identifier": env["BLUESKY_HANDLE"], "password": env["BLUESKY_APP_PASSWORD"]})
    auth = {"Authorization": f"Bearer {s['accessJwt']}"}
    blob = None
    if meta.get("image"):
        status, headers, img = send("GET", meta["image"])
        ctype = headers.get("Content-Type", "image/jpeg").split(";")[0]
        if status == 200 and ctype.startswith("image/") and len(img) <= THUMB_MAX:
            st, _, raw = send("POST", f"{pds}/xrpc/com.atproto.repo.uploadBlob",
                              headers={**auth, "Content-Type": ctype}, data=img)
            if st < 300:
                blob = json.loads(raw)["blob"]
    rec = json_call(send, "POST", f"{pds}/xrpc/com.atproto.repo.createRecord",
                    {"repo": s["did"], "collection": "app.bsky.feed.post",
                     "record": bluesky_record(item, meta, blob, now)}, auth)
    # at://did/app.bsky.feed.post/<rkey> -> the post's web address
    rkey = rec["uri"].rsplit("/", 1)[-1]
    return f"https://bsky.app/profile/{s.get('handle', env['BLUESKY_HANDLE'])}/post/{rkey}"


# ---------------------------------------------------------------- mastodon

def post_mastodon(send, item, meta, env, now):
    base = env["MASTODON_INSTANCE"].rstrip("/")
    if not base.startswith("http"):
        base = "https://" + base
    body = urllib.parse.urlencode({"status": item["posts"]["mastodon"], "visibility": "public",
                                   "language": "en"}).encode()
    status, _, raw = send("POST", f"{base}/api/v1/statuses", data=body, headers={
        "Authorization": f"Bearer {env['MASTODON_TOKEN']}",
        "Content-Type": "application/x-www-form-urlencoded",
        # Same item -> same key: a retried request returns the first post.
        "Idempotency-Key": f"brianpfeil.com:{item['id']}",
    })
    if status >= 300:
        raise PostError(f"Mastodon -> HTTP {status}: {raw[:300].decode('utf-8', 'replace')}")
    return json.loads(raw)["url"]


POSTERS = {"bluesky": post_bluesky, "mastodon": post_mastodon}
NEEDS = {"bluesky": ("BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD"),
         "mastodon": ("MASTODON_INSTANCE", "MASTODON_TOKEN")}


# ---------------------------------------------------------------- run

def run(channels, *, post, env, send=http, ledger_path=LEDGER, now=None, log=print):
    """Post (or preview) the next item on each channel. Returns the number
    of channels that failed."""
    now = now or dt.datetime.now(dt.timezone.utc)
    items = kit.build(now.date())
    ledger = load_ledger(ledger_path)
    failed = 0
    for ch in channels:
        missing = [k for k in NEEDS[ch] if not env.get(k)]
        if post and missing:
            log(f"{ch}: skipped, {' and '.join(missing)} not set")
            continue
        item = next_item(items, ledger, ch)
        if not item:
            log(f"{ch}: nothing left to post ({len(items)} items all posted)")
            continue
        page = item["url"].split("#")[0]
        if not post:
            text = item["posts"]["bluesky_card" if ch == "bluesky" else ch]
            log(f"--- {ch} would post {item['id']} ({page})\n{text}\n")
            continue
        meta = page_meta(send, page)
        if meta is None:
            log(f"{ch}: skipped {item['id']}, {page} doesn't load yet")
            continue
        try:
            url = POSTERS[ch](send, item, meta, env, now)
        except (PostError, KeyError, ValueError, urllib.error.URLError) as e:
            log(f"{ch}: FAILED {item['id']}: {e}")
            failed += 1
            continue
        ledger.setdefault(ch, {})[item["id"]] = {"at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "url": url}
        save_ledger(ledger, ledger_path)  # after every post, so a later failure can't lose it
        log(f"{ch}: posted {item['id']} -> {url}")
    return failed


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--post", action="store_true", help="really post (default: dry run)")
    ap.add_argument("--channel", choices=CHANNELS, action="append", help="limit to a channel (repeatable)")
    a = ap.parse_args(argv)
    return 1 if run(a.channel or CHANNELS, post=a.post, env=os.environ) else 0


if __name__ == "__main__":
    sys.exit(main())
