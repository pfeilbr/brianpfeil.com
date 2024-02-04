+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2024-02-04
description = ""
summary = " "
draft = false
slug = "pkl"
tags = []
title = "Pkl"
repoFullName = "pfeilbr/pkl-playground"
repoHTMLURL = "https://github.com/pfeilbr/pkl-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/pkl-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/pkl-playground</a>
</div>


learn [Pkl](https://pkl-lang.org/index.html), configuration that is Programmable, Scalable, and Safe

## demo

[install](https://pkl-lang.org/main/current/pkl-cli/index.html#installation) the cli for your platform

```sh
# verify install
pkl --version

FILE=config.pkl
pkl eval $FILE
pkl eval --format json $FILE 
pkl eval --format yaml $FILE 
```

## resources

- [Pkl](https://pkl-lang.org/index.html)
- [Pkl // Docs](https://pkl-lang.org/main/current/index.html)
- [Truffle Language Implementation Framework](https://github.com/oracle/graal/tree/master/truffle) Pkl was built using the GraalVM Truffle framework


