#!/usr/bin/env python3
"""Checks of the CI setup itself, so it can't drift apart unnoticed.

- Every workflow that installs Hugo pins the same version. The pin lives in
  five workflows (deploy, Tests and three refreshes); a bump that missed one
  would build the checked page with a different Hugo than the deployed one.

    python3 tools/ci-check/check_ci.py

Standard library only.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WORKFLOWS = REPO / ".github" / "workflows"
HUGO_PIN = re.compile(r"""^\s*hugo-version:\s*["']?([^"'\s#]+)""", re.MULTILINE)


def hugo_pins(workflows: dict[str, str]) -> dict[str, list[str]]:
    """workflow name -> every hugo-version it sets."""
    return {name: HUGO_PIN.findall(text) for name, text in workflows.items() if HUGO_PIN.search(text)}


def hugo_problems(workflows: dict[str, str]) -> list[str]:
    pins = hugo_pins(workflows)
    if not pins:
        return ["no workflow pins hugo-version"]
    versions = {v for vs in pins.values() for v in vs}
    if len(versions) == 1:
        return []
    return [
        "hugo-version differs between workflows: "
        + ", ".join(f"{name} {'/'.join(vs)}" for name, vs in sorted(pins.items()))
    ]


def load_workflows() -> dict[str, str]:
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(WORKFLOWS.glob("*.y*ml"))}


def main() -> int:
    workflows = load_workflows()
    found = hugo_problems(workflows)
    for problem in found:
        print(f"error: {problem}", file=sys.stderr)
    if found:
        return 1
    version = next(iter({v for vs in hugo_pins(workflows).values() for v in vs}))
    print(f"ok: Hugo {version} pinned in {len(hugo_pins(workflows))} workflows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
