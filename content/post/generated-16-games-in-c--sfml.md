+++
author = "Brian Pfeil"
categories = ["C++", "playground"]
date = 2022-04-15
description = ""
summary = " "
draft = false
slug = "16-games-in-c-sfml"
tags = ["cpp","game","sfml"]
title = "16 Games in C++/SFML"
repoFullName = "pfeilbr/16-games-in-c--sfml"
repoHTMLURL = "https://github.com/pfeilbr/16-games-in-c--sfml"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/16-games-in-c--sfml" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/16-games-in-c--sfml</a>
</div>


* From youtube series [Let's make 16 games in C++/SFML!](https://www.youtube.com/playlist?list=PLB_ibvUSN7mzUffhiay5g5GUHyJRO4DYr)
* [source code download](https://drive.google.com/uc?export=download&id=1naW_v6WAWYPgCIWNDskxtBsM84FoaOLh)

## Build and Run

Can compile each from command line on Mac via

```sh
# clang
clang++ \
-framework sfml-window \
-framework sfml-graphics \
-framework sfml-system \
-framework sfml-audio \
-framework sfml-network \
main.cpp -o main

# gcc
g++ \
-framework sfml-window \
-framework sfml-graphics \
-framework sfml-system \
-framework sfml-audio \
-framework sfml-network \
main.cpp -o main

# run
./main

```

> NOTE: assumes [SFML](https://www.sfml-dev.org/index.php) installed.  Frameworks should exist in `/Library/Frameworks`
