# brianpfeil.com

Personal blog built with [Hugo](https://gohugo.io/) and [Tailwind CSS](https://tailwindcss.com/).

## Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) (v0.128+)
- [Node.js](https://nodejs.org/) (v20+) — for Tailwind CSS
- [Go](https://go.dev/) (v1.22+) — only needed for generating posts from GitHub repos

## Quick Start

    npm install          # Install Tailwind/PostCSS dependencies
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
    │   ├── projects/          # Custom projects list layout
    │   └── shortcodes/
    ├── assets/
    │   ├── css/main.css       # Tailwind directives + prose styles
    │   ├── css/syntax.css     # Chroma syntax highlighting
    │   └── js/search.js       # Vanilla JS search
    ├── static/                # Images, CNAME, apps
    ├── tools/
    │   └── generate-posts/    # Go tool to generate posts from GitHub repos
    ├── scripts/verify.sh      # Build verification script
    ├── site                   # Helper script (run local, create post, generate posts)
    ├── config.yaml            # Hugo configuration
    ├── Makefile
    └── package.json           # Node.js dependencies (Tailwind, PostCSS)

## Writing a New Post

### Manual post

    ./site post -t "My New Post Title"

This creates `content/post/my-new-post-title/index.md` with Hugo front matter.
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

    # Via the site script:
    ./site generate-posts-from-repos

    # Or via Make:
    make generate-posts

    # Or directly:
    cd tools/generate-posts && go run . -user=pfeilbr -dest=../../content/post -debug

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
| `make install` | Install Node.js dependencies |
| `make verify` | Build + run verification checks |
| `make generate-posts` | Run the post generator tool |
| `make test-tools` | Run Go tests for the post generator |

## The `site` Script

    ./site run-local              # Start dev server + open browser
    ./site post -t "Title"        # Create a new manual post
    ./site generate-posts-from-repos  # Generate posts from GitHub repos

## Deployment

The site deploys to GitHub Pages via GitHub Actions (`.github/workflows/gh-pages.yml`).
On push to `master`, the workflow:
1. Installs Node.js dependencies
2. Builds with `hugo --minify`
3. Deploys to GitHub Pages

Posts are generated locally and committed — the CI workflow does not run the Go tool.

## Search

Client-side search powered by vanilla JS (`assets/js/search.js`). Hugo generates
a JSON search index at `/index.json`. No external search libraries.

## Dark Mode

Toggle via the sun/moon icon in the nav. Uses [DarkReader](https://darkreader.org/)
with localStorage persistence.
