#!/usr/bin/env python3
"""Refresh every page whose content comes from somewhere else, in one run.

Each step is one of the site's own refreshers (the `make *-refresh` / `*-sync`
targets); this script only runs them in turn, keeps going when one fails, and
prints what changed. Updates to sourced content go through these scripts, not
hand edits, so a refresh is always repeatable.

  python3 tools/refresh/refresh_all.py                  # every step, no commit
  python3 tools/refresh/refresh_all.py music movies     # just those steps
  python3 tools/refresh/refresh_all.py --list           # the steps and what they write
  python3 tools/refresh/refresh_all.py --commit         # + make verify, commit, push

Every run (but --list) first pulls main, since the daily Actions commit to the
same files. --commit stages only the files the successful steps own, runs
`make verify`, then commits and pushes. Unrelated work in progress is left
alone. A missing tool (go, hugo) skips its step and says so.

Not here, on purpose:
  /ai/          ai-radar.yml commits data/ai.json twice a day; local copies
                must never be committed.
  /media/       `make media-sync` uploads to S3 and commits on its own; it runs
                here only when the Instagram archive and an AWS session exist.
  /learn/, /apps/  hand-curated; their link checks are reports, not updates.

Standard library only.
"""
import argparse
import datetime
import os
import pathlib
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]


def aws_signed_in():
    return shutil.which("aws") and subprocess.run(
        ["aws", "sts", "get-caller-identity"], capture_output=True).returncode == 0


def instagram_archive():
    cfg = (ROOT / "tools/instagram-media/config.yaml").read_text()
    line = next((l for l in cfg.splitlines() if l.startswith("archive_dir:")), "")
    path = line.partition(":")[2].strip().strip('"\'')
    return path and pathlib.Path(path).expanduser().is_dir()


def gh_token():
    r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


# name, command, files it owns, why it might be skipped (None = always runs)
STEPS = [
    ("music", ["python3", "tools/music/refresh.py"],
     ["data/music.yaml"], None),
    ("twitch", ["python3", "tools/subscriptions/twitch.py"],
     ["data/twitch.yaml"], None),
    ("youtube", ["python3", "tools/subscriptions/youtube.py"],
     ["data/subscriptions.yaml", "static/subscriptions/avatars"], None),
    ("movies", ["python3", "-u", "tools/movies/refresh.py"],
     ["data/movies.json", "static/movies"], None),
    ("github", ["python3", "tools/github-repos/refresh.py"],
     ["data/github.json"], None),
    ("notes", ["go", "run", ".", "-user=pfeilbr", "-dest=../../content/post"],
     ["content/post"], None),
    ("repo-links", ["python3", "tools/link-check/check_repo_links.py", "--write"],
     ["data/repo_gone.json"], None),
    ("courses", ["python3", "tools/courses/sync_courses.py"],
     ["data/courses.json", "static/courses", "content/courses", "static/sitemap-courses.xml"],
     lambda: None if (pathlib.Path.home() / "projects/learn").is_dir()
     else "~/projects/learn is not on this machine"),
    ("media", ["make", "media-sync"], [],  # commits and pushes its own files
     lambda: None if instagram_archive() and aws_signed_in()
     else "needs the Instagram archive and `aws sso login`"),
]
CWD = {"notes": ROOT / "tools/generate-posts"}


def run_step(name, cmd):
    env = dict(os.environ)
    if name == "notes" and not env.get("GITHUB_TOKEN"):
        env["GITHUB_TOKEN"] = gh_token()
    start = time.monotonic()
    code = subprocess.run(cmd, cwd=CWD.get(name, ROOT), env=env).returncode
    return code, time.monotonic() - start


def changed(paths):
    if not paths:
        return []
    out = subprocess.run(["git", "status", "--porcelain", "--", *paths],
                         cwd=ROOT, capture_output=True, text=True).stdout
    return [l[3:] for l in out.splitlines()]


def git(*args):
    subprocess.run(["git", *args], cwd=ROOT, check=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("steps", nargs="*", help="run only these steps")
    ap.add_argument("--list", action="store_true", help="list the steps and exit")
    ap.add_argument("--commit", action="store_true", help="verify, commit and push what changed")
    args = ap.parse_args(argv)

    names = [s[0] for s in STEPS]
    if args.list:
        for name, cmd, owns, _ in STEPS:
            print(f"{name:<11} {' '.join(cmd):<60} {', '.join(owns) or '(commits itself)'}")
        return 0
    unknown = set(args.steps) - set(names)
    if unknown:
        raise SystemExit(f"unknown step(s): {', '.join(sorted(unknown))}; choose from {', '.join(names)}")

    # The daily Actions commit to these same files, so start from the latest
    # main or the push ends in conflicts over week-old data.
    if subprocess.run(["git", "pull", "--rebase", "--autostash", "-q"], cwd=ROOT).returncode != 0:
        raise SystemExit("git pull failed; resolve it, then re-run")

    results = []
    for name, cmd, owns, skip in STEPS:
        if args.steps and name not in args.steps:
            continue
        why = skip() if skip else None
        if not why and not shutil.which(cmd[0]):
            why = f"`{cmd[0]}` is not installed"
        if why:
            results.append((name, "skipped", why, []))
            continue
        before = set(changed(owns))
        print(f"\n=== {name}: {' '.join(cmd)}", flush=True)
        code, secs = run_step(name, cmd)
        files = [f for f in changed(owns) if f not in before]
        status = "ok" if code == 0 else f"exit {code}"
        results.append((name, status, f"{secs:.0f}s, {len(files)} file(s) changed", files))

    print("\n=== summary")
    for name, status, note, _ in results:
        print(f"{name:<11} {status:<8} {note}")
    # A step that failed partway may still have written good data (movies keeps
    # each film's old data on failure, for one); commit only clean runs.
    to_commit = sorted({f for _, status, _, files in results if status == "ok" for f in files})
    failed = [n for n, status, *_ in results if status not in ("ok", "skipped")]

    if args.commit and to_commit:
        print("\n=== make verify", flush=True)
        if subprocess.run(["make", "verify"], cwd=ROOT).returncode != 0:
            print("verify failed; nothing committed", file=sys.stderr)
            return 1
        git("add", "--", *to_commit)
        done = [n for n, status, _, files in results if status == "ok" and files]
        git("commit", "-m", f"Refresh: {datetime.date.today()} ({', '.join(done)})\n\n"
            "Ran tools/refresh/refresh_all.py.")
        git("push")
    elif args.commit:
        print("nothing changed; nothing to commit")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
