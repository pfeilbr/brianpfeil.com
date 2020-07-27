+++
author = "Brian Pfeil"
categories = ["C++", "playground"]
date = 2018-09-25
description = ""
summary = "learning AWS SDK Cpp"
draft = false
slug = "aws-sdk-cpp"
tags = ["aws","sdk","cpp","playground",]
title = "AWS SDK Cpp"
repoFullName = "pfeilbr/aws-sdk-cpp-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-sdk-cpp-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/aws-sdk-cpp-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-sdk-cpp-playground</a>
-->


learn [aws-sdk-app](https://github.com/aws/aws-sdk-cpp) C++ SDK

see `README.md` file(s) in subdirectories of [`src`](src)

## install aws-sdk-cpp

```sh
cd ~/dev
git clone https://github.com/aws/aws-sdk-cpp.git
cd aws-sdk-cpp
mkdir build
cd build
cmake ..
make
make install
```

## build and run example

```sh
cd src/s3-example
mkdir -p build && cd build
cmake .. && make
# run
./s3-example 
```

**output**

![](https://www.evernote.com/l/AAHbKsr3KeNGBJvW9Vd8ksfJseH3wqGG7y4B/image.png)


**Key Install File Locations**

* `/usr/local/lib/cmake/AWSSDK` - cmake modules
* `/usr/local/include` - headers installed
* `/usr/local/lib` - libraries installed (e.g. libaws-cpp-sdk-core.dylib)


