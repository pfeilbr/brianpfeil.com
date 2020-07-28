+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2018-09-02
description = ""
summary = " "
draft = false
slug = "lerna"
tags = []
title = "Lerna"
repoFullName = "pfeilbr/lerna-playground"
repoHTMLURL = "https://github.com/pfeilbr/lerna-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/lerna-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/lerna-playground</a>
</div>


learn [lerna](https://lernajs.io/) *A tool for managing JavaScript projects with multiple packages*

## Prerequisites

install lerna 
`npm install --global lerna`

## Example Workflow

```sh
# init lerna repo
mkdir lerna-playground
cd lerna-playground
git init
lerna init

# create mathlib
cd packages
mkdir mathlib
cd mathlib
npm init -f
touch index.js # write mathlib code

# create client that depends on mathlib
cd ..
mkdir client
cd client
npm init -f

# add mathlib
lerna add mathlib

# create client code
touch index.js

# run client
node index.js
```


