#!/usr/bin/env python3
"""Write data/github.json: every public repo of pfeilbr, classified for /github/.

The page (layouts/_default/github.html) is drawn in the browser from
/data/github.json, so this file is its only source. Re-running refreshes
stars, push dates and descriptions; the output is sorted and stable, so an
unchanged account produces an unchanged file apart from the date.

Where the fields come from:
  GitHub GraphQL (via the `gh` CLI, so no token handling here)
      name, description, languages, topics, stars, dates, fork parent,
      and the README, of which only a plain-text excerpt is kept
  content/post/*.md
      the tags of the article written about a repo (repoFullName), which
      are far richer than GitHub topics -- 13 topics across 411 repos

Classification is by tokens: post tags, topics, the primary language and
the words of the repo name, matched against the areas and tracks in
config.json. An area's glyph and the order of the areas mirror
layouts/partials/icons/topic-id.html, so a repo wears the same icon here as
its article does in the post list.

  python3 tools/github-repos/refresh.py            # fetch and write
  python3 tools/github-repos/refresh.py --cached   # reuse the last fetch

Only public repos are fetched: the page never lists what a visitor can't open.
Standard library only; needs `gh` signed in for the fetch.
"""
import argparse
import datetime
import json
import re
import subprocess
import sys
import time
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "data" / "github.json"
POSTS = ROOT / "content" / "post"
CONFIG = HERE / "config.json"
CACHE = HERE / ".cache" / "repos.json"
USER = "pfeilbr"

README_NAMES = ["README.md", "readme.md", "Readme.md", "README.markdown", "README", "README.txt", "README.rst"]

QUERY = """
query($cursor: String) {
  user(login: "%s") {
    repositories(first: 40, after: $cursor, privacy: PUBLIC, ownerAffiliations: OWNER,
                 orderBy: {field: NAME, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name description homepageUrl isFork isArchived stargazerCount forkCount
        createdAt pushedAt diskUsage
        licenseInfo { spdxId }
        parent { nameWithOwner }
        primaryLanguage { name color }
        languages(first: 6, orderBy: {field: SIZE, direction: DESC}) {
          totalSize edges { size node { name color } }
        }
        repositoryTopics(first: 20) { nodes { topic { name } } }
        %s
      }
    }
  }
}
""" % (USER, "\n        ".join(
    'r%d: object(expression: "HEAD:%s") { ... on Blob { text } }' % (i, n)
    for i, n in enumerate(README_NAMES)))


# --- fetching ---------------------------------------------------------------

def gh_graphql(cursor, tries=4, run=subprocess.run, sleep=time.sleep):
    """One page of the query. Retries GitHub's occasional 502/timeout with
    backoff; a missing or signed-out `gh` fails at once with what to do."""
    args = ["gh", "api", "graphql", "-f", "query=" + QUERY]
    if cursor:
        args += ["-f", "cursor=" + cursor]
    for attempt in range(tries):
        try:
            res = run(args, capture_output=True, text=True)
        except FileNotFoundError:
            raise SystemExit("refresh: the GitHub CLI (gh) is not installed")
        if res.returncode == 0:
            return json.loads(res.stdout)
        err = (res.stderr or "").strip()
        if "auth login" in err or "GH_TOKEN" in err or "401" in err:
            raise SystemExit("refresh: gh is not signed in -- run `gh auth login` or set GH_TOKEN")
        if attempt == tries - 1:
            raise SystemExit(f"refresh: GitHub API failed after {tries} tries: {err}")
        print(f"  retrying after: {err[:120]}", file=sys.stderr)
        sleep(2 ** attempt * 3)


def fetch_all():
    repos, cursor = [], None
    while True:
        conn = gh_graphql(cursor)["data"]["user"]["repositories"]
        repos += conn["nodes"]
        print(f"  fetched {len(repos)}", file=sys.stderr)
        if not conn["pageInfo"]["hasNextPage"]:
            return repos
        cursor = conn["pageInfo"]["endCursor"]


