"""Tests for check_structure.py against a tiny fixture site. No Hugo needed."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_structure as cs  # noqa: E402

NOTE = '+++\nslug = "{slug}"\ndraft = false\nrepoFullName = "pfeilbr/{repo}"\n{extra}+++\nbody\n'
PROJECT_BUILD = '[build]\n  list = "never"\n  render = "never"\n'


def nav(pre):
    links = "".join(f'<a href={pre}/{p}/ class=x>{p}</a>' for p in cs.NAV)
    return f'<div class="nav-wide items-center">{links}<button id=dark-mode-toggle>'


def home(pre):
    return (nav(pre) + '<nav class=hub-cta aria-label=x><a href=1>a</a><a href=2>b</a><a href=3>c</a></nav>'
            '<ol class="hub-latest hub-guides"></ol>')


def row(slug):
    return f'<article class="post-preview post-row py-2.5" data-href=/post/{slug}/>'


class StructureTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.content, self.data, self.public = (self.root / d for d in ("content", "data", "public"))
        (self.content / "post").mkdir(parents=True)
        (self.content / "projects" / "chess").mkdir(parents=True)
        self.data.mkdir()
        (self.content / "post" / "generated-a.md").write_text(NOTE.format(slug="a", repo="a", extra=""))
        (self.content / "post" / "generated-gone.md").write_text(NOTE.format(slug="gone", repo="gone", extra=""))
        (self.content / "post" / "generated-chess.md").write_text(
            NOTE.format(slug="chess", repo="chess", extra=PROJECT_BUILD))
        (self.content / "projects" / "chess" / "index.md").write_text(
            '+++\ntitle = "Chess"\nrepo = "pfeilbr/chess"\naliases = ["/post/chess/"]\n+++\n')
        (self.data / "repo_gone.json").write_text(json.dumps({"repos": ["pfeilbr/gone"]}))
        for lang in cs.LANGS:
            pre = "" if lang == "en" else f"/{lang}"
            self.write(cs.page(self.public, lang, ""), home(pre))
            self.write(cs.page(self.public, lang, "post"), row("article-one"))
            self.write(cs.page(self.public, lang, "notes"), row("a") + row("gone"))
        self.write(self.public / "post" / "chess" / "index.html",
                   '<meta http-equiv=refresh content="0; url=https://x/projects/chess/">')
        self.write(self.public / "post" / "gone" / "index.html", "<article><p>no link</p></article>")

    def write(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def check(self):
        return cs.check(self.public, self.content, self.data, accounts=["529276214230"])

    def test_good_site_passes(self):
        self.assertEqual(self.check(), [])

    def test_a_seventh_nav_link_fails(self):
        self.write(cs.page(self.public, "de", ""), home("/de").replace("<button", "<a href=/de/music/>m</a><button"))
        self.assertTrue(any(e.startswith("/de/ nav:") for e in self.check()))

    def test_missing_calls_to_action_fail(self):
        self.write(cs.page(self.public, "ja", ""), nav("/ja") + "hub-guides")
        self.assertIn("/ja/: home page has no three calls to action", self.check())

    def test_a_note_on_the_articles_page_fails(self):
        self.write(cs.page(self.public, "en", "post"), row("article-one") + row("a"))
        self.assertTrue(any(e.startswith("/en/post/: lists 1 that are not articles") for e in self.check()))

    def test_an_article_on_the_notes_page_fails(self):
        self.write(cs.page(self.public, "ko", "notes"), row("article-one"))
        self.assertTrue(any(e.startswith("/ko/notes/: lists 1 that are not notes") for e in self.check()))

    def test_project_post_rendered_as_a_page_fails(self):
        self.write(self.public / "post" / "chess" / "index.html", "<article>README</article>")
        self.assertIn("/post/chess/: should only redirect to /projects/chess/", self.check())

    def test_gone_repo_still_linked_fails(self):
        self.write(self.public / "post" / "gone" / "index.html", '<a href="https://github.com/pfeilbr/gone">code</a>')
        self.assertIn("/post/gone/: links pfeilbr/gone, which is gone", self.check())

    def test_contents_need_the_sidebar_class(self):
        self.write(self.public / "post" / "a" / "index.html", '<article><nav class="toc"></nav></article>')
        self.assertIn("/post/a/: contents without the has-toc article", self.check())
        self.write(self.public / "post" / "a" / "index.html", '<article class="has-toc"><nav class="toc"></nav></article>')
        self.assertEqual(self.check(), [])

    def test_own_account_anywhere_in_the_build_fails(self):
        self.write(self.public / "index.json", '[{"contents": "arn:aws:iam::529276214230:root"}]')
        self.assertIn("/index.json: shows account 529276214230", self.check())

    def test_example_account_is_fine(self):
        self.write(self.public / "post" / "a" / "index.html", "arn:aws:iam::123456789012:root")
        self.assertEqual(self.check(), [])

    def test_accounts_read_from_the_generator_config(self):
        self.assertEqual(cs.own_accounts(), ["529276214230"])

    def test_draft_notes_are_ignored(self):
        (self.content / "post" / "generated-d.md").write_text(
            NOTE.format(slug="d", repo="d", extra="").replace("draft = false", "draft = true"))
        self.assertNotIn("d", cs.notes(self.content))


if __name__ == "__main__":
    unittest.main()
