#!/usr/bin/env python3
"""Pull the drafts matching some keywords out of a Drafts backup.

A full Drafts backup (Settings > Backups, a .draftsExport JSON array) is
too big for the Google Drive connector's 10 MB download limit. This writes
only the matching drafts, oldest first, as one Markdown file that is:

    python3 tools/drafts-extract/extract.py ~/Downloads/DraftsBackup-*.draftsExport \
        -o ~/Desktop/bipolar-drafts.md

Keywords are case-insensitive substrings; pass -k to replace the defaults.
Trashed drafts are skipped. Nothing is written into this repo.
"""
import argparse
import json
import sys

DEFAULT_KEYWORDS = [
    "bipolar", "manic", "mania", "hypomani", "depress", "psychiatr", "therap",
    "medication", "vraylar", "prozac", "fluoxetine", "citalopram", "lithium",
    "lamictal", "lamotrigine", "seroquel", "ketamine", "tms", "leave of absence",
    "disability", "brain fog", "mood",
]


def matches(draft, keywords):
    text = (draft.get("content") or "").lower()
    tags = " ".join(draft.get("tags") or []).lower()
    return any(k in text or k in tags for k in keywords)


def extract(drafts, keywords):
    keep = [d for d in drafts if not d.get("is_trashed") and matches(d, keywords)]
    keep.sort(key=lambda d: d.get("created_at") or "")
    out = []
    for d in keep:
        head = (d.get("created_at") or "undated")[:10]
        tags = ", ".join(d.get("tags") or [])
        out.append(f"## {head}" + (f"  ({tags})" if tags else ""))
        out.append("")
        out.append((d.get("content") or "").strip())
        out.append("")
        out.append("---")
        out.append("")
    return len(keep), "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("backup", help="a .draftsExport file")
    ap.add_argument("-o", "--out", required=True, help="Markdown file to write")
    ap.add_argument("-k", "--keyword", action="append", help="keyword (repeatable)")
    args = ap.parse_args(argv)
    with open(args.backup, encoding="utf-8") as f:
        drafts = json.load(f)
    keywords = [k.lower() for k in (args.keyword or DEFAULT_KEYWORDS)]
    n, md = extract(drafts, keywords)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"{n} of {len(drafts)} drafts -> {args.out} ({len(md.encode()) / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
