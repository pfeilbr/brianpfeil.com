#!/usr/bin/env python3
"""Check the built /media/ page and its data against tests/fixtures/media.yaml
(Instagram) and tests/fixtures/photos.yaml (the Google Photos categories).

/media/ is drawn in the browser from /data/media.json, the whitelisted payload
that partials/media-payload.html builds from data/media.yaml. So this checks
two things Hugo produced: the JSON (every field the viewer needs, and nothing
it must never have -- coordinates, a colour that isn't hex), and the page
shell in all nine languages (the viewer's translated strings, the empty
state, and no inline copy of the data).

It exists because the layout has already failed silently once: without
safeJS the lightbox's JSON payload rendered as a quoted string, the page
looked fine, and nothing opened.

    python3 check_layout.py --build               # build both ways and check
    python3 check_layout.py PUBLIC_DIR            # an already-built fixture site
    python3 check_layout.py PUBLIC_DIR --empty    # an already-built empty site

Standard library only, so it runs in the Hugo CI job without a venv.
Production HTML is minified with unquoted attributes, so this parses the HTML
rather than grepping for class="...".
"""

import json
import sys
from html.parser import HTMLParser
from pathlib import Path

LANGS = ["", "zh", "es", "pt", "fr", "de", "it", "ja", "ko"]

# What the fixture holds; kept here rather than parsed so this needs no YAML.
FIXTURE_ITEMS = 3
FIXTURE_MEDIA = 4  # the album has two
FIXTURE_BASE = "https://cdn.example.test/"

VIEWER_STRINGS = ("data-instagram", "data-likes", "data-with", "data-location", "data-music",
                  "data-archived", "data-reshare-other", "data-reshare-own", "data-count",
                  "data-untitled", "data-open", "data-error")


class MediaPage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cat_names: dict[str, str] = {}
        self._cat = None
        self.sections_nav = False
        self.tiles = 0
        self.empty_state = False
        self.inline_payload = False
        self.strings: dict[str, str] = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        if "media-tile" in classes:
            self.tiles += 1
        if tag == "p" and "media-empty" in classes:
            self.empty_state = True
        if tag == "script" and a.get("id") == "media-data":
            self.inline_payload = True
        if "media-strings" in classes:
            self.strings = {k: v or "" for k, v in a.items() if k.startswith("data-")}
        if tag == "nav" and "media-sections" in classes:
            self.sections_nav = True
        if tag == "li" and a.get("data-key"):
            self._cat = a["data-key"]

    def handle_data(self, data):
        if self._cat and data.strip():
            self.cat_names[self._cat] = data.strip()
            self._cat = None


def page_for(public: Path, lang: str) -> Path:
    return public / lang / "media" / "index.html" if lang else public / "media" / "index.html"


def check_shell(public: Path) -> list[str]:
    """What every language's page must carry, with or without data."""
    errors = []
    for lang in LANGS:
        path = page_for(public, lang)
        label = f"/{lang}/media/" if lang else "/media/"
        if not path.exists():
            errors.append(f"{label}: not built")
            continue
        html = path.read_text(encoding="utf-8")
        page = MediaPage()
        page.feed(html)
        if page.tiles:
            errors.append(f"{label}: {page.tiles} tiles in the HTML; they are drawn from the JSON")
        if page.inline_payload:
            errors.append(f"{label}: an inline #media-data payload; the page reads /data/media.json")
        if "/data/media.json" not in html:
            errors.append(f"{label}: does not load /data/media.json")
        # The empty state is in the shell, shown when there is nothing to draw.
        if not page.empty_state:
            errors.append(f"{label}: no empty-state message")
        for attr in VIEWER_STRINGS:
            if not page.strings.get(attr):
                errors.append(f"{label}: missing viewer string {attr}")
        if lang and ("Reshared post" in html or "Reshared reel" in html):
            errors.append(f"{label}: a reshare label fell back to English")
        if lang and "Archived post" in html:
            errors.append(f"{label}: data-archived fell back to English")
        if lang and page.strings.get("data-count", "").endswith(" posts"):
            errors.append(f"{label}: data-count fell back to English")
    return errors


