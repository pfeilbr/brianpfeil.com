#!/usr/bin/env python3
"""Check /apps/ and its short links in a built site.

data/apps.json lists the apps; the build turns it into /data/apps.json (the
page draws from it), /apps/ in nine languages, a home card, and a redirect
at /apps/<key>/ for every app. This checks, against a built site:

  - data/apps.json is well formed: unique lowercase keys (they are URLs),
    https urls, an icon file that exists, a blurb in every i18n file;
  - /data/apps.json was published with every app;
  - /apps/<key>/index.html redirects to that app (refresh, script and
    canonical all agree) and is noindex;
  - /apps/ exists in every language, loads apps.json and carries that
    language's blurbs, and the home page links to it.

    python3 tools/apps/check_page.py --public public

Exit status 1 on any problem. Standard library only.
"""

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LANGS = ("en", "zh", "es", "pt", "fr", "de", "it", "ja", "ko")
KEY = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def prefix(lang: str) -> str:
    return "" if lang == "en" else f"{lang}/"


def check_data(data: dict, i18n: dict[str, dict], static: Path) -> list[str]:
    errors = []
    apps = data.get("apps") or []
    if not apps:
        return ["data/apps.json: no apps"]
    seen = set()
    for a in apps:
        key = a.get("key", "")
        if not KEY.match(key):
            errors.append(f"{key!r}: key must be lowercase letters, digits and dashes")
        if key in seen:
            errors.append(f"{key}: duplicate key")
        seen.add(key)
        if not a.get("name"):
            errors.append(f"{key}: no name")
        if not str(a.get("url", "")).startswith("https://"):
            errors.append(f"{key}: url must be https")
        icon = a.get("icon", "")
        if not icon.startswith("/") or not (static / icon.lstrip("/")).is_file():
            errors.append(f"{key}: icon {icon!r} is not a file under static/")
        for lang in LANGS:
            if not i18n.get(lang, {}).get(f"apps_blurb_{key}", {}).get("other"):
                errors.append(f"{key}: no apps_blurb_{key} in i18n/{lang}.toml")
    return errors


def check_redirect(html: str, url: str) -> list[str]:
    errors = []
    if f'content="0; url={url}"' not in html:
        errors.append("no meta refresh to the app")
    if f'<link rel="canonical" href="{url}">' not in html:
        errors.append("canonical is not the app")
    if f"location.replace({json.dumps(url)}" not in html:
        errors.append("script does not go to the app")
    if '<meta name="robots" content="noindex">' not in html:
        errors.append("not noindex")
    return errors


def check_build(public: Path, data: dict, i18n: dict[str, dict]) -> list[str]:
    errors = []
    published = public / "data" / "apps.json"
    if not published.is_file():
        return ["/data/apps.json was not published"]
    keys = [a["key"] for a in data["apps"]]
    if [a.get("key") for a in json.loads(published.read_text(encoding="utf-8")).get("apps", [])] != keys:
        errors.append("/data/apps.json does not list the same apps as data/apps.json")
    for a in data["apps"]:
        page = public / "apps" / a["key"] / "index.html"
        if not page.is_file():
            errors.append(f"/apps/{a['key']}/ was not published")
            continue
        errors += [f"/apps/{a['key']}/: {e}" for e in check_redirect(page.read_text(encoding="utf-8"), a["url"])]
    for lang in LANGS:
        page = public / prefix(lang) / "apps" / "index.html"
        if not page.is_file():
            errors.append(f"/{prefix(lang)}apps/ missing")
            continue
        html = page.read_text(encoding="utf-8")
        if not re.search(r'load\("apps"\)', html):
            errors.append(f"/{prefix(lang)}apps/: does not load apps.json")
        for key in keys:
            blurb = i18n[lang][f"apps_blurb_{key}"]["other"]
            if json.dumps(blurb, ensure_ascii=False)[1:-1] not in html:
                errors.append(f"/{prefix(lang)}apps/: {lang} blurb for {key} missing")
        home = (public / prefix(lang) / "index.html").read_text(encoding="utf-8")
        if not re.search(rf'href="?/{prefix(lang)}apps/"?[\s>]', home):
            errors.append(f"/{prefix(lang)}: no home card linking to /{prefix(lang)}apps/")
    return errors


def load_i18n() -> dict[str, dict]:
    return {lang: tomllib.loads((REPO / "i18n" / f"{lang}.toml").read_text(encoding="utf-8")) for lang in LANGS}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", help="a built site; without it only data/apps.json is checked")
    args = ap.parse_args(argv)
    data = json.loads((REPO / "data" / "apps.json").read_text(encoding="utf-8"))
    i18n = load_i18n()
    errors = check_data(data, i18n, REPO / "static")
    if args.public and not errors:
        errors += check_build(Path(args.public), data, i18n)
    for e in errors:
        print(f"apps: {e}", file=sys.stderr)
    if errors:
        return 1
    print(f"ok: {len(data['apps'])} apps" + (", page and short links built" if args.public else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
