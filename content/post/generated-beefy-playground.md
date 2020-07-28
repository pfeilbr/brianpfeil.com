+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2015-10-16
description = ""
summary = " "
draft = false
slug = "beefy"
tags = ["nodejs","tools",]
title = "Beefy"
repoFullName = "pfeilbr/beefy-playground"
repoHTMLURL = "https://github.com/pfeilbr/beefy-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/beefy-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/beefy-playground</a>
</div>


Learn and experiment with [Beefy](http://didact.us/beefy/), which makes working with [Browserify](http://browserify.org/) a little nicer.

---

### Running

1. Clone this repo
2. Install deps

  ```sh
  $ npm install
  ```

3. Run with live reload and es6 support ([babelify](https://github.com/babel/babelify))

  ```sh
  $ beefy index.js --live --open -- -t babelify
  ```

![](http://didact.us/beefy/cows.jpg)


