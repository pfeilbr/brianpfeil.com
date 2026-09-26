# brianpfeil.com

Hugo site. `content/post/*.md` are blog/project posts; `content/projects/` are project bundles.

**The home page is a table of contents, not the post list.** `/` is an
about-style hero plus a card per section (`layouts/index.html`, driven by
`data/home.yaml`; titles/blurbs are `hub_<key>_title` / `hub_<key>_blurb`).
Posts, Media and Movies are wide cards with a preview (latest titles, newest
tiles, first posters); the rest are plain cards listed in the YAML.
The searchable, infinitely-scrolling post list lives at `/post/`
(`layouts/post/list.html`, `content/post/_index.<lang>.md` in all nine
languages). A new section = one entry in `data/home.yaml` + its i18n keys.

## Where /media/ stands (read this first)

**Live, with all 89 feed items** (79 posts, 10 reels, 2011–2026; 575 photos
and videos, 1,382 files on the CDN) — released as `bf44087` on 2026-09-21.

**The source is the instagram-archive project**, `~/projects/instagram/archive`
(`archive_dir` in `tools/instagram-media/config.yaml`), which keeps every feed
item as `metadata.json` + `media/`. Only posts and reels are read; stories,
highlights and `_oversized/` (higher-bitrate duplicates of reels) are not.
Every record carries a GPS location and tagged users; neither is published.
Ids are local date + Instagram shortcode, so they survive re-downloads.

To refresh after the archive picks up new posts — one command, repeatable,
and a no-op when nothing is new:

```sh
make media-sync        # stage, approve every item, encode, upload, commit, push
make media-audit       # confirm every referenced file is on the CDN
```

The account is public, which is why everything is approved by default. To
publish selectively instead: `make media-stage`, tick items in
`tools/instagram-media/build/review.html`, `make media-release`. To take
something down: `pull.py approve --id …` to unapprove, then
`pull.py release --prune` (also evicts it from CloudFront).

**Every video has sound.** 102 of 234 had none; they get original music
composed by `igmedia/music.py` (six seeded tracks, royalty-free because they
are generated here, never downloaded). "Silent" includes an audio track that
never gets louder than -45 dBFS. The viewer labels it "♪ Sunlit · music
added" so nobody mistakes it for recorded sound.

**Everything B made goes on /media/, whether or not the profile shows it** —
stories and posts hidden with "Archive" included. Both exist only in the
export (`archived_posts.json`, `stories.json`); the viewer labels them
"Story" / "Archived post". Stories that reshared a post go up as well,
labelled "Reshared post" (someone else's) or "Reshared reel" (one of B's,
already on the page) — B asked for reshares included. Still never
published: recently-deleted items.

