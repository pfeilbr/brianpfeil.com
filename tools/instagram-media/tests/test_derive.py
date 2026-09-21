"""Tests for turning originals into the files the site serves.

This module carries the privacy promise — no GPS or other metadata reaches the
public CDN — so these use real images and inspect the real output rather than
mocking the encoder. Video tests need ffmpeg and are skipped without it.
"""

import shutil
import subprocess
import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from igmedia import derive  # noqa: E402

HAS_FFMPEG = shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None

GPS_IFD = 0x8825
ORIENTATION = 0x0112


@dataclass
class Media:
    path: Path
    kind: str
    sha256: str


def jpeg_with_gps(path: Path, size=(2400, 1800), orientation=None) -> Path:
    """A JPEG carrying GPS coordinates, as a phone original might."""
    im = Image.new("RGB", size, (200, 80, 40))
    exif = Image.Exif()
    exif[0x010F] = "Apple"                      # Make
    exif.get_ifd(GPS_IFD)[2] = (40.0, 26.0, 46.0)  # GPSLatitude
    exif.get_ifd(GPS_IFD)[4] = (79.0, 58.0, 56.0)  # GPSLongitude
    if orientation is not None:
        exif[ORIENTATION] = orientation
    im.save(path, format="JPEG", exif=exif.tobytes())
    return path


class PhotoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.out = self.root / "out"
        self.lock = derive.Lock(self.root / "lock.json")

    def derive_photo(self, src: Path, sha="a" * 64):
        return derive.derive(Media(src, "photo", sha), "20230101-x", self.out, "instagram", self.lock)

    def test_fixture_really_has_gps_to_strip(self):
        src = jpeg_with_gps(self.root / "in.jpg")
        with Image.open(src) as im:
            self.assertTrue(im.getexif().get_ifd(GPS_IFD))

    def test_gps_and_all_exif_are_stripped(self):
        src = jpeg_with_gps(self.root / "in.jpg")
        d = self.derive_photo(src)
        for name in (Path(d.key).name, Path(d.thumb_key).name):
            with Image.open(self.out / "20230101-x" / name) as im:
                exif = im.getexif()
                self.assertFalse(exif.get_ifd(GPS_IFD), f"{name} still has GPS")
                self.assertEqual(len(exif), 0, f"{name} still has EXIF: {dict(exif)}")

    def test_sizes_are_capped_and_aspect_kept(self):
        d = self.derive_photo(jpeg_with_gps(self.root / "in.jpg", size=(2400, 1800)))
        self.assertEqual((d.width, d.height), (derive.IMAGE_MAX, 1200))
        with Image.open(self.out / "20230101-x" / Path(d.thumb_key).name) as thumb:
            self.assertEqual(max(thumb.size), derive.THUMB_MAX)

    def test_small_images_are_not_upscaled(self):
        d = self.derive_photo(jpeg_with_gps(self.root / "in.jpg", size=(640, 480)))
        self.assertEqual((d.width, d.height), (640, 480))

    def test_exif_rotation_is_baked_in_before_it_is_dropped(self):
        """Orientation 6 means 'rotate 90'. Dropping EXIF without applying it
        first would publish a sideways photo."""
        src = jpeg_with_gps(self.root / "in.jpg", size=(1600, 1200), orientation=6)
        d = self.derive_photo(src)
        self.assertGreater(d.height, d.width)

    def test_keys_carry_prefix_item_and_content_hash(self):
        d = self.derive_photo(jpeg_with_gps(self.root / "in.jpg"), sha="b" * 64)
        self.assertEqual(d.key, "instagram/20230101-x/bbbbbbbbbbbb.jpg")
        self.assertEqual(d.thumb_key, "instagram/20230101-x/bbbbbbbbbbbb-t.jpg")
        self.assertIsNone(d.poster_key)


class CacheTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.out = self.root / "out"
        self.src = jpeg_with_gps(self.root / "in.jpg", size=(800, 600))
        self.media = Media(self.src, "photo", "c" * 64)

    def run_derive(self, lock):
        return derive.derive(self.media, "id", self.out, "instagram", lock)

    def test_second_run_reuses_without_encoding(self):
        lock = derive.Lock(self.root / "lock.json")
        first = self.run_derive(lock)
        with mock.patch.object(derive, "_save_image", side_effect=AssertionError("re-encoded")):
            second = self.run_derive(lock)
        self.assertEqual(first, second)

    def test_lock_survives_a_save_and_reload(self):
        lock = derive.Lock(self.root / "lock.json")
        self.run_derive(lock)
        lock.save()
        reloaded = derive.Lock(self.root / "lock.json")
        with mock.patch.object(derive, "_save_image", side_effect=AssertionError("re-encoded")):
            self.run_derive(reloaded)

    def test_missing_output_is_rebuilt(self):
        lock = derive.Lock(self.root / "lock.json")
        d = self.run_derive(lock)
        (self.out / "id" / Path(d.key).name).unlink()
        self.run_derive(lock)
        self.assertTrue((self.out / "id" / Path(d.key).name).exists())

    def test_a_profile_bump_forces_a_re_encode(self):
        lock = derive.Lock(self.root / "lock.json")
        self.run_derive(lock)
        calls = []
        real = derive._save_image
        with mock.patch.object(derive, "PROFILE_VERSION", derive.PROFILE_VERSION + 1), \
             mock.patch.object(derive, "_save_image",
                               side_effect=lambda *a, **k: calls.append(1) or real(*a, **k)):
            self.run_derive(lock)
        self.assertEqual(len(calls), 2)  # full and thumb

    def test_a_corrupt_lock_file_starts_empty(self):
        path = self.root / "lock.json"
        path.write_text("{not json")
        self.assertEqual(derive.Lock(path).data, {})


