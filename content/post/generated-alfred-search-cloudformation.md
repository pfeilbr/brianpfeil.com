+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2022-02-28
description = ""
summary = " "
draft = false
slug = "alfred-search-cloudformation"
tags = ["cloudformation"]
title = "Alfred Search CloudFormation"
repoFullName = "pfeilbr/alfred-search-cloudformation"
repoHTMLURL = "https://github.com/pfeilbr/alfred-search-cloudformation"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/alfred-search-cloudformation" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/alfred-search-cloudformation</a>
</div>


---

## Install

```sh
git clone https://github.com/pfeilbr/alfred-search-cloudformation.git`
cd alfred-search-cloudformation
npm install

# follow [alfy#usage instructions](https://github.com/sindresorhus/alfy#usage)
# enable "Alfred filters results" checkbox

# symlink workflow directory to here
# example
cd /Users/pfeilbr/Dropbox/Alfred/Alfred.alfredpreferences/workflows
ln -s ~/projects/alfred-search-cloudformation user.workflow.3AFB139F-7BE0-4430-9EE4-36FCD4B2376D
```

---

![](https://www.evernote.com/l/AAGX4W0tBY1OJq8mFHkyHnIeJBUbpO_2bXQB/image.png)

---

## Usage

In Alfred, type `cfn`, <kbd>Enter</kbd>, and your query.

Select an item and press <kbd>Enter</kbd> open documentation in browser.<br>
Press <kbd>Shift</kbd> to view the link in Quick Look.
## To update to latest aws-sdk

## Updating CloudFormation Data

```sh
pushd data/aws-sdk
git pull
popd
npm run make
```



---

## Resources

* [sindresorhus/alfy](https://github.com/sindresorhus/alfy)
* [Script Filter JSON Format](https://www.alfredapp.com/help/workflows/inputs/script-filter/json/)
