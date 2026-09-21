#!/usr/bin/env python3
"""Fail if a Makefile target is undocumented.

The README once documented 5 of 21 targets without anyone noticing. Every
target must carry a `## description` (which `make help` prints) and be named
in README.md, so adding a target without documenting it fails CI.

    python3 tools/docs-check/check_docs.py

Standard library only.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TARGET = re.compile(r"^([a-z0-9][a-z0-9-]*):(?!=)(.*)$", re.MULTILINE)


def targets(makefile: str) -> dict[str, str]:
    """name -> the rest of the line (dependencies and any ## description)."""
    return {m.group(1): m.group(2) for m in TARGET.finditer(makefile)}


def problems(makefile: str, readme: str) -> list[str]:
    found = []
    for name, rest in sorted(targets(makefile).items()):
        if "## " not in rest:
            found.append(f"{name}: no '## description' for make help")
        if not re.search(rf"(?<![a-z0-9-]){re.escape(name)}(?![a-z0-9-])", readme):
            found.append(f"{name}: not mentioned in README.md")
    return found


def main() -> int:
    makefile = (REPO / "Makefile").read_text(encoding="utf-8")
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    found = problems(makefile, readme)
    if found:
        print(f"FAIL: {len(found)} undocumented target(s)")
        for p in found:
            print(f"  {p}")
        return 1
    print(f"ok: all {len(targets(makefile))} Makefile targets documented")
    return 0


if __name__ == "__main__":
    sys.exit(main())
