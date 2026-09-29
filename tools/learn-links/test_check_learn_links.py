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


class FetchTest(unittest.TestCase):
    def test_classify(self):
        self.assertEqual(c.classify(200), "ok")
        for code in (401, 403, 429):
            self.assertEqual(c.classify(code), "blocked")
        for status in (404, 410, 500, "URLError"):
            self.assertEqual(c.classify(status), "broken")

    def run_fetch(self, answers):
        calls = []

        def fake(url):
            calls.append(url)
            return answers[len(calls) - 1]
        orig, sleep = c.fetch_once, c.time.sleep
        c.fetch_once, c.time.sleep = fake, lambda _: None
        try:
            return c.fetch("https://a.example/"), len(calls)
        finally:
            c.fetch_once, c.time.sleep = orig, sleep

    def test_network_error_is_retried(self):
        result, calls = self.run_fetch([("URLError", "u"), (200, "https://a.example/")])
        self.assertEqual((result[0], calls), (200, 2))

    def test_network_error_twice_is_believed(self):
        result, calls = self.run_fetch([("URLError", "u"), ("TimeoutError", "u")])
        self.assertEqual((result[0], calls), ("TimeoutError", 2))

    def test_http_status_is_not_retried(self):
        result, calls = self.run_fetch([(404, "u")])
        self.assertEqual((result[0], calls), (404, 1))


class RealDataTest(unittest.TestCase):
    """The shipped data/learn.json must pass the offline checks."""

    def test_repo_data(self):
        data = json.loads(c.DATA.read_text(encoding="utf-8"))
        with c.EN.open("rb") as fh:
            en = tomllib.load(fh)
        self.assertEqual(c.check_shape(data, en), [])


if __name__ == "__main__":
    unittest.main()
