+++
author = "Brian Pfeil"
categories = ["Makefile", "playground"]
date = 2020-01-13
description = ""
summary = "learning Make"
draft = false
slug = "make"
tags = ["make","github",]
title = "Make"
repoFullName = "pfeilbr/make-playground"
repoHTMLURL = "https://github.com/pfeilbr/make-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/make-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/make-playground</a>
-->


learn [make](https://www.gnu.org/software/make/manual/make.html)

## Resources

* [GNU make manual](https://www.gnu.org/software/make/manual/make.html)
* [The GNU Make Book](https://learning.oreilly.com/library/view/the-gnu-make/9781457189883/ch01.html)
* [purpose of .PHONY](https://stackoverflow.com/questions/2145590/what-is-the-purpose-of-phony-in-a-makefile)

```sh
# run `make` whenever Makefile changes
fswatch -o Makefile | xargs -n1 -I{} make
```


