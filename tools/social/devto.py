#!/usr/bin/env python3
"""Cross-post the architecture guides to dev.to as drafts, canonical to this site.

    python3 tools/social/devto.py                      # convert only: build/devto/*.md
    python3 tools/social/devto.py --push               # create/update drafts on dev.to
    python3 tools/social/devto.py --push --only compute-ladder

Every article goes up as a *draft* with canonical_url pointing back here,
so Google keeps crediting brianpfeil.com and nothing is public until you
press Publish on dev.to. Running it again updates the same drafts rather
than making new ones: tools/social/devto.json maps each guide to its dev.to
article id, and when that file doesn't know a guide, your existing dev.to
articles are searched by canonical URL first. A guide already published on
dev.to is left alone unless you pass --update-published.

What changes on the way (dev.to renders plain Markdown, not Hugo):
  - callouts become blockquotes ("**Key point:**" / "**Watch out:**")
  - inline SVG diagrams become a line describing the diagram, linked to the
    original, since dev.to can't show inline SVG
  - site-relative links become absolute; "{#id}" heading anchors go
  - checklists "- [ ]" become "- ☐"
  - the site's share card is the cover image, the guides form one series,
    and a footer links the original (utm_source=devto)

Needs DEVTO_API_KEY (dev.to → Settings → Extensions → DEV Community API
Keys) for --push. DEVTO_ORG_ID optionally posts under an organization you
belong to (e.g. AWS Community Builders).

Standard library only.
"""

import argparse
import json
import os
import re
import sys
import time
import tomllib
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit  # noqa: E402
import post  # noqa: E402  (http + page_meta)

REPO = Path(__file__).resolve().parents[2]
GUIDES = REPO / "content" / "architecture"
LEDGER = Path(__file__).resolve().parent / "devto.json"
OUT = Path(__file__).resolve().parent / "build" / "devto"
API = "https://dev.to/api"
SERIES = "Cloud Architecture Guides"
LABEL = {"key": "Key point", "warn": "Watch out"}


class DevtoError(Exception):
    pass


# ---------------------------------------------------------------- convert

def read_guide(path):
    text = path.read_text()
    m = re.match(r"\+\+\+\n(.*?)\n\+\+\+\n", text, re.S)
    if not m:
        raise ValueError(f"{path.name}: no TOML front matter")
    fm = tomllib.loads(m.group(1))
    return fm, text[m.end():]


def canonical(fm, path):
    return f"{kit.SITE}/architecture/{fm.get('slug', path.stem)}/"


def tracked(url):
    return url + "?" + urllib.parse.urlencode({"utm_source": "devto", "utm_medium": "crosspost",
                                               "utm_campaign": "guide"})


def convert(body, url):
    """Hugo guide Markdown -> dev.to Markdown."""
    def callout(m):
        kind = m.group(1) or "key"
        inner = m.group(2).strip()
        lines = f"**{LABEL.get(kind, 'Note')}:** {inner}".split("\n")
        return "\n".join("> " + l if l.strip() else ">" for l in lines)

    body = re.sub(r'\{\{<\s*callout(?:\s+"(\w+)")?\s*>\}\}(.*?)\{\{<\s*/callout\s*>\}\}', callout, body, flags=re.S)

    def diagram(m):
        label = re.search(r'aria-label="([^"]*)"', m.group(1))
        what = label.group(1) if label else "A diagram"
        return f"*📐 Diagram — {what} ([see it in the original]({tracked(url)}))*"

    body = re.sub(r"\{\{<\s*diagram\s*>\}\}(.*?)\{\{<\s*/diagram\s*>\}\}", diagram, body, flags=re.S)
    # Relative links -> absolute (Markdown links and bare href="/...").
    body = re.sub(r"\]\((/[^)\s]*)\)", lambda m: f"]({kit.SITE}{m.group(1)})", body)
    body = re.sub(r"[ \t]*\{#[\w-]+\}[ \t]*$", "", body, flags=re.M)
    body = re.sub(r"^(\s*)- \[ \] ", r"\1- ☐ ", body, flags=re.M)
    body = re.sub(r"^(\s*)- \[[xX]\] ", r"\1- ☑ ", body, flags=re.M)
    leftover = re.findall(r"\{\{[<%].*?[>%]\}\}", body)
    if leftover:
        raise ValueError(f"unconverted shortcode(s): {leftover[:3]}")
    footer = (f"\n\n---\n\n*Originally published at [brianpfeil.com]({tracked(url)}), "
              f"part of a series of cloud architecture guides drawn from the reviews I run.*\n")
    return body.strip() + footer


def tags(fm):
    """dev.to allows four tags, lowercase alphanumeric."""
    out = []
    for t in fm.get("tags", []):
        t = re.sub(r"[^a-z0-9]", "", t.lower())
        if t and t not in out:
            out.append(t)
    return out[:4]


