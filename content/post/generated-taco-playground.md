+++
author = "Brian Pfeil"
categories = ["Java", "playground"]
date = 2016-05-20
description = ""
summary = " "
draft = false
slug = "taco"
tags = ["mobile","ios","framework",]
title = "Taco"
repoFullName = "pfeilbr/taco-playground"
repoHTMLURL = "https://github.com/pfeilbr/taco-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/taco-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/taco-playground</a>
</div>


learn and experiment with [TACO](http://taco.tools/) (Tools for [Apache Cordova](https://cordova.apache.org/))

### setup log

```sh
taco create taco-playground
cd taco-playground/
taco platform add ios
taco install-reqs ios
taco build ios

// livereload of web asset (.js, .html. css) changes via BrowserSync
taco emulate ios --livereload

// add a plugin using cordova
cordova plugin add cordova-plugin-device

//rebuild
taco build ios

// launch in emulator
taco emulate ios --livereload

// NOTE: see livereload workaround below if livereload doesn't work
```

## Workaround for TACO livereload not working

* Install [cdvlive](https://www.npmjs.com/package/cdvlive) module

Run

```sh
$ cdvlive ios --target="iPhone-6s, 9.2"
```

see <https://github.com/Microsoft/TACO/issues/269> for details

Livereload issue

![](http://static-content-01.s3-website-us-east-1.amazonaws.com/taco-playground_—_-bash_—_80×24_and_index_js_—__Users_pfeilbr_Dropbox_mac01_Users_brianpfeil_projects_taco-playground_1CEF80DE.png)

## Resources

* to start specific iOS simulator version see <http://stackoverflow.com/questions/22310526/cordova-start-specific-ios-emulator-image>
* live debug by attaching to simulator via safari dev tools ![](http://static-content-01.s3-website-us-east-1.amazonaws.com/Screenshot_5_20_16__1_35_PM_1CEF826B.png)



