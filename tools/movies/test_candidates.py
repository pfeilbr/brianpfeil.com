import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import candidates as c  # noqa: E402


def edge(title, year, imdb):
    return {"node": {"id": imdb, "content": {
        "title": title, "originalReleaseYear": year, "posterUrl": None, "runtime": 100,
        "externalIds": {"imdbId": imdb}}}}


class Norm(unittest.TestCase):
    def test_article_case_and_punctuation(self):
        self.assertEqual(c.norm("The Goonies"), c.norm("goonies"))
        self.assertEqual(c.norm("Extremely Loud & Incredibly Close"),
                         c.norm("extremely loud and incredibly close"))
        self.assertEqual(c.norm("Aquaman (2018)"), c.norm("Aquaman"))


class Pick(unittest.TestCase):
    edges = [edge("Godzilla", 1998, "tt1"), edge("Godzilla", 2014, "tt2"),
             edge("Godzilla vs. Kong", 2021, "tt3")]

    def test_year_chooses_between_namesakes(self):
        self.assertEqual(c.pick(self.edges, "Godzilla", 2014)["id"], "tt2")

    def test_without_year_takes_first_exact(self):
        self.assertEqual(c.pick(self.edges, "Godzilla", None)["id"], "tt1")

    def test_no_loose_match_without_year(self):
        self.assertIsNone(c.pick(self.edges, "Godzilla vs", None))


class Build(unittest.TestCase):
    def test_merges_and_drops_existing(self):
        hits = {"elf": {"imdb": "tt0319343", "title": "Elf", "year": 2003, "poster": None, "runtime": 97},
                "pulp fiction": {"imdb": "tt0110912", "title": "Pulp Fiction", "year": 1994,
                                 "poster": None, "runtime": 154}}
        orig = c.lookup
        c.lookup = lambda t, y, cache: hits.get(c.norm(t))
        try:
            films, unmatched = c.build(
                [{"title": "Elf", "source": "gmail", "evidence": "rental 2013", "date": "2013-12-01"},
                 {"title": "elf", "source": "drafts", "evidence": "list", "date": "2015-12-02"},
                 {"title": "Pulp Fiction", "source": "drafts", "evidence": "list"},
                 {"title": "Nope Not A Film", "source": "drafts", "evidence": "x"}],
                [{"title": "Pulp Fiction", "imdb": "tt0110912"}], {})
        finally:
            c.lookup = orig
        self.assertEqual([f["imdb"] for f in films], ["tt0319343"])
        self.assertEqual(films[0]["sources"], ["gmail", "drafts"])
        self.assertEqual((films[0]["first"], films[0]["last"]), ("2013-12-01", "2015-12-02"))
        self.assertEqual(len(unmatched), 1)


class Add(unittest.TestCase):
    def test_parse_and_append_skips_existing_and_dupes(self):
        import add
        self.assertEqual(add.parse("tt1:Synecdoche, New York:2008"),
                         {"title": "Synecdoche, New York", "imdb": "tt1", "year": 2008})
        self.assertEqual(add.parse("tt2"), {"title": "tt2", "imdb": "tt2"})
        doc = {"movies": [{"title": "Old", "imdb": "tt0"}]}
        ids = add.append(doc, [{"imdb": "tt0"}, {"imdb": "tt3"}, {"imdb": "tt3"}])
        self.assertEqual(ids, ["tt3"])
        self.assertEqual(len(doc["movies"]), 2)


if __name__ == "__main__":
    unittest.main()
