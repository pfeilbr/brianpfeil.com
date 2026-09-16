+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2016-03-14
description = ""
summary = " "
draft = false
slug = "angular-material-boilerplate"
tags = ["angular","redux","javascript"]
title = "Angular Material Boilerplate"
repoFullName = "pfeilbr/ng-material-boilerplate"
repoHTMLURL = "https://github.com/pfeilbr/ng-material-boilerplate"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/ng-material-boilerplate" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/ng-material-boilerplate</a>
</div>

## ng-material-boilerplate

Boilerplate template with the following baked in

* [Babel](https://babeljs.io/) - es6
* [Browserify](http://browserify.org/) - bundle
* [Watchify](https://github.com/substack/watchify) - re-bundle on change for dev
* [live-server](https://github.com/tapio/live-server) - livereload for dev
* [Angular Material](https://material.angularjs.org) - UI
* [Redux](http://redux.js.org/) - state container
* [ng-redux](https://github.com/wbuchwalter/ng-redux) - Angular bindings for Redux
* [concurrently](https://github.com/kimmobrunfeldt/concurrently) - run commands concurrently

**Install/Setup**

```sh
$ git clone https://github.com/pfeilbr/ng-material-boilerplate
$ cd ng-material-boilerplate
$ npm install
$ npm install watchify -g
$ npm install live-server -g
```

**Develop with Livereload**

```sh
$ npm run dev
```

> rebuilds on file change and livereloads in browser

**Build**

```sh
$ npm run build
```

