import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rescue  # noqa: E402
import selfhost as sh  # noqa: E402

SHORT = "https://www.evernote.com/l/AAE_dm6okTFHs6TCPnRfFcmAdBo-yIVHs7YB/image.png"
SHARD = "https://www.evernote.com/shard/s1/sh/81d7-fa1c/u6hQ-Ote/deep/0/image.png"


class MatchTest(unittest.TestCase):
    def test_both_evernote_forms_and_nothing_else(self):
        images = {SHORT: [], SHARD: [], "https://www.evernote.com/l/AAEG72PQ": [],
                  "https://raw.githubusercontent.com/u/r/a.png": [], "https://evernote.com.evil.test/l/x/image.png": []}
        self.assertEqual(sh.evernote_images(images), sorted([SHORT, SHARD, "https://www.evernote.com/l/AAEG72PQ"]))

    def test_local_names(self):
        self.assertEqual(sh.local_name(SHORT), "evernote-AAE_dm6okTFHs6TCPnRfFcmAdBo-yIVHs7YB.webp")
        self.assertRegex(sh.local_name(SHARD), r"^evernote-[0-9a-f]{16}\.webp$")


class RealDataTest(unittest.TestCase):
    """What is committed: every Evernote image in a post is mapped, and every
    self-hosted file the map points at exists."""

    def test_every_evernote_image_is_mapped(self):
        mapping = json.loads(rescue.MAP.read_text(encoding="utf-8"))
        missing = [u for u in sh.evernote_images(rescue.remote_images()) if u not in mapping]
        self.assertEqual(missing, [])

    def test_mapped_files_exist(self):
        mapping = json.loads(rescue.MAP.read_text(encoding="utf-8"))
        for url, local in mapping.items():
            if local:
                self.assertTrue((rescue.REPO / "static" / local.lstrip("/")).exists(), f"{url} -> {local}")


if __name__ == "__main__":
    unittest.main()
