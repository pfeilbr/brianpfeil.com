"""Tests for tools/ai-radar/digest.py with a fake Claude client -- no network,
no API key, and no `anthropic` package needed."""
import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import digest  # noqa: E402
import radar  # noqa: E402

NOW = dt.datetime(2026, 9, 26, 12, 0, tzinfo=dt.timezone.utc)
SCHEMA = json.loads((HERE.parent / "schema.json").read_text())


def doc():
    return {
        "schema_version": 1, "generated": radar.iso(NOW), "window_days": 14, "sections": radar.SECTIONS,
        "sources": [{"id": "hn", "section": "community", "name": "Hacker News", "home": "https://news.ycombinator.com/", "status": "ok", "checked": radar.iso(NOW)},
                    {"id": "openai", "section": "labs", "name": "OpenAI", "home": "https://openai.com/news/", "status": "ok", "checked": radar.iso(NOW)}],
        "items": [
            {"id": "a1", "source": "openai", "section": "labs", "title": "GPT-6 Luna", "url": "https://openai.com/luna",
             "published": radar.iso(NOW - dt.timedelta(hours=3)), "first_seen": radar.iso(NOW), "summary": "A model.", "also": ["hn"]},
            {"id": "b2", "source": "hn", "section": "community", "title": "Old thing", "url": "https://e.com/old",
             "published": radar.iso(NOW - dt.timedelta(days=5)), "first_seen": radar.iso(NOW - dt.timedelta(days=5)), "summary": ""},
        ],
        "models": {"new": [{"id": "acme/m1", "name": "M1", "provider": "Acme", "created": radar.iso(NOW - dt.timedelta(hours=5)),
                            "price_in": 1.0, "price_out": 2.0, "url": "https://openrouter.ai/acme/m1"}], "trending": []},
        "mine": [],
    }


def answer(refs_by_point):
    v = lambda tag: {"headline": tag + " headline", "points": [{"text": "%s point %d" % (tag, n), "refs": r} for n, r in enumerate(refs_by_point)]}
    return {lang: v(lang) for lang in digest.LANGS}


class FakeStream:
    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def get_final_message(self):
        return self.msg


class FakeClient:
    def __init__(self, payload, stop="end_turn"):
        self.kwargs = None
        msg = SimpleNamespace(stop_reason=stop, stop_details=None, model="claude-opus-5",
                              content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=json.dumps(payload))])
        self.beta = SimpleNamespace(messages=SimpleNamespace(stream=self._stream))
        self._msg = msg

    def _stream(self, **kwargs):
        self.kwargs = kwargs
        return FakeStream(self._msg)


class Digest(unittest.TestCase):
    def test_prompt_uses_only_the_last_day(self):
        prompt, items, models = digest.build_prompt(doc(), NOW)
        self.assertEqual([i["id"] for i in items], ["a1"])
        self.assertEqual(items[0]["also_in"], ["Hacker News"])
        self.assertEqual([m["id"] for m in models], ["model:acme/m1"])
        self.assertIn('"a1"', prompt)

    def test_request_shape(self):
        c = FakeClient(answer([["a1"]]))
        digest.make_digest(doc(), NOW, client=c)
        k = c.kwargs
        self.assertEqual(k["model"], "claude-opus-5")
        self.assertEqual(k["thinking"], {"type": "adaptive"})
        self.assertEqual(k["output_config"]["format"]["type"], "json_schema")
        self.assertEqual(sorted(k["output_config"]["format"]["schema"]["required"]), sorted(digest.LANGS))
        self.assertEqual((k["fallbacks"], k["betas"]), ("default", ["server-side-fallback-2026-07-01"]))

    def test_unresolved_refs_are_dropped_in_every_language(self):
        d = digest.make_digest(doc(), NOW, client=FakeClient(answer([["a1", "zzz"], ["nope"], ["model:acme/m1"]])))
        for lang in digest.LANGS:
            pts = d["lang"][lang]["points"]
            self.assertEqual([p["refs"] for p in pts], [["a1"], ["model:acme/m1"]], lang)
            self.assertEqual(pts[1]["text"], "%s point 2" % lang, "points stay aligned across languages")
        self.assertEqual(set(d["refs"]), {"a1", "model:acme/m1"})
        self.assertEqual(d["refs"]["a1"]["url"], "https://openai.com/luna")
        self.assertEqual(radar.validate(d, SCHEMA["properties"]["digest"]), [])

    def test_nothing_citable_is_an_error(self):
        with self.assertRaises(RuntimeError):
            digest.make_digest(doc(), NOW, client=FakeClient(answer([["nope"]])))

    def test_refusal_and_truncation_raise(self):
        for stop in ("refusal", "max_tokens"):
            with self.assertRaises(RuntimeError):
                digest.make_digest(doc(), NOW, client=FakeClient(answer([["a1"]]), stop=stop))

    def test_save_writes_file_and_archive(self):
        d = digest.make_digest(doc(), NOW, client=FakeClient(answer([["a1"]])))
        with tempfile.TemporaryDirectory() as tmp:
            out, arch = Path(tmp) / "ai.json", Path(tmp) / "ai-digests.json"
            full = doc()
            full["topics"] = []
            digest.save(full, d, out=out, archive=arch)
            digest.save(full, d, out=out, archive=arch)  # same day twice: one entry
            self.assertEqual(json.loads(out.read_text())["digest"]["date"], "2026-09-26")
            self.assertEqual(len(json.loads(arch.read_text())["digests"]), 1)

    def test_no_key_is_a_quiet_no_op(self):
        import os
        old = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            self.assertEqual(digest.main([]), 0)
        finally:
            if old is not None:
                os.environ["ANTHROPIC_API_KEY"] = old


if __name__ == "__main__":
    unittest.main()


class Health(unittest.TestCase):
    def test_report(self):
        import health
        ok = {"sources": [{"id": "a", "name": "A", "fail_streak": 2}]}
        self.assertEqual(health.report(ok), "")
        bad = {"sources": [{"id": "a", "name": "A", "fail_streak": 4, "error": "HTTPError: 403"},
                           {"id": "b", "name": "B"}]}
        text = health.report(bad)
        self.assertIn("**A** (`a`, 4 runs): HTTPError: 403", text)
        self.assertNotIn("**B**", text)
