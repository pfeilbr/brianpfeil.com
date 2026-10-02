#!/usr/bin/env python3
"""Write an app's tile for /apps/ to static/images/apps/<key>.webp.

Icons are copied in and downscaled, never hotlinked (same rule as avatars).
Either take the app's own icon, or draw one -- an emoji on a rounded,
gradient square, matching the look of the PWA icons -- for an app that has
none (Money Trees).

    uv run --with pillow tools/apps/icon.py --key mandarin --from ~/projects/chinese-mandarin-language-app/web/icons/icon-512.png
    uv run --with pillow tools/apps/icon.py --key money-trees --emoji 🌳 --colors '#24412f,#0c1410'

Deterministic: the same input always writes the same file.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "static" / "images" / "apps"
SIZE = 128          # shown at 56 CSS px; 2x plus headroom
EMOJI_FONT = "/System/Library/Fonts/Apple Color Emoji.ttc"
EMOJI_PX = 160      # Apple Color Emoji only has bitmap strikes at fixed sizes


def gradient_tile(top: str, bottom: str, size: int = 512) -> Image.Image:
    """A vertical gradient clipped to the iOS-ish rounded square."""
    a = Image.new("RGB", (size, size), top)
    b = Image.new("RGB", (size, size), bottom)
    ramp = Image.linear_gradient("L").resize((size, size))
    tile = Image.composite(b, a, ramp).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=size * 0.225, fill=255)
    tile.putalpha(mask)
    return tile


def emoji_icon(emoji: str, top: str, bottom: str) -> Image.Image:
    # Sized so the emoji's native strike fills ~62% of the tile with no upscaling.
    tile = gradient_tile(top, bottom, size=256)
    font = ImageFont.truetype(EMOJI_FONT, EMOJI_PX)
    glyph = Image.new("RGBA", (EMOJI_PX * 2, EMOJI_PX * 2), (0, 0, 0, 0))
    ImageDraw.Draw(glyph).text((EMOJI_PX // 2, EMOJI_PX // 2), emoji, font=font, embedded_color=True)
    glyph = glyph.crop(glyph.getbbox())
    side = int(tile.width * 0.62)
    scale = side / max(glyph.size)
    glyph = glyph.resize((round(glyph.width * scale), round(glyph.height * scale)), Image.LANCZOS)
    tile.alpha_composite(glyph, ((tile.width - glyph.width) // 2, (tile.height - glyph.height) // 2))
    return tile


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True, help="the app's key in data/apps.json")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--from", dest="src", type=Path, help="the app's own icon (PNG)")
    src.add_argument("--emoji", help="draw a tile with this emoji instead")
    ap.add_argument("--colors", default="#24412f,#0c1410", help="gradient top,bottom for --emoji")
    args = ap.parse_args(argv)

    if args.src:
        img = Image.open(args.src.expanduser()).convert("RGBA")
    else:
        top, bottom = args.colors.split(",")
        img = emoji_icon(args.emoji, top.strip(), bottom.strip())
    img = img.resize((SIZE, SIZE), Image.LANCZOS)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{args.key}.webp"
    img.save(out, "WEBP", quality=90, method=6)
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
