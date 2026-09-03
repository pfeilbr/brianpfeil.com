# brianpfeil.com

Hugo site. `content/post/*.md` are blog/project posts; `content/projects/` are project bundles.

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

## Page conventions

Data-driven pages keep their content in `data/` so adding an entry never means
touching a template:

| Page | Data | Layout |
| --- | --- | --- |
| `/music/` | `data/music.yaml` | `layouts/_default/music.html` |
| `/subscriptions/` | `data/subscriptions.yaml`, `data/twitch.yaml` | `layouts/_default/subscriptions.html` |

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
