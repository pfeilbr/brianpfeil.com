#!/usr/bin/env python3
"""Open every outbound link in posts, projects and guides, as a visitor would.

The repo links, /learn/ and the course resources each have a checker; the
~1,800 links written into the articles themselves had none. This reads them
from a built site (the article body only, code blocks skipped, since a URL
in a code sample isn't a link) and fetches each with the /learn/ checker's
fetch: browser user agent, cookies kept, redirects followed, a network
error retried once.

    hugo -d /tmp/site && python3 tools/link-check/check_post_links.py --public /tmp/site
    ... --json out.json    # every result, machine-readable

Sites that refuse scripts (401/403/429) are "blocked" and don't count; they
usually open in a browser. "gone" is 404/410 or a host that can't be
reached at all (twice running); "error" is anything else (5xx, timeouts).
Dev-server and placeholder addresses (localhost, http://MY-SITE/) are skipped.
Exit status 1 when anything is gone. Standard library only.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "learn-links"))
from check_learn_links import BLOCKED, fetch  # noqa: E402

SECTIONS = ("post", "projects", "architecture")
BODY = re.compile(r'<div class="?prose"?>(.*?)</article>', re.S)
CODE = re.compile(r"<pre\b.*?</pre>|<code\b.*?</code>", re.S | re.I)
HREF = re.compile(r"""href=(?:"(https?://[^"]+)"|'(https?://[^']+)'|(https?://[^\s>"']+))""")
GONE = {404, 410}
DNS = {"URLError", "gaierror"}  # urllib wraps a failed lookup in URLError
# Dev-server addresses in setup instructions (http://localhost:3000) are
# autolinked by Markdown but were never links anyone could follow; nor are
# placeholders with no dot in the host (http://WP-VIP-SITE/wp-admin).
LOCAL = re.compile(r"^https?://(?:localhost|127\.|0\.0\.0\.0|10\.|192\.168\.|\[::1\]|[^/.:]+(?::\d+)?(?:/|$))", re.I)


def links(public: Path) -> dict[str, list[str]]:
    """{url: [page, ...]} for every external link in an article body."""
    found: dict[str, set[str]] = defaultdict(set)
    for page in public.glob("*/*/index.html"):
        rel = page.parent.relative_to(public).as_posix()
        if rel.split("/")[0] not in SECTIONS:
            continue
        m = BODY.search(page.read_text(encoding="utf-8", errors="replace"))
        if not m:
            continue
        for h in HREF.finditer(CODE.sub("", m.group(1))):
            url = next(g for g in h.groups() if g).replace("&amp;", "&")
            if LOCAL.match(url):
                continue
            found[url].add("/" + rel + "/")
    return {u: sorted(p) for u, p in sorted(found.items())}


def classify(status) -> str:
    if status == 200:
        return "ok"
    if status in BLOCKED:
        return "blocked"
    if status in GONE or status in DNS:
        return "gone"
    return "error"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", default="public")
    ap.add_argument("--json", help="write every result here")
    args = ap.parse_args(argv)
    found = links(Path(args.public))
    urls = list(found)
    with ThreadPoolExecutor(max_workers=16) as pool:
        statuses = list(pool.map(lambda u: fetch(u)[0], urls))
    results = [{"url": u, "status": s, "kind": classify(s), "pages": found[u]}
               for u, s in zip(urls, statuses)]
    counts = defaultdict(int)
    for r in results:
        counts[r["kind"]] += 1
        if r["kind"] in ("gone", "error"):
            print(f"{r['kind'].upper():5} {r['status']} {r['url']}  ({r['pages'][0]})")
    print(f"{len(results)} links: " + ", ".join(f"{counts[k]} {k}" for k in ("ok", "blocked", "error", "gone")))
    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    return 1 if counts["gone"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
