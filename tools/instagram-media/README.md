# instagram-media

Builds `/media/` from an Instagram data export: reads the export, encodes web
copies, uploads them to S3, and writes `data/media.yaml`.

There is no Instagram scraping here and no Instagram credentials anywhere. The
export is the only input, which is what makes a run reproducible — and it is
also the only way to get this media without breaking Instagram's terms.

## Getting an export

[accountscenter.instagram.com/info_and_permissions/dyi](https://accountscenter.instagram.com/info_and_permissions/dyi/)
→ *Download or transfer information* → the Instagram account → *Some of your
information* → tick **Posts** and **Reels** → *Download to device* →
**Date range: All time**, **Format: JSON**, **Media quality: High**.

**Format must be JSON.** The HTML export carries the same media but no
machine-readable metadata, and nothing here can read it.

Instagram emails a link when the archive is ready; that can take hours.

A large account comes back as several part ZIPs. Pass them all, or just the
directory holding them — the JSON lives in one part and the media it refers to
is spread across the others, so they only make sense merged:

```sh
make media-stage EXPORT=~/Downloads/instagram-parts      # a directory, or
make media-stage EXPORT="part-1.zip part-2.zip part-3.zip"
```

If the whole archive is unwieldy, narrow the date range instead and run it
again later: ids are content hashes, so a second export merges rather than
duplicating, and keeps the approvals already made.

## Watching for it

`make media-watch-install` sets up a launchd agent that notices the export
arriving in `~/Downloads` and stages it straight away, with a macOS
notification pointing at the review sheet. It fires when Downloads changes
and every 30 minutes as a fallback.

- It only **stages**. Nothing is approved, encoded or uploaded.
- It waits for a download to finish: browser temp names (`.crdownload`,
  `.download`) are ignored, and a file must be two minutes old.
- It recognises an export by its contents, not just its name, and picks up
  every part together; the same set of parts is only staged once.
- `make media-watch-status` shows whether it is loaded and its last runs;
  the log is `~/Library/Logs/brianpfeil-instagram-watch.log`.
  `make media-watch-uninstall` removes it.

## Running it

```sh
make media-deps                                        # one-time venv
make media-stage EXPORT=~/Downloads/instagram-export.zip
open tools/instagram-media/build/review.html           # tick what to publish
python3 tools/instagram-media/pull.py approve --id ...  # the sheet writes this for you
make media-release EXPORT=~/Downloads/instagram-export.zip
```

`release` is `publish` followed by a commit and push of `data/media.yaml` and
`manifest.yaml` — by path, so nothing else that happens to be staged or
modified goes with them. `publish` on its own does everything but the commit.

`make media-status` prints what is approved and what is live.

## Approving

Nothing reaches the site until it is approved. `stage` writes every item into
`manifest.yaml` as `approved: false`; the review sheet is a local contact sheet
for flipping those to `true` by looking at the pictures. `approve --all`,
`--year 2019`, `--id a,b,c` and `--none` all work if editing YAML is faster.

Approvals survive a re-export. Item ids are derived from the media's own
bytes, so a fresh export of the same post produces the same id and keeps its
decision; only genuinely new posts arrive as `approved: false`.

## What ends up public

- Feed posts and reels only. Stories, archived posts, tagged photos and
  messages are never read, even though some exports contain them.
- Images are resized to 1600px, video re-encoded to 720p H.264.
- **All metadata is stripped** on the way through — export originals can still
  carry GPS coordinates, and these files go on a public CDN.
- Captions are published as-is, in whatever language they were written in.

## The page

- Thumbnails only in the grid; each tile is a real link to the full-size
  file, so the page works with JavaScript off.
- The lightbox opens on the cached thumbnail and sharpens when the full image
  arrives, preloads one neighbour each way (a poster, never a video), traps
  focus, and pages with arrow keys or a horizontal swipe.
- `tests/check_layout.py --build` renders the real page from
  `tests/fixtures/media.yaml` and checks it in all nine languages.

## Where the files go

Private S3 bucket `brianpfeil-media01`, served through CloudFront
(`dfalwjniugna7.cloudfront.net`) with origin access control — the bucket has no
public policy and direct S3 URLs return 403. Names contain a content hash, so
objects are immutable and cached for a year.

`--prune` deletes objects for items that are no longer approved. Without it,
un-approving an item removes it from the page but leaves the file on the CDN.

## Determinism

Re-running over the same export does nothing twice:

- ids come from the sha256 of the media, not filenames or ordering
- `derivatives.lock.json` records what has been encoded, keyed by source hash
  plus `PROFILE_VERSION` in `igmedia/derive.py` — bump that to force a re-encode
- uploads use `aws s3 sync --size-only` against content-hashed names
- `data/media.yaml` is regenerated wholesale and sorted newest-first

## Layout

| File | Does |
| --- | --- |
| `pull.py` | CLI: `stage`, `approve`, `publish`, `status` |
| `igmedia/export.py` | reads the export JSON, resolves media, assigns ids |
| `igmedia/derive.py` | resize/transcode via Pillow and ffmpeg, plus the lockfile |
| `igmedia/manifest.py` | the approve list |
| `igmedia/review.py` | the local contact sheet |
| `igmedia/publish.py` | `aws s3 sync` and `data/media.yaml` |
| `tests/` | `make test-media`; `make_fixture.py` builds a synthetic export |

Requires ffmpeg and an AWS CLI that is already logged in; uploads use whatever
credentials the shell has rather than storing any of their own.
