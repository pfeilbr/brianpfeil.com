#!/usr/bin/env python3
"""Fetch the AWS Terraform provider over a slow link, then init, validate, plan.

`terraform init` cannot resume a partial download. On a ~50 KB/s link the AWS
provider (174 MB) takes about an hour, so any interruption throws the whole
thing away. This resumes with curl, checks the published SHA256, installs into
a local filesystem mirror and then runs Terraform against that mirror.

Re-runnable and idempotent: a complete download is verified and skipped, an
installed provider is left alone. Safe to run again after an interruption.

    python3 infra/scripts/fetch_provider.py [--detach]

--detach puts it in its own session so it outlives the shell that started it;
progress goes to infra/.provider-cache/fetch.log.
"""

import hashlib
import os
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

# Pinned deliberately: the checksum below belongs to this exact build. Bump
# both together, from https://releases.hashicorp.com/terraform-provider-aws/.
VERSION = "6.65.0"
PLATFORM = "darwin_arm64"
SHA256 = "9ddfdefef226c8ff3c8de03d8df23ab3199fed9f0684618a62489e0e90a21cab"
SIZE = 173742642

BASE = f"https://releases.hashicorp.com/terraform-provider-aws/{VERSION}"
ZIP_NAME = f"terraform-provider-aws_{VERSION}_{PLATFORM}.zip"

INFRA = Path(__file__).resolve().parents[1]
CACHE = INFRA / ".provider-cache"
ZIP_PATH = CACHE / ZIP_NAME
LOG = CACHE / "fetch.log"
MIRROR = Path.home() / ".terraform.d" / "plugin-mirror"
INSTALL_DIR = MIRROR / "registry.terraform.io" / "hashicorp" / "aws" / VERSION / PLATFORM

MAX_ATTEMPTS = 60


def log(message: str) -> None:
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    CACHE.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line, flush=True)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download() -> bool:
    CACHE.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        have = ZIP_PATH.stat().st_size if ZIP_PATH.exists() else 0
        if have >= SIZE:
            break
        log(f"attempt {attempt}: {have:,}/{SIZE:,} bytes ({have * 100 // SIZE}%)")
        proc = subprocess.run(
            ["curl", "-sS", "-L", "-C", "-", "--retry", "3", "--retry-delay", "5",
             "--max-time", "1800", "--speed-limit", "1024", "--speed-time", "120",
             "-o", str(ZIP_PATH), f"{BASE}/{ZIP_NAME}"],
            capture_output=True, text=True,
        )
        gained = (ZIP_PATH.stat().st_size if ZIP_PATH.exists() else 0) - have
        # Log why, not just that: an earlier run sat at 209 KB for six hours
        # because curl's exit code and stderr were being discarded.
        if proc.returncode != 0 or gained <= 0:
            log(f"  curl exit {proc.returncode}, gained {gained:,} bytes"
                f"{': ' + proc.stderr.strip()[:200] if proc.stderr.strip() else ''}")
        if gained <= 0:
            time.sleep(10)  # no progress at all; back off
    else:
        log("gave up: too many attempts without finishing")
        return False

    digest = sha256_of(ZIP_PATH)
    if digest != SHA256:
        # A corrupt resume poisons every later attempt, so drop it.
        log(f"CHECKSUM MISMATCH: got {digest}, expected {SHA256} — discarding")
        ZIP_PATH.unlink(missing_ok=True)
        return False
    log("checksum matches the published SHA256SUMS")
    return True


def install() -> bool:
    if any(INSTALL_DIR.glob("terraform-provider-aws*")):
        log(f"already installed at {INSTALL_DIR}")
        return True
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH) as zf:
        for member in zf.namelist():
            if member.startswith("terraform-provider-aws"):
                zf.extract(member, INSTALL_DIR)
                (INSTALL_DIR / member).chmod(0o755)
                log(f"installed {member}")
    return any(INSTALL_DIR.glob("terraform-provider-aws*"))


def terraform(*args: str) -> tuple[int, str]:
    proc = subprocess.run(["terraform", *args], cwd=INFRA, capture_output=True, text=True)
    return proc.returncode, (proc.stdout + proc.stderr)


def run() -> int:
    log(f"=== {ZIP_NAME} ({SIZE:,} bytes) ===")
    if not shutil.which("curl") or not shutil.which("terraform"):
        log("FAILED: curl or terraform not on PATH")
        return 1
    if not download() or not install():
        log("FAILED: provider unavailable")
        return 1

    for step in (["init", "-input=false", "-no-color", f"-plugin-dir={MIRROR}"],
                 ["validate", "-no-color"],
                 ["plan", "-input=false", "-no-color", "-lock=false"]):
        log(f"terraform {step[0]}")
        code, out = terraform(*step)
        if step[0] == "plan":
            (CACHE / "plan.txt").write_text(out, encoding="utf-8")
        log(out.strip()[-3000:])
        if code != 0:
            log(f"FAILED: {step[0]}")
            return 1

    log("DONE — review the plan: expect 6 to import, 0 to add/change/destroy")
    return 0


def main() -> int:
    if "--detach" in sys.argv:
        if os.fork() != 0:
            print(f"detached; progress in {LOG}")
            return 0
        os.setsid()
        with open(CACHE / "runner.out", "w") as out:
            os.dup2(out.fileno(), 1)
            os.dup2(out.fileno(), 2)
    return run()


if __name__ == "__main__":
    CACHE.mkdir(parents=True, exist_ok=True)
    sys.exit(main())
