#!/usr/bin/env python3
"""Write data/ai.json: the day's AI news for /ai/ (layouts/_default/ai.html).

Every source is listed in config.json -- people B reads, the labs, the coding
tools' release feeds, Hacker News and a few subreddits, and learning
material -- plus two model catalogues: OpenRouter (every new model, open or
closed, with price and context) and Hugging Face (trending open weights).

The file is merged, not replaced. An entry keeps the date it was first seen,
and a source that fails today (Reddit rate-limits, a feed times out) keeps
yesterday's entries instead of vanishing from the page; its status says so.
Entries older than window_days drop off, except that each person keeps their
latest few posts however old, so a quiet writer still has a card.

The page is drawn in the browser from /data/ai.json and checks
schema_version. Changing the shape of the file means bumping SCHEMA_VERSION,
adding a step to MIGRATIONS that upgrades the previous file, and updating
schema.json -- the tests hold all three to each other.

  python3 tools/ai-radar/radar.py              # fetch everything, write data/ai.json
  python3 tools/ai-radar/radar.py --only hn    # just these sources (others kept as-is)
  python3 tools/ai-radar/radar.py --dry-run    # fetch and report, write nothing

Standard library only, so the daily GitHub Action needs no install step.
"""
import argparse
import datetime as dt
import email.utils
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "data" / "ai.json"
CONFIG = HERE / "config.json"
FEEDLY = ROOT / "data" / "feedly.yaml"
POSTS = ROOT / "content" / "post"
SITE = "https://brianpfeil.com"
UA = "Mozilla/5.0 (compatible; brianpfeil.com AI radar; +https://brianpfeil.com/ai/)"

SCHEMA_VERSION = 1
SECTIONS = ["people", "labs", "tools", "community", "learning"]
SUMMARY_CHARS = 280
PERSON_KEEP = 3          # latest posts a writer keeps past the window
EVERGREEN = ("people", "learning")   # sections whose writers keep them
DEFAULT_LIMIT = 5

# Title/summary words that make an entry from a general-purpose feed count as AI.
AI_WORDS = re.compile(
    r"\b(ai|a\.i\.|llms?|gpt[-\w.]*|chatgpt|claude|anthropic|openai|gemini|copilot|"
    r"agents?|agentic|mcp|model context protocol|machine learning|ml|neural|transformers?|"
    r"inference|fine-?tun\w*|rag|embeddings?|prompts?|deepseek|mistral|llama|qwen|"
    r"diffusion|reasoning models?|foundation models?|bedrock|sagemaker|vibe coding|"
    r"codex|cursor|superintelligence|agi|openrouter|hugging ?face|ollama)\b", re.I)
BEDROCK_WORDS = re.compile(r"\b(bedrock|sagemaker|amazon q|kiro|nova|agentcore|generative ai)\b", re.I)
FILTERS = {"ai": AI_WORDS, "bedrock": BEDROCK_WORDS}
PRERELEASE = re.compile(r"(alpha|beta|preview|nightly|\brc\d*|-pre\b|canary|insiders)", re.I)

ATOM = "{http://www.w3.org/2005/Atom}"
MEDIA = "{http://search.yahoo.com/mrss/}"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}"
SITEMAP = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


# --- small helpers ------------------------------------------------------------

def now_utc():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(d):
    return d.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if d else None


def parse_date(s):
    """RFC 822 (RSS), ISO 8601 (Atom, APIs) or a Unix timestamp -> aware UTC."""
    if s is None or s == "":
        return None
    if isinstance(s, (int, float)):
        return dt.datetime.fromtimestamp(s, dt.timezone.utc)
    s = s.strip()
    try:
        d = email.utils.parsedate_to_datetime(s)
        if d:
            return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)
    except (TypeError, ValueError, IndexError):
        pass
    try:
        d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return None


def plain(s, limit=SUMMARY_CHARS):
    """Markup to one line of plain text, cut on a word boundary."""
    if not s:
        return ""
    s = re.sub(r"(?is)<(script|style|pre|code)\b.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(html.unescape(s))
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0].rstrip(",.;:-–— ") + "…"
    return s


def item_id(url):
    return hashlib.sha1(canonical(url).encode()).hexdigest()[:12]


