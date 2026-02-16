+++
author = "Brian Pfeil"
categories = ["Python", "playground"]
date = 2021-11-24
description = ""
summary = " "
draft = false
slug = "pre-commit"
tags = ["git"]
title = "Pre Commit"
repoFullName = "pfeilbr/pre-commit-playground"
repoHTMLURL = "https://github.com/pfeilbr/pre-commit-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/pre-commit-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/pre-commit-playground</a>
</div>


learn [pre-commit](https://pre-commit.com/)

## Demo

```sh
# install
brew install pre-commit

# generate config
pre-commit sample-config > .pre-commit-config.yaml

# setup git hook scrips
pre-commit install

# run against all the files
pre-commit run --all-files
```

![](https://www.evernote.com/l/AAHJTrybBvFPXrUHVHUMfDDxCUkS_0jCwnwB/image.png)

## Resources

* [pre-commit](https://pre-commit.com/)

