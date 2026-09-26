import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_site as c  # noqa: E402


class SiteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def test_links(self):
        self.write("public/index.html", '<a href="/about/">a</a><a href=/gone/>g</a><img src="/img/x.png">'
                   '<a href="https://example.com/">e</a><a href="#top">t</a><a href="/about/#s">s</a>'
                   '<script>var u="/not/a/link/";</script><a href="/lesson.html">l</a>')
        self.write("public/about/index.html", "<p>about</p>")
        self.write("public/img/x.png", "png")
        self.write("public/lesson.html", "<p>l</p>")
        self.assertEqual(set(c.broken_links(self.root / "public")), {"/gone/"})

    def test_case_clash(self):
        self.write("content/a.md", '+++\ncategories = ["HTML"]\ntags = ["aws"]\n+++\n')
        self.write("content/b.md", '+++\ncategories = ["html"]\ntags = ["aws"]\n+++\n')
        self.assertEqual(c.term_case_clashes(self.root / "content"), {"categories:html": {"HTML", "html"}})


if __name__ == "__main__":
    unittest.main()
