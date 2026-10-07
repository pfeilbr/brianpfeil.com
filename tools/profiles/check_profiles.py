#!/usr/bin/env python3
"""Check that B's social profiles are linked everywhere they are listed.

The profiles live in four places that are edited by hand: the about page
(content/about.<lang>.md, nine copies), the home hero (data/home.yaml
`social`), the footer (config.yaml `params.author`) and the home page's
Person `sameAs` (partials/head-meta.html). Adding a network means touching
all four, so this checks a built site for every profile in each of them:

  - /about/ in every language links every profile;
  - the home page in every language links every profile from the hero and
    lists every one in the Person's sameAs;
  - the footer (read from the English home page) links FOOTER.

    python3 tools/profiles/check_profiles.py --public public

Exit status 1 on any problem. Standard library only.
"""

import argparse
import json
import re
import sys
from pathlib import Path

LANGS = ("en", "zh", "es", "pt", "fr", "de", "it", "ja", "ko")

PROFILES = {
    "github": "https://github.com/pfeilbr",
    "linkedin": "https://www.linkedin.com/in/brian-pfeil-175a011/",
    "instagram": "https://www.instagram.com/pfeilbr/",
    "x": "twitter.com/pfeilbr",
    "youtube": "https://www.youtube.com/@pfeilbr",
    "pinterest": "https://www.pinterest.com/pfeilbr/",
    "snapchat": "https://www.snapchat.com/@pfeilbr",
    "tiktok": "https://www.tiktok.com/@user8768514322831",
    "stackoverflow": "stackoverflow.com/users/29148/pfeilbr",
}
# The JSON-LD spells X as x.com; the links still use twitter.com.
SAME_AS = {**PROFILES, "x": "https://x.com/pfeilbr"}
FOOTER = ("x", "github", "stackoverflow", "youtube", "pinterest", "snapchat", "tiktok")

LD = re.compile(r'<script type="?application/ld\+json"?>(.*?)</script>', re.S)
FOOT = re.compile(r"<footer\b.*?</footer>", re.S)


def page(public: Path, lang: str, path: str) -> Path:
    return public / ("" if lang == "en" else lang) / path / "index.html"


def missing(html: str, keys, urls=PROFILES) -> list[str]:
    return [k for k in keys if urls[k] not in html]


def same_as(html: str) -> list[str]:
    for block in LD.findall(html):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        for node in data.get("@graph", []):
            if node.get("@type") == "Person":
                return node.get("sameAs") or []
    return []


def check(public: Path) -> list[str]:
    errors = []
    for lang in LANGS:
        about = page(public, lang, "about")
        home = page(public, lang, "")
        unbuilt = [f for f in (about, home) if not f.exists()]
        errors += [f"{f}: not built" for f in unbuilt]
        if unbuilt:
            continue
        for k in missing(about.read_text(), PROFILES):
            errors.append(f"/{lang}/about/: no link to {k} ({PROFILES[k]})")
        html = home.read_text()
        foot = FOOT.search(html)
        hero = LD.sub("", html[: foot.start()] if foot else html)
        for k in missing(hero, PROFILES):
            errors.append(f"/{lang}/ hero: no link to {k} ({PROFILES[k]})")
        sa = " ".join(same_as(html))
        for k in missing(sa, SAME_AS, SAME_AS):
            errors.append(f"/{lang}/ sameAs: missing {k} ({SAME_AS[k]})")
        if lang == "en":
            for k in missing(foot.group(0) if foot else "", FOOTER):
                errors.append(f"footer: no link to {k} ({PROFILES[k]})")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--public", type=Path, default=Path("public"))
    errors = check(ap.parse_args().public)
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    if errors:
        return 1
    print(f"ok: {len(PROFILES)} profiles linked on /about/, the home hero and sameAs in all {len(LANGS)} languages, and the footer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
