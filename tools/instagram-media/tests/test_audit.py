"""Tests for comparing the page's references with the bucket's contents."""

import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from igmedia import audit  # noqa: E402

DATA = {
    "items": [
        {"id": "v", "media": [{"kind": "video", "src": "i/v/1.mp4", "thumb": "i/v/1-t.jpg",
                               "poster": "i/v/1-p.jpg"}]},
        {"id": "a", "media": [
            {"kind": "photo", "src": "i/a/1.jpg", "thumb": "i/a/1-t.jpg"},
            {"kind": "photo", "src": "i/a/2.jpg", "thumb": "i/a/2-t.jpg"},
        ]},
    ]
}


def listing(stdout, returncode=0):
    return lambda cmd, **kw: subprocess.CompletedProcess(cmd, returncode, stdout=stdout, stderr="nope")


class ReferencedTest(unittest.TestCase):
    def test_collects_src_thumb_and_poster(self):
        self.assertEqual(audit.referenced_keys(DATA), {
            "i/v/1.mp4", "i/v/1-t.jpg", "i/v/1-p.jpg",
            "i/a/1.jpg", "i/a/1-t.jpg", "i/a/2.jpg", "i/a/2-t.jpg",
        })

    def test_grid_tiles_count_as_referenced(self):
        """They're used through srcset; missing them made the audit call every
        tile an orphan and suggest pruning files the page shows."""
        data = {"items": [{"media": [{"src": "a.jpg", "thumb": "a-t.jpg",
                                      "grid": ["a-g360.webp", "a-g720.webp"]}]}]}
        self.assertEqual(audit.referenced_keys(data),
                         {"a.jpg", "a-t.jpg", "a-g360.webp", "a-g720.webp"})

    def test_photos_have_no_poster_to_collect(self):
        keys = audit.referenced_keys({"items": [DATA["items"][1]]})
        self.assertFalse(any(k.endswith("-p.jpg") for k in keys))

    def test_empty_data(self):
        self.assertEqual(audit.referenced_keys({}), set())
        self.assertEqual(audit.referenced_keys({"items": None}), set())


class ListTest(unittest.TestCase):
    def test_keys_parsed(self):
        run = listing('["instagram/a/1.jpg", "instagram/a/1-t.jpg"]')
        self.assertEqual(audit.list_objects("b", "instagram", run=run),
                         {"instagram/a/1.jpg", "instagram/a/1-t.jpg"})

    def test_empty_prefix_comes_back_as_null(self):
        self.assertEqual(audit.list_objects("b", "instagram", run=listing("null")), set())

    def test_listing_failure_raises(self):
        with self.assertRaises(RuntimeError):
            audit.list_objects("b", "instagram", run=listing("", returncode=255))

    def test_lists_under_the_prefix_only(self):
        seen = {}

        def run(cmd, **kw):
            seen["cmd"] = cmd
            return subprocess.CompletedProcess(cmd, 0, stdout="null", stderr="")

        audit.list_objects("brianpfeil-media01", "instagram", run=run)
        self.assertEqual(seen["cmd"][seen["cmd"].index("--prefix") + 1], "instagram/")


class AuditTest(unittest.TestCase):
    def test_everything_present(self):
        refs = audit.referenced_keys(DATA)
        self.assertEqual(audit.audit(refs, set(refs)), ([], []))

    def test_a_partial_upload_shows_as_missing(self):
        refs = audit.referenced_keys(DATA)
        present = refs - {"i/a/2.jpg", "i/v/1-p.jpg"}
        missing, orphaned = audit.audit(refs, present)
        self.assertEqual(missing, ["i/a/2.jpg", "i/v/1-p.jpg"])
        self.assertEqual(orphaned, [])

    def test_unapproved_leftovers_show_as_orphaned(self):
        refs = audit.referenced_keys(DATA)
        missing, orphaned = audit.audit(refs, refs | {"i/old/1.jpg"})
        self.assertEqual((missing, orphaned), ([], ["i/old/1.jpg"]))


if __name__ == "__main__":
    unittest.main()
