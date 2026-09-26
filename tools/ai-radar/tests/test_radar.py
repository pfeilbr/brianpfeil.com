"""Unit tests for tools/ai-radar/radar.py. No network: every parser is fed a
fixture, and build() is given fake fetchers.

  python3 -m unittest discover -s tools/ai-radar/tests
"""
import datetime as dt
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import radar  # noqa: E402

FX = HERE / "fixtures"
NOW = dt.datetime(2026, 9, 26, 12, 0, tzinfo=dt.timezone.utc)
SCHEMA = json.loads((HERE.parent / "schema.json").read_text())


def fx(name):
    return (FX / name).read_bytes()


class Parsers(unittest.TestCase):
    def test_atom(self):
        e = radar.parse_feed(fx("atom.xml"))
        self.assertEqual(len(e), 2, "the entry without a link is dropped")
        self.assertEqual(e[0]["title"], "Trying out a new model")
        self.assertEqual(e[0]["url"], "https://simonwillison.net/2026/Sep/25/new-model/")
        self.assertEqual(radar.plain(e[0]["summary"]), "I ran it through my pelican benchmark.")
        self.assertEqual(e[1]["published"], "2026-09-01T09:00:00Z", "updated stands in for published")

    def test_rss(self):
        e = radar.parse_feed(fx("rss.xml"))
        self.assertEqual([x["title"] for x in e][:2], ["Why I let agents write my tests", "My sourdough starter"])
        self.assertEqual(radar.parse_date(e[0]["published"]), dt.datetime(2026, 9, 24, 12, tzinfo=dt.timezone.utc))

    def test_ai_filter_and_stable(self):
        src = {"filter": "ai", "stable": True}
        kept = [x["title"] for x in radar.parse_feed(fx("rss.xml")) if radar.keep_entry(src, x)]
        self.assertEqual(kept, ["Why I let agents write my tests"])

    def test_sitemap_needs_slug_and_date(self):
        e = radar.parse_sitemap(fx("sitemap.xml"), ["/news/", "/engineering/"])
        self.assertEqual([x["url"].rsplit("/", 1)[1] for x in e], ["building-agents", "claude-text-watermark"])

    def test_page_meta(self):
        t, d = radar.page_meta(b'<html><title>How Claude&#x27;s watermark works \\ Anthropic</title>'
                               b'<meta name="description" content="A short note."></html>')
        self.assertEqual((t, d), ("How Claude's watermark works", "A short note."))
        t, _ = radar.page_meta(b'<meta property="og:title" content="OG wins"><title>x | y</title>')
        self.assertEqual(t, "OG wins")

    def test_hn_keeps_ai_stories_over_threshold(self):
        e = radar.parse_hn(fx("hn.json"), 100)
        self.assertEqual([x["title"] for x in e], ["Claude gets a new model", "Ask HN: How do you use LLMs at work?"])
        self.assertEqual(e[1]["url"], "https://news.ycombinator.com/item?id=3", "text posts link to the thread")
        self.assertEqual(e[0]["discuss"], "https://news.ycombinator.com/item?id=1")

    def test_reddit_links_to_the_post_target(self):
        [e] = radar.parse_reddit(fx("reddit.xml"))
        self.assertEqual(e["url"], "https://huggingface.co/org/model-30b")
        self.assertTrue(e["discuss"].startswith("https://www.reddit.com/r/LocalLLaMA/comments/abc"))
        self.assertEqual(e["summary"], "Benchmarks inside")

    def test_openrouter(self):
        since = NOW - dt.timedelta(days=45)
        m = radar.parse_openrouter(fx("openrouter.json"), since, 10)
        self.assertEqual([x["id"] for x in m], ["acme/closed-1", "open/weights-7b"],
                         "variants, routers and old models are skipped; newest first")
        self.assertEqual((m[0]["provider"], m[0]["name"]), ("Acme", "Closed One"))
        self.assertEqual((m[0]["price_in"], m[0]["price_out"]), (3.0, 15.0), "per million tokens")
        self.assertEqual(m[0]["summary"], "A frontier model.", "markdown links flattened")
        self.assertIsNone(m[0]["open_weights"])
        self.assertEqual(m[1]["open_weights"], "open/weights-7b")

    def test_hf_skips_private(self):
        self.assertEqual([x["id"] for x in radar.parse_hf(fx("hf.json"), 10)], ["Qwen/Qwen-Image-2.1"])


class Helpers(unittest.TestCase):
    def test_canonical_ignores_tracking_and_www(self):
        self.assertEqual(radar.canonical("http://www.Example.com/a/?utm_source=x&id=2"),
                         radar.canonical("https://example.com/a?id=2"))

    def test_plain_truncates_on_a_word(self):
        s = radar.plain("<p>" + "word " * 100 + "</p>", 30)
        self.assertTrue(s.endswith("…") and len(s) <= 31, s)

    def test_parse_date_forms(self):
        want = dt.datetime(2026, 9, 25, 18, 4, tzinfo=dt.timezone.utc)
        for s in ("2026-09-25T18:04:00+00:00", "2026-09-25T18:04:00Z", "Fri, 25 Sep 2026 18:04:00 GMT", want.timestamp()):
            self.assertEqual(radar.parse_date(s), want, s)
        self.assertIsNone(radar.parse_date("not a date"))

    def test_feedly_hosts(self):
        p = FX / "feedly.yaml"
        p.write_text('groups:\n  - feeds:\n      - title: "Simon"\n        url: "https://simonwillison.net/"\n')
        try:
            self.assertEqual(radar.feedly_hosts(p), {"simonwillison.net"})
        finally:
            p.unlink()

    def test_my_posts(self):
        posts = radar.my_posts(FX / "posts")
        self.assertEqual([p["title"] for p in posts], ["Amazon Bedrock"], "untagged and draft posts are left out")
        self.assertEqual(posts[0]["url"], "/post/amazon-bedrock/")
        self.assertEqual(posts[0]["tags"], ["ai", "genai", "llm"])


def item(source, n, days_ago, section="people"):
    d = NOW - dt.timedelta(days=days_ago)
    return {"id": "%s%d" % (source, n), "source": source, "section": section, "title": "t",
            "url": "https://e.com/%s/%d" % (source, n), "published": radar.iso(d),
            "first_seen": radar.iso(d), "summary": ""}


class Merge(unittest.TestCase):
    def test_first_seen_survives_and_window_applies(self):
        old = [item("hn", 1, 1, "community"), item("hn", 2, 30, "community")]
        new = [dict(item("hn", 1, 1, "community"), first_seen=radar.iso(NOW))]
        out = radar.merge_items(old, new, NOW, 14, set())
        self.assertEqual([i["id"] for i in out], ["hn1"], "30-day-old item dropped")
        self.assertEqual(out[0]["first_seen"], old[0]["first_seen"])

    def test_a_person_keeps_their_latest_posts_past_the_window(self):
        old = [item("zvi", n, 40 + n) for n in range(5)]
        out = radar.merge_items(old, [], NOW, 14, {"zvi"})
        self.assertEqual(len(out), radar.PERSON_KEEP)
        self.assertEqual(out[0]["id"], "zvi0")

    def test_hn_points_never_go_down(self):
        old = [dict(item("hn", 1, 0, "community"), points=500, comments=90)]
        new = [dict(item("hn", 1, 0, "community"), points=120, comments=10)]
        [out] = radar.merge_items(old, new, NOW, 14, set())
        self.assertEqual((out["points"], out["comments"]), (500, 90))

    def test_crosslink(self):
        a = item("simonw", 1, 0)
        b = dict(item("hn", 9, 0, "community"), url="https://www.e.com/simonw/1/", discuss="https://news.ycombinator.com/item?id=9")
        radar.crosslink([a, b])
        self.assertEqual((a["also"], b["also"]), (["hn"], ["simonw"]))


def fake_fetch(results):
    def fetch(src, now):
        return results.get(src["id"], ([], None))
    return fetch


