"""Decide which exported stories to publish, using the iPhone story inventory.

The instagram-archive project read every archived story off the iOS app
(harvest/iphone/story-inventory.jsonl): day, position in the day, and whether
it was a reshare. The export carries the media but not that last fact, and it
matters:

- a reshare of someone else's post is their content — never republished
- a reshare of one of B's own reels is already on the page as the reel

Stories are matched to the inventory by local day and order within the day,
which the inventory records ("2 of 5"); a minute alone is ambiguous, since
two dozen pairs of stories share one. When a day's count doesn't line up,
matching falls back to the minute, and every story in a minute that holds a
reshare is left out. The failure mode is dropping one of B's stories, never
publishing someone else's.
"""

import json
from collections import defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo

LOCAL = ZoneInfo("America/New_York")  # the inventory's clock

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


def filter_reshares(items: list, inventory: list[dict]) -> tuple[list, list[tuple]]:
    """(kept, dropped) where dropped is [(item, reason)]. Non-story items and
    stories on days the inventory doesn't cover pass straight through."""
    by_day: dict[str, list] = defaultdict(list)
    for entry in inventory:
        by_day[entry["day"]].append(entry)

    stories = defaultdict(list)
    for item in items:
        if (item.details or {}).get("story"):
            stories[_local(item)[0]].append(item)

    drop: dict[str, str] = {}
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
                    drop[item.id] = REASONS[entry["reshare_of"]]
        else:
            # Counts differ, so order can't be trusted. Drop every story in a
            # minute that holds a reshare — erring toward leaving B's out.
            for entry in reshares:
                for item in day_stories:
                    if _local(item)[1] == entry.get("local_time"):
                        drop[item.id] = REASONS[entry["reshare_of"]] + " (matched by minute)"

    kept = [i for i in items if i.id not in drop]
    dropped = [(i, drop[i.id]) for i in items if i.id in drop]
    return kept, dropped
