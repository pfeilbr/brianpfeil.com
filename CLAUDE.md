# brianpfeil.com

Hugo site. `content/post/*.md` are posts; `content/projects/` are project bundles.

**Posts are two kinds (2026-10-11).** Hand-written *articles* (24) are listed
at `/post/`; the generated `generated-*.md` posts, one per playground repo's
README, are *lab notes* (~290), listed at `/notes/`. A cascade in
`content/post/_index.md` gives every `generated-*` file `kind = "note"`;
`partials/site-articles.html` / `site-notes.html` are the two lists (use
them, not `site-posts.html`, for anything a visitor browses). Both pages
share `partials/post-list-page.html` (switch, search, infinite scroll, a
one-line summary per row from `partials/post-summary.html`). Note URLs stay
`/post/<slug>/`; each note opens with a "Lab note" line naming its repo.
Search covers both and takes `?q=` (the 404 page searches the words of the
missing URL). Posts 3+ years old open with an age notice; previous/next
stay within one kind. Feeds: `/index.xml` is articles + projects + guides,
`/post/index.xml` articles, `/notes/index.xml` lab notes. Lab notes carry no laptop-specific setup and none of B's own names:
`tools/generate-posts/local_setup.toml` (his AWS profiles, SSO logins,
`/Users/pfeilbr` paths, `cd ~/projects`, "where I installed X" lines, his
account number as AWS's example 123456789012, his S3 buckets as
`amzn-s3-demo-*`, his Azure resources as Microsoft's `contoso`/`my*`
names) is applied by the generator to every README and by
`make github-refresh` to the /github/ excerpts; `make notes-strip`
re-applies it to the notes in place. Its `[[redact]]` rules rewrite
secret-shaped strings (AWS key ids, JWTs, stream keys, tokens) to AWS's
example values or a marker. The structure check fails if any account,
`[replace]` key or unredacted secret reaches the built site; it names the
kind of secret, never the value. A new personal name
goes in that file, never in a hand edit of a note.

