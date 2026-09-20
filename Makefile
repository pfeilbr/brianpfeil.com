dev:
	hugo server --watch --disableFastRender --forceSyncStatic --buildDrafts

build:
	hugo --minify

verify: build

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

media-status:
	cd tools/instagram-media && .venv/bin/python pull.py status

test-media:
	cd tools/instagram-media && .venv/bin/python -m unittest discover -s tests


.PHONY: dev build verify generate-posts test-tools media-deps media-stage media-publish media-status test-media
