import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import sync_courses as s  # noqa: E402

CFG = s.load_config()

LESSON = """<!DOCTYPE html><html><head><title>Lesson 2 · Cookies <code>Done</code> Right</title></head>
<body>
<a href="../RESOURCES.md">resources</a>
<a href="../MISSION.md">mission</a>
<a href="../../../index.html">all courses</a>
<a href="0001-intro.html">prev</a>
<a href="../reference/glossary.html#jwt">glossary</a>
<a href="../learning-records/0001.md">record</a>
<a href="https://example.org/x">out</a>
<a href="#top">top</a>
<p>For Brian's spare time: signing identity Apple Development: Brian Pfeil (ABCDE12345)</p>
<p>{"email":"brian@example.com","name":"Brian"}</p>
</body></html>"""


def make_course(root: Path, slug="auth", lesson=LESSON, resources=None):
    d = root / slug
    (d / "lessons").mkdir(parents=True)
    (d / "reference").mkdir()
    (d / "learning-records").mkdir()
    (d / "course.json").write_text(json.dumps({
        "title": "Web Auth", "category": "AI & ML", "tags": "a, b",
        "description": "Sessions and tokens."}))
    (d / "lessons" / "0001-intro.html").write_text("<title>Lesson 1 · Intro</title>")
    (d / "lessons" / "0002-cookies.html").write_text(lesson)
    (d / "reference" / "glossary.html").write_text("<title>Glossary</title>")
    (d / "MISSION.md").write_text("Brian wants to learn auth.")
    (d / "learning-records" / "0001.md").write_text("Brian covered sessions.")
    if resources is not None:
        (d / "RESOURCES.md").write_text(resources)
    return d


class BuildTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def build(self, **kw):
        return s.build_course(make_course(self.root, **kw), CFG)

    def test_only_lessons_and_reference_are_published(self):
        _, files = self.build()
        self.assertEqual(sorted(files), ["lessons/0001-intro.html", "lessons/0002-cookies.html", "reference/glossary.html"])

    def test_links_to_unpublished_files_point_at_the_course_page(self):
        _, files = self.build()
        page = files["lessons/0002-cookies.html"]
        self.assertIn('href="/courses/auth/#resources"', page)
        self.assertIn('href="/courses/auth/">mission', page)
        self.assertIn('href="/courses/">all courses', page)
        self.assertIn('href="/courses/auth/">record', page)
        # Published neighbours, external links and fragments are untouched.
        self.assertIn('href="0001-intro.html"', page)
        self.assertIn('href="../reference/glossary.html#jwt"', page)
        self.assertIn('href="https://example.org/x"', page)
        self.assertIn('href="#top"', page)

    def test_site_bar_links_back(self):
        _, files = self.build(lesson="<html><head><style>/* <body> */</style></head><body class=x><p>hi</p></body></html>")
        page = files["lessons/0002-cookies.html"]
        self.assertIn('<body class=x><nav data-site-bar', page)
        self.assertEqual(page.count("data-site-bar"), 1)
        self.assertIn('href="/courses/auth/"', page)
        self.assertIn("&larr; Web Auth", page)

    def test_lessons_get_canonical_and_description(self):
        _, files = self.build(lesson="<html><head><title>Lesson 2 · Cookies</title></head><body></body></html>")
        page = files["lessons/0002-cookies.html"]
        self.assertIn('<link rel="canonical" href="https://brianpfeil.com/courses/auth/lessons/0002-cookies.html">', page)
        self.assertIn('<meta name="description" content="Cookies — lesson 2 of 2 in the free Web Auth course. Sessions and tokens.">', page)
        self.assertLess(page.index("canonical"), page.index("</head>"))
        self.assertIn('<meta property="og:title" content="Cookies · Web Auth">', page)
        self.assertIn('<meta property="og:url" content="https://brianpfeil.com/courses/auth/lessons/0002-cookies.html">', page)

    def test_existing_description_is_kept(self):
        _, files = self.build(lesson='<html><head><meta name="description" content="Mine"></head><body></body></html>')
        self.assertEqual(files["lessons/0002-cookies.html"].count('name="description"'), 1)

    def test_sitemap_lists_every_page(self):
        entry, _ = self.build()
        xml = s.sitemap([entry], "https://brianpfeil.com")
        self.assertIn("<loc>https://brianpfeil.com/courses/auth/lessons/0001-intro.html</loc>", xml)
        self.assertIn("<loc>https://brianpfeil.com/courses/auth/reference/glossary.html</loc>", xml)

    def test_personal_details_are_redacted(self):
        _, files = self.build()
        page = files["lessons/0002-cookies.html"]
        self.assertNotIn("Brian", page)
        self.assertIn("For your spare time", page)
        self.assertIn("Your Name (TEAMID1234)", page)
        self.assertIn("alex@example.com", page)

    def test_site_url_is_allowed_but_nothing_else(self):
        self.assertEqual(s.deny_hits('href="https://brianpfeil.com/x"', CFG["deny"], (CFG["site"],)), [])
        self.assertNotEqual(s.deny_hits('https://brianpfeil.com/ and Brian', CFG["deny"], (CFG["site"],)), [])

    def test_deny_hit_stops_the_course(self):
        with self.assertRaises(s.PrivacyError):
            self.build(lesson="<title>x</title><p>see /Users/someone/notes</p>")

    def test_entry_shape(self):
        entry, _ = self.build()
        self.assertEqual(entry["category"], "ai_ml")
        self.assertEqual(entry["tags"], ["a", "b"])
        self.assertEqual([l["title"] for l in entry["lessons"]], ["Intro", "Cookies Done Right"])
        self.assertEqual(entry["lessons"][0]["href"], "/courses/auth/lessons/0001-intro.html")
        self.assertEqual(entry["reference"][0]["title"], "Glossary")


