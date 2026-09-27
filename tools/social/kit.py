#!/usr/bin/env python3
"""Build a posting kit for the site's teaching content: every /learn/ path,
every course and every architecture guide, with copy sized for each channel
and a one-click composer link where the channel has one.

    python3 tools/social/kit.py                 # writes tools/social/build/
    python3 tools/social/kit.py --start 2026-10-05

Nothing is posted: the kit is a local page (build/kit.html) you open, read,
and press "Post" from, so every post goes out under your own eyes. Links
carry utm_source/utm_campaign so Google Analytics shows which channel sent
whom (the canonical link on every page keeps search engines on the clean
URL).

Order is priority order: the "people I follow" path first, then the AI
paths, the rest of /learn/, the courses and the guides. The calendar
spreads them one per weekday from --start (default: next Monday).

Standard library only; deterministic for a given repo state and --start.
"""

import argparse
import datetime as dt
import html
import json
import re
import tomllib
import urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SITE = "https://brianpfeil.com"
OUT = Path(__file__).resolve().parent / "build"

# Hard limits per channel. X counts any link as 23 characters.
X_MAX, X_URL = 280, 23
BSKY_MAX = 300
THREADS_MAX = 500
MASTODON_MAX = 500

# X handles for the people path, in B's priority order. Only X gets @s:
# the handles elsewhere differ or don't exist.
PEOPLE_X = {
    "Simon Willison": "simonw",
    "Lex Fridman": "lexfridman",
    "Andrew Huberman": "hubermanlab",
    "Addy Osmani": "addyosmani",
    "Mitchell Hashimoto": "mitchellh",
    "Pieter Levels (@levelsio)": "levelsio",
}

# What each one teaches, for the people post (English; posts are English).
PEOPLE_TOPIC = {
    "Simon Willison": "building with LLMs",
    "Lex Fridman": "long-form interviews",
    "Andrew Huberman": "sleep, focus, learning",
    "Addy Osmani": "web + AI coding",
    "Mitchell Hashimoto": "systems + agents",
    "Pieter Levels (@levelsio)": "shipping solo",
}

# Learn paths in posting order; anything new in learn.json goes after these.
PATH_ORDER = ["people", "ai", "models", "code", "cloud", "university", "kids", "papers"]

# Where each piece fits on Reddit. Read each subreddit's self-promotion rule
# before posting; most want the post to stand on its own.
SUBREDDITS = {
    "learn:people": ["learnprogramming"],
    "learn:ai": ["learnmachinelearning", "MachineLearning"],
    "learn:models": ["ClaudeAI", "LocalLLaMA"],
    "learn:code": ["learnprogramming", "learnjavascript"],
    "learn:cloud": ["aws", "AWSCertifications", "Terraform"],
    "learn:university": ["learnprogramming", "compsci"],
    "learn:kids": ["homeschool", "teachers"],
    "learn:papers": ["compsci", "programming"],
    "learn": ["learnprogramming", "InternetIsBeautiful"],
    "guide": ["softwarearchitecture", "aws", "ExperiencedDevs"],
    "course": ["learnprogramming"],
}
COURSE_SUBS = {
    "terraform": ["Terraform", "devops"], "pytorch": ["pytorch", "learnmachinelearning"],
    "stripe": ["stripe", "webdev"], "ebpf": ["linux", "kernel"], "nix": ["NixOS"],
    "mlx": ["LocalLLaMA", "apple"], "v8": ["javascript", "node"], "cpp": ["cpp_questions", "cpp"],
    "rust": ["learnrust"], "go": ["golang"], "agent": ["ClaudeAI", "LLMDevs"],
}


# ---------------------------------------------------------------- content

def load_en():
    return tomllib.loads((REPO / "i18n" / "en.toml").read_text())


def t(en, key):
    v = en.get(key, {})
    return v.get("other", "") if isinstance(v, dict) else str(v)


def front_matter(path):
    text = path.read_text()
    m = re.match(r"\+\+\+\n(.*?)\n\+\+\+", text, re.S)
    return tomllib.loads(m.group(1)) if m else {}