# --- posts ------------------------------------------------------------------

def post_tags(posts_dir=POSTS):
    """repo name -> set of lowercased tags/categories from its article."""
    out = {}
    for path in sorted(posts_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"\+\+\+\n(.*?)\n\+\+\+", text, re.S)
        if not m:
            continue
        try:
            fm = tomllib.loads(m.group(1))
        except tomllib.TOMLDecodeError:
            continue
        full = fm.get("repoFullName") or ""
        if not full.lower().startswith(USER + "/"):
            continue
        name = full.split("/", 1)[1].lower()
        toks = {str(t).strip().lower() for t in (fm.get("tags") or []) + (fm.get("categories") or [])}
        toks -= {"", "<nil>", "playground", "project"}
        out.setdefault(name, set()).update(toks)
    return out


# --- README -> plain text ---------------------------------------------------

BADGE = re.compile(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)")
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
REFDEF = re.compile(r"^\s*\[[^\]]+\]:\s*\S+.*$", re.M)
TAG = re.compile(r"<[^>]+>")
FENCE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)


def readme_text(md):
    """Markdown -> list of plain-text paragraphs (headings, code and tables dropped)."""
    if not md:
        return []
    md = FENCE.sub("", md.replace("\r\n", "\n"))
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    md = BADGE.sub("", md)
    md = IMAGE.sub("", md)
    md = REFDEF.sub("", md)
    md = LINK.sub(r"\1", md)
    md = TAG.sub("", md)
    paras = []
    for block in re.split(r"\n\s*\n", md):
        lines = []
        for line in block.split("\n"):
            s = line.strip()
            # Headings, tables, rules, shell prompts and indented code.
            if not s or s.startswith(("#", "|", "===", "---", "$ ")) or line.startswith(("    ", "\t")):
                continue
            # The post generator's `tags: [...]` line, not prose.
            if re.match(r"(tags|categories|title)\s*:", s, re.I):
                continue
            s = re.sub(r"^[-*+]\s+|^\d+\.\s+|^>\s*", "", s)
            s = re.sub(r"[`*_]{1,3}", "", s)
            s = re.sub(r"\s+", " ", s).strip()
            if s:
                lines.append(s)
        text = " ".join(lines).strip()
        if len(re.sub(r"[^A-Za-z]", "", text)) >= 3:
            paras.append(text)
    return paras


def safe_url(url):
    """A homepage is shown as a link, so only http(s) gets through; a bare
    "example.com" (GitHub allows it) is given a scheme."""
    url = (url or "").strip()
    if not url or re.search(r"\s", url):
        return ""
    if not re.match(r"[a-z][a-z0-9+.-]*:", url, re.I):
        url = "https://" + url
    return url if re.match(r"https?://[^/\s]+", url, re.I) else ""


def same_words(a, b):
    norm = lambda s: re.sub(r"[^a-z0-9]+", "", s.lower())
    return norm(a) == norm(b)


def clip(text, limit):
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(",;:-(")
    return cut + "…"


def summary_from(paras, limit=220):
    """The first sentence-ish of the README, for repos with no description."""
    for p in paras:
        if p.lower().startswith(("todo", "note:", "install", "usage")) or len(p) < 12:
            continue
        m = re.match(r"(.{20,}?[.!?])(\s|$)", p)
        return clip(m.group(1) if m else p, limit)
    return ""


# --- classification -----------------------------------------------------------

def name_tokens(name):
    """The words of a repo name, plus every run of adjacent words, so
    "aws-step-functions-playground" yields "step-functions" as well."""
    words = [w for w in re.split(r"[-_.\s]+", name.lower()) if w]
    toks = set(words)
    for n in (2, 3):
        for i in range(len(words) - n + 1):
            toks.add("-".join(words[i:i + n]))
    return toks


