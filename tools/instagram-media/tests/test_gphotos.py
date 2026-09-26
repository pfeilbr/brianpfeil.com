"""Tests for the Google Photos picker: harvest parsing, the screening policy,
the picks file, and the data file the category sections are drawn from.

The screening policy is the privacy guarantee for this content — only B, no
number plates or addresses — so it is tested case by case.
"""

import io
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from igmedia import fetch, gphotos, gphotos_publish, screen  # noqa: E402
from igmedia.derive import Derived  # noqa: E402

KEY = "AF1QipNEQMnbiqIZxATi6YJ0ggPD80A_viLBciWZoY-0"
KEY2 = "AF1QipNcbkpKE_ufBDlOtXP7rw1ydNNJ-DzGy9PQJrS2"
URL = "https://photos.fife.usercontent.google.com/pw/AP1GczOabcdefghijklmnop=w256-h171-k-no?authuser=0"


def frame(faces=(), humans=(), upper=(), persons=(), text=(), aesthetics=0.5, utility=False):
    return {"ok": True, "faceAreas": list(faces), "humanAreas": list(humans),
            "upperBodies": list(upper), "personAreas": list(persons), "text": list(text),
            "aesthetics": aesthetics, "utility": utility}


class LabelTest(unittest.TestCase):
    def test_video_label(self):
        self.assertEqual(gphotos.parse_label("Video - Landscape - Dec 25, 2022, 1:33:46 PM"),
                         ("video", "2022-12-25T13:33:46", "landscape"))

    def test_photo_label(self):
        self.assertEqual(gphotos.parse_label("Photo - Portrait - Jan 30, 2026, 10:08:39 AM"),
                         ("photo", "2026-01-30T10:08:39", "portrait"))

    def test_unparseable_label_keeps_kind(self):
        self.assertEqual(gphotos.parse_label("Photo"), ("photo", None, None))


class UrlTest(unittest.TestCase):
    def test_base_url_drops_query_and_size(self):
        self.assertEqual(gphotos.base_url(URL),
                         "https://photos.fife.usercontent.google.com/pw/AP1GczOabcdefghijklmnop")

    def test_only_googles_image_hosts(self):
        self.assertTrue(gphotos.valid_url(URL))
        self.assertTrue(gphotos.valid_url("https://lh3.googleusercontent.com/pw/abc=w1"))
        self.assertFalse(gphotos.valid_url("http://lh3.googleusercontent.com/x"))
        self.assertFalse(gphotos.valid_url("https://evil.example/x"))
        self.assertFalse(gphotos.valid_url("https://lh3.googleusercontent.com.evil.example/x"))

    def test_item_id_is_stable_and_hides_the_key(self):
        a = gphotos.item_id(KEY, "2025-02-27T09:25:54")
        self.assertEqual(a, gphotos.item_id(KEY, "2025-02-27T09:25:54"))
        self.assertTrue(a.startswith("20250227-g"))
        self.assertNotIn(KEY, a)


class CandidatesTest(unittest.TestCase):
    def rows(self):
        return [{"key": KEY, "label": "Photo - Portrait - Jan 30, 2026, 10:08:39 AM", "url": URL},
                {"key": "not-a-key", "label": "", "url": URL},
                {"key": KEY2, "label": "", "url": "https://evil.example/x"},
                {"key": KEY2, "label": "", "url": None}]

    def test_add_filters_and_merges(self):
        with TemporaryDirectory() as d:
            c = gphotos.Candidates(Path(d) / "c.json")
            self.assertEqual(c.add(self.rows(), "skiing", "scene", "skiing"), 1)
            self.assertEqual(c.items[KEY]["tier"], "scene")
            # Found again by the "me" search: tier upgrades, not duplicated.
            self.assertEqual(c.add(self.rows(), "skiing", "me", "Brian Pfeil skiing"), 0)
            self.assertEqual(c.items[KEY]["tier"], "me")
            self.assertEqual(c.items[KEY]["queries"], ["skiing", "Brian Pfeil skiing"])
            c.save()
            again = gphotos.Candidates(Path(d) / "c.json")
            self.assertEqual(set(again.items), {KEY})

    def test_reject_reasons(self):
        rows = self.rows()
        self.assertIsNone(gphotos.reject_reason(rows[0]))
        self.assertEqual(gphotos.reject_reason(rows[1]), "unrecognised media key")
        self.assertIn("evil.example", gphotos.reject_reason(rows[2]))
        self.assertEqual(gphotos.reject_reason(rows[3]), "thumbnail had not loaded")

    def test_exclusion_survives_a_save(self):
        with TemporaryDirectory() as d:
            c = gphotos.Candidates(Path(d) / "c.json")
            c.add(self.rows()[:1], "skiing", "me", "Brian Pfeil skiing")
            self.assertEqual(c.exclude([{"key": KEY}, {"key": KEY2}]), [KEY])
            self.assertEqual(c.exclude([{"key": KEY}]), [])
            c.save()
            self.assertEqual(gphotos.Candidates(Path(d) / "c.json").excluded, {KEY, KEY2})

    def test_queries_per_category(self):
        cats = gphotos.load_categories({"categories": [{"key": "skiing", "query": "skiing"}]})
        idx = gphotos.query_index(cats, "Brian Pfeil", ["Wyatt Pfeil"])
        self.assertEqual(idx["brian pfeil skiing"], ("skiing", "me"))
        self.assertEqual(idx["skiing"], ("skiing", "scene"))
        self.assertEqual(idx["wyatt pfeil skiing"], ("skiing", "exclude"))


