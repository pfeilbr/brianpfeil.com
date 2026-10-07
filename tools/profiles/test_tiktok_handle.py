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


if __name__ == "__main__":
    unittest.main()
