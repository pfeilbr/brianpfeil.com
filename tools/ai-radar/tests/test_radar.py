"""Unit tests for tools/ai-radar/radar.py. No network: every parser is fed a
fixture, and build() is given fake fetchers.

  python3 -m unittest discover -s tools/ai-radar/tests
"""
import datetime as dt
import io
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

    def test_feedly_stream(self):
        [e] = radar.parse_feedly(fx("feedly.json"))
        self.assertEqual((e["title"], e["url"]), ("BREAKING: a post", "https://garymarcus.substack.com/p/breaking"))
        self.assertEqual(e["published"], "2026-09-25T21:58:42Z")
        self.assertIn("streamId=feed%2Fhttps%3A%2F%2Fx.com%2Ffeed", radar.feedly_url("https://x.com/feed"))

    def test_blocked_feed_falls_back_to_feedly(self):
        def refuse(url, **kw):
            raise radar.urllib.error.HTTPError(url, 403, "Forbidden", {}, io.BytesIO())
        real_get, real_feedly = radar.http_get, radar.get_feedly
        radar.http_get, radar.get_feedly = refuse, lambda feed: fx("feedly.json")
        try:
            entries, err = radar.fetch_source({"id": "g", "feed": "https://g.substack.com/feed"}, NOW)
            self.assertIsNone(err)
            self.assertEqual(len(entries), 1)
            radar.get_feedly = refuse
            entries, err = radar.fetch_source({"id": "g", "feed": "https://g.substack.com/feed"}, NOW)
            self.assertEqual(entries, [])
            self.assertIn("403", err, "the direct error is the one reported")
        finally:
            radar.http_get, radar.get_feedly = real_get, real_feedly

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


class Improvements(unittest.TestCase):
    def test_clean_release(self):
        self.assertEqual(radar.clean_release("What's Changed Release highlights could not be determined from the supplied PR index. Fix login loop (#123) by @dev in https://x/pull/1"),
                         "Fix login loop")
        self.assertEqual(radar.clean_release("release: v2.0.18"), "")
        self.assertEqual(radar.clean_release("Bug Fixes: faster startup"), "Bug Fixes: faster startup")
        self.assertEqual(radar.clean_release("rust-v0.157.0...rust-v0.157.1"), "")
        self.assertEqual(radar.clean_release("jinja : implement sameas test ( #29448 ) done"), "jinja : implement sameas test done")
        self.assertEqual(radar.clean_release("Merge pull request #5036 from ms/branch nes: clipping"), "nes: clipping")
        self.assertEqual(radar.clean_release("Fix x Signed-off-by: A B a@b.c"), "Fix x")

    def test_prerelease_patterns(self):
        for t in ("v0.30.1rc0: [ROCm] x", "v0.43.2026040705", "v1.2.0-beta.1", "VS Code 1.140 (Insiders)"):
            self.assertTrue(radar.PRERELEASE.search(t), t)
        for t in ("v0.30.0", "v2.1.283", "Release v0.61.0", "Desktop v0.0.37", "source maps"):
            self.assertFalse(radar.PRERELEASE.search(t), t)

    def test_same_story_by_headline(self):
        self.assertTrue(radar.same_story("OpenAI releases GPT-6 Luna with 2M context window",
                                         "GPT-6 Luna: OpenAI releases model with 2M context window"))
        self.assertFalse(radar.same_story("OpenAI releases GPT-6 Luna", "Anthropic releases Claude Opus 5.5"))

    def test_crosslink_by_headline_gives_hn_thread(self):
        a = dict(item("openai", 1, 0, "labs"), title="Introducing GPT-6 Luna Pro reasoning model for developers")
        b = dict(item("hn", 7, 0, "community"), title="GPT-6 Luna Pro reasoning model for developers",
                 discuss="https://news.ycombinator.com/item?id=7", points=400, comments=120)
        radar.crosslink([a, b])
        self.assertEqual(a["also"], ["hn"])
        self.assertEqual(a["hn"], {"url": "https://news.ycombinator.com/item?id=7", "points": 400, "comments": 120})
        self.assertNotIn("hn", b)

    def test_topics(self):
        items = [dict(item("hn", n, 0, "community"), title=t) for n, t in enumerate(
            ["Claude gets agents", "Claude Code 2", "Gemini update", "Qwen open weights", "Qwen 4 open-weights model"])]
        got = {t["key"]: t["n"] for t in radar.topics(items, NOW)}
        self.assertEqual(got.get("Claude"), 2)
        self.assertEqual(got.get("Qwen"), 2)
        self.assertEqual(got.get("Open weights"), 2)
        self.assertNotIn("Gemini", got, "a single mention is not a topic")
        self.assertEqual(items[3]["topics"], ["Qwen", "Open weights"])
        self.assertEqual(items[2]["topics"], ["Gemini"], "items are tagged even below the chip threshold")

    def test_busy_source_is_capped(self):
        old = [item("awsml", n, 0.1 * n, "labs") for n in range(radar.SOURCE_KEEP + 5)]
        out = radar.merge_items(old, [], NOW, 14, set())
        self.assertEqual(len(out), radar.SOURCE_KEEP)

    def test_cap_scales_with_the_source(self):
        old = [item("hn", n, 0.05 * n, "community") for n in range(70)]
        out = radar.merge_items(old, [], NOW, 14, set(), caps={"hn": 60})
        self.assertEqual(len(out), 60)

    def test_build_caps_hn_by_its_limit(self):
        cfg = {"window_days": 14, "sources": [{"id": "hn", "section": "community", "name": "HN",
                                              "home": "https://news.ycombinator.com/", "kind": "hn", "limit": 30}], "models": {}}
        prev = {"schema_version": 1, "sources": [], "items": [item("hn", n, 0.05 * n, "community") for n in range(70)]}
        doc = radar.build(cfg, radar.migrate(prev), NOW, fetch=lambda s, n: ([], None), get=None,
                          posts_dir=FX / "posts", feedly=set(), only={"hn"})
        self.assertEqual(len(doc["items"]), 60)

    def test_gate_spaces_requests(self):
        t = [100.0]
        slept = []
        gate = radar.Gate(30, clock=lambda: t[0], sleep=lambda s: (slept.append(s), t.__setitem__(0, t[0] + s)))
        with gate:          # the request itself takes 5s
            t[0] += 5
        t[0] += 2           # 2s pass before the next one is asked for
        with gate:
            pass
        self.assertEqual(slept, [28.0], "30s from the end of the previous request")

    def test_retry_after(self):
        self.assertEqual(radar.retry_after({"Retry-After": "7"}, default=15), 7)
        self.assertEqual(radar.retry_after({"Retry-After": "600"}, default=15), 90)
        self.assertEqual(radar.retry_after({}, default=15), 15)
        self.assertEqual(radar.retry_after({"Retry-After": "Wed, 21 Oct"}, default=15), 15)


