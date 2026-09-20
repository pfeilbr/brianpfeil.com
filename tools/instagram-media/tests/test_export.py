"""Tests for reading an Instagram export.

These use dummy files rather than real media: read_items only cares about the
JSON, the file extension and the bytes it hashes, so nothing here needs
ffmpeg. tests/make_fixture.py builds a real-media export for end-to-end runs.
"""

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from igmedia import export  # noqa: E402


def write_export(root: Path, posts: list, reels: dict | None = None) -> None:
    activity = root / "your_instagram_activity" / "media"
    activity.mkdir(parents=True, exist_ok=True)
    (activity / "posts_1.json").write_text(json.dumps(posts), encoding="utf-8")
    if reels is not None:
        (activity / "reels.json").write_text(json.dumps(reels), encoding="utf-8")


def add_media(root: Path, rel: str, content: bytes) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


class MojibakeTest(unittest.TestCase):
    def test_undoes_metas_double_encoding(self):
        original = "Café 😀"
        as_exported = original.encode("utf-8").decode("latin-1")
        self.assertEqual(export.fix_mojibake(as_exported), original)

    def test_leaves_clean_text_alone(self):
        self.assertEqual(export.fix_mojibake("plain ascii"), "plain ascii")

    def test_leaves_undecodable_text_alone(self):
        # Already-correct non-latin text cannot be latin-1 encoded; it must
        # come back untouched rather than raising.
        self.assertEqual(export.fix_mojibake("日本語"), "日本語")

    def test_empty(self):
        self.assertEqual(export.fix_mojibake(""), "")


class ReadItemsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

        add_media(self.root, "media/posts/a.jpg", b"photo-a")
        add_media(self.root, "media/posts/b.jpg", b"photo-b")
        add_media(self.root, "media/posts/c.mp4", b"video-c")
        add_media(self.root, "media/reels/d.mp4", b"reel-d")

        write_export(
            self.root,
            posts=[
                {
                    "media": [
                        {"uri": "media/posts/a.jpg", "creation_timestamp": 1672574400},
                        {"uri": "media/posts/b.jpg", "creation_timestamp": 1672574400},
                    ],
                    "title": "carousel",
                    "creation_timestamp": 1672574400,
                },
                {
                    "media": [{"uri": "media/posts/c.mp4", "creation_timestamp": 1653004800,
                               "title": "video caption"}],
                    "creation_timestamp": 1653004800,
                },
                {
                    "media": [{"uri": "media/posts/nope.jpg", "creation_timestamp": 1653004800}],
                    "creation_timestamp": 1653004800,
                },
            ],
            reels={"ig_reels_media": [
                {"media": [{"uri": "media/reels/d.mp4", "creation_timestamp": 1709424000}],
                 "title": "reel", "creation_timestamp": 1709424000}
            ]},
        )

    def test_skips_entries_whose_file_is_absent(self):
        ids = [i.id for i in export.read_items(self.root)]
        self.assertEqual(len(ids), 3)

    def test_reads_reels_from_their_wrapper_key(self):
        captions = [i.caption for i in export.read_items(self.root)]
        self.assertIn("reel", captions)

    def test_kinds(self):
        by_caption = {i.caption: i for i in export.read_items(self.root)}
        self.assertEqual(by_caption["carousel"].kind, "album")
        self.assertEqual(by_caption["video caption"].kind, "video")
        self.assertEqual(len(by_caption["carousel"].media), 2)

    def test_caption_falls_back_to_the_media_entry(self):
        by_kind = {i.kind: i for i in export.read_items(self.root)}
        self.assertEqual(by_kind["video"].caption, "video caption")

    def test_newest_first(self):
        dates = [i.date for i in export.read_items(self.root)]
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test_ids_are_stable_across_runs(self):
        first = [i.id for i in export.read_items(self.root)]
        second = [i.id for i in export.read_items(self.root)]
        self.assertEqual(first, second)

    def test_id_tracks_content_not_filename(self):
        """The same bytes under a new name keep the id — that is what lets the
        approve list survive a re-export."""
        before = {i.caption: i.id for i in export.read_items(self.root)}

        renamed = Path(self.tmp.name) / "media/posts/c-renamed.mp4"
        (Path(self.tmp.name) / "media/posts/c.mp4").rename(renamed)
        posts = json.loads((self.root / "your_instagram_activity/media/posts_1.json").read_text())
        posts[1]["media"][0]["uri"] = "media/posts/c-renamed.mp4"
        (self.root / "your_instagram_activity/media/posts_1.json").write_text(json.dumps(posts))

        after = {i.caption: i.id for i in export.read_items(self.root)}
        self.assertEqual(before["video caption"], after["video caption"])

    def test_id_changes_when_the_media_changes(self):
        before = {i.caption: i.id for i in export.read_items(self.root)}
        (self.root / "media/posts/c.mp4").write_bytes(b"different-bytes")
        after = {i.caption: i.id for i in export.read_items(self.root)}
        self.assertNotEqual(before["video caption"], after["video caption"])


class UnpackTest(unittest.TestCase):
    def test_rejects_a_traversal_path(self):
        import zipfile

        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        archive = root / "evil.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            zf.writestr("../escaped.txt", "nope")

        with self.assertRaises(ValueError):
            export.unpack(archive, root / "work")


if __name__ == "__main__":
    unittest.main()
