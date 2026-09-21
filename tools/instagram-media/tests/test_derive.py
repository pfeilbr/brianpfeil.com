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


@unittest.skipUnless(HAS_FFMPEG, "ffmpeg not installed")
class VideoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.src = self.root / "in.mp4"
        subprocess.run(
            ["ffmpeg", "-nostdin", "-y", "-loglevel", "error",
             "-f", "lavfi", "-i", "testsrc2=size=1080x1920:rate=30",
             "-f", "lavfi", "-i", "sine=frequency=440", "-t", "1",
             "-metadata", "location=+40.4461-079.9822/",
             "-metadata", "creation_time=2023-01-01T12:00:00Z",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
             str(self.src)],
            check=True,
        )
        self.lock = derive.Lock(self.root / "lock.json")

    def test_video_is_capped_at_720_and_stripped_of_location(self):
        d = derive.derive(Media(self.src, "video", "d" * 64), "vid", self.root / "out",
                          "instagram", self.lock)
        self.assertEqual(d.height, derive.VIDEO_MAX_HEIGHT)
        self.assertEqual(d.width % 2, 0)
        self.assertIsNotNone(d.poster_key)

        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format_tags", "-of", "default",
             str(self.root / "out" / "vid" / Path(d.key).name)],
            capture_output=True, text=True, check=True,
        ).stdout
        self.assertNotIn("location", probe.lower())
        self.assertNotIn("2023-01-01", probe)


if __name__ == "__main__":
    unittest.main()
