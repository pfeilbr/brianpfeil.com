"""Poster frame choice and the poster repair's data edits (no network, no AWS)."""

import sys
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOL))
from igmedia import derive  # noqa: E402
import repair_posters as rp  # noqa: E402


class FrameChoice(unittest.TestCase):
    def test_times_start_then_spread_and_stay_inside_the_clip(self):
        self.assertEqual(derive.candidate_times(20), [0.0, 1.0, 2.0, 5.0, 10.0])
        self.assertEqual(derive.candidate_times(1.5), [0.0, 1.0, 0.15, 0.38, 0.75])
        self.assertEqual(derive.candidate_times(None), [0.0, 1.0, 2.0])

    def test_first_frame_that_is_not_black_wins(self):
        self.assertEqual(derive.pick_frame([(0.0, 2.0), (1.0, 40.0), (2.0, 90.0)]), 1.0)

    def test_a_bright_first_frame_is_kept(self):
        self.assertEqual(derive.pick_frame([(0.0, 80.0)]), 0.0)

    def test_all_dark_falls_back_to_the_brightest(self):
        self.assertEqual(derive.pick_frame([(0.0, 1.0), (1.0, 9.0), (2.0, 4.0)]), 1.0)


class Repair(unittest.TestCase):
    YAML = """items:
- id: a
  media:
  - kind: video
    src: instagram/a/aaa.mp4
    poster: instagram/a/aaa-p.jpg
    grid:
    - instagram/a/aaa-g360.webp
    - instagram/a/aaa-g720.webp
    color: '#000000'
- id: b
  media:
  - kind: video
    src: instagram/b/bbb.mp4
    poster: instagram/b/bbb-p.jpg
    grid:
    - instagram/b/bbb-g360.webp
    color: '#000000'
"""

    def test_only_dark_posters_are_picked(self):
        import yaml
        items = yaml.safe_load(self.YAML)["items"]
        lumas = {"instagram/a/aaa-p.jpg": 3.0, "instagram/b/bbb-p.jpg": 70.0}
        self.assertEqual([i for i, _ in rp.dark_videos(items, lumas.get)], ["a"])

    def test_set_color_edits_only_that_entry(self):
        out = rp.set_color(self.YAML, "instagram/a/aaa-g360.webp", "#6b5a4e")
        self.assertIn("    - instagram/a/aaa-g720.webp\n    color: '#6b5a4e'", out)
        self.assertIn("    - instagram/b/bbb-g360.webp\n    color: '#000000'", out)
        self.assertEqual(out.count("\n"), self.YAML.count("\n"))

    def test_set_color_refuses_an_unknown_entry(self):
        with self.assertRaises(ValueError):
            rp.set_color(self.YAML, "instagram/zzz-g360.webp", "#ffffff")


if __name__ == "__main__":
    unittest.main()
