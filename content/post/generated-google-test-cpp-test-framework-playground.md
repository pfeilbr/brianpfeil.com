+++
author = "Brian Pfeil"
categories = ["C++", "playground"]
date = 2018-09-25
description = ""
summary = " "
draft = false
slug = "google-test-cpp-test-framework"
tags = ["google","cpp",]
title = "Google Test CPP Test Framework"
repoFullName = "pfeilbr/google-test-cpp-test-framework-playground"
repoHTMLURL = "https://github.com/pfeilbr/google-test-cpp-test-framework-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/google-test-cpp-test-framework-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/google-test-cpp-test-framework-playground</a>
</div>


learn [googletest](https://github.com/google/googletest) / [gtest](https://github.com/google/googletest) C++ test framework

see `README.md` in each subdirectory under [`src`](src)

## gtest install

```sh
# download source
cd ~/dev
curl -LO https://github.com/google/googletest/archive/release-1.8.1.zip
unzip release-1.8.1.zip
cd googletest-release-1.8.1
mkdir build
cd build
cmake ..
make
make install
```