def tokens_for(repo, tags):
    lang = (repo.get("primaryLanguage") or {}).get("name") or ""
    toks = set(tags) | set(repo.get("topics", [])) | name_tokens(repo["name"])
    if lang:
        toks.add(lang.lower())
    return toks


def matches(toks, rule):
    return bool(toks & set(rule["match"])) and not toks & set(rule.get("exclude", []))


def classify(toks, areas):
    """Every area whose tokens intersect, in config order; the first is the
    primary one (its glyph is the repo's icon). None -> ["other"]."""
    hit = [a["key"] for a in areas if matches(toks, a)]
    return hit or ["other"]


def display_tags(toks, vocab, lang):
    """Tokens worth showing as chips: known technology words only, so a name
    like "my-first-try" doesn't produce a "my" tag."""
    keep = sorted(t for t in toks if t in vocab and t != (lang or "").lower())
    # "step-functions" makes "step" and "functions" redundant.
    multi = [t for t in keep if "-" in t]
    return [t for t in keep if not any(t != m and t in m.split("-") for m in multi)][:8]


def beginner_score(r, depth=0):
    """Higher is a better first stop for someone learning the technology:
    an article that walks through it, a small self-contained playground, a
    README with something in it, how squarely it sits in the path (depth:
    how many of the path's words it carries), a short name (the basics
    rather than a combination), then recency."""
    s = 0
    if r.get("post"):
        s += 4
    if r["kind"] == "playground":
        s += 2
    if r.get("desc"):
        s += 1
    if r.get("readme"):
        s += 1
    if r["_size"] and r["_size"] < 2000:
        s += 1
    s += min(depth, 3)
    if len(re.split(r"[-_.]+", r["name"])) <= 3:
        s += 1
    return (s, r["pushed"])


# --- assembly ---------------------------------------------------------------

def slim(repo, tags, cfg, vocab, posted):
    lang = repo.get("primaryLanguage") or {}
    topics = [n["topic"]["name"] for n in (repo.get("repositoryTopics") or {}).get("nodes", [])]
    repo["topics"] = topics
    toks = tokens_for(repo, tags)
    readme = ""
    for i in range(len(README_NAMES)):
        blob = repo.get(f"r{i}")
        if blob and blob.get("text"):
            readme = blob["text"]
            break
    paras = readme_text(readme)
    desc = (repo.get("description") or "").strip()
    if same_words(desc, repo["name"]):
        desc = ""  # "aws-ecs-playground" says nothing the name doesn't
    langs = []
    total = (repo.get("languages") or {}).get("totalSize") or 0
    for e in (repo.get("languages") or {}).get("edges", []):
        pct = round(100 * e["size"] / total) if total else 0
        if pct >= 1:
            langs.append([e["node"]["name"], pct])
    areas = classify(toks, cfg["areas"])
    out = {
        "name": repo["name"],
        "desc": desc or summary_from(paras),
        "lang": lang.get("name") or "",
        "langs": langs,
        "areas": areas,
        "_tracks": [t["key"] for t in cfg["tracks"] if matches(toks, t)],
        "_depth": {t["key"]: len(toks & set(t["match"])) for t in cfg["tracks"]},
        "tags": display_tags(toks | set(topics), vocab, lang.get("name")),
        "kind": "fork" if repo["isFork"] else ("playground" if "playground" in repo["name"].lower() else "project"),
        "stars": repo["stargazerCount"],
        "created": repo["createdAt"][:10],
        "pushed": repo["pushedAt"][:10] if repo.get("pushedAt") else repo["createdAt"][:10],
        "_size": repo.get("diskUsage") or 0,
        "readme": clip(" ".join(paras), 600),
        "post": repo["name"].lower() in posted,
    }
    home = safe_url(repo.get("homepageUrl"))
    if home:
        out["homepage"] = home
    if (repo.get("licenseInfo") or {}).get("spdxId") not in (None, "NOASSERTION"):
        out["license"] = repo["licenseInfo"]["spdxId"]
    if repo.get("parent"):
        out["parent"] = repo["parent"]["nameWithOwner"]
    if repo.get("isArchived"):
        out["archived"] = True
    return out, lang


