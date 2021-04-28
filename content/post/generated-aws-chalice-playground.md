+++
author = "Brian Pfeil"
categories = ["Python", "playground"]
date = 2021-04-28
description = ""
summary = " "
draft = false
slug = "aws-chalice"
tags = ["aws","serverless","python","lambda",]
title = "AWS Chalice"
repoFullName = "pfeilbr/aws-chalice-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-chalice-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-chalice-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-chalice-playground</a>
</div>


learn [aws/chalice](https://github.com/aws/chalice)

> framework for writing serverless apps in python. It allows you to quickly create and deploy applications that use AWS Lambda.

## Notes

* focus is on building REST APIs (API Gateway + lambda)
* event sources support - cron, EventBridge, S3, SNS, SQS, Kinesis, DynamoDB
* compiles down to SAM template + zip containing python code + dependencies
* can combine with CDK to get all CDK features + chalice easy workflow/deploy benefits

---

## Demo

```sh
# install in isolated venv via pipx
pipx install chalice

# create new project
chalice new-project helloworld

# deploy
cd helloworld
chalice deploy

# see `helloworld/.chalice` for package artifacts

# test api gateway endpoint
curl https://zqzmirc025.execute-api.us-east-1.amazonaws.com/api/
# output: {"hello":"world"}

# generate package
chalice package packaged/

# SAM template created at `helloworld/packaged/sam.json`
# bundled python code + deps at `helloworld/packaged/deployment.zip`

# tear down
chalice delete

```

contents of `helloworld/packaged/deployment.zip`

<img src="https://www.evernote.com/l/AAHyCwsWwYtG96AmUf3xm04ZnMMIPOVDlD4B/image.png" alt="" width="75%" />


## Resources

[aws/chalice](https://github.com/aws/chalice)


