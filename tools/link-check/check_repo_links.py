#!/usr/bin/env python3
"""Find posts whose "code for article" link a stranger can't open.

Generated posts link to the GitHub repo they were built from. When a repo
goes private or is deleted, the post stays up and the link quietly 404s for
everyone but the owner. This checks every such link anonymously — as a
visitor would — and lists the ones that are broken.

    python3 tools/link-check/check_repo_links.py          # report
    python3 tools/link-check/check_repo_links.py --json   # machine-readable
    python3 tools/link-check/check_repo_links.py --write  # record them

Posts whose repo is gone keep their text but lose the link: every repo in
data/repo_gone.json is rendered without one (layouts/_default/single.html).
--write records today's broken set there. Exit status is 1 only when a repo
is broken and not yet recorded, so a newly private repo still gates a
workflow, and one that comes back is reported so it can be dropped.
Standard library only.
"""

import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POSTS = REPO / "content" / "post"
GONE = REPO / "data" / "repo_gone.json"

URL_LINE = re.compile(r'^repoHTMLURL\s*=\s*"([^"]+)"', re.MULTILINE)
TITLE_LINE = re.compile(r'^title\s*=\s*"((?:[^"\\]|\\.)*)"', re.MULTILINE)


def repo_links(posts_dir: Path) -> list[dict]:
    """Every generated post that names a repo, sorted by file name."""
    links = []
    for path in sorted(posts_dir.glob("generated-*.md")):
        text = path.read_text(encoding="utf-8")
        url = URL_LINE.search(text)
        if not url:
            continue
        title = TITLE_LINE.search(text)
        links.append({
            "file": path.name,
            "title": title.group(1) if title else path.stem,
            "url": url.group(1),
        })
    return links


def status_of(url: str, timeout: float = 15.0) -> int:
    """HTTP status an anonymous visitor gets. 0 means no answer at all."""
    request = urllib.request.Request(
        url, method="HEAD",
        # No cookies, no token: exactly what a stranger's browser sends.
        headers={"User-Agent": "brianpfeil.com-link-check"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0


def check(links: list[dict], fetch=status_of, workers: int = 16) -> list[dict]:
    """Annotate each link with its status; order is preserved."""
    with ThreadPoolExecutor(max_workers=workers) as pool:
        statuses = list(pool.map(lambda link: fetch(link["url"]), links))
    return [{**link, "status": status} for link, status in zip(links, statuses)]


def broken(results: list[dict]) -> list[dict]:
    """GitHub answers 404 for private and deleted repos alike."""
    return [r for r in results if r["status"] != 200]


def full_name(url: str) -> str:
    """"https://github.com/pfeilbr/x" -> "pfeilbr/x"."""
    return url.rstrip("/").split("github.com/", 1)[-1]


def recorded(path: Path = GONE) -> set[str]:
    """Repos already known to be gone (rendered without a link)."""
    if not path.exists():
        return set()
    return set(json.loads(path.read_text(encoding="utf-8")).get("repos", []))


def write_gone(bad: list[dict], path: Path = GONE) -> None:
    """Record the broken set; sorted so a re-run with no change is a no-op."""
    data = {"repos": sorted({full_name(r["url"]) for r in bad})}
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def unrecorded(bad: list[dict], known: set[str]) -> list[dict]:
    return [r for r in bad if full_name(r["url"]) not in known]


def main() -> int:
    args = sys.argv[1:]
    results = check(repo_links(POSTS))
    bad = broken(results)
    if "--write" in args:
        write_gone(bad)
    known = recorded()
    new = unrecorded(bad, known)
    back = sorted(known - {full_name(r["url"]) for r in bad})

    if "--json" in args:
        print(json.dumps({"checked": len(results), "broken": bad,
                          "unrecorded": new, "back": back}, indent=2))
    else:
        print(f"checked {len(results)} repo links, {len(bad)} broken, "
              f"{len(new)} not yet in data/repo_gone.json")
        for r in bad:
            reason = "no response" if r["status"] == 0 else f"HTTP {r['status']}"
            flag = "" if r in new else "  (recorded: shown without a link)"
            print(f"  {reason:<12} {r['file']}{flag}\n               {r['url']}")
        for name in back:
            print(f"  public again: {name} (re-run with --write to restore its link)")
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main())
