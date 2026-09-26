"""Candidates from Google Photos, and the picks made from them.

Google Photos has no API that can read a library any more (the Library API
lost its read scopes in 2025), so candidates come from the Google Photos web
app itself: `picker/harvest.js` runs on a search results page in B's own,
signed-in browser and posts what the page shows to the local picker server.
Each result is a media key (Google's opaque id), a label such as
"Video - Landscape - Dec 25, 2022, 1:33:46 PM" and an lh3.googleusercontent.com
base URL, from which sized thumbnails and the original can be fetched.

Two files, with different lifetimes:

- build/gphotos/candidates.json — everything harvested, plus what screening
  found. Rebuildable, never committed: it holds URLs into a private library.
- picks.yaml — the decisions: which keys go on the site, in which category,
  and which were looked at and skipped. Committed (it is the record of what was
  chosen), so it holds opaque keys and nothing else — no URLs, no labels.
"""

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import yaml

LABEL = re.compile(
    r"^(?P<kind>Photo|Video)\b.*?-\s*(?P<date>[A-Z][a-z]{2} \d{1,2}, \d{4}, \d{1,2}:\d{2}:\d{2}\s*[AP]M)"
)
KEY = re.compile(r"^AF1Qip[A-Za-z0-9_-]{20,}$")
# Everything the page hands over is fetched from the Mac, so only Google's
# image host is accepted: a harvested "url" can never point anywhere else.
ALLOWED_HOST = re.compile(r"^(lh\d\.googleusercontent\.com|photos\.fife\.usercontent\.google\.com)$")


def parse_label(label: str) -> tuple[str, str | None, str | None]:
    """("photo"|"video", ISO timestamp or None, orientation or None)."""
    label = (label or "").replace(" ", " ").replace("\xa0", " ")
    m = LABEL.search(label)
    kind = "video" if label.startswith("Video") else "photo"
    orient = None
    for o in ("Portrait", "Landscape", "Square"):
        if f"- {o} -" in label:
            orient = o.lower()
    if not m:
        return kind, None, orient
    try:
        taken = datetime.strptime(m.group("date"), "%b %d, %Y, %I:%M:%S %p")
    except ValueError:
        return kind, None, orient
    return kind, taken.isoformat(timespec="seconds"), orient


def valid_url(url: str) -> bool:
    try:
        u = urlparse(url)
    except ValueError:
        return False
    return u.scheme == "https" and bool(ALLOWED_HOST.match(u.hostname or ""))


def reject_reason(row: dict) -> str | None:
    """Why a harvested row is ignored (for the harvest reply), or None."""
    if not KEY.match(row.get("key") or ""):
        return "unrecognised media key"
    url = row.get("url") or ""
    if not url:
        return "thumbnail had not loaded"
    if not valid_url(url):
        try:
            host = urlparse(url).hostname or "none"
        except ValueError:
            host = "unparseable"
        return f"image not on Google's image host ({host})"
    return None


def base_url(url: str) -> str:
    """Strip the query (?authuser=0) and the size suffix (=w256-h256-no…),
    so any size can be asked for."""
    return re.sub(r"=[^/=]*$", "", url.split("?", 1)[0])


def item_id(key: str, taken: str | None) -> str:
    """Stable, short and not the Google key: date plus a hash of the key."""
    day = (taken or "")[:10].replace("-", "") or "undated"
    return f"{day}-g{hashlib.sha1(key.encode()).hexdigest()[:10]}"


@dataclass
class Category:
    key: str
    query: str

    def queries(self, person: str, exclude: list[str] = ()) -> dict[str, str]:
        """Search text -> tier. "me": Google matched B's face; "scene": the
        activity alone, used only for shots with nobody in them (POV clips);
        "exclude": Google matched someone who must not appear, so every result
        is blocked wherever else it turns up."""
        out = {f"{person} {self.query}": "me", self.query: "scene"}
        for other in exclude:
            out[f"{other} {self.query}"] = "exclude"
        return out


def load_categories(cfg: dict) -> list[Category]:
    return [Category(c["key"], c["query"]) for c in cfg.get("categories") or []]


def query_index(categories: list[Category], person: str,
                exclude: list[str] = ()) -> dict[str, tuple[str, str]]:
    """Lower-cased search text -> (category key, tier)."""
    out = {}
    for c in categories:
        for q, tier in c.queries(person, exclude).items():
            out[q.lower()] = (c.key, tier)
    return out


class Candidates:
    """build/gphotos/candidates.json, keyed by media key."""

    def __init__(self, path: Path):
        self.path = path
        self.items: dict[str, dict] = {}
        # Keys Google matched to someone in exclude_people. Kept apart from
        # items: an exclusion search usually finds things no other search has.
        self.excluded: set[str] = set()
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            self.items = data.get("items", {})
            self.excluded = set(data.get("excluded", []))

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"items": self.items, "excluded": sorted(self.excluded)},
                                  indent=1, sort_keys=True), encoding="utf-8")
        tmp.replace(self.path)

    def exclude(self, rows: list[dict]) -> list[str]:
        """Record an exclusion search; returns candidate keys it newly blocks."""
        keys = {r.get("key") for r in rows if KEY.match(r.get("key") or "")}
        fresh = keys - self.excluded
        self.excluded |= keys
        return [k for k in fresh if k in self.items]

    def add(self, rows: list[dict], category: str, tier: str, query: str) -> int:
        """Merge one harvested results page; returns how many keys were new.

        A key found by a "me" search keeps tier "me" even if a scene search
        also finds it. The URL is refreshed every time, since Google's are
        long-lived but not permanent.
        """
        new = 0
        for row in rows:
            if reject_reason(row):
                continue
            key, url = row["key"], row["url"]
            kind, taken, orient = parse_label(row.get("label") or "")
            c = self.items.get(key)
            if c is None:
                new += 1
                c = self.items[key] = {"key": key, "id": item_id(key, taken), "categories": [],
                                       "tier": tier, "queries": []}
            c.update({"kind": kind, "taken": taken, "orient": orient, "url": base_url(url)})
            if category not in c["categories"]:
                c["categories"].append(category)
            if query not in c["queries"]:
                c["queries"].append(query)
            if tier == "me":
                c["tier"] = "me"
        return new


PICKS_HEADER = """\
# Google Photos picks for /media/. Written by the picker (make media-picker);
# fine to edit by hand. include: goes on the site in that category.
# skip: looked at and left out, so it is not suggested again. Keys are Google
# Photos media ids — opaque, and useless without access to the library.
"""


def load_picks(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {p["key"]: p for p in data.get("picks") or [] if isinstance(p, dict) and p.get("key")}


def save_picks(path: Path, picks: dict[str, dict]) -> None:
    rows = []
    for key in sorted(picks, key=lambda k: (picks[k].get("decision") != "include",
                                            picks[k].get("category") or "", k)):
        p = picks[key]
        row = {"key": key, "decision": p["decision"]}
        if p.get("category"):
            row["category"] = p["category"]
        rows.append(row)
    body = yaml.safe_dump({"picks": rows}, sort_keys=False, width=120)
    path.write_text(PICKS_HEADER + body, encoding="utf-8")
