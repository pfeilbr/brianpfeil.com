dev:
	hugo server --watch --disableFastRender --forceSyncStatic --buildDrafts

build:
	hugo --minify

install:
	npm install

verify: build
	bash scripts/verify.sh

generate-posts:
	cd tools/generate-posts && go run . -user=pfeilbr -dest=../../content/post -debug

test-tools:
	cd tools/generate-posts && go test ./...

.PHONY: dev build install verify generate-posts test-tools