**A finished project has one page: `/projects/<x>/`.** Repos in the
generator's `project_repos` get `[build] list/render = "never"` in their
generated post, so the README is shown folded ("Under the hood") on the
project page (matched by the bundle's `repo` param) and the old
`/post/<slug>/` is an `aliases` redirect on the project's English
`index.md`. A new project = bundle with `repo` + alias, and the repo in
`project_repos`. GitHub and /apps/ link the project page, not the README.

**The home page is a pitch, then a table of contents.** `/` is a hero
(positioning line, three calls to action: guides, courses, articles; four
professional profiles, `hero: true` in `data/home.yaml` — /about/ and the
footer keep all of them), then wide cards for Architecture guides, Courses,
Articles and Learn, plain cards listed in `data/home.yaml` (projects, apps,
lab notes, AI, GitHub, résumé; titles/blurbs `hub_<key>_title` /
`hub_<key>_blurb`), and one "Off the clock" card for media, movies, music
and subscriptions (its title links `/off-the-clock/`, which is also in the nav). Archive and Tags are footer-only. The footer's site map
(`partials/footer.html`) links every section not in the nav.
`tools/site-check/check_structure.py` (verify and CI) holds all of this in
place in every language.

## Where /media/ stands (read this first)

**Live, with all 143 feed items** (2011–2026; 2,972 Instagram files on the
CDN) — last released as `2b8734e` on 2026-10-16. First release `bf44087`
on 2026-09-21.

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
composed by `igmedia/music.py` (royalty-free because they are generated
here, never downloaded). Every clip has its own song, recorded in the
shared music ledger. "Silent" includes an audio track that
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
documents. **Live since 2026-09-26: 42 items** (skiing 8, mountain biking 4,
kayaking 6, beach 13, hiking 11; swimming has no picks yet, so no section).
`make media-photos-publish` publishes from the command line; `DATA_ONLY=1`
when AWS is signed out. `make media-audit` checks both halves. The browser does all fetching from Google (a bookmarklet), since
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

**Every video's poster is a real frame.** `derive.py` takes the first frame
that isn't near-black (mean grey under 16), because clips that fade in from
black gave nine reels an all-black tile; `make media-posters` repaired those
on the CDN in place (same file names, invalidated) and is a no-op now. It
reads the derive lock from the main checkout's
`tools/instagram-media/derivatives.lock.json` (not in git), so run it there.

**Posts whose repo went private keep their text, minus the link**
(decided 2026-10-11; 16 repos, 10 of them published notes).
`data/repo_gone.json` lists them and `single.html` renders those notes
without a repo link. `make check-repo-links` exits 1 only for a broken repo
not yet in that file; `python3 tools/link-check/check_repo_links.py --write`
records the current set (and drops any that are public again). The Monday
`.github/workflows/repo-links.yml` keeps the issue "Lab notes: repo links"
open while a newly private repo is unrecorded, and closes it after.

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
- **When a post's title changes, change its slug to match** (and rename the
  bundle directory), and add the old URL to `aliases` so existing links
  still land. B asked for this every time, without being asked again.
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
  `max-width: 60rem`: widening the browser adds nothing. `.lang-label`
  truncates so flexbox can shrink instead of overlapping — check a
  long-worded language (es, fr) before adding another nav item.
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
| `/music/` | `data/music.yaml` (`make music-refresh`) | `layouts/_default/music.html` |
| `/subscriptions/` | `data/subscriptions.yaml`, `data/twitch.yaml` | `layouts/_default/subscriptions.html` |
| `/media/` | `data/media.yaml`, `data/photos.yaml` (both generated) | `layouts/_default/media.html` |
| `/movies/` | `data/movies.json` (`make movies-refresh`) | `layouts/_default/movies.html` |
| `/learn/` | `data/learn.json` (`make check-learn-links`) | `layouts/_default/learn.html` |
| `/courses/` | `data/courses.json` (`make courses-sync`) | `layouts/courses/` |
| `/ai/` | `data/ai.json` (daily Action, `make ai-refresh`) | `layouts/_default/ai.html` |
| `/` (home) | `data/home.yaml` | `layouts/index.html` |
| `/github/` | `data/github.json` (`make github-refresh`) | `layouts/_default/github.html` |
| `/apps/` | `data/apps.json` (hand-edited) | `layouts/_default/apps.html` |

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
- **/apps/:** B's own apps, each with a short link `/apps/<key>/` (all
  lowercase) that redirects to it — `partials/apps-links.html` publishes those
  from the English home page, carrying `?query` and `#hash` along. To add one:
  `{"key", "name", "url", "icon"}` (+ `repo` if public, `offline`,
  `sign_in`) in `data/apps.json`, `apps_blurb_<key>` in all nine i18n files,
  then `make apps-icon KEY=… FROM=<its icon png>` (or `EMOJI=…`). The home
  card counts them; `tools/apps/check_page.py` (in verify and CI) checks the
  data, the page in every language and every redirect.
- **/movies/:** append `{"title", "year"}` (or `"imdb"`) to
  `data/movies.json` and run `make movies-refresh`; check the new title in its
  output, since a year match can pick a same-year namesake. Synopses, titles
  and genres come back in all nine languages from JustWatch, so they are
  data, not i18n. Set `"mpa"` on an entry to override a wrong rating.
  To add many at once by IMDb id: `python3 tools/movies/add.py tt… …`
  (appends, skips ones already listed, refreshes only the new ones).
  `tools/movies/candidates.py` turns raw mentions (title, source,
  evidence) into matched films not yet on the page, for a pick list.
  The page loads `/data/movies.<lang>.json` (those three maps cut to its
  language + English, ~40–60 KB gzipped instead of 207 KB); the full
  `movies.json` is still published for the raw link.
  `tools/movies/check_payload.py` (in verify) keeps the two in step.
  Scores, streaming offers and trailers refresh daily
  (`.github/workflows/data-refresh.yml`, with the Twitch follower counts):
  `refresh.py --budget 25` takes the stalest films first (each entry's
  `refreshed` date) and stops when JustWatch starts answering 429, which it
  does to GitHub's runners after about ten films. It refuses to commit if a
  tenth of the trailers, offers or scores vanish at once.
