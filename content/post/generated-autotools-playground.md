+++
author = "Brian Pfeil"
categories = ["M4", "playground"]
date = 2018-10-10
description = ""
summary = " "
draft = false
slug = "autotools"
tags = ["autotools","playground",]
title = "Autotools"
repoFullName = "pfeilbr/autotools-playground"
repoHTMLURL = "https://github.com/pfeilbr/autotools-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/autotools-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/autotools-playground</a>
</div>


learn Autotools

> Autotools is composed of several tools: aclocal, autoconf, automake and others, belonging to two packages: Automake and Autoconf

## Prerequisites

```brew install automake```

## Build and Run

```sh
brew install automake
mkdir hello_world
cd hello_world
touch main.c
touch configure.ac
touch Makefile.am
aclocal
autoconf
automake --add-missing
./configure
make
./helloworld

# make distrubution .tar.gz
make dist

# test that the distribution tarball
make distcheck

# Use Makefile to install the program
make install
```

**Resources**

* [The magic behind configure, make, make install](https://robots.thoughtbot.com/the-magic-behind-configure-make-make-install)
* [Using Autotools](https://developer.gnome.org/anjuta-build-tutorial/stable/create-autotools.html.en)


