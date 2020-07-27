+++
author = "Brian Pfeil"
categories = ["Go", "playground"]
date = 2020-04-16
description = ""
summary = "learning Goreleaser"
draft = false
slug = "goreleaser"
tags = ["playground",]
title = "Goreleaser"
repoFullName = "pfeilbr/goreleaser-playground"
repoHTMLURL = "https://github.com/pfeilbr/goreleaser-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/goreleaser-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/goreleaser-playground</a>
-->


learn [GoReleaser](https://goreleaser.com/) release automation tool for Go projects.

see <https://goreleaser.com/quick-start/>

## Session

```sh
goreleaser --snapshot --skip-publish --rm-dist

export GITHUB_TOKEN='GITHUB_TOKEN'

# tag.  release name is based on it
git tag -a v0.1.0 -m "First release"
git push origin v0.1.0

# run locally without publishing to github
goreleaser --snapshot --rm-dist

# build and publish
goreleaser

```


