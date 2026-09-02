+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2022-02-28
description = ""
summary = " "
draft = false
slug = "alfred-search-aws-sdk-for-javascript"
tags = ["aws","sdk"]
title = "Alfred Search AWS SDK for JavaScript"
repoFullName = "pfeilbr/alfred-search-aws-sdk-for-javascript"
repoHTMLURL = "https://github.com/pfeilbr/alfred-search-aws-sdk-for-javascript"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/alfred-search-aws-sdk-for-javascript" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/alfred-search-aws-sdk-for-javascript</a>
</div>


* search [AWS SDK for JavaScript v2](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html) from [Alfred](https://www.alfredapp.com/)
* works with [AWS SDK for JavaScript v2](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html)
* open documentation link in default browser
* forked from [SamVerschueren/alfred-aws](https://github.com/SamVerschueren/alfred-aws)

---

<img src="https://www.evernote.com/l/AAFaRIMMNSlF2IXYpKA4_ynFbrNVloyKbjUB/image.png" width="600px" />

---

## Install

```sh
git clone https://github.com/pfeilbr/alfred-search-aws-sdk-for-javascript.git`
cd alfred-search-aws-sdk-for-javascript
npm install

# follow [alfy#usage instructions](https://github.com/sindresorhus/alfy#usage)
# enable "Alfred filters results" checkbox

# symlink workflow directory to here
# example
cd /Users/pfeilbr/Dropbox/Alfred/Alfred.alfredpreferences/workflows
ln -s ~/projects/alfred-search-aws-sdk-for-javascript user.workflow.3AFB139F-7BE0-4430-9EE4-36FCD4B2376D
```

![](https://www.evernote.com/l/AAF0Rp6zliFL1qMl7WqPd7O7MNaHnaqUr1YB/image.png)

**Screenshots of Config in Alfred Workflow View**

![](https://www.evernote.com/l/AAFAU04pElBHZqUqk1SITrouQx3no0X8FRAB/image.png)

![](https://www.evernote.com/l/AAF3RKegmTJHsIjwIH7TYPbwMfhU9k1vFAkB/image.png)

![](https://www.evernote.com/l/AAHWchAAHcNM6oiNpaUU27cpXWG4Nkmc3FUB/image.png)


---

## Usage

In Alfred, type `awssdk`, <kbd>Enter</kbd>, and your query.

Select an item and press <kbd>Enter</kbd> to go to the AWS SDK documentation page.<br>
Press <kbd>Shift</kbd> to view the documentaion in Quick Look.

---

## To update to latest aws-sdk

```sh
# update to latest or specified version `aws-sdk`
npm install aws-sdk

# update `data.json` from local `aws-sdk` npm package
# it reads service metadata .json files from `./node_modules/aws-sdk/apis`
npm run generate-data
```

---

## Resources

* [SamVerschueren/alfred-aws](https://github.com/SamVerschueren/alfred-aws)
* [sindresorhus/alfy](https://github.com/sindresorhus/alfy)
* [Script Filter JSON Format](https://www.alfredapp.com/help/workflows/inputs/script-filter/json/)
