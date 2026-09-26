# instagram-media

Builds `/media/` from an Instagram data export: reads the export, encodes web
copies, uploads them to S3, and writes `data/media.yaml`.

There is no Instagram scraping here and no Instagram credentials anywhere. The
export is the only input, which is what makes a run reproducible — and it is
also the only way to get this media without breaking Instagram's terms.

## Sources

**The instagram-archive project (default).** `~/projects/instagram/archive`,
set as `archive_dir` in `config.yaml`, keeps every feed item as a directory of
`metadata.json` + `media/`. `igmedia/archive.py` reads `posts/` and `reels/`
only — not stories, highlights, or `_oversized/` (higher-bitrate duplicates
of reels already in `reels/`). Location, tagged users and the raw API object
never leave that module. Ids are the local date plus Instagram's shortcode.

    make media-sync     # stage, approve everything, release; a no-op when nothing is new

**An Instagram export**, with `--export` / `EXPORT=…`, as described below.

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
arriving in `~/Downloads` and publishes its stories straight away (`sync`),
with a macOS notification. It fires when Downloads changes and every 30
minutes as a fallback.

- It **publishes** (`WATCH_ACTION = "sync"` in `watch_downloads.py`); set it
  to `"stage"` to review before anything goes live.
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

- Feed posts and reels, plus — from an export — stories and archived posts
  (ones taken off the profile with "Archive"; the viewer labels them
  "Archived post"). Stories that reshare a post are published too, labelled
  "Reshared post" / "Reshared reel". Recently deleted items, tagged photos
  and messages are never read, even though some exports contain them.
- Images are capped at 1600px on the long edge. Video that is already
  web-ready (H.264, AAC or silent, ≤1280px, ≤8 Mbps) is remuxed untouched;
  anything else (HEVC, larger, higher bitrate) is re-encoded to H.264.
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

## Sound

Every published video has sound. A clip with no audio track — or one whose
loudest moment is below -45 dBFS — gets music from `igmedia/music.py`: six
original tracks synthesised with numpy (pad, arpeggio, bass, light drums,
reverb), deterministic, seamless when looped, and royalty-free because they
are composed here rather than downloaded. Each post gets one track at a
deterministic offset; the picture is copied untouched; the file gets a new
name so the silent version's year-long cache can't leave anyone hearing
nothing. The viewer says "♪ <track> · music added".

## Stories

The archive has no story files, only an inventory. Stories come from an
Instagram export: `--export` adds the export's stories to the archive's
posts and reels. Stories that reshare a post are found by matching the
inventory on local day and order within the day (`igmedia/stories.py`) and
published with a label — "Reshared post" for someone else's, "Reshared reel"
for one of B's reels that is already on the page — so nobody takes them
for B's own footage.

## Archived posts

A post hidden with Instagram's "Archive" is on no profile page, so the
instagram-archive project never sees it; the export's `archived_posts.json`
is the only source. `--export` reads it alongside the stories. One that was
archived and later restored is already in the archive project, and is
skipped by matching the second it was posted.

## Google Photos categories

Below Instagram, `/media/` has a section per activity — skiing, mountain
biking, kayaking, swimming, beach, hiking (`gphotos.categories` in
`config.yaml`) — with a row of links at the top to jump between Instagram
and each of them. The picks come from Google Photos, chosen by hand in a
local web app:

    make media-picker        # http://127.0.0.1:8790

**Only B, nothing private.** Candidates come from Google Photos' own
search. "Brian Pfeil skiing" finds shots Google matched to B's face; plain
"skiing" finds scenes, which are only offered if nobody is in them (POV
clips, landscapes). Then:

- every candidate is screened on this Mac with Apple Vision
  (`vision/screen.swift`, policy in `igmedia/screen.py`): a "me" shot must
  show exactly one person and a visible face; people are counted by face,
  body, upper body and person segmentation, and the highest count wins —
  bodies down to 0.1% of the frame, so kids riding far off still count;
- anything Google matched to someone in `gphotos.exclude_people` (B's sons)
  is blocked, whatever else found it — "Wyatt Pfeil skiing" and so on are
  harvested for that alone;
- a "scene" shot (found by the activity alone) is blocked by anyone at all
  in it, however small — a swimmer far out on a beach counts;
- readable text that looks like a number plate, house number, phone number,
  street, email or a page of writing blocks it; other text (a logo, a trail
  sign) is shown as a warning; receipts, screenshots and documents are blocked;
- publishing screens each pick again from the file it is published from;
- nothing is published with a caption, place, date-and-time or person: only
  the media and its date. Metadata (GPS included) is stripped by the same
  encode Instagram media goes through.

Screening has one known gap: two people pressed together in a selfie, both
in goggles and one in a balaclava, can read as one. B looks at everything
before including it; the picker says so.

**The picker.** Categories down the side, best suggestions first, bursts of
near-identical shots folded behind the best one ("+3 similar", `e` to open).
`i` (or a click) to include, `x` to skip, `s` to skip everything else on
screen, `1`–`9` to include into another category, `z` to undo. What is
picked for the category sits in a strip above the grid (× to remove; red if
it no longer passes screening). Enter, `p` or a video's ▶ opens it large —
videos play with sound, and the viewer has Include and Skip buttons.
Videos also play silently on hover. A motion photo (a still with a few
seconds of video, which Google marks with a play button) plays its clip
too, labelled "motion"; the still is what goes on the site, and its clip is
screened along with it, since the clip can show someone the still doesn't. Every decision is written to
`picks.yaml` at once; skipped items are never suggested again. **Publish**
encodes, uploads to `s3://brianpfeil-media01/photos/`, writes
`data/photos.yaml`, and commits and pushes just those two files.

**Getting more from Google Photos.** Google has no API that can read a
library any more, and its image host only answers B's signed-in browser, so
the browser does the fetching. "Get more from Google Photos" in the picker
has a **Send to picker** bookmarklet and a link to every search. Open a
search, click the bookmarklet: it scrolls the results, sends them to the
picker, then downloads what the picker asks for (thumbnails and screening
copies, and 1080p video for picks) and posts the bytes to 127.0.0.1. No
cookie leaves Chrome. The first time, Chrome asks whether photos.google.com
may reach devices on the local network — allow it. The bookmarklet only
loads `picker/harvest.js` from the picker, so changes to it need no re-drag.

What stays local: `build/gphotos/` (candidates, their Google URLs, thumbnails,
screening results) is never committed. `picks.yaml` is — it holds Google's
opaque media keys and decisions, nothing else.

## Checking it

`make media-audit` compares every file `data/media.yaml` references with what
is actually in the bucket. Missing files are broken images on the live page
(an upload that died partway) and make it exit 1; files nothing references
are reported as orphans that `publish --prune` would remove.

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
| `igmedia/picker.py` | the Google Photos picker's server (`make media-picker`) |
| `igmedia/gphotos.py` | harvested candidates and `picks.yaml` |
| `igmedia/screen.py` | the screening policy: only B, nothing private |
| `igmedia/gphotos_publish.py` | picks to `data/photos.yaml` |
| `vision/screen.swift` | Apple Vision: people, text, aesthetics |
| `picker/` | the picker page and the harvest script |
| `tests/` | `make test-media`; `make_fixture.py` builds a synthetic export |

Requires ffmpeg and an AWS CLI that is already logged in; uploads use whatever
credentials the shell has rather than storing any of their own.
