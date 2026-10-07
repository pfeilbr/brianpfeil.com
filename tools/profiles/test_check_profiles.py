import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_profiles as cp  # noqa: E402


def links(keys, urls=cp.PROFILES):
    return "".join(f"<a href={urls[k]}>{k}</a>" for k in keys)


def home(keys=cp.PROFILES, same=cp.SAME_AS, foot=cp.FOOTER):
    ld = json.dumps({"@graph": [{"@type": "Person", "sameAs": [same[k] for k in same]}]})
    return (f"<script type=application/ld+json>{ld}</script>"
            f"<div>{links(keys)}</div><footer>{links(foot)}</footer>")


class CheckProfiles(unittest.TestCase):
    def build(self, about=None, home_html=None):
        root = Path(tempfile.mkdtemp())
        for lang in cp.LANGS:
            base = root / ("" if lang == "en" else lang)
            (base / "about").mkdir(parents=True)
            (base / "about" / "index.html").write_text(about or links(cp.PROFILES))
            (base / "index.html").write_text(home_html or home())
        return root

    def test_complete_site_passes(self):
        self.assertEqual(cp.check(self.build()), [])

    def test_about_missing_profile(self):
        keys = [k for k in cp.PROFILES if k != "snapchat"]
        errors = cp.check(self.build(about=links(keys)))
        self.assertEqual(len(errors), len(cp.LANGS))
        self.assertTrue(all("snapchat" in e for e in errors))

    def test_footer_link_does_not_count_for_hero(self):
        keys = [k for k in cp.PROFILES if k != "youtube"]
        errors = cp.check(self.build(home_html=home(keys=keys)))
        self.assertTrue(any("hero: no link to youtube" in e for e in errors))

    def test_same_as_missing(self):
        same = {k: v for k, v in cp.SAME_AS.items() if k != "pinterest"}
        errors = cp.check(self.build(home_html=home(same=same)))
        self.assertTrue(any("sameAs: missing pinterest" in e for e in errors))

    def test_footer_missing(self):
        errors = cp.check(self.build(home_html=home(foot=("x", "github"))))
        self.assertIn("footer: no link to youtube (https://www.youtube.com/@pfeilbr)", errors)

    def test_unbuilt_site(self):
        self.assertTrue(cp.check(Path(tempfile.mkdtemp())))


if __name__ == "__main__":
    unittest.main()
