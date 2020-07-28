+++
author = "Brian Pfeil"
categories = ["C", "playground"]
date = 2016-06-02
description = ""
summary = "learn Emscripten"
draft = false
slug = "emscripten"
tags = ["playground",]
title = "Emscripten"
repoFullName = "pfeilbr/emscripten-playground"
repoHTMLURL = "https://github.com/pfeilbr/emscripten-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/emscripten-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/emscripten-playground</a>
</div>


learn and experiment with [emscripten](http://kripken.github.io/emscripten-site/)

## Running

1. Follow the [Download and install](http://kripken.github.io/emscripten-site/docs/getting_started/downloads.html) instructions
2. Run the following

```sh
# base install location
# ~/dev/emsdk_portable

# source in environment to update PATH and make tools available
# could add to .bash_profile to make available in all shells
$ source ~/dev/emsdk_env.sh


# needed to add python2 symlink (see https://github.com/kripken/emscripten/issues/3872)
$ cd /usr/local/bin
$ ln -s /usr/bin/python2.7 python2

# compile c file to javascript -> generates output/hello_world.js
$ emcc hello_world.c -o output/hello_world.js
$ node output/hello_world.js

# compile c file and generate html to view it -> generates output/hello.html and output/hello.js
# NOTE: overwrites
$ emcc hello_world.c -o output/hello.html
```