def learn_items(en):
    data = json.loads((REPO / "data" / "learn.json").read_text())
    rank = {k: i for i, k in enumerate(PATH_ORDER)}
    paths = sorted(data["paths"], key=lambda p: rank.get(p["key"], len(rank)))
    out = []
    for p in paths:
        items = p["items"]
        picks = [i for i in items if i.get("pick")] or items[:2]
        out.append({
            "id": f"learn:{p['key']}",
            "kind": "learn",
            "title": t(en, f"learn_path_{p['key']}"),
            "blurb": t(en, f"learn_path_blurb_{p['key']}"),
            "path": f"/learn/#{p['key']}",
            "n": len(items),
            "names": [i.get("name") or i.get("key") for i in items],
            "picks": [label(i) for i in picks],
            "people": sorted({i["by"] for i in items if i.get("by")},
                             key=lambda b: list(PEOPLE_X).index(b) if b in PEOPLE_X else 99)
                      if p["key"] == "people" else [],
        })
    total = sum(len(p["items"]) for p in data["paths"])
    out.append({"id": "learn", "kind": "learn", "title": "Learn anything, free",
                "blurb": t(en, "learn_intro").replace("{count}", str(total)),
                "path": "/learn/", "n": total, "names": [], "picks": [], "people": []})
    return out


def label(item):
    name = item.get("name") or item.get("key")
    by = item.get("by")
    return f"{name} ({by})" if by and by not in name else name


def course_items():
    data = json.loads((REPO / "data" / "courses.json").read_text())
    out = []
    for c in data["courses"]:
        out.append({
            "id": f"course:{c['slug']}", "kind": "course", "title": c["title"],
            "blurb": c["description"], "path": f"/courses/{c['slug']}/",
            "n": len(c.get("lessons", [])), "names": [l["title"] for l in c.get("lessons", [])[:3]],
            "picks": [], "people": [], "slug": c["slug"],
        })
    return out


def guide_items():
    out = []
    for f in sorted((REPO / "content" / "architecture").glob("*.md")):
        if f.name.startswith("_"):
            continue
        fm = front_matter(f)
        if fm.get("draft"):
            continue
        out.append({
            "id": f"guide:{fm.get('slug', f.stem)}", "kind": "guide", "title": fm["title"],
            "blurb": fm.get("description", ""), "path": f"/architecture/{fm.get('slug', f.stem)}/",
            "weight": fm.get("weight", 0), "n": 0, "names": [], "picks": [], "people": [],
        })
    return sorted(out, key=lambda i: i["weight"])


# ---------------------------------------------------------------- copy

def link(item, source):
    base, _, frag = (SITE + item["path"]).partition("#")
    q = urllib.parse.urlencode({"utm_source": source, "utm_medium": "social", "utm_campaign": item["kind"]})
    return f"{base}?{q}" + (f"#{frag}" if frag else "")


def x_len(text):
    """Length as X counts it: every URL is 23."""
    return len(re.sub(r"https?://\S+", "x" * X_URL, text))


def fit(parts, url, limit, measure=len):
    """Join parts + url, dropping trailing parts until it fits."""
    parts = [p for p in parts if p]
    while parts:
        text = "\n\n".join(parts + [url])
        if measure(text) <= limit:
            return text
        if len(parts) == 1:
            head = parts[0]
            room = limit - measure("\n\n" + url) - 1
            return head[:room].rstrip() + "…\n\n" + url
        parts = parts[:-1]
    return url


def bullets(names, n=4):
    return "\n".join(f"→ {x}" for x in names[:n])


def hook(item):
    k = item["kind"]
    if item["id"] == "learn:people":
        return "The people I learn the most from, all free:"
    if item["id"] == "learn":
        return f"I put every free way to learn I'd recommend in one place: {item['n']} resources, sorted by goal, every link checked."
    if k == "learn":
        return f"{item['title']}: {item['n']} free resources, the ones I'd actually use."
    if k == "course":
        return f"Free course: {item['title']} ({item['n']} lessons)."
    return item["title"]


def body_lines(item, channel):
    if item["people"]:
        names = [(f"@{PEOPLE_X[p]}" if channel == "x" and p in PEOPLE_X else p.replace(" (@levelsio)", ""))
                 + (f": {PEOPLE_TOPIC[p]}" if p in PEOPLE_TOPIC else "")
                 for p in item["people"]]
        return bullets(names, 6)
    if item["picks"]:
        return "Start here:\n" + bullets(item["picks"], 3)
    if item["kind"] == "course" and item["names"]:
        return bullets(item["names"], 3)
    return ""


