+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2021-12-05
description = ""
summary = " "
draft = false
slug = "aws-sam"
tags = ["aws","sam",]
title = "AWS SAM"
repoFullName = "pfeilbr/aws-sam-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-sam-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-sam-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-sam-playground</a>
</div>


playground for all things AWS SAM

## Demo

```sh
cd sam-app

sam sync --watch --stack-name sam-app

sam logs --tail

# run tests in `__tests__/`
AWS_SAM_STACK_NAME=sam-app npm run test

aws lambda invoke \
  --cli-binary-format "raw-in-base64-out" \
  --function-name "sam-app-helloFromLambdaFunction-SvAJyAV6zcDN" \
  --payload '{"msg": "hello"}' \
  output.log; cat output.log; rm output.log

```



