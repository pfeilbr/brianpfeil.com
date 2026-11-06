import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import check_ci  # noqa: E402


class HugoPinTest(unittest.TestCase):
    def test_one_version_everywhere_passes(self):
        wf = {"a.yml": '  hugo-version: "0.166.0"\n', "b.yml": "      hugo-version: 0.166.0\n", "c.yml": "on: push\n"}
        self.assertEqual(check_ci.hugo_problems(wf), [])
        self.assertEqual(set(check_ci.hugo_pins(wf)), {"a.yml", "b.yml"})

    def test_a_missed_bump_is_reported(self):
        wf = {"deploy.yml": 'hugo-version: "0.167.0"\n', "tests.yml": 'hugo-version: "0.166.0"\n'}
        [problem] = check_ci.hugo_problems(wf)
        self.assertIn("deploy.yml 0.167.0", problem)
        self.assertIn("tests.yml 0.166.0", problem)

    def test_no_pin_at_all_is_reported(self):
        self.assertEqual(check_ci.hugo_problems({"x.yml": "on: push\n"}), ["no workflow pins hugo-version"])

    def test_the_repo_passes(self):
        self.assertEqual(check_ci.hugo_problems(check_ci.load_workflows()), [])


MAKEFILE = """verify: test-a test-b ## Every test suite
\thugo --minify

test-a: ## a
\tpython3 -m unittest discover -s tools/a -p 'test_*.py'

test-b: ## b
\tcd tools/b && go test ./...

test-c: ## c, not in verify
\tpython3 -m unittest discover -s tools/c -p 'test_*.py'
"""


class SuiteWiringTest(unittest.TestCase):
    def test_suites_in_both_pass(self):
        ci = "run: python -m unittest discover -s tools/a\nworking-directory: tools/b\n"
        self.assertEqual(check_ci.suite_problems(["tools/a", "tools/b"], MAKEFILE, ci), [])

    def test_a_suite_missing_from_verify_or_ci_is_named(self):
        ci = "run: python -m unittest discover -s tools/a\n"
        problems = check_ci.suite_problems(["tools/a", "tools/b", "tools/c"], MAKEFILE, ci)
        self.assertEqual(problems, [
            "tools/b: has tests but the Tests workflow never runs them",
            "tools/c: has tests but `make verify` never runs them",
            "tools/c: has tests but the Tests workflow never runs them",
        ])

    def test_a_name_that_prefixes_another_is_not_a_match(self):
        ci = "tools/ab\n"
        self.assertIn("tools/a: has tests but the Tests workflow never runs them",
                      check_ci.suite_problems(["tools/a"], MAKEFILE, ci))

    def test_finds_python_go_and_node_suites_and_skips_venvs(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for f in ["py/test_x.py", "go/x_test.go", "js/x.test.mjs", "none/x.py", "venv/.venv/lib/test_y.py"]:
                (root / f).parent.mkdir(parents=True, exist_ok=True)
                (root / f).write_text("")
            self.assertEqual(check_ci.tools_with_tests(root), ["tools/go", "tools/js", "tools/py"])

    def test_the_repo_passes(self):
        from pathlib import Path
        repo = Path(check_ci.REPO)
        problems = check_ci.suite_problems(
            check_ci.tools_with_tests(repo / "tools"),
            (repo / "Makefile").read_text(encoding="utf-8"),
            check_ci.load_workflows()["tests.yml"],
        )
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
