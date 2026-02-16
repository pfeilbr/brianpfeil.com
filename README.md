# brianpfeil.com

Personal blog built with [Hugo](https://gohugo.io/).

## Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) (v0.128+)
- [Go](https://go.dev/) (v1.22+) — only needed for generating posts from GitHub repos

## Quick Start

    make dev             # Start local dev server at http://localhost:1313

## Project Structure

    .
    ├── content/
    │   ├── post/              # Blog posts (manual + generated)
    │   ├── projects/          # Project pages
    │   └── about.md           # About page
    ├── layouts/               # Hugo templates (no theme — all layouts in-repo)
    │   ├── _default/          # baseof, single, list, index.json
    │   ├── partials/          # nav, footer, search
    │   └── projects/          # Custom projects list layout
    ├── assets/
    │   ├── css/main.css       # CSS reset + utility classes + prose + syntax highlighting
    │   └── js/search.js       # Vanilla JS search
    ├── static/                # Images
    ├── tools/
    │   └── generate-posts/    # Go tool to generate posts from GitHub repos
    ├── config.yaml            # Hugo configuration
    └── Makefile

## Writing a New Post

### Manual post

    hugo new post/my-new-post-title/index.md

Edit the file, then run `make dev` to preview.

### Generated posts (from GitHub repos)

The tool at `tools/generate-posts/` automatically creates blog posts from your
GitHub repository READMEs (e.g., `*-playground` repos).

**One-time setup:**

1. Create a GitHub personal access token at https://github.com/settings/tokens
   (needs `repo` scope for private repos, or just `public_repo` for public only)
2. Create the local config file:

       cp tools/generate-posts/config.yaml tools/generate-posts/config.local.yaml

3. Add your token to `config.local.yaml`:

       github_access_token: "ghp_your_token_here"

   This file is gitignored and will not be committed.

**Running the generator:**

    make generate-posts

This fetches all matching repos, downloads their READMEs, and writes/updates
`generated-*.md` files in `content/post/`.

**Configuration** is in `tools/generate-posts/config.yaml`:
- `repo_filters.include/exclude` — regex patterns to select repos
- `title_mappings` — override auto-generated titles for specific repos
- `casing_corrections` — words that need specific casing (e.g., "AWS", "CDK")
- `tags.*` — auto-tagging rules, per-repo tag mappings, tag normalization

## Makefile Targets

| Target | Description |
|--------|-------------|
| `make dev` | Start Hugo dev server with live reload |
| `make build` | Build the site (`hugo --minify`) |
| `make verify` | Build + run verification checks |
| `make generate-posts` | Run the post generator tool |
| `make test-tools` | Run Go tests for the post generator |

## Deployment

The site deploys to GitHub Pages via GitHub Actions (`.github/workflows/gh-pages.yml`).
On push to `main`, the workflow:
1. Builds with `hugo --minify`
2. Deploys to GitHub Pages

Posts are generated locally and committed — the CI workflow does not run the Go tool.

