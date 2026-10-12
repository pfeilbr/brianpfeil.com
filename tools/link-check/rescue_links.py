#!/usr/bin/env python3
"""Point dead outbound links in posts at the Wayback Machine, or unlink them.

check_post_links.py finds the links written into posts, projects and guides
whose page is gone (404/410, or a host that no longer resolves). For each,
this asks the Wayback Machine for the copy closest to the date of the post
that links it, and records the result in data/link_rewrites.json:

- an archive URL: the link opens that copy instead (titled as an archived
  copy);
- null: there is no copy, so the link text stays and the link goes.

The map is applied when pages render (partials/content-a11y.html), not by
editing posts, so it survives `make generate-posts` rewriting the generated
ones. A URL already in the map is not looked up again (delete its line to
have it re-checked), but every run first re-opens each mapped URL and drops
the ones that answer again: a network error under load, or a page that
came back, shouldn't keep a working link pointed at the archive.

    make check-post-links                              # writes post-links.json
    python3 tools/link-check/rescue_links.py --results <post-links.json> --public <site>
    python3 tools/link-check/rescue_links.py ... --apply   # write the map

Standard library only.
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "learn-links"))
from check_learn_links import BLOCKED, fetch  # noqa: E402

DATA = REPO / "data" / "link_rewrites.json"
API = "https://archive.org/wayback/available?url={url}&timestamp={ts}"
# The availability API sometimes answers "no snapshots" for pages that have
# them; the CDX index (slow, 30-50 s a query) is asked before believing it.
CDX = ("https://web.archive.org/cdx/search/cdx?url={url}&output=json"
       "&filter=statuscode:200&closest={ts}&sort=closest&limit=1&fl=timestamp,original")
UA = "brianpfeil.com link rescue (+https://brianpfeil.com/)"
# Cloudflare's "origin unreachable" family: the site behind it is gone,
# however long the check waits.
DEAD_ORIGIN = {521, 522, 523, 530}
PUBLISHED = re.compile(r'property="?article:published_time"? content="?(\d{4})-(\d{2})-(\d{2})')


def dead(results: list[dict]) -> list[dict]:
    """The results worth rescuing: gone, or an origin that no longer answers."""
    return [r for r in results
            if r["kind"] == "gone" or (r["kind"] == "error" and r["status"] in DEAD_ORIGIN)]


def post_date(public: Path, page: str) -> str:
    """YYYYMMDD a page was published, from its meta tag; "" if unknown."""
    f = public / page.strip("/") / "index.html"
    if not f.exists():
        return ""
    m = PUBLISHED.search(f.read_text(encoding="utf-8", errors="replace"))
    return "".join(m.groups()) if m else ""


def snapshot(payload: dict) -> str | None:
    """The archive URL from an availability API answer, if it is a 200 copy."""
    closest = (payload.get("archived_snapshots") or {}).get("closest") or {}
    if closest.get("available") and str(closest.get("status")) == "200" and closest.get("url"):
        return closest["url"].replace("http://web.archive.org/", "https://web.archive.org/")
    return None


def cdx_snapshot(rows: list) -> str | None:
    """The archive URL from a CDX answer (a header row, then matches)."""
    if len(rows) > 1 and len(rows[1]) >= 2:
        ts, original = rows[1][0], rows[1][1]
        return f"https://web.archive.org/web/{ts}/{original}"
    return None


def get_json(url: str, tries: int = 3, timeout: int = 90):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                return json.loads(body) if body.strip() else []
        except Exception:
            time.sleep(3 * (attempt + 1))
    return None


def lookup(url: str, ts: str) -> str | None | bool:
    """Archive URL, None (no copy), or False (Wayback didn't answer: try later)."""
    q = urllib.parse.quote(url, safe="")
    ts = ts or "2015"
    fast = get_json(API.format(url=q, ts=ts))
    if isinstance(fast, dict) and (hit := snapshot(fast)):
        return hit
    rows = get_json(CDX.format(url=q, ts=ts))
    if rows is None:
        return False
    return cdx_snapshot(rows)


def alive(status) -> bool:
    """A page that answers: 200, or a site refusing scripts (it exists)."""
    return status == 200 or status in BLOCKED


def prune(current: dict, statuses: dict) -> dict:
    """The map without the URLs that answer again."""
    return {u: v for u, v in current.items() if not alive(statuses.get(u))}


def merge(current: dict, found: dict) -> dict:
    """Existing entries win (sticky); new ones are added; sorted by URL."""
    out = dict(found)
    out.update(current)
    return dict(sorted(out.items()))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True, help="check_post_links.py --json output")
    ap.add_argument("--public", default="public", help="built site, for each post's date")
    ap.add_argument("--apply", action="store_true", help="write data/link_rewrites.json")
    args = ap.parse_args(argv)

    current = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    candidates = [r for r in dead(json.loads(Path(args.results).read_text(encoding="utf-8")))
                  if r["url"] not in current]
    # Re-open everything first, four at a time (the checker's 16 parallel
    # fetches produce network errors that look like dead hosts).
    urls = list(current) + [r["url"] for r in candidates]
    with ThreadPoolExecutor(max_workers=4) as pool:
        statuses = dict(zip(urls, pool.map(lambda u: fetch(u)[0], urls)))
    revived = [u for u in current if alive(statuses[u])]
    for u in revived:
        print(f"BACK  {u}  ({statuses[u]}): dropped from the map", flush=True)
    current = prune(current, statuses)
    todo = [r for r in candidates if not alive(statuses[r["url"]])]
    for r in candidates:
        if alive(statuses[r["url"]]):
            print(f"OK    {r['url']}  ({statuses[r['url']]}): not dead after all", flush=True)
    found: dict[str, str | None] = {}
    skipped = 0
    public = Path(args.public)
    with ThreadPoolExecutor(max_workers=4) as pool:
        answers = pool.map(lambda r: lookup(r["url"], post_date(public, r["pages"][0])), todo)
        for r, got in zip(todo, answers):
            if got is False:
                skipped += 1
                print(f"SKIP  {r['url']}  (Wayback didn't answer; run again)", flush=True)
                continue
            found[r["url"]] = got
            print(f"{'ARCH' if got else 'NONE'}  {r['url']}" + (f"  -> {got}" if got else ""), flush=True)
    archived = sum(1 for v in found.values() if v)
    print(f"{len(todo)} new dead links: {archived} archived, "
          f"{len(found) - archived} unlinked, {skipped} skipped")
    if args.apply and (found or revived):
        DATA.write_text(json.dumps(merge(current, found), indent=1) + "\n", encoding="utf-8")
        print(f"wrote {DATA.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
