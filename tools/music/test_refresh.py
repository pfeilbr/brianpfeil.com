"""Unit tests for tools/music/refresh.py. No network: the YouTube responses
are built by hand in the shape the pages and the browse API return."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refresh  # noqa: E402


def artist_run(name):
    cfg = {"browseEndpointContextMusicConfig": {"pageType": "MUSIC_PAGE_TYPE_ARTIST"}}
    return {"text": name, "navigationEndpoint": {"browseEndpoint": {
        "browseId": "UC" + name, "browseEndpointContextSupportedConfigs": cfg}}}


def item(vid, runs):
    return {"musicResponsiveListItemRenderer": {
        "playlistItemData": {"videoId": vid},
        "flexColumns": [
            {"musicResponsiveListItemFlexColumnRenderer": {"text": {"runs": [
                {"text": "song", "navigationEndpoint": {"watchEndpoint": {"videoId": vid}}}]}}},
            {"musicResponsiveListItemFlexColumnRenderer": {"text": {"runs": runs}}},
        ]}}


class Parsing(unittest.TestCase):
    def test_initial_data(self):
        html = '<script>var ytInitialData = {"a": {"b": 1}};</script>'
        self.assertEqual(refresh.initial_data(html), {"a": {"b": 1}})
        with self.assertRaises(ValueError):
            refresh.initial_data("<html></html>")

    def test_channel_playlists_skips_videos(self):
        data = {"items": [
            {"lockupViewModel": {"contentId": "PL1", "contentType": "LOCKUP_CONTENT_TYPE_PLAYLIST",
                                 "metadata": {"lockupMetadataViewModel": {"title": {"content": "gym"}}}}},
            {"lockupViewModel": {"contentId": "vid", "contentType": "LOCKUP_CONTENT_TYPE_VIDEO"}},
            {"gridPlaylistRenderer": {"playlistId": "PL2", "title": {"simpleText": "old"}}},
        ]}
        self.assertEqual(refresh.channel_playlists(data), [("PL1", "gym"), ("PL2", "old")])

    def test_artists_are_the_linked_runs(self):
        runs = [artist_run("Drake"), {"text": " & "}, artist_run("21 Savage"), {"text": " • "},
                {"text": "Her Loss"}]
        self.assertEqual(refresh.tracks({"x": [item("v1", runs)]}), [("v1", ["Drake", "21 Savage"])])

    def test_uploaded_video_falls_back_to_channel_name(self):
        self.assertEqual(refresh.artists_of(item("v", [{"text": "DrakeVEVO"}])["musicResponsiveListItemRenderer"]),
                         ["Drake"])
        self.assertEqual(refresh.artists_of(item("v", [{"text": "Nas - Topic"}])["musicResponsiveListItemRenderer"]),
                         ["Nas"])

    def test_header(self):
        data = {"h": {"musicResponsiveHeaderRenderer": {
            "title": {"runs": [{"text": "Jazzhop Studies"}]},
            "subtitle": {"runs": [{"text": "Playlist • 2026"}]},
            "secondSubtitle": {"runs": [{"text": "1,089 songs • 7+ hours"}]},
            "facepile": {"avatarStackViewModel": {"text": {"content": "YouTube Music"}}}}}}
        self.assertEqual(refresh.header(data), ("Jazzhop Studies", "YouTube Music", 1089))
        self.assertEqual(refresh.header({}), (None, None, None))

    def test_embed_status_reads_escaped_player_config(self):
        ok = r'var x = "{\"previewPlayabilityStatus\":{\"status\":\"OK\",\"playableInEmbed\":true}}";'
        bad = r'"{\\\"previewPlayabilityStatus\\\":{\\\"status\\\":\\\"UNPLAYABLE\\\",\\\"reason\\\":\\\"Video unavailable\\\"'
        plain = '{"previewPlayabilityStatus": {"status": "ERROR"}}'
        self.assertEqual(refresh.embed_status(ok), "OK")
        self.assertEqual(refresh.embed_status(bad), "UNPLAYABLE")
        self.assertEqual(refresh.embed_status(plain), "ERROR")
        self.assertEqual(refresh.embed_status("<html></html>"), "UNKNOWN")

    def test_continuation_either_shape(self):
        self.assertEqual(refresh.continuation({"a": {"continuationCommand": {"token": "t1"}}}), "t1")
        self.assertEqual(refresh.continuation({"a": [{"nextContinuationData": {"continuation": "t2"}}]}), "t2")
        self.assertIsNone(refresh.continuation({}))


class Retries(unittest.TestCase):
    def setUp(self):
        self._sleep, self._open = refresh.time.sleep, refresh.urllib.request.urlopen
        refresh.time.sleep = lambda s: None

    def tearDown(self):
        refresh.time.sleep, refresh.urllib.request.urlopen = self._sleep, self._open

    def test_a_stalled_read_is_retried(self):
        calls = []

        class Resp:
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self): return b"ok"

        def opener(req, timeout):
            calls.append(1)
            if len(calls) < 3:
                raise TimeoutError("The read operation timed out")
            return Resp()
        refresh.urllib.request.urlopen = opener
        self.assertEqual(refresh.get("https://example.test/"), "ok")
        self.assertEqual(len(calls), 3)

    def test_an_http_error_is_not_retried(self):
        calls = []

        def opener(req, timeout):
            calls.append(1)
            raise refresh.urllib.error.HTTPError(req.full_url, 404, "nope", {}, None)
        refresh.urllib.request.urlopen = opener
        with self.assertRaises(refresh.urllib.error.HTTPError):
            refresh.get("https://example.test/")
        self.assertEqual(len(calls), 1)


class Output(unittest.TestCase):
    def test_top_artists_counts_every_entry_and_ranks_stably(self):
        a = [("v1", ["Drake", "21 Savage"]), ("v2", ["Nas"])]
        b = [("v1", ["Drake", "21 Savage"]), ("v3", ["drake2", "Drake", "Drake"])]
        total, top = refresh.top_artists([a, b], 2)
        self.assertEqual(total, 4)
        self.assertEqual(top, [{"name": "Drake", "count": 3}, {"name": "21 Savage", "count": 2}])

    def test_yaml_is_valid_and_keeps_emoji(self):
        out = refresh.to_yaml(3, [{"name": "Drake", "count": 2}],
                              [{"title": 'gym 💪 "x"', "id": "PL1", "tracks": 3, "note_key": "gym"},
                               {"title": "new", "id": "PL2", "tracks": 1, "note_key": None}],
                              [{"title": "Focus", "id": "RD1", "by": "YouTube Music", "tracks": 9}])
        self.assertIn('title: "gym 💪 \\"x\\""', out)
        self.assertIn('note_key: "gym"', out)
        self.assertEqual(out.count("note_key"), 1)
        self.assertTrue(out.startswith("# GENERATED"))
        try:
            import yaml
        except ImportError:
            return
        d = yaml.safe_load(out)
        self.assertEqual(d["mine"][0]["title"], 'gym 💪 "x"')
        self.assertEqual(d["saved"][0]["by"], "YouTube Music")
        self.assertEqual(d["tracks_counted"], 3)

    def test_vanished_share(self):
        old = '  - title: "a"\n    id: "PL1"\n  - title: "b"\n    id: "PL2"\n'
        self.assertEqual(refresh.vanished(old, old), 0.0)
        self.assertEqual(refresh.vanished(old, '    id: "PL1"\n    id: "PL3"\n'), 0.5)
        self.assertEqual(refresh.vanished("", old), 0.0)

    def test_current_data_file_parses(self):
        ids = refresh.listed_ids(refresh.OUT.read_text())
        self.assertGreater(len(ids), 5)

    def test_config_notes_have_english_strings(self):
        cfg = json.loads(refresh.CONFIG.read_text())
        en = (refresh.ROOT / "i18n" / "en.toml").read_text()
        for key in cfg["note_keys"].values():
            self.assertIn(f"[pl_note_{key}]", en)


if __name__ == "__main__":
    unittest.main()
