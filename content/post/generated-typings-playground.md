+++
author = "Brian Pfeil"
categories = ["TypeScript", "playground"]
date = 2016-05-02
description = ""
summary = "learning Typings"
draft = false
slug = "typings"
tags = ["playground",]
title = "Typings"
repoFullName = "pfeilbr/typings-playground"
repoHTMLURL = "https://github.com/pfeilbr/typings-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/typings-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/typings-playground</a>
</div>


learn and experiment with TypeScript typings

```sh
# install typescript
$ npm install typescript --global

# install typings
$ npm install typings --global

# install node typings
$ typings install node --ambient --save

# compile index.ts to index.js
$ tsc

# run
$ node index.js
```

see contents of `tsconfig.json`, which tells `tsc` how to compile

### Resources

* [How to add type definitions to a TypeScript project](http://www.davevoyles.com/how-to-add-type-definitions-to-a-typescript-project/)
* [typings](https://github.com/typings/typings)
* [DefinitelyTyped/DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped)
* <http://definitelytyped.org/>