def canonical(url):
    """The same story from two places compares equal: no tracking query, no
    trailing slash, no www, http == https."""
    p = urllib.parse.urlsplit(url.strip())
    q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query)
         if not k.startswith("utm_") and k not in ("ref", "source", "s")]
    host = p.netloc.lower().removeprefix("www.")
    return urllib.parse.urlunsplit(("https", host, p.path.rstrip("/") or "/",
                                    urllib.parse.urlencode(q), ""))


# Substack answers a bot User-Agent from a datacenter IP (the daily Action)
# with 403; the same request as a browser goes through.
BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def http_get(url, tries=3, timeout=30):
    ua = UA
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 403 and ua == UA and attempt + 1 < tries:
                ua = BROWSER_UA
                continue
            if e.code == 429 and attempt + 1 < tries:
                time.sleep(5 * (attempt + 1))
                continue
            if e.code < 500 or attempt + 1 == tries:
                raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt + 1 == tries:
                raise
        time.sleep(2 * (attempt + 1))


# --- parsers (pure: bytes in, entries out -- the tests feed them fixtures) ----

def text(el, *paths):
    for p in paths:
        e = el.find(p)
        if e is not None and (e.text or "").strip():
            return e.text.strip()
    return ""


def parse_feed(body):
    """RSS 2.0 or Atom -> [{title, url, published, summary, author}]."""
    root = ET.fromstring(body)
    out = []
    if root.tag == ATOM + "feed":
        for e in root.iter(ATOM + "entry"):
            link = ""
            for l in e.findall(ATOM + "link"):
                if l.get("rel", "alternate") == "alternate":
                    link = l.get("href", "")
                    break
            out.append({
                "title": plain(text(e, ATOM + "title"), 200),
                "url": link,
                "published": text(e, ATOM + "published", ATOM + "updated"),
                "summary": text(e, ATOM + "summary", ATOM + "content"),
                "author": text(e, ATOM + "author/" + ATOM + "name"),
            })
    else:
        for e in root.iter("item"):
            out.append({
                "title": plain(text(e, "title"), 200),
                "url": text(e, "link") or text(e, "guid"),
                "published": text(e, "pubDate", "{http://purl.org/dc/elements/1.1/}date"),
                "summary": text(e, "description", CONTENT + "encoded"),
                "author": text(e, "{http://purl.org/dc/elements/1.1/}creator", "author"),
            })
    return [x for x in out if x["title"] and x["url"].startswith("http")]


def parse_sitemap(body, paths):
    """Sitemap URLs under one of `paths` that carry a lastmod, newest first.
    Index pages (/news/ itself) are skipped: an entry needs a slug."""
    root = ET.fromstring(body)
    out = []
    for u in root.iter(SITEMAP + "url"):
        loc, mod = text(u, SITEMAP + "loc"), text(u, SITEMAP + "lastmod")
        path = urllib.parse.urlsplit(loc).path
        if not mod or not any(path.startswith(p) and len(path) > len(p) for p in paths):
            continue
        out.append({"title": "", "url": loc, "published": mod, "summary": "", "author": ""})
    out.sort(key=lambda x: x["published"], reverse=True)
    return out


def page_meta(body):
    """<title> (minus the site suffix) and meta description of an HTML page."""
    s = body.decode("utf-8", "replace")
    def meta(name):
        m = re.search(r'<meta[^>]+(?:name|property)="%s"[^>]+content="([^"]*)"' % name, s, re.I) \
            or re.search(r'<meta[^>]+content="([^"]*)"[^>]+(?:name|property)="%s"' % name, s, re.I)
        return html.unescape(m.group(1)) if m else ""
    title = meta("og:title")
    if not title:
        m = re.search(r"<title[^>]*>(.*?)</title>", s, re.I | re.S)
        # "How X works \ Anthropic" -> "How X works"
        title = re.sub(r"\s+[|\\]\s+[^|\\]{1,40}$", "", html.unescape(m.group(1)).strip()) if m else ""
    return plain(title, 200), meta("og:description") or meta("description")


def slug_title(url):
    slug = urllib.parse.urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]
    return slug.replace("-", " ").capitalize()


