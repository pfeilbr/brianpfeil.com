"""Tests for the approve list and the data file the site reads.

The manifest is the one hand-edited file in the tool, and losing an approval
on a re-export would quietly un-publish something. data/media.yaml is what
Hugo renders, so its shape and its determinism both matter.
"""

import sys
import unittest
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from igmedia import manifest, publish  # noqa: E402
from igmedia.derive import Derived  # noqa: E402


@dataclass
class FakeMedia:
    kind: str


@dataclass
class FakeItem:
    id: str
    caption: str
    kind: str
    taken_at: datetime
    media: list = field(default_factory=list)
    details: dict = field(default_factory=dict)

    @property
    def date(self) -> str:
        return self.taken_at.strftime("%Y-%m-%d")


def item(item_id, caption="", kind="photo", n=1, year=2023):
    return FakeItem(
        id=item_id, caption=caption, kind=kind,
        taken_at=datetime(year, 5, 17, tzinfo=timezone.utc),
        media=[FakeMedia(kind) for _ in range(n)],
    )


class ManifestTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "manifest.yaml"

    def test_new_items_arrive_unapproved(self):
        records = manifest.merge([item("a"), item("b")], {})
        self.assertEqual([r["approved"] for r in records], [False, False])

    def test_an_approval_survives_a_re_export(self):
        manifest.save(self.path, manifest.merge([item("a"), item("b")], {}))
        records = list(manifest.load(self.path).values())
        records[0]["approved"] = True
        manifest.save(self.path, records)

        # The next export has the same two posts plus a new one.
        again = manifest.merge([item("a"), item("b"), item("c")], manifest.load(self.path))
        by_id = {r["id"]: r["approved"] for r in again}
        self.assertEqual(by_id, {"a": True, "b": False, "c": False})

    def test_captions_round_trip_through_yaml(self):
        tricky = 'Café 😀 — "quoted", colon: yes, # not a comment\nsecond line'
        manifest.save(self.path, manifest.merge([item("a", caption=tricky)], {}))
        self.assertEqual(manifest.load(self.path)["a"]["caption"], tricky)

    def test_header_explains_itself(self):
        manifest.save(self.path, manifest.merge([item("a")], {}))
        self.assertTrue(self.path.read_text().startswith("# Approve list"))

    def test_approved_ids(self):
        records = [{"id": "a", "approved": True}, {"id": "b", "approved": False}, {"id": "c"}]
        self.assertEqual(manifest.approved_ids(records), {"a"})

    def test_missing_manifest_loads_empty(self):
        self.assertEqual(manifest.load(self.path), {})


def photo(key):
    return Derived(kind="photo", key=f"{key}.jpg", thumb_key=f"{key}-t.jpg",
                   poster_key=None, width=1600, height=1200, duration=None)


def video(key):
    return Derived(kind="video", key=f"{key}.mp4", thumb_key=f"{key}-t.jpg",
                   poster_key=f"{key}-p.jpg", width=720, height=1280, duration=12.5)


class DataFileTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "data" / "media.yaml"

    def test_photo_entry_shape(self):
        entry = publish.entry_for(item("a", caption="hi"), [photo("x")])
        self.assertEqual(entry["year"], "2023")
        self.assertEqual(entry["media"][0], {
            "kind": "photo", "src": "x.jpg", "thumb": "x-t.jpg", "w": 1600, "h": 1200,
        })

    def test_video_entry_carries_poster_and_duration(self):
        entry = publish.entry_for(item("v", kind="video"), [video("y")])
        media = entry["media"][0]
        self.assertEqual(media["poster"], "y-p.jpg")
        self.assertEqual(media["duration"], 12.5)

    def test_photos_carry_no_video_fields(self):
        entry = publish.entry_for(item("a"), [photo("x")])
        self.assertNotIn("poster", entry["media"][0])
        self.assertNotIn("duration", entry["media"][0])

    def test_base_url_always_ends_in_one_slash(self):
        """The layout concatenates base_url + key, so this has to be exact."""
        for given in ("https://cdn.example", "https://cdn.example/", "https://cdn.example//"):
            publish.write_data_file(self.path, given, [])
            base = yaml.safe_load(self.path.read_text())["base_url"]
            self.assertEqual(base, "https://cdn.example/")

    def test_count_matches_items(self):
        entries = [publish.entry_for(item(i), [photo(i)]) for i in ("a", "b", "c")]
        publish.write_data_file(self.path, "https://cdn.example", entries)
        data = yaml.safe_load(self.path.read_text())
        self.assertEqual(data["count"], 3)
        self.assertEqual(len(data["items"]), 3)

    def test_same_input_writes_identical_bytes(self):
        """Determinism: a re-run must not churn the committed data file."""
        entries = [publish.entry_for(item("a", caption="Café 😀"), [photo("a"), video("b")])]
        publish.write_data_file(self.path, "https://cdn.example", entries)
        first = self.path.read_bytes()
        publish.write_data_file(self.path, "https://cdn.example", entries)
        self.assertEqual(self.path.read_bytes(), first)

    def test_details_are_copied_into_the_entry(self):
        it = item("a", caption="hi")
        it.details = {"permalink": "https://www.instagram.com/p/a/", "likes": 5,
                      "location": {"name": "Somewhere", "id": "1"}}
        entry = publish.entry_for(it, [photo("x")])
        self.assertEqual(entry["permalink"], "https://www.instagram.com/p/a/")
        self.assertEqual(entry["likes"], 5)
        self.assertEqual(entry["location"], {"name": "Somewhere", "id": "1"})
        self.assertEqual(list(entry)[-1], "media")  # media stays last in the YAML

    def test_no_details_means_none_in_the_entry(self):
        entry = publish.entry_for(item("a"), [photo("x")])
        self.assertEqual(set(entry), {"id", "date", "year", "kind", "caption", "media"})

    def test_unicode_is_written_as_text_not_escapes(self):
        entries = [publish.entry_for(item("a", caption="Café 😀"), [photo("a")])]
        publish.write_data_file(self.path, "https://cdn.example", entries)
        self.assertIn("Café 😀", self.path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
