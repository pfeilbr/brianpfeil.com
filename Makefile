dev:
	hugo server --watch --disableFastRender --forceSyncStatic --buildDrafts

build:
	hugo --minify

verify: build

generate-posts:
	cd tools/generate-posts && go run . -user=pfeilbr -dest=../../content/post -debug

test-tools:
	cd tools/generate-posts && go test ./...

.PHONY: dev build verify generate-posts test-tools
