import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import indexnow as ix  # noqa: E402

SITE = "https://example.com"


def page(title="T", desc="d", main="<p>hi</p>", css="main.abc123.css"):
    return (f'<html><head><title>{title}</title><meta name=description content="{desc}">'
            f'<link rel=stylesheet href=/{css}></head><body><nav>nav</nav>'
            f'<main id=main-content>{main}</main><footer>f</footer></body></html>')


class HashTest(unittest.TestCase):
    def test_chrome_changes_do_not_count(self):
        self.assertEqual(ix.page_hash(page(css="main.aaa.css")), ix.page_hash(page(css="main.bbb.css")))
        self.assertEqual(ix.page_hash(page()), ix.page_hash(page().replace("<nav>nav</nav>", "<nav>new</nav>")))

    def test_content_title_and_description_count(self):
        base = ix.page_hash(page())
        self.assertNotEqual(base, ix.page_hash(page(main="<p>changed</p>")))
        self.assertNotEqual(base, ix.page_hash(page(title="New")))
        self.assertNotEqual(base, ix.page_hash(page(desc="new")))

    def test_page_without_main_is_hashed_whole(self):
        self.assertNotEqual(ix.page_hash("<p>a</p>"), ix.page_hash("<p>b</p>"))


class ManifestTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.pub = Path(self.tmp.name)
        files = {
            "index.html": page(),
            "about/index.html": page(title="About"),
            "courses/x/lessons/0001.html": "<html><body>lesson</body></html>",
            "404.html": page(title="Not found"),
            "old/index.html": '<html><head><meta http-equiv="refresh" content="0; url=/new/"></head></html>',
            "data/x.json": "{}",
        }
        for rel, text in files.items():
            (self.pub / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.pub / rel).write_text(text)

    def tearDown(self):
        self.tmp.cleanup()

    def test_urls(self):
        m = ix.manifest(self.pub, SITE)
        self.assertEqual(sorted(m), [
            "https://example.com/", "https://example.com/about/",
            "https://example.com/courses/x/lessons/0001.html"])

    def test_changed(self):
        new = ix.manifest(self.pub, SITE)
        self.assertEqual(ix.changed(new, new), [])
        old = dict(new)
        old["https://example.com/about/"] = "stale"
        del old["https://example.com/"]
        self.assertEqual(ix.changed(new, old), ["https://example.com/", "https://example.com/about/"])


class PayloadTest(unittest.TestCase):
    def test_batches_and_key_location(self):
        cfg = {"site": "https://example.com", "key": "k" * 32, "endpoint": "x"}
        bodies = ix.payloads([f"https://example.com/{i}" for i in range(10_001)], cfg)
        self.assertEqual([len(b["urlList"]) for b in bodies], [10_000, 1])
        self.assertEqual(bodies[0]["host"], "example.com")
        self.assertEqual(bodies[0]["keyLocation"], "https://example.com/" + "k" * 32 + ".txt")


class SubmitTest(unittest.TestCase):
    def test_nothing_to_submit_is_success(self):
        self.assertEqual(ix.submit([], {"site": "https://example.com", "key": "k", "endpoint": "x"}), 0)

    def test_refusal_to_verify_is_retry(self):
        import io
        from unittest import mock
        err = ix.urllib.error.HTTPError("x", 403, "Forbidden", {}, io.BytesIO(b"{}"))
        cfg = {"site": "https://example.com", "key": "k", "endpoint": "https://api.example/indexnow"}
        with mock.patch.object(ix.urllib.request, "urlopen", side_effect=err):
            self.assertEqual(ix.submit(["https://example.com/"], cfg), ix.RETRY)


class PlanTest(unittest.TestCase):
    def test_previous_file_wins_over_live(self):
        import json
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp:
            pub = Path(tmp) / "public"
            (pub / "a").mkdir(parents=True)
            (pub / "a" / "index.html").write_text(page())
            prev = Path(tmp) / "prev.json"
            prev.write_text(json.dumps({"pages": ix.manifest(pub, "https://brianpfeil.com")}))
            out = Path(tmp) / "changed.txt"
            with mock.patch.object(ix, "fetch_previous", side_effect=AssertionError("should not fetch")):
                ix.main(["plan", str(pub), "--out", str(out), "--previous-file", str(prev)])
            self.assertEqual(out.read_text(), "")
            self.assertTrue((pub / "indexnow-manifest.json").exists())


class ConfigTest(unittest.TestCase):
    def test_key_file_is_published(self):
        key = ix.CONFIG["key"]
        self.assertRegex(key, r"^[0-9a-f]{32}$")
        key_file = Path(__file__).resolve().parents[2] / "static" / f"{key}.txt"
        self.assertEqual(key_file.read_text(), key)


if __name__ == "__main__":
    unittest.main()
