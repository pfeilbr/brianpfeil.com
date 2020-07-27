+++
author = "Brian Pfeil"
categories = ["HTML", "playground"]
date = 2017-08-17
description = ""
summary = "experimenting with S3 Website"
draft = false
slug = "s3-website"
tags = ["playground",]
title = "S3 Website"
repoFullName = "pfeilbr/s3-website-playground"
repoHTMLURL = "https://github.com/pfeilbr/s3-website-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/s3-website-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/s3-website-playground</a>
-->


learn [s3-website](https://github.com/klaemo/s3-website) npm module

**usage session**

```sh
# install deps
npm install

# create static website
./node_modules/s3-website/s3-website.js create 

# deploy static website
com.brianpfeil.s3-website-playground.site01
./node_modules/s3-website/s3-website.js deploy

# view 
open http://com.brianpfeil.s3-website-playground.site01.s3-website-us-east-1.amazonaws.com

# NOTE: using `./node_modules/s3-website/s3-website.js` to avoid global install and
# doesn't work with `npx` because of https://www.evernote.com/l/AAH8gou8OCZKF6rfnqA2Tom3BU7c0xuFTM0B/image.png
```


