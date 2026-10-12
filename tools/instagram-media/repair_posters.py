#!/usr/bin/env python3
"""Rebuild the poster, thumbnail and grid tiles of videos whose poster is black.

Clips that fade in from black got their first frame as poster, so the reel
showed an all-black tile on /media/ and the home page. derive.py now picks
the first frame that isn't near-black; this applies that to videos already
on the CDN, without re-encoding anything:

  for each video in data/media.yaml whose poster (from the CDN) is near-black:
    download the published mp4, pick a better frame, rebuild <stem>-p.jpg,
    <stem>-t.jpg and the grid WebPs under the same names, upload them,
    invalidate those paths, and set the new average colour in data/media.yaml
    and in the derive lock (so the next media-sync keeps it).

    .venv/bin/python repair_posters.py --dry-run     # list what is black
    .venv/bin/python repair_posters.py               # fix it (needs AWS)
    .venv/bin/python repair_posters.py --lock PATH   # lock outside this dir

Re-runnable: a fixed poster is no longer dark, so a second run does nothing.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

import yaml

TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
sys.path.insert(0, str(TOOL_DIR))
from igmedia import derive, publish  # noqa: E402

CONTENT_TYPES = {".jpg": "image/jpeg", ".webp": "image/webp"}


def dark_videos(items: list[dict], luma_of) -> list[tuple[str, dict]]:
    """(item id, media) for every video whose poster is near-black."""
    out = []
    for item in items:
        for m in item.get("media", []):
            if m.get("kind") == "video" and m.get("poster") and luma_of(m["poster"]) < derive.DARK_LUMA:
                out.append((item["id"], m))
    return out


def set_color(yaml_text: str, grid_file: str, color: str) -> str:
    """Change the `color:` that follows a media entry's grid list, in place,
    so the rest of the file (comments, order, quoting) is untouched."""
    pat = re.compile(r"(    - " + re.escape(grid_file) + r"\n(?:    - .*\n)*    color: )'#[0-9a-f]{6}'")
    out, n = pat.subn(lambda m: m.group(1) + f"'{color}'", yaml_text, count=1)
    if n != 1:
        raise ValueError(f"no color line after {grid_file}")
    return out


def fetch(url: str, dest: Path) -> Path:
    # The CDN answers 403 to urllib's default user agent.
    req = urllib.request.Request(url, headers={"User-Agent": "brianpfeil.com-media-repair"})
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--lock", type=Path, default=None)
    args = ap.parse_args()

    cfg = yaml.safe_load((TOOL_DIR / "config.yaml").read_text(encoding="utf-8"))
    data_path = REPO_ROOT / cfg["data_file"]
    text = data_path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    base = (data.get("base_url") or cfg["base_url"]).rstrip("/")
    lock_path = args.lock or TOOL_DIR / cfg["lock_file"]

    work = Path(tempfile.mkdtemp(prefix="posters-"))

    def luma_of(key: str) -> float:
        return derive.frame_luma(fetch(f"{base}/{key}", work / Path(key).name))

    todo = dark_videos(data["items"], luma_of)
    print(f"{len(todo)} video(s) with a near-black poster")
    for item_id, m in todo:
        print(f"  {item_id}  {m['poster']}")
    if args.dry_run or not todo:
        return 0

    publish.check_credentials(cfg["bucket"])
    lock = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.exists() else {}
    # Build every file first and upload only when all of them built, so a
    # failure part way leaves the CDN untouched.
    built = []
    for item_id, m in todo:
        d = work / item_id
        d.mkdir(exist_ok=True)
        # The tiles' stem, not the video's: a clip given music is
        # <stem>-mt<id>.mp4 while its poster and tiles keep <stem>.
        stem = Path(m["grid"][0]).name.rsplit("-g", 1)[0]
        video = fetch(f"{base}/{m['src']}", d / Path(m["src"]).name)
        frame = d / f"{stem}-frame.png"
        derive._extract_frame(video, frame, m.get("duration"))
        poster, thumb = d / Path(m["poster"]).name, d / Path(m["thumb"]).name
        derive._save_image(frame, poster, derive.IMAGE_MAX, derive.IMAGE_QUALITY)
        derive._save_image(frame, thumb, derive.THUMB_MAX, derive.THUMB_QUALITY)
        grid, color = derive._grid(poster, d, stem)
        if [f"{Path(m['src']).parent}/{g}" for g in grid] != m.get("grid", []):
            raise RuntimeError(f"{item_id}: grid names changed ({grid}); nothing uploaded")
        print(f"  {item_id}: frame luma {derive.frame_luma(frame):.0f}, colour {m.get('color')} -> {color}")
        built.append((item_id, m, stem, color, [poster, thumb] + [d / g for g in grid]))

    paths = []
    for item_id, m, stem, color, files in built:
        for f in files:
            key = f"{Path(m['src']).parent}/{f.name}"
            subprocess.run(["aws", "s3", "cp", str(f), f"s3://{cfg['bucket']}/{key}",
                            "--content-type", CONTENT_TYPES[f.suffix],
                            "--cache-control", publish.CACHE_CONTROL, "--only-show-errors"], check=True)
            paths.append("/" + key)
        text = set_color(text, m["grid"][0], color)
        for rec in lock.values():
            if isinstance(rec, dict) and stem in (rec.get("grid") or [""])[0]:
                rec["color"] = color
    publish.invalidate(cfg["distribution_id"], paths)
    data_path.write_text(text, encoding="utf-8")
    if lock:
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"uploaded and invalidated {len(paths)} file(s); updated {data_path.name} and the lock")
    return 0


if __name__ == "__main__":
    sys.exit(main())
