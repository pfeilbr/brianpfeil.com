+++
author = "Brian Pfeil"
categories = ["C++", "playground"]
date = 2018-09-25
description = ""
summary = "experimenting with Google Test CPP Test Framework"
draft = false
slug = "google-test-cpp-test-framework"
tags = ["google","cpp","playground",]
title = "Google Test CPP Test Framework"
repoFullName = "pfeilbr/google-test-cpp-test-framework-playground"
repoHTMLURL = "https://github.com/pfeilbr/google-test-cpp-test-framework-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/google-test-cpp-test-framework-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/google-test-cpp-test-framework-playground</a>
-->


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


