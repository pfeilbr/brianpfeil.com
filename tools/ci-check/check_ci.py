#!/usr/bin/env python3
"""Checks of the CI setup itself, so it can't drift apart unnoticed.

- Every workflow that installs Hugo pins the same version. The pin lives in
  five workflows (deploy, Tests and three refreshes); a bump that missed one
  would build the checked page with a different Hugo than the deployed one.
- Every tool with tests (tools/<name>/ holding test_*.py, *_test.go or
  *.test.mjs) is run both by `make verify` and by the Tests workflow. Four
  suites once ran in only one of them, or in neither.

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


SKIP_DIRS = {".venv", "node_modules", "build", "__pycache__"}
TEST_FILE = re.compile(r"^(test_.*\.py|.*_test\.go|.*\.test\.mjs)$")
TARGET = re.compile(r"^([a-z0-9][a-z0-9-]*):(?!=)([^\n#]*)", re.MULTILINE)


def tools_with_tests(tools: Path) -> list[str]:
    """tools/<name> for every tool directory that holds a test file."""
    found = []
    for tool in sorted(p for p in tools.iterdir() if p.is_dir()):
        for path in tool.rglob("*"):
            if any(part in SKIP_DIRS for part in path.relative_to(tool).parts):
                continue
            if path.is_file() and TEST_FILE.match(path.name):
                found.append(f"tools/{tool.name}")
                break
    return found


def verify_recipes(makefile: str) -> str:
    """The recipe text of every target `verify` depends on, plus its own."""
    recipes, current = {}, None
    for line in makefile.splitlines():
        m = TARGET.match(line)
        if m:
            current = m.group(1)
            recipes[current] = [m.group(2)]
        elif current and line.startswith("\t"):
            recipes[current].append(line)
        elif not line.strip():
            current = None
    deps = recipes.get("verify", [""])[0].split("##")[0].split()
    return "\n".join(line for name in ["verify", *deps] for line in recipes.get(name, [])[1:])


def suite_problems(suites: list[str], makefile: str, tests_workflow: str) -> list[str]:
    verify = verify_recipes(makefile)
    found = []
    for suite in suites:
        if not re.search(rf"{re.escape(suite)}(?![a-z0-9-])", verify):
            found.append(f"{suite}: has tests but `make verify` never runs them")
        if not re.search(rf"{re.escape(suite)}(?![a-z0-9-])", tests_workflow):
            found.append(f"{suite}: has tests but the Tests workflow never runs them")
    return found


def load_workflows() -> dict[str, str]:
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(WORKFLOWS.glob("*.y*ml"))}


def main() -> int:
    workflows = load_workflows()
    suites = tools_with_tests(REPO / "tools")
    found = hugo_problems(workflows) + suite_problems(
        suites, (REPO / "Makefile").read_text(encoding="utf-8"), workflows.get("tests.yml", "")
    )
    for problem in found:
        print(f"error: {problem}", file=sys.stderr)
    if found:
        return 1
    version = next(iter({v for vs in hugo_pins(workflows).values() for v in vs}))
    print(f"ok: Hugo {version} pinned in {len(hugo_pins(workflows))} workflows; "
          f"all {len(suites)} tool test suites run in make verify and CI")
    return 0


if __name__ == "__main__":
    sys.exit(main())