def parse_hn(body, min_points):
    hits = json.loads(body).get("hits", [])
    out = []
    for h in hits:
        title = h.get("title") or ""
        if (h.get("points") or 0) < min_points or not AI_WORDS.search(title):
            continue
        hn_url = "https://news.ycombinator.com/item?id=%s" % h["objectID"]
        out.append({
            "title": plain(title, 200),
            "url": h.get("url") or hn_url,
            "published": h.get("created_at"),
            "summary": "",
            "author": h.get("author", ""),
            "points": h.get("points") or 0,
            "comments": h.get("num_comments") or 0,
            "discuss": hn_url,
        })
    out.sort(key=lambda x: x["points"], reverse=True)
    return out


def parse_reddit(body):
    """Reddit's Atom: the entry links to the thread; the post's own link, when
    it has one, is the '[link]' anchor in the content."""
    out = []
    for e in parse_feed(body):
        m = re.search(r'<a href="([^"]+)">\[link\]</a>', e["summary"])
        target = html.unescape(m.group(1)) if m else e["url"]
        body_text = re.sub(r"submitted by.*$", "", plain(e["summary"], 2000), flags=re.S).strip()
        e.update(summary=body_text, discuss=e["url"], url=target)
        out.append(e)
    return out


def parse_openrouter(body, since, limit):
    """Models added to OpenRouter since `since`, newest first. Variants
    (:free, :batch, :thinking…) and routers (no price) are skipped."""
    out = []
    for m in json.loads(body).get("data", []):
        created = parse_date(m.get("created"))
        if ":" in m["id"] or not created or created < since:
            continue
        p = m.get("pricing") or {}
        try:
            price_in, price_out = float(p.get("prompt", -1)), float(p.get("completion", -1))
        except (TypeError, ValueError):
            continue
        if price_in < 0 or price_out < 0:
            continue
        name = m.get("name", m["id"])
        provider = name.split(":", 1)[0].strip() if ":" in name else m["id"].split("/")[0]
        arch = m.get("architecture") or {}
        out.append({
            "id": m["id"],
            "name": name.split(":", 1)[1].strip() if ":" in name else name,
            "provider": provider,
            "created": iso(created),
            "context": m.get("context_length") or None,
            "price_in": round(price_in * 1e6, 4),
            "price_out": round(price_out * 1e6, 4),
            "modalities": sorted(set(arch.get("input_modalities") or ["text"])),
            "open_weights": m.get("hugging_face_id") or None,
            "summary": plain(re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", m.get("description", "")), 220),
            "url": "https://openrouter.ai/" + m["id"],
        })
    out.sort(key=lambda x: x["created"], reverse=True)
    return out[:limit]


def parse_hf(body, limit):
    out = []
    for m in json.loads(body):
        if m.get("private"):
            continue
        out.append({
            "id": m["id"],
            "task": m.get("pipeline_tag") or None,
            "likes": m.get("likes") or 0,
            "downloads": m.get("downloads") or 0,
            "created": iso(parse_date(m.get("createdAt"))),
            "url": "https://huggingface.co/" + m["id"],
        })
    return out[:limit]


# --- personal: who B follows, and B's own AI posts ----------------------------

def feedly_hosts(path=FEEDLY):
    """Hosts of the feeds in B's Feedly (data/feedly.yaml, url: lines)."""
    try:
        s = path.read_text()
    except OSError:
        return set()
    return {urllib.parse.urlsplit(u).netloc.lower().removeprefix("www.")
            for u in re.findall(r'^\s*url:\s*"?([^"\s]+)', s, re.M)}


def my_posts(posts_dir=POSTS, limit=8):
    """B's own posts tagged AI, newest first, from content/post front matter."""
    tags_ai = {"ai", "llm", "llms", "openai", "claude", "anthropic", "bedrock", "langchain",
               "gpt", "mcp", "agents", "machine-learning", "genai", "generative-ai"}
    out = []
    for p in sorted(posts_dir.glob("*.md")):
        s = p.read_text(errors="replace")
        fm = s.split("+++" if s.startswith("+++") else "---", 2)
        if len(fm) < 3:
            continue
        fm = fm[1]
        m = re.search(r"^tags\s*[=:]\s*\[(.*?)\]", fm, re.M)
        tags = {t.lower() for t in re.findall(r'"([^"]+)"', m.group(1))} if m else set()
        if not tags & tags_ai or re.search(r"^draft\s*[=:]\s*true", fm, re.M):
            continue
        title = re.search(r'^title\s*[=:]\s*"?(.*?)"?\s*$', fm, re.M)
        date = re.search(r'^date\s*[=:]\s*"?([^"\s]+)', fm, re.M)
        slug = re.search(r'^slug\s*[=:]\s*"?(.*?)"?\s*$', fm, re.M)
        if not (title and date):
            continue
        d = parse_date(date.group(1))
        out.append({
            "title": title.group(1),
            "url": "/post/%s/" % (slug.group(1) if slug else p.stem),
            "published": iso(d),
            "tags": sorted(tags & tags_ai),
        })
    out.sort(key=lambda x: x["published"] or "", reverse=True)
    return out[:limit]


# --- fetching -----------------------------------------------------------------

def keep_entry(src, e):
    f = FILTERS.get(src.get("filter", ""))
    if f and not (f.search(e["title"]) or f.search(plain(e["summary"], 600))):
        return False
    if src.get("stable") and PRERELEASE.search(e["title"]):
        return False
    return True


def fetch_source(src, now):
    """-> (entries, error). Never raises: one broken feed must not stop the run."""
    kind = src.get("kind", "rss")
    try:
        if kind == "hn":
            since = int((now - dt.timedelta(days=2)).timestamp())
            url = ("https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=1000"
                   "&numericFilters=" + urllib.parse.quote("created_at_i>%d,points>%d" % (since, src.get("min_points", 100))))
            entries = parse_hn(http_get(url), src.get("min_points", 100))
        elif kind == "reddit":
            entries = parse_reddit(http_get(src["feed"]))
        elif kind == "sitemap":
            entries = parse_sitemap(http_get(src["feed"]), src["paths"])
        else:
            entries = parse_feed(http_get(src["feed"]))
    except Exception as e:  # noqa: BLE001 -- recorded on the source, shown on the page
        return [], "%s: %s" % (type(e).__name__, str(e)[:160])
    entries = [e for e in entries if keep_entry(src, e)]
    if kind != "hn":
        entries.sort(key=lambda e: iso(parse_date(e["published"])) or "", reverse=True)
    entries = entries[: src.get("limit", DEFAULT_LIMIT)]
    if kind == "sitemap":
        for e in entries:
            try:
                e["title"], e["summary"] = page_meta(http_get(e["url"], tries=2))
            except Exception:  # noqa: BLE001
                pass
            e["title"] = e["title"] or slug_title(e["url"])
    return entries, None


def to_item(src, e, now):
    published = parse_date(e.get("published")) or now
    item = {
        "id": item_id(e["url"]),
        "source": src["id"],
        "section": src["section"],
        "title": e["title"],
        "url": e["url"],
        "published": iso(min(published, now)),
        "first_seen": iso(now),
        "summary": plain(e.get("summary", "")),
    }
    if src.get("release"):
        item["kind"] = "release"
    for k in ("points", "comments", "discuss"):
        if e.get(k):
            item[k] = e[k]
    return item


# --- merging and pruning --------------------------------------------------------

def merge_items(old, new, now, window_days, person_ids):
    """Today's entries win, keeping each one's original first_seen. Yesterday's
    stay too -- a feed lists only its newest few, and a source that failed
    today must not empty its section -- until the window drops them."""
    by_id = {(i["id"], i["source"]): i for i in old}
    for i in new:
        prev = by_id.get((i["id"], i["source"]))
        if prev:
            i["first_seen"] = prev.get("first_seen", i["first_seen"])
            if prev.get("points", 0) > i.get("points", 0):
                i["points"], i["comments"] = prev["points"], prev.get("comments", 0)
        by_id[(i["id"], i["source"])] = i

    cutoff = iso(now - dt.timedelta(days=window_days))
    kept, per_person = [], {}
    for i in sorted(by_id.values(), key=lambda i: i["published"], reverse=True):
        if i["source"] in person_ids:
            n = per_person.get(i["source"], 0)
            if i["published"] >= cutoff or n < PERSON_KEEP:
                per_person[i["source"]] = n + 1
                kept.append(i)
        elif i["published"] >= cutoff:
            kept.append(i)
    return kept


def crosslink(items):
    """The same story from several sources: record where else it appeared
    (`also`), which the page shows and uses to rank the Latest tab."""
    by_url = {}
    for i in items:
        by_url.setdefault(canonical(i["url"]), []).append(i)
        if i.get("discuss"):
            by_url.setdefault(canonical(i["discuss"]), []).append(i)
    also = {}
    for group in by_url.values():
        srcs = {g["source"] for g in group}
        for g in group:
            also.setdefault(id(g), set()).update(srcs - {g["source"]})
    for i in items:
        if also.get(id(i)):
            i["also"] = sorted(also[id(i)])
        else:
            i.pop("also", None)
    return items


def dedupe(items):
    """One row per id per section (a URL can come back from two feeds)."""
    seen, out = set(), []
    for i in items:
        k = (i["id"], i["section"])
        if k not in seen:
            seen.add(k)
            out.append(i)
    return out


# --- schema migrations ------------------------------------------------------------

def _v0_to_v1(doc):
    """v0: the unversioned draft, items without first_seen or section."""
    for i in doc.get("items", []):
        i.setdefault("first_seen", i.get("published"))
        i.setdefault("section", "community")
    doc.setdefault("models", {"new": [], "trending": []})
    doc.setdefault("mine", [])
    return doc


MIGRATIONS = {0: _v0_to_v1}


def migrate(doc):
    """Bring a previously written file up to SCHEMA_VERSION, one step at a time."""
    v = doc.get("schema_version", 0)
    if v > SCHEMA_VERSION:
        raise SystemExit("data/ai.json is schema v%d; this tool only knows v%d" % (v, SCHEMA_VERSION))
    while v < SCHEMA_VERSION:
        doc = MIGRATIONS[v](doc)
        v += 1
        doc["schema_version"] = v
    return doc


def load_previous(path=OUT):
    try:
        return migrate(json.loads(path.read_text()))
    except FileNotFoundError:
        return migrate({"schema_version": SCHEMA_VERSION, "items": [], "sources": []})


# --- validation -------------------------------------------------------------------

SCHEMA = HERE / "schema.json"
_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None),
          "number": (int, float), "integer": int}


