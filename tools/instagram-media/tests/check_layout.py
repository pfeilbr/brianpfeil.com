#!/usr/bin/env python3
"""Check the rendered /media/ page against tests/fixtures/media.yaml.

Hugo templates have no unit tests, so this reads what Hugo actually produced.
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


class MediaPage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tiles: list[dict] = []
        self.empty = False
        self.payload: str | None = None
        self._in_payload = False
        self._in_empty = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        if "media-tile" in classes:
            self.tiles.append({"tag": tag, **a})
        if tag == "p" and "media-empty" in classes:
            self._in_empty = True
        if tag == "script" and a.get("id") == "media-data":
            self._in_payload = True
            self.payload = ""

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_payload = False
        if tag == "p":
            self._in_empty = False

    def handle_data(self, data):
        if self._in_payload:
            self.payload += data
        if self._in_empty and data.strip():
            self.empty = True


def page_for(public: Path, lang: str) -> Path:
    return public / lang / "media" / "index.html" if lang else public / "media" / "index.html"


def check_populated(public: Path) -> list[str]:
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

        if len(page.tiles) != FIXTURE_ITEMS:
            errors.append(f"{label}: {len(page.tiles)} tiles, expected {FIXTURE_ITEMS}")
        for tile in page.tiles:
            # Links, not buttons, so the grid works with JavaScript off.
            if tile["tag"] != "a" or not (tile.get("href") or "").startswith(FIXTURE_BASE):
                errors.append(f"{label}: tile is not a link to the CDN: {tile}")
                break

        if page.payload is None:
            errors.append(f"{label}: no #media-data payload")
        else:
            try:
                data = json.loads(page.payload)
            except json.JSONDecodeError as exc:
                errors.append(f"{label}: payload is not JSON: {exc}")
                data = None
            # The safeJS regression: valid JSON, but a string, not a list.
            if data is not None and not isinstance(data, list):
                errors.append(f"{label}: payload decoded to {type(data).__name__}, expected list"
                              " (missing safeJS?)")
            elif isinstance(data, list) and len(data) != FIXTURE_MEDIA:
                errors.append(f"{label}: payload has {len(data)} entries, expected {FIXTURE_MEDIA}")

        # The hostile caption must not survive as markup anywhere on the page:
        # jsonify escapes "<" as a unicode escape in the payload, and the
        # aria-label is entity-escaped, so the raw tag should appear nowhere.
        if "</script><img" in html:
            errors.append(f"{label}: hostile caption rendered unescaped")

        if page.empty:
            errors.append(f"{label}: shows the empty state despite having items")
    return errors


def check_empty(public: Path) -> list[str]:
    errors = []
    for lang in LANGS:
        path = page_for(public, lang)
        label = f"/{lang}/media/" if lang else "/media/"
        if not path.exists():
            errors.append(f"{label}: not built")
            continue
        page = MediaPage()
        page.feed(path.read_text(encoding="utf-8"))
        if not page.empty:
            errors.append(f"{label}: no empty-state message")
        if page.tiles or page.payload is not None:
            errors.append(f"{label}: renders tiles or a payload with no data")
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
    data = repo / "data" / "media.yaml"
    fixture = Path(__file__).resolve().parent / "fixtures" / "media.yaml"

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        stash = tmp / "media.yaml.real"
        had_real = data.exists()
        if had_real:
            shutil.move(data, stash)
        try:
            results = []
            for mode, source in (("fixture", fixture), ("empty", None)):
                if source:
                    shutil.copy(source, data)
                elif data.exists():
                    data.unlink()
                out = tmp / f"public-{mode}"
                subprocess.run(["hugo", "--minify", "--quiet", "-d", str(out)],
                               cwd=repo, check=True)
                errors = check_empty(out) if mode == "empty" else check_populated(out)
                results.append((mode, errors))
        finally:
            if data.exists():
                data.unlink()
            if had_real:
                shutil.move(stash, data)

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