- **/architecture/:** hand-written guides in `content/architecture/*.md`,
  English only, ordered by `weight`; the section index is translated. They
  are generic by design — drawn from B's review practice with every company,
  system and person removed; keep it that way. `{{< callout "key"|"warn" >}}`
  and `{{< diagram >}}` (inline SVG using `--dg-*` colours) are the two
  shortcodes; `- [ ]` task lists render as a checklist. After editing a
  guide, run `make guides-pdf` to refresh its PDF (only changed guides are
  reprinted; the page links the PDF when it exists).
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
  Every path has its own page, `/learn/<key>/` (own title, description, share
  card), generated into `content/learn/<key>.<lang>.md` by `make learn-pages`;
  a new path or changed path string needs a re-run, and verify/CI fail while
  those files are stale. Old `/learn/#<key>` links redirect there.
  Every Monday `.github/workflows/learn-links.yml` opens each link; while any
  is broken, the issue "Learn: broken links" stays open (closes itself).
  `page` instead of `url` links one of this site's projects in the visitor's
  language. Archive is linked from the footer.
- **/ai/ refreshes itself.** `.github/workflows/ai-radar.yml` runs
  `tools/ai-radar/radar.py` twice a day, then `digest.py` (the daily Claude
  briefing, nine languages, a no-op without the `ANTHROPIC_API_KEY` secret),
  commits `data/ai.json` + `data/ai-digests.json` — never commit local
  copies of those — and
  dispatches the deploy (a `GITHUB_TOKEN` push does not trigger it). Sources
  are `tools/ai-radar/config.json`; the file's shape is
  `tools/ai-radar/schema.json`, versioned, with migrations — see
  `tools/ai-radar/README.md` before changing a field. Its UI strings live in
  `tools/ai-radar/i18n_strings.py` (`make ai-i18n` writes them into the nine
  toml files between markers), so after a merge conflict in `i18n/`, re-run
  that rather than hand-merging the block.
- **Seven nav links** since 2026-10-16 (guides, courses, learn, articles,
  projects, off the clock, about; it was ten, then six). "Off the clock" goes
  to `/off-the-clock/` (`layouts/_default/offclock.html`), a landing page for
  media, movies, music and subscriptions; it and the home card share
  `partials/offclock-items.html` and `offclock-strip.html`. Its nav label is
  short on purpose (es "tiempo libre", fr "loisirs", de "freizeit") and
  matches `hub_offclock_title`. The full row shows from 820px, measured in
  es, fr and de (narrowest clearance: es, 80px at 820). Every other section
  is in the footer's site map; keep it that way rather than growing the row
  again.

- **/github/:** `make github-refresh` re-fetches every *public* repo (via
  `gh`, README excerpts included) and classifies it. Areas and learning
  paths are token rules in `tools/github-repos/config.json` — area order and
  glyphs mirror `partials/icons/topic-id.html`; a path's `exclude` keeps
  look-alikes out (OpenSearch *Serverless* is not a Lambda lesson). Names are
  i18n `gh_area_<key>` / `gh_track_<key>_title|_blurb`. Article links come
  from the posts' `repoFullName` at build time, not from the JSON.
  `check_page.py --public public` is the render check. It refreshes itself
  every Monday (`.github/workflows/github-refresh.yml`); a run that changes
  nothing but the date writes nothing, and one that loses >10% of repos
  refuses to write (`--force` by hand if that is real). The query language
  lives in `assets/js/gh-search.js` (no DOM) and is tested with
  `node --test tools/github-repos/search.test.mjs`.
  Learners' ticked-off steps live in `localStorage` (`gh-learn-done`) only.
  On this page `.gh [hidden]` is forced to `display: none` -- a class that
  sets `display` otherwise beats the attribute (it kept "Show more" visible).
