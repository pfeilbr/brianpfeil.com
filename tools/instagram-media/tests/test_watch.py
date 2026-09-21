"""Tests for the Downloads watcher's decision about when to stage.

The failure modes that matter: staging a half-written download, staging some
unrelated ZIP, missing a media-only part, or staging the same export twice.
Staging itself is injected, so none of this runs pull.py.
"""

import json
import os
import sys
import time
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import watch_downloads as w  # noqa: E402

OLD = time.time() - 3600  # comfortably past the settle window


def make_zip(path: Path, names: list[str], mtime: float = OLD) -> Path:
    with zipfile.ZipFile(path, "w") as zf:
        for name in names:
            zf.writestr(name, b"x")
    os.utime(path, (mtime, mtime))
    return path


class Recorder:
    """Stands in for run_stage and remembers what it was asked to stage."""

    def __init__(self, ok=True, output="4 items (0 approved)\n"):
        self.calls = []
        self.ok, self.output = ok, output

    def __call__(self, exports):
        self.calls.append([p.name for p in exports])
        return self.ok, self.output


class DetectionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def test_export_recognised_by_its_contents(self):
        make_zip(self.dir / "download.zip", ["your_instagram_activity/media/posts_1.json"])
        self.assertEqual([p.name for p in w.find_exports(self.dir)], ["download.zip"])

    def test_media_only_part_recognised_by_its_name(self):
        make_zip(self.dir / "instagram-pfeilbr-2026-09-21-part2.zip", ["media/posts/a.jpg"])
        self.assertEqual(len(w.find_exports(self.dir)), 1)

    def test_unrelated_zip_ignored(self):
        make_zip(self.dir / "iTerm2-3_7_0.zip", ["iTerm.app/Contents/Info.plist"])
        self.assertEqual(w.find_exports(self.dir), [])

    def test_download_in_progress_ignored(self):
        make_zip(self.dir / "instagram-pfeilbr.zip.crdownload", ["your_instagram_activity/x.json"])
        self.assertEqual(w.find_exports(self.dir), [])

    def test_freshly_written_file_left_to_settle(self):
        make_zip(self.dir / "instagram-pfeilbr.zip", ["your_instagram_activity/x.json"],
                 mtime=time.time())
        self.assertEqual(w.find_exports(self.dir), [])

    def test_corrupt_zip_ignored_rather_than_raising(self):
        bad = self.dir / "instagram-truncated.zip"
        bad.write_bytes(b"PK\x03\x04 not really a zip")
        os.utime(bad, (OLD, OLD))
        # The name says instagram, but it can't be opened, so it isn't staged.
        self.assertEqual(w.find_exports(self.dir), [])

    def test_hidden_files_ignored(self):
        make_zip(self.dir / ".instagram.zip", ["your_instagram_activity/x.json"])
        self.assertEqual(w.find_exports(self.dir), [])

    def test_missing_directory_is_just_empty(self):
        self.assertEqual(w.find_exports(self.dir / "nope"), [])


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name) / "Downloads"
        self.dir.mkdir()
        self.state = Path(self.tmp.name) / "state.json"

    def test_nothing_to_do(self):
        rec = Recorder()
        self.assertEqual(w.check(self.dir, self.state, rec), "no export")
        self.assertEqual(rec.calls, [])

    def test_stages_every_part_together(self):
        make_zip(self.dir / "instagram-pfeilbr-part1.zip", ["your_instagram_activity/x.json"])
        make_zip(self.dir / "instagram-pfeilbr-part2.zip", ["media/posts/a.jpg"])
        rec = Recorder()
        result = w.check(self.dir, self.state, rec)
        self.assertTrue(result.startswith("staged 2 archive(s)"))
        self.assertEqual(rec.calls, [["instagram-pfeilbr-part1.zip", "instagram-pfeilbr-part2.zip"]])

    def test_same_export_is_staged_once(self):
        make_zip(self.dir / "instagram-pfeilbr.zip", ["your_instagram_activity/x.json"])
        rec = Recorder()
        w.check(self.dir, self.state, rec)
        self.assertEqual(w.check(self.dir, self.state, rec), "already staged")
        self.assertEqual(len(rec.calls), 1)

    def test_a_new_part_triggers_a_restage(self):
        make_zip(self.dir / "instagram-pfeilbr-part1.zip", ["your_instagram_activity/x.json"])
        rec = Recorder()
        w.check(self.dir, self.state, rec)
        make_zip(self.dir / "instagram-pfeilbr-part2.zip", ["media/posts/a.jpg"])
        w.check(self.dir, self.state, rec)
        self.assertEqual(len(rec.calls), 2)
        self.assertEqual(len(rec.calls[1]), 2)

    def test_a_failed_stage_is_retried_next_time(self):
        make_zip(self.dir / "instagram-pfeilbr.zip", ["your_instagram_activity/x.json"])
        failing = Recorder(ok=False, output="boom")
        self.assertTrue(w.check(self.dir, self.state, failing).startswith("stage failed"))
        rec = Recorder()
        self.assertTrue(w.check(self.dir, self.state, rec).startswith("staged"))

    def test_state_file_is_valid_json(self):
        make_zip(self.dir / "instagram-pfeilbr.zip", ["your_instagram_activity/x.json"])
        w.check(self.dir, self.state, Recorder())
        data = json.loads(self.state.read_text())
        self.assertEqual(data["staged"][0][0], "instagram-pfeilbr.zip")


class PlistTest(unittest.TestCase):
    def test_watches_downloads_and_never_publishes(self):
        body = w.plist_body()
        self.assertEqual(body["WatchPaths"], [str(w.WATCH_DIR)])
        self.assertIn("StartInterval", body)
        # It runs this script with no arguments: a check, never publish.
        self.assertEqual(len(body["ProgramArguments"]), 2)
        self.assertTrue(body["ProgramArguments"][1].endswith("watch_downloads.py"))


if __name__ == "__main__":
    unittest.main()
