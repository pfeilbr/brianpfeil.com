+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2021-05-11
description = ""
summary = " "
draft = false
slug = "serverless-finance"
tags = ["serverless"]
title = "Serverless Finance"
repoFullName = "pfeilbr/serverless-finance"
repoHTMLURL = "https://github.com/pfeilbr/serverless-finance"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/serverless-finance" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/serverless-finance</a>
</div>


send balance in google sheets to SMS notification phone numbers. runs daily.  SMS numbers stored in SSM parameter store.

* access to google sheets doc is via [Google APIs Node.js Client](https://github.com/googleapis/google-api-nodejs-client).  OAuth is used to authenticate and the first time requires user interaction.  `credentials.json` contains the OAuth details and `token.json` contains `access_token`, `refresh_token`, etc.
* you must generate [`credentials.json`](https://cloud.google.com/docs/authentication/getting-started) and save in the root
* `token.json` is created on first run and required manual interaction
* To update functon with `token.json`, run locally which will generate `token.json`, then deploy.

## Running

```sh
# install deps
npm install

# copy `.env.sample` and update
cp .env.sample .env

# run tests in watch mode
npm run test -- --watch

# run tests
npm run test

# deploy
npm run deploy

# manual run of `notifySubscribers` function
SLS_DEBUG=* ./node_modules/.bin/serverless invoke --function notifySubscribers
```

## TODO

* store and maintain `token.json` contents in secrets manager