class Build(unittest.TestCase):
    CFG = {
        "window_days": 14,
        "sources": [
            {"id": "simonw", "section": "people", "name": "Simon", "home": "https://simonwillison.net/", "pin": True, "x": "simonw"},
            {"id": "hn", "section": "community", "name": "HN", "home": "https://news.ycombinator.com/", "kind": "hn"},
            {"id": "werner", "section": "people", "name": "Werner", "home": "https://www.allthingsdistributed.com/", "follow": True},
        ],
        "models": {"openrouter": "or", "huggingface": "hf"},
    }

    def get(self, url):
        return fx({"or": "openrouter.json", "hf": "hf.json"}[url])

    def run_build(self, prev, results, **kw):
        return radar.build(self.CFG, prev, NOW, fetch=fake_fetch(results), get=self.get,
                           posts_dir=FX / "posts", feedly={"simonwillison.net"}, **kw)

    def test_output_matches_schema(self):
        doc = self.run_build(radar.load_previous(FX / "missing.json"), {
            "simonw": (radar.parse_feed(fx("atom.xml")), None),
            "hn": (radar.parse_hn(fx("hn.json"), 100), None),
            "werner": ([], "HTTPError: 503"),
        })
        self.assertEqual(radar.validate(doc, SCHEMA), [])
        src = {s["id"]: s for s in doc["sources"]}
        self.assertEqual(src["simonw"]["via"], ["feedly"])
        self.assertEqual(src["werner"]["via"], ["x"])
        self.assertEqual(src["werner"]["status"], "error")
        self.assertEqual(len(doc["models"]["new"]), 2)
        self.assertEqual(doc["mine"][0]["title"], "Amazon Bedrock")

    def test_a_failed_source_keeps_yesterdays_items(self):
        prev = self.run_build(radar.load_previous(FX / "missing.json"),
                              {"simonw": (radar.parse_feed(fx("atom.xml")), None)})
        doc = self.run_build(json.loads(json.dumps(prev)), {"simonw": ([], "URLError: timed out")})
        self.assertEqual(len([i for i in doc["items"] if i["source"] == "simonw"]), 2)
        self.assertEqual(doc["sources"][0]["status"], "error")

    def test_only_leaves_other_sources_alone(self):
        prev = self.run_build(radar.load_previous(FX / "missing.json"), {
            "simonw": (radar.parse_feed(fx("atom.xml")), None),
            "hn": (radar.parse_hn(fx("hn.json"), 100), None)})
        doc = self.run_build(json.loads(json.dumps(prev)), {"hn": ([], None)}, only={"hn"})
        self.assertEqual({s["id"]: s["checked"] for s in doc["sources"]}["simonw"], radar.iso(NOW))
        self.assertTrue(any(i["source"] == "simonw" for i in doc["items"]))

    def test_removed_source_items_are_dropped(self):
        prev = {"schema_version": 1, "items": [item("gone", 1, 0)], "sources": []}
        doc = self.run_build(radar.migrate(prev), {})
        self.assertFalse(any(i["source"] == "gone" for i in doc["items"]))


    def test_old_items_obey_todays_filter(self):
        cfg = json.loads(json.dumps(self.CFG))
        cfg["sources"][1]["stable"] = True
        prev = {"schema_version": 1, "sources": [], "items": [
            dict(item("hn", 1, 0, "community"), title="Tool 2.0 (Insiders)"),
            dict(item("hn", 2, 0, "community"), title="Tool 2.0")]}
        doc = radar.build(cfg, radar.migrate(prev), NOW, fetch=fake_fetch({}), get=self.get,
                          posts_dir=FX / "posts", feedly=set())
        self.assertEqual([i["title"] for i in doc["items"] if i["source"] == "hn"], ["Tool 2.0"])


class Schema(unittest.TestCase):
    def test_v0_migrates_to_current(self):
        v0 = {"items": [{"id": "a", "source": "hn", "title": "t", "url": "u", "published": "2026-09-25T00:00:00Z", "summary": ""}]}
        doc = radar.migrate(v0)
        self.assertEqual(doc["schema_version"], radar.SCHEMA_VERSION)
        self.assertEqual(doc["items"][0]["first_seen"], "2026-09-25T00:00:00Z")

    def test_every_version_has_a_migration(self):
        self.assertEqual(sorted(radar.MIGRATIONS), list(range(radar.SCHEMA_VERSION)))

    def test_schema_version_matches_the_tool(self):
        self.assertEqual(SCHEMA["properties"]["schema_version"]["enum"], [radar.SCHEMA_VERSION])

    def test_newer_file_is_refused(self):
        with self.assertRaises(SystemExit):
            radar.migrate({"schema_version": radar.SCHEMA_VERSION + 1})

    def test_validator_catches_problems(self):
        errs = radar.validate({"schema_version": 1, "extra": 1}, SCHEMA)
        self.assertTrue(any("missing generated" in e for e in errs))
        self.assertTrue(any("unexpected field extra" in e for e in errs))
        self.assertEqual(radar.validate(True, {"type": "integer"}), ["$: expected integer, got bool"])

    def test_committed_data_file_is_valid(self):
        p = radar.OUT
        if not p.exists():
            self.skipTest("data/ai.json not generated yet")
        doc = json.loads(p.read_text())
        self.assertEqual(radar.validate(doc, SCHEMA), [])

    def test_config_sources_are_well_formed(self):
        cfg = json.loads(radar.CONFIG.read_text())
        ids = [s["id"] for s in cfg["sources"]]
        self.assertEqual(len(ids), len(set(ids)), "duplicate source id")
        for s in cfg["sources"]:
            self.assertIn(s["section"], radar.SECTIONS, s["id"])
            self.assertTrue(s["home"].startswith("https://"), s["id"])
            self.assertIn(s.get("kind", "rss"), ("rss", "sitemap", "hn", "reddit"), s["id"])
            if s.get("kind") != "hn":
                self.assertTrue(s["feed"].startswith("https://"), s["id"])
            if s.get("filter"):
                self.assertIn(s["filter"], radar.FILTERS, s["id"])


if __name__ == "__main__":
    unittest.main()
