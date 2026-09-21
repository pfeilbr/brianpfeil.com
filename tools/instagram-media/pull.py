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

from igmedia import archive, audit, derive, export, manifest, publish, release, review  # noqa: E402

TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]


def load_config() -> dict:
    return yaml.safe_load((TOOL_DIR / "config.yaml").read_text(encoding="utf-8"))


def paths(cfg: dict) -> tuple[Path, Path, Path]:
    workdir = TOOL_DIR / cfg["work_dir"]
    manifest_path = TOOL_DIR / cfg["manifest"]
    data_path = REPO_ROOT / cfg["data_file"]
    return workdir, manifest_path, data_path


def load_items(args, cfg: dict, workdir: Path):
    """Items from an Instagram export if one was given, otherwise from the
    instagram-archive project (config archive_dir), which is the default."""
    if getattr(args, "export", None):
        root = export.unpack([p.expanduser() for p in args.export], workdir)
        return export.read_items(root)
    source = Path(getattr(args, "archive", None) or cfg["archive_dir"]).expanduser()
    return archive.read_archive(source)


def cmd_stage(args, cfg) -> int:
    workdir, manifest_path, _ = paths(cfg)
    items = load_items(args, cfg, workdir)
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

    # Before any encoding: a dead SSO token should cost a second, not an hour.
    if not args.dry_run:
        try:
            publish.check_credentials(cfg["bucket"])
        except publish.NotSignedIn as exc:
            print(exc, file=sys.stderr)
            return 1

    items = [i for i in load_items(args, cfg, workdir) if i.id in approved]
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
    removed = publish.deleted_paths(out)
    if removed:
        publish.invalidate(cfg["distribution_id"], removed)
        print(f"removed {len(removed)} files and evicted them from the CDN cache")
    publish.write_data_file(data_path, cfg["base_url"], entries)
    print(f"{len(entries)} items; {uploaded} files uploaded → {data_path.relative_to(REPO_ROOT)}")
    return 0


def cmd_release(args, cfg) -> int:
    """publish, then commit and push the data file and manifest — only those."""
    code = cmd_publish(args, cfg)
    if code != 0 or args.dry_run:
        return code

    _, manifest_path, data_path = paths(cfg)
    data = yaml.safe_load(data_path.read_text(encoding="utf-8")) or {}
    approved = len(manifest.approved_ids(list(manifest.load(manifest_path).values())))
    try:
        sha = release.commit_and_push(
            REPO_ROOT, [data_path, manifest_path],
            release.message_for(int(data.get("count", 0)), approved),
        )
    except release.ReleaseError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"released as {sha}; the site deploys from main" if sha
          else "nothing changed since the last release")
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


def cmd_audit(args, cfg) -> int:
    """Check every file the page references exists on the CDN."""
    _, _, data_path = paths(cfg)
    if not data_path.exists():
        print("nothing published yet; nothing to audit")
        return 0
    data = yaml.safe_load(data_path.read_text(encoding="utf-8")) or {}
    referenced = audit.referenced_keys(data)
    try:
        present = audit.list_objects(cfg["bucket"], cfg["s3_prefix"])
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1

    missing, orphaned = audit.audit(referenced, present)
    print(f"{len(referenced)} files referenced by the page, {len(present)} in the bucket")
    if missing:
        print(f"MISSING — broken on the live page ({len(missing)}):")
        for key in missing[:20]:
            print(f"  {key}")
        if len(missing) > 20:
            print(f"  … and {len(missing) - 20} more")
        print("re-run publish to upload them")
    if orphaned:
        print(f"{len(orphaned)} file(s) in the bucket that nothing references; "
              "publish --prune removes them and evicts them from the CDN")
    if not missing and not orphaned:
        print("ok: bucket and page agree")
    return 1 if missing else 0


def add_source(parser) -> None:
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--archive", type=Path,
                     help="instagram-archive directory (default: archive_dir in config.yaml)")
    src.add_argument("--export", nargs="+", type=Path,
                     help="Instagram export .zip(s), a directory of part ZIPs, or an unpacked export")


def main() -> int:
    cfg = load_config()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    stage = sub.add_parser("stage", help="read an export, update the approve list, build the review sheet")
    add_source(stage)
    stage.set_defaults(func=cmd_stage)

    approve = sub.add_parser("approve", help="mark items as publishable")
    group = approve.add_mutually_exclusive_group(required=True)
    group.add_argument("--id", help="comma-separated item ids")
    group.add_argument("--all", action="store_true", help="approve everything")
    group.add_argument("--none", action="store_true", help="unapprove everything")
    group.add_argument("--year", help="approve everything from this year, e.g. 2019")
    approve.set_defaults(func=cmd_approve)

    pub = sub.add_parser("publish", help="encode approved items, upload them, write the data file")
    add_source(pub)
    pub.add_argument("--prune", action="store_true", help="also delete S3 objects that are no longer approved")
    pub.add_argument("--dry-run", action="store_true", help="build locally, upload nothing")
    pub.set_defaults(func=cmd_publish)

    rel = sub.add_parser("release", help="publish, then commit and push only the data file and manifest")
    add_source(rel)
    rel.add_argument("--prune", action="store_true", help="also delete S3 objects that are no longer approved")
    rel.add_argument("--dry-run", action="store_true", help="build locally, upload and commit nothing")
    rel.set_defaults(func=cmd_release)

    aud = sub.add_parser("audit", help="check every file the page references is on the CDN")
    aud.set_defaults(func=cmd_audit)

    status = sub.add_parser("status", help="what is approved and what is live")
    status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    return args.func(args, cfg)


if __name__ == "__main__":
    sys.exit(main())
