"""Read an Instagram "Download your information" export.

The export is the only source of truth here: no network calls, no scraping,
so a given ZIP always produces the same items in the same order.
"""

import hashlib
import json
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# Instagram has moved the activity files around between export versions, so
# look for the JSON by name anywhere under the export root rather than
# hard-coding "your_instagram_activity/media/".
POST_GLOBS = ("posts_*.json", "posts.json")
REEL_GLOBS = ("reels.json", "reels_*.json")

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
VIDEO_SUFFIXES = {".mp4", ".mov", ".m4v"}


@dataclass
class Media:
    """One photo or video file inside a post."""

    path: Path
    kind: str  # "photo" | "video"
    sha256: str
    taken_at: datetime


@dataclass
class Item:
    """A post, reel, or carousel — one tile on the media page."""

    id: str
    taken_at: datetime
    caption: str
    kind: str  # "photo" | "video" | "album"
    media: list[Media] = field(default_factory=list)

    @property
    def date(self) -> str:
        return self.taken_at.strftime("%Y-%m-%d")


def fix_mojibake(text: str) -> str:
    """Undo the double-encoding Meta applies to exported strings.

    Captions come out of the export as UTF-8 bytes that were then decoded as
    latin-1, so an emoji arrives as "\\u00f0\\u009f\\u0098\\u0080". Reversing
    that is lossless when it round-trips and a no-op when it doesn't, which is
    what makes it safe to apply to every string.
    """
    if not text:
        return ""
    try:
        return text.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def unpack(export: Path, workdir: Path) -> Path:
    """Return a directory holding the export, extracting the ZIP if needed."""
    if export.is_dir():
        return export
    if export.suffix.lower() != ".zip":
        raise ValueError(f"expected a .zip or a directory, got {export}")

    # Key the extraction on the archive's size and name so re-running against
    # the same download doesn't unpack it again.
    tag = hashlib.sha256(f"{export.name}:{export.stat().st_size}".encode()).hexdigest()[:12]
    dest = workdir / "export" / tag
    marker = dest / ".extracted"
    if marker.exists():
        return dest

    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(export) as zf:
        for member in zf.namelist():
            # Refuse absolute paths and traversal; an export is trusted input
            # but a ZIP is still a ZIP.
            target = (dest / member).resolve()
            if not str(target).startswith(str(dest.resolve())):
                raise ValueError(f"unsafe path in archive: {member}")
        zf.extractall(dest)
    marker.write_text("")
    return dest


def _find_json(root: Path, globs: tuple[str, ...]) -> list[Path]:
    found: list[Path] = []
    for pattern in globs:
        found.extend(root.rglob(pattern))
    # Sorted so posts_1.json, posts_2.json … are always read in the same order.
    return sorted(set(found))


def _media_kind(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix in IMAGE_SUFFIXES:
        return "photo"
    if suffix in VIDEO_SUFFIXES:
        return "video"
    return None


def _resolve(root: Path, uri: str) -> Path | None:
    """Map a URI from the JSON onto a file on disk."""
    uri = uri.lstrip("/")
    candidate = root / uri
    if candidate.exists():
        return candidate
    # Some exports prefix the media paths with the account folder; fall back to
    # matching on the trailing path so those still resolve.
    tail = Path(uri).name
    matches = sorted(root.rglob(tail))
    return matches[0] if matches else None


def _entries(payload: object) -> list[dict]:
    """Posts are a bare list; reels and stories are wrapped in a single key."""
    if isinstance(payload, list):
        return [e for e in payload if isinstance(e, dict)]
    if isinstance(payload, dict):
        for value in payload.values():
            if isinstance(value, list):
                return [e for e in value if isinstance(e, dict)]
    return []


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, (int, float)) or value <= 0:
        return None
    return datetime.fromtimestamp(value, tz=timezone.utc)


def _build_item(entry: dict, root: Path) -> Item | None:
    raw_media = entry.get("media")
    if not isinstance(raw_media, list):
        return None

    media: list[Media] = []
    for m in raw_media:
        if not isinstance(m, dict):
            continue
        uri = m.get("uri")
        if not isinstance(uri, str):
            continue
        path = _resolve(root, uri)
        if path is None or not path.is_file():
            continue
        kind = _media_kind(path)
        if kind is None:
            continue
        taken = _timestamp(m.get("creation_timestamp")) or _timestamp(
            entry.get("creation_timestamp")
        )
        media.append(
            Media(
                path=path,
                kind=kind,
                sha256=sha256_file(path),
                taken_at=taken or datetime.fromtimestamp(0, tz=timezone.utc),
            )
        )

    if not media:
        return None

    taken_at = _timestamp(entry.get("creation_timestamp")) or min(m.taken_at for m in media)

    # The caption sits on the post for carousels and on the single media entry
    # for everything else, so prefer the post's and fall back.
    caption = fix_mojibake(entry.get("title") or "")
    if not caption:
        for m in raw_media:
            if isinstance(m, dict) and m.get("title"):
                caption = fix_mojibake(m["title"])
                break

    if len(media) > 1:
        kind = "album"
    else:
        kind = media[0].kind

    # The id has to survive re-exports, so derive it from the bytes rather than
    # from filenames or list position, both of which Instagram reshuffles.
    digest = hashlib.sha256("".join(m.sha256 for m in media).encode()).hexdigest()[:8]
    item_id = f"{taken_at.strftime('%Y%m%d')}-{digest}"

    return Item(id=item_id, taken_at=taken_at, caption=caption.strip(), kind=kind, media=media)


def read_items(root: Path) -> list[Item]:
    """Return every post and reel in the export, newest first."""
    items: dict[str, Item] = {}
    for path in _find_json(root, POST_GLOBS) + _find_json(root, REEL_GLOBS):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        for entry in _entries(payload):
            item = _build_item(entry, root)
            if item is not None:
                # Cross-posted reels can appear in both files; the id is
                # content-derived, so the duplicate collapses onto itself.
                items[item.id] = item

    return sorted(items.values(), key=lambda i: (i.taken_at, i.id), reverse=True)
