#!/usr/bin/env python3
"""Check every link on /learn/ opens for a visitor who isn't signed in.

The page only lists what a stranger can actually open, so each url in
data/learn.json is fetched anonymously, following redirects. It also checks
the file's shape, the part that can break the page without any network:
unique keys, every item has either a url or a site `page`, and every key
has its i18n strings in English (tools/i18n-check covers the other eight).

    python3 tools/learn-links/check_learn_links.py            # report
    python3 tools/learn-links/check_learn_links.py --offline  # shape only

A redirect is reported but is not a failure; update the url when it lands
somewhere permanent. A site that refuses scripts (401/403/429 -- Cloudflare's
own Learning Center does) is listed as "blocked" and doesn't fail the check:
open it in a browser before listing it. A network error is retried once,
since a single timeout or reset is usually the network, not the site.
Exit status is 1 when anything is broken.
Standard library only.
"""

import http.cookiejar
import json
import sys
import tomllib
import urllib.error
import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data" / "learn.json"
EN = REPO / "i18n" / "en.toml"
GROUPS = {"neutral", "local", "made_here"}
BLOCKED = {401, 403, 429}  # bot walls and rate limits, not dead pages

# A browser's user agent: several course sites refuse the default urllib one.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def items(data: dict):
    for path in data["paths"]:
        for item in path["items"]:
            yield path, item


def check_shape(data: dict, strings: dict) -> list[str]:
    """Problems that would break or blank part of the page."""
    errors = []
    seen = set()
    for key in ("learn_path_%s", "learn_path_blurb_%s"):
        for path in data["paths"]:
            if key % path["key"] not in strings:
                errors.append(f"path {path['key']}: no i18n key {key % path['key']}")
    for path, item in items(data):
        key = item.get("key", "")
        if not key:
            errors.append(f"{path['key']}: item without a key")
            continue
        if key in seen:
            errors.append(f"{key}: duplicate key")
        seen.add(key)
        if bool(item.get("url")) == bool(item.get("page")):
            errors.append(f"{key}: needs exactly one of url or page")
        if item.get("url") and not item.get("name"):
            errors.append(f"{key}: a url item needs a name")
        if item.get("url") and f"learn_res_{key}" not in strings:
            errors.append(f"{key}: no i18n key learn_res_{key}")
        page = REPO / "content" / item.get("page", "").strip("/")
        if item.get("page") and not (page.is_dir() or page.with_suffix(".md").is_file()):
            errors.append(f"{key}: no page at content{item['page']}")
        group = item.get("group")
        if group and (group not in GROUPS or f"learn_group_{group}" not in strings):
            errors.append(f"{key}: unknown group {group}")
    return errors


def fetch(url: str, tries: int = 2) -> tuple[int | str, str]:
    """(status, final url). A status that is not an int is a network error,
    which is retried (tries in all) before it is believed."""
    for attempt in range(tries):
        status, final = fetch_once(url)
        if isinstance(status, int):
            break
        if attempt + 1 < tries:
            time.sleep(3)
    return status, final


def classify(status: int | str) -> str:
    """"ok", "blocked" (refuses scripts, fine in a browser) or "broken"."""
    if status == 200:
        return "ok"
    return "blocked" if status in BLOCKED else "broken"


def fetch_once(url: str) -> tuple[int | str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    # A cookie jar per fetch, as a browser would keep: some sites (Google's
    # docs) set a cookie and redirect to the same url, a loop without one.
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    try:
        with opener.open(req, timeout=25) as resp:
            return resp.status, resp.geturl()
    except urllib.error.HTTPError as err:
        return err.code, url
    except Exception as err:  # DNS, TLS, timeout
        return type(err).__name__, url


def same(a: str, b: str) -> bool:
    return a.rstrip("/") == b.rstrip("/")


def main(argv: list[str]) -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    with EN.open("rb") as fh:
        strings = tomllib.load(fh)
    errors = check_shape(data, strings)
    for e in errors:
        print(f"SHAPE  {e}")
    if "--offline" in argv:
        return 1 if errors else 0

    links = [(i["key"], i["url"]) for _, i in items(data) if i.get("url")]
    with ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(lambda l: fetch(l[1]), links))
    broken = blocked = 0
    for (key, url), (status, final) in zip(links, results):
        kind = classify(status)
        if kind == "ok":
            if not same(final, url):
                print(f"MOVED  {key}: {url} -> {final}")
        elif kind == "blocked":
            blocked += 1
            print(f"blocked {key}: {status} {url}")
        else:
            broken += 1
            print(f"BROKEN {key}: {status} {url}")
    print(f"{len(links)} links, {broken} broken, {blocked} blocked to scripts, "
          f"{len(errors)} shape problems")
    return 1 if broken or errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
