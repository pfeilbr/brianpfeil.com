+++
author = "Brian Pfeil"
categories = ["C", "playground"]
date = 2019-11-11
description = ""
summary = "learning Glib"
draft = false
slug = "glib"
tags = ["github",]
title = "Glib"
repoFullName = "pfeilbr/glib-playground"
repoHTMLURL = "https://github.com/pfeilbr/glib-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/glib-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/glib-playground</a>
-->


learn [GNOME | GLib](https://wiki.gnome.org/Projects/GLib)

see [`main.c`](main.c)

## Prerequisites

```sh
brew install cmake
brew install glib
brew install pkg-config
```

## Build and Run
```sh
mkdir -p build && cd build
cmake .. && make

# run
./glib-playground
```

**output**

![](https://www.evernote.com/l/AAGf1T2-fgtCd6uHZGme-lg4Wl3IeEdUV-UB/image.png)

## Resources


* [Manage C data using the GLib collections](https://developer.ibm.com/tutorials/l-glib/)
* [GNOME | GLib](https://wiki.gnome.org/Projects/GLib)
* [GNOME/glib](https://github.com/GNOME/glib) repo


