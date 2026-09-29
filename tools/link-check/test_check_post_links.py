"""Tests for check_post_links.py. No network."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_post_links as c  # noqa: E402

PAGE = """<html><nav><a href="https://nav.example/">nav</a></nav>
<article><div class="prose">
<p><a href="https://a.example/x?y=1&amp;z=2">a</a> <a href=https://b.example/>b</a></p>
<pre><code><a href="https://code.example/">in code</a></code></pre>
<p><code>https://inline.example/</code> <a href="http://localhost:3000/">dev</a>
<a href="http://WP-VIP-SITE/wp-admin">placeholder</a> <a href="/post/other/">same site</a></p>
</div></article></html>"""


class LinksTest(unittest.TestCase):
    def test_article_links_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in ("post/one", "projects/two", "tags/aws"):
                (root / rel).mkdir(parents=True)
                (root / rel / "index.html").write_text(PAGE)
            found = c.links(root)
        self.assertEqual(set(found), {"https://a.example/x?y=1&z=2", "https://b.example/"})
        self.assertEqual(found["https://b.example/"], ["/post/one/", "/projects/two/"])

    def test_classify(self):
        self.assertEqual(c.classify(200), "ok")
        self.assertEqual(c.classify(403), "blocked")
        self.assertEqual(c.classify(404), "gone")
        self.assertEqual(c.classify(410), "gone")
        self.assertEqual(c.classify("URLError"), "gone")
        self.assertEqual(c.classify(503), "error")
        self.assertEqual(c.classify("TimeoutError"), "error")


if __name__ == "__main__":
    unittest.main()
