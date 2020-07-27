+++
author = "Brian Pfeil"
categories = ["PHP", "playground"]
date = 2020-07-13
description = ""
summary = "learning Bref PHP Lambda"
draft = false
slug = "bref-php-lambda"
tags = ["php","lambda","github",]
title = "Bref PHP Lambda"
repoFullName = "pfeilbr/bref-php-lambda-playground"
repoHTMLURL = "https://github.com/pfeilbr/bref-php-lambda-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/bref-php-lambda-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/bref-php-lambda-playground</a>
-->


learn [bref](https://bref.sh/), deploy and run serverless PHP applications

## Prerequisites

* [PHP](https://www.php.net/)
* [serverless framework](https://www.serverless.com/)

## Running

```sh
# install
composer require bref/bref

# init
vendor/bin/bref init

# edit `index.php`

# deploy
serverless deploy

# test / invoke
serverless invoke -f "function"

# test / invoke with event data
serverless invoke --function "function" --data '{"name": "foo"}'
```

## Resources

* [bref | Installation](https://bref.sh/docs/installation.html)