class ScreenTest(unittest.TestCase):
    def test_b_alone_with_face_is_ok(self):
        v = screen.verdict([frame(faces=[0.05], humans=[0.4], persons=[0.3])], "me")
        self.assertEqual(v["status"], "ok")

    def test_two_people_blocked(self):
        v = screen.verdict([frame(faces=[0.05, 0.04], persons=[0.3, 0.2])], "me")
        self.assertEqual(v["status"], "blocked")
        self.assertIn("2 people in frame", v["reasons"])

    def test_masked_second_person_found_by_segmentation(self):
        # Goggles and a balaclava: one face found, but two people segmented.
        v = screen.verdict([frame(faces=[0.2], humans=[], upper=[0.6], persons=[0.49, 0.19])], "me")
        self.assertEqual(v["status"], "blocked")

    def test_merged_bodies_split_by_upper_body_detector(self):
        v = screen.verdict([frame(faces=[0.07], humans=[0.38], upper=[0.29, 0.3], persons=[0.5])], "me")
        self.assertEqual(v["status"], "blocked")

    def test_me_without_a_face_is_blocked(self):
        v = screen.verdict([frame(faces=[], humans=[0.06], persons=[0.03])], "me")
        self.assertEqual(v["status"], "blocked")
        self.assertIn("can't be confirmed", v["reasons"][0])

    def test_far_away_speck_is_not_a_person(self):
        v = screen.verdict([frame(faces=[0.05, 0.0001], humans=[0.4, 0.0003], persons=[0.3, 0.0004])], "me")
        self.assertEqual(v["status"], "ok")

    def test_small_distant_riders_count(self):
        # Kids on bikes across a slope, 360p: only an upper body at 0.002.
        v = screen.verdict([frame(upper=[0.0021])], "scene")
        self.assertEqual(v["status"], "blocked")

    def test_scene_must_be_empty(self):
        self.assertEqual(screen.verdict([frame()], "scene")["status"], "ok")
        self.assertEqual(screen.verdict([frame(humans=[0.1])], "scene")["status"], "blocked")

    def test_scene_blocks_anyone_at_all(self):
        # A swimmer far out in a "nobody in it" beach shot.
        self.assertEqual(screen.verdict([frame(humans=[0.0002])], "scene")["status"], "blocked")
        # The same speck doesn't block a shot of B.
        v = screen.verdict([frame(faces=[0.05], humans=[0.4, 0.0002], persons=[0.3])], "me")
        self.assertEqual(v["status"], "ok")

    def test_worst_video_frame_decides(self):
        frames = [frame(faces=[0.05], persons=[0.3])] * 5 + [frame(faces=[0.05, 0.05], persons=[0.3, 0.3])]
        self.assertEqual(screen.verdict(frames, "me")["status"], "blocked")

    def test_google_exclusion_blocks(self):
        v = screen.verdict([frame(faces=[0.05], persons=[0.3])], "me", excluded=True)
        self.assertEqual(v["status"], "blocked")

    def test_private_text_blocks(self):
        for text in (["NY", "KGH 4471"], ["123 Main"], ["brian@example.com"], ["Maple Ave"],
                     ["a" * 50]):
            with self.subTest(text=text):
                v = screen.verdict([frame(faces=[0.05], persons=[0.3], text=text)], "me")
                self.assertEqual(v["status"], "blocked")

    def test_harmless_text_warns(self):
        v = screen.verdict([frame(faces=[0.05], persons=[0.3], text=["GIRO", "GoPro"])], "me")
        self.assertEqual(v["status"], "warn")
        self.assertIn("text: GIRO, GoPro", v["reasons"])

    def test_utility_shot_blocked(self):
        v = screen.verdict([frame(faces=[0.05], persons=[0.3], utility=True)], "me")
        self.assertEqual(v["status"], "blocked")

    def test_unscreenable_blocked(self):
        self.assertEqual(screen.verdict([{"ok": False}], "me")["status"], "blocked")

    def test_bursts_fold_behind_the_best(self):
        cands = [
            {"key": "a", "taken": "2025-01-01T10:00:00", "screen": {"score": 0.2}},
            {"key": "b", "taken": "2025-01-01T10:00:05", "screen": {"score": 0.6}},
            {"key": "c", "taken": "2025-01-01T11:00:00", "screen": {"score": 0.1}},
        ]
        self.assertEqual(screen.similar_groups(cands), {"a": "b", "b": "b", "c": "c"})


