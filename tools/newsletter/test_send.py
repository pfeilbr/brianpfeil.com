import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import send  # noqa: E402


class ParseIssue(unittest.TestCase):
    def test_front_matter_and_body(self):
        meta, body = send.parse_issue('---\nsubject: "Hi: there"\nurl: https://x/\n---\n\nBody **text**\n')
        self.assertEqual(meta, {"subject": "Hi: there", "url": "https://x/"})
        self.assertEqual(body, "Body **text**\n")

    def test_needs_subject(self):
        with self.assertRaises(ValueError):
            send.parse_issue("---\nurl: x\n---\nbody\n")

    def test_needs_front_matter(self):
        with self.assertRaises(ValueError):
            send.parse_issue("just a body\n")


class Pending(unittest.TestCase):
    def test_skips_issues_in_the_ledger(self):
        with tempfile.TemporaryDirectory() as d:
            for name in ("002-b", "001-a", "003-c"):
                Path(d, name + ".md").write_text('---\nsubject: "s"\n---\nb\n')
            got = [p.stem for p in send.pending(Path(d), {"002-b": {}})]
            self.assertEqual(got, ["001-a", "003-c"])


class RealIssues(unittest.TestCase):
    """Every committed issue parses and links only to this site over https."""

    def test_issues(self):
        ledger = send.load_ledger()
        issues = sorted(send.ISSUES.glob("*.md"))
        self.assertTrue(issues)
        for p in issues:
            meta, body = send.parse_issue(p.read_text())
            self.assertTrue(meta["url"].startswith("https://brianpfeil.com/"), p.name)
            for url in re.findall(r"\]\((\S+?)\)", body):
                self.assertTrue(url.startswith("https://brianpfeil.com/"), f"{p.name}: {url}")
        for stem in ledger:
            self.assertTrue((send.ISSUES / f"{stem}.md").exists(), f"ledger entry {stem} has no issue file")

    def test_ledger_is_valid_json(self):
        json.loads(send.LEDGER.read_text())


if __name__ == "__main__":
    unittest.main()
