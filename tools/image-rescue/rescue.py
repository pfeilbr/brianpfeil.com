#!/usr/bin/env python3
"""Find remote images in posts that no longer load, and rescue or retire them.

Posts embed screenshots from hosts that have since gone away: note.io,
Evernote and Skitch shares, and two of B's own S3 website buckets
(static-content-01, static-screenshots-01) that were deleted. A deleted
bucket's name is up for grabs, so anyone could recreate it and have their
images appear inside these posts -- the references must go, not just the
broken pictures.

For every remote image in content/ that doesn't answer 200 with an image
(or whose host is in DEAD_HOSTS, whatever it answers), this:

1. asks the Wayback Machine for a copy and, if there is one, saves it under
   static/images/rescued/ and maps the URL to that local path;
2. otherwise maps it to null, which the templates render as a short
   "image no longer available" note instead of the <img>.

The map is data/image_rewrites.json. It's applied when pages render
(layouts/_default/_markup/render-image.html and
partials/content-a11y.html), not by editing posts, so it survives
`make generate-posts` rewriting the generated ones. Entries are sticky:
once a URL is mapped it stays mapped, so a bucket someone re-registers can't
put its images back on the page.

    python3 tools/image-rescue/rescue.py            # report
    python3 tools/image-rescue/rescue.py --apply    # download and write the map

Standard library only.
"""

import argparse
import hashlib
import http.cookiejar
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTENT = REPO / "content"
MAP = REPO / "data" / "image_rewrites.json"
RESCUED = REPO / "static" / "images" / "rescued"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

# Hosts whose content can't be trusted any more, even if they answer: deleted
# S3 buckets (the name can be re-registered by anyone) and dead share links.
DEAD_HOSTS = {
    "static-content-01.s3-website-us-east-1.amazonaws.com",
    "static-screenshots-01.s3-website-us-east-1.amazonaws.com",
    "note.io",
}

IMG = re.compile(r'!\[[^\]]*\]\((https?://[^)\s]+)|<img\b[^>]*?\bsrc=["\']?(https?://[^"\'\s>]+)', re.I)
EXT = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif",
       "image/svg+xml": ".svg", "image/webp": ".webp"}


def remote_images(content: Path = CONTENT) -> dict[str, list[str]]:
    """{url: [files that use it]} for every remote image in Markdown content."""
    found: dict[str, list[str]] = {}
    for md in sorted(content.rglob("*.md")):
        for m in IMG.finditer(md.read_text(encoding="utf-8", errors="replace")):
            url = m.group(1) or m.group(2)
            found.setdefault(url, []).append(md.relative_to(REPO).as_posix())
    return found


def safe(url: str) -> str:
    """Percent-encode the non-ASCII in a URL (some screenshots are named
    with em dashes and multiplication signs) without double-encoding."""
    return urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%~")


def get(url: str, timeout: int = 25) -> tuple[int | str, str, bytes]:
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    try:
        with opener.open(urllib.request.Request(safe(url), headers={"User-Agent": UA}), timeout=timeout) as r:
            return r.status, r.headers.get("Content-Type", "").split(";")[0].strip(), r.read()
    except urllib.error.HTTPError as err:
        return err.code, "", b""
    except Exception as err:  # DNS, TLS, timeout
        return type(err).__name__, "", b""


def host(url: str) -> str:
    return urllib.parse.urlsplit(url).hostname or ""


def is_dead(url: str) -> bool:
    if host(url) in DEAD_HOSTS:
        return True
    status, ctype, _ = get(url)
    return not (status == 200 and ctype.startswith("image/"))


def wayback(url: str) -> tuple[bytes, str] | None:
    """The Wayback Machine's closest copy of an image, raw (id_), or None."""
    api = "https://archive.org/wayback/available?url=" + urllib.parse.quote(safe(url), safe="")
    status, _, body = get(api, timeout=40)
    if status != 200:
        return None
    snap = (json.loads(body or b"{}").get("archived_snapshots") or {}).get("closest") or {}
    if not snap.get("available"):
        return None
    raw = re.sub(r"/web/(\d+)/", r"/web/\1id_/", snap["url"], count=1)
    status, ctype, data = get(raw, timeout=60)
    if status == 200 and ctype in EXT and data:
        return data, ctype
    return None


def local_name(url: str, ctype: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16] + EXT[ctype]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)

    mapping = json.loads(MAP.read_text(encoding="utf-8")) if MAP.exists() else {}
    images = remote_images()
    todo = [u for u in images if u not in mapping]
    with ThreadPoolExecutor(max_workers=16) as pool:
        dead = [u for u, d in zip(todo, pool.map(is_dead, todo)) if d]
    print(f"{len(images)} remote images, {len(mapping)} already mapped, {len(dead)} newly dead")

    for url in dead:
        copy = wayback(url)
        if copy:
            data, ctype = copy
            name = local_name(url, ctype)
            print(f"rescued  {url}  ->  /images/rescued/{name}")
            if args.apply:
                RESCUED.mkdir(parents=True, exist_ok=True)
                (RESCUED / name).write_bytes(data)
            mapping[url] = f"/images/rescued/{name}"
        else:
            print(f"retired  {url}  (no archived copy; used in {images[url][0]})")
            mapping[url] = None

    if args.apply:
        MAP.write_text(json.dumps(dict(sorted(mapping.items())), indent=1, ensure_ascii=False) + "\n",
                       encoding="utf-8")
        print(f"wrote {MAP.relative_to(REPO)} ({len(mapping)} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
