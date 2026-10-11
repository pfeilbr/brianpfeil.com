import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_profiles as cp  # noqa: E402


def links(keys, urls=cp.PROFILES):
    return "".join(f"<a href={urls[k]}>{k}</a>" for k in keys)


def copies(place, skip=()):
    return "".join(f"<button data-copy={h}>{k}</button>"
                   for k, (h, where) in cp.HANDLES.items() if place in where and k not in skip)


def tel(place, skip=()):
    return "" if place in skip else f"<a href=tel:{cp.PHONE}>call</a>"


def home(keys=cp.HERO, same=cp.SAME_AS, foot=cp.FOOTER, skip=(), phone=cp.PHONE):
    ld = json.dumps({"@graph": [{"@type": "Person", "telephone": phone,
                                 "sameAs": [same[k] for k in same]}]})
    return (f"<script type=application/ld+json>{ld}</script>"
            f"<div>{links(keys)}{copies('hero', skip)}{tel('hero', skip)}</div>"
            f"<footer>{links(foot)}{copies('footer', skip)}{tel('footer', skip)}</footer>")


def about_page(keys=cp.PROFILES, skip=()):
    return links(keys) + copies("about", skip) + tel("about", skip)


class CheckProfiles(unittest.TestCase):
    def build(self, about=None, home_html=None):
        root = Path(tempfile.mkdtemp())
        for lang in cp.LANGS:
            base = root / ("" if lang == "en" else lang)
            (base / "about").mkdir(parents=True)
            (base / "about" / "index.html").write_text(about or about_page())
            (base / "index.html").write_text(home_html or home())
        return root

    def test_complete_site_passes(self):
        self.assertEqual(cp.check(self.build()), [])

    def test_about_missing_profile(self):
        keys = [k for k in cp.PROFILES if k != "snapchat"]
        errors = cp.check(self.build(about=about_page(keys)))
        self.assertEqual(len(errors), len(cp.LANGS))
        self.assertTrue(all("snapchat" in e for e in errors))

    def test_footer_link_does_not_count_for_hero(self):
        keys = [k for k in cp.HERO if k != "youtube"]
        errors = cp.check(self.build(home_html=home(keys=keys)))
        self.assertTrue(any("hero: no link to youtube" in e for e in errors))

    def test_hero_needs_only_the_professional_four(self):
        self.assertEqual(cp.HERO, ("github", "linkedin", "x", "youtube"))
        errors = cp.check(self.build(home_html=home(keys=cp.HERO)))
        self.assertFalse(any("hero" in e for e in errors), errors)

    def test_same_as_missing(self):
        same = {k: v for k, v in cp.SAME_AS.items() if k != "pinterest"}
        errors = cp.check(self.build(home_html=home(same=same)))
        self.assertTrue(any("sameAs: missing pinterest" in e for e in errors))

    def test_footer_missing(self):
        errors = cp.check(self.build(home_html=home(foot=("x", "github"))))
        self.assertIn("footer: no link to youtube (https://www.youtube.com/@pfeilbr)", errors)

    def test_wechat_copy_button_missing(self):
        errors = cp.check(self.build(about=about_page(skip=("wechat",)),
                                     home_html=home(skip=("wechat",))))
        self.assertIn("/en/about/: no wechat copy button", errors)
        self.assertFalse(any("hero: no wechat" in e for e in errors))
        self.assertIn("footer: no wechat copy button", errors)
        self.assertFalse(any("discord" in e for e in errors))

    def test_quoted_copy_attribute_counts(self):
        self.assertNotIn("wechat", cp.no_copy('<button data-copy="methym00">', "about"))
        self.assertIn("wechat", cp.no_copy("<button data-copy=methym00x>", "about"))

    def test_phone_missing(self):
        errors = cp.check(self.build(about=about_page(skip=("about",)),
                                     home_html=home(skip=("hero", "footer"), phone="")))
        self.assertIn("/en/about/: no phone link", errors)
        self.assertFalse(any("hero: no phone" in e for e in errors))
        self.assertIn("footer: no phone link", errors)
        self.assertIn("/fr/ JSON-LD: telephone is '', not +12158722791", errors)

    def test_hero_without_phone_passes(self):
        errors = cp.check(self.build(home_html=home(skip=("hero",))))
        self.assertEqual(errors, [])

    def test_quoted_tel_counts(self):
        self.assertTrue(cp.has_tel('<a href="tel:+12158722791">'))
        self.assertTrue(cp.has_tel('<a href="tel:&#43;12158722791" title=x>'))
        self.assertFalse(cp.has_tel("<a href=tel:+121587227910>"))

    def test_unbuilt_site(self):
        self.assertTrue(cp.check(Path(tempfile.mkdtemp())))


if __name__ == "__main__":
    unittest.main()
