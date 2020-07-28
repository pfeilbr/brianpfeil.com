+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2018-11-13
description = ""
summary = " "
draft = false
slug = "aws-amplify-js-app"
tags = ["aws","amplify","js",]
title = "AWS Amplify JS App"
repoFullName = "pfeilbr/aws-amplify-js-app-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-amplify-js-app-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-amplify-js-app-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-amplify-js-app-playground</a>
</div>


* learn [AWS Amplify Framework](https://aws-amplify.github.io/)
* getting started walkthrough @ <https://aws-amplify.github.io/docs/js/start?ref=amplify-js-btn&platform=purejs>

**Session**

```sh
mkdir aws-amplify-js-app-playground
cd aws-amplify-js-app-playground/\\n
mkdir src
touch package.json index.html webpack.config.js src/app.js
touch README.md
npm i
npm start
npm install --save aws-amplify
amplify init
amplify status
amplify add analytics
amplify push
amplify add hosting
amplify publish
amplify status
```


