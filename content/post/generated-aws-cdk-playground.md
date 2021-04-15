+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-07-11
description = ""
summary = " "
draft = false
slug = "aws-cdk"
tags = ["aws","cdk",]
title = "AWS CDK"
repoFullName = "pfeilbr/aws-cdk-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-cdk-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-cdk-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-cdk-playground</a>
</div>


learn [AWS Cloud Development Kit (CDK)](https://docs.aws.amazon.com/cdk/latest/guide/home.html)

see [`kitchen-sink/README.md`](kitchen-sink/README.md)
## Description

* express resources using general purpose programming languages (ts/js/python/java/C#)
* constructs - cfn (L1), CDK (L2), pattern/solution (L3)
* synth to cfn
* cloud assemblies - cfn + source code, docker images, assets (s3)
* aspects - ability to visit each node/resource in stack and apply changes
* Application -> Stacks -> Constructs
* [Runtime context](https://docs.aws.amazon.com/cdk/latest/guide/context.html#context_example)
* `[tf|k8s]` CDKs
* jsii - core/foundational tech for multi-language/polyglot support.  bind any language to underlying typescript implementation.
* CDK pipelines for CI/CD
## Key Files and Directories

* `bin` - entry point to CDK app.  imports 1 or more stacks from `lib` folder
* `lib/*-stack.*` - define stacks here which contain constructs
* `cdk.json` - cdk configuration
* `test` - unit/integration/e2e tests
* `cdk.out` - CDK assembly / synth output (cfn, assets, etc.)

## Common Areas

* `@aws-cdk/core - App, Stack, Stack.account, Stack.region, Stack.tags, Stack.terminationProtection, Construct, Duration, CfnOutput`
* `lambda.Function`, `lambda.Code.fromAsset`, `lambda.Code.fromInline`
* `@aws-cdk/aws-iam - Role, User, Group, PolicyStatement`

## Common Steps
```sh
# init cdk app
cdk init app --language javascript
cdk init app --language typescript

# list stacks in the app
cdk list

# [optional] build for ts -> js.  not required for js
npm run build

# synthesize to cfn (`cdk.out`)
cdk synth

# run tests
npm test

# compare the specified stack with the deployed stack
cdk diff

# deploy
cdk deploy

# force deploy, no prompt
cdk deploy  --force --require-approval never

# delete
cdk destroy [STACKS..]

```
## Resources

* [AWS CDK · AWS CDK Reference Documentation](https://docs.aws.amazon.com/cdk/api/latest/)
* [Infrastructure-as-Code | Constructs | AWS Solutions](https://aws.amazon.com/solutions/constructs/)
* [awslabs/aws-solutions-constructs](https://github.com/awslabs/aws-solutions-constructs)
* [aws-samples/aws-cdk-examples](https://github.com/aws-samples/aws-cdk-examples)
* [panacloud-modern-global-apps/full-stack-serverless-cdk](https://github.com/panacloud-modern-global-apps/full-stack-serverless-cdk)
* [github | search | "filename:cdk.json"](https://github.com/search?l=&q=filename%3Acdk.json&type=code)