def check_payload(public: Path) -> list[str]:
    errors = []
    path = public / "data" / "media.json"
    if not path.exists():
        return ["/data/media.json: not published"]
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"/data/media.json: not JSON: {exc}"]
    if not isinstance(data, dict):
        return [f"/data/media.json: decoded to {type(data).__name__}, expected object"]

    posts, media = data.get("posts") or [], data.get("media") or []
    if data.get("base") != FIXTURE_BASE:
        errors.append(f"payload base is {data.get('base')!r}")
    if len(posts) != FIXTURE_ITEMS:
        errors.append(f"payload has {len(posts)} posts, expected {FIXTURE_ITEMS}")
    if len(media) != FIXTURE_MEDIA:
        errors.append(f"payload has {len(media)} media, expected {FIXTURE_MEDIA}")
    # Every media row must point at a real post and carry both kinds right.
    for row in media:
        if not (isinstance(row, dict) and 0 <= row.get("i", -1) < len(posts)
                and row.get("k") in ("p", "v") and row.get("s") and row.get("t")):
            errors.append(f"bad media row {row!r}")
            break
    if any("://" in str(row.get(k, "")) for row in media for k in ("s", "t", "p")):
        errors.append("media rows repeat the CDN address")
    if sum(1 for row in media if row.get("k") == "v" and not row.get("p")):
        errors.append("a video row has no poster")
    # The grid needs a year and kind per post.
    for p in posts:
        if not p.get("year") or p.get("kind") not in ("photo", "video", "album"):
            errors.append(f"post {p.get('id')} has no year or kind")
            break
    # Post details: carried for the post that has them...
    album = next((p for p in posts if p.get("id") == "20230101-bbbb2222"), {})
    want = {"url": "https://www.instagram.com/p/bbbb2222/", "loc": "Somewhere Nice",
            "locId": "12345", "likes": 12, "comments": 3, "tagged": ["friend", "other"]}
    for key, value in want.items():
        if album.get(key) != value:
            errors.append(f"post detail {key} is {album.get(key)!r}, want {value!r}")
    # ...but never coordinates, even though the data file has them.
    if any(k in p for p in posts for k in ("lat", "lng")) or "39.9488" in text:
        errors.append("coordinates reached /data/media.json")
    # Grid tiles: the video has both sizes, its colour and its length; the
    # malformed colour is dropped rather than passed to the page.
    video = next((r for r in media if r.get("k") == "v"), {})
    if video.get("g") != ["instagram/a/v-g360.webp", "instagram/a/v-g720.webp"]:
        errors.append(f"grid tiles missing: {video.get('g')!r}")
    if video.get("c") != "#1a2b3c":
        errors.append(f"tile colour is {video.get('c')!r}")
    if video.get("d") != 2:
        errors.append(f"video length is {video.get('d')!r}, want 2")
    if "evil.example" in text:
        errors.append("a malformed colour reached the payload")
    # The fixture's video had no sound and was given a track.
    if video.get("m") != "Sunlit":
        errors.append("added music not carried in the payload")
    # The hostile caption is data: jsonify escapes "<", so the raw tag
    # appears nowhere, and the page sets captions as text.
    if "</script><img" in text:
        errors.append("hostile caption stored unescaped")
    if not any("<img src=x" in (p.get("caption") or "") for p in posts):
        errors.append("hostile caption was altered rather than kept as text")
    if not any(p.get("story") for p in posts):
        errors.append("story not flagged in the payload")
    if not any(p.get("reshare") == "other_post" for p in posts):
        errors.append("reshare not carried in the payload")
    if not any(p.get("archived") for p in posts):
        errors.append("archived post not flagged in the payload")
    return errors


ENGLISH_CATS = {"skiing": "Skiing", "beach": "Beach"}


