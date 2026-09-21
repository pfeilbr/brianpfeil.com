#!/usr/bin/env python3
"""Check the nine i18n files agree, and that no page falls back to English.

Hugo falls back to English silently, and an empty value counts as missing —
that is how /ja/ once shipped an English author line. Matching key counts
prove nothing, so this checks what actually matters:

1. every English key exists in every language, and no language has keys
   English doesn't (usually a rename that left a stale copy behind)
2. no value is empty
3. every placeholder in the English string survives translation — a
   translation that drops {{ .count }} renders without the number
4. with --public DIR: no translated page contains the English text of a
   string whose translation differs, which is what a fallback looks like

    python3 tools/i18n-check/check_i18n.py
    python3 tools/i18n-check/check_i18n.py --public public

Standard library only (tomllib, Python >= 3.11).
"""

import html
import re
import sys
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
I18N = REPO / "i18n"
BASE = "en"
LANGS = ["zh", "es", "pt", "fr", "de", "it", "ja", "ko"]

PLACEHOLDER = re.compile(r"\{\{-?\s*([^}]*?)\s*-?\}\}")

# A fallback is only detectable when the English text is distinctive enough
# not to appear on the page for some other reason.
MIN_LEAK_LENGTH = 20


def load(lang: str, directory: Path = I18N) -> dict[str, str]:
    """Flatten one language to key -> text (the `other` form)."""
    with (directory / f"{lang}.toml").open("rb") as fh:
        raw = tomllib.load(fh)
    flat = {}
    for key, value in raw.items():
        if isinstance(value, dict):
            flat[key] = value.get("other", "")
        else:
            flat[key] = value
    return flat


def placeholders(text: str) -> set[str]:
    return {m.group(1) for m in PLACEHOLDER.finditer(text)}


def check_files(directory: Path = I18N) -> list[str]:
    errors = []
    base = load(BASE, directory)

    for key, text in sorted(base.items()):
        if not str(text).strip():
            errors.append(f"{BASE}: [{key}] is empty")

    for lang in LANGS:
        try:
            other = load(lang, directory)
        except FileNotFoundError:
            errors.append(f"{lang}: i18n/{lang}.toml is missing")
            continue

        for key in sorted(set(base) - set(other)):
            errors.append(f"{lang}: [{key}] missing (would render in English)")
        for key in sorted(set(other) - set(base)):
            errors.append(f"{lang}: [{key}] is not in {BASE}.toml (stale?)")

        for key in sorted(set(base) & set(other)):
            text = str(other[key])
            if not text.strip():
                errors.append(f"{lang}: [{key}] is empty (Hugo falls back to English)")
                continue
            missing = placeholders(str(base[key])) - placeholders(text)
            if missing:
                errors.append(f"{lang}: [{key}] drops {', '.join(sorted(missing))}")
    return errors


def pages_for(public: Path, lang: str) -> list[Path]:
    root = public / lang
    return sorted(root.rglob("index.html")) if root.is_dir() else []


def check_rendered(public: Path, directory: Path = I18N) -> list[str]:
    """Look for English text on translated pages where a translation exists."""
    base = load(BASE, directory)
    errors = []
    for lang in LANGS:
        other = load(lang, directory)
        # Only strings that are actually translated can leak: a brand name
        # that is the same in every language is supposed to appear.
        suspects = {
            key: str(base[key]) for key in base
            if key in other and str(other[key]) != str(base[key])
            and not placeholders(str(base[key]))  # rendered form differs
            and len(str(base[key])) >= MIN_LEAK_LENGTH
        }
        for page in pages_for(public, lang):
            body = html.unescape(page.read_text(encoding="utf-8"))
            for key, english in suspects.items():
                if english in body:
                    rel = page.relative_to(public).as_posix()
                    errors.append(f"{lang}: /{rel} shows English [{key}]: {english[:60]!r}")
    return errors


def main() -> int:
    args = sys.argv[1:]
    errors = check_files()
    if "--public" in args:
        public = Path(args[args.index("--public") + 1])
        errors += check_rendered(public)

    if errors:
        print(f"FAIL: {len(errors)} i18n problem(s)")
        for e in errors:
            print(f"  {e}")
        return 1
    base = load(BASE)
    scope = " and rendered pages" if "--public" in args else ""
    print(f"ok: {len(base)} keys consistent across {len(LANGS) + 1} languages{scope}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
