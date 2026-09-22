"""Label the exported stories that reshare a post, using the iPhone story
inventory.

The instagram-archive project read every archived story off the iOS app
(harvest/iphone/story-inventory.jsonl): day, position in the day, and whether
it was a reshare. The export carries the media but not that last fact. Every
story is published — B wants the whole account here, reshares included — but
a reshare is labelled, so a visitor can tell someone else's post, or a reel
that is already on the page, from B's own story.

Stories are matched to the inventory by local day and order within the day,
which the inventory records ("2 of 5"); a minute alone is ambiguous, since
two dozen pairs of stories share one. When a day's count doesn't line up,
matching falls back to the minute, and every story in a minute that holds a
reshare gets the label. The failure mode is over-labelling one of B's
stories, never presenting someone else's post as B's.
"""

import json
from collections import defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo

LOCAL = ZoneInfo("America/New_York")  # the inventory's clock

# The kinds the inventory records, and how to say them. The key also goes
# into the data file as the item's `reshare`, which the viewer translates.
REASONS = {
    "other_post": "reshare of someone else's post",
    "own_reel": "reshare of a reel already on the page",
}


def load_inventory(path: Path | None) -> list[dict]:
    if not path:
        return []
    path = Path(path).expanduser()
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _local(item) -> tuple[str, str]:
    t = item.taken_at.astimezone(LOCAL)
    return t.strftime("%Y-%m-%d"), t.strftime("%H:%M")


def tag_reshares(items: list, inventory: list[dict]) -> list[tuple]:
    """Set `reshare` in the details of every story the inventory says is one,
    and return [(item, reason)] for them. Non-story items and stories on days
    the inventory doesn't cover are left alone."""
    by_day: dict[str, list] = defaultdict(list)
    for entry in inventory:
        by_day[entry["day"]].append(entry)

    stories = defaultdict(list)
    for item in items:
        if (item.details or {}).get("story"):
            stories[_local(item)[0]].append(item)

    tag: dict[str, str] = {}
    for day, day_stories in stories.items():
        entries = sorted(by_day.get(day, []), key=lambda e: e.get("seq", 0))
        reshares = [e for e in entries if e.get("reshare_of") in REASONS]
        if not reshares:
            continue
        day_stories.sort(key=lambda i: (i.taken_at, i.id))
        if len(entries) == len(day_stories):
            # The same stories, in the same order: pair them up.
            for entry, item in zip(entries, day_stories):
                if entry.get("reshare_of") in REASONS:
                    tag[item.id] = entry["reshare_of"]
        else:
            # Counts differ, so order can't be trusted. Label every story in a
            # minute that holds a reshare — erring toward over-labelling B's.
            for entry in reshares:
                for item in day_stories:
                    if _local(item)[1] == entry.get("local_time"):
                        tag[item.id] = entry["reshare_of"]

    tagged = []
    for item in items:
        if item.id in tag:
            item.details = {**(item.details or {}), "reshare": tag[item.id]}
            tagged.append((item, REASONS[tag[item.id]]))
    return tagged