def check_photos(public: Path) -> list[str]:
    """The category half: its payload, and its names in every language."""
    errors = []
    path = public / "data" / "photos.json"
    if not path.exists():
        return ["/data/photos.json: not published"]
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    if data.get("categories") != ["skiing", "beach"]:
        errors.append(f"photos categories are {data.get('categories')!r}")
    posts, media = data.get("posts") or [], data.get("media") or []
    if [p.get("cat") for p in posts] != ["skiing", "beach"]:
        errors.append("photos posts lost their category")
    if len(media) != 2 or any(not (0 <= r.get("i", -1) < len(posts)) for r in media):
        errors.append(f"bad photos media rows {media!r}")
    video = next((r for r in media if r.get("k") == "v"), {})
    if video.get("p") != "photos/20250301-gaaaa111111/v-p.jpg" or video.get("d") != 15 or video.get("m") != "Sunlit":
        errors.append(f"photos video row incomplete: {video!r}")
    for leak in ("should not ship", "Secret Place", "40.1234", "AF1QipSECRETKEY"):
        if leak in text:
            errors.append(f"/data/photos.json leaks {leak!r}")
    for lang in LANGS:
        label = f"/{lang}/media/" if lang else "/media/"
        page = MediaPage()
        page.feed(page_for(public, lang).read_text(encoding="utf-8"))
        if not page.sections_nav:
            errors.append(f"{label}: no section nav")
        if set(page.cat_names) != {"skiing", "beach"}:
            errors.append(f"{label}: category names {page.cat_names!r}")
        elif lang and page.cat_names == ENGLISH_CATS:
            errors.append(f"{label}: category names fell back to English")
        for attr in ("data-instagram-label", "data-photos-note"):
            if not page.strings.get(attr):
                errors.append(f"{label}: missing {attr}")
    return errors


def check_populated(public: Path) -> list[str]:
    return check_shell(public) + check_payload(public) + check_photos(public)


def check_empty(public: Path) -> list[str]:
    errors = check_shell(public)
    path = public / "data" / "media.json"
    if path.exists() and (json.loads(path.read_text(encoding="utf-8")).get("posts") or []):
        errors.append("/data/media.json has posts with no data file")
    if (public / "data" / "photos.json").exists():
        errors.append("/data/photos.json published with no data file")
    return errors


def build_and_check() -> int:
    """Build the site twice — with the fixture, then with no data — and check both.

    The real data/media.yaml, if there is one, is moved aside for the
    duration and always put back, so this is safe to run in a working copy.
    """
    import shutil
    import subprocess
    import tempfile

    repo = Path(__file__).resolve().parents[3]
    fixtures = Path(__file__).resolve().parent / "fixtures"
    names = ("media.yaml", "photos.yaml")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        stashed = []
        for name in names:
            real = repo / "data" / name
            if real.exists():
                shutil.move(real, tmp / f"{name}.real")
                stashed.append(name)
        try:
            results = []
            for mode in ("fixture", "empty"):
                for name in names:
                    target = repo / "data" / name
                    if mode == "fixture":
                        shutil.copy(fixtures / name, target)
                    elif target.exists():
                        target.unlink()
                out = tmp / f"public-{mode}"
                subprocess.run(["hugo", "--minify", "--quiet", "-d", str(out)],
                               cwd=repo, check=True)
                errors = check_empty(out) if mode == "empty" else check_populated(out)
                results.append((mode, errors))
        finally:
            for name in names:
                target = repo / "data" / name
                if target.exists():
                    target.unlink()
                if name in stashed:
                    shutil.move(tmp / f"{name}.real", target)

    failed = False
    for mode, errors in results:
        if errors:
            failed = True
            print(f"FAIL ({mode}):")
            for e in errors:
                print(f"  {e}")
        else:
            print(f"ok ({mode}): /media/ correct in all {len(LANGS)} languages")
    return 1 if failed else 0


def main() -> int:
    if "--build" in sys.argv[1:]:
        return build_and_check()
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    public = Path(sys.argv[1])
    empty = "--empty" in sys.argv[2:]

    errors = check_empty(public) if empty else check_populated(public)
    mode = "empty state" if empty else "fixture"
    if errors:
        print(f"FAIL ({mode}):")
        for e in errors:
            print(f"  {e}")
        return 1
    print(f"ok ({mode}): /media/ correct in all {len(LANGS)} languages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
