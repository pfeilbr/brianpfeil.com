#!/usr/bin/env python3
"""Render check for the site's structure (2026-10 usability pass).

What it holds in place, on a built site (hugo --minify first):

  - the nav row has the six section links, in every language;
  - the home page leads with the three calls to action and the guides card;
  - /post/ lists articles only and /notes/ lists lab notes only (a lab note
    is a generated-*.md post; see the cascade in content/post/_index.md),
    and both exist in every language;
  - a project's old /post/ URL redirects to its /projects/ page, and the
    README post is not published on its own;
  - a lab note whose repo is gone (data/repo_gone.json) links to it nowhere
    on its page;
  - every page with a table of contents marks its article .has-toc, so the
    contents become the sidebar on wide screens;
  - no built page, feed or index shows B's own AWS account number (the
    generator's local_setup accounts; examples use 123456789012).

    python3 tools/site-check/check_structure.py --public public

Exit status 1 on any problem. Standard library only.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LANGS = ("en", "zh", "es", "pt", "fr", "de", "it", "ja", "ko")
NAV = ("architecture", "courses", "learn", "post", "projects", "about")

FRONT = re.compile(r"\A\+\+\+\n(.*?)\n\+\+\+", re.S)
ROW = re.compile(r'<article class="?post-preview post-row[^>]*data-href="?([^">\s]+)')


def front(path: Path) -> str:
    m = FRONT.match(path.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def field(fm: str, key: str) -> str:
    m = re.search(rf'^{key}\s*=\s*"([^"]*)"', fm, re.M)
    return m.group(1) if m else ""


def notes(content: Path) -> dict[str, dict]:
    """Published lab notes by slug: {slug: {"repo", "project"}}."""
    out = {}
    for f in sorted((content / "post").glob("generated-*.md")):
        fm = front(f)
        if re.search(r"^draft\s*=\s*true", fm, re.M):
            continue
        out[field(fm, "slug")] = {
            "repo": field(fm, "repoFullName"),
            "project": bool(re.search(r'^\[build\]\n\s*list = "never"', fm, re.M)),
        }
    return out


def project_aliases(content: Path) -> dict[str, str]:
    """Old URL -> project page path, from each project's English front matter."""
    out = {}
    for f in sorted((content / "projects").glob("*/index.md")):
        m = re.search(r"^aliases\s*=\s*\[(.*)\]", front(f), re.M)
        for alias in re.findall(r'"([^"]+)"', m.group(1)) if m else []:
            out[alias] = f"/projects/{f.parent.name}/"
    return out


GENERATOR_CONFIG = REPO / "tools" / "generate-posts" / "config.yaml"


def own_accounts(config: Path = GENERATOR_CONFIG) -> list[str]:
    """local_setup.accounts from the generator config (no YAML library)."""
    m = re.search(r"^  accounts:\n((?:\s+- \"?\d{12}\"?\n)+)", config.read_text(encoding="utf-8"), re.M)
    return re.findall(r"\d{12}", m.group(1)) if m else []


def account_leaks(public: Path, accounts: list[str]) -> list[str]:
    """Built text files (pages, feeds, search index, llms.txt) naming one."""
    hits = []
    for f in sorted(public.rglob("*")):
        if f.suffix in (".html", ".xml", ".json", ".txt") and f.is_file():
            text = f.read_text(encoding="utf-8", errors="ignore")
            hits += [f"/{f.relative_to(public)}: shows account {a}" for a in accounts if a in text]
    return hits


def page(public: Path, lang: str, path: str) -> Path:
    return public / ("" if lang == "en" else lang) / path.strip("/") / "index.html"


def nav_links(html: str) -> list[str]:
    m = re.search(r'class="?nav-wide[^>]*>(.*?)<button', html, re.S)
    return re.findall(r'<a href="?([^">\s]+)', m.group(1)) if m else []


def rows(html: str) -> list[str]:
    return ROW.findall(html)


def slug_of(href: str) -> str:
    m = re.search(r"/post/([^/]+)/", href)
    return m.group(1) if m else ""


def check(public: Path, content: Path = REPO / "content", data: Path = REPO / "data",
          accounts: list[str] | None = None) -> list[str]:
    errors = account_leaks(public, own_accounts() if accounts is None else accounts)
    lab = notes(content)
    note_slugs = {s for s, n in lab.items() if not n["project"]}
    for lang in LANGS:
        pre = "" if lang == "en" else f"/{lang}"
        home = page(public, lang, "")
        if not home.exists():
            errors.append(f"/{lang}/: not built")
            continue
        html = home.read_text(encoding="utf-8")
        want = [f"{pre}/{p}/" for p in NAV]
        if nav_links(html) != want:
            errors.append(f"/{lang}/ nav: {nav_links(html)} != {want}")
        cta = re.search(r'class="?hub-cta"?.*?</nav>', html, re.S)
        if not cta or len(re.findall(r"<a ", cta.group(0))) != 3:
            errors.append(f"/{lang}/: home page has no three calls to action")
        if "hub-guides" not in html:
            errors.append(f"/{lang}/: home page has no guides card")
        for path, kind in (("post", "article"), ("notes", "note")):
            f = page(public, lang, path)
            if not f.exists():
                errors.append(f"/{lang}/{path}/: not built")
                continue
            listed = [slug_of(h) for h in rows(f.read_text(encoding="utf-8"))]
            if not listed:
                errors.append(f"/{lang}/{path}/: lists nothing")
            wrong = [s for s in listed if (s in note_slugs) != (kind == "note")]
            if wrong:
                errors.append(f"/{lang}/{path}/: lists {len(wrong)} that are not {kind}s, e.g. {wrong[0]}")
    for alias, target in project_aliases(content).items():
        f = public / alias.strip("/") / "index.html"
        text = f.read_text(encoding="utf-8") if f.exists() else ""
        if target not in text or "post-row" in text or "<article" in text:
            errors.append(f"{alias}: should only redirect to {target}")
    gone = set(json.loads((data / "repo_gone.json").read_text()).get("repos", [])) \
        if (data / "repo_gone.json").exists() else set()
    for slug, n in lab.items():
        if n["repo"] in gone and not n["project"]:
            f = page(public, "en", f"post/{slug}")
            if f.exists() and re.search(r'href="?https://github\.com/' + re.escape(n["repo"]) + r'(?=[/"\s>#?])',
                                        f.read_text(encoding="utf-8")):
                errors.append(f"/post/{slug}/: links {n['repo']}, which is gone")
    for f in sorted((public / "post").glob("*/index.html")):
        text = f.read_text(encoding="utf-8")
        if 'class="toc"' in text or "class=toc" in text:
            if not re.search(r'<article class="?has-toc', text):
                errors.append(f"/post/{f.parent.name}/: contents without the has-toc article")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--public", type=Path, default=Path("public"))
    errors = check(ap.parse_args().public)
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    if errors:
        return 1
    print(f"ok: nav, home, articles vs lab notes, project redirects, gone repos and no own account number in all {len(LANGS)} languages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
