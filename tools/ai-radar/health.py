#!/usr/bin/env python3
"""Which /ai/ sources keep failing, as the body of a GitHub issue.

Prints nothing when every source is healthy; otherwise a Markdown list of
the sources that have failed STREAK or more runs in a row (fail_streak in
data/ai.json) with their last error. The daily Action opens or updates one
issue with this text, and closes it once the list is empty.

  python3 tools/ai-radar/health.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STREAK = 3
TITLE = "AI radar: sources failing"


def report(doc, streak=STREAK):
    bad = [s for s in doc.get("sources", []) if s.get("fail_streak", 0) >= streak]
    if not bad:
        return ""
    lines = ["These `/ai/` sources have failed %d or more runs in a row. Their items stay on the page "
             "until they age out; fix the feed URL in `tools/ai-radar/config.json` or remove the source." % streak, ""]
    for s in sorted(bad, key=lambda s: -s["fail_streak"]):
        lines.append("- **%s** (`%s`, %d runs): %s" % (s["name"], s["id"], s["fail_streak"], s.get("error", "unknown error")))
    lines += ["", "_Updated automatically by `.github/workflows/ai-radar.yml`; it closes itself when every source recovers._"]
    return "\n".join(lines)


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "ai.json"
    sys.stdout.write(report(json.loads(path.read_text())))
