+++
author = "Brian Pfeil"
categories = ["Shell", "playground"]
date = 2019-01-29
description = ""
summary = "learning Fswatch"
draft = false
slug = "fswatch"
tags = ["github",]
title = "Fswatch"
repoFullName = "pfeilbr/fswatch-playground"
repoHTMLURL = "https://github.com/pfeilbr/fswatch-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/fswatch-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/fswatch-playground</a>


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



