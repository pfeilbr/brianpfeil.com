+++
author = "Brian Pfeil"
categories = ["TypeScript", "playground"]
date = 2021-09-18
description = ""
summary = " "
draft = false
slug = "remote-development"
tags = ["vscode","docker","typescript"]
title = "Remote Development"
repoFullName = "pfeilbr/remote-development"
repoHTMLURL = "https://github.com/pfeilbr/remote-development"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/remote-development" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/remote-development</a>
</div>


project to facilitate remote development environment

## Requirements

* [projen](https://github.com/projen/projen/)

## Build & Deploy

```sh
npx projen new awscdk-app-ts

# make dep changes in `.projenrc.js` then run
npx projen

# watch
npm run test:watch

# update jest snapshots
npm run test:update

# test lambda(s)
pushd src/lambda/dev-env-schedule
pipenv run pytest
popd


# deploy
npm run deploy
./node_modules/.bin/cdk deploy --outputs-file ./cdk-outputs.json

# remove
npm run destroy
```

## TODO

* stashed changes for ApigatewayToLambda solution construct
