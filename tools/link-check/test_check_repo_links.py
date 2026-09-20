"""Tests for check_repo_links.py. No network: fetching is injected."""

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_repo_links as crl  # noqa: E402

POST = '''+++
author = "Brian Pfeil"
title = "{title}"
repoFullName = "pfeilbr/{name}"
repoHTMLURL = "https://github.com/pfeilbr/{name}"
+++
body
'''


class RepoLinksTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def write(self, filename, text):
        (self.dir / filename).write_text(text, encoding="utf-8")

    def test_reads_url_and_title_from_front_matter(self):
        self.write("generated-alpha.md", POST.format(title="Alpha", name="alpha"))
        links = crl.repo_links(self.dir)
        self.assertEqual(links, [{
            "file": "generated-alpha.md", "title": "Alpha",
            "url": "https://github.com/pfeilbr/alpha",
        }])

    def test_only_generated_posts_are_considered(self):
        self.write("generated-alpha.md", POST.format(title="Alpha", name="alpha"))
        self.write("hand-written.md", POST.format(title="Manual", name="manual"))
        self.assertEqual([l["file"] for l in crl.repo_links(self.dir)], ["generated-alpha.md"])

    def test_posts_without_a_repo_url_are_skipped(self):
        self.write("generated-norepo.md", '+++\ntitle = "No repo"\n+++\n')
        self.assertEqual(crl.repo_links(self.dir), [])

    def test_titles_with_escaped_quotes(self):
        self.write("generated-q.md", POST.format(title='Say \\"hi\\"', name="q"))
        self.assertEqual(crl.repo_links(self.dir)[0]["title"], 'Say \\"hi\\"')

    def test_sorted_by_file_name(self):
        for name in ("zeta", "alpha", "mu"):
            self.write(f"generated-{name}.md", POST.format(title=name, name=name))
        self.assertEqual([l["file"] for l in crl.repo_links(self.dir)],
                         ["generated-alpha.md", "generated-mu.md", "generated-zeta.md"])


class CheckTest(unittest.TestCase):
    LINKS = [
        {"file": "a.md", "title": "A", "url": "https://github.com/pfeilbr/public"},
        {"file": "b.md", "title": "B", "url": "https://github.com/pfeilbr/private"},
        {"file": "c.md", "title": "C", "url": "https://github.com/pfeilbr/unreachable"},
    ]
    STATUSES = {
        "https://github.com/pfeilbr/public": 200,
        "https://github.com/pfeilbr/private": 404,
        "https://github.com/pfeilbr/unreachable": 0,
    }

    def test_statuses_attach_in_order(self):
        results = crl.check(self.LINKS, fetch=self.STATUSES.get)
        self.assertEqual([r["status"] for r in results], [200, 404, 0])

    def test_anything_but_200_is_broken(self):
        results = crl.check(self.LINKS, fetch=self.STATUSES.get)
        self.assertEqual([r["file"] for r in crl.broken(results)], ["b.md", "c.md"])

    def test_all_public_means_nothing_broken(self):
        results = crl.check(self.LINKS[:1], fetch=self.STATUSES.get)
        self.assertEqual(crl.broken(results), [])


if __name__ == "__main__":
    unittest.main()
