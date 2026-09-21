dev: ## Hugo dev server with live reload
	hugo server --watch --disableFastRender --forceSyncStatic --buildDrafts

build: ## Production build (hugo --minify)
	hugo --minify

verify: test-tools test-media test-layout test-link-check test-i18n test-docs ## Every test suite, then a production build and the i18n fallback check
	hugo --minify --printI18nWarnings --printPathWarnings
	python3 tools/i18n-check/check_i18n.py --public public

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

test-media: ## Python tests for the media tool
	cd tools/instagram-media && .venv/bin/python -m unittest discover -s tests

test-layout: ## Render /media/ from a fixture and check it in all nine languages
	python3 tools/instagram-media/tests/check_layout.py --build

test-link-check: ## Tests for the repo-link checker
	python3 -m unittest discover -s tools/link-check -p 'test_*.py'

# Live and network-bound, so not part of verify: lists posts whose repo
# link 404s for a visitor (the repo went private or was deleted).
test-docs: ## Every Makefile target has help text and is in the README
	python3 -m unittest discover -s tools/docs-check -p 'test_*.py'
	python3 tools/docs-check/check_docs.py

test-i18n: ## Tests for, and a run of, the i18n consistency check
	python3 -m unittest discover -s tools/i18n-check -p 'test_*.py'
	python3 tools/i18n-check/check_i18n.py

check-repo-links: ## List posts whose repo link 404s for a visitor (live, needs network)
	python3 tools/link-check/check_repo_links.py


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

.PHONY: help dev build verify generate-posts test-tools media-deps media-stage media-publish media-release media-sync media-audit media-status media-watch-install media-watch-uninstall media-watch-status test-media test-layout test-link-check test-i18n test-docs check-repo-links tf-init tf-plan tf-validate
