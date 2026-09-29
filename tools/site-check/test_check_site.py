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

    def test_relative_links(self):
        # A translated bundle page pointing at images/ next to itself, where
        # Hugo never published them, is broken; the English copy is fine.
        self.write("public/projects/app/index.html", '<img src="images/a.png"><a href="../">up</a>')
        self.write("public/projects/app/images/a.png", "png")
        self.write("public/projects/index.html", "<p>list</p>")
        self.write("public/ja/projects/app/index.html",
                   '<img src="images/a.png"><a href="mailto:x@y.z">m</a><a href="?q=1">q</a>'
                   '<a href="C&#43;&#43;/">c</a><pre>href="nope/"</pre><code>src=gone.png</code>')
        self.write("public/ja/projects/app/C++/index.html", "<p>c</p>")
        self.assertEqual(set(c.broken_links(self.root / "public")), {"/ja/projects/app/images/a.png"})

    def test_dead_hosts(self):
        self.write("public/a/index.html", '<img src="http://static-content-01.s3-website-us-east-1.amazonaws.com/x.png">'
                   '<pre># http://note.io/abc</pre><a href="https://example.com/">ok</a>')
        self.assertEqual(set(c.dead_hosts(self.root / "public")), {"static-content-01.s3-website-us-east-1.amazonaws.com"})

    def test_case_clash(self):
        self.write("content/a.md", '+++\ncategories = ["HTML"]\ntags = ["aws"]\n+++\n')
        self.write("content/b.md", '+++\ncategories = ["html"]\ntags = ["aws"]\n+++\n')
        self.assertEqual(c.term_case_clashes(self.root / "content"), {"categories:html": {"HTML", "html"}})


if __name__ == "__main__":
    unittest.main()
