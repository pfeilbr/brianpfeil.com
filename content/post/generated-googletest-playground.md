+++
author = "Brian Pfeil"
categories = ["C++", "playground"]
date = 2020-01-02
description = ""
summary = "learning Googletest"
draft = false
slug = "googletest"
tags = ["github",]
title = "Googletest"
repoFullName = "pfeilbr/googletest-playground"
repoHTMLURL = "https://github.com/pfeilbr/googletest-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/googletest-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/googletest-playground</a>


learn [Googletest](https://github.com/google/googletest), Google Testing and Mocking Framework with CMake

based on <https://raymii.org/s/tutorials/Cpp_project_setup_with_cmake_and_unit_tests.html>

```sh
# begin: one-time setup to add googletest dependency
mkdir lib
pushd lib
git clone https://github.com/google/googletest/
popd
# end: one-time setup

#clean
./run.sh clean

# build
./run.sh buildandtest

# run tests
./run.sh test

# build and run tests when file changes under src/ and tst/
./run.sh watch

# build main binary
./run.sh buildmain

# run main binary
./run.sh main
```

### googletest command line examples

```sh
# run all tests
./build/tst/app_tst

# list tests
./build/tst/app_tst --gtest_list_tests

# run specific test
./build/tst/app_tst --gtest_filter=MyLib.adhoc

# run all tests in MyLib
./build/tst/app_tst --gtest_filter='MyLib.*'

# list command line options
./build/tst/app_tst --help
```


