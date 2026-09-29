import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_payload as c  # noqa: E402

FULL = {"region": "US", "updated": "2026-09-25", "movies": [
    {"imdb": "tt1", "year": 1994, "offers": [{"type": "stream"}],
     "titles": {"en": "A", "ja": "エー", "fr": "Le A"},
     "synopsis": {"en": "a", "ja": "あ", "fr": "à"}}]}


def slim(**changes):
    movie = {"imdb": "tt1", "year": 1994, "offers": [{"type": "stream"}],
             "titles": {"en": "A", "ja": "エー"}, "synopsis": {"en": "a", "ja": "あ"}}
    movie.update(changes)
    return {"region": "US", "updated": "2026-09-25", "movies": [movie]}


class CheckTest(unittest.TestCase):
    def test_cut_file_passes(self):
        self.assertEqual(c.check(FULL, slim(), "ja"), [])

    def test_english_file_keeps_only_english(self):
        en = slim(titles={"en": "A"}, synopsis={"en": "a"})
        self.assertEqual(c.check(FULL, en, "en"), [])

    def test_uncut_map_fails(self):
        errs = c.check(FULL, slim(synopsis=FULL["movies"][0]["synopsis"]), "ja")
        self.assertIn("ja tt1: synopsis is not cut to ['en', 'ja']", errs)

    def test_changed_field_fails(self):
        self.assertIn("ja tt1: year differs", c.check(FULL, slim(year=1995), "ja"))

    def test_missing_movie_fails(self):
        self.assertEqual(len(c.check(FULL, {"movies": []}, "ja")), 1)

    def test_fetch_pattern_survives_minifying(self):
        self.assertTrue(c.FETCH.search('fetch("/data/movies." + LANG + ".json")'))
        self.assertTrue(c.FETCH.search('fetch("/data/movies."+r+".json")'))
        self.assertFalse(c.FETCH.search('fetch("/data/movies.json")'))


if __name__ == "__main__":
    unittest.main()
