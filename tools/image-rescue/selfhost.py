#!/usr/bin/env python3
"""Self-host the Evernote screenshots that posts still hotlink.

rescue.py deals with images that no longer load. This deals with the ones
that still do but live on a host the site doesn't control: about 320 post
screenshots are Evernote share links (www.evernote.com/l/<id>/image.png, or
the longer /shard/.../image.png form). Each one that still serves an image
is downloaded once, scaled to at most MAX_WIDTH px wide, saved as WebP under
static/images/remote/ (16 MB for all of them, against 90 KB-1.7 MB PNGs
each on Evernote), and mapped to that local path in data/image_rewrites.json
-- the same map rescue.py writes, applied when pages render, so
`make generate-posts` can't bring the Evernote URLs back.

An Evernote URL that doesn't serve an image is left unmapped for rescue.py,
which looks for an archived copy before retiring it. Existing entries are
never changed.

    python3 tools/image-rescue/selfhost.py            # report
    python3 tools/image-rescue/selfhost.py --apply    # download, convert, map
    python3 tools/image-rescue/selfhost.py --check    # exit 1 if any is unmapped

Needs ImageMagick 7 (`magick`) for the WebP conversion.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rescue  # noqa: E402

OUT = rescue.REPO / "static" / "images" / "remote"
MAX_WIDTH = 1600
QUALITY = 80

EVERNOTE = re.compile(r"^https?://www\.evernote\.com/(?:l/([A-Za-z0-9_-]+)(?:/image\.png)?"
                      r"|shard/[^\s)\"']+/image\.png)$")


def evernote_images(images: dict) -> list[str]:
    return sorted(u for u in images if EVERNOTE.match(u))


def local_name(url: str) -> str:
    m = EVERNOTE.match(url)
    return f"evernote-{m.group(1) or hashlib.sha1(url.encode()).hexdigest()[:16]}.webp"


def to_webp(data: bytes, dest: Path) -> None:
    with tempfile.NamedTemporaryFile(suffix=".img") as src:
        src.write(data)
        src.flush()
        subprocess.run(["magick", src.name + "[0]", "-strip", "-resize", f"{MAX_WIDTH}x>",
                        "-quality", str(QUALITY), str(dest)], check=True)


def selfhost(url: str) -> str | None:
    """The local path for a live Evernote image, or None if it isn't live."""
    dest = OUT / local_name(url)
    if not dest.exists():
        status, ctype, data = rescue.get(url, timeout=40)
        if not (status == 200 and ctype.startswith("image/") and data):
            return None
        to_webp(data, dest)
    return "/images/remote/" + dest.name


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)

    mapping = json.loads(rescue.MAP.read_text(encoding="utf-8")) if rescue.MAP.exists() else {}
    todo = [u for u in evernote_images(rescue.remote_images()) if u not in mapping]
    if args.check:
        if todo:
            print(f"{len(todo)} Evernote image(s) not self-hosted; run make images-selfhost:")
            for u in todo[:20]:
                print("  ", u)
            return 1
        print("ok: every Evernote image in a post is self-hosted or retired")
        return 0
    print(f"{len(todo)} Evernote image(s) to self-host")
    if not args.apply:
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(selfhost, todo))
    left = []
    for url, local in zip(todo, results):
        if local:
            mapping[url] = local
        else:
            left.append(url)
    rescue.MAP.write_text(json.dumps(dict(sorted(mapping.items())), indent=1, ensure_ascii=False) + "\n",
                          encoding="utf-8")
    print(f"self-hosted {len(todo) - len(left)}; {len(left)} not live, left for rescue.py")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
