+++
author = "Brian Pfeil"
categories = ["Rust", "playground"]
date = 2018-12-21
description = ""
summary = "learning Rust"
draft = false
slug = "rust"
tags = ["rust","playground",]
title = "Rust"
repoFullName = "pfeilbr/rust-playground"
repoHTMLURL = "https://github.com/pfeilbr/rust-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/rust-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/rust-playground</a>
</div>


learn [Rust](https://www.rust-lang.org/) programming language

## Prerequisites

* [nodemon](https://nodemon.io/) - enables compile and run on file change

## Development

```sh
# run on file(s) change (ensure `nodemon` is installed)
# turn off dead_code warning
nodemon --exec "RUSTFLAGS=\"$RUSTFLAGS -A dead_code\" cargo run" src/main.rs
```

## Resources

* [The Rust Programming Language book](https://doc.rust-lang.org/stable/book/)
* [Rust by Example](https://doc.rust-lang.org/rust-by-example/)



