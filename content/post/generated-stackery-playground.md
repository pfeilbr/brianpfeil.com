+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-10-09
description = ""
summary = "learning Stackery"
draft = false
slug = "stackery"
tags = ["playground",]
title = "Stackery"
repoFullName = "pfeilbr/stackery-playground"
repoHTMLURL = "https://github.com/pfeilbr/stackery-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/stackery-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/stackery-playground</a>
-->


learn [stackery](https://www.stackery.io).  Project based on [Stackery Quickstart NodeJS](https://docs.stackery.io/docs/quickstart/quickstart-nodejs/).


## Comments (as of 2019-10-09)

* competes with [serverless dashboard](https://serverless.com/dashboard/).  many of the same features.  secrets service, environment management, team/collaboration support
* says it supports serverless framework (serverless.yml), but SAM seems to be the first class citizen.  SAM since its based on CF, lags behind in feature support over serverless.  Serverless fills the gaps with custom plugins.
* installs a stack (roles, buckets, CodeBuild project, lambdas, SNS topics, etc.) into your account to link your aws account to the stackery SaaS service.
* the stackery cli feels heavy due to the number of flags and arguments you need to supply.  e.g. always specifying env and aws profile.
* documentation feels a bit all over the place.  this may be because the tool doesn't have strong opinions and is favoring flexibility.

## Prerequisites

* docker

## Session

```sh
# ensure docker is running

# install
brew tap stackery/tap
brew install stackery-cli

stackery login

# init
stackery init -n stackery-quickstart

# visual editor
stackery edit

# deploy
stackery deploy --interactive-setup

# cd to function directory
cd src/get

# invoke
stackery local invoke -e pfeilbr-development --aws-profile admin

```

Stackery editor that generates cloudformation (`template.yml`) or serverless framework (`serverless.yml`).

![](https://www.evernote.com/l/AAFgto9OKTlMwKVUOV7Lhf2CztcnBgXKJ_MB/image.png)

![](https://www.evernote.com/l/AAFgto9OKTlMwKVUOV7Lhf2CztcnBgXKJ_MB/image.png)

There is a ["link your AWS account with Stackery"](https://docs.stackery.io/docs/using-stackery/security-permissions-and-controls/) one time setup.

Creates CF Stack for initial setup.  Includes Roles, Bucket, CodeBuild, Lambdas, SNS.
![](https://www.evernote.com/l/AAF1h3yovr1McrljVXDcmL0UbeDZ91r_Do0B/image.png)

Roles created during one time setup
![](https://www.evernote.com/l/AAEqUjVG_31HLZX63acjnPe3Xs7L4BYbn_AB/image.png)

## Resources

* [Stackery Quickstart NodeJS](https://docs.stackery.io/docs/quickstart/quickstart-nodejs/)
* [Stackery Documentation](https://docs.stackery.io)


