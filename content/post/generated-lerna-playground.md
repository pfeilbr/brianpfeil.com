+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2018-09-02
description = ""
summary = "learning Lerna"
draft = false
slug = "lerna"
tags = ["github",]
title = "Lerna"
repoFullName = "pfeilbr/lerna-playground"
repoHTMLURL = "https://github.com/pfeilbr/lerna-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/lerna-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/lerna-playground</a>
-->


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


