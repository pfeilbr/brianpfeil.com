#!/usr/bin/env python3
"""Build the site with a fixture /ai/ data file, and with none, and check what
Hugo produced in all nine languages:

- /data/ai.json and /data/ai-digests.json are published;
- each language's /ai/ page has the shell the script fills (briefing,
  search, people, seven tabs, sources) and describes itself with that
  language's briefing headline;
- each language's /ai/index.xml carries the briefing in that language,
  with its sources linked;
- the home page's AI card shows the headline;
- with no data at all the page and feed still build, empty.

    python3 tools/ai-radar/check_page.py --build

The real data/ai.json and data/ai-digests.json are moved aside for the
build and always put back. Standard library only.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANGS = ["en", "zh", "es", "pt", "fr", "de", "it", "ja", "ko"]
NAMES = ("ai.json", "ai-digests.json")
SHELL_IDS = ("ai-briefing", "ai-briefing-points", "ai-q", "ai-topic-chips", "ai-people", "ai-sources", "ai-stamp")
TABS = ("latest", "labs", "models", "tools", "community", "learning", "mine")


def headline(lang):
    return "Fixture headline %s" % lang.upper()


def fixture():
    now = "2026-09-26T10:00:00Z"
    digest = {
        "date": "2026-09-26", "generated": now, "model": "claude-opus-5",
        "lang": {l: {"headline": headline(l), "points": [{"text": "Point one %s" % l, "refs": ["a1"]}]} for l in LANGS},
        "refs": {"a1": {"title": "GPT-6 Luna", "url": "https://openai.com/luna", "source": "OpenAI"}},
    }
    doc = {
        "schema_version": 1, "generated": now, "window_days": 14,
        "sections": ["people", "labs", "tools", "community", "learning"],
        "sources": [{"id": "openai", "section": "labs", "name": "OpenAI", "home": "https://openai.com/news/", "status": "ok", "checked": now},
                    {"id": "simonw", "section": "people", "name": "Simon Willison", "home": "https://simonwillison.net/", "status": "ok", "checked": now}],
        "items": [{"id": "a1", "source": "openai", "section": "labs", "title": "GPT-6 Luna", "url": "https://openai.com/luna",
                   "published": now, "first_seen": now, "summary": "A model."}],
        "models": {"new": [], "trending": []}, "mine": [], "topics": [], "digest": digest,
    }
    return doc, {"schema_version": 1, "digests": [digest]}


def page(public, lang, *parts):
    base = public if lang == "en" else public / lang
    return base.joinpath(*parts)


def check(public, populated):
    errors = []
    for name in NAMES:
        p = public / "data" / name
        if populated and not p.exists():
            errors.append("missing /data/%s" % name)
    if populated:
        published = json.loads((public / "data" / "ai.json").read_text())
        if published.get("digest", {}).get("date") != "2026-09-26":
            errors.append("/data/ai.json lacks the fixture briefing")
    for lang in LANGS:
        html_path = page(public, lang, "ai", "index.html")
        if not html_path.exists():
            errors.append("%s: no /ai/ page" % lang)
            continue
        html = html_path.read_text()
        for i in SHELL_IDS:
            if not re.search(r'id="?%s"?[\s>]' % i, html):
                errors.append("%s: /ai/ lacks #%s" % (lang, i))
        for t in TABS:
            if not re.search(r'id="?panel-%s"?[\s>]' % t, html):
                errors.append("%s: /ai/ lacks the %s tab" % (lang, t))
        desc = re.search(r'<meta name="?description"? content="([^"]*)"', html)
        if populated and (not desc or desc.group(1) != headline(lang)):
            errors.append("%s: meta description is %r, not the briefing headline" % (lang, desc and desc.group(1)))
        rss_path = page(public, lang, "ai", "index.xml")
        if not rss_path.exists():
            errors.append("%s: no /ai/index.xml" % lang)
        else:
            rss = rss_path.read_text()
            items = rss.count("<item>")
            if populated and (items != 1 or headline(lang) not in rss or "https://openai.com/luna" not in rss):
                errors.append("%s: the feed does not carry the %s briefing with its source" % (lang, lang))
            if not populated and items:
                errors.append("%s: the feed has items with no data" % lang)
        if not re.search(r'type="?application/rss\+xml"?[^>]*/ai/index\.xml', html):
            errors.append("%s: /ai/ does not link its feed" % lang)
        home = page(public, lang, "index.html").read_text()
        if populated and headline(lang) not in home:
            errors.append("%s: the home page does not show the briefing headline" % lang)
    return errors


def build_and_check():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        stashed = []
        for name in NAMES:
            real = ROOT / "data" / name
            if real.exists():
                shutil.move(real, tmp / (name + ".real"))
                stashed.append(name)
        failed = False
        try:
            doc, arch = fixture()
            for mode in ("fixture", "empty"):
                for name, content in zip(NAMES, (doc, arch)):
                    target = ROOT / "data" / name
                    if mode == "fixture":
                        target.write_text(json.dumps(content))
                    elif target.exists():
                        target.unlink()
                out = tmp / ("public-" + mode)
                subprocess.run(["hugo", "--minify", "--quiet", "-d", str(out)], cwd=ROOT, check=True)
                errors = check(out, mode == "fixture")
                for e in errors:
                    print("FAIL (%s): %s" % (mode, e))
                if not errors:
                    print("ok (%s): /ai/ correct in all %d languages" % (mode, len(LANGS)))
                failed = failed or bool(errors)
        finally:
            for name in NAMES:
                target = ROOT / "data" / name
                if target.exists():
                    target.unlink()
            for name in stashed:
                shutil.move(tmp / (name + ".real"), ROOT / "data" / name)
    return 1 if failed else 0


if __name__ == "__main__":
    if "--build" in sys.argv:
        sys.exit(build_and_check())
    sys.exit(1 if [print(e) for e in check(Path(sys.argv[1]), True)] else 0)
