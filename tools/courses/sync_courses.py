#!/usr/bin/env python3
"""Publish the /teach courses from the learn project to /courses/.

Each course in the learn project (~/projects/learn/public/courses/<slug>/) is
a /teach workspace. Only the parts meant for any reader are published:

    lessons/*.html     -> static/courses/<slug>/lessons/
    reference/*.html   -> static/courses/<slug>/reference/
    course.json, the lesson and reference titles, RESOURCES.md
                       -> data/courses.json (drawn by /courses/ and each
                          course page)
                       -> content/courses/<slug>/index.md (the course page)

MISSION.md, NOTES.md and learning-records/ describe the learner, not the
subject, and never leave the learn project. Every published page goes
through the `redact` rules in config.json and is then checked against the
`deny` patterns; a hit stops the sync before anything is written.

Links inside a lesson to files that aren't published (RESOURCES.md, the
workspace index, a learning record) are pointed at the course page instead,
so nothing on the site 404s.

    python3 tools/courses/sync_courses.py            # write
    python3 tools/courses/sync_courses.py --check    # report only; exit 1 on a deny hit

Re-running is a no-op when nothing changed. Courses that disappear from the
source (or are listed under `exclude`) are removed from the site.
Standard library only.
"""

import html
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from posixpath import normpath

REPO = Path(__file__).resolve().parents[2]
CONFIG = Path(__file__).with_name("config.json")
STATIC = REPO / "static" / "courses"
CONTENT = REPO / "content" / "courses"
DATA = REPO / "data" / "courses.json"
PUBLISHED_DIRS = ("lessons", "reference")

TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
LESSON_PREFIX = re.compile(r"^Lesson\s+\d+\s*[·:\-–—]\s*", re.I)
LINK_ATTR = re.compile(r'(\b(?:href|src)=")([^"]*)(")')
MD_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
BARE_URL = re.compile(r"https?://[^\s)>\]]+")
TAG = re.compile(r"<[^>]+>")


class PrivacyError(Exception):
    pass


def load_config(path: Path = CONFIG) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg["source"] = str(Path(cfg["source"]).expanduser())
    return cfg


def category_key(category: str) -> str:
    """"AI & ML" -> "ai_ml": the suffix of its i18n key, course_cat_<key>."""
    return re.sub(r"[^a-z0-9]+", "_", category.lower()).strip("_") or "other"


def page_title(text: str, lesson: bool) -> str:
    m = TITLE.search(text)
    title = html.unescape(re.sub(r"\s+", " ", TAG.sub("", m.group(1))).strip()) if m else ""
    return LESSON_PREFIX.sub("", title) if lesson else title


def redact(text: str, rules: list) -> str:
    for pattern, repl in rules:
        text = re.sub(pattern, repl, text)
    return text


def deny_hits(text: str, patterns: list) -> list[str]:
    hits = []
    for p in patterns:
        for m in re.finditer(p, text):
            start = max(0, m.start() - 30)
            hits.append(f"{p!r}: …{text[start:m.end() + 30]!r}…")
    return hits


BODY = re.compile(r"<body[^>]*>", re.I)


def site_bar(text: str, slug: str, course_title: str) -> str:
    """A one-line way back to the course and the site, for a reader who lands
    on a lesson from a search. Inline styles only: lessons carry their own
    stylesheet and theme, and this has to sit on top of any of them."""
    bar = (
        '<nav data-site-bar style="font:600 13px/1.4 system-ui,-apple-system,sans-serif;'
        'padding:10px 16px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;'
        'border-bottom:1px solid rgba(127,127,127,.25)">'
        f'<a href="/courses/{slug}/" style="color:inherit;text-decoration:none">&larr; {html.escape(course_title)}</a>'
        '<span style="opacity:.4">·</span>'
        '<a href="/courses/" style="color:inherit;text-decoration:none;opacity:.7">Courses</a>'
        '<span style="opacity:.4">·</span>'
        '<a href="/" style="color:inherit;text-decoration:none;opacity:.7">Home</a>'
        '</nav>'
    )
    # The real <body>, after </head>: the lesson theme's CSS comments
    # mention "<body>" too.
    head_end = text.lower().find("</head>")
    m = BODY.search(text, head_end if head_end != -1 else 0)
    return text[:m.end()] + bar + text[m.end():] if m else text