class SniffTest(unittest.TestCase):
    def test_sniff(self):
        self.assertEqual(fetch.sniff(b"\xff\xd8\xff\xe0" + b"0" * 12), "image")
        self.assertEqual(fetch.sniff(b"\x00\x00\x00\x18ftypmp42" + b"0" * 4), "video")
        self.assertEqual(fetch.sniff(b"\x00\x00\x00\x18ftypheic" + b"0" * 4), "image")
        self.assertEqual(fetch.sniff(b"<html>"), "other")


class PicksTest(unittest.TestCase):
    def test_round_trip_holds_only_keys_and_decisions(self):
        with TemporaryDirectory() as d:
            path = Path(d) / "picks.yaml"
            gphotos.save_picks(path, {
                KEY: {"key": KEY, "decision": "include", "category": "skiing", "url": URL},
                KEY2: {"key": KEY2, "decision": "skip", "category": None},
            })
            text = path.read_text()
            self.assertNotIn("usercontent", text)  # never a URL into the library
            picks = gphotos.load_picks(path)
            self.assertEqual(picks[KEY]["category"], "skiing")
            self.assertEqual(picks[KEY2]["decision"], "skip")
            self.assertNotIn("category", yaml.safe_load(text)["picks"][1])


class PublishTest(unittest.TestCase):
    def derived(self, kind="photo"):
        return Derived(kind=kind, key="photos/x/a.jpg", thumb_key="photos/x/a-t.jpg",
                       poster_key="photos/x/a-p.jpg" if kind == "video" else None,
                       width=1600, height=1200, duration=12.3 if kind == "video" else None,
                       grid_keys=("photos/x/a-g360.webp", "photos/x/a-g720.webp"), color="#aabbcc")

    def test_entry_has_no_caption_place_or_people(self):
        e = gphotos_publish.entry({"id": "20250101-gabc", "taken": "2025-01-01T10:00:00"}, "skiing",
                                  self.derived())
        self.assertEqual(set(e), {"id", "date", "year", "category", "kind", "media"})
        self.assertEqual(e["date"], "2025-01-01")

    def test_order_is_category_then_newest(self):
        es = [{"id": "a", "category": "beach", "date": "2025-01-01"},
              {"id": "b", "category": "skiing", "date": "2024-01-01"},
              {"id": "c", "category": "skiing", "date": "2025-06-01"}]
        self.assertEqual([e["id"] for e in gphotos_publish.order(es, ["skiing", "beach"])], ["c", "b", "a"])

    def test_write_lists_only_categories_with_items(self):
        with TemporaryDirectory() as d:
            path = Path(d) / "photos.yaml"
            e = gphotos_publish.entry({"id": "x", "taken": "2025-01-01T00:00:00"}, "beach", self.derived())
            gphotos_publish.write(path, "https://cdn.example", ["skiing", "beach"], [e])
            data = yaml.safe_load(path.read_text())
            self.assertEqual(data["categories"], ["beach"])
            self.assertEqual(data["base_url"], "https://cdn.example/")

    def test_build_refuses_before_encoding_when_a_source_is_missing(self):
        with TemporaryDirectory() as d:
            cands = {KEY: {"key": KEY, "id": "x", "kind": "video", "tier": "me"}}
            picks = {KEY: {"key": KEY, "decision": "include", "category": "skiing"}}
            with self.assertRaises(gphotos_publish.MissingSource):
                gphotos_publish.build(picks, cands, ["skiing"], Path(d), "photos", None,
                                      vision=None, source=lambda c: Path(d) / "nope.mp4", log=lambda s: None)

    def test_build_refuses_what_fails_the_full_size_screen(self):
        with TemporaryDirectory() as d:
            src = Path(d) / "a.jpg"
            src.write_bytes(b"\xff\xd8\xff" + b"0" * 100)
            cands = {KEY: {"key": KEY, "id": "x", "kind": "photo", "tier": "me"}}
            picks = {KEY: {"key": KEY, "decision": "include", "category": "skiing"}}

            class Lock:
                def get(self, _):
                    return None

                def save(self):
                    pass

            two_people = lambda imgs: [frame(faces=[0.05, 0.05], persons=[0.3, 0.3])]  # noqa: E731
            entries, refused = gphotos_publish.build(picks, cands, ["skiing"], Path(d), "photos", Lock(),
                                                     two_people, lambda c: src, log=lambda s: None)
            self.assertEqual((entries, refused), ([], [KEY]))


if __name__ == "__main__":
    unittest.main()
