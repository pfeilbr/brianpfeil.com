+++
author = "Brian Pfeil"
categories = ["Shell", "playground"]
date = 2020-02-04
description = ""
summary = " "
draft = false
slug = "fetch-all-github-repos-for-user"
tags = ["github","bash","cli"]
title = "Fetch All GitHub Repos for User"
repoFullName = "pfeilbr/fetch-all-github-repos-for-user"
repoHTMLURL = "https://github.com/pfeilbr/fetch-all-github-repos-for-user"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/fetch-all-github-repos-for-user" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/fetch-all-github-repos-for-user</a>
</div>


script to fetch all github repos for a given user

* [`fetch-all-github-repos-for-user.sh`](https://github.com/pfeilbr/fetch-all-github-repos-for-user/blob/master/fetch-all-github-repos-for-user.sh) - script

## Prerequisites

* [jq](https://stedolan.github.io/jq/) - command-line JSON processor

## Install

install to `~/bin` via `make install`

## Usage

`fetch-all-github-repos-for-user.sh [GTIHUB USERNAME]`

e.g. `fetch-all-github-repos-for-user.sh pfeilbr`

> creates `[GTIHUB USERNAME]` directory relative to current and stores each repo beneath it

## TODO

* only fetches first 100 repos.  update to fetch all of them
* fetch all updates to an existing "local" on disk repo.
    > cleanest option maybe to delete the local repo directory and re-clone
    > downside is dropbox need to resync everything