def make_video(path: Path, size: str, codec: str = "libx264", audio: bool = True,
               extra: list[str] | None = None) -> Path:
    """A short clip tagged with a location and creation time on the container
    and on the streams, as a phone video can be."""
    cmd = ["ffmpeg", "-nostdin", "-y", "-loglevel", "error",
           "-f", "lavfi", "-i", f"testsrc2=size={size}:rate=30"]
    if audio:
        cmd += ["-f", "lavfi", "-i", "sine=frequency=440"]
    cmd += ["-t", "1",
            "-metadata", "location=+40.4461-079.9822/",
            "-metadata", "creation_time=2023-01-01T12:00:00Z",
            "-metadata:s:v", "creation_time=2023-01-01T12:00:00Z",
            "-c:v", codec, "-pix_fmt", "yuv420p", *(extra or [])]
    if audio:
        cmd += ["-c:a", "aac", "-shortest"]
    subprocess.run(cmd + [str(path)], check=True)
    return path


def tags(path: Path) -> str:
    """Every container and stream tag, lower-cased, for asserting absence."""
    return subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format_tags:stream_tags",
         "-of", "default", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.lower()


class RemuxDecisionTest(unittest.TestCase):
    """Pure logic: which files are already what a browser wants."""

    def info(self, **over):
        base = {"video": "h264", "audio": "aac", "width": 720, "height": 960,
                "bit_rate": 2_000_000}
        base.update(over)
        return base

    def test_web_ready_h264_is_remuxed(self):
        self.assertTrue(derive.can_remux(self.info()))

    def test_silent_clip_is_remuxed(self):
        self.assertTrue(derive.can_remux(self.info(audio=None)))

    def test_hevc_is_re_encoded(self):
        self.assertFalse(derive.can_remux(self.info(video="hevc")))

    def test_oversized_is_re_encoded(self):
        self.assertFalse(derive.can_remux(self.info(width=1920, height=1080)))

    def test_high_bitrate_is_re_encoded(self):
        self.assertFalse(derive.can_remux(self.info(bit_rate=derive.VIDEO_MAX_REMUX_BITRATE + 1)))

    def test_odd_audio_is_re_encoded(self):
        self.assertFalse(derive.can_remux(self.info(audio="opus")))


@unittest.skipUnless(HAS_FFMPEG, "ffmpeg not installed")
class VideoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.lock = derive.Lock(self.root / "lock.json")

    def derive_video(self, src: Path, name="vid"):
        d = derive.derive(Media(src, "video", name.ljust(64, "0")), name, self.root / "out",
                          "instagram", self.lock)
        return d, self.root / "out" / name / Path(d.key).name

    def assert_clean(self, out: Path):
        found = tags(out)
        self.assertNotIn("location", found)
        self.assertNotIn("2023-01-01", found)

    def test_web_ready_clip_is_remuxed_untouched_and_stripped(self):
        src = make_video(self.root / "ready.mp4", "720x960")
        d, out = self.derive_video(src, "ready")
        self.assertEqual((d.width, d.height), (720, 960))  # not scaled down
        self.assertEqual(derive.probe_streams(out)["video"], "h264")
        self.assert_clean(out)

    def test_silent_clip_remuxes_without_inventing_audio(self):
        src = make_video(self.root / "silent.mp4", "720x900", audio=False)
        _, out = self.derive_video(src, "silent")
        self.assertIsNone(derive.probe_streams(out)["audio"])
        self.assert_clean(out)

    def test_oversized_clip_is_re_encoded_to_the_long_edge_cap(self):
        src = make_video(self.root / "big.mp4", "1080x1920")
        d, out = self.derive_video(src, "big")
        self.assertEqual(max(d.width, d.height), derive.VIDEO_MAX_EDGE)
        self.assertEqual((d.width % 2, d.height % 2), (0, 0))
        self.assertIsNotNone(d.poster_key)
        self.assert_clean(out)

    def test_hevc_is_re_encoded_to_h264(self):
        if "libx265" not in subprocess.run(["ffmpeg", "-hide_banner", "-encoders"],
                                           capture_output=True, text=True).stdout:
            self.skipTest("ffmpeg built without libx265")
        src = make_video(self.root / "hevc.mp4", "720x960", codec="libx265",
                         extra=["-tag:v", "hvc1"])
        _, out = self.derive_video(src, "hevc")
        self.assertEqual(derive.probe_streams(out)["video"], "h264")
        self.assert_clean(out)


if __name__ == "__main__":
    unittest.main()
