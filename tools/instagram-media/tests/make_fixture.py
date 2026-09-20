#!/usr/bin/env python3
"""Build a synthetic Instagram export for testing.

Real exports carry personal media, so the tests run against generated files
that reproduce the shapes that matter: a carousel, a single photo, a video
post, a reel in its own wrapper key, mojibake captions, and an entry whose
media file is missing.
"""

import json
import subprocess
import sys
from pathlib import Path


def ff(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *args], check=True)


def build(root: Path) -> None:
    activity = root / "your_instagram_activity" / "media"
    activity.mkdir(parents=True, exist_ok=True)
    (root / "media" / "posts" / "202301").mkdir(parents=True, exist_ok=True)
    (root / "media" / "posts" / "202205").mkdir(parents=True, exist_ok=True)
    (root / "media" / "reels" / "202403").mkdir(parents=True, exist_ok=True)

    ff(["-f", "lavfi", "-i", "testsrc2=size=1920x1440:rate=1", "-frames:v", "1",
        str(root / "media/posts/202301/a.jpg")])
    ff(["-f", "lavfi", "-i", "smptebars=size=1440x1920:rate=1", "-frames:v", "1",
        str(root / "media/posts/202301/b.jpg")])
    ff(["-f", "lavfi", "-i", "rgbtestsrc=size=1200x1200:rate=1", "-frames:v", "1",
        str(root / "media/posts/202205/c.jpg")])
    ff(["-f", "lavfi", "-i", "testsrc2=size=1080x1920:rate=30", "-f", "lavfi",
        "-i", "sine=frequency=440", "-t", "3", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest", str(root / "media/posts/202205/d.mp4")])
    ff(["-f", "lavfi", "-i", "testsrc2=size=1080x1350:rate=30", "-f", "lavfi",
        "-i", "sine=frequency=330", "-t", "2", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest", str(root / "media/reels/202403/e.mp4")])

    # "Café \U0001f600" as Instagram writes it: UTF-8 bytes decoded as latin-1.
    mojibake = "Café \U0001f600 carousel".encode("utf-8").decode("latin-1")

    posts = [
        {
            "media": [
                {"uri": "media/posts/202301/a.jpg", "creation_timestamp": 1672574400, "title": ""},
                {"uri": "media/posts/202301/b.jpg", "creation_timestamp": 1672574400, "title": ""},
            ],
            "title": mojibake,
            "creation_timestamp": 1672574400,
        },
        {
            "media": [
                {"uri": "media/posts/202205/c.jpg", "creation_timestamp": 1652918400,
                 "title": "Single photo caption"}
            ],
            "creation_timestamp": 1652918400,
        },
        {
            "media": [
                {"uri": "media/posts/202205/d.mp4", "creation_timestamp": 1653004800,
                 "title": "A video post"}
            ],
            "creation_timestamp": 1653004800,
        },
        {
            "media": [
                {"uri": "media/posts/202301/gone.jpg", "creation_timestamp": 1672574400,
                 "title": "file not in the export"}
            ],
            "creation_timestamp": 1672574400,
        },
    ]
    reels = {
        "ig_reels_media": [
            {
                "media": [{"uri": "media/reels/202403/e.mp4", "creation_timestamp": 1709424000,
                           "title": "A reel"}],
                "creation_timestamp": 1709424000,
            }
        ]
    }

    (activity / "posts_1.json").write_text(json.dumps(posts, indent=2), encoding="utf-8")
    (activity / "reels.json").write_text(json.dumps(reels, indent=2), encoding="utf-8")


if __name__ == "__main__":
    dest = Path(sys.argv[1]).expanduser()
    dest.mkdir(parents=True, exist_ok=True)
    build(dest)
    print(f"fixture export written to {dest}")
