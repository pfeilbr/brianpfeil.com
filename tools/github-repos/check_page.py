#!/usr/bin/env python3
"""Render check for /github/ against a built site (hugo --minify first).

In all nine languages: the page shell is there, the translated strings the
script needs reached it with their {placeholders} intact, the data preload,
search module and structured data are in the head, and both the nav and the
home page link to it. /data/github.json is published and matches data/github.json.

    python3 tools/github-repos/check_page.py --public public
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANGS = ["en", "zh", "es", "pt", "fr", "de", "it", "ja", "ko"]


def check(public):
    errors = []
    pub = json.loads((public / "data" / "github.json").read_text())
    src = json.loads((ROOT / "data" / "github.json").read_text())
    if pub["count"] != src["count"] or len(pub["repos"]) != len(src["repos"]):
        errors.append("/data/github.json does not match data/github.json")
    for lang in LANGS:
        pre = public if lang == "en" else public / lang
        page = pre / "github" / "index.html"
        if not page.exists():
            errors.append(f"{lang}: github/index.html missing")
            continue
        html = page.read_text()
        for needle in ["gh-list", "panel-learn", "panel-timeline", "{shown}", "{total}", "data/github.json"]:
            if needle not in html:
                errors.append(f"{lang}: /github/ lacks {needle!r}")
        # Every area and path name is looked up per key; a missing one would
        # render as an empty chip. Minified JS drops the quotes on keys.
        for key in [a["key"] for a in src["areas"]]:
            if not re.search(r'(?:"%s"|\b%s):"[^"]+"' % (re.escape(key), re.escape(key)), html):
                errors.append(f"{lang}: area {key} has no label")
        # The data preload, the search module (fingerprinted, with SRI), the
        # structured data and this page's nav link.
        if not re.search(r'rel="?preload"? href="?/data/github\.json', html):
            errors.append(f"{lang}: /github/ does not preload /data/github.json")
        if not re.search(r'src="?/js/gh-search\.min\.[0-9a-f]{64}\.js"? integrity="?sha', html):
            errors.append(f"{lang}: /github/ lacks the fingerprinted search module")
        if "CollectionPage" not in html or "SoftwareSourceCode" not in html:
            errors.append(f"{lang}: /github/ lacks its CollectionPage structured data")
        nav = "/github/" if lang == "en" else f"/{lang}/github/"
        if not re.search(r'<nav[^>]*>.*?href="?%s' % re.escape(nav), html, re.S):
            errors.append(f"{lang}: nav does not link to {nav}")
        home = (pre / "index.html").read_text()
        href = "/github/" if lang == "en" else f"/{lang}/github/"
        if href not in home:
            errors.append(f"{lang}: home page does not link to {href}")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", default=str(ROOT / "public"))
    errors = check(Path(ap.parse_args().public))
    for e in errors:
        print("error:", e)
    print("ok: /github/ renders in all nine languages" if not errors else f"{len(errors)} problem(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
