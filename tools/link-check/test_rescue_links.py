import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rescue_links as rl  # noqa: E402


class DeadTest(unittest.TestCase):
    def test_gone_and_dead_origins_only(self):
        results = [
            {"url": "a", "kind": "gone", "status": 404},
            {"url": "b", "kind": "error", "status": 530},
            {"url": "c", "kind": "error", "status": "TimeoutError"},
            {"url": "d", "kind": "blocked", "status": 403},
            {"url": "e", "kind": "ok", "status": 200},
        ]
        self.assertEqual([r["url"] for r in rl.dead(results)], ["a", "b"])


class SnapshotTest(unittest.TestCase):
    def test_200_copy_is_used_over_https(self):
        payload = {"archived_snapshots": {"closest": {
            "available": True, "status": "200",
            "url": "http://web.archive.org/web/20190101000000/http://x.test/"}}}
        self.assertEqual(rl.snapshot(payload),
                         "https://web.archive.org/web/20190101000000/http://x.test/")

    def test_no_copy_or_non_200_copy_is_none(self):
        self.assertIsNone(rl.snapshot({"archived_snapshots": {}}))
        self.assertIsNone(rl.snapshot({"archived_snapshots": {"closest": {
            "available": True, "status": "404", "url": "http://web.archive.org/x"}}}))


class CdxTest(unittest.TestCase):
    def test_first_match_after_the_header_row(self):
        rows = [["timestamp", "original"], ["20120101182339", "http://api.jquery.com:80/jquery.template/"]]
        self.assertEqual(rl.cdx_snapshot(rows),
                         "https://web.archive.org/web/20120101182339/http://api.jquery.com:80/jquery.template/")

    def test_no_match_is_none(self):
        self.assertIsNone(rl.cdx_snapshot([]))
        self.assertIsNone(rl.cdx_snapshot([["timestamp", "original"]]))


class PostDateTest(unittest.TestCase):
    def test_reads_quoted_and_minified_meta(self):
        with tempfile.TemporaryDirectory() as d:
            for name, tag in (("a", '<meta property="article:published_time" content="2018-03-04T00:00:00Z">'),
                              ("b", "<meta property=article:published_time content=2020-11-12T00:00:00-04:00>")):
                f = Path(d) / "post" / name / "index.html"
                f.parent.mkdir(parents=True)
                f.write_text(tag)
            self.assertEqual(rl.post_date(Path(d), "/post/a/"), "20180304")
            self.assertEqual(rl.post_date(Path(d), "/post/b/"), "20201112")
            self.assertEqual(rl.post_date(Path(d), "/post/missing/"), "")


class PruneTest(unittest.TestCase):
    def test_answering_urls_leave_the_map(self):
        current = {"a": None, "b": "https://web.archive.org/web/1/b", "c": None}
        statuses = {"a": 200, "b": 403, "c": 404}
        self.assertEqual(rl.prune(current, statuses), {"c": None})

    def test_network_errors_stay(self):
        self.assertEqual(rl.prune({"a": None}, {"a": "URLError"}), {"a": None})


class MergeTest(unittest.TestCase):
    def test_existing_entries_are_sticky_and_sorted(self):
        out = rl.merge({"b": None}, {"b": "https://web.archive.org/b", "a": None})
        self.assertEqual(list(out), ["a", "b"])
        self.assertIsNone(out["b"])


class DataFileTest(unittest.TestCase):
    """data/link_rewrites.json stays in the shape the template expects."""

    def test_shape(self):
        if not rl.DATA.exists():
            self.skipTest("no map yet")
        data = json.loads(rl.DATA.read_text(encoding="utf-8"))
        self.assertEqual(list(data), sorted(data))
        for url, to in data.items():
            self.assertRegex(url, r"^https?://")
            if to is not None:
                self.assertTrue(to.startswith("https://web.archive.org/web/"), to)


if __name__ == "__main__":
    unittest.main()
