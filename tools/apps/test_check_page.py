import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_page as cp  # noqa: E402

URL = "https://example.github.io/app/"
APP = {"key": "mandarin", "name": "Say It", "url": URL, "icon": "/images/apps/mandarin.webp"}
I18N = {lang: {"apps_blurb_mandarin": {"other": f"blurb {lang}"}} for lang in cp.LANGS}


def redirect(url: str = URL) -> str:
    return (f'<meta name="robots" content="noindex"><link rel="canonical" href="{url}">'
            f'<meta http-equiv="refresh" content="0; url={url}">'
            f"<script>location.replace({json.dumps(url)} + location.search)</script>")


class DataTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.static = Path(self.tmp.name)
        (self.static / "images" / "apps").mkdir(parents=True)
        (self.static / "images" / "apps" / "mandarin.webp").write_bytes(b"x")

    def tearDown(self):
        self.tmp.cleanup()

    def test_good_data_passes(self):
        self.assertEqual(cp.check_data({"apps": [APP]}, I18N, self.static), [])

    def test_key_must_be_a_lowercase_slug(self):
        errors = cp.check_data({"apps": [{**APP, "key": "Mandarin"}]}, I18N, self.static)
        self.assertTrue(any("lowercase" in e for e in errors))

    def test_duplicate_keys_fail(self):
        errors = cp.check_data({"apps": [APP, APP]}, I18N, self.static)
        self.assertTrue(any("duplicate" in e for e in errors))

    def test_missing_icon_fails(self):
        errors = cp.check_data({"apps": [{**APP, "icon": "/images/apps/nope.webp"}]}, I18N, self.static)
        self.assertTrue(any("icon" in e for e in errors))

    def test_missing_translation_fails(self):
        i18n = {**I18N, "ko": {}}
        errors = cp.check_data({"apps": [APP]}, i18n, self.static)
        self.assertEqual(errors, ["mandarin: no apps_blurb_mandarin in i18n/ko.toml"])

    def test_plain_http_fails(self):
        errors = cp.check_data({"apps": [{**APP, "url": "http://x/"}]}, I18N, self.static)
        self.assertTrue(any("https" in e for e in errors))


class RedirectTest(unittest.TestCase):
    def test_good_redirect_passes(self):
        self.assertEqual(cp.check_redirect(redirect(), URL), [])

    def test_redirect_to_another_app_fails(self):
        self.assertEqual(len(cp.check_redirect(redirect("https://other/"), URL)), 3)

    def test_indexable_redirect_fails(self):
        html = redirect().replace('<meta name="robots" content="noindex">', "")
        self.assertEqual(cp.check_redirect(html, URL), ["not noindex"])


class BuildTest(unittest.TestCase):
    def build(self, root: Path, *, home_link: bool = True, blurb: bool = True) -> None:
        (root / "data").mkdir(parents=True)
        (root / "data" / "apps.json").write_text(json.dumps({"apps": [APP]}))
        (root / "apps" / "mandarin").mkdir(parents=True)
        (root / "apps" / "mandarin" / "index.html").write_text(redirect())
        for lang in cp.LANGS:
            d = root / cp.prefix(lang)
            (d / "apps").mkdir(parents=True, exist_ok=True)
            text = f"blurb {lang}" if blurb else ""
            (d / "apps" / "index.html").write_text(f'<script>D.load("apps");var T={{"b":"{text}"}}</script>')
            link = f"<a href=/{cp.prefix(lang)}apps/ class=x>" if home_link else ""
            (d / "index.html").write_text(link)

    def test_complete_build_passes(self):
        with tempfile.TemporaryDirectory() as t:
            self.build(Path(t))
            self.assertEqual(cp.check_build(Path(t), {"apps": [APP]}, I18N), [])

    def test_untranslated_page_fails(self):
        with tempfile.TemporaryDirectory() as t:
            self.build(Path(t), blurb=False)
            errors = cp.check_build(Path(t), {"apps": [APP]}, I18N)
            self.assertEqual(len(errors), len(cp.LANGS))

    def test_missing_home_card_fails(self):
        with tempfile.TemporaryDirectory() as t:
            self.build(Path(t), home_link=False)
            errors = cp.check_build(Path(t), {"apps": [APP]}, I18N)
            self.assertTrue(all("home card" in e for e in errors) and errors)

    def test_missing_short_link_fails(self):
        with tempfile.TemporaryDirectory() as t:
            self.build(Path(t))
            (Path(t) / "apps" / "mandarin" / "index.html").unlink()
            self.assertIn("/apps/mandarin/ was not published", cp.check_build(Path(t), {"apps": [APP]}, I18N))


if __name__ == "__main__":
    unittest.main()
