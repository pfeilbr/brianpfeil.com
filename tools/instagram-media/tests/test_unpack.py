"""Tests for turning whatever Instagram hands over into one export tree.

A large account does not come back as a single archive: Instagram splits it
into parts, with the JSON in one and media spread across the rest, so the
parts only mean anything merged.
"""

import json
import sys
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from igmedia import export  # noqa: E402

POSTS = [
    {
        "media": [{"uri": "media/posts/a.jpg", "creation_timestamp": 1672574400}],
        "title": "from part one",
        "creation_timestamp": 1672574400,
    },
    {
        "media": [{"uri": "media/posts/b.jpg", "creation_timestamp": 1672574400}],
        "title": "media lives in part two",
        "creation_timestamp": 1672574400,
    },
]


class UnpackPartsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.work = self.root / "work"

        # part 1: the JSON and one photo. part 2: the other photo only.
        self.part1 = self.root / "instagram-part-1.zip"
        with zipfile.ZipFile(self.part1, "w") as zf:
            zf.writestr("your_instagram_activity/media/posts_1.json", json.dumps(POSTS))
            zf.writestr("media/posts/a.jpg", b"photo-a")
        self.part2 = self.root / "instagram-part-2.zip"
        with zipfile.ZipFile(self.part2, "w") as zf:
            zf.writestr("media/posts/b.jpg", b"photo-b")

    def test_a_single_part_misses_the_media_in_the_other(self):
        root = export.unpack([self.part1], self.work)
        captions = [i.caption for i in export.read_items(root)]
        self.assertEqual(captions, ["from part one"])

    def test_parts_listed_together_are_merged(self):
        root = export.unpack([self.part1, self.part2], self.work)
        captions = sorted(i.caption for i in export.read_items(root))
        self.assertEqual(captions, ["from part one", "media lives in part two"])

    def test_a_directory_of_parts_is_merged(self):
        root = export.unpack([self.root], self.work)
        captions = sorted(i.caption for i in export.read_items(root))
        self.assertEqual(captions, ["from part one", "media lives in part two"])

    def test_adding_a_part_later_re_extracts(self):
        """The cache key covers every part, so a second part isn't ignored."""
        first = export.unpack([self.part1], self.work)
        second = export.unpack([self.part1, self.part2], self.work)
        self.assertNotEqual(first, second)
        self.assertEqual(len(export.read_items(second)), 2)

    def test_an_unpacked_directory_is_used_as_is(self):
        unpacked = self.root / "already-unpacked"
        (unpacked / "your_instagram_activity" / "media").mkdir(parents=True)
        (unpacked / "your_instagram_activity" / "media" / "posts_1.json").write_text(
            json.dumps(POSTS[:1])
        )
        (unpacked / "media" / "posts").mkdir(parents=True)
        (unpacked / "media" / "posts" / "a.jpg").write_bytes(b"photo-a")

        self.assertEqual(export.unpack([unpacked], self.work), unpacked)

    def test_re_extraction_is_skipped_for_the_same_parts(self):
        first = export.unpack([self.part1, self.part2], self.work)
        marker = first / ".extracted"
        stamp = marker.stat().st_mtime_ns
        again = export.unpack([self.part1, self.part2], self.work)
        self.assertEqual(first, again)
        self.assertEqual(marker.stat().st_mtime_ns, stamp)

    def test_a_directory_with_no_zips_and_no_export_is_rejected(self):
        empty = self.root / "empty"
        empty.mkdir()
        # Looks like an unpacked export but has nothing in it; read_items will
        # simply find no posts, which stage reports rather than crashing on.
        self.assertEqual(export.unpack([empty], self.work), empty)
        self.assertEqual(export.read_items(empty), [])

    def test_a_non_zip_file_is_rejected(self):
        stray = self.root / "notes.txt"
        stray.write_text("hello")
        with self.assertRaises(ValueError):
            export.unpack([stray], self.work)


if __name__ == "__main__":
    unittest.main()
