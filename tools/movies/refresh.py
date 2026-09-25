#!/usr/bin/env python3
"""Fill in data/movies.json from a list of titles.

data/movies.json is both the input and the output. Each entry needs only an
IMDb id (and a title, so a human can read the file); everything else --
poster, runtime, rating, cast, Rotten Tomatoes scores, the trailer, where to
stream it in the US, and the title and synopsis in all nine site languages --
is looked up and written back. Re-running refreshes scores and streaming,
which drift; entries keep their order, which is the order on the page.

Sources, all public and keyless:
  JustWatch GraphQL   metadata, localized text, poster, US offers, trailer
  Wikidata            the Rotten Tomatoes slug for an IMDb id
  rottentomatoes.com  Tomatometer and Popcornmeter
  YouTube             a trailer when JustWatch has none; every trailer is
                      checked against oEmbed, which refuses non-embeddable ones

Posters and service logos are downloaded into static/movies/, never hotlinked.

  python3 tools/movies/refresh.py            # every movie
  python3 tools/movies/refresh.py tt0111161  # just these
"""
import datetime
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "movies.json"
STATIC = ROOT / "static" / "movies"
UA = "Mozilla/5.0 (brianpfeil.com movie list refresher)"

# Site language -> JustWatch (language, country). The country only picks the
# regional title ("El club de la lucha" in Spain); offers are always the US.
# JustWatch has no mainland-China catalogue, so Chinese is asked of the US one.
LANGS = {
    "en": ("en", "US"), "zh": ("zh", "US"), "es": ("es", "ES"),
    "pt": ("pt", "BR"), "fr": ("fr", "FR"), "de": ("de", "DE"),
    "it": ("it", "IT"), "ja": ("ja", "JP"), "ko": ("ko", "KR"),
}

# JustWatch monetization types, cheapest first -> the page's groups.
GROUPS = {"FREE": "free", "ADS": "free", "FLATRATE": "stream", "RENT": "rent", "BUY": "buy"}
QUALITY = {"_4K": 3, "HD": 2, "SD": 1}


def http(url, data=None, headers=None, tries=3):
    hdrs = {"User-Agent": UA, **(headers or {})}
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=hdrs)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code < 500:
                return e.code, b""
        except (urllib.error.URLError, OSError):
            pass
        time.sleep(2 ** attempt)
    return 0, b""


