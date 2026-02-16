+++
author = "Brian Pfeil"
categories = ["PHP", "playground"]
date = 2020-07-13
description = ""
summary = " "
draft = false
slug = "bref-php-lambda"
tags = ["php","lambda"]
title = "Bref PHP Lambda"
repoFullName = "pfeilbr/bref-php-lambda-playground"
repoHTMLURL = "https://github.com/pfeilbr/bref-php-lambda-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/bref-php-lambda-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/bref-php-lambda-playground</a>
</div>


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