def article(path, fm, body, cover=None, org=None):
    url = canonical(fm, path)
    a = {
        "title": fm["title"],
        "body_markdown": convert(body, url),
        "published": False,
        "canonical_url": url,
        "description": fm.get("description", "")[:250],
        "tags": tags(fm),
        "series": SERIES,
    }
    if cover:
        a["main_image"] = cover
    if org:
        a["organization_id"] = int(org)
    return a


def guides(only=None):
    out = []
    for f in sorted(GUIDES.glob("*.md")):
        if f.name.startswith("_"):
            continue
        fm, body = read_guide(f)
        slug = fm.get("slug", f.stem)
        if fm.get("draft") or (only and slug not in only):
            continue
        out.append((f, fm, body, slug))
    return sorted(out, key=lambda g: g[1].get("weight", 0))


# ---------------------------------------------------------------- api

def api(send, method, path, key, body=None):
    data = None if body is None else json.dumps(body).encode()
    headers = {"api-key": key, "Accept": "application/vnd.forem.api-v1+json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    for attempt in range(4):
        status, _, raw = send(method, f"{API}{path}", headers=headers, data=data)
        if status == 429 and attempt < 3:  # dev.to rate-limits article writes
            time.sleep(10 * (attempt + 1))
            continue
        if status >= 300:
            raise DevtoError(f"{method} {path} -> HTTP {status}: {raw[:300].decode('utf-8', 'replace')}")
        return json.loads(raw or b"null")


def my_articles(send, key):
    """Every article of yours, drafts included, keyed by canonical URL."""
    out, page = {}, 1
    while True:
        batch = api(send, "GET", f"/articles/me/all?per_page=100&page={page}", key)
        for a in batch or []:
            if a.get("canonical_url"):
                out[a["canonical_url"].rstrip("/") + "/"] = a
        if not batch or len(batch) < 100:
            return out
        page += 1


def load_ledger(path=LEDGER):
    return json.loads(path.read_text()) if path.exists() else {}


def save_ledger(ledger, path=LEDGER):
    path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")


# ---------------------------------------------------------------- run

def run(*, push, env, only=None, update_published=False, send=post.http, ledger_path=LEDGER,
        out=OUT, log=print, pause=3):
    items = guides(only)
    if not items:
        log("no guides matched")
        return 1
    key = env.get("DEVTO_API_KEY")
    if push and not key:
        log("DEVTO_API_KEY is not set (dev.to → Settings → Extensions → DEV Community API Keys)")
        return 1
    out.mkdir(parents=True, exist_ok=True)
    ledger = load_ledger(ledger_path)
    mine = my_articles(send, key) if push else {}
    failed = 0
    for i, (path, fm, body, slug) in enumerate(items):
        url = canonical(fm, path)
        meta = post.page_meta(send, url) if push else None
        if push and meta is None:
            log(f"{slug}: skipped, {url} doesn't load")
            failed += 1
            continue
        a = article(path, fm, body, cover=(meta or {}).get("image") or None, org=env.get("DEVTO_ORG_ID"))
        (out / f"{slug}.md").write_text(f"# {a['title']}\n\n{a['body_markdown']}")
        if not push:
            log(f"{slug}: converted -> {out / (slug + '.md')} (tags: {', '.join(a['tags'])})")
            continue
        existing = ledger.get(slug, {}).get("id")
        found = mine.get(url)
        if not existing and found:
            existing = found["id"]
        if existing and (found or {}).get("published") and not update_published:
            log(f"{slug}: already published on dev.to ({found.get('url')}); left alone (--update-published to overwrite)")
            ledger[slug] = {"id": existing, "url": found.get("url")}
            continue
        if existing and found and found.get("published"):
            a.pop("published")  # updating a live article must not unpublish it
        try:
            if existing:
                res = api(send, "PUT", f"/articles/{existing}", key, {"article": a})
                verb = "updated"
            else:
                res = api(send, "POST", "/articles", key, {"article": a})
                verb = "created draft"
        except DevtoError as e:
            log(f"{slug}: FAILED: {e}")
            failed += 1
            continue
        ledger[slug] = {"id": res["id"], "url": res.get("url")}
        save_ledger(ledger, ledger_path)
        log(f"{slug}: {verb} {res.get('url')}")
        if pause and i < len(items) - 1:
            time.sleep(pause)
    if push:
        save_ledger(ledger, ledger_path)
        log("Drafts: https://dev.to/dashboard — review each, then Publish.")
    return 1 if failed else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--push", action="store_true", help="create/update drafts on dev.to (default: convert only)")
    ap.add_argument("--only", nargs="+", metavar="SLUG", help="just these guides")
    ap.add_argument("--update-published", action="store_true", help="also overwrite articles already published there")
    a = ap.parse_args(argv)
    return run(push=a.push, env=os.environ, only=a.only, update_published=a.update_published)


if __name__ == "__main__":
    sys.exit(main())
