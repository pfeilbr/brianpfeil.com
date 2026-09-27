"""Tests for tools/social/post.py with a fake HTTP layer -- no network."""
import datetime as dt
import json
import sys
import tempfile
import unittest
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import post  # noqa: E402

NOW = dt.datetime(2026, 10, 5, 14, 30, tzinfo=dt.timezone.utc)
PAGE = (b'<html><head><meta property=og:title content="Learn | Brian Pfeil">'
        b'<meta property=og:description content="Free courses &amp; docs.">'
        b'<meta property=og:image content=https://brianpfeil.com/og/abc.jpg></head></html>')
ENV = {"BLUESKY_HANDLE": "b.bsky.social", "BLUESKY_APP_PASSWORD": "app-pw",
       "MASTODON_INSTANCE": "hachyderm.io", "MASTODON_TOKEN": "tok"}


class FakeNet:
    def __init__(self, page_status=200, mastodon_status=200):
        self.calls = []
        self.page_status, self.mastodon_status = page_status, mastodon_status

    def __call__(self, method, url, headers=None, data=None, timeout=30):
        self.calls.append((method, url, headers or {}, data))
        if url.startswith("https://brianpfeil.com/og/"):
            return 200, {"Content-Type": "image/jpeg"}, b"\xff\xd8jpeg"
        if url.startswith("https://brianpfeil.com/"):
            return self.page_status, {}, PAGE
        if url.endswith("createSession"):
            return 200, {}, json.dumps({"accessJwt": "jwt", "did": "did:plc:x", "handle": "b.bsky.social"}).encode()
        if url.endswith("uploadBlob"):
            return 200, {}, json.dumps({"blob": {"$type": "blob", "ref": {"$link": "bafy"}, "mimeType": "image/jpeg", "size": 6}}).encode()
        if url.endswith("createRecord"):
            return 200, {}, json.dumps({"uri": "at://did:plc:x/app.bsky.feed.post/3kabc", "cid": "c"}).encode()
        if url.endswith("/api/v1/statuses"):
            return self.mastodon_status, {}, json.dumps({"url": "https://hachyderm.io/@b/1"}).encode()
        raise AssertionError(url)

    def find(self, suffix):
        return [c for c in self.calls if c[1].endswith(suffix)]


class Post(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = Path(self.tmp.name) / "posted.json"
        self.log = []

    def tearDown(self):
        self.tmp.cleanup()

    def go(self, net, channels=post.CHANNELS, env=ENV, do_post=True):
        return post.run(channels, post=do_post, env=env, send=net, ledger_path=self.ledger, now=NOW, log=self.log.append)

    def test_posts_people_path_first_to_both_and_records_it(self):
        net = FakeNet()
        self.assertEqual(self.go(net), 0)
        led = json.loads(self.ledger.read_text())
        self.assertEqual(led["bluesky"]["learn:people"]["url"], "https://bsky.app/profile/b.bsky.social/post/3kabc")
        self.assertEqual(led["mastodon"]["learn:people"]["url"], "https://hachyderm.io/@b/1")

    def test_next_run_moves_down_the_queue(self):
        self.go(FakeNet())
        net = FakeNet()
        self.go(net)
        led = json.loads(self.ledger.read_text())
        self.assertEqual(len(led["bluesky"]), 2)
        self.assertIn("learn:ai", led["bluesky"])

    def test_bluesky_record_has_card_with_thumb_and_no_url_in_text(self):
        net = FakeNet()
        self.go(net, channels=["bluesky"])
        body = json.loads(net.find("createRecord")[0][3])
        rec = body["record"]
        self.assertNotIn("://", rec["text"])
        self.assertIn("Simon Willison", rec["text"])
        ext = rec["embed"]["external"]
        self.assertIn("utm_source=bluesky", ext["uri"])
        self.assertEqual(ext["description"], "Free courses & docs.")
        self.assertEqual(ext["thumb"]["ref"]["$link"], "bafy")
        self.assertEqual(net.find("createRecord")[0][2]["Authorization"], "Bearer jwt")
        self.assertLessEqual(len(rec["text"]), 300)

    def test_mastodon_status_and_idempotency_key(self):
        net = FakeNet()
        self.go(net, channels=["mastodon"])
        method, url, headers, data = net.find("/api/v1/statuses")[0]
        self.assertEqual(url, "https://hachyderm.io/api/v1/statuses")
        self.assertEqual(headers["Idempotency-Key"], "brianpfeil.com:learn:people")
        form = urllib.parse.parse_qs(data.decode())
        self.assertIn("utm_source=mastodon", form["status"][0])
        self.assertEqual(form["visibility"], ["public"])

    def test_missing_credentials_skip_quietly(self):
        net = FakeNet()
        self.assertEqual(self.go(net, env={}), 0)
        self.assertEqual(net.calls, [])
        self.assertFalse(self.ledger.exists())

    def test_page_not_live_is_skipped_not_failed(self):
        net = FakeNet(page_status=404)
        self.assertEqual(self.go(net), 0)
        self.assertFalse(self.ledger.exists())

    def test_one_channel_failing_keeps_the_other(self):
        net = FakeNet(mastodon_status=500)
        self.assertEqual(self.go(net), 1)
        led = json.loads(self.ledger.read_text())
        self.assertIn("learn:people", led["bluesky"])
        self.assertNotIn("learn:people", led.get("mastodon", {}))

    def test_dry_run_touches_nothing(self):
        net = FakeNet()
        self.go(net, do_post=False)
        self.assertEqual(net.calls, [])
        self.assertTrue(any("would post learn:people" in m for m in self.log))


if __name__ == "__main__":
    unittest.main()
