import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import tiktok_handle as th  # noqa: E402


def page(uid):
    data = {"__DEFAULT_SCOPE__": {"webapp.user-detail": {"userInfo": {"user": {"id": uid}}} if uid else {"statusCode": 10221}}}
    return f'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">{json.dumps(data)}</script>'


class Owner(unittest.TestCase):
    def test_reads_user_id(self):
        self.assertEqual(th.owner(page(th.ACCOUNT_ID)), th.ACCOUNT_ID)

    def test_missing_account(self):
        self.assertIsNone(th.owner(page(None)))

    def test_no_data_block(self):
        self.assertIsNone(th.owner("<html>blocked</html>"))


class Rewrite(unittest.TestCase):
    def test_rewrites_only_the_handle(self):
        root = Path(tempfile.mkdtemp())
        for name in th.FILES:
            (root / name).parent.mkdir(parents=True, exist_ok=True)
            (root / name).write_text("untouched\n")
        (root / "config.yaml").write_text(f'    tiktok: "{th.CURRENT}"\n    snapchat: "pfeilbr"\n')
        (root / "content/about.ja.md").write_text(f'<a href="https://www.tiktok.com/@{th.CURRENT}">TikTok</a>\n')
        changed = th.rewrite(root)
        self.assertEqual(changed, ["config.yaml", "content/about.ja.md"])
        self.assertIn('tiktok: "pfeilbr"', (root / "config.yaml").read_text())
        self.assertIn("tiktok.com/@pfeilbr\"", (root / "content/about.ja.md").read_text())
        self.assertEqual(th.rewrite(root), [])

    def test_every_listed_file_names_the_current_handle(self):
        if f'tiktok: "{th.CURRENT}"' not in (th.REPO / "config.yaml").read_text():
            self.skipTest("already switched to @pfeilbr")
        for name in th.FILES:
            self.assertIn(th.CURRENT, (th.REPO / name).read_text(), name)


class Main(unittest.TestCase):
    def run_main(self, config, who):
        root = Path(tempfile.mkdtemp())
        (root / "config.yaml").write_text(config)
        th_repo, th_fetch, argv = th.REPO, th.fetch, sys.argv
        th.REPO, th.fetch, sys.argv = root, (lambda h: page(who)), ["tiktok_handle.py"]
        try:
            return th.main()
        finally:
            th.REPO, th.fetch, sys.argv = th_repo, th_fetch, argv

    def test_switched_and_still_bs(self):
        self.assertEqual(self.run_main('tiktok: "pfeilbr"', th.ACCOUNT_ID), 0)

    def test_switched_but_not_found_fails(self):
        self.assertEqual(self.run_main('tiktok: "pfeilbr"', None), 1)

    def test_switched_but_someone_else_fails(self):
        self.assertEqual(self.run_main('tiktok: "pfeilbr"', "123"), 1)

    def test_not_switched_and_unclaimed_is_quiet(self):
        self.assertEqual(self.run_main(f'tiktok: "{th.CURRENT}"', None), 0)


if __name__ == "__main__":
    unittest.main()