def copy_for(item):
    h = hook(item)
    b = "" if item["people"] else item["blurb"]
    posts = {}
    posts["x"] = fit([h, body_lines(item, "x"), b], link(item, "x"), X_MAX, x_len)
    posts["bluesky"] = fit([h, body_lines(item, "bluesky"), b], link(item, "bluesky"), BSKY_MAX)
    posts["threads"] = fit([h, body_lines(item, "threads"), b], link(item, "threads"), THREADS_MAX)
    posts["mastodon"] = fit([h, body_lines(item, "mastodon"), b, hashtags(item)], link(item, "mastodon"), MASTODON_MAX)
    posts["linkedin"] = linkedin(item)
    posts["facebook"] = "\n\n".join(p for p in [h, b, link(item, "facebook")] if p)
    return posts


def hashtags(item):
    tags = {"learn": "#learning #programming", "course": "#programming #learning", "guide": "#softwarearchitecture #aws #cloud"}
    return tags[item["kind"]]


def linkedin(item):
    # LinkedIn shows ~3 lines before "see more": lead with the point. The
    # link goes in the first comment (LinkedIn down-ranks posts with links).
    lines = [hook(item)] + ([] if item["people"] else ["", item["blurb"]])
    bl = body_lines(item, "linkedin")
    if bl:
        lines += ["", bl]
    lines += ["", "Link in the first comment."]
    return "\n".join(lines).strip()


def intents(item, posts):
    q = urllib.parse.quote
    subs = SUBREDDITS.get(item["id"]) or SUBREDDITS.get(item["kind"], [])
    if item["kind"] == "course":
        for key, extra in COURSE_SUBS.items():
            if key in item["slug"]:
                subs = extra + subs
    reddit_title = {"learn": f"{item['title']} – {item['n']} free resources",
                    "course": f"Free course: {item['title']} ({item['n']} lessons)"}.get(item["kind"], item["title"])
    return {
        "x": f"https://x.com/intent/post?text={q(posts['x'])}",
        "bluesky": f"https://bsky.app/intent/compose?text={q(posts['bluesky'])}",
        "threads": f"https://www.threads.net/intent/post?text={q(posts['threads'])}",
        "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url={q(link(item, 'linkedin'))}",
        "facebook": f"https://www.facebook.com/sharer/sharer.php?u={q(link(item, 'facebook'))}",
        "hn": f"https://news.ycombinator.com/submitlink?u={q(SITE + item['path'].split('#')[0])}&t={q(item['title'])}",
        "reddit": [{"sub": s, "url": f"https://www.reddit.com/r/{s}/submit?url={q(link(item, 'reddit'))}&title={q(reddit_title)}"}
                   for s in dict.fromkeys(subs)][:3],
    }


# ---------------------------------------------------------------- calendar

def weekdays(start):
    d = start
    while True:
        if d.weekday() < 5:
            yield d
        d += dt.timedelta(days=1)


def next_monday(today):
    return today + dt.timedelta(days=(7 - today.weekday()) % 7 or 7)


def build(start):
    en = load_en()
    items = learn_items(en) + guide_items() + course_items()
    days = weekdays(start)
    for it in items:
        it["posts"] = copy_for(it)
        it["intents"] = intents(it, it["posts"])
        it["date"] = next(days).isoformat()
        it["url"] = SITE + it["path"]
    return items


# ---------------------------------------------------------------- output

CHANNELS = [("x", "X"), ("bluesky", "Bluesky"), ("threads", "Threads"), ("mastodon", "Mastodon"),
            ("linkedin", "LinkedIn"), ("facebook", "Facebook")]

