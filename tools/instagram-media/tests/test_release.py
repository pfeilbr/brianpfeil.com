"""Tests for release.commit_and_push against a real throwaway git repo.

The property that matters most: a release commits the data file and the
approve list and nothing else, even when unrelated work is staged.
"""

import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from igmedia import release  # noqa: E402


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                          text=True, check=True).stdout.strip()


class ReleaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.remote = root / "remote.git"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(self.remote)], check=True)

        self.repo = root / "site"
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.repo)], check=True)
        git(self.repo, "config", "user.email", "test@example.com")
        git(self.repo, "config", "user.name", "Test")
        git(self.repo, "remote", "add", "origin", str(self.remote))
        (self.repo / "README.md").write_text("site\n")
        git(self.repo, "add", "README.md")
        git(self.repo, "commit", "-q", "-m", "init")
        git(self.repo, "push", "-q", "origin", "main")

        (self.repo / "data").mkdir()
        self.data = self.repo / "data" / "media.yaml"
        self.manifest = self.repo / "manifest.yaml"
        self.data.write_text("count: 2\n")
        self.manifest.write_text("items: []\n")

    def files_in(self, ref="HEAD"):
        return sorted(git(self.repo, "show", "--name-only", "--pretty=format:", ref).split())

    def test_commits_both_files_and_pushes(self):
        sha = release.commit_and_push(self.repo, [self.data, self.manifest], "Publish 2 items")
        self.assertTrue(sha)
        self.assertEqual(self.files_in(), ["data/media.yaml", "manifest.yaml"])
        self.assertEqual(git(self.remote, "rev-parse", "--short", "main"), sha)

    def test_unrelated_staged_work_is_left_out_and_left_staged(self):
        (self.repo / "wip.txt").write_text("half done\n")
        git(self.repo, "add", "wip.txt")
        release.commit_and_push(self.repo, [self.data, self.manifest], "Publish 2 items")
        self.assertNotIn("wip.txt", self.files_in())
        self.assertIn("wip.txt", git(self.repo, "diff", "--cached", "--name-only"))

    def test_unrelated_unstaged_changes_are_untouched(self):
        (self.repo / "README.md").write_text("edited, not staged\n")
        release.commit_and_push(self.repo, [self.data, self.manifest], "Publish 2 items")
        self.assertNotIn("README.md", self.files_in())
        self.assertIn("README.md", git(self.repo, "diff", "--name-only"))

    def test_no_change_since_last_release_is_a_no_op(self):
        release.commit_and_push(self.repo, [self.data, self.manifest], "Publish 2 items")
        head = git(self.repo, "rev-parse", "HEAD")
        self.assertEqual(release.commit_and_push(self.repo, [self.data, self.manifest], "again"), "")
        self.assertEqual(git(self.repo, "rev-parse", "HEAD"), head)

    def test_only_a_changed_file_is_recommitted(self):
        release.commit_and_push(self.repo, [self.data, self.manifest], "first")
        self.data.write_text("count: 3\n")
        release.commit_and_push(self.repo, [self.data, self.manifest], "second")
        self.assertEqual(self.files_in(), ["data/media.yaml"])

    def test_push_can_be_skipped(self):
        sha = release.commit_and_push(self.repo, [self.data], "local only", push=False)
        self.assertNotEqual(git(self.remote, "rev-parse", "--short", "main"), sha)

    def test_a_rejected_push_says_the_commit_exists(self):
        git(self.repo, "remote", "set-url", "origin", str(self.repo / "no-such-remote"))
        with self.assertRaises(release.ReleaseError) as ctx:
            release.commit_and_push(self.repo, [self.data], "Publish")
        self.assertIn("push failed", str(ctx.exception))
        self.assertIn("committed", str(ctx.exception))

    def test_nothing_to_release(self):
        with self.assertRaises(release.ReleaseError):
            release.commit_and_push(self.repo, [self.repo / "absent.yaml"], "x")


class MessageTest(unittest.TestCase):
    def test_singular_and_plural(self):
        self.assertTrue(release.message_for(1, 1).startswith("Publish 1 item to /media/"))
        self.assertTrue(release.message_for(12, 12).startswith("Publish 12 items to /media/"))


if __name__ == "__main__":
    unittest.main()
