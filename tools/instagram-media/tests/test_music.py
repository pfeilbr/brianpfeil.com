"""Tests for the generated music: deterministic, well-levelled, seamless."""

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from igmedia import music  # noqa: E402

# Four bars instead of forty-eight: the same code paths, a fraction of the time.
SHORT = (("intro", 1), ("verse", 1), ("chorus", 1), ("outro", 1))


class RenderTest(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.object(music, "SECTIONS", SHORT)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_same_track_renders_identical_samples(self):
        a, b = music.render(music.TRACKS[0]), music.render(music.TRACKS[0])
        self.assertTrue(np.array_equal(a, b))

    def test_tracks_differ(self):
        a, b = music.render(music.TRACKS[0]), music.render(music.TRACKS[1])
        self.assertFalse(len(a) == len(b) and np.allclose(a, b))

    def test_peak_is_minus_one_dbfs_and_nothing_clips(self):
        for track in music.TRACKS:
            audio = music.render(track)
            self.assertAlmostEqual(20 * np.log10(np.abs(audio).max()), -1.0, delta=0.05)
            self.assertFalse(np.isnan(audio).any())

    def test_it_is_audible_background_music(self):
        audio = music.render(music.TRACKS[0])
        rms_db = 20 * np.log10(np.sqrt((audio ** 2).mean()))
        self.assertTrue(-26 < rms_db < -10, rms_db)

    def test_loop_seam_is_no_bigger_than_an_ordinary_step(self):
        for track in music.TRACKS:
            audio = music.render(track)
            seam = np.abs(audio[-1] - audio[0]).max()
            ordinary = np.percentile(np.abs(np.diff(audio, axis=0)).max(axis=1), 99.9)
            self.assertLessEqual(seam, ordinary, track.title)


class AssignTest(unittest.TestCase):
    """One song per video, recorded in the shared index (B, 2026-10-06)."""

    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ledger = Path(self.tmp.name) / "ledger.jsonl"

    def test_a_video_keeps_its_song(self):
        a = music.assign("brianpfeil.com/media/x/abc", self.ledger)
        b = music.assign("brianpfeil.com/media/x/abc", self.ledger)
        self.assertEqual(a, b)
        self.assertEqual(len(self.ledger.read_text().splitlines()), 1)

    def test_every_video_gets_a_different_key_and_progression(self):
        sigs = set()
        for n in range(40):
            t = music.assign(f"brianpfeil.com/media/x/{n}", self.ledger)
            sig = (t.root, t.progression)
            self.assertNotIn(sig, sigs)
            sigs.add(sig)

    def test_other_projects_rows_are_kept_verbatim(self):
        other = '{"at": "2026-10-07T09:12:58+00:00", "key": -1, "prog": 1, "seed": 5, "style": "drive", "video": "v"}\n'
        self.ledger.write_text(other)
        music.assign("brianpfeil.com/media/x/abc", self.ledger)
        lines = self.ledger.read_text().splitlines(keepends=True)
        self.assertEqual(lines[0], other)
        row = json.loads(lines[1])
        self.assertEqual((row["style"], row["video"]), (music.STYLE, "brianpfeil.com/media/x/abc"))
        self.assertEqual((row["key"], row["prog"]), music.signature(row["seed"]))

    def test_a_concurrent_write_is_retried_not_overwritten(self):
        real_save = music._save
        calls = []

        def racing_save(path, raw, tag):
            if not calls:  # someone else appends between our read and write
                calls.append(1)
                with open(path, "a") as f:
                    f.write('{"key": 0, "prog": 0, "seed": 1, "style": "night", "video": "w"}\n')
            return real_save(path, raw, tag)

        with mock.patch.object(music, "_save", racing_save):
            music.assign("brianpfeil.com/media/x/abc", self.ledger)
        videos = [json.loads(l)["video"] for l in self.ledger.read_text().splitlines()]
        self.assertEqual(videos, ["w", "brianpfeil.com/media/x/abc"])

    def test_seeded_track_is_a_valid_song(self):
        t = music.track_from_seed(123456)
        self.assertEqual(t, music.track_from_seed(123456))
        self.assertTrue(t.id.startswith("t"))
        self.assertIn(t.root, music.ROOTS)
        with mock.patch.object(music, "SECTIONS", SHORT):
            audio = music.render(t)
        self.assertAlmostEqual(20 * np.log10(np.abs(audio).max()), -1.0, delta=0.05)
