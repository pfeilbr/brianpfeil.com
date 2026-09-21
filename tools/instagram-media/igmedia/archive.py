"""Read the instagram-archive project (~/projects/instagram/archive).

That project keeps every feed item as a directory with a normalised
metadata.json and a media/ folder:

    archive/posts/2025/2025-03-14__DHLzXu1uX9f/
        metadata.json   caption, taken_at, media list, location, …
        media/01.mp4, 01.thumb.jpg, 02.jpg, …

It is a better source than an Instagram export: complete (the index reports
every item on the profile), already downloaded, and keyed by shortcode.

Only feed posts and reels are read. Stories, highlights and the _oversized
copies (higher-bitrate duplicates of reels that are also in reels/) are not.
Location, tagged users and the raw API object are never carried through —
only caption, date and media leave this module.
"""

import json
from datetime import datetime
from pathlib import Path

from .export import Item, Media, sha256_file

SECTIONS = ("posts", "reels")


def _when(meta: dict) -> datetime:
    """The local time the photo was taken, so a late-evening post isn't
    dated the next day just because it was already tomorrow in UTC."""
    for key in ("taken_at_local", "taken_at"):
        value = meta.get(key)
        if value:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
    raise ValueError("no taken_at")


def _item(directory: Path) -> Item | None:
    meta_path = directory / "metadata.json"
    if not meta_path.is_file():
        return None
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    shortcode = meta.get("id") or directory.name.split("__")[-1]
    try:
        taken_at = _when(meta)
    except ValueError:
        return None

    media = []
    for entry in sorted(meta.get("media") or [], key=lambda m: m.get("index", 0)):
        path = directory / str(entry.get("file") or "")
        if not entry.get("file") or not path.is_file():
            continue
        kind = "video" if entry.get("type") == "video" else "photo"
        media.append(Media(path=path, kind=kind, sha256=sha256_file(path), taken_at=taken_at))
    if not media:
        return None

    caption = ((meta.get("caption") or {}).get("text") or "").strip()
    kind = "album" if len(media) > 1 else media[0].kind

    # The shortcode is Instagram's own identity for the post, so the id stays
    # the same whether the file is re-downloaded, re-encoded or re-exported —
    # unlike a content hash, which a different download quality would change.
    item_id = f"{taken_at.strftime('%Y%m%d')}-{shortcode}"
    return Item(id=item_id, taken_at=taken_at, caption=caption, kind=kind, media=media)


def read_archive(root: Path) -> list[Item]:
    """Every feed post and reel in the archive, newest first."""
    root = Path(root).expanduser()
    if not all((root / s).is_dir() for s in SECTIONS):
        raise ValueError(f"{root} doesn't look like an instagram-archive (needs posts/ and reels/)")

    items: dict[str, Item] = {}
    for section in SECTIONS:
        for directory in sorted((root / section).glob("*/*")):
            if directory.is_dir():
                item = _item(directory)
                if item is not None:
                    items[item.id] = item
    return sorted(items.values(), key=lambda i: (i.taken_at, i.id), reverse=True)
