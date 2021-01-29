+++
author = "Brian Pfeil"
categories = ["Python", "playground"]
date = 2021-01-08
description = ""
summary = " "
draft = false
slug = "sam-lambda-layers"
tags = ["sam","lambda","aws",]
title = "SAM Lambda Layers"
repoFullName = "pfeilbr/sam-lambda-layers-playground"
repoHTMLURL = "https://github.com/pfeilbr/sam-lambda-layers-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/sam-lambda-layers-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/sam-lambda-layers-playground</a>
</div>


learn [SAM lambda layers](https://aws.amazon.com/blogs/compute/working-with-aws-lambda-and-lambda-layers-in-aws-sam/)

## Running Example

```sh
cd lambda-layer-python

sam build

# run lambda with layer locally
# `--force-image-build` to clear out layer cache
sam local invoke --force-image-build

# start local api endpoint
sam local start-api --force-image-build
curl http://127.0.0.1:3000/

# deploy
sam deploy --guided

# run lambda behind api gateway endpoint
curl https://hl6u5bubr4.execute-api.us-east-1.amazonaws.com/Prod/
```

## Resources

* [Working with AWS Lambda and Lambda Layers in AWS SAM](https://aws.amazon.com/blogs/compute/working-with-aws-lambda-and-lambda-layers-in-aws-sam/)


