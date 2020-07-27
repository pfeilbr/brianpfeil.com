+++
author = "Brian Pfeil"
categories = ["Go", "playground"]
date = 2020-01-15
description = ""
summary = "learning Go Modules"
draft = false
slug = "go-modules"
tags = ["go","github",]
title = "Go Modules"
repoFullName = "pfeilbr/go-modules-playground"
repoHTMLURL = "https://github.com/pfeilbr/go-modules-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/go-modules-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/go-modules-playground</a>
-->


learn using [golang modules](https://blog.golang.org/using-go-modules)

## Resources

* <https://blog.golang.org/using-go-modules>
* [golang/go/wiki/Modules](https://github.com/golang/go/wiki/Modules)

## Session

```sh
# run tests recursively on change
fswatch -o . | xargs -n1 -I{} go test -v ./...

# run main on change
fswatch -o . | xargs -n1 -I{} go run main.go
```


