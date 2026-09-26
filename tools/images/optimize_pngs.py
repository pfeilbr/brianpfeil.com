#!/usr/bin/env python3
"""Shrink heavy PNGs under content/ and static/ in place, keeping their names.

Screenshots and photos saved as PNG are often 1 MB+ for what renders at a
couple of hundred pixels wide. This quantizes each PNG over --min-kb to a
256-colour palette (no dithering, metadata stripped) and keeps the result
only if it is both clearly smaller and visually close:

- at least --min-saving smaller (default 30%), and
- PSNR against the original of at least --min-psnr dB (default 35).

Anything that fails either test is left untouched, so re-running is safe
and a no-op once everything that can shrink has.

    python3 tools/images/optimize_pngs.py            # report what would change
    python3 tools/images/optimize_pngs.py --apply    # rewrite in place

Needs ImageMagick 7 (`magick`) on PATH.
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ROOTS = ("content", "static")


def psnr(a: Path, b: Path) -> float:
    out = subprocess.run(["magick", "compare", "-metric", "PSNR", str(a), str(b), "null:"],
                         capture_output=True, text=True)
    m = re.match(r"\s*([\d.]+|inf)", out.stderr or out.stdout)
    return float("inf") if not m or m.group(1) == "inf" else float(m.group(1))


def candidate(src: Path, tmp: Path) -> Path:
    dst = tmp / src.name
    subprocess.run(["magick", str(src), "-strip", "+dither", "-colors", "256",
                    "-define", "png:compression-level=9", str(dst)], check=True)
    return dst


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--min-kb", type=int, default=300)
    ap.add_argument("--min-saving", type=float, default=0.30)
    ap.add_argument("--min-psnr", type=float, default=35.0)
    args = ap.parse_args(argv)
    if not shutil.which("magick"):
        print("needs ImageMagick 7 (magick)", file=sys.stderr)
        return 1
    saved = 0
    with tempfile.TemporaryDirectory() as t:
        for root in ROOTS:
            for src in sorted((REPO / root).rglob("*.png")):
                before = src.stat().st_size
                if before < args.min_kb * 1024:
                    continue
                dst = candidate(src, Path(t))
                after = dst.stat().st_size
                quality = psnr(src, dst)
                ok = after <= before * (1 - args.min_saving) and quality >= args.min_psnr
                rel = src.relative_to(REPO)
                print(f"{'shrink' if ok else 'keep  '} {rel}: {before // 1024} KB -> {after // 1024} KB, PSNR {quality:.1f}")
                if ok:
                    saved += before - after
                    if args.apply:
                        shutil.copyfile(dst, src)
    print(f"{'saved' if args.apply else 'would save'} {saved / 1e6:.2f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
