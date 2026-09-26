"""Unit tests for tools/github-repos/refresh.py. No network: the GitHub
responses are built by hand in the shape the GraphQL query returns."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refresh  # noqa: E402

CFG = json.loads(refresh.CONFIG.read_text())


def raw(name, **kw):
    r = {
        "name": name, "description": None, "homepageUrl": None, "isFork": False, "isArchived": False,
        "stargazerCount": 0, "forkCount": 0, "createdAt": "2019-03-01T00:00:00Z",
        "pushedAt": "2020-01-02T00:00:00Z", "diskUsage": 100, "licenseInfo": None, "parent": None,
        "primaryLanguage": None, "languages": {"totalSize": 0, "edges": []},
        "repositoryTopics": {"nodes": []},
    }
    r.update(kw)
    return r


class ReadmeText(unittest.TestCase):
    def test_strips_markdown_noise(self):
        md = (
            "# Title\n\n[![Build](https://x/badge.svg)](https://x)\n\n"
            "Learn **AWS Lambda** with [SAM](https://aws.amazon.com/sam).\n\n"
            "```sh\nnpm install\n```\n\n| a | b |\n|---|---|\n\n    indented code\n\n"
            "<img src=x> tags: [\"aws\", \"lambda\"]\n"
        )
        self.assertEqual(refresh.readme_text(md), ["Learn AWS Lambda with SAM."])

    def test_summary_takes_first_sentence(self):
        paras = ["Short.", "A tool to sync things between two places. Then more text."]
        self.assertEqual(refresh.summary_from(paras), "A tool to sync things between two places.")

    def test_clip_cuts_on_a_word(self):
        self.assertEqual(refresh.clip("alpha beta gamma", 12), "alpha beta…")
        self.assertEqual(refresh.clip("short", 12), "short")


class Classification(unittest.TestCase):
    def test_name_tokens_include_runs(self):
        toks = refresh.name_tokens("aws-step-functions-playground")
        self.assertIn("step-functions", toks)
        self.assertIn("aws", toks)

    def test_first_matching_area_is_primary(self):
        # Mirrors topic-id.html: aws + lambda reads as serverless, not cloud.
        areas = refresh.classify({"aws", "lambda"}, CFG["areas"])
        self.assertEqual(areas[0], "serverless")
        self.assertIn("cloud", areas)

    def test_unmatched_is_other(self):
        self.assertEqual(refresh.classify({"zzz"}, CFG["areas"]), ["other"])

    def test_exclude_keeps_a_repo_out_of_a_track(self):
        rule = {"match": ["serverless"], "exclude": ["opensearch"]}
        self.assertTrue(refresh.matches({"serverless"}, rule))
        self.assertFalse(refresh.matches({"serverless", "opensearch"}, rule))

    def test_display_tags_drop_parts_of_compounds(self):
        tags = refresh.display_tags({"step", "functions", "step-functions", "my"}, {"step", "functions", "step-functions"}, "")
        self.assertEqual(tags, ["step-functions"])


class Build(unittest.TestCase):
    def test_build_shapes_repos_and_tracks(self):
        repos = [
            raw("aws-lambda-playground", description="aws-lambda-playground",
                primaryLanguage={"name": "JavaScript", "color": "#f1e05a"},
                r0={"text": "Learn AWS Lambda basics.\n"}),
            raw("aws-lambda-advanced-combo-thing-playground", diskUsage=90000),
            raw("someone-elses", isFork=True, parent={"nameWithOwner": "x/someone-elses"}),
        ]
        posts = {"aws-lambda-playground": {"lambda", "serverless"}}
        doc = refresh.build(repos, posts, CFG, "2026-09-26")
        by = {r["name"]: r for r in doc["repos"]}

        first = by["aws-lambda-playground"]
        # A description that only repeats the name falls back to the README.
        self.assertEqual(first["desc"], "Learn AWS Lambda basics.")
        self.assertEqual(first["kind"], "playground")
        self.assertTrue(first["post"])
        self.assertEqual(first["areas"][0], "serverless")
        self.assertEqual(doc["colors"]["JavaScript"], "#f1e05a")
        # Ranking-only fields never reach the page.
        self.assertFalse([k for k in first if k.startswith("_")])
        for gone in ("desc_src", "forks", "size", "tracks"):
            self.assertNotIn(gone, first)

        self.assertEqual(by["someone-elses"]["kind"], "fork")
        self.assertEqual(by["someone-elses"]["parent"], "x/someone-elses")

        track = {t["key"]: t["repos"] for t in doc["tracks"]}["serverless"]
        # The one with an article and a README comes before the big combo repo;
        # forks never appear in a learning path.
        self.assertEqual(track[0], "aws-lambda-playground")
        self.assertNotIn("someone-elses", track)
        self.assertEqual(doc["count"], 3)

    def test_post_tags_reads_front_matter(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "a.md").write_text('+++\ntitle = "x"\ntags = ["Lambda", "aws"]\n'
                                       'categories = ["JavaScript", "playground"]\n'
                                       'repoFullName = "pfeilbr/Aws-Thing"\n+++\nbody\n')
            Path(d, "b.md").write_text('+++\ntitle = "y"\nrepoFullName = "someone/else"\n+++\n')
            tags = refresh.post_tags(Path(d))
        self.assertEqual(tags, {"aws-thing": {"lambda", "aws", "javascript"}})


class Safety(unittest.TestCase):
    def test_safe_url_only_lets_http_through(self):
        self.assertEqual(refresh.safe_url("https://x.dev/a"), "https://x.dev/a")
        self.assertEqual(refresh.safe_url(" example.com "), "https://example.com")
        self.assertEqual(refresh.safe_url("javascript:alert(1)"), "")
        self.assertEqual(refresh.safe_url("ftp://x"), "")
        self.assertEqual(refresh.safe_url("a b"), "")
        self.assertEqual(refresh.safe_url(None), "")

    def test_decide_skips_date_only_changes(self):
        old = {"updated": "2026-01-01", "count": 10, "repos": [1]}
        self.assertEqual(refresh.decide(dict(old, updated="2026-02-01"), old), "same")
        self.assertEqual(refresh.decide(dict(old, repos=[2]), old), "write")
        self.assertEqual(refresh.decide(old, None), "write")

    def test_decide_refuses_a_big_drop_unless_forced(self):
        old = {"updated": "d", "count": 400, "repos": []}
        new = {"updated": "d", "count": 100, "repos": [1]}
        self.assertEqual(refresh.decide(new, old), "shrunk")
        self.assertEqual(refresh.decide(new, old, force=True), "write")
        self.assertEqual(refresh.decide(dict(new, count=390), old), "write")

    def test_graphql_retries_then_succeeds(self):
        calls = []

        class R:
            def __init__(self, code, out="", err=""):
                self.returncode, self.stdout, self.stderr = code, out, err

        def run(args, **kw):
            calls.append(args)
            return R(1, err="HTTP 502") if len(calls) < 3 else R(0, out='{"ok": 1}')

        self.assertEqual(refresh.gh_graphql("c1", run=run, sleep=lambda s: None), {"ok": 1})
        self.assertEqual(len(calls), 3)
        self.assertIn("cursor=c1", calls[0])

    def test_graphql_signed_out_fails_fast(self):
        class R:
            returncode, stdout, stderr = 4, "", "To get started with GitHub CLI, please run:  gh auth login"
        with self.assertRaises(SystemExit) as cm:
            refresh.gh_graphql(None, run=lambda a, **k: R(), sleep=lambda s: None)
        self.assertIn("gh auth login", str(cm.exception))


class Output(unittest.TestCase):
    def test_committed_file_is_public_only_and_well_formed(self):
        doc = json.loads(refresh.OUT.read_text())
        keys = {a["key"] for a in doc["areas"]}
        for r in doc["repos"]:
            self.assertTrue(set(r["areas"]) <= keys, r["name"])
            self.assertNotIn("private", r)
            if "homepage" in r:
                self.assertRegex(r["homepage"], r"^https?://")
        self.assertEqual(doc["count"], len(doc["repos"]))
        names = {r["name"] for r in doc["repos"]}
        for t in doc["tracks"]:
            self.assertTrue(set(t["repos"]) <= names, t["key"])


if __name__ == "__main__":
    unittest.main()