def jw(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    status, raw = http("https://apis.justwatch.com/graphql", body,
                       {"Content-Type": "application/json"})
    if status != 200:
        raise RuntimeError(f"JustWatch {status}")
    out = json.loads(raw)
    if out.get("errors"):
        raise RuntimeError(out["errors"][0]["message"])
    return out["data"]


SEARCH = """
query($q: String!) {
  popularTitles(country: US, first: 8, filter: {searchQuery: $q, objectTypes: [MOVIE]}) {
    edges { node { id content(country: US, language: "en") {
      originalReleaseYear externalIds { imdbId } } } }
  }
}"""

DETAIL = """
query($id: ID!, $lang: Language!, $country: Country!) {
  node(id: $id) { ... on Movie {
    content(country: $country, language: $lang) {
      title fullPath originalReleaseYear runtime shortDescription posterUrl
      ageCertification
      genres { translation(language: $lang) }
      credits { role name }
      clips { externalId provider }
      scoring { imdbScore imdbVotes }
    }
  } }
}"""

OFFERS = """
query($id: ID!) {
  node(id: $id) { ... on Movie {
    offers(country: US, platform: WEB) {
      monetizationType presentationType standardWebURL
      retailPrice(language: "en")
      package { clearName technicalName icon }
    }
  } }
}"""


def find_jw_id(movie):
    """The JustWatch node whose IMDb id matches; titles alone are ambiguous."""
    for q in (movie["title"], f'{movie["title"]} {movie.get("year", "")}'.strip()):
        for e in jw(SEARCH, {"q": q})["popularTitles"]["edges"]:
            if e["node"]["content"]["externalIds"]["imdbId"] == movie["imdb"]:
                return e["node"]["id"]
    raise RuntimeError(f'{movie["title"]}: no JustWatch match for {movie["imdb"]}')


def download(url, dest):
    if dest.exists():
        return True
    status, raw = http(url)
    if status != 200 or not raw:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
    return True


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def offers_for(jw_id):
    """US offers, one per service per group, best picture quality kept."""
    best = {}
    for o in jw(OFFERS, {"id": jw_id})["node"]["offers"]:
        group = GROUPS.get(o["monetizationType"])
        if not group:
            continue
        pkg = o["package"]
        key = (group, pkg["technicalName"])
        q = QUALITY.get(o["presentationType"], 0)
        if key in best and best[key]["_q"] >= q:
            continue
        icon = f'/movies/services/{pkg["technicalName"]}.webp'
        if not download("https://images.justwatch.com" +
                        pkg["icon"].replace("{profile}", "s100").replace("{format}", "webp"),
                        ROOT / "static" / icon.lstrip("/")):
            icon = None
        best[key] = {"_q": q, "type": group, "service": pkg["clearName"],
                     "icon": icon, "url": o["standardWebURL"],
                     "price": o["retailPrice"],
                     "quality": o["presentationType"].lstrip("_")}
    order = list(dict.fromkeys(GROUPS.values()))
    out = sorted(best.values(), key=lambda o: (order.index(o["type"]), o["service"].lower()))
    for o in out:
        del o["_q"]
    return out


def wikidata(imdb):
    """(Rotten Tomatoes slug, MPA rating) for an IMDb id. JustWatch's own
    certification is sometimes a TV rating (Inception comes back TV-14)."""
    q = ('SELECT ?rt ?mpa WHERE { ?f wdt:P345 "%s" . '
         'OPTIONAL { ?f wdt:P1258 ?rt } '
         'OPTIONAL { ?f wdt:P1657 ?r . ?r rdfs:label ?mpa FILTER(lang(?mpa) = "en") } }' % imdb)
    status, raw = http("https://query.wikidata.org/sparql?format=json&query=" +
                       urllib.parse.quote(q))
    if status != 200:
        return None, None
    rows = json.loads(raw)["results"]["bindings"]
    slugs = [r["rt"]["value"] for r in rows if r.get("rt", {}).get("value", "").startswith("m/")]
    mpa = [r["mpa"]["value"] for r in rows if "mpa" in r]
    # Labels read like "R" or "PG-13"; anything longer is not a certificate.
    mpa = [m for m in mpa if re.fullmatch(r"G|PG|PG-13|R|NC-17", m)]
    return (slugs[0] if slugs else None), (mpa[0] if mpa else None)


def rt_scores(slug):
    url = f"https://www.rottentomatoes.com/{slug}"
    status, raw = http(url)
    if status != 200:
        return None
    html = raw.decode("utf-8", "replace")

    def grab(name):
        m = re.search(r'"%s":(\{[^{}]*\})' % name, html)
        return json.loads(m.group(1)) if m else {}

    critics, audience = grab("criticsScore"), grab("audienceScore")

    def score(d):
        return int(d["score"]) if d.get("score") else None

    if score(critics) is None and score(audience) is None:
        return None
    # criticsScore.certified is the Certified Fresh badge.
    return {"url": url, "critics": score(critics), "audience": score(audience),
            "certified": bool(critics.get("certified"))}


def embeddable(video_id):
    status, _ = http("https://www.youtube.com/oembed?format=json&url=" +
                     urllib.parse.quote(f"https://www.youtube.com/watch?v={video_id}"))
    return status == 200


def youtube_search(query):
    status, raw = http("https://www.youtube.com/results?search_query=" + urllib.parse.quote(query))
    if status != 200:
        return []
    return list(dict.fromkeys(re.findall(r'"videoId":"([\w-]{11})"', raw.decode("utf-8", "replace"))))


def trailer_for(movie, clips):
    candidates = [c["externalId"] for c in clips if c["provider"] == "YOUTUBE"]
    candidates += youtube_search(f'{movie["title"]} {movie.get("year", "")} official trailer')[:5]
    for vid in candidates:
        if embeddable(vid):
            return vid
    return None


def refresh(movie):
    jw_id = movie.get("justwatch_id") or find_jw_id(movie)
    movie["justwatch_id"] = jw_id

    detail = {}
    for site_lang, (lang, country) in LANGS.items():
        try:
            c = jw(DETAIL, {"id": jw_id, "lang": lang, "country": country})["node"]["content"]
        except RuntimeError:
            c = None
        if c:
            detail[site_lang] = c
    en = detail["en"]

    slug = slugify(en["title"]) + f'-{en["originalReleaseYear"]}'
    poster = f"/movies/posters/{slug}.webp"
    if en.get("posterUrl") and download(
            "https://images.justwatch.com" +
            en["posterUrl"].replace("{profile}", "s332").replace("{format}", "webp"),
            ROOT / "static" / poster.lstrip("/")):
        movie["poster"] = poster

    movie["title"] = en["title"]
    movie["year"] = en["originalReleaseYear"]
    movie["runtime"] = en["runtime"]
    movie["rating"] = en["ageCertification"] or None
    movie["genres"] = {k: [g["translation"] for g in v["genres"]] for k, v in detail.items()}
    movie["directors"] = [c["name"] for c in en["credits"] if c["role"] == "DIRECTOR"]
    movie["cast"] = [c["name"] for c in en["credits"] if c["role"] == "ACTOR"][:4]
    movie["titles"] = {k: v["title"] for k, v in detail.items() if v.get("title")}
    movie["synopsis"] = {k: v["shortDescription"] for k, v in detail.items() if v.get("shortDescription")}
    movie["imdb_url"] = f'https://www.imdb.com/title/{movie["imdb"]}/'
    if en["scoring"].get("imdbScore"):
        movie["imdb_rating"] = en["scoring"]["imdbScore"]
    movie["justwatch_url"] = "https://www.justwatch.com" + en["fullPath"]

    slug_rt, mpa = wikidata(movie["imdb"])
    if mpa:
        movie["rating"] = mpa
    slug_rt = movie.get("rt_slug") or slug_rt
    if slug_rt:
        movie["rt_slug"] = slug_rt
        scores = rt_scores(slug_rt)
        if scores:
            movie["rotten_tomatoes"] = scores

    # A trailer someone picked by hand stays; otherwise re-check the old one.
    if not (movie.get("trailer") and embeddable(movie["trailer"])):
        movie["trailer"] = trailer_for(movie, en.get("clips") or [])

    movie["offers"] = offers_for(jw_id)
    return movie


def main(argv):
    doc = json.loads(DATA.read_text())
    only = set(argv)
    failed = []
    for movie in doc["movies"]:
        if only and movie["imdb"] not in only:
            continue
        try:
            refresh(movie)
            rt = (movie.get("rotten_tomatoes") or {}).get("critics")
            print(f'{movie["title"]:<45} RT {rt}  trailer {movie["trailer"]}  '
                  f'{len(movie["offers"])} offers')
        except Exception as e:  # keep going; report at the end
            failed.append(f'{movie.get("title")}: {e}')
    doc["updated"] = datetime.date.today().isoformat()
    DATA.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
    for f in failed:
        print("FAILED", f, file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
