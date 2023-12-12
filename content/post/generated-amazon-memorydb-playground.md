+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2023-09-05
description = ""
summary = " "
draft = false
slug = "amazon-memorydb"
tags = ["aws","db",]
title = "Amazon MemoryDB"
repoFullName = "pfeilbr/amazon-memorydb-playground"
repoHTMLURL = "https://github.com/pfeilbr/amazon-memorydb-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/amazon-memorydb-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/amazon-memorydb-playground</a>
</div>


learn [Amazon MemoryDB for Redis](https://aws.amazon.com/memorydb/)

## Demo

```sh
export AWS_PROFILE="hub01-admin"
export STACK_NAME=amazon-memorydb-playground
export REGION=us-east-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

sam build --use-container

sam deploy --guided
sam deploy

aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --region $REGION \
  --query 'Stacks[0].Outputs' \
  > stack-outputs.json

sam delete --no-prompts

```

## resources

- [Amazon MemoryDB for Redis](https://aws.amazon.com/memorydb/)
- [Amazon MemoryDB for Redis Documentation](https://docs.aws.amazon.com/memorydb/)
- [serverless-patterns/apigw-lambda-memorydb](https://github.com/aws-samples/serverless-patterns/tree/main/apigw-lambda-memorydb)
- [AWSinAction/code3/chapter11/memorydb-minimal.yaml](https://github.com/AWSinAction/code3/blob/main/chapter11/memorydb-minimal.yaml)
- [Configure ACLs with the ACL command](https://redis.io/docs/management/security/acl/)


