# brianpfeil.com

Hugo site. `content/post/*.md` are blog/project posts; `content/projects/` are project bundles.

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

**Stories are pending the Instagram export.** The archive knows about 153
archived stories only as an inventory (`harvest/iphone/story-inventory.jsonl`),
not their files. The export requested 2026-09-21 (Media, all time, JSON,
medium) carries them. When it lands in `~/Downloads`, the watcher runs
`pull.py sync --export …`: posts and reels still from the archive, stories
from the export, reshares dropped (2 of someone else's posts, 9 of B's own
reels — `igmedia/stories.py`), silent stories given music, pushed live.
Download it within four days of Meta's email; it needs B's password.

`aws sso login` first if the session has expired — `publish` checks before encoding.

`make verify` runs every test suite (Go post generator, Python media tool,
link checker), a render check that builds `/media/` from a fixture and with
no data and asserts on the HTML in all nine languages, and a
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
  `max-width: 52rem`: widening the browser adds nothing, and a seventh link
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
| `/media/` | `data/media.yaml` (generated) | `layouts/_default/media.html` |

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
  **visible** and are only hidden by that script, so the page still works with
  JavaScript off. It fires `tabhide` on a panel before hiding it; pages listen
  for that to tear down playing embeds, because a hidden iframe keeps playing
  audio. Emit the partial *after* the page's own script so listeners exist first.
