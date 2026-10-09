#!/usr/bin/env python3
"""Turn raw movie mentions into a list of films to pick from.

Input: one or more JSON files, each an array of mentions
  {"title", "year"?, "source", "evidence", "kind"?, "date"?}
gathered from wherever B wrote a movie down (Drafts, Dropbox notes, Gmail
receipts, ...). Each mention is matched to a JustWatch movie (title search,
year when the mention has one), mentions of the same film are merged, and
anything already in data/movies.json is dropped. The output is what the
picker page shows:

  {"imdb", "title", "year", "poster", "sources": [...], "evidence": [...],
   "kinds": [...], "first", "last", "query"}

Unmatched mentions are listed under "unmatched" so nothing disappears
silently. Lookups are cached in --cache, so re-runs are fast and stable.

  python3 tools/movies/candidates.py --out cand.json mentions/*.json
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refresh  # noqa: E402  (http + JustWatch helpers)

SEARCH = """
query($q: String!) {
  popularTitles(country: US, first: 10, filter: {searchQuery: $q, objectTypes: [MOVIE]}) {
    edges { node { id content(country: US, language: "en") {
      title originalReleaseYear posterUrl runtime externalIds { imdbId } } } }
  }
}"""


def norm(title):
    """Comparable form of a title: no accents, case, punctuation or a
    leading article ("The Goonies" == "goonies")."""
    t = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    t = t.lower().replace("&", "and")
    t = re.sub(r"\(\d{4}\)", "", t)
    t = re.sub(r"[^a-z0-9]+", " ", t).strip()
    return re.sub(r"^(the|a|an) ", "", t)


def pick(edges, title, year):
    """Best search hit: exact normalized title first (matching year if we
    have one, else the most popular), then a year match on a prefix."""
    want = norm(title)
    hits = [e["node"] for e in edges if e["node"]["content"]["externalIds"]["imdbId"]]
    exact = [n for n in hits if norm(n["content"]["title"]) == want]
    if year:
        for pool in (exact, hits):
            for n in pool:
                if abs((n["content"]["originalReleaseYear"] or 0) - year) <= 1:
                    if pool is exact or norm(n["content"]["title"]).startswith(want):
                        return n
    if exact:
        return exact[0]
    return None


def lookup(title, year, cache):
    key = f"{norm(title)}|{year or ''}"
    if key not in cache:
        edges = refresh.jw(SEARCH, {"q": title})["popularTitles"]["edges"]
        n = pick(edges, title, year)
        cache[key] = None if not n else {
            "imdb": n["content"]["externalIds"]["imdbId"],
            "title": n["content"]["title"],
            "year": n["content"]["originalReleaseYear"],
            "runtime": n["content"]["runtime"],
            "poster": ("https://images.justwatch.com" +
                       n["content"]["posterUrl"].replace("{profile}", "s166").replace("{format}", "jpg"))
            if n["content"].get("posterUrl") else None,
        }
    return cache[key]


def build(mentions, existing, cache):
    have_ids = {m.get("imdb") for m in existing}
    have_titles = {norm(m["title"]) for m in existing}
    films, unmatched = {}, []
    for m in mentions:
        hit = lookup(m["title"], m.get("year"), cache)
        if not hit:
            unmatched.append(m)
            continue
        if hit["imdb"] in have_ids or (norm(hit["title"]) in have_titles and not m.get("year")):
            continue
        f = films.setdefault(hit["imdb"], {**hit, "sources": [], "evidence": [],
                                           "kinds": [], "dates": [], "query": m["title"]})
        for k, v in (("sources", m["source"]), ("evidence", m.get("evidence")), ("kinds", m.get("kind"))):
            if v and v not in f[k]:
                f[k].append(v)
        if m.get("date"):
            f["dates"].append(m["date"])
    out = []
    for f in films.values():
        d = sorted(f.pop("dates"))
        f["first"], f["last"] = (d[0], d[-1]) if d else (None, None)
        out.append(f)
    out.sort(key=lambda f: (-len(f["evidence"]), f["title"].lower()))
    return out, unmatched


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cache", default="build/movie-candidates-cache.json")
    a = ap.parse_args(argv)
    cache_path = Path(a.cache)
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    mentions = [m for p in a.inputs for m in json.loads(Path(p).read_text())]
    existing = json.loads(refresh.DATA.read_text())["movies"]
    try:
        films, unmatched = build(mentions, existing, cache)
    finally:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, indent=1))
    Path(a.out).write_text(json.dumps({"films": films, "unmatched": unmatched}, indent=1))
    print(f"{len(mentions)} mentions -> {len(films)} new films, {len(unmatched)} unmatched")


if __name__ == "__main__":
    main(sys.argv[1:])