def validate(value, schema, path="$"):
    """The subset of JSON Schema that schema.json uses -> list of errors."""
    errs = []
    types = schema.get("type")
    if types:
        types = types if isinstance(types, list) else [types]
        ok = any(isinstance(value, _TYPES[t]) and not (t in ("integer", "number") and isinstance(value, bool))
                 for t in types)
        if not ok:
            return ["%s: expected %s, got %s" % (path, "/".join(types), type(value).__name__)]
    if "enum" in schema and value not in schema["enum"]:
        errs.append("%s: %r not in %r" % (path, value, schema["enum"]))
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for k in schema.get("required", []):
            if k not in value:
                errs.append("%s: missing %s" % (path, k))
        for k, v in value.items():
            if k in props:
                errs += validate(v, props[k], "%s.%s" % (path, k))
            elif schema.get("additionalProperties") is False:
                errs.append("%s: unexpected field %s" % (path, k))
    if isinstance(value, list) and "items" in schema:
        for n, v in enumerate(value):
            errs += validate(v, schema["items"], "%s[%d]" % (path, n))
    return errs


# --- the run ----------------------------------------------------------------------

def public_source(src, status, checked, error, feedly):
    host = urllib.parse.urlsplit(src["home"]).netloc.lower().removeprefix("www.")
    out = {
        "id": src["id"],
        "section": src["section"],
        "name": src["name"],
        "home": src["home"],
        "status": status,
        "checked": checked,
    }
    for k in ("x", "pin"):
        if src.get(k):
            out[k] = src[k]
    via = []
    if host in feedly:
        via.append("feedly")
    if src.get("follow"):
        via.append("x")
    if via:
        out["via"] = via
    if error:
        out["error"] = error
    return out


