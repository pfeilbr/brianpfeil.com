"""Tests for evicting pruned files from the CDN.

Everything is cached for a year and marked immutable, so a file deleted from
S3 keeps being served from CloudFront unless it is invalidated. Un-approving a
photo has to actually take it down.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from igmedia import publish  # noqa: E402

SYNC_OUTPUT = """\
upload: build/media/20240303-aa/new.jpg to s3://brianpfeil-media01/instagram/20240303-aa/new.jpg
delete: s3://brianpfeil-media01/instagram/20220519-cc/1.jpg
delete: s3://brianpfeil-media01/instagram/20220519-cc/1-t.jpg
delete: s3://brianpfeil-media01/instagram/20220519-cc/1.jpg
"""


class Runner:
    """Records CLI calls instead of making them."""

    def __init__(self, returncode=0):
        self.calls = []
        self.returncode = returncode

    def __call__(self, cmd, **kwargs):
        self.calls.append(cmd)
        return subprocess.CompletedProcess(cmd, self.returncode, stdout="", stderr="denied")

    def batches(self):
        return [json.loads(c[c.index("--invalidation-batch") + 1]) for c in self.calls]


class DeletedPathsTest(unittest.TestCase):
    def test_takes_deletes_and_ignores_uploads(self):
        self.assertEqual(publish.deleted_paths(SYNC_OUTPUT), [
            "/instagram/20220519-cc/1-t.jpg",
            "/instagram/20220519-cc/1.jpg",
        ])

    def test_paths_are_cdn_relative_not_s3_urls(self):
        for path in publish.deleted_paths(SYNC_OUTPUT):
            self.assertTrue(path.startswith("/instagram/"))
            self.assertNotIn("s3://", path)
            self.assertNotIn("brianpfeil-media01", path)

    def test_nothing_deleted(self):
        self.assertEqual(publish.deleted_paths("upload: a to s3://b/c\n"), [])
        self.assertEqual(publish.deleted_paths(""), [])


class InvalidateTest(unittest.TestCase):
    def test_no_paths_makes_no_request(self):
        run = Runner()
        self.assertEqual(publish.invalidate("E123", [], run=run), 0)
        self.assertEqual(run.calls, [])

    def test_request_targets_the_distribution_with_the_paths(self):
        run = Runner()
        publish.invalidate("E2U0TCXARHWOEF", ["/instagram/x/1.jpg"], run=run)
        cmd = run.calls[0]
        self.assertEqual(cmd[:3], ["aws", "cloudfront", "create-invalidation"])
        self.assertEqual(cmd[cmd.index("--distribution-id") + 1], "E2U0TCXARHWOEF")
        batch = run.batches()[0]
        self.assertEqual(batch["Paths"], {"Quantity": 1, "Items": ["/instagram/x/1.jpg"]})

    def test_large_prunes_are_split_at_cloudfronts_limit(self):
        run = Runner()
        paths = [f"/instagram/x/{n}.jpg" for n in range(publish.INVALIDATION_BATCH + 5)]
        self.assertEqual(publish.invalidate("E1", paths, run=run), 2)
        sizes = [b["Paths"]["Quantity"] for b in run.batches()]
        self.assertEqual(sizes, [publish.INVALIDATION_BATCH, 5])

    def test_pruning_the_same_file_again_is_a_new_request(self):
        """A reused CallerReference is treated as already done, forever — so a
        file approved, pruned, approved and pruned again would stay cached."""
        run = Runner()
        publish.invalidate("E1", ["/instagram/x/1.jpg"], run=run)
        publish.invalidate("E1", ["/instagram/x/1.jpg"], run=run)
        refs = [b["CallerReference"] for b in run.batches()]
        self.assertNotEqual(refs[0], refs[1])

    def test_a_failed_invalidation_raises(self):
        with self.assertRaises(RuntimeError):
            publish.invalidate("E1", ["/instagram/x/1.jpg"], run=Runner(returncode=1))


if __name__ == "__main__":
    unittest.main()
