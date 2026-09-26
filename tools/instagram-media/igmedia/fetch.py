"""What the browser is asked to download, how to check what it sent, and
frames from videos.

Google's image host answers only B's signed-in browser (a plain request from
Python gets 403), so the Mac never fetches from Google itself: the harvest
script in the Google Photos tab downloads each file and posts the bytes to
the picker. Nothing here makes a network request.
"""

import subprocess
from pathlib import Path

# Size suffixes on Google's image URLs, tried in order until one works:
# =wW-hH a JPEG of at most that size; =mNN an MP4 rendition (18: 360p,
# 22: 720p, 37: 1080p); =dv the original video. The site caps photos at
# 1600px and video at 1280px, so "large" and "hq" are all publishing needs —
# the original is never required.
SUFFIXES = {
    "small": ["=w480-h480"],
    "large": ["=w1600-h1600"],
    "preview": ["=m18", "=m22", "=dv"],
    "hq": ["=m37", "=m22", "=dv"],
}
MAX_BYTES = {"small": 5 << 20, "large": 30 << 20, "preview": 200 << 20, "hq": 2 << 30}


def sniff(data: bytes) -> str:
    """"image", "video" or "other", from the bytes rather than a header."""
    if data[:3] == b"\xff\xd8\xff" or data[:8] == b"\x89PNG\r\n\x1a\n" or data[8:12] == b"WEBP":
        return "image"
    if data[4:8] == b"ftyp":
        brand = data[8:12]
        return "image" if brand in (b"heic", b"heix", b"mif1", b"avif") else "video"
    return "other"


def duration(path: Path) -> float | None:
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True)
    try:
        return float(p.stdout.strip())
    except ValueError:
        return None


def frames(video: Path, outdir: Path, count: int = 6) -> list[Path]:
    """Evenly spaced stills — the first and last seconds included, since a
    clip that ends by panning to someone else should not slip through."""
    dur = duration(video) or 0
    outdir.mkdir(parents=True, exist_ok=True)
    out = []
    for i in range(count):
        t = dur * (0.02 + 0.96 * i / max(count - 1, 1))
        dest = outdir / f"f{i}.jpg"
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", f"{t:.2f}",
                        "-i", str(video), "-frames:v", "1", "-q:v", "3", str(dest)],
                       capture_output=True)
        if dest.exists():
            out.append(dest)
    return out
