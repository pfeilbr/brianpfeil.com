+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2016-04-05
description = ""
summary = "learning Nexe"
draft = false
slug = "nexe"
tags = ["github",]
title = "Nexe"
repoFullName = "pfeilbr/nexe-playground"
repoHTMLURL = "https://github.com/pfeilbr/nexe-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/nexe-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/nexe-playground</a>
-->


Learn and experiment with [nexe](https://github.com/jaredallard/nexe)

nexe lets you *create a single executable out of your node.js apps*

## Install

```sh
$ npm install nexe -g
```

## Running

There are two methods to run nexe, command line and by specifying the paramaters in `package.json`

### Command line

```sh
$ nexe -r 4.2.4 -i ./index.js -o ./main.nex
```

> Downloads node source 4.2.4 for the platform it's running on in `./tmp` directory, compiles
> it, uses browserify on `./index.js` then bundles it all an outputs `./main.nex`

### `package.json`

`nexe` property of `package.json` specifies all the parameters

```sh
$ nexe

# output is ./main.nex, which is specified in the nexe.output property
```



