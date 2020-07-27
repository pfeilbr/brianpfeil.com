+++
author = "Brian Pfeil"
categories = ["C++", "playground"]
date = 2015-05-19
description = ""
summary = "learn V8"
draft = false
slug = "v8"
tags = ["v8","github",]
title = "V8"
repoFullName = "pfeilbr/v8-playground"
repoHTMLURL = "https://github.com/pfeilbr/v8-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/v8-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/v8-playground</a>


Project to learn and experiment with the [V8](https://developers.google.com/v8/) javascript engine.

## Building V8 with Xcode

1. Install [depot-tools](http://dev.chromium.org/developers/how-tos/install-depot-tools).  And add to `PATH` environment variable.
2. Clone repo
    $ git clone https://chromium.googlesource.com/v8/v8.git
3. Build
    $ cd v8
    $ build/gyp_v8 -Dtarget_arch=x64

## Background

This project was created with a new `Application | Command Line Tool` with the language set to `C++` in Xcode.

The static libraries from the v8 build were copied in
![](http://note.io/1c3cOzl)

The v8 include files were copied from `v8/include` to `v8-includes`

## Resources

* [Google V8 Docs](https://developers.google.com/v8/)


