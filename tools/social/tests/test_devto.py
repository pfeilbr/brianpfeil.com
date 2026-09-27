"""Tests for tools/social/devto.py -- real guides, fake dev.to, no network."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import devto  # noqa: E402

PAGE = b'<meta property=og:image content=https://brianpfeil.com/og/card.jpg>'
URL = "https://brianpfeil.com/architecture/compute-ladder/"


class FakeDevto:
    def __init__(self, mine=(), fail_post=False):
        self.mine = list(mine)
        self.calls = []
        self.fail_post = fail_post
        self.next_id = 100

    def __call__(self, method, url, headers=None, data=None, timeout=30):
        self.calls.append((method, url, headers or {}, json.loads(data) if data else None))
        if url.startswith("https://brianpfeil.com/"):
            return 200, {}, PAGE
        if "/articles/me/all" in url:
            return 200, {}, json.dumps(self.mine if url.endswith("page=1") else []).encode()
        if method == "POST" and url.endswith("/articles"):
            if self.fail_post:
                return 422, {}, b'{"error":"bad"}'
            self.next_id += 1
            return 201, {}, json.dumps({"id": self.next_id, "url": f"https://dev.to/b/x-{self.next_id}"}).encode()
        if method == "PUT":
            aid = int(url.rsplit("/", 1)[-1])
            return 200, {}, json.dumps({"id": aid, "url": f"https://dev.to/b/x-{aid}"}).encode()
        raise AssertionError(url)

    def writes(self):
        return [c for c in self.calls if c[0] in ("POST", "PUT")]


class Convert(unittest.TestCase):
    def test_hugo_markup_is_gone(self):
        for path, fm, body, slug in devto.guides():
            md = devto.convert(body, devto.canonical(fm, path))
            self.assertNotIn("{{<", md, slug)
            self.assertNotIn("<svg", md, slug)
            self.assertNotIn("](/", md, slug)
            self.assertNotRegex(md, r"\{#[\w-]+\}", slug)
            self.assertNotIn("- [ ]", md, slug)
            self.assertIn("Originally published at [brianpfeil.com]", md)

    def test_callout_becomes_a_blockquote_on_every_line(self):
        md = devto.convert('{{< callout "warn" >}}\nFirst line\nsecond line.\n{{< /callout >}}', URL)
        self.assertTrue(md.startswith("> **Watch out:** First line\n> second line."))

    def test_diagram_keeps_its_description_and_links_back(self):
        md = devto.convert('{{< diagram >}}\n<svg aria-label="A ladder.">x</svg>\n{{< /diagram >}}', URL)
        self.assertIn("Diagram — A ladder.", md)
        self.assertIn("utm_source=devto", md)

    def test_tags_are_four_and_alphanumeric(self):
        self.assertEqual(devto.tags({"tags": ["event-driven", "AWS", "aws", "a b", "x", "y"]}),
                         ["eventdriven", "aws", "ab", "x"])


class Push(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.ledger, self.out, self.log = d / "devto.json", d / "out", []

    def tearDown(self):
        self.tmp.cleanup()

    def go(self, net, **kw):
        return devto.run(push=True, env={"DEVTO_API_KEY": "k"}, send=net, ledger_path=self.ledger,
                         out=self.out, log=self.log.append, pause=0, **kw)

    def test_creates_drafts_with_canonical_cover_and_series(self):
        net = FakeDevto()
        self.assertEqual(self.go(net, only=["compute-ladder"]), 0)
        method, url, headers, body = net.writes()[0]
        a = body["article"]
        self.assertEqual((method, headers["api-key"]), ("POST", "k"))
        self.assertIs(a["published"], False)
        self.assertEqual(a["canonical_url"], URL)
        self.assertEqual(a["main_image"], "https://brianpfeil.com/og/card.jpg")
        self.assertEqual(a["series"], devto.SERIES)
        self.assertEqual(json.loads(self.ledger.read_text())["compute-ladder"]["id"], 101)

    def test_second_run_updates_instead_of_duplicating(self):
        self.go(FakeDevto(), only=["compute-ladder"])
        net = FakeDevto()
        self.go(net, only=["compute-ladder"])
        self.assertEqual([(c[0], c[1].rsplit("/", 1)[-1]) for c in net.writes()], [("PUT", "101")])

    def test_finds_an_existing_draft_by_canonical_url_without_a_ledger(self):
        net = FakeDevto(mine=[{"id": 7, "canonical_url": URL.rstrip("/"), "published": False, "url": "u"}])
        self.go(net, only=["compute-ladder"])
        self.assertEqual([(c[0], c[1].rsplit("/", 1)[-1]) for c in net.writes()], [("PUT", "7")])

    def test_published_articles_are_left_alone(self):
        net = FakeDevto(mine=[{"id": 7, "canonical_url": URL, "published": True, "url": "u"}])
        self.go(net, only=["compute-ladder"])
        self.assertEqual(net.writes(), [])

    def test_update_published_never_unpublishes(self):
        net = FakeDevto(mine=[{"id": 7, "canonical_url": URL, "published": True, "url": "u"}])
        self.go(net, only=["compute-ladder"], update_published=True)
        self.assertNotIn("published", net.writes()[0][3]["article"])

    def test_no_key_refuses_to_push(self):
        net = FakeDevto()
        rc = devto.run(push=True, env={}, send=net, ledger_path=self.ledger, out=self.out, log=self.log.append)
        self.assertEqual((rc, net.calls), (1, []))

    def test_api_error_is_reported_and_not_recorded(self):
        net = FakeDevto(fail_post=True)
        self.assertEqual(self.go(net, only=["compute-ladder"]), 1)
        self.assertFalse(self.ledger.exists() and "compute-ladder" in json.loads(self.ledger.read_text()))

    def test_all_six_guides_go_up(self):
        net = FakeDevto()
        self.go(net)
        self.assertGreaterEqual(len(net.writes()), 6)


if __name__ == "__main__":
    unittest.main()
