import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rescue as r  # noqa: E402


class ScanTest(unittest.TestCase):
    def test_finds_markdown_and_html_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text('![x](https://a.example/1.png) <img class=x src="http://b.example/2.jpg">\n'
                                       '[not an image](https://c.example/) ![local](images/3.png)')
            old = r.REPO
            try:
                r.REPO = root
                found = r.remote_images(root)
            finally:
                r.REPO = old
        self.assertEqual(sorted(found), ["http://b.example/2.jpg", "https://a.example/1.png"])

    def test_non_ascii_urls_are_encoded_once(self):
        url = "http://h.example/app_—_bash_—_80×24.png"
        self.assertEqual(r.safe(url), "http://h.example/app_%E2%80%94_bash_%E2%80%94_80%C3%9724.png")
        self.assertEqual(r.safe(r.safe(url)), r.safe(url))

    def test_dead_hosts_are_dead_whatever_they_answer(self):
        self.assertTrue(r.is_dead("http://static-content-01.s3-website-us-east-1.amazonaws.com/x.png"))


class MapTest(unittest.TestCase):
    """The committed map only points at files that exist."""

    def test_rescued_files_exist(self):
        mapping = json.loads(r.MAP.read_text(encoding="utf-8"))
        for url, local in mapping.items():
            if local:
                self.assertTrue((r.REPO / "static" / local.lstrip("/")).exists(), url)

    def test_every_dead_host_url_is_mapped(self):
        mapping = json.loads(r.MAP.read_text(encoding="utf-8"))
        for url in r.remote_images():
            if r.host(url) in r.DEAD_HOSTS:
                self.assertIn(url, mapping)


if __name__ == "__main__":
    unittest.main()
