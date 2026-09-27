"""Tests for tools/social/kit.py against the real repo content -- no network."""
import datetime as dt
import sys
import tempfile
import unittest
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import kit  # noqa: E402

START = dt.date(2026, 10, 5)  # a Monday


class Kit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = kit.build(START)

    def test_people_path_comes_first_with_handles(self):
        first = self.items[0]
        self.assertEqual(first["id"], "learn:people")
        for h in ("@simonw", "@lexfridman", "@hubermanlab", "@addyosmani", "@mitchellh", "@levelsio"):
            self.assertIn(h, first["posts"]["x"])
        # @handles are X-only
        self.assertNotIn("@simonw", first["posts"]["linkedin"])

    def test_every_post_fits_its_channel(self):
        for it in self.items:
            p = it["posts"]
            self.assertLessEqual(kit.x_len(p["x"]), kit.X_MAX, it["id"])
            self.assertLessEqual(len(p["bluesky"]), kit.BSKY_MAX, it["id"])
            self.assertLessEqual(len(p["threads"]), kit.THREADS_MAX, it["id"])
            self.assertLessEqual(len(p["mastodon"]), kit.MASTODON_MAX, it["id"])

    def test_links_are_tagged_per_channel(self):
        for it in self.items:
            for ch in ("x", "bluesky", "threads", "mastodon", "facebook"):
                self.assertIn(f"utm_source={ch}", it["posts"][ch], (it["id"], ch))
            self.assertNotIn("://", it["posts"]["linkedin"])  # link goes in the first comment

    def test_fragment_stays_after_the_query(self):
        u = kit.link({"path": "/learn/#ai", "kind": "learn"}, "x")
        parts = urllib.parse.urlsplit(u)
        self.assertEqual((parts.path, parts.fragment), ("/learn/", "ai"))
        self.assertIn("utm_campaign=learn", parts.query)

    def test_intent_links_carry_the_post(self):
        it = self.items[0]
        q = urllib.parse.parse_qs(urllib.parse.urlsplit(it["intents"]["x"]).query)
        self.assertEqual(q["text"][0], it["posts"]["x"])

    def test_calendar_is_weekdays_only_and_unique(self):
        dates = [dt.date.fromisoformat(i["date"]) for i in self.items]
        self.assertEqual(dates[0], START)
        self.assertTrue(all(d.weekday() < 5 for d in dates))
        self.assertEqual(len(dates), len(set(dates)))

    def test_every_learn_path_guide_and_course_is_in(self):
        kinds = {k: sum(1 for i in self.items if i["kind"] == k) for k in ("learn", "guide", "course")}
        self.assertGreaterEqual(kinds["learn"], 8)
        self.assertGreaterEqual(kinds["guide"], 6)
        self.assertGreaterEqual(kinds["course"], 1)

    def test_fit_truncates_a_single_long_part(self):
        out = kit.fit(["y" * 400], "https://e.com", 100)
        self.assertLessEqual(len(out), 100)
        self.assertTrue(out.endswith("https://e.com"))

    def test_writes_html_and_json(self):
        with tempfile.TemporaryDirectory() as d:
            kit.main(["--start", START.isoformat(), "--out", d])
            html = (Path(d) / "kit.html").read_text()
            self.assertIn("x.com/intent/post", html)
            self.assertTrue((Path(d) / "kit.json").exists())


if __name__ == "__main__":
    unittest.main()
