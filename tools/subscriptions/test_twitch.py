import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import twitch  # noqa: E402

SAMPLE = '''# c
following_total: 2

following:
  - login: "a"
    name: "A"
    followers: "7K"
    avatar: "/a.jpg"
  - login: "b"
    name: "B"
    followers: "5K"
    avatar: "/b.jpg"

past:
  - login: "c"
    name: "C"
    followers: "1.2M"
    avatar: "/c.jpg"
'''


class TwitchTest(unittest.TestCase):
    def test_fmt(self):
        self.assertEqual(twitch.fmt(11_512_345), "11.5M")
        self.assertEqual(twitch.fmt(6_012_000), "6M")
        self.assertEqual(twitch.fmt(709_400), "709K")
        self.assertEqual(twitch.fmt(950), "950")

    def test_updates_and_resorts_each_list(self):
        live = {"a": {"name": "A", "followers": 4000}, "b": {"name": "Bee", "followers": 9000},
                "c": {"name": "C", "followers": 1_260_000}}
        out = twitch.refresh(SAMPLE, live)
        self.assertLess(out.index('login: "b"'), out.index('login: "a"'))
        self.assertIn('name: "Bee"', out)
        self.assertIn('followers: "1.3M"', out)
        self.assertTrue(out.startswith("# c\nfollowing_total: 2\n"))

    def test_unchanged_is_identical(self):
        live = {"a": {"name": "A", "followers": 7000}, "b": {"name": "B", "followers": 5000},
                "c": {"name": "C", "followers": 1_200_000}}
        self.assertEqual(twitch.refresh(SAMPLE, live), SAMPLE)

    def test_missing_channel_is_kept(self):
        out = twitch.refresh(SAMPLE, {})
        self.assertEqual(out, SAMPLE)


if __name__ == "__main__":
    unittest.main()