def build(cfg, prev, now, only=None, fetch=fetch_source, get=http_get, posts_dir=POSTS, feedly=None):
    feedly = feedly_hosts() if feedly is None else feedly
    srcs = [s for s in cfg["sources"] if not only or s["id"] in only]
    prev_sources = {s["id"]: s for s in prev.get("sources", [])}

    def run(src):
        if src.get("kind") == "reddit":
            time.sleep(SOURCE_DELAY.get(src["id"], 0))
        return src, fetch(src, now)

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(run, srcs))

    new_items, failed, sources = [], set(), {}
    for src, (entries, error) in results:
        if error:
            failed.add(src["id"])
            p = prev_sources.get(src["id"], {})
            sources[src["id"]] = public_source(src, "error", p.get("checked"), error, feedly)
        else:
            new_items += [to_item(src, e, now) for e in entries]
            sources[src["id"]] = public_source(src, "ok", iso(now), None, feedly)
    # Sources not fetched this run (--only) keep their previous status.
    for src in cfg["sources"]:
        if src["id"] not in sources:
            p = prev_sources.get(src["id"])
            sources[src["id"]] = public_source(src, p["status"] if p else "pending",
                                               p.get("checked") if p else None,
                                               p.get("error") if p else None, feedly)

    # Yesterday's items still have to pass today's config: a source that was
    # removed, or given a filter, stops showing what it no longer would.
    by_id = {s["id"]: s for s in cfg["sources"]}
    old = [i for i in prev.get("items", []) if i["source"] in by_id and keep_entry(by_id[i["source"]], i)]
    person_ids = {s["id"] for s in cfg["sources"] if s["section"] in EVERGREEN}
    items = merge_items(old, new_items, now, cfg.get("window_days", 14), person_ids)
    items = crosslink(dedupe(items))

    models = prev.get("models") or {"new": [], "trending": []}
    mcfg = cfg.get("models", {})
    if not only or "models" in only:
        since = now - dt.timedelta(days=mcfg.get("new_days", 45))
        try:
            models["new"] = parse_openrouter(get(mcfg["openrouter"]), since, mcfg.get("limit", 40))
            models["new_checked"] = iso(now)
            models.pop("new_error", None)
        except Exception as e:  # noqa: BLE001
            models["new_error"] = str(e)[:160]
        try:
            models["trending"] = parse_hf(get(mcfg["huggingface"]), mcfg.get("trending_limit", 20))
            models["trending_checked"] = iso(now)
            models.pop("trending_error", None)
        except Exception as e:  # noqa: BLE001
            models["trending_error"] = str(e)[:160]

    order = {s["id"]: n for n, s in enumerate(cfg["sources"])}
    return {
        "schema_version": SCHEMA_VERSION,
        "generated": iso(now),
        "window_days": cfg.get("window_days", 14),
        "sections": SECTIONS,
        "sources": sorted(sources.values(), key=lambda s: order[s["id"]]),
        "items": items,
        "models": models,
        "mine": my_posts(posts_dir),
    }


# Reddit answers a burst from one IP with 429s, so its feeds are staggered.
SOURCE_DELAY = {"r-localllama": 0, "r-claudeai": 20, "r-chatgptcoding": 40}


def summary(doc):
    ok = sum(1 for s in doc["sources"] if s["status"] == "ok")
    lines = ["%d/%d sources ok, %d items, %d new models, %d trending" % (
        ok, len(doc["sources"]), len(doc["items"]), len(doc["models"].get("new", [])),
        len(doc["models"].get("trending", [])))]
    for s in doc["sources"]:
        if s["status"] != "ok":
            lines.append("  %-18s %s %s" % (s["id"], s["status"], s.get("error", "")))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="*", help="source ids (and/or 'models') to fetch")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args(argv)
    cfg = json.loads(CONFIG.read_text())
    doc = build(cfg, load_previous(a.out), now_utc(), only=set(a.only) if a.only else None)
    print(summary(doc))
    errors = validate(doc, json.loads(SCHEMA.read_text()))
    if errors:
        print("not written -- the result does not match schema.json:", *errors[:20], sep="\n  ")
        return 1
    if not a.dry_run:
        a.out.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
        print("wrote", a.out.relative_to(ROOT) if a.out.is_relative_to(ROOT) else a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
