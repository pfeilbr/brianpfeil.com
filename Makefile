dev: ## Hugo dev server with live reload
	hugo server --watch --disableFastRender --forceSyncStatic --buildDrafts

build: ## Production build (hugo --minify)
	hugo --minify

verify: test-tools test-media test-layout test-link-check test-learn-links test-courses test-indexnow test-site-check test-i18n test-docs test-github test-ai test-ai-page ## Every test suite, then a production build and the i18n fallback check
	hugo --minify --printI18nWarnings --printPathWarnings
	python3 tools/i18n-check/check_i18n.py --public public
	python3 tools/site-check/check_site.py --public public
	python3 tools/github-repos/check_page.py --public public

generate-posts: ## Regenerate generated-*.md posts from GitHub
	cd tools/generate-posts && go run . -user=pfeilbr -dest=../../content/post -debug

test-tools: ## Go tests for the post generator
	cd tools/generate-posts && go test ./...

# --- Instagram media page (/media/) ---------------------------------------
# Source: the instagram-archive project (~/projects/instagram/archive, set in
# tools/instagram-media/config.yaml) by default; EXPORT=… uses an Instagram
# "Download your information" zip instead.
#   make media-deps
#   make media-stage EXPORT=~/Downloads/instagram-export.zip
#   open tools/instagram-media/build/review.html   # tick what should be public
#   make media-publish EXPORT=~/Downloads/instagram-export.zip

EXPORT ?=
SOURCE = $(if $(EXPORT),--export $(EXPORT),)

media-deps: ## Create the media tool's venv
	cd tools/instagram-media && python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt

media-stage: ## Read the archive (or EXPORT=…), update the approve list, build the review sheet
	cd tools/instagram-media && .venv/bin/python pull.py stage $(SOURCE)

media-publish: ## Encode and upload approved items, write data/media.yaml
	cd tools/instagram-media && .venv/bin/python pull.py publish $(SOURCE)

# publish, then commit and push data/media.yaml and the manifest — only those.
media-release: ## media-publish, then commit and push only the media files
	cd tools/instagram-media && .venv/bin/python pull.py release $(SOURCE)

# Every file the page references exists on the CDN; exits 1 if any are missing.
media-sync: ## Archive to live: stage, approve every item, release (repeatable; no-op when nothing is new)
	cd tools/instagram-media && .venv/bin/python pull.py sync $(SOURCE)

media-audit: ## Check every file the page references exists on the CDN
	cd tools/instagram-media && .venv/bin/python pull.py audit

media-status: ## What is approved and what is live
	cd tools/instagram-media && .venv/bin/python pull.py status

# A launchd agent that stages an Instagram export as soon as it lands in
# ~/Downloads. It only stages; approving and publishing stay manual.
media-watch-install: ## Install the launchd agent that stages exports from ~/Downloads
	tools/instagram-media/.venv/bin/python tools/instagram-media/watch_downloads.py --install

media-watch-uninstall: ## Remove the Downloads watcher
	tools/instagram-media/.venv/bin/python tools/instagram-media/watch_downloads.py --uninstall

media-watch-status: ## Is the watcher loaded, and its last runs
	tools/instagram-media/.venv/bin/python tools/instagram-media/watch_downloads.py --status

# The Google Photos picker: a local web app that suggests photos and videos
# of B alone (screened on-device with Apple Vision) for the category
# sections of /media/, and publishes the picks. See tools/instagram-media/README.md.
media-picker: ## Google Photos picker on http://127.0.0.1:8790 (suggest, pick, publish)
	cd tools/instagram-media && .venv/bin/python pull.py picker

test-media: ## Python tests for the media tool
	cd tools/instagram-media && .venv/bin/python -m unittest discover -s tests

test-layout: ## Build /media/ from a fixture; check /data/media.json and the page in all nine languages
	python3 tools/instagram-media/tests/check_layout.py --build

test-link-check: ## Tests for the repo-link checker
	python3 -m unittest discover -s tools/link-check -p 'test_*.py'

test-learn-links: ## Tests for the /learn/ link checker, and its offline check of data/learn.json
	python3 -m unittest discover -s tools/learn-links -p 'test_*.py'
	python3 tools/learn-links/check_learn_links.py --offline

test-courses: ## Tests for the course sync, and a privacy check of every published lesson
	python3 -m unittest discover -s tools/courses -p 'test_*.py'

test-indexnow: ## Tests for the IndexNow change detector
	python3 -m unittest discover -s tools/indexnow -p 'test_*.py'

test-site-check: ## Tests for the built-site link and taxonomy checker
	python3 -m unittest discover -s tools/site-check -p 'test_*.py'

