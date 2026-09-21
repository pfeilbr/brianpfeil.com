"""Tests for check_docs.py."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_docs as c  # noqa: E402

MAKE = """\
dev: ## Dev server
build: ## Build
verify: test-a test-b ## Everything
FOO := bar
test-a: ## A
"""
README = "make dev, make build, make verify and make test-a"


class DocsTest(unittest.TestCase):
    def test_documented_targets_pass(self):
        self.assertEqual(c.problems(MAKE, README), [])

    def test_variable_assignments_are_not_targets(self):
        self.assertNotIn("FOO", c.targets(MAKE))
        self.assertNotIn("foo", c.targets("foo := 1\n"))

    def test_missing_help_text(self):
        self.assertIn("lint: no '## description' for make help",
                      c.problems(MAKE + "lint:\n", README + " lint"))

    def test_missing_from_readme(self):
        self.assertIn("deploy: not mentioned in README.md",
                      c.problems(MAKE + "deploy: ## Ship it\n", README))

    def test_a_prefix_match_does_not_count(self):
        """'test' must not be satisfied by 'test-a' appearing in the README."""
        self.assertIn("test: not mentioned in README.md",
                      c.problems(MAKE + "test: ## All\n", README))


if __name__ == "__main__":
    unittest.main()
