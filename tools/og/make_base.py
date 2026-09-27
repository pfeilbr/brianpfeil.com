#!/usr/bin/env python3
"""Write assets/og/base.png, the background every share card is drawn on.

Hugo (partials/og-image.html) adds the section label, title, avatar and
name at build time; this only paints the 1200x630 backdrop: the site's dark
colour with a soft teal glow from the top right and an accent bar down the
left edge. Pure standard library, so it runs anywhere and always writes the
same bytes.
"""
import pathlib
import struct
import zlib

W, H = 1200, 630
BG = (15, 17, 21)        # --bg in dark mode (#0f1115)
GLOW = (13, 126, 168)    # the site's accent (#0d7ea8)
BAR = 14                 # accent bar width, px

ROOT = pathlib.Path(__file__).resolve().parents[2] / "assets" / "og"
OUT = ROOT / "base.png"
MASK = ROOT / "avatar-mask.png"   # white disc on black: images.Mask keeps the white
M = 112                            # avatar size on the card, px
TITLE = ROOT / "title-canvas.png"  # transparent box the title is drawn on,
TW, TH = 1040, 320                 # so it wraps 80px short of the right edge


def pixel(x, y):
    if x < BAR:
        return GLOW
    # distance from the top-right corner, 0 there and 1 at ~1000px away
    d = min(1.0, (((W - x) ** 2 + y ** 2) ** 0.5) / 1000)
    t = (1 - d) ** 2 * 0.35
    return tuple(round(b + (g - b) * t) for b, g in zip(BG, GLOW))


def png(width, height, rows, alpha=False):
    def chunk(kind, data):
        c = kind + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + bytes(v for p in row for v in p) for row in rows)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6 if alpha else 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def main():
    rows = [[pixel(x, y) for x in range(W)] for y in range(H)]
    OUT.write_bytes(png(W, H, rows))
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    r = M / 2
    disc = [[(255,) * 3 if (x + .5 - r) ** 2 + (y + .5 - r) ** 2 <= r * r else (0,) * 3
             for x in range(M)] for y in range(M)]
    MASK.write_bytes(png(M, M, disc))
    print(f"wrote {MASK}")
    TITLE.write_bytes(png(TW, TH, [[(0, 0, 0, 0)] * TW for _ in range(TH)], alpha=True))
    print(f"wrote {TITLE}")


if __name__ == "__main__":
    main()
