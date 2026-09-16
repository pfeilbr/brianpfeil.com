+++
author = "Brian Pfeil"
categories = ["CMake", "playground"]
date = 2018-10-07
description = ""
summary = " "
draft = false
slug = "cmake-vs-code-example"
tags = ["cmake","cpp","nix","vscode"]
title = "CMake VS Code Example"
repoFullName = "pfeilbr/cmake-vscode-example"
repoHTMLURL = "https://github.com/pfeilbr/cmake-vscode-example"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/cmake-vscode-example" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/cmake-vscode-example</a>
</div>


* example project using cmake
    * uses cmake `Find*.cmake` files in [`cmake/`](https://github.com/pfeilbr/cmake-vscode-example/blob/master/cmake/)
* uses [Nix](https://nixos.org/nixpkgs/manual/) package manager for managing development dependencies
    * see [`default.nix`](https://github.com/pfeilbr/cmake-vscode-example/blob/master/default.nix)
* [`main.cpp`](https://github.com/pfeilbr/cmake-vscode-example/blob/master/main.cpp) contains examples/code that leverages SFML, SDL2, GLFW,OpenGL, and SQLite3 to demonstrate leveraging dependencies

## Prerequisites

* [Nix](https://nixos.org/nix/download.html)

## Build and Run
```sh
git clone
cd cmake-vscode-example

# install dependencies if needed and setup shell
nix-shell

mkdir build
cd build
cmake ..
make

# run
./example
```
