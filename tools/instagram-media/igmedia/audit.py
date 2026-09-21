"""Compare what the page references with what the bucket holds.

The data file and the uploads are separate steps, so they can disagree: an
upload that died partway leaves the page pointing at files that don't exist,
and un-approving without --prune leaves files nothing points at. The first is
a broken page for visitors; the second is just clutter (and, for something
un-approved, still reachable by anyone holding the URL).
"""

import json
import subprocess


def referenced_keys(data: dict) -> set[str]:
    """Every object key data/media.yaml points at."""
    keys = set()
    for item in data.get("items") or []:
        for media in item.get("media") or []:
            for field in ("src", "thumb", "poster"):
                if media.get(field):
                    keys.add(media[field])
    return keys


def list_objects(bucket: str, prefix: str, run=subprocess.run) -> set[str]:
    """Every key under the prefix. The CLI paginates for us."""
    proc = run(
        ["aws", "s3api", "list-objects-v2", "--bucket", bucket, "--prefix", f"{prefix}/",
         "--query", "Contents[].Key", "--output", "json"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"listing s3://{bucket}/{prefix} failed: {proc.stderr.strip()[:300]}")
    keys = json.loads(proc.stdout or "null")
    return set(keys or [])  # an empty prefix comes back as null


def audit(referenced: set[str], present: set[str]) -> tuple[list[str], list[str]]:
    """(missing, orphaned), both sorted."""
    return sorted(referenced - present), sorted(present - referenced)
