"""Tests for reading the instagram-archive project's layout."""

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from igmedia import archive  # noqa: E402


def add_item(root: Path, section: str, folder: str, meta: dict, files: dict[str, bytes]) -> Path:
    d = root / section / folder[:4] / folder
    (d / "media").mkdir(parents=True)
    for name, content in files.items():
        (d / name).write_bytes(content)
    (d / "metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    return d


def meta(shortcode, kind, taken_at, local, media, caption="", location=True):
    m = {
        "id": shortcode, "kind": kind, "taken_at": taken_at, "taken_at_local": local,
        "caption": {"text": caption, "file": "caption.md"},
        "media": media,
        "tagged_users": [{"username": "someone"}],
    }
    if location:
        m["location"] = {"name": "Woody's", "lat": 39.9488443, "lng": -75.1623162}
    return m


class ArchiveTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "archive"
        for s in ("posts", "reels", "stories", "_oversized"):
            (self.root / s).mkdir(parents=True)

        add_item(self.root, "posts", "2025-03-14__CAROUSEL1",
                 meta("CAROUSEL1", "post", "2025-03-14T15:14:59Z", "2025-03-14T11:14:59-04:00",
                      [{"index": 2, "type": "video", "file": "media/02.mp4"},
                       {"index": 1, "type": "image", "file": "media/01.jpg"}],
                      caption="2025-03-13 | woody’s"),
                 {"media/01.jpg": b"img-1", "media/02.mp4": b"vid-2", "media/02.thumb.jpg": b"t"})
        add_item(self.root, "posts", "2011-10-01__OxAiV",
                 meta("OxAiV", "post", "2011-10-01T16:22:16Z", "2011-10-01T12:22:16-04:00",
                      [{"index": 1, "type": "image", "file": "media/01.jpg"}]),
                 {"media/01.jpg": b"old"})
        add_item(self.root, "reels", "2025-01-09__REEL1",
                 meta("REEL1", "reel", "2025-01-10T02:30:00Z", "2025-01-09T21:30:00-05:00",
                      [{"index": 1, "type": "video", "file": "media/01.mp4"}], caption="skiing"),
                 {"media/01.mp4": b"reel"})
        # A higher-bitrate duplicate of a reel, and a story: neither is published.
        add_item(self.root, "_oversized", "2025-01-09__REEL1",
                 meta("REEL1", "reel", "2025-01-10T02:30:00Z", "2025-01-09T21:30:00-05:00",
                      [{"index": 1, "type": "video", "file": "media/01.mp4"}]),
                 {"media/01.mp4": b"bigger"})
        add_item(self.root, "stories", "2025-02-01__STORY1",
                 meta("STORY1", "story", "2025-02-01T12:00:00Z", "2025-02-01T07:00:00-05:00",
                      [{"index": 1, "type": "image", "file": "media/01.jpg"}]),
                 {"media/01.jpg": b"story"})

    def items(self):
        return archive.read_archive(self.root)

    def test_reads_posts_and_reels_only(self):
        ids = {i.id for i in self.items()}
        self.assertEqual(ids, {"20250314-CAROUSEL1", "20111001-OxAiV", "20250109-REEL1"})

    def test_oversized_duplicates_are_not_published_twice(self):
        self.assertEqual(sum(1 for i in self.items() if i.id.endswith("REEL1")), 1)
        reel = next(i for i in self.items() if i.id.endswith("REEL1"))
        self.assertNotIn("_oversized", str(reel.media[0].path))

    def test_id_is_local_date_plus_shortcode(self):
        """21:30 on Jan 9 in New York is already Jan 10 in UTC; the post is
        dated the day it was taken."""
        reel = next(i for i in self.items() if i.id.endswith("REEL1"))
        self.assertEqual(reel.id, "20250109-REEL1")
        self.assertEqual(reel.date, "2025-01-09")

    def test_media_in_index_order_with_kinds(self):
        carousel = next(i for i in self.items() if i.id.endswith("CAROUSEL1"))
        self.assertEqual(carousel.kind, "album")
        self.assertEqual([m.path.name for m in carousel.media], ["01.jpg", "02.mp4"])
        self.assertEqual([m.kind for m in carousel.media], ["photo", "video"])

    def test_captions_kept_verbatim(self):
        carousel = next(i for i in self.items() if i.id.endswith("CAROUSEL1"))
        self.assertEqual(carousel.caption, "2025-03-13 | woody’s")

    def test_location_and_tagged_users_never_leave_the_module(self):
        for item in self.items():
            flat = json.dumps(item.__dict__, default=str)
            self.assertNotIn("39.9488", flat)
            self.assertNotIn("Woody's", flat.replace("woody’s", ""))
            self.assertNotIn("someone", flat)

    def test_newest_first(self):
        dates = [i.date for i in self.items()]
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test_media_hashes_are_of_the_files(self):
        old = next(i for i in self.items() if i.id.endswith("OxAiV"))
        import hashlib
        self.assertEqual(old.media[0].sha256, hashlib.sha256(b"old").hexdigest())

    def test_missing_media_file_is_skipped_and_an_empty_item_dropped(self):
        add_item(self.root, "posts", "2024-05-05__GONE",
                 meta("GONE", "post", "2024-05-05T12:00:00Z", "2024-05-05T08:00:00-04:00",
                      [{"index": 1, "type": "image", "file": "media/01.jpg"}]), {})
        self.assertNotIn("20240505-GONE", {i.id for i in self.items()})

    def test_not_an_archive(self):
        with self.assertRaises(ValueError):
            archive.read_archive(Path(self.tmp.name) / "nothing-here")


if __name__ == "__main__":
    unittest.main()
