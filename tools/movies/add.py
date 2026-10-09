#!/usr/bin/env python3
"""Add movies to data/movies.json by IMDb id, then fill them in.

  python3 tools/movies/add.py tt0120601 "tt0335266:Lost in Translation:2003" ...

Each argument is an IMDb id, optionally with ":title:year" so the file stays
readable before the refresh runs. Ids already on the page are skipped, new
ones are appended (page order = file order) and only they are refreshed, so
re-running with the same ids is a no-op.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refresh  # noqa: E402


def parse(arg):
    imdb, _, rest = arg.partition(":")
    title, _, year = rest.rpartition(":") if rest.count(":") else (rest, "", "")
    entry = {"title": title or imdb, "imdb": imdb}
    if year.isdigit():
        entry["year"] = int(year)
    return entry


def append(doc, entries):
    have = {m.get("imdb") for m in doc["movies"]}
    new = [e for e in entries if e["imdb"] not in have and not have.add(e["imdb"])]
    doc["movies"].extend(new)
    return [e["imdb"] for e in new]


def main(argv):
    doc = json.loads(refresh.DATA.read_text())
    ids = append(doc, [parse(a) for a in argv])
    if not ids:
        print("nothing new")
        return 0
    refresh.DATA.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
    print(f"added {len(ids)}; refreshing them")
    return refresh.main(ids)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
