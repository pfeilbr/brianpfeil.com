#!/usr/bin/env python3
"""Tell search engines which pages changed, via IndexNow.

IndexNow (Bing, Yandex, Seznam, Naver and others share one endpoint) lets a
site announce new and changed URLs instead of waiting to be recrawled. The
deploy workflow runs this in two steps:

    # build job, after `hugo --minify`, before the artifact is uploaded:
    python3 tools/indexnow/indexnow.py plan public --out changed.txt

        Hashes every page in public/, writes that as
        public/indexnow-manifest.json (so it ships with the site), fetches the
        manifest the live site is serving right now, and writes the URLs whose
        hash is new or different to changed.txt.

    # after the deploy job succeeds:
    python3 tools/indexnow/indexnow.py submit changed.txt

A page's hash covers its <title>, meta description and <main> -- not the
nav, footer or fingerprinted asset links, which change on every page whenever
the CSS does and would otherwise make every deploy look like a full rewrite.
Pages with no <main> (the course lessons) are hashed whole. Redirect stubs,
the 404 page and the IndexNow key file are skipped.

    python3 tools/indexnow/indexnow.py plan public --previous none   # first run: everything
    python3 tools/indexnow/indexnow.py submit changed.txt --dry-run

Standard library only.
"""

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

CONFIG = json.loads(Path(__file__).with_name("config.json").read_text(encoding="utf-8"))
BATCH = 10_000  # IndexNow's per-request limit

TITLE = re.compile(r"<title[^>]*>.*?</title>", re.S | re.I)
DESCRIPTION = re.compile(r"<meta\s+name=[\"']?description[\"']?\s+content=(\"[^\"]*\"|'[^']*'|[^\s>]+)", re.I)
MAIN = re.compile(r"<main\b.*?</main>", re.S | re.I)
REFRESH = re.compile(r"http-equiv=[\"']?refresh", re.I)
UA = "brianpfeil.com-indexnow/1.0"


def page_hash(text: str) -> str:
    """Hash of what a reader (and a search engine) cares about on the page."""
    main = MAIN.search(text)
    parts = [m.group(0) for m in (TITLE.search(text), DESCRIPTION.search(text)) if m]
    parts.append(main.group(0) if main else text)
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]


def url_for(public: Path, path: Path, site: str) -> str | None:
    rel = path.relative_to(public).as_posix()
    if rel == "404.html" or not rel.endswith(".html"):
        return None
    if rel == "index.html":
        return site + "/"
    if rel.endswith("/index.html"):
        return f"{site}/{rel[: -len('index.html')]}"
    return f"{site}/{rel}"


def manifest(public: Path, site: str) -> dict[str, str]:
    out = {}
    for path in sorted(public.rglob("*.html")):
        url = url_for(public, path, site)
        if not url:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if REFRESH.search(text[:2000]):  # Hugo alias redirect stubs
            continue
        out[url] = page_hash(text)
    return out


def changed(new: dict[str, str], old: dict[str, str]) -> list[str]:
    return sorted(u for u, h in new.items() if old.get(u) != h)


def fetch_previous(url: str) -> dict[str, str]:
    """The manifest the live site serves; empty if there isn't one yet."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("pages", {}) if isinstance(data, dict) else {}
    except (urllib.error.URLError, ValueError, TimeoutError) as err:
        print(f"no previous manifest ({err}); treating every page as new", file=sys.stderr)
        return {}


def payloads(urls: list[str], cfg: dict) -> list[dict]:
    host = cfg["site"].split("://", 1)[1].rstrip("/")
    return [{
        "host": host,
        "key": cfg["key"],
        "keyLocation": f"{cfg['site'].rstrip('/')}/{cfg['key']}.txt",
        "urlList": urls[i:i + BATCH],
    } for i in range(0, len(urls), BATCH)]


def submit(urls: list[str], cfg: dict, dry_run: bool = False) -> int:
    if not urls:
        print("nothing changed; nothing to submit")
        return 0
    for body in payloads(urls, cfg):
        if dry_run:
            print(f"dry run: would submit {len(body['urlList'])} URL(s) to {cfg['endpoint']}")
            continue
        req = urllib.request.Request(
            cfg["endpoint"], data=json.dumps(body).encode("utf-8"), method="POST",
            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"submitted {len(body['urlList'])} URL(s): HTTP {resp.status}")
        except urllib.error.HTTPError as err:
            # 200/202 are success. 403 = key not verified yet, 422 = URLs not
            # on this host, 429 = too many requests. None should fail a deploy.
            print(f"IndexNow answered HTTP {err.code}: {err.read()[:200]!r}", file=sys.stderr)
            return 0 if err.code in (403, 429) else 1
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan", help="write the manifest into PUBLIC and list changed URLs")
    p.add_argument("public", type=Path)
    p.add_argument("--out", type=Path, default=Path("changed.txt"))
    p.add_argument("--previous", help="manifest URL, or 'none' (default: the live one)")
    s = sub.add_parser("submit", help="send the URLs in FILE to IndexNow")
    s.add_argument("file", type=Path)
    s.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    site = CONFIG["site"].rstrip("/")
    if args.cmd == "plan":
        new = manifest(args.public, site)
        (args.public / CONFIG["manifest"]).write_text(
            json.dumps({"pages": new}, separators=(",", ":"), sort_keys=True), encoding="utf-8")
        prev_url = args.previous or f"{site}/{CONFIG['manifest']}"
        old = {} if prev_url == "none" else fetch_previous(prev_url)
        urls = changed(new, old)
        args.out.write_text("".join(u + "\n" for u in urls), encoding="utf-8")
        print(f"{len(new)} pages, {len(urls)} new or changed -> {args.out}")
        return 0
    urls = [u.strip() for u in args.file.read_text(encoding="utf-8").splitlines() if u.strip()]
    return submit(urls, CONFIG, args.dry_run)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
