"""Decide what the picker may suggest, from what Apple Vision saw.

`vision/screen.swift` (compiled to build/bin/vision-screen) reports faces,
bodies, readable text, an aesthetics score and scene labels for an image.
This module turns that into a verdict — and it is the whole privacy policy
for Google Photos content, so it lives in Python where it is tested:

- **Only B.** A "me" candidate (Google matched B's face) must show exactly
  one person, and a visible face — without one there is no telling it is B
  and not one of his sons in the same helmet. A "scene" candidate (found by
  the activity alone) must show nobody: those are POV clips and landscapes.
  People are counted four ways — faces, whole bodies, upper bodies, and
  person segmentation, which separates people even behind goggles and a
  balaclava — and the highest count wins. Anything Google itself matched to
  one of the people in `exclude_people` is blocked outright (see picker.py).
  People too small to recognise are ignored — a speck on a far ski slope is
  not a person anyone could identify.
- **Nothing private.** Readable text that looks like a number plate, house
  number, phone number, address, email, or a page of writing blocks the item
  outright; any other text (a logo, a trail sign) is a warning the picker
  shows. Vision's "utility" shots (receipts, screenshots, documents) are
  blocked.
- Videos are screened frame by frame; the worst frame decides.
"""

import json
import re
import subprocess
from pathlib import Path

# Fractions of the frame's area. A face at 0.0008 is about 3% of the width —
# roughly the smallest face a stranger could recognise. Bodies count from
# much smaller: three kids on bikes across a ski slope measured 0.002 in a
# 360p clip, and a figure that small is still someone B knows.
MIN_FACE_AREA = 0.0008
MIN_HUMAN_AREA = 0.001
MIN_PERSON_AREA = 0.001  # segmentation mask coverage

DIGITS = re.compile(r"\d{3,}")
PLATE = re.compile(r"\b[A-Z0-9]{2,4}[- ]?[A-Z0-9]{3,4}\b")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.\w+|www\.|https?://|\.com\b", re.I)
STREET = re.compile(r"\b(st|street|ave|avenue|rd|road|dr|drive|ln|lane|blvd|ct|court|way)\b\.?", re.I)
TOO_MUCH_TEXT = 40  # characters: past this it is a sign, a page or a screen

SUGGEST_MIN_SCORE = 0.0  # Vision aesthetics, -1..1


def faces(result: dict) -> int:
    return sum(1 for a in result.get("faceAreas") or [] if a >= MIN_FACE_AREA)


def people(result: dict) -> int:
    bodies = sum(1 for a in result.get("humanAreas") or [] if a >= MIN_HUMAN_AREA)
    upper = sum(1 for a in result.get("upperBodies") or [] if a >= MIN_HUMAN_AREA)
    persons = sum(1 for a in result.get("personAreas") or [] if a >= MIN_PERSON_AREA)
    return max(faces(result), bodies, upper, persons)


def text_problem(strings: list[str]) -> str | None:
    """Why this text is private, or None if it is merely text."""
    joined = " ".join(s.strip() for s in strings if s.strip())
    if not joined:
        return None
    if DIGITS.search(joined):
        return "numbers (plate, address or phone?)"
    if EMAIL.search(joined):
        return "email or web address"
    if STREET.search(joined):
        return "street name"
    if len(joined) > TOO_MUCH_TEXT:
        return "a lot of text"
    if any(PLATE.fullmatch(s.strip()) and any(ch.isdigit() for ch in s) for s in strings):
        return "number plate"
    return None


def verdict(frames: list[dict], tier: str, excluded: bool = False) -> dict:
    """Combine one or more Vision results into what the picker shows.

    Returns {status: ok|warn|blocked, reasons: [...], people, text, score}.
    """
    reasons, warnings = [], []
    if excluded:
        reasons.append("Google recognised someone else in it")
    ok_frames = [f for f in frames if f.get("ok")]
    if not ok_frames:
        return {"status": "blocked", "reasons": reasons + ["could not be screened"], "people": None,
                "text": [], "score": None}

    most = max(people(f) for f in ok_frames)
    if tier == "scene" and most > 0:
        reasons.append("has people in it, and Google didn't match B's face")
    elif most > 1:
        reasons.append(f"{most} people in frame")
    elif tier == "me" and not any(faces(f) for f in ok_frames):
        reasons.append("no face visible, so it can't be confirmed as B")

    text = []
    for f in ok_frames:
        for s in f.get("text") or []:
            if s not in text:
                text.append(s)
    problem = text_problem(text)
    if problem:
        reasons.append(f"readable text: {problem}")
    elif text:
        warnings.append("text: " + ", ".join(text[:4]))

    if any(f.get("utility") for f in ok_frames):
        reasons.append("looks like a document or screenshot")

    scores = [f["aesthetics"] for f in ok_frames if f.get("aesthetics") is not None]
    score = round(sum(scores) / len(scores), 3) if scores else None

    status = "blocked" if reasons else ("warn" if warnings else "ok")
    return {"status": status, "reasons": reasons + warnings, "people": most, "text": text[:8],
            "score": score}


def run_vision(binary: Path, images: list[Path]) -> list[dict]:
    if not images:
        return []
    proc = subprocess.run([str(binary), *map(str, images)], capture_output=True, text=True,
                          timeout=600)
    out = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith("{")]
    by_path = {r["path"]: r for r in out}
    return [by_path.get(str(p), {"path": str(p), "ok": False}) for p in images]


def build_vision(swift_src: Path, binary: Path) -> Path:
    """Compile the Swift screener if it is missing or older than its source."""
    if binary.exists() and binary.stat().st_mtime >= swift_src.stat().st_mtime:
        return binary
    binary.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["swiftc", "-O", str(swift_src), "-o", str(binary)], check=True)
    return binary


def similar_groups(cands: list[dict], seconds: int = 20) -> dict[str, str]:
    """Bursts: key -> key of the best-scoring shot taken within `seconds`.

    The picker shows the best of each burst as the suggestion and folds the
    rest behind it, so ten near-identical frames cost one decision.
    """
    from datetime import datetime

    dated = sorted((c for c in cands if c.get("taken")), key=lambda c: c["taken"])
    leader, groups, current, last = {}, [], [], None
    for c in dated:
        t = datetime.fromisoformat(c["taken"])
        if last is not None and (t - last).total_seconds() > seconds:
            groups.append(current)
            current = []
        current.append(c)
        last = t
    if current:
        groups.append(current)
    for g in groups:
        best = max(g, key=lambda c: (c.get("screen") or {}).get("score") or -9)
        for c in g:
            leader[c["key"]] = best["key"]
    return leader
