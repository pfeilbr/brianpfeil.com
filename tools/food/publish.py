#!/usr/bin/env python3
"""Publish a food gallery to /food/: the labeled dish stills and the video of one food montage.

The media library makes the gallery (~/projects/media, publish/scripts/food_gallery.py): every dish of a
montage as a 1080x1920 still with its on-screen label, the posted video and a manifest.json, kept in
s3://com.brianpfeil.media/derived/review/food-gallery/<key>/. This reads that folder (or a local copy), makes the
web sizes (WebP 360/720 wide for the grid, 1080 for the viewer, a poster for the video), uploads them to the
site's CDN bucket under food/<key>/ and writes the collection into data/food.json, newest first. File names
carry a content hash, so every URL is cached for a year and a re-run uploads nothing new. Only titles, sections
and file names reach the page: the manifest's photo ids and dates stay in the library.

  uv run --with pillow tools/food/publish.py KEY [--src DIR|s3://...] [--data-only] [--dry-run]

KEY is the collection id (e.g. 2026-11-15-everything-i-eat). The video goes up as is (same file, same encode).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data" / "food.json"
BUILD = Path(__file__).resolve().parent / "build"
LIBRARY = "s3://com.brianpfeil.media/derived/review/food-gallery"
BUCKET = "brianpfeil-media01"
PREFIX = "food"
BASE_URL = "https://dfalwjniugna7.cloudfront.net/"
CACHE = "public, max-age=31536000, immutable"
GRID = (360, 720)
FULL = 1080


def short_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:10]


def stem(file: str) -> str:
    """stills/012-peking-duck.jpg -> 012-peking-duck"""
    return Path(file).stem


def collection(manifest: dict, names: dict[str, dict]) -> dict:
    """The page's record for one collection: only what the page shows. `names` maps a manifest file to its
    uploaded names ({"g": [360w, 720w], "s": full} for stills, {"src", "poster"} for the video)."""
    v = manifest["video"]
    out = {
        "key": manifest["key"],
        "date": manifest["date"],
        "title": manifest["title"],
        "subtitle": manifest.get("subtitle", ""),
        "video": {**names[v["file"]], "w": v["width"], "h": v["height"], "d": round(v["duration"])},
        "sections": [],
    }
    for s in manifest["sections"]:
        out["sections"].append({"key": s["key"], "items": [{"t": i["title"], **names[i["file"]]} for i in s["items"]]})
    return out


def merge(data: dict | None, col: dict) -> dict:
    """data/food.json with `col` in place of any collection of the same key, newest date first."""
    cols = [c for c in (data or {}).get("collections", []) if c["key"] != col["key"]] + [col]
    cols.sort(key=lambda c: (c["date"], c["key"]), reverse=True)
    return {"base_url": BASE_URL, "photos": sum(len(i["items"]) for c in cols for i in c["sections"]), "collections": cols}


def fetch(src: str, key: str) -> Path:
    if not src.startswith("s3://"):
        return Path(src)
    local = BUILD / "src" / key
    subprocess.run(["aws", "s3", "sync", src.rstrip("/") + "/", str(local), "--only-show-errors"], check=True)
    return local


def make_sizes(src_dir: Path, manifest: dict, out: Path) -> dict[str, dict]:
    """WebP grid + full sizes for each still and a poster for the video, named <stem>-<hash>-<w>.webp."""
    from PIL import Image

    names: dict[str, dict] = {}
    for s in manifest["sections"]:
        for it in s["items"]:
            f = src_dir / it["file"]
            h = short_hash(f)
            im = Image.open(f).convert("RGB")
            rec = {"g": [], "s": ""}
            for w in (*GRID, FULL):
                name = f"{stem(it['file'])}-{h}-{w}.webp"
                if not (out / name).exists():
                    im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out / name, "WEBP", quality=80 if w < FULL else 84, method=4)
                if w == FULL:
                    rec["s"] = name
                else:
                    rec["g"].append(name)
            names[it["file"]] = rec
    v = src_dir / manifest["video"]["file"]
    h = short_hash(v)
    video = f"video-{h}.mp4"
    poster = f"video-{h}-poster.webp"
    if not (out / video).exists():
        shutil.copyfile(v, out / video)  # as is: no re-encode
    if not (out / poster).exists():
        jpg = out / f"video-{h}-poster.jpg"
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", "1", "-i", str(v), "-frames:v", "1",
                        "-vf", "scale=720:-2", str(jpg)], check=True)  # fmt: skip
        Image.open(jpg).save(out / poster, "WEBP", quality=80)
        jpg.unlink()
    names[manifest["video"]["file"]] = {"src": video, "poster": poster}
    return names


def upload(out: Path, key: str) -> None:
    subprocess.run(["aws", "s3", "sync", str(out), f"s3://{BUCKET}/{PREFIX}/{key}/", "--cache-control", CACHE,
                    "--only-show-errors"], check=True)  # fmt: skip


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("key", help="collection id, e.g. 2026-11-15-everything-i-eat")
    ap.add_argument("--src", help=f"gallery folder (default {LIBRARY}/<key>/)")
    ap.add_argument("--data-only", action="store_true", help="write data/food.json from files already built, no upload")
    ap.add_argument("--dry-run", action="store_true", help="show what would change; write and upload nothing")
    a = ap.parse_args(argv)
    src = fetch(a.src or f"{LIBRARY}/{a.key}/", a.key)
    manifest = json.loads((src / "manifest.json").read_text())
    n = sum(len(s["items"]) for s in manifest["sections"])
    print(f"{a.key}: {n} photos in {len(manifest['sections'])} sections + video ({manifest['video']['duration']:.0f} s)")
    if a.dry_run:
        return 0
    out = BUILD / "out" / a.key
    out.mkdir(parents=True, exist_ok=True)
    names = make_sizes(src, manifest, out)
    names = {k: {f: ([f"{PREFIX}/{a.key}/{x}" for x in v] if isinstance(v, list) else f"{PREFIX}/{a.key}/{v}") for f, v in r.items()}
             for k, r in names.items()}  # fmt: skip
    if not a.data_only:
        upload(out, a.key)
    data = merge(json.loads(DATA.read_text()) if DATA.exists() else None, collection(manifest, names))
    DATA.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {DATA.relative_to(REPO)}: {len(data['collections'])} collection(s), {data['photos']} photos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
