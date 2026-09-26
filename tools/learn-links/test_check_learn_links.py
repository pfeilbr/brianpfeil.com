import json
import sys
import tomllib
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_learn_links as c  # noqa: E402


def strings(*keys):
    return {k: {"other": "x"} for k in keys}


PATH_KEYS = ("learn_path_p", "learn_path_blurb_p")


class ShapeTest(unittest.TestCase):
    def data(self, *items):
        return {"paths": [{"key": "p", "icon": "i-cloud", "items": list(items)}]}

    def test_good_url_item(self):
        d = self.data({"key": "a", "name": "A", "url": "https://a.example/"})
        self.assertEqual(c.check_shape(d, strings(*PATH_KEYS, "learn_res_a")), [])

    def test_missing_blurb(self):
        d = self.data({"key": "a", "name": "A", "url": "https://a.example/"})
        self.assertIn("a: no i18n key learn_res_a", c.check_shape(d, strings(*PATH_KEYS)))

    def test_missing_path_strings(self):
        d = self.data()
        self.assertEqual(len(c.check_shape(d, strings())), 2)

    def test_duplicate_key(self):
        item = {"key": "a", "name": "A", "url": "https://a.example/"}
        errs = c.check_shape(self.data(item, item), strings(*PATH_KEYS, "learn_res_a"))
        self.assertIn("a: duplicate key", errs)

    def test_url_and_page_are_exclusive(self):
        d = self.data({"key": "a", "name": "A", "url": "https://a.example/", "page": "/projects/animal-fun"})
        self.assertIn("a: needs exactly one of url or page", c.check_shape(d, strings(*PATH_KEYS, "learn_res_a")))

    def test_page_must_exist(self):
        d = self.data({"key": "a", "page": "/projects/does-not-exist"})
        self.assertIn("a: no page at content/projects/does-not-exist", c.check_shape(d, strings(*PATH_KEYS)))

    def test_unknown_group(self):
        d = self.data({"key": "a", "name": "A", "url": "https://a.example/", "group": "nope"})
        self.assertIn("a: unknown group nope", c.check_shape(d, strings(*PATH_KEYS, "learn_res_a")))


class RealDataTest(unittest.TestCase):
    """The shipped data/learn.json must pass the offline checks."""

    def test_repo_data(self):
        data = json.loads(c.DATA.read_text(encoding="utf-8"))
        with c.EN.open("rb") as fh:
            en = tomllib.load(fh)
        self.assertEqual(c.check_shape(data, en), [])


if __name__ == "__main__":
    unittest.main()
