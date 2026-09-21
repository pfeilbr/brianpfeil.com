dev:
	hugo server --watch --disableFastRender --forceSyncStatic --buildDrafts

build:
	hugo --minify

verify: test-tools test-media test-layout test-link-check test-i18n
	hugo --minify --printI18nWarnings --printPathWarnings
	python3 tools/i18n-check/check_i18n.py --public public

generate-posts:
	cd tools/generate-posts && go run . -user=pfeilbr -dest=../../content/post -debug

test-tools:
	cd tools/generate-posts && go test ./...

# --- Instagram media page (/media/) ---------------------------------------
# EXPORT points at the "Download your information" zip (or an unpacked copy).
#   make media-deps
#   make media-stage EXPORT=~/Downloads/instagram-export.zip
#   open tools/instagram-media/build/review.html   # tick what should be public
#   make media-publish EXPORT=~/Downloads/instagram-export.zip

EXPORT ?=

media-deps:
	cd tools/instagram-media && python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt

media-stage:
	@test -n "$(EXPORT)" || (echo "set EXPORT=/path/to/instagram-export.zip" && exit 1)
	cd tools/instagram-media && .venv/bin/python pull.py stage --export $(EXPORT)

media-publish:
	@test -n "$(EXPORT)" || (echo "set EXPORT=/path/to/instagram-export.zip" && exit 1)
	cd tools/instagram-media && .venv/bin/python pull.py publish --export $(EXPORT)

# publish, then commit and push data/media.yaml and the manifest — only those.
media-release:
	@test -n "$(EXPORT)" || (echo "set EXPORT=/path/to/instagram-export.zip" && exit 1)
	cd tools/instagram-media && .venv/bin/python pull.py release --export $(EXPORT)

media-status:
	cd tools/instagram-media && .venv/bin/python pull.py status

# A launchd agent that stages an Instagram export as soon as it lands in
# ~/Downloads. It only stages; approving and publishing stay manual.
media-watch-install:
	tools/instagram-media/.venv/bin/python tools/instagram-media/watch_downloads.py --install

media-watch-uninstall:
	tools/instagram-media/.venv/bin/python tools/instagram-media/watch_downloads.py --uninstall

media-watch-status:
	tools/instagram-media/.venv/bin/python tools/instagram-media/watch_downloads.py --status

test-media:
	cd tools/instagram-media && .venv/bin/python -m unittest discover -s tests

test-layout:
	python3 tools/instagram-media/tests/check_layout.py --build

test-link-check:
	python3 -m unittest discover -s tools/link-check -p 'test_*.py'

# Live and network-bound, so not part of verify: lists posts whose repo
# link 404s for a visitor (the repo went private or was deleted).
test-i18n:
	python3 -m unittest discover -s tools/i18n-check -p 'test_*.py'
	python3 tools/i18n-check/check_i18n.py

check-repo-links:
	python3 tools/link-check/check_repo_links.py


# --- Terraform (infra/) ---------------------------------------------------
# State lives in S3 (infra/backend.hcl). The provider comes from a local
# mirror because the registry download is unreliable here; populate it with
# `python3 infra/scripts/fetch_provider.py --detach` if it is missing.
TF_MIRROR := $(HOME)/.terraform.d/plugin-mirror
TF_INIT = terraform init -input=false -backend-config=$(1) -plugin-dir=$(TF_MIRROR)

tf-init:
	cd infra && $(call TF_INIT,backend.hcl)
	cd infra/bootstrap && $(call TF_INIT,../backend.hcl)

tf-plan:
	cd infra && terraform plan -input=false
	cd infra/bootstrap && terraform plan -input=false

tf-validate:
	cd infra && terraform fmt -check -recursive && terraform validate


.PHONY: dev build verify generate-posts test-tools media-deps media-stage media-publish media-release media-status media-watch-install media-watch-uninstall media-watch-status test-media test-layout test-link-check test-i18n check-repo-links tf-init tf-plan tf-validate
