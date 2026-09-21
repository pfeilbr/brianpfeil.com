"""Tests for the generated music: deterministic, well-levelled, seamless."""

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


class ChooseTest(unittest.TestCase):
    SECONDS = {t.id: 120.0 for t in music.TRACKS}

    def test_same_key_same_track_and_offset(self):
        self.assertEqual(music.choose("20250314-DHLzXu1uX9f", self.SECONDS),
                         music.choose("20250314-DHLzXu1uX9f", self.SECONDS))

    def test_offset_stays_inside_the_track(self):
        for n in range(200):
            track, offset = music.choose(f"post-{n}", self.SECONDS)
            self.assertTrue(0 <= offset <= self.SECONDS[track.id] - 8)

    def test_every_track_gets_used(self):
        used = {music.choose(f"post-{n}", self.SECONDS)[0].id for n in range(200)}
        self.assertEqual(used, {t.id for t in music.TRACKS})


class LibraryTest(unittest.TestCase):
    def test_rendered_once_then_reused(self):
        with TemporaryDirectory() as tmp, mock.patch.object(music, "SECTIONS", SHORT):
            first = music.ensure_library(Path(tmp))
            with mock.patch.object(music, "render", side_effect=AssertionError("re-rendered")):
                again = music.ensure_library(Path(tmp))
            self.assertEqual(first, again)
            self.assertTrue(all(p.exists() for p in first.values()))


if __name__ == "__main__":
    unittest.main()
