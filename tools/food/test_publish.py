import importlib.util
import json
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("food_publish", Path(__file__).with_name("publish.py"))
pub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)

MANIFEST = {
    "schema": 1, "key": "2026-11-15-everything-i-eat", "date": "2026-11-15", "title": "everything i eat",
    "subtitle": "sushi, chinese and more",
    "video": {"file": "video.mp4", "sha256": "x", "width": 1080, "height": 1920, "duration": 179.03},
    "sections": [
        {"key": "sushi", "items": [{"n": 1, "title": "Otoro Nigiri", "file": "stills/001-otoro-nigiri.jpg",
                                    "uuid": "SECRET-UUID", "taken": "2024-01-02T19:00:00", "sha256": "y"}]},
        {"key": "chinese", "items": [{"n": 2, "title": "Peking Duck", "file": "stills/002-peking-duck.jpg",
                                      "uuid": "U2", "taken": "2023-05-06T12:00:00", "sha256": "z"}]},
    ],
}
NAMES = {
    "video.mp4": {"src": "food/k/video-1.mp4", "poster": "food/k/video-1-poster.webp"},
    "stills/001-otoro-nigiri.jpg": {"g": ["food/k/a-360.webp", "food/k/a-720.webp"], "s": "food/k/a-1080.webp"},
    "stills/002-peking-duck.jpg": {"g": ["food/k/b-360.webp", "food/k/b-720.webp"], "s": "food/k/b-1080.webp"},
}


class TestCollection(unittest.TestCase):
    def test_only_what_the_page_shows(self):
        col = pub.collection(MANIFEST, NAMES)
        self.assertEqual(col["video"], {"src": "food/k/video-1.mp4", "poster": "food/k/video-1-poster.webp",
                                        "w": 1080, "h": 1920, "d": 179})
        self.assertEqual([s["key"] for s in col["sections"]], ["sushi", "chinese"])
        self.assertEqual(col["sections"][0]["items"][0]["t"], "Otoro Nigiri")
        text = json.dumps(col)
        for private in ("SECRET-UUID", "2024-01-02", "taken", "sha256"):
            self.assertNotIn(private, text)

    def test_merge_replaces_same_key_and_sorts_newest_first(self):
        old = {"collections": [{"key": "2026-11-15-everything-i-eat", "date": "2026-11-15", "sections": []},
                               {"key": "2026-12-01-dumplings", "date": "2026-12-01", "sections": [{"key": "chinese", "items": [1, 2]}]}]}
        data = pub.merge(old, pub.collection(MANIFEST, NAMES))
        self.assertEqual([c["key"] for c in data["collections"]], ["2026-12-01-dumplings", "2026-11-15-everything-i-eat"])
        self.assertEqual(data["photos"], 4)
        self.assertEqual(data["base_url"], pub.BASE_URL)

    def test_merge_from_nothing(self):
        data = pub.merge(None, pub.collection(MANIFEST, NAMES))
        self.assertEqual((len(data["collections"]), data["photos"]), (1, 2))


class TestRepoData(unittest.TestCase):
    def test_data_file_shape(self):
        if not pub.DATA.exists():
            self.skipTest("no data/food.json yet")
        data = json.loads(pub.DATA.read_text())
        self.assertTrue(data["base_url"].startswith("https://"))
        total = 0
        for c in data["collections"]:
            self.assertEqual(set(c), {"key", "date", "title", "subtitle", "video", "sections"})
            self.assertTrue(c["video"]["src"].startswith(f"food/{c['key']}/"))
            for s in c["sections"]:
                for it in s["items"]:
                    self.assertEqual(set(it), {"t", "g", "s"})
                    self.assertEqual(len(it["g"]), 2)
                    total += 1
        self.assertEqual(total, data["photos"])


if __name__ == "__main__":
    unittest.main()
