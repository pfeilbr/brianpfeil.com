"""Tests for check_i18n.py against small fixture language files."""

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_i18n as c  # noqa: E402

EN = '''
[greeting]
other = "Hello there, welcome to the site"

[count]
other = "{{ .count }} posts"

[brand]
other = "AWS Community Builder (Serverless)"

[apples]
one = "one apple"
other = "{{ . }} apples"
'''


def translated(**overrides) -> str:
    values = {
        "greeting": "こんにちは、サイトへようこそ",
        "count": "{{ .count }} 件",
        "brand": "AWS Community Builder (Serverless)",  # same everywhere, on purpose
        "apples": "{{ . }} 個",
    }
    values.update(overrides)
    return "\n".join(f'[{k}]\nother = "{v}"\n' for k, v in values.items() if v is not None)


class FilesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        (self.dir / "en.toml").write_text(EN, encoding="utf-8")
        for lang in c.LANGS:
            (self.dir / f"{lang}.toml").write_text(translated(), encoding="utf-8")

    def errors(self):
        return c.check_files(self.dir)

    def set_lang(self, lang, **overrides):
        (self.dir / f"{lang}.toml").write_text(translated(**overrides), encoding="utf-8")

    def test_consistent_files_pass(self):
        self.assertEqual(self.errors(), [])

    def test_missing_key(self):
        self.set_lang("ja", greeting=None)
        self.assertIn("ja: [greeting] missing (would render in English)", self.errors())

    def test_empty_value(self):
        self.set_lang("ko", greeting="")
        self.assertIn("ko: [greeting] is empty (Hugo falls back to English)", self.errors())

    def test_whitespace_only_counts_as_empty(self):
        self.set_lang("ko", greeting="   ")
        self.assertIn("ko: [greeting] is empty (Hugo falls back to English)", self.errors())

    def test_stale_key(self):
        (self.dir / "fr.toml").write_text(translated() + '\n[old_name]\nother = "x"\n',
                                          encoding="utf-8")
        self.assertIn("fr: [old_name] is not in en.toml (stale?)", self.errors())

    def test_dropped_placeholder(self):
        self.set_lang("de", count="Beiträge")
        self.assertIn("de: [count] drops .count", self.errors())

    def test_reordered_placeholder_is_fine(self):
        self.set_lang("ko", count="게시물 {{ .count }}개")
        self.assertEqual(self.errors(), [])

    def test_missing_language_file(self):
        (self.dir / "it.toml").unlink()
        self.assertIn("it: i18n/it.toml is missing", self.errors())

    def test_plural_tables_use_the_other_form(self):
        self.assertEqual(c.load("en", self.dir)["apples"], "{{ . }} apples")


class RenderedTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.i18n = root / "i18n"
        self.i18n.mkdir()
        (self.i18n / "en.toml").write_text(EN, encoding="utf-8")
        for lang in c.LANGS:
            (self.i18n / f"{lang}.toml").write_text(translated(), encoding="utf-8")
        self.public = root / "public"

    def page(self, lang, body):
        path = self.public / lang / "about" / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"<html><body>{body}</body></html>", encoding="utf-8")

    def test_english_fallback_on_a_translated_page_is_caught(self):
        self.page("ja", "<p>Hello there, welcome to the site</p>")
        errors = c.check_rendered(self.public, self.i18n)
        self.assertEqual(len(errors), 1)
        self.assertIn("ja: /ja/about/index.html shows English [greeting]", errors[0])

    def test_entity_encoded_english_is_still_caught(self):
        self.page("es", "<p>Hello there, welcome to the site</p>".replace(",", "&#44;"))
        self.assertEqual(len(c.check_rendered(self.public, self.i18n)), 1)

    def test_a_string_identical_in_every_language_is_allowed(self):
        self.page("zh", "<p>AWS Community Builder (Serverless)</p>")
        self.assertEqual(c.check_rendered(self.public, self.i18n), [])

    def test_translated_page_passes(self):
        self.page("ja", "<p>こんにちは、サイトへようこそ</p>")
        self.assertEqual(c.check_rendered(self.public, self.i18n), [])


if __name__ == "__main__":
    unittest.main()