def rewrite_links(text: str, slug: str, here: str, published: set[str]) -> str:
    """Point relative links at files that won't exist on the site to the
    course page. `here` is the page's own directory within the course
    ("lessons" or "reference"); `published` holds "lessons/x.html" paths."""
    course_page = f"/courses/{slug}/"

    def fix(m):
        url = m.group(2)
        if not url or re.match(r"^(?:[a-z][a-z0-9+.-]*:|#|/|\{)", url, re.I):
            return m.group(0)
        path, _, frag = url.partition("#")
        target = normpath(f"{here}/{path}")
        if target in published:
            return m.group(0)
        if target.startswith("../"):
            new = "/courses/"  # above the course: the old all-courses index
        elif target == "RESOURCES.md":
            new = course_page + "#resources"
        else:
            new = course_page
        return m.group(1) + new + m.group(3)

    return LINK_ATTR.sub(fix, text)


def _clean(text: str) -> str:
    text = MD_LINK.sub(r"\1", text)
    return re.sub(r"[`*_]", "", text).strip(" —–-:")


def _bullet(text: str) -> tuple[list[dict], str]:
    """One bullet's links and note, in either shape /teach writes:
    "[Title](url) · [Other](url)" with the note on the next line, or
    "**Title** — https://url — note" with bare urls."""
    links = [{"title": t.strip(), "url": u} for t, u in MD_LINK.findall(text)]
    if links:
        return links, ""
    m = BARE_URL.search(text)
    if not m:
        return [], ""
    bold = re.search(r"\*\*(.+?)\*\*", text[:m.start()])
    title = _clean(bold.group(1) if bold else text[:m.start()]) or m.group(0)
    return [{"title": title, "url": m.group(0).rstrip(".,;)")}], _clean(text[m.end():])


def parse_resources(text: str) -> list[dict]:
    """RESOURCES.md -> [{section, items: [{links: [{title, url}], note}]}]."""
    sections, current, item = [], None, None
    for line in text.splitlines():
        if line.startswith("## "):
            current = {"section": _clean(line[3:]), "items": []}
            sections.append(current)
            item = None
        elif line.startswith("- ") and current is not None:
            links, note = _bullet(line[2:])
            item = {"links": links, "note": note} if links else None
            if item:
                current["items"].append(item)
        elif item is not None and line.startswith("  ") and line.strip():
            sub = line.strip()
            if sub.startswith("- "):
                links, note = _bullet(sub[2:])
                if links:
                    item["links"] += links
                    continue
                sub = sub[2:]
            item["note"] = (item["note"] + " " + _clean(sub)).strip()
    return [s for s in sections if s["items"]]


def last_updated(course_dir: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(course_dir), "log", "-1", "--format=%cs", "--", "."],
            capture_output=True, text=True, check=True).stdout.strip()
        if out:
            return out
    except (OSError, subprocess.CalledProcessError):
        pass
    newest = max(p.stat().st_mtime for p in course_dir.rglob("*") if p.is_file())
    return date.fromtimestamp(newest).isoformat()


def build_course(course_dir: Path, cfg: dict) -> tuple[dict, dict[str, str]]:
    """(entry for courses.json, {relative path: published html})."""
    slug = course_dir.name
    meta = json.loads((course_dir / "course.json").read_text(encoding="utf-8"))
    tags = meta.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    sources = {}
    for d in PUBLISHED_DIRS:
        for f in sorted((course_dir / d).glob("*.html")):
            sources[f"{d}/{f.name}"] = f.read_text(encoding="utf-8")
    published = set(sources)

    files, lessons, reference, problems = {}, [], [], []
    for rel, text in sources.items():
        here = rel.split("/")[0]
        text = redact(text, cfg["redact"])
        text = rewrite_links(text, slug, here, published)
        text = site_bar(text, slug, meta.get("title", slug))
        problems += [f"{slug}/{rel}: {h}" for h in deny_hits(text, cfg["deny"])]
        files[rel] = text
        entry = {"href": f"/courses/{slug}/{rel}", "title": page_title(text, here == "lessons")}
        (lessons if here == "lessons" else reference).append(entry)

    resources = []
    res_file = course_dir / "RESOURCES.md"
    if res_file.exists():
        res_text = redact(res_file.read_text(encoding="utf-8"), cfg["redact"])
        problems += [f"{slug}/RESOURCES.md: {h}" for h in deny_hits(res_text, cfg["deny"])]
        resources = parse_resources(res_text)

    entry = {
        "slug": slug,
        "title": meta.get("title", slug),
        "description": redact(meta.get("description", ""), cfg["redact"]),
        "category": category_key(meta.get("category", "Other")),
        "tags": tags,
        "updated": last_updated(course_dir),
        "lessons": lessons,
        "reference": reference,
        "resources": resources,
    }
    problems += [f"{slug}/course.json: {h}" for h in deny_hits(json.dumps(entry), cfg["deny"])]
    if problems:
        raise PrivacyError("\n".join(problems))
    return entry, files


