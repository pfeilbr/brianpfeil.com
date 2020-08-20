+++
author = "Brian Pfeil"
categories = ["Go", "playground"]
date = 2020-08-18
description = ""
summary = " "
draft = false
slug = "mage"
tags = ["golang","build","tools",]
title = "Mage"
repoFullName = "pfeilbr/mage-playground"
repoHTMLURL = "https://github.com/pfeilbr/mage-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/mage-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/mage-playground</a>
</div>


learn [mage](https://magefile.org/), a make/rake-like build tool using Go. You write plain-old go functions, and Mage automatically uses them as Makefile-like runnable targets.

## Install

```sh
git clone https://github.com/magefile/mage
cd mage
go run bootstrap.go
```


## Demo

```sh
git clone https://github.com/pfeilbr/mage-playground
cd mage-playground
go mod init mage-playground
# NOTE: `go.mod` must exist in same directory as `magefile.go`

# show targets
mage

# run "hello" target
mage hello
```


