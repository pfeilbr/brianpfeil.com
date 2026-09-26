# brianpfeil.com

Personal site built with [Hugo](https://gohugo.io/), in nine languages:
English at the root, and `zh es pt fr de it ja ko` under `/<code>/`. Posts are
English-only; pages, layouts and UI strings are translated.

For working on it with an AI agent, `CLAUDE.md` holds the conventions and the
gotchas that have bitten before, and opens with where current work stands.

## Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) **0.166.0** — the version
  CI is pinned to. A different local version can build fine and still fail to
  deploy.
- [Go](https://go.dev/) 1.25+ — only for generating posts from GitHub repos
- Python 3.11+ and [ffmpeg](https://ffmpeg.org/) — only for the media page
- [Terraform](https://www.terraform.io/) 1.10+ and the AWS CLI — only for
  `infra/`

## Quick start

    make dev       # dev server at http://localhost:1313
    make verify    # every test suite, then a checked production build

## Project structure

    .
    ├── content/
    │   ├── post/              # posts (manual + generated-*.md)
    │   ├── projects/          # project bundles
    │   └── *.md, *.<lang>.md  # standalone pages, one file per language
    ├── data/                  # structure behind data-driven pages (music, media, …)
    ├── i18n/                  # UI strings — every key in all nine files
    ├── layouts/               # all templates in-repo, no theme
    ├── assets/
    │   ├── css/main.css       # hand-written utility CSS (not Tailwind)
    │   └── js/search.js       # client-side search
    ├── static/                # images and other files served as-is
    ├── tools/
    │   ├── generate-posts/    # Go: posts from GitHub repo READMEs
    │   ├── instagram-media/   # Python: /media/ from an Instagram export
    │   ├── i18n-check/        # Python: the nine languages agree; no English fallback
    │   └── link-check/        # Python: posts whose repo link a visitor can't open
    ├── infra/                 # Terraform for the AWS side (see infra/README.md)
    ├── config.yaml            # Hugo config, including per-language menus
    └── Makefile

## Writing a new post

### Manual post

    hugo new post/my-new-post-title/index.md

Edit the file, then run `make dev` to preview.

### Generated posts (from GitHub repos)

`tools/generate-posts/` creates posts from GitHub repository READMEs (for
example `*-playground` repos).

The quickest way to run it uses the GitHub CLI's token, with nothing on disk:

    cd tools/generate-posts
    GITHUB_TOKEN=$(gh auth token) go run . -user=pfeilbr -dest=../../content/post

Or put a token in `tools/generate-posts/config.local.yaml` (gitignored) as
`github_access_token: "..."` and run `make generate-posts`.

**Configuration** is in `tools/generate-posts/config.yaml`:
- `repo_filters.include/exclude` — regexes selecting repos. They are
  **unanchored**: anchor a name that is a prefix of another repo's, and list
  deliberately removed posts under `exclude` so they aren't regenerated.
- `date_overrides` — date a post by last activity rather than repo creation
- `title_mappings` — override generated titles
- `casing_corrections` — words needing specific casing ("AWS", "CDK")
- `tags.*` — auto-tagging, per-repo tags, tag normalisation

## The media page (`/media/`)

Photos and video from Instagram, built from the instagram-archive project
(`~/projects/instagram/archive`) or an official Instagram data export — no
scraping, no stored credentials. Files are re-encoded with all metadata
(including GPS) stripped, and served from a private S3 bucket behind
CloudFront; only `data/media.yaml` lives in the repo. **Nothing is published
until it is approved by hand.**

    make media-deps       # once
    make media-sync       # archive -> live: stage, approve all, encode, upload, commit, push

Or selectively: `make media-stage`, tick items in
`tools/instagram-media/build/review.html`, then `make media-release`.

See [`tools/instagram-media/README.md`](tools/instagram-media/README.md).

## Makefile targets

| Target | Does |
| --- | --- |
| **Site** | |
| `make dev` | Hugo dev server with live reload |
| `make build` | Production build (`hugo --minify`) |
| `make help` | List every target with a one-line description |
| `make verify` | Every `test-*` target below, then a production build and the i18n fallback check on it (not the live link check or Terraform) |
| **Posts** | |
| `make generate-posts` | Regenerate `generated-*.md` from GitHub |
| `make check-repo-links` | List posts whose repo link 404s for a visitor (live, needs network) |
| `make check-learn-links` | Open every /learn/ link as an anonymous visitor (live, needs network) |
| `make courses-sync` | Publish the /teach courses from ~/projects/learn to /courses/ |
| **Movies** | |
| `make movies-refresh` | Fill in and refresh `data/movies.json`: posters, scores, trailers, US streaming, nine languages |
| **GitHub** | |
| `make github-refresh` | Refresh `data/github.json`: every public repo, README excerpts, areas and learning paths for `/github/` |
| **AI radar** | |
| `make ai-refresh` | Fetch every `/ai/` source and rewrite `data/ai.json` (the daily Action does this) |
| `make ai-i18n` | Write the `/ai/` UI strings into all nine i18n files |
| **Media** | |
| `make media-deps` | Create the tool's venv |
| `make media-stage` | Read the archive (or `EXPORT=…`), update the approve list, build the review sheet |
| `make media-publish` | Encode and upload approved items, write `data/media.yaml` |
| `make media-release` | `media-publish`, then commit and push only the media files |
| `make media-sync` | Archive to live in one step: stage, approve every item, release (no-op when nothing is new) |
| `make media-status` | What is approved and what is live |
| `make media-picker` | Google Photos picker on http://127.0.0.1:8790: suggests photos and video of B alone by activity, publishes the picks |
| `make media-audit` | Every file the page references exists on the CDN (exits 1 if not) |
| `make media-watch-install` | Install the launchd agent that stages exports from `~/Downloads` |
| `make media-watch-uninstall` | Remove the Downloads watcher |
| `make media-watch-status` | Whether the watcher is loaded, and its last runs |
| **Tests** | |
| `make test-tools` | Go tests for the post generator |
| `make test-media` | Python tests for the media tool |
| `make test-layout` | Build `/media/` from a fixture; check `/data/media.json` and the page in all nine languages |
| `make test-link-check` | Tests for the repo-link checker |
| `make test-github` | Tests for the GitHub page's data refresher |
| `make test-learn-links` | Tests for the /learn/ link checker, and its offline check of data/learn.json |
| `make test-courses` | Tests for the course sync, and a privacy check of every published lesson |
| `make test-i18n` | Tests for, and a run of, the i18n consistency check |
| `make test-docs` | Every Makefile target has help text and is in the README |
| `make test-ai` | Unit tests for the AI radar, and its i18n block is current |
| **Infrastructure** | |
| `make tf-init` / `tf-plan` / `tf-validate` | Terraform, both stacks, S3 backend |

## CI and deployment

Two workflows run on every push to `main`:

- **Tests** — Go and Python test suites, the `/media/` render check, the i18n
  consistency and fallback check, a Hugo build with warnings surfaced, and
  `terraform fmt` + `validate` on both stacks. Runs on pull requests too.
- **Deploy to GitHub Pages** — `hugo --minify`, then publish.

Generated posts and `data/media.yaml` are produced locally and committed. CI
runs neither the post generator nor the media tool, so it needs no GitHub
token, no Instagram data and no AWS credentials.

AWS resources (the media bucket, its CDN and the Terraform state bucket) are
all Terraform-managed — see [`infra/README.md`](infra/README.md).
