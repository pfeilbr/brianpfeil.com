+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2019-07-10
description = ""
summary = "learn AWS Fargate"
draft = false
slug = "aws-fargate"
tags = ["aws","fargate","playground",]
title = "AWS Fargate"
repoFullName = "pfeilbr/aws-fargate-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-fargate-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-fargate-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-fargate-playground</a>
</div>


learn [AWS Fargate](https://aws.amazon.com/fargate/)

```sh
# register task definition
aws ecs register-task-definition --cli-input-json file://./task-definitions/hello-world.json

# run task
aws ecs run-task --task-definition "fargate-001" --launch-type "FARGATE" --network-configuration '{"awsvpcConfiguration": {"subnets": ["subnet-154b7928", "subnet-4700526d", "subnet-6cf9a534", "subnet-af5052d9"],"securityGroups": ["sg-047fbd9524f6e2b5e"],"assignPublicIp": "ENABLED"}}'

# *** NOTE ***
# * "assignPublicIp": "ENABLED" is needed for ecs/fargate to pull image from docker hub
# * "securityGroups": must allow outbund traffic
# * make sure log group is already created
```


