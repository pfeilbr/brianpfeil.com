#!/usr/bin/env python3
"""Send the newsletter issues in tools/newsletter/issues/ through Buttondown.

    python3 tools/newsletter/send.py            # list issues not sent yet
    python3 tools/newsletter/send.py --send     # send them (needs BUTTONDOWN_API_KEY)
    python3 tools/newsletter/send.py --send --only 006-foo

Each issue is a Markdown file with a small front matter block:

    ---
    subject: "The subject line"
    url: https://brianpfeil.com/<the page it points at>/
    ---
    Body in Markdown (Buttondown renders it).

tools/newsletter/sent.json is the ledger: one entry per issue that has gone
out, keyed by file stem, with the Buttondown email id and archive URL. An
issue in the ledger is never sent again, so re-running is safe. Issues sent
by hand in the Buttondown editor are recorded there too.

Standard library only.
"""

import argparse
import datetime
import json
import os
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ISSUES = HERE / "issues"
LEDGER = HERE / "sent.json"
API = "https://api.buttondown.com/v1/emails"
ARCHIVE = "https://buttondown.com/pfeilbr/archive/"


def parse_issue(text):
    """Split an issue file into (front matter dict, body)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError("issue must start with a --- front matter block")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise ValueError("front matter block is not closed") from None
    meta = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1]
        meta[key.strip()] = value
    if not meta.get("subject"):
        raise ValueError("front matter needs a subject")
    body = "\n".join(lines[end + 1:]).strip() + "\n"
    return meta, body


def load_ledger(path=LEDGER):
    return json.loads(path.read_text()) if path.exists() else {}


def pending(issue_dir=ISSUES, ledger=None):
    """Issue files (sorted by name) that are not in the ledger."""
    ledger = load_ledger() if ledger is None else ledger
    return [p for p in sorted(issue_dir.glob("*.md")) if p.stem not in ledger]


def send(meta, body, key):
    req = urllib.request.Request(
        API,
        data=json.dumps({"subject": meta["subject"], "body": body,
                         "status": "about_to_send"}).encode(),
        headers={"Authorization": f"Token {key}",
                 "Content-Type": "application/json",
                 "X-Buttondown-Live-Dangerously": "true"},
        method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--send", action="store_true", help="send pending issues")
    ap.add_argument("--only", help="send just this issue (file stem)")
    args = ap.parse_args(argv)

    ledger = load_ledger()
    todo = [p for p in pending(ledger=ledger) if not args.only or p.stem == args.only]
    if not todo:
        print("Nothing to send: every issue is in sent.json.")
        return 0
    for p in todo:
        meta, _ = parse_issue(p.read_text())
        print(f"pending  {p.stem}  {meta['subject']}")
    if not args.send:
        return 0

    key = os.environ.get("BUTTONDOWN_API_KEY")
    if not key:
        print("BUTTONDOWN_API_KEY is not set (Buttondown → Settings → API).", file=sys.stderr)
        return 1
    for p in todo:
        meta, body = parse_issue(p.read_text())
        email = send(meta, body, key)
        # Record each send the moment it succeeds, so a failure later in the
        # loop can never cause a repeat.
        ledger[p.stem] = {
            "subject": meta["subject"],
            "id": email.get("id"),
            "archive": ARCHIVE + email.get("slug", "") + "/" if email.get("slug") else None,
            "sent": datetime.date.today().isoformat(),
        }
        LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")
        print(f"sent     {p.stem}  {email.get('id')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
