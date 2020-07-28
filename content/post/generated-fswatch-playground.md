+++
author = "Brian Pfeil"
categories = ["Shell", "playground"]
date = 2019-01-29
description = ""
summary = " "
draft = false
slug = "fswatch"
tags = ["playground",]
title = "fswatch"
repoFullName = "pfeilbr/fswatch-playground"
repoHTMLURL = "https://github.com/pfeilbr/fswatch-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/fswatch-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/fswatch-playground</a>
</div>


* learn [fswatch](http://emcrisostomo.github.io/fswatch/) file change monitor
* github @ [emcrisostomo/fswatch](https://github.com/emcrisostomo/fswatch)

### Example Script

see [`watch.sh`](watch.sh)

### Example Usage

```sh
# get file path information for changed files
fswatch -0 .

# print file path information for each changed file on separate line
fswatch -0 . | xargs -0 -n 1 -I {} echo {}
```