- **/music/ refreshes itself** every Thursday (`.github/workflows/music-refresh.yml`,
  `make music-refresh` by hand). Every public playlist on @pfeilbr is listed
  if its embed plays; the check fetches `embed/videoseries?list=<id>` with
  this site as the Referer and reads `previewPlayabilityStatus` — without a
  referer every embed answers error 153, and oEmbed passes rights-blocked
  tracks. Saved (other people's) playlists are ids in
  `tools/music/config.json`, since the library needs B's sign-in. Losing
  more than a quarter of the list in one run refuses to write (`--force`).
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

## SEO

- `partials/head-meta.html`: descriptions fall back to `i18n "site_description"`
  (translated), tag pages use `tag_desc`. Only `post`, `projects` and
  `architecture` pages are articles (`BlogPosting` / `TechArticle`); every
  other page is a `WebPage`. The home page carries a Person + WebSite
  `@graph`; articles point at the Person by `@id`. New section of articles →
  add it to `$isArticle`.
- The home RSS (`layouts/index.rss.xml`) lists posts, projects and guides only.
- `llms.txt` is a short linked index; `llms-full.txt` has the full text.
- Course lessons are static files, so `sync_courses.py` gives each a
  canonical link and meta description and writes `static/sitemap-courses.xml`,
  which `robots.txt` lists next to Hugo's sitemap.

- **IndexNow:** the deploy writes `/indexnow-manifest.json` (a hash of each
  page's title, description and `<main>`), diffs it against the live one, and
  after the deploy submits only the changed URLs (`tools/indexnow/`). The key
  file is `static/<key>.txt`; the key is public by design.

- **Site check** (`tools/site-check`, in verify and CI): every same-site
  link and image in the build must resolve, relative ones included (Hugo
  publishes a bundle's files once, under the English path, so
  `layouts/_default/single.html` points raw `src="images/…"` at each
  resource's real URL), and no tag/category may be used with two
  casings — with `disablePathToLower`, "HTML" and "html" race for one URL
  and the build output changes from run to run.
- **Contrast:** secondary text uses a colour token (`--text-subtle`), never
  `opacity` — the opacity versions measured 2–4:1 and failed WCAG AA.

- **Dead remote images** (`make images-rescue`): `data/image_rewrites.json`
  maps each dead image URL to a Wayback copy in `static/images/rescued/`, or
  to null (rendered as "image no longer available"). Applied at render
  time, so `make generate-posts` can't bring them back. Two of B's old S3
  website buckets (static-content-01, static-screenshots-01) were deleted;
  their names can be re-registered by anyone, so the site check fails on
  any page that loads or links to them (`DEAD_HOSTS` in the rescue tool).
- **Dead outbound links** (`data/link_rewrites.json`): `make check-post-links`
  finds links in posts, projects and guides whose page is gone;
  `python3 tools/link-check/rescue_links.py --results <post-links.json>
  --public <site> --apply` maps each to the Wayback Machine copy closest to
  the post's date (availability API, then the slower CDX index, which finds
  what the first misses), or to null when there is none.
  `partials/content-a11y.html` applies it at render time: the archived copy
  (titled `link_archived`), or the text kept with the link dropped
  (`.link-gone`, titled `link_gone`). Every run re-opens the mapped URLs
  first and drops any that answer again — the checker's parallel fetches
  report GitHub network errors as dead hosts.
- **Evernote screenshots are self-hosted** (`make images-selfhost`, then
  `make images-rescue`): the ~320 that still load are WebP copies in
  `static/images/remote/`, mapped in the same `image_rewrites.json`. A new
  post that embeds an Evernote image fails `make test-image-rescue` until
  it's run.

- **Story posts:** `story = true` plus `hero` / `hero_alt` / `hero_credit` /
  `hero_href` in a post's front matter turns it into a long-form feature
  (serif text, hero photo, progress bar; `assets/css/story.css`,
  `partials/story.html`). `{{< mood src="images/x.webp" alt credit href >}}`
  is a wide photo that fades in, `{{< standout >}}` sets one line large.
  Photos live in the bundle as WebP and are CC0/public domain with a credit
  line. Motion is off with reduced motion or no JS; everything stays visible.
- **Keep learning** (`partials/keep-learning.html`): posts show up to two
  guides and two courses whose tag lists in `data/keep_learning.yaml` match
  the post's tags. A new guide or course needs an entry there to be found.

## Newsletter

`partials/newsletter.html` sits on the home page, posts, guides, /courses/ and
/learn/. It renders nothing until `params.newsletter.buttondown` in
`config.yaml` names a Buttondown account; the form posts straight to
Buttondown (double opt-in, unsubscribe handled there). No script, no
third-party request until someone presses Subscribe.

**Issues** are Markdown files in `tools/newsletter/issues/` (front matter
`subject`, `url`); `tools/newsletter/sent.json` is the ledger of what has
gone out (Buttondown id + archive URL), so nothing is sent twice. Five went
out on 2026-10-11 (four guides + the courses), sent by hand in the
Buttondown editor from B's Chrome session, since there is no API key yet.
With `BUTTONDOWN_API_KEY` set, `make newsletter-send` sends new issues and
records them. In the editor, the first input after `/emails/new` loads is
dropped, and an empty subject is auto-filled from the body: paste the body,
then set the subject. Archive: https://buttondown.com/pfeilbr/archive/

## Social

Every page but home has a Hugo-drawn share card (`partials/og-image.html`).
`make social-kit` writes per-channel copy for every learn path, guide and
course; the "people I follow" path (Simon Willison, Lex Fridman, Andrew
Huberman, Addy Osmani, Mitchell Hashimoto, levelsio — B's priority, also
pinned in that order on /ai/) always goes first. The weekday
`social-post.yml` Action posts the next item to Bluesky and Mastodon and
commits `tools/social/posted.json` — never hand-commit a local copy of it.
X, LinkedIn, Threads and Facebook stay manual (from the kit).
The guides and the /learn/ paths (as list articles, slugs `learn-<key>`)
cross-post to dev.to as drafts, canonical to this site, via the
manual "dev.to cross-post" Action (`tools/social/devto.py`, ledger
`tools/social/devto.json`); a new Hugo shortcode in the guides must get a
conversion there, or the script refuses to convert.

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

## Waiting on B

Stubbed so nothing breaks until B fills them in; each renders nothing (or
changes nothing) while empty.

- **Search-engine verification:** Google is done (2026-10-12): property
  `https://brianpfeil.com/` in B's Search Console, verified by the Analytics
  tag, the domain provider and the `params.verification.google` meta tag;
  `sitemap.xml` and `sitemap-courses.xml` submitted. The domain property
  `sc-domain:brianpfeil.com` (every subdomain) is verified too, by the apex
  TXT record `aws_route53_record.apex_txt` in `infra/dns.tf` — add any
  future TXT value to that one record. Bing is waiting on B: sign in to Bing Webmaster Tools and
  "Import from Google Search Console" (an OAuth grant only B can give), or
  paste its `msvalidate.01` code into `params.verification.bing`.
- **Repo secrets for the automation** (each is a no-op until set):
  `ANTHROPIC_API_KEY` (the daily /ai/ briefing) and `BLUESKY_APP_PASSWORD`
  (the weekday Bluesky post; `BLUESKY_HANDLE` = pfeilbr.bsky.social is
  set). Mastodon stays off: no @pfeilbr account was found on the big
  instances. `gh secret set NAME --repo pfeilbr/brianpfeil.com` and paste.
- **16 private repos:** the lab notes show without their link
  (`data/repo_gone.json`). Making any of them public again brings the link
  back on the next `check_repo_links.py --write`.
