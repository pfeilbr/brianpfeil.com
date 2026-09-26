#!/usr/bin/env python3
"""Check a built site (public/) for problems that break things for visitors.

    python3 tools/site-check/check_site.py --public public

1. Every same-site link and asset (href/src starting with "/") resolves to a
   file in the build -- a page's index.html, or the file itself. Links to
   pages that exist only on the live host (none today) can be listed in
   ALLOW.
2. No two taxonomy terms differ only by case. With disablePathToLower on,
   "HTML" and "html" fight over one URL and the build picks a winner at
   random, so the same source produces different sites.

Exit status 1 on any problem. Standard library only.
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[2]
ATTR = re.compile(r"""\b(?:href|src)=(?:"([^"]*)"|'([^']*)'|([^\s>"']+))""")
SCRIPT = re.compile(r"<script\b.*?</script>", re.S | re.I)
ALLOW: set[str] = set()


def targets(path: str) -> list[str]:
    """Files that would satisfy a request for `path` on a static host."""
    if re.search(r"\.[A-Za-z0-9]+$", path):
        return [path]
    base = path.rstrip("/")
    return [base + "/index.html", base + ".html"] if base else ["/index.html"]


def case_insensitive(public: Path) -> bool:
    """True on a case-insensitive disk (macOS default). There a directory
    left from an earlier build decides the on-disk casing of pages written
    into it, so only compare case-insensitively; CI (Linux) stays strict."""
    probe = next((p for p in public.iterdir() if p.name != p.name.swapcase()), None)
    return bool(probe) and (public / probe.name.swapcase()).exists()


def broken_links(public: Path) -> dict[str, set[str]]:
    files = {"/" + p.relative_to(public).as_posix() for p in public.rglob("*") if p.is_file()}
    fold = case_insensitive(public)
    if fold:
        files = {f.lower() for f in files}
    broken: dict[str, set[str]] = defaultdict(set)
    for page in public.rglob("*.html"):
        text = SCRIPT.sub("", page.read_text(encoding="utf-8", errors="replace"))
        here = "/" + page.relative_to(public).as_posix()
        for m in ATTR.finditer(text):
            url = next(g for g in m.groups() if g is not None)
            if not url.startswith("/") or url.startswith("//"):
                continue
            path = unquote(url.split("#", 1)[0].split("?", 1)[0])
            if not path or path in ALLOW:
                continue
            if not any((t.lower() if fold else t) in files for t in targets(path)):
                broken[path].add(here)
    return broken


def term_case_clashes(content: Path) -> dict[str, set[str]]:
    """Taxonomy values (tags, categories) used with more than one casing."""
    seen: dict[str, set[str]] = defaultdict(set)
    line = re.compile(r'^(tags|categories)\s*=\s*\[(.*?)\]', re.M)
    for md in content.rglob("*.md"):
        head = md.read_text(encoding="utf-8", errors="replace")[:4000]
        for kind, values in line.findall(head):
            for v in re.findall(r'"([^"]+)"', values):
                seen[f"{kind}:{v.lower()}"].add(v)
    return {k: v for k, v in seen.items() if len(v) > 1}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Check a built site for broken links.")
    ap.add_argument("--public", type=Path, default=REPO / "public")
    ap.add_argument("--content", type=Path, default=REPO / "content")
    args = ap.parse_args(argv)
    problems = 0
    for path, pages in sorted(broken_links(args.public).items()):
        problems += 1
        print(f"broken link {path}  (on {len(pages)} page(s), e.g. {sorted(pages)[0]})")
    for key, forms in sorted(term_case_clashes(args.content).items()):
        problems += 1
        print(f"{key.split(':')[0]} used with different casing: {sorted(forms)}")
    if problems:
        print(f"FAIL: {problems} problem(s)")
        return 1
    print("ok: every same-site link resolves; no taxonomy casing clashes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