def build(raw, posts, cfg, today):
    vocab = set(cfg.get("vocab", []))
    for group in cfg["areas"] + cfg["tracks"]:
        vocab |= set(group["match"])
    for tags in posts.values():
        vocab |= tags
    vocab -= set(cfg.get("not_tags", []))

    repos, colors = [], {}
    for r in sorted(raw, key=lambda r: r["name"].lower()):
        tags = posts.get(r["name"].lower(), set())
        item, lang = slim(r, tags, cfg, vocab, posts)
        for name, color in [(lang.get("name"), lang.get("color"))] + [
                (e["node"]["name"], e["node"]["color"]) for e in (r.get("languages") or {}).get("edges", [])]:
            if name and color:
                colors[name] = color
        repos.append(item)

    tracks = []
    for t in cfg["tracks"]:
        members = [r for r in repos if t["key"] in r["_tracks"] and r["kind"] != "fork"]
        members.sort(key=lambda r: beginner_score(r, r["_depth"][t["key"]]), reverse=True)
        tracks.append({"key": t["key"], "icon": t["icon"], "repos": [r["name"] for r in members]})

    # Working fields for ranking only; the page never reads them.
    for r in repos:
        for k in [k for k in r if k.startswith("_")]:
            del r[k]
    return {
        "user": USER,
        "updated": today,
        "count": len(repos),
        "areas": [{"key": a["key"], "icon": a["icon"]} for a in cfg["areas"]] + [{"key": "other", "icon": "i-doc"}],
        "tracks": tracks,
        "colors": dict(sorted(colors.items())),
        "repos": repos,
    }


# A partial API answer must never empty the page: a drop this large is far
# more likely a GitHub hiccup than a week of deleting repos.
MAX_DROP = 0.10


def decide(new, old, force=False):
    """What to do with a freshly built doc given the committed one:
    "same" (nothing but the date moved -- leave the file alone, so a weekly
    run with no news makes no commit), "shrunk" (refuse), or "write"."""
    if old is None:
        return "write"
    strip = lambda d: {k: v for k, v in d.items() if k != "updated"}
    if strip(new) == strip(old):
        return "same"
    if not force and new["count"] < old.get("count", 0) * (1 - MAX_DROP):
        return "shrunk"
    return "write"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cached", action="store_true", help="reuse the last fetch instead of calling GitHub")
    ap.add_argument("--force", action="store_true", help="write even if more than 10%% of repos vanished")
    args = ap.parse_args()
    cfg = json.loads(CONFIG.read_text())
    if args.cached and CACHE.exists():
        raw = json.loads(CACHE.read_text())
    else:
        raw = fetch_all()
        CACHE.parent.mkdir(exist_ok=True)
        CACHE.write_text(json.dumps(raw))
    doc = build(raw, post_tags(), cfg, datetime.date.today().isoformat())
    old = json.loads(OUT.read_text()) if OUT.exists() else None
    verdict = decide(doc, old, args.force)
    if verdict == "same":
        print(f"{OUT.relative_to(ROOT)}: unchanged ({doc['count']} repos)")
        return
    if verdict == "shrunk":
        sys.exit(f"refresh: {doc['count']} repos, down from {old['count']}; not writing "
                 f"(re-run with --force if that is real)")
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    kinds = {}
    for r in doc["repos"]:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    other = sum(1 for r in doc["repos"] if r["areas"] == ["other"])
    print(f"wrote {OUT.relative_to(ROOT)}: {doc['count']} repos {kinds}, {other} unclassified")
    for t in doc["tracks"]:
        print(f"  track {t['key']:<12} {len(t['repos'])}")


if __name__ == "__main__":
    main()
