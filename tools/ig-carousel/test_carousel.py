"""Offline tests for the carousel builder (no Chrome)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import carousel as c  # noqa: E402


class Markdown(unittest.TestCase):
    def test_inline(self):
        self.assertEqual(c.inline("**a** and *b* & [x](https://e.com)"),
                         "<strong>a</strong> and <em>b</em> &amp; x")

    def test_site_link_becomes_address(self):
        self.assertEqual(c.inline("[about](/about/)"), "brianpfeil.com/about")

    def test_blocks(self):
        html = c.to_html("## T\n\npara one\ncontinued\n\n- a\n- b\n\n---\n\nend")
        self.assertEqual(html, "<h2>T</h2>\n<p>para one continued</p>\n"
                               "<ul><li>a</li><li>b</li></ul>\n<p>end</p>")


class Post(unittest.TestCase):
    def test_every_section_is_in_exactly_one_part(self):
        parts = c.series(c.post_body())
        self.assertEqual(len(parts), len(c.PARTS))
        joined = "\n".join(parts)
        for heading in c.sections(c.post_body()):
            if heading:
                self.assertEqual(joined.count(f"## {heading}\n"), 1, heading)

    def test_rewrites_leave_no_in_page_links(self):
        body = c.post_body()
        self.assertNotIn("](#", body)
        self.assertNotIn("about page", body)


class Captions(unittest.TestCase):
    def test_one_per_carousel_within_limits(self):
        caps = c.captions()
        self.assertEqual(set(caps), {"condensed"} | {f"part-{n}" for n in range(1, len(c.PARTS) + 1)})
        for key, text in caps.items():
            self.assertLessEqual(len(text), c.CAPTION_LIMIT, key)
            self.assertLessEqual(text.count("#"), 5, key)  # Instagram's hashtag cap
            self.assertIn("988", text, key)

    def test_condensed_starts_with_cover(self):
        slides = c.condensed_slides()
        self.assertTrue(slides[0].startswith("# "))
        self.assertLessEqual(len(slides), c.MAX_SLIDES)
        self.assertNotIn("father had bipolar", c.CONDENSED.read_text())


if __name__ == "__main__":
    unittest.main()
