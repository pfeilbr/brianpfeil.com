+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2022-09-08
description = ""
summary = " "
draft = false
slug = "alfred-utilities-workflow"
tags = []
title = "Alfred Utilities Workflow"
repoFullName = "pfeilbr/alfred-utilities-workflow"
repoHTMLURL = "https://github.com/pfeilbr/alfred-utilities-workflow"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/alfred-utilities-workflow" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/alfred-utilities-workflow</a>
</div>


- general set of utility commands that can be invoked via alfred. `u` is the alfred keyword

---

## Install

```sh
git clone https://github.com/pfeilbr/alfred-utilities-workflow.git`
cd alfred-utilities-workflow
npm install

# follow [alfy#usage instructions](https://github.com/sindresorhus/alfy#usage)
# enable "Alfred filters results" checkbox

# symlink workflow directory to here
# example
cd /Users/pfeilbr/Dropbox/Alfred/Alfred.alfredpreferences/workflows
ln -s ~/projects/alfred-utilities-workflow user.workflow.3AFB139F-7BE0-4430-9EE4-36FCD4B2376D
```

---

![](https://www.evernote.com/l/AAGoCc1APOhGLKmQVjVmPpnU2tox4TdOuyoB/image.png)

![](https://www.evernote.com/l/AAHWlbSpgllGJaqiPdWDdse0pCjXiTTxsZIB/image.png)

![](https://www.evernote.com/l/AAFvF5NC8f5F4p88l9aERsoFUnD-WBbnZPIB/image.png)


---

## Usage

In Alfred, type `u`, <kbd>Enter</kbd>, and your query.

Select a command to run press <kbd>Enter</kbd>

---

## Resources

* [sindresorhus/alfy](https://github.com/sindresorhus/alfy)
* [Script Filter JSON Format](https://www.alfredapp.com/help/workflows/inputs/script-filter/json/)


