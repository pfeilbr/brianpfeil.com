"""Read the instagram-archive project (~/projects/instagram/archive).

That project keeps every feed item as a directory with a normalised
metadata.json and a media/ folder:

    archive/posts/2025/2025-03-14__DHLzXu1uX9f/
        metadata.json   caption, taken_at, media list, location, …
        media/01.mp4, 01.thumb.jpg, 02.jpg, …

It is a better source than an Instagram export: complete (the index reports
every item on the profile), already downloaded, keyed by shortcode, and it
carries what Instagram shows beside a post — see details().

Only feed posts and reels are read. Stories, highlights and the _oversized
copies (higher-bitrate duplicates of reels that are also in reels/) are not.
Only what Instagram itself displays leaves this module: the place *name*
but never the GPS coordinates stored with it, tagged usernames but not their
on-photo positions, and none of the raw API object.
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


def details(meta: dict) -> dict:
    """What Instagram shows beside the post, and nothing more.

    Built by allow-list: a field only appears here if it is named below, so
    a new field in the archive can't reach the page by accident. The place
    comes through as its name and Instagram's place id — the lat/lng stored
    next to them never do; Instagram doesn't show those either.
    """
    out: dict = {}
    if meta.get("permalink"):
        out["permalink"] = meta["permalink"]

    place = meta.get("location") or {}
    if place.get("name"):
        out["location"] = {"name": place["name"]}
        if place.get("pk"):
            out["location"]["id"] = str(place["pk"])

    counts = meta.get("counts") or {}
    for key in ("likes", "comments"):
        if isinstance(counts.get(key), int):
            out[key] = counts[key]
    # Counts are a snapshot, not live; say when it was taken.
    if meta.get("archived_at") and ("likes" in out or "comments" in out):
        out["counted"] = str(meta["archived_at"])[:10]

    tagged = []
    for tag in meta.get("tagged_users") or []:
        name = tag.get("username") if isinstance(tag, dict) else None
        if name and name not in tagged:
            tagged.append(name)
    if tagged:
        out["tagged"] = tagged

    audio = meta.get("audio") or {}
    if audio.get("type") == "original_audio":
        out["audio"] = "original"
    elif audio.get("type") not in (None, "none") and audio.get("title"):
        out["audio"] = " · ".join(x for x in (audio.get("title"), audio.get("artist")) if x)

    if meta.get("kind") == "reel":
        out["reel"] = True
    return out


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
    return Item(id=item_id, taken_at=taken_at, caption=caption, kind=kind, media=media,
                details=details(meta))


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