class ResourcesTest(unittest.TestCase):
    def test_markdown_links_with_note_below(self):
        md = "## Knowledge\n\n- [OAuth](https://oauth.net/2/) · [RFC](https://rfc.example/)\n  Use for: `grant types`.\n"
        r = s.parse_resources(md)
        self.assertEqual(r[0]["section"], "Knowledge")
        item = r[0]["items"][0]
        self.assertEqual([l["url"] for l in item["links"]], ["https://oauth.net/2/", "https://rfc.example/"])
        self.assertEqual(item["note"], "Use for: grant types.")

    def test_bold_title_bare_url_and_sub_bullets(self):
        md = ("## Canonical\n- **mlx-lm repo** — https://github.com/ml-explore/mlx-lm — the source of truth.\n"
              "  - LoRA guide: https://github.com/x/LORA.md\n  - plain note line\n")
        item = s.parse_resources(md)[0]["items"][0]
        self.assertEqual(item["links"][0], {"title": "mlx-lm repo", "url": "https://github.com/ml-explore/mlx-lm"})
        self.assertEqual(item["links"][1], {"title": "LoRA guide", "url": "https://github.com/x/LORA.md"})
        self.assertEqual(item["note"], "the source of truth. plain note line")

    def test_sections_without_links_are_dropped(self):
        self.assertEqual(s.parse_resources("## Notes\nJust prose.\n"), [])


class CategoryKeyTest(unittest.TestCase):
    def test_keys(self):
        self.assertEqual(s.category_key("DevOps & Infra"), "devops_infra")
        self.assertEqual(s.category_key(""), "other")


class RealDataTest(unittest.TestCase):
    """What is committed must be what the sync would write, and pass the gate."""

    def test_published_pages_pass_the_deny_list(self):
        for page in s.STATIC.rglob("*.html"):
            self.assertEqual(s.deny_hits(page.read_text(encoding="utf-8"), CFG["deny"], (CFG["site"],)), [], page)

    def test_relative_links_resolve(self):
        """Every same-site link in a published page lands on something."""
        from posixpath import normpath
        for page in s.STATIC.rglob("*.html"):
            rel = "/" + page.relative_to(s.REPO / "static").as_posix()
            for url in re.findall(r'(?:href|src)="([^"#]+)', page.read_text(encoding="utf-8")):
                if re.match(r"^(?:[a-z][a-z0-9+.-]*:|\{)", url, re.I):
                    continue
                target = url if url.startswith("/") else normpath(rel.rsplit("/", 1)[0] + "/" + url)
                if target in ("/", "/courses/") or re.fullmatch(r"/courses/[^/]+/", target):
                    continue
                self.assertTrue((s.REPO / "static" / target.lstrip("/")).exists(), f"{rel}: {url}")

    def test_every_listed_page_exists(self):
        data = json.loads(s.DATA.read_text(encoding="utf-8"))
        for c in data["courses"]:
            for entry in c["lessons"] + c["reference"]:
                self.assertTrue((s.REPO / "static" / entry["href"].lstrip("/")).exists(), entry["href"])
            self.assertTrue((s.CONTENT / c["slug"] / "index.md").exists(), c["slug"])


if __name__ == "__main__":
    unittest.main()
