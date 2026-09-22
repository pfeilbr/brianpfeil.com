"""Tests for stories: reading them from an export, labelling reshares, and
combining them with the archive without duplicating anything."""

import argparse
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pull  # noqa: E402
from igmedia import export, stories  # noqa: E402
from igmedia.export import Item, Media  # noqa: E402

# 2026-08-30 00:53 in New York is 04:53 UTC.
def at(local_hhmm: str, day: str = "2026-08-30") -> datetime:
    naive = datetime.fromisoformat(f"{day}T{local_hhmm}:00")
    return naive.replace(tzinfo=stories.LOCAL).astimezone(timezone.utc)


def story(item_id: str, when: datetime) -> Item:
    return Item(id=item_id, taken_at=when, caption="", kind="photo",
                media=[Media(Path("x.jpg"), "photo", "0" * 64, when)], details={"story": True})


def inv(day, seq, of, hhmm, reshare=None):
    return {"day": day, "seq": seq, "of": of, "local_time": hhmm,
            "audio": "reshare" if reshare else "none", "reshare_of": reshare}


class ReshareTagTest(unittest.TestCase):
    def test_counts_line_up_so_reshares_are_labelled_by_position(self):
        items = [story("a", at("00:53")), story("b", at("01:50")), story("c", at("01:50")),
                 story("d", at("02:10"))]
        inventory = [inv("2026-08-30", 1, 4, "00:53"), inv("2026-08-30", 2, 4, "01:50"),
                     inv("2026-08-30", 3, 4, "01:50", "other_post"),
                     inv("2026-08-30", 4, 4, "02:10", "own_reel")]
        tagged = stories.tag_reshares(items, inventory)
        # b and c share a minute; position still tells them apart.
        self.assertEqual({i.id: r for i, r in tagged}, {
            "c": "reshare of someone else's post",
            "d": "reshare of a reel already on the page",
        })
        self.assertEqual([i.details.get("reshare") for i in items],
                         [None, None, "other_post", "own_reel"])
        # Nothing is dropped: every story stays in the list it came in.
        self.assertEqual(len(items), 4)

    def test_counts_differ_so_the_whole_minute_is_labelled(self):
        """Erring toward over-labelling one of B's stories, never presenting
        someone else's post as B's."""
        items = [story("a", at("01:50")), story("b", at("01:50")), story("c", at("02:10"))]
        inventory = [inv("2026-08-30", 1, 2, "01:50", "other_post"), inv("2026-08-30", 2, 2, "02:10")]
        tagged = stories.tag_reshares(items, inventory)
        self.assertEqual(sorted(i.id for i, _ in tagged), ["a", "b"])
        self.assertIsNone(items[2].details.get("reshare"))

    def test_days_without_reshares_or_inventory_pass_through(self):
        items = [story("a", at("09:00", "2026-09-01")), story("b", at("09:00", "2026-07-01"))]
        inventory = [inv("2026-09-01", 1, 1, "09:00")]
        self.assertEqual(stories.tag_reshares(items, inventory), [])
        self.assertTrue(all("reshare" not in i.details for i in items))

    def test_posts_are_never_touched(self):
        post = Item(id="p", taken_at=at("01:50"), caption="", kind="photo", media=[])
        self.assertEqual(stories.tag_reshares([post], [inv("2026-08-30", 1, 1, "01:50", "other_post")]), [])
        self.assertEqual(post.details, {})

    def test_no_inventory_keeps_everything(self):
        self.assertEqual(stories.load_inventory(None), [])
        self.assertEqual(stories.load_inventory(Path("/nonexistent.jsonl")), [])


def write_export(root: Path) -> Path:
    media = root / "your_instagram_activity" / "media"
    media.mkdir(parents=True)
    for rel, data in {"media/posts/p.jpg": b"post", "media/stories/s1.jpg": b"story-1",
                      "media/stories/s2.mp4": b"story-2"}.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_bytes(data)
    (media / "posts_1.json").write_text(json.dumps([
        {"media": [{"uri": "media/posts/p.jpg", "creation_timestamp": 1700000000}],
         "title": "a post", "creation_timestamp": 1700000000}]))
    (media / "stories.json").write_text(json.dumps({"ig_stories": [
        {"uri": "media/stories/s1.jpg", "creation_timestamp": 1788000000, "title": "first"},
        {"uri": "media/stories/s2.mp4", "creation_timestamp": 1788000600, "title": ""},
    ]}))
    return root


class ExportStoriesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = write_export(Path(self.tmp.name) / "export")

    def test_stories_are_read_only_when_asked(self):
        self.assertEqual(len(export.read_items(self.root)), 1)
        both = export.read_items(self.root, stories=True)
        self.assertEqual(len(both), 3)

    def test_a_story_is_its_own_single_media_item(self):
        only = export.read_items(self.root, stories=True, posts=False)
        self.assertEqual(sorted(i.kind for i in only), ["photo", "video"])
        self.assertTrue(all(i.details.get("story") for i in only))
        self.assertEqual(sorted(i.caption for i in only), ["", "first"])


class CombinedSourceTest(unittest.TestCase):
    """The archive owns posts and reels; an export adds stories only."""

    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.export = write_export(base / "export")
        self.archive = base / "archive"
        d = self.archive / "posts" / "2025" / "2025-03-14__SHORT1"
        (d / "media").mkdir(parents=True)
        (self.archive / "reels").mkdir()
        (d / "media" / "01.jpg").write_bytes(b"archived post")
        (d / "metadata.json").write_text(json.dumps({
            "id": "SHORT1", "kind": "post", "taken_at": "2025-03-14T15:14:59Z",
            "media": [{"index": 1, "type": "image", "file": "media/01.jpg"}],
            "caption": {"text": "from the archive"}}))
        self.cfg = {"archive_dir": str(self.archive), "story_inventory": None}

    def load(self, **kw):
        args = argparse.Namespace(archive=None, export=kw.get("export"),
                                  no_archive=kw.get("no_archive", False))
        return pull.load_items(args, self.cfg, Path(self.tmp.name) / "work")

    def test_archive_alone(self):
        self.assertEqual([i.caption for i in self.load()], ["from the archive"])

    def test_export_adds_stories_but_not_its_posts(self):
        items = self.load(export=[self.export])
        captions = sorted(i.caption for i in items)
        self.assertEqual(captions, ["", "first", "from the archive"])
        self.assertNotIn("a post", captions)   # the export's copy of a post

    def add_archived(self, entries):
        (self.export / "media/archived_posts").mkdir(parents=True, exist_ok=True)
        for n, e in enumerate(entries):
            (self.export / f"media/archived_posts/h{n}.jpg").write_bytes(f"hidden-{n}".encode())
            e["media"] = [{"uri": f"media/archived_posts/h{n}.jpg",
                           "creation_timestamp": e["creation_timestamp"]}]
        (self.export / "your_instagram_activity/media/archived_posts.json").write_text(
            json.dumps({"ig_archived_post_media": entries}))

    def test_export_adds_posts_archived_off_the_profile(self):
        self.add_archived([{"title": "hidden from the grid", "creation_timestamp": 1500000000}])
        items = {i.caption: i for i in self.load(export=[self.export])}
        self.assertIn("hidden from the grid", items)
        self.assertTrue(items["hidden from the grid"].details.get("archived"))

    def test_a_restored_post_is_not_shown_twice(self):
        # Same second as the archive's SHORT1 (2025-03-14T15:14:59Z): it was
        # archived once and put back, so the profile copy is the one to keep.
        self.add_archived([{"title": "restored", "creation_timestamp": 1741965299}])
        captions = [i.caption for i in self.load(export=[self.export])]
        self.assertNotIn("restored", captions)
        self.assertIn("from the archive", captions)

    def test_no_archive_uses_the_export_for_everything(self):
        captions = sorted(i.caption for i in self.load(export=[self.export], no_archive=True))
        self.assertEqual(captions, ["", "a post", "first"])


if __name__ == "__main__":
    unittest.main()