PAGE = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Social kit</title>
<style>
:root{--bg:#fff;--fg:#111;--mut:#666;--card:#f6f7f9;--line:#e3e5e8;--acc:#0d7ea8}
@media (prefers-color-scheme:dark){:root{--bg:#0f1115;--fg:#eee;--mut:#9aa;--card:#171a20;--line:#2a2f37;--acc:#5ec8ee}}
body{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;margin:0 auto;max-width:980px;padding:24px 16px}
h1{margin:0 0 4px}.mut{color:var(--mut)}
.item{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:18px 0}
.item h2{font-size:18px;margin:0 0 2px}.meta{font-size:13px;color:var(--mut)}
.item.done{opacity:.55}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:10px;margin-top:12px}
.ch{border:1px solid var(--line);border-radius:8px;padding:10px;background:var(--bg)}
.ch b{font-size:13px}.ch pre{white-space:pre-wrap;font:13px/1.45 system-ui,sans-serif;margin:6px 0;max-height:220px;overflow:auto}
.n{font-size:12px;color:var(--mut)}
a.btn,button{font:inherit;font-size:13px;border:1px solid var(--acc);color:var(--acc);background:none;border-radius:6px;padding:3px 9px;cursor:pointer;text-decoration:none;margin-right:6px}
.row{margin-top:10px;display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:13px}
label.dn{margin-left:auto}
</style>
<h1>Social kit</h1>
<p class="mut">__N__ posts, one per weekday from __START__. Generated by <code>tools/social/kit.py</code>. "Open" pre-fills the composer; nothing posts until you press Post there. Ticks are remembered in this browser only.</p>
__ITEMS__
<script>
document.addEventListener("click",function(e){var b=e.target.closest("button[data-copy]");if(!b)return;
var t=document.getElementById(b.dataset.copy).textContent;navigator.clipboard.writeText(t).then(function(){b.textContent="Copied";setTimeout(function(){b.textContent="Copy"},1200)})});
document.querySelectorAll("input[data-done]").forEach(function(c){var k="kit:"+c.dataset.done;try{c.checked=localStorage.getItem(k)==="1"}catch(e){}
c.closest(".item").classList.toggle("done",c.checked);c.addEventListener("change",function(){try{localStorage.setItem(k,c.checked?"1":"0")}catch(e){}c.closest(".item").classList.toggle("done",c.checked)})});
</script>
"""


def render(items, start):
    e = html.escape
    blocks = []
    for n, it in enumerate(items):
        chans = []
        for key, name in CHANNELS:
            text = it["posts"][key]
            pid = f"p{n}-{key}"
            count = f"{x_len(text)}/{X_MAX}" if key == "x" else f"{len(text)} chars"
            open_ = it["intents"].get(key)
            chans.append(
                f'<div class="ch"><b>{name}</b> <span class="n">{count}</span>'
                f'<pre id="{pid}">{e(text)}</pre>'
                f'<button type="button" data-copy="{pid}">Copy</button>'
                + (f'<a class="btn" href="{e(open_)}" target="_blank" rel="noopener">Open</a>' if open_ else "")
                + (f'<span class="n">first comment: {e(link(it, "linkedin"))}</span>' if key == "linkedin" else "")
                + "</div>")
        reddit = " ".join(f'<a class="btn" href="{e(r["url"])}" target="_blank" rel="noopener">r/{e(r["sub"])}</a>'
                          for r in it["intents"]["reddit"])
        blocks.append(
            f'<section class="item"><h2>{e(it["title"])}</h2>'
            f'<div class="meta">{e(it["date"])} · {e(it["kind"])} · <a href="{e(it["url"])}">{e(it["url"])}</a></div>'
            f'<div class="grid">{"".join(chans)}</div>'
            f'<div class="row">Reddit: {reddit or "—"} '
            f'<a class="btn" href="{e(it["intents"]["hn"])}" target="_blank" rel="noopener">Hacker News</a>'
            f'<label class="dn"><input type="checkbox" data-done="{e(it["id"])}"> posted</label></div></section>')
    return (PAGE.replace("__N__", str(len(items))).replace("__START__", start.isoformat())
            .replace("__ITEMS__", "\n".join(blocks)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--start", type=dt.date.fromisoformat, help="first posting day (default: next Monday)")
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args(argv)
    start = a.start or next_monday(dt.date.today())
    items = build(start)
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "kit.json").write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n")
    (a.out / "kit.html").write_text(render(items, start))
    print(f"{len(items)} posts, {items[0]['date']} to {items[-1]['date']}: {a.out / 'kit.html'}")


if __name__ == "__main__":
    main()
