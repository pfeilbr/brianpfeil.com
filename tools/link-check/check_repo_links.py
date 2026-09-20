#!/usr/bin/env python3
"""Find posts whose "code for article" link a stranger can't open.

Generated posts link to the GitHub repo they were built from. When a repo
goes private or is deleted, the post stays up and the link quietly 404s for
everyone but the owner. This checks every such link anonymously — as a
visitor would — and lists the ones that are broken.

    python3 tools/link-check/check_repo_links.py          # report
    python3 tools/link-check/check_repo_links.py --json   # machine-readable

Exit status is 1 when anything is broken, so it can gate a workflow.
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


def main() -> int:
    as_json = "--json" in sys.argv[1:]
    results = check(repo_links(POSTS))
    bad = broken(results)

    if as_json:
        print(json.dumps({"checked": len(results), "broken": bad}, indent=2))
    else:
        print(f"checked {len(results)} repo links, {len(bad)} broken")
        for r in bad:
            reason = "no response" if r["status"] == 0 else f"HTTP {r['status']}"
            print(f"  {reason:<12} {r['file']}\n               {r['url']}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
