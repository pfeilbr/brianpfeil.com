+++
author = "Brian Pfeil"
categories = ["Makefile", "playground"]
date = 2020-07-02
description = ""
summary = " "
draft = false
slug = "php-lambda-layer"
tags = ["php","lambda"]
title = "PHP Lambda Layer"
repoFullName = "pfeilbr/php-lambda-layer-playground"
repoHTMLURL = "https://github.com/pfeilbr/php-lambda-layer-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/php-lambda-layer-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/php-lambda-layer-playground</a>
</div>


learn [stackery/php-lambda-layer](https://github.com/stackery/php-lambda-layer) for running PHP on lambda

**Prerequisites**

* [php](https://www.php.net/) 7.x
* [composer](https://getcomposer.org/) installed globally (used by makefile)

**Key Files**

* [src/php/index.php](https://github.com/pfeilbr/php-lambda-layer-playground/blob/master/src/php/index.php)
* [src/php/php.ini](https://github.com/pfeilbr/php-lambda-layer-playground/blob/master/src/php/php.ini) - for enabled extensions
* [template.yaml](https://github.com/pfeilbr/php-lambda-layer-playground/blob/master/template.yaml)
* [packaged.yaml](https://github.com/pfeilbr/php-lambda-layer-playground/blob/master/packaged.yaml) - *generated via sam*

**Session**

see [Makefile](https://github.com/pfeilbr/php-lambda-layer-playground/blob/master/Makefile) for details and make changes to variables as necessary.

```sh
# deploy stack
make deploy

# test api gateway endpoint URL
make test

# delete stack
make delete

```

## Resources

* [Introducing the new Serverless LAMP stack](https://aws.amazon.com/blogs/compute/introducing-the-new-serverless-lamp-stack/)
* [Introducing the serverless LAMP stack – part 2 relational databases](https://aws.amazon.com/blogs/compute/introducing-the-serverless-lamp-stack-part-2-relational-databases/)
* [aws-samples/php-examples-for-aws-lambda](https://github.com/aws-samples/php-examples-for-aws-lambda) - github repo for article.
* [AWS Lambda Custom Runtime for PHP: A Practical Example](https://aws.amazon.com/blogs/apn/aws-lambda-custom-runtime-for-php-a-practical-example/) - *older article, but covers low level details*
* [AWS SDK for PHP](https://aws.amazon.com/sdk-for-php/)