# Live and network-bound, so not part of verify: lists posts whose repo
# link 404s for a visitor (the repo went private or was deleted).
test-docs: ## Every Makefile target has help text and is in the README
	python3 -m unittest discover -s tools/docs-check -p 'test_*.py'
	python3 tools/docs-check/check_docs.py

test-i18n: ## Tests for, and a run of, the i18n consistency check
	python3 -m unittest discover -s tools/i18n-check -p 'test_*.py'
	python3 tools/i18n-check/check_i18n.py

# Add a movie to data/movies.json as {"title": …, "year": …} (or "imdb": "tt…"), then run this.
movies-refresh: ## Fill in and refresh data/movies.json (posters, scores, trailers, streaming)
	python3 tools/movies/refresh.py

# Every public repo of pfeilbr, classified into areas and learning paths
# (tools/github-repos/config.json). Needs `gh auth login`.
github-refresh: ## Refresh data/github.json from GitHub (repos, READMEs, areas, learning paths)
	python3 tools/github-repos/refresh.py

test-github: ## Tests for the GitHub page's data refresher and its search
	python3 -m unittest discover -s tools/github-repos -p 'test_*.py'
	node --test tools/github-repos/search.test.mjs

# /ai/: the daily AI radar. The GitHub Action ai-radar.yml runs ai-refresh
# every morning and deploys; run it by hand to see today's sources locally.
ai-refresh: ## Fetch every /ai/ source and rewrite data/ai.json (merges, keeps yesterday's on failure)
	python3 tools/ai-radar/radar.py

ai-i18n: ## Write the /ai/ UI strings (tools/ai-radar/i18n_strings.py) into all nine i18n files
	python3 tools/ai-radar/i18n_strings.py

test-ai: ## Unit tests for the AI radar, and a check that its i18n block is current
	python3 -m unittest discover -s tools/ai-radar/tests
	python3 tools/ai-radar/i18n_strings.py --check

test-ai-page: ## Build /ai/ from a fixture and with no data; check page, briefing, feed and home card in all nine languages
	python3 tools/ai-radar/check_page.py --build

ai-digest: ## Write today's AI briefing with Claude (needs ANTHROPIC_API_KEY and the tool's venv)
	cd tools/ai-radar && ([ -d .venv ] || (python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt)) && .venv/bin/python digest.py

check-repo-links: ## List posts whose repo link 404s for a visitor (live, needs network)
	python3 tools/link-check/check_repo_links.py

check-learn-links: ## Open every /learn/ link as an anonymous visitor (live, needs network)
	python3 tools/learn-links/check_learn_links.py

# Pull lessons from the learn project into /courses/ (redacted, privacy-gated).
courses-sync: ## Publish the /teach courses from ~/projects/learn to /courses/
	python3 tools/courses/sync_courses.py

check-course-links: ## Open every course resource link as an anonymous visitor (live, needs network)
	python3 tools/courses/check_course_links.py

# Quantizes PNGs over 300 KB when it's clearly smaller and visually close.
images-optimize: ## Shrink heavy PNGs in content/ and static/ in place (needs ImageMagick)
	python3 tools/images/optimize_pngs.py --apply


# --- Terraform (infra/) ---------------------------------------------------
# State lives in S3 (infra/backend.hcl). The provider comes from a local
# mirror because the registry download is unreliable here; populate it with
# `python3 infra/scripts/fetch_provider.py --detach` if it is missing.
TF_MIRROR := $(HOME)/.terraform.d/plugin-mirror
TF_INIT = terraform init -input=false -backend-config=$(1) -plugin-dir=$(TF_MIRROR)

tf-init: ## Terraform init, both stacks, S3 backend + local provider mirror
	cd infra && $(call TF_INIT,backend.hcl)
	cd infra/bootstrap && $(call TF_INIT,../backend.hcl)

tf-plan: ## Terraform plan, both stacks
	cd infra && terraform plan -input=false
	cd infra/bootstrap && terraform plan -input=false

tf-validate: ## terraform fmt -check and validate
	cd infra && terraform fmt -check -recursive && terraform validate


help: ## List every target
	@awk 'BEGIN {FS = ":.*## "} /^[a-z0-9-]+:.*## / {printf "  \033[1m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: help dev build verify generate-posts movies-refresh ai-refresh ai-i18n ai-digest test-ai test-ai-page github-refresh test-github test-tools media-deps media-stage media-publish media-release media-sync media-audit media-status media-watch-install media-watch-uninstall media-watch-status test-media test-layout test-link-check test-learn-links test-courses test-indexnow test-site-check test-i18n test-docs check-repo-links check-learn-links courses-sync check-course-links images-optimize tf-init tf-plan tf-validate
