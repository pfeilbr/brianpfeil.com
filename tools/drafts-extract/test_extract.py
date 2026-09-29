import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import extract  # noqa: E402

DRAFTS = [
    {"content": "Grocery list", "created_at": "2024-01-01T00:00:00Z", "tags": []},
    {"content": "Up at 4am, gym twice", "created_at": "2023-05-01T00:00:00Z", "tags": ["Mood"]},
    {"content": "Vraylar to 3mg", "created_at": "2023-02-28T00:00:00Z", "tags": []},
    {"content": "old bipolar note", "created_at": "2022-01-01T00:00:00Z", "is_trashed": True},
]


class ExtractTest(unittest.TestCase):
    def test_keeps_matches_oldest_first_and_skips_trash(self):
        n, md = extract.extract(DRAFTS, extract.DEFAULT_KEYWORDS)
        self.assertEqual(n, 2)
        self.assertLess(md.index("Vraylar"), md.index("gym twice"))
        self.assertNotIn("Grocery", md)
        self.assertNotIn("old bipolar", md)

    def test_tag_match_and_heading(self):
        _, md = extract.extract(DRAFTS, ["mood"])
        self.assertIn("## 2023-05-01  (Mood)", md)


if __name__ == "__main__":
    unittest.main()
