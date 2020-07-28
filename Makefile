.PHONY: dev install-site-script

dev:
	hugo server --watch --disableFastRender --forceSyncStatic --buildDrafts

install-site-script:
	cp site ~/bin
	chmod a+x ~/bin/site