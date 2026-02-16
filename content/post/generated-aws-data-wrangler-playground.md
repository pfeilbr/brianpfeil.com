+++
author = "Brian Pfeil"
categories = ["Python", "playground"]
date = 2021-01-06
description = ""
summary = " "
draft = false
slug = "aws-data-wrangler"
tags = ["aws","data","python"]
title = "AWS Data Wrangler"
repoFullName = "pfeilbr/aws-data-wrangler-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-data-wrangler-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-data-wrangler-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-data-wrangler-playground</a>
</div>


learn [AWS Data Wrangler](https://aws-data-wrangler.readthedocs.io)

> python initiative that extends the power of Pandas library to AWS connecting DataFrames and AWS data related services (Amazon Redshift, AWS Glue, Amazon Athena, Amazon Timestream, Amazon EMR, Amazon QuickSight, etc).


## Running Examples

```sh
# install venv and deps
pipenv install

# activate venv
pipenv shell

# run examples
python main.py
```

See <https://github.com/awslabs/aws-data-wrangler/tree/master/tutorials> for example usages.

## Lambda Layer

Can be used via a [lambda layer](https://aws-data-wrangler.readthedocs.io/en/stable/install.html#aws-lambda-layer).

## Resources

* <https://aws-data-wrangler.readthedocs.io/>
* [awslabs/aws-data-wrangler](https://github.com/awslabs/aws-data-wrangler)
* [AWS Data Wrangler| API Reference](https://aws-data-wrangler.readthedocs.io/en/stable/api.html)
* <https://github.com/awslabs/aws-data-wrangler/tree/master/tutorials> - notebooks with examples