class TopAndSummaries(unittest.TestCase):
    def test_top_stories_rank_and_dedupe(self):
        a = dict(item("openai", 1, 0.1, "labs"), title="OpenAI ships GPT-6 Luna reasoning model today", also=["hn"],
                 hn={"url": "u", "points": 900, "comments": 300})
        b = dict(item("hn", 2, 0.1, "community"), title="OpenAI ships GPT-6 Luna reasoning model", url=a["url"], also=["openai"], points=900)
        c = dict(item("r-localllama", 3, 0.2, "community"), title="Small local model tricks", points=50)
        d = dict(item("awsml", 4, 0.3, "labs"), title="SageMaker thing")
        old = dict(item("hn", 5, 3, "community"), title="Old but huge", points=3000)
        tool = dict(item("codex", 6, 0.1, "tools"), title="0.158.0")
        top = radar.top_stories([c, d, b, a, old, tool], NOW)
        self.assertEqual(top[0], a["id"], "the cross-posted, discussed lab story wins")
        self.assertNotIn(b["id"], top, "its Hacker News copy is the same story")
        self.assertNotIn(old["id"], top, "older than 36 hours")
        self.assertNotIn(tool["id"], top)
        self.assertEqual(set(top[1:]), {c["id"], d["id"]})

    def test_top_stories_two_per_source(self):
        titles = ["Voice apps with vLLM-Omni", "Synthetic monitoring using Nova Act", "Grok on Bedrock",
                  "Datacor rental analytics", "Speech with Qwen3-TTS"]
        many = [dict(item("awsml", n, 0.1, "labs"), title=t) for n, t in enumerate(titles)]
        self.assertEqual(len(radar.top_stories(many, NOW)), 2)

    def test_fill_summaries_only_new_and_capped(self):
        got = []
        def get(url):
            got.append(url)
            return b'<meta name="description" content="A real description taken from the page itself.">'
        new = [dict(item("hfblog", n, 0, "labs"), summary="") for n in range(4)]
        new[0]["summary"] = "has one"
        n = radar.fill_summaries(new, {new[1]["id"]}, get, limit=1)
        self.assertEqual(n, 1)
        self.assertEqual([i["summary"] for i in new], ["has one", "", "A real description taken from the page itself.", ""],
                         "skips the one that has a summary and the one known to have one; stops at the limit")

    def test_generic_descriptions_are_ignored(self):
        new = [dict(item("hfblog", 1, 0, "labs"), summary="")]
        radar.fill_summaries(new, set(), lambda u: b'<meta name="description" content="A Blog post by Liquid AI on Hugging Face">')
        self.assertEqual(new[0]["summary"], "")

    def test_merge_keeps_an_earlier_summary(self):
        old = [dict(item("hfblog", 1, 0, "labs"), summary="From the page.")]
        new = [dict(item("hfblog", 1, 0, "labs"), summary="")]
        [out] = radar.merge_items(old, new, NOW, 14, set())
        self.assertEqual(out["summary"], "From the page.")


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

    def test_fail_streak_counts_and_resets(self):
        prev = self.run_build(radar.load_previous(FX / "missing.json"), {"werner": ([], "boom")})
        prev = self.run_build(json.loads(json.dumps(prev)), {"werner": ([], "boom")})
        self.assertEqual({s["id"]: s for s in prev["sources"]}["werner"]["fail_streak"], 2)
        doc = self.run_build(json.loads(json.dumps(prev)), {"werner": ([], None)})
        self.assertNotIn("fail_streak", {s["id"]: s for s in doc["sources"]}["werner"])

    def test_briefing_survives_a_refresh(self):
        prev = radar.load_previous(FX / "missing.json")
        prev["digest"] = {"date": "2026-09-26"}
        doc = self.run_build(prev, {})
        self.assertEqual(doc["digest"], {"date": "2026-09-26"})

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
        self.assertEqual(radar.validate({"a": 1}, {"type": "object", "additionalProperties": {"type": "string"}}),
                         ["$.a: expected string, got int"])

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
