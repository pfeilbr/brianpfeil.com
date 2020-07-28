+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2015-09-29
description = ""
summary = " "
draft = false
slug = "node-coveralls"
tags = ["testing","nodejs",]
title = "Node Coveralls"
repoFullName = "pfeilbr/node-coveralls-playground"
repoHTMLURL = "https://github.com/pfeilbr/node-coveralls-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/node-coveralls-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/node-coveralls-playground</a>
</div>


# node-coveralls-playground

To learn and experiment with [coveralls](https://coveralls.io/) test coverage service.

## Setup Steps

1. Install deps

    ```
    $ npm install mocha coveralls mocha-lcov-reporter --save-dev
    ```

2. Install [istanbul](https://gotwarlost.github.io/istanbul/)

    ```
    $ npm install istanbul --save-dev -g
    ```

3. If running from command line, ensure `.coveralls.yml` is in current directory.  It should contain a line with `repo_token: REPO_TOKEN`

## Running

To run on the tests in the `test/` directory.

```
$ istanbul cover ./node_modules/mocha/bin/_mocha --report lcovonly -- -R spec && cat ./coverage/lcov.info | ./node_modules/coveralls/bin/coveralls.js && rm -rf ./coverage
```

> You can view the raw coverage output in the `./coverage` directory.



