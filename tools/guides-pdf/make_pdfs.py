#!/usr/bin/env python3
"""Print every architecture guide to a PDF, for sharing and printing.

A checklist is most useful on paper or as a LinkedIn document post. This
builds the site into a temporary directory, serves it on localhost, and has
headless Chrome print each guide (the site's print styles drop the nav,
footer and sign-up boxes) to static/architecture/<slug>.pdf. The guide page
links its PDF when the file exists.

A PDF is only regenerated when its guide's Markdown changed (hashes in
static/architecture/pdf-sources.json), so re-running is a no-op otherwise;
--force rebuilds them all -- e.g. after a print-style change.

    python3 tools/guides-pdf/make_pdfs.py
    python3 tools/guides-pdf/make_pdfs.py --force

Needs hugo and Google Chrome.
"""

import argparse
import functools
import hashlib
import http.server
import json
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GUIDES = REPO / "content" / "architecture"
OUT = REPO / "static" / "architecture"
SOURCES = OUT / "pdf-sources.json"
CHROME = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
]


def chrome() -> str:
    for c in CHROME:
        if Path(c).exists() or shutil.which(c):
            return c
    raise SystemExit("Google Chrome not found")


def guides() -> dict[str, Path]:
    return {p.stem: p for p in sorted(GUIDES.glob("*.md")) if not p.name.startswith("_")}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def stale(force: bool) -> list[str]:
    seen = json.loads(SOURCES.read_text()) if SOURCES.exists() else {}
    return [slug for slug, md in guides().items()
            if force or seen.get(slug) != digest(md) or not (OUT / f"{slug}.pdf").exists()]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(root: Path) -> tuple[http.server.ThreadingHTTPServer, int]:
    handler = functools.partial(QuietHandler, directory=str(root))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    todo = stale(args.force)
    if not todo:
        print("all guide PDFs are current")
        return 0
    browser = chrome()
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["hugo", "--minify", "--quiet", "-d", tmp], cwd=REPO, check=True)
        httpd, port = serve(Path(tmp))
        try:
            OUT.mkdir(parents=True, exist_ok=True)
            for slug in todo:
                pdf = OUT / f"{slug}.pdf"
                subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                                "--virtual-time-budget=4000", f"--print-to-pdf={pdf}",
                                f"http://127.0.0.1:{port}/architecture/{slug}/"],
                               check=True, capture_output=True, timeout=120)
                print(f"{pdf.relative_to(REPO)}  {pdf.stat().st_size // 1024} KB")
        finally:
            httpd.shutdown()
    seen = json.loads(SOURCES.read_text()) if SOURCES.exists() else {}
    seen.update({slug: digest(guides()[slug]) for slug in todo})
    SOURCES.write_text(json.dumps(dict(sorted(seen.items())), indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
