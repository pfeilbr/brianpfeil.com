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


if __name__ == "__main__":
    unittest.main()
