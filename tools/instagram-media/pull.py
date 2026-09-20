#!/usr/bin/env python3
"""Build /media/ from an Instagram data export.

    pull.py stage   --export ~/Downloads/instagram-export.zip   # read + review
    pull.py approve --id 20230101-ab12cd34,20230115-9f0e1d2c    # decide
    pull.py publish --export ~/Downloads/instagram-export.zip   # encode + upload

The export is the only input; there is no network call to Instagram. Running
the same export twice produces the same ids, the same files and the same
uploads, so a re-run after a new export only does the work that is new.
"""

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from igmedia import derive, export, manifest, publish, review  # noqa: E402

TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]


def load_config() -> dict:
    return yaml.safe_load((TOOL_DIR / "config.yaml").read_text(encoding="utf-8"))


def paths(cfg: dict) -> tuple[Path, Path, Path]:
    workdir = TOOL_DIR / cfg["work_dir"]
    manifest_path = TOOL_DIR / cfg["manifest"]
    data_path = REPO_ROOT / cfg["data_file"]
    return workdir, manifest_path, data_path


def cmd_stage(args, cfg) -> int:
    workdir, manifest_path, _ = paths(cfg)
    root = export.unpack(Path(args.export).expanduser(), workdir)
    items = export.read_items(root)
    if not items:
        print("no posts or reels found — is this a JSON export with media?", file=sys.stderr)
        return 1

    records = manifest.merge(items, manifest.load(manifest_path))
    manifest.save(manifest_path, records)

    sheet = review.build(items, records, workdir)
    approved = len(manifest.approved_ids(records))
    print(f"{len(items)} items ({approved} approved) → {manifest_path.relative_to(REPO_ROOT)}")
    print(f"review: open {sheet}")
    return 0


def cmd_approve(args, cfg) -> int:
    _, manifest_path, _ = paths(cfg)
    existing = manifest.load(manifest_path)
    if not existing:
        print("no manifest yet — run `stage` first", file=sys.stderr)
        return 1

    records = list(existing.values())
    wanted = set()
    if args.id:
        wanted = {i.strip() for i in args.id.split(",") if i.strip()}
        unknown = wanted - set(existing)
        if unknown:
            print(f"unknown ids: {', '.join(sorted(unknown))}", file=sys.stderr)
            return 1

    changed = 0
    for record in records:
        if args.all:
            new = True
        elif args.none:
            new = False
        elif args.year:
            new = record["date"].startswith(args.year) or bool(record.get("approved"))
        else:
            new = record["id"] in wanted
        if bool(record.get("approved")) != new:
            record["approved"] = new
            changed += 1

    manifest.save(manifest_path, records)
    total = len(manifest.approved_ids(records))
    print(f"{changed} changed; {total} of {len(records)} approved")
    return 0


def cmd_publish(args, cfg) -> int:
    workdir, manifest_path, data_path = paths(cfg)
    records = list(manifest.load(manifest_path).values())
    if not records:
        print("no manifest yet — run `stage` first", file=sys.stderr)
        return 1

    approved = manifest.approved_ids(records)
    if not approved:
        print("nothing approved yet; see the manifest or the review sheet", file=sys.stderr)
        return 1

    root = export.unpack(Path(args.export).expanduser(), workdir)
    items = [i for i in export.read_items(root) if i.id in approved]
    missing = approved - {i.id for i in items}
    if missing:
        print(f"warning: {len(missing)} approved items are not in this export", file=sys.stderr)

    build_dir = workdir / "media"
    lock = derive.Lock(TOOL_DIR / cfg["lock_file"])
    entries = []
    for n, item in enumerate(items, 1):
        derived = [
            derive.derive(m, item.id, build_dir, cfg["s3_prefix"], lock) for m in item.media
        ]
        entries.append(publish.entry_for(item, derived))
        print(f"  [{n}/{len(items)}] {item.id} {item.kind}", flush=True)
    lock.save()

    if args.dry_run:
        print(f"dry run: {len(entries)} items built in {build_dir}, nothing uploaded")
        return 0

    out = publish.sync(build_dir, cfg["bucket"], cfg["s3_prefix"], prune=args.prune)
    uploaded = len([l for l in out.splitlines() if l.startswith("upload:")])
    publish.write_data_file(data_path, cfg["base_url"], entries)
    print(f"{len(entries)} items; {uploaded} files uploaded → {data_path.relative_to(REPO_ROOT)}")
    return 0


def cmd_status(args, cfg) -> int:
    _, manifest_path, data_path = paths(cfg)
    records = list(manifest.load(manifest_path).values())
    approved = manifest.approved_ids(records)
    print(f"manifest: {len(records)} items, {len(approved)} approved")
    if data_path.exists():
        data = yaml.safe_load(data_path.read_text(encoding="utf-8")) or {}
        print(f"published: {data.get('count', 0)} items at {data.get('base_url')}")
    else:
        print("published: nothing yet")
    return 0


def main() -> int:
    cfg = load_config()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    stage = sub.add_parser("stage", help="read an export, update the approve list, build the review sheet")
    stage.add_argument("--export", required=True, help="path to the export .zip or unpacked directory")
    stage.set_defaults(func=cmd_stage)

    approve = sub.add_parser("approve", help="mark items as publishable")
    group = approve.add_mutually_exclusive_group(required=True)
    group.add_argument("--id", help="comma-separated item ids")
    group.add_argument("--all", action="store_true", help="approve everything")
    group.add_argument("--none", action="store_true", help="unapprove everything")
    group.add_argument("--year", help="approve everything from this year, e.g. 2019")
    approve.set_defaults(func=cmd_approve)

    pub = sub.add_parser("publish", help="encode approved items, upload them, write the data file")
    pub.add_argument("--export", required=True, help="path to the export .zip or unpacked directory")
    pub.add_argument("--prune", action="store_true", help="also delete S3 objects that are no longer approved")
    pub.add_argument("--dry-run", action="store_true", help="build locally, upload nothing")
    pub.set_defaults(func=cmd_publish)

    status = sub.add_parser("status", help="what is approved and what is live")
    status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    return args.func(args, cfg)


if __name__ == "__main__":
    sys.exit(main())
