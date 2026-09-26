#!/usr/bin/env python3
"""Open every "Where to go next" link on the course pages as a visitor would.

The resources come from each course's RESOURCES.md in the learn project and
land in data/courses.json via `make courses-sync`. Links rot; this lists
the ones that no longer open, reusing the /learn/ checker's fetch (browser
user agent, cookies kept, redirects followed).

    python3 tools/courses/check_course_links.py

Sites that refuse scripts (401/403/429 -- Stack Overflow, Medium, npm) are
listed as "blocked" and don't count: they open fine in a browser. Only
pages that are gone (404/410, DNS failure, 5xx) fail the check.

Exit status 1 when anything is broken. Standard library only.
"""

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "learn-links"))
from check_learn_links import fetch  # noqa: E402

BLOCKED = {401, 403, 429}  # bot walls and rate limits, not dead pages


def links(data: dict) -> list[tuple[str, str]]:
    """(course slug, url) for every resource link, de-duplicated."""
    seen, out = set(), []
    for course in data["courses"]:
        for section in course["resources"]:
            for item in section["items"]:
                for link in item["links"]:
                    if link["url"] not in seen:
                        seen.add(link["url"])
                        out.append((course["slug"], link["url"]))
    return out


def main() -> int:
    data = json.loads((REPO / "data" / "courses.json").read_text(encoding="utf-8"))
    todo = links(data)
    with ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(lambda l: fetch(l[1]), todo))
    broken, blocked = [], []
    for (slug, url), (status, _) in zip(todo, results):
        if status == 200:
            continue
        (blocked if status in BLOCKED else broken).append((slug, url, status))
    for slug, url, status in blocked:
        print(f"blocked {slug}: {status} {url}")
    for slug, url, status in broken:
        print(f"BROKEN  {slug}: {status} {url}")
    print(f"{len(todo)} links, {len(broken)} broken, {len(blocked)} blocked to scripts")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
