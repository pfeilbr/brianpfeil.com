# brianpfeil.com

Hugo site. `content/post/*.md` are blog/project posts; `content/projects/` are project bundles.

## Where /media/ stands (read this first)

The page, the pull tool and the AWS hosting are all built, live and pushed.
`/media/` renders an empty state in all nine languages.

**It is empty because no Instagram export exists on this machine** — the
pipeline has no input, not a half-finished one. Requesting the export needs an
Instagram login, so it is the one step B has to do:
[accountscenter.instagram.com/info_and_permissions/dyi](https://accountscenter.instagram.com/info_and_permissions/dyi/)
→ Posts + Reels → **Format: JSON**, All time, High quality. Instagram emails a
link; a large account comes back as several part ZIPs.

With the archive on disk:

```sh
make media-deps                                          # one-time venv
make media-stage EXPORT=~/Downloads/instagram-export.zip
open tools/instagram-media/build/review.html             # tick what goes public
python3 tools/instagram-media/pull.py approve --id ...   # the sheet prints this
make media-publish EXPORT=~/Downloads/instagram-export.zip
git add data/media.yaml tools/instagram-media/manifest.yaml && git commit && git push
```

Nothing publishes without an explicit approval — see
`tools/instagram-media/README.md`.

**Terraform in `infra/` is written but NOT applied.** It describes the bucket
and CloudFront distribution that already exist (created with the CLI before
the Terraform-only rule was in play), with `import` blocks so applying adopts
them rather than rebuilding. `terraform init` needs a 174 MB provider that
downloads at ~50 KB/s, so run `python3 infra/scripts/fetch_provider.py
--detach` and check `infra/.provider-cache/fetch.log`. A correct plan is
**6 to import, 0 to add, 0 to change, 0 to destroy** — anything proposing a
change or destroy means stop, those resources serve the live media page.

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
