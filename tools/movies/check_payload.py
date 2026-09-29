#!/usr/bin/env python3
"""Check the per-language movie files a build publishes for /movies/.

partials/publish-data.html writes /data/movies.json (every language) and
/data/movies.<lang>.json for each of the nine sites, with titles, genres and
synopses cut to that language and English. The page loads only the second,
so a missing file blanks /movies/ in that language and a stale field shows
the wrong thing. This checks, against a built site:

  - each language file exists and lists the same movies, in the same order;
  - its language maps hold only en and that language, with the same values;
  - every other field is identical to the full file;
  - the /movies/ page for each language asks for its own file.

    python3 tools/movies/check_payload.py --public public

Exit status 1 on any problem. Standard library only.
"""

import argparse
import json
import re
import sys
from pathlib import Path

LANGS = ("en", "zh", "es", "pt", "fr", "de", "it", "ja", "ko")
CUT = ("titles", "genres", "synopsis")
# The minifier renames the language variable, so match the shape only.
FETCH = re.compile(r'"/data/movies\."\s*\+\s*\w+\s*\+\s*"\.json"')


def check(full: dict, slim: dict, lang: str) -> list[str]:
    errors = []
    if len(full["movies"]) != len(slim["movies"]):
        return [f"{lang}: {len(slim['movies'])} movies, full file has {len(full['movies'])}"]
    for key in full:
        if key != "movies" and full[key] != slim.get(key):
            errors.append(f"{lang}: top-level {key} differs")
    keep = {"en", lang}
    for a, b in zip(full["movies"], slim["movies"]):
        name = a.get("imdb") or a.get("title")
        if set(a) != set(b):
            errors.append(f"{lang} {name}: fields differ")
            continue
        for key, value in a.items():
            if key in CUT and isinstance(value, dict):
                want = {k: v for k, v in value.items() if k in keep}
                if b[key] != want:
                    errors.append(f"{lang} {name}: {key} is not cut to {sorted(keep)}")
            elif b[key] != value:
                errors.append(f"{lang} {name}: {key} differs")
    return errors


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", default="public")
    args = ap.parse_args(argv)
    public = Path(args.public)
    full = json.loads((public / "data" / "movies.json").read_text(encoding="utf-8"))
    errors = []
    for lang in LANGS:
        path = public / "data" / f"movies.{lang}.json"
        if not path.exists():
            errors.append(f"{lang}: no {path}")
            continue
        errors += check(full, json.loads(path.read_text(encoding="utf-8")), lang)
        page = public / ("" if lang == "en" else lang) / "movies" / "index.html"
        if page.exists() and not FETCH.search(page.read_text(encoding="utf-8")):
            errors.append(f"{lang}: /movies/ does not load its own file")
    for e in errors[:40]:
        print(e)
    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        return 1
    print(f"ok: /data/movies.<lang>.json matches movies.json in all {len(LANGS)} languages")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
