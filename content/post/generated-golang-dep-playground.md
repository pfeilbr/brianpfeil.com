+++
author = "Brian Pfeil"
categories = ["Go", "playground"]
date = 2018-02-03
description = ""
summary = " "
draft = false
slug = "golang-dep"
tags = []
title = "Golang Dep"
repoFullName = "pfeilbr/golang-dep-playground"
repoHTMLURL = "https://github.com/pfeilbr/golang-dep-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/golang-dep-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/golang-dep-playground</a>
</div>


project to learn to use [dep](https://golang.github.io/dep/) the dependency management tool for [go](https://golang.org/)

```sh
# create new project
dep init

# add new import(s) in source code

# pull down imports into ./vendor/
dep ensure

# can always run `dep ensure` to sync everything up
```