def course_page(entry: dict) -> str:
    def q(s):
        return json.dumps(s, ensure_ascii=False)
    return (
        "+++\n"
        f"title = {q(entry['title'])}\n"
        f"description = {q(entry['description'])}\n"
        f"date = {entry['updated']}\n"
        f"slug = {q(entry['slug'])}\n"
        f"course = {q(entry['slug'])}\n"
        "# Written by tools/courses/sync_courses.py -- edit the course in the\n"
        "# learn project and re-run `make courses-sync`, not this file.\n"
        "generated = true\n"
        "+++\n"
    )


def collect(cfg: dict) -> tuple[list[dict], dict[str, dict[str, str]]]:
    src = Path(cfg["source"])
    if not src.is_dir():
        raise SystemExit(f"no courses at {src}")
    entries, files, problems = [], {}, []
    for course_dir in sorted(p for p in src.iterdir() if (p / "course.json").exists()):
        if course_dir.name in cfg.get("exclude", []):
            continue
        try:
            entry, pages = build_course(course_dir, cfg)
        except PrivacyError as err:
            problems.append(str(err))
            continue
        if not entry["lessons"]:
            continue
        entries.append(entry)
        files[entry["slug"]] = pages
    if problems:
        raise PrivacyError("\n".join(problems))
    # Most lessons first, then by title: the fuller courses lead.
    entries.sort(key=lambda e: (-len(e["lessons"]), e["title"].lower()))
    return entries, files


def write_if_changed(path: Path, text: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def write(entries: list[dict], files: dict[str, dict[str, str]]) -> list[str]:
    changed = []
    slugs = {e["slug"] for e in entries}
    for entry in entries:
        slug = entry["slug"]
        wanted = set(files[slug])
        for rel, text in files[slug].items():
            if write_if_changed(STATIC / slug / rel, text):
                changed.append(f"static/courses/{slug}/{rel}")
        for old in (STATIC / slug).rglob("*.html"):
            if old.relative_to(STATIC / slug).as_posix() not in wanted:
                old.unlink()
                changed.append(f"removed static/courses/{slug}/{old.relative_to(STATIC / slug)}")
        if write_if_changed(CONTENT / slug / "index.md", course_page(entry)):
            changed.append(f"content/courses/{slug}/index.md")
    # Anything this script published before for a course that is gone now.
    for d in list(STATIC.glob("*/")) if STATIC.exists() else []:
        if d.is_dir() and d.name not in slugs:
            shutil.rmtree(d)
            changed.append(f"removed static/courses/{d.name}")
    for d in list(CONTENT.glob("*/")) if CONTENT.exists() else []:
        page = d / "index.md"
        if d.is_dir() and d.name not in slugs and page.exists() and "generated = true" in page.read_text(encoding="utf-8"):
            shutil.rmtree(d)
            changed.append(f"removed content/courses/{d.name}")
    data = {
        "_comment": "Generated by tools/courses/sync_courses.py (make courses-sync). Don't edit by hand.",
        "total_lessons": sum(len(e["lessons"]) for e in entries),
        "courses": entries,
    }
    if write_if_changed(DATA, json.dumps(data, indent=1, ensure_ascii=False) + "\n"):
        changed.append("data/courses.json")
    return changed


def main(argv: list[str]) -> int:
    cfg = load_config()
    try:
        entries, files = collect(cfg)
    except PrivacyError as err:
        print("Not published -- personal details found after redaction:\n" + str(err), file=sys.stderr)
        print("Add a redact rule in tools/courses/config.json or fix the lesson in the learn project.", file=sys.stderr)
        return 1
    lessons = sum(len(e["lessons"]) for e in entries)
    if "--check" in argv:
        print(f"ok: {len(entries)} courses, {lessons} lessons, nothing personal found")
        return 0
    changed = write(entries, files)
    for c in changed:
        print(c)
    print(f"{len(entries)} courses, {lessons} lessons; {len(changed)} file(s) changed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