**Stories and archived posts are pending the Instagram export.** The archive knows about 153
archived stories only as an inventory (`harvest/iphone/story-inventory.jsonl`),
not their files. The export requested 2026-09-21 (Media, all time, JSON,
medium) carries them. When it lands in `~/Downloads`, the watcher runs
`pull.py sync --export …`: posts and reels still from the archive, stories
and archived posts from the export, reshares labelled (2 of someone else's
posts, 9 of B's own reels — `igmedia/stories.py`), silent stories given
music, pushed live.
Download it within four days of Meta's email; it needs B's password.

**Below Instagram: activity sections from Google Photos** (skiing, mountain
biking, kayaking, swimming, beach, hiking), with a row of links at the top of
/media/ to jump between them. B picks them in a local web app,
`make media-picker` (http://127.0.0.1:8790), which only suggests what passed
screening: only B (Apple Vision people count + Google's own face matching of
`exclude_people` — his sons must never appear), no plates, addresses or
documents. The browser does all fetching from Google (a bookmarklet), since
Google's image host refuses anything without B's session. Details and the one
known screening gap: `tools/instagram-media/README.md`, "Google Photos
categories". Never publish a pick B didn't make.

`aws sso login` first if the session has expired — `publish` checks before encoding.

`make verify` runs every test suite (Go post generator, Python media tool,
link checker), a render check that builds `/media/` from a fixture and with
no data and asserts on `/data/media.json` and the page shell in all nine
languages, and a
warning-surfacing Hugo build. The Tests workflow runs the same on every push
and PR, plus `terraform fmt` and `validate` on both stacks.

**Open decision for B: 16 posts link to repos that are now private.** Their
"code for article" link 404s for visitors. `make check-repo-links` lists them
(it exits 1 while any are broken). The options are to make those repos
public, remove the posts, or keep the posts and drop the link — nothing has
been changed until B picks one.

**Terraform manages all of the AWS side.** State is remote in
`s3://brianpfeil-tfstate-529276214230` (versioned, native S3 locking, no
DynamoDB); `infra/bootstrap/` creates that bucket. `aws sso login`, then
`make tf-init` and `make tf-plan` — both stacks should report no changes.
Apply only from a saved plan (`terraform plan -out=x.tfplan`, read it, then
`terraform apply x.tfplan`); `-auto-approve` is blocked as a blind apply.
The AWS provider comes from a local mirror because the registry download is
unreliable here — see `infra/README.md`.

## Workflow

- **Always commit and push immediately** after making changes — don't wait to be asked.
  The site deploys from `main`, and B wants to see changes live quickly.
- Commit only the files related to the current task; leave unrelated
  work-in-progress changes uncommitted.
- After pushing, poll the live site until the change appears — the deploy takes
  roughly one to two minutes. Verify the real thing, don't just assume.

## Gotchas that have bitten before

- **The CSS is not Tailwind.** `assets/css/main.css` is hand-written utility CSS
  that happens to use Tailwind-ish names. Only the classes actually defined in
  that file exist; any other utility class in a template is a silent no-op.
  Check before using one.
- **The site ships in nine languages.** English at the root; `zh es pt fr de it
  ja ko` under `/<code>/`. Every new UI string goes in **all nine**
  `i18n/*.toml`. Posts are English-only by design; standalone pages and layouts
  are translated.
- **Hugo falls back to English silently, and an empty value counts as
  missing.** A blank `other = ""` renders the English string with no warning —
  that is how `/ja/` once shipped an English author line. So key-count parity
  is not proof; check the rendered HTML for English sentences too.
- **Editorial prose belongs in i18n, not in `data/`.** Category labels, group
  blurbs and playlist notes are looked up as `cat_label_<key>`,
  `cat_blurb_<key>`, `feeds_label_<key>`, `feeds_blurb_<key>` and
  `pl_note_<key>`; the YAML holds structure and ids only. Anything left as
  prose in a data file will render in English on all eight other sites.
- **A string that has to wrap around a link needs a placeholder, not a
  prefix/suffix pair.** `author_role` takes `{{ .company }}` because Japanese
  and Korean put the employer before the job title.
- **Production HTML is minified**, so attributes come out unquoted
  (`class=ptab`). `grep 'class="ptab"'` against the live site finds nothing and
  looks like a broken deploy. Grep for the bare value.
- Run the dev server through the preview tooling (`.claude/launch.json`, config
  name `hugo`), never `hugo server` in Bash.
- **CI's Hugo version is pinned** in `.github/workflows/gh-pages.yml`. It used
  to be `latest`, and 0.166.0 broke the build (`return` must be the last
  command in its pipeline). A push can build locally and still fail to deploy
  if the local Hugo is a different version, so check the Actions run, not just
  the local build. Bump the pin on purpose.
- **The nav row is capped, so it never gets roomier.** `.nav-row` is
  `max-width: 56rem`: widening the browser adds nothing, and a seventh link
  overlapped the language switcher at *every* width, not just narrow ones.
  `.lang-label` truncates so flexbox can shrink instead of overlapping —
  check a long-worded language (es, fr) before adding another nav item.
- **Inline JSON for a script needs `safeJS`.** Same trap as the JSON-LD in
  `head-meta.html`: without it Go wraps the array in quotes and `JSON.parse`
  returns a string. `jsonify` escapes `<` first, so a caption still cannot
  close the tag.
- **Generator include patterns are unanchored regexes.** `serverless-finance`
  also matched the empty `serverless-finances` repo. Anchor any new name that
  is a prefix of another repo's name, and list deliberately removed posts under
  `exclude`, or `make generate-posts` will quietly publish them again.

## Page conventions

Data-driven pages keep their content in `data/` so adding an entry never means
touching a template:

| Page | Data | Layout |
| --- | --- | --- |
| `/music/` | `data/music.yaml` | `layouts/_default/music.html` |
| `/subscriptions/` | `data/subscriptions.yaml`, `data/twitch.yaml` | `layouts/_default/subscriptions.html` |
| `/media/` | `data/media.yaml`, `data/photos.yaml` (both generated) | `layouts/_default/media.html` |
| `/movies/` | `data/movies.json` (`make movies-refresh`) | `layouts/_default/movies.html` |
| `/learn/` | `data/learn.json` (`make check-learn-links`) | `layouts/_default/learn.html` |
| `/courses/` | `data/courses.json` (`make courses-sync`) | `layouts/courses/` |
| `/ai/` | `data/ai.json` (daily Action, `make ai-refresh`) | `layouts/_default/ai.html` |
| `/` (home) | `data/home.yaml` | `layouts/index.html` |
| `/github/` | `data/github.json` (`make github-refresh`) | `layouts/_default/github.html` |

- **Every data-driven page is drawn in the browser from `/data/<name>.json`.**
  `partials/publish-data.html` publishes each `data/` file there (media gets
  the whitelisted payload from `partials/media-payload.html`, never the raw
  YAML — add a field there deliberately or it does not ship). The layouts
  supply only the shell and translated strings, passed to the script with
  their placeholders intact (`i18n "x" "{n}"`) and filled by
  `DataPage.fill` from `partials/data-render.html`. Keyed editorial strings
  (`cat_label_*`, `pl_note_*`, …) are still i18n, looked up per key in the
  layout. With JavaScript off these pages show a `<noscript>` link to their
  JSON instead of content — that was B's call.
- **/movies/:** append `{"title", "year"}` (or `"imdb"`) to
  `data/movies.json` and run `make movies-refresh`; check the new title in its
  output, since a year match can pick a same-year namesake. Synopses, titles
  and genres come back in all nine languages from JustWatch, so they are
  data, not i18n. Set `"mpa"` on an entry to override a wrong rating.
- **/courses/:** generated from the learn project (`~/projects/learn`) by
  `make courses-sync`. Only `lessons/` and `reference/` are published —
  MISSION, NOTES and learning records describe B and never leave that repo.
  Every page is redacted (`tools/courses/config.json`) and then checked
  against a deny list; a hit stops the sync. Course pages are English only
  (like posts); the `/courses/` index is translated. Don't hand-edit
  `static/courses/`, `content/courses/<slug>/` or `data/courses.json`.
- **/learn/:** add `{"key", "name", "by", "url"}` to a path in
  `data/learn.json`, its blurb as `learn_res_<key>` in all nine i18n files,
  then `make check-learn-links` — only list what opens without signing in.
  `page` instead of `url` links one of this site's projects in the visitor's
  language. Learn took Archive's nav slot; Archive is still a home card.
- **/ai/ refreshes itself.** `.github/workflows/ai-radar.yml` runs
  `tools/ai-radar/radar.py` every morning, commits `data/ai.json` and
  dispatches the deploy (a `GITHUB_TOKEN` push does not trigger it). Sources
  are `tools/ai-radar/config.json`; the file's shape is
  `tools/ai-radar/schema.json`, versioned, with migrations — see
  `tools/ai-radar/README.md` before changing a field. Its UI strings live in
  `tools/ai-radar/i18n_strings.py` (`make ai-i18n` writes them into the nine
  toml files between markers), so after a merge conflict in `i18n/`, re-run
  that rather than hand-merging the block.
- **Ten nav links** (GitHub was the tenth). `.nav-row` is now `60rem` and the
  full row appears from 980px, because Spanish needs ~950px with a legible
  language label. An eleventh link means re-measuring every language.

- **/github/:** `make github-refresh` re-fetches every *public* repo (via
  `gh`, README excerpts included) and classifies it. Areas and learning
  paths are token rules in `tools/github-repos/config.json` — area order and
  glyphs mirror `partials/icons/topic-id.html`; a path's `exclude` keeps
  look-alikes out (OpenSearch *Serverless* is not a Lambda lesson). Names are
  i18n `gh_area_<key>` / `gh_track_<key>_title|_blurb`. Article links come
  from the posts' `repoFullName` at build time, not from the JSON.
  `check_page.py --public public` is the render check.
- **Only publish what a stranger can actually open.** Private YouTube playlists
  403 and some public ones refuse to embed, so every embed was verified against
  `youtube.com/embed/videoseries?list=<id>` (or the IFrame Player API) before
  being listed. Do the same for anything new, and say in the copy when something
  is a link rather than a player and why.
- **Embeds are click-to-load.** Nothing is fetched from a third party until the
  visitor presses play, and only one plays at a time.
- A YouTube channel's latest video comes from its uploads playlist: `UU` +
  the channel id minus its leading `UC`.
- Avatars are downscaled and copied into `static/`, never hotlinked.

## Shared UI pieces

- **Icons** — `layouts/partials/icons/`. `chip.html` renders a tinted square;
  glyphs live in two `<symbol>` sprites referenced with `<use>` so a long list
  costs one copy each. `sprite-topics.html` ships everywhere;
  `sprite-projects.html` only on the projects list (see `baseof.html`). Post
  rows pick a glyph from their tags via `topic-id.html`, falling back to the
  language category. Chips are decorative and `aria-hidden`.
- **Tabs** — `layouts/partials/tabs-script.html` drives any page with `.ptab`
  buttons (`data-panel="x"`) and matching `#panel-x` elements. Panels render
  **visible** and are only hidden by that script; their contents are filled
  from JSON by the page's own script. It fires `tabhide` on a panel before hiding it; pages listen
  for that to tear down playing embeds, because a hidden iframe keeps playing
  audio. Emit the partial *after* the page's own script so listeners exist first.
- **Back to top** — `layouts/partials/back-to-top.html`, included once in
  `baseof.html`, so every page gets the same floating arrow (bottom right,
  after 400px of scroll). Don't add a per-page one. It sits at `z-index: 50`,
  under the lightbox/zoom overlays (100).
