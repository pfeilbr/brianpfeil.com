+++
author = "Brian Pfeil"
categories = ["TypeScript", "playground"]
date = 2019-09-03
description = ""
summary = "learn AWS Delivlib"
draft = false
slug = "aws-delivlib"
tags = ["aws","playground",]
title = "AWS Delivlib"
repoFullName = "pfeilbr/aws-delivlib-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-delivlib-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-delivlib-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-delivlib-playground</a>
</div>


learn [aws-delivlib](https://github.com/awslabs/aws-delivlib), which is a library that leverages [AWS Cloud Development Kit (CDK)](https://aws.amazon.com/cdk/) for defining continuous pipelines for building, testing and publishing code libraries through AWS CodeBuild and AWS CodePipeline.  

## Prerequisites

* pipeline source github repo must exist. (e.g. [pfeilbr/aws-delivlib-playground](https://github.com/pfeilbr/aws-delivlib-playground))
* github personal access token must be stored in SSM Parameter named `/com/brianpfeil/aws-delivlib-playground/github-personal-access-token`
    ![](https://www.evernote.com/l/AAF_-QmIfApO6L_mprwOy_t1KOBcrEHejtwB/image.png)


## Running

[`src/pipeline-hello-world`](src/pipeline-hello-world) is an example code pipeline where the source is *this* github repo ([pfeilbr/aws-delivlib-playground](https://github.com/pfeilbr/aws-delivlib-playground)).  The source nodejs app is [`src/hello-world`](src/hello-world) with jest tests.

**Code Pipeline**
```
source -> build -> test (linux)
                -> test (windows)
```

> If any of the tests (`*.sh`) in [`src/pipeline-hello-world/tests/`](src/pipeline-hello-world/tests) change, be sure to do a `npm run build && npm run cdk deploy`.  Internally uses `assets.ZipDirectoryAsset` from `"@aws-cdk/assets"` package.

```sh
mkdir -p src/pipeline-hello-world
cd src/pipeline-hello-world
cdk init --language typescript

# at this time, `aws-delivlib` is not using the most recent version of CDK
# need to do the following
# see https://github.com/aws/aws-cdk/issues/1733
npm remove aws-cdk @aws-cdk/core aws-delivlib
npm i aws-cdk@0.24.1 -D
npm i @aws-cdk/cdk@0.24.1
npm i aws-delivlib

# for dev
npm run watch

# build
npm run build

# generate cfn to stdout
npm run cdk synth

# deploy stack
npm run cdk deploy

# make changes

# build
npm run build

# diff
npm run cdk diff

# delete stack
npm run cdk destroy
```

---

**AWS Console | CodePipeline**

![](https://www.evernote.com/l/AAEVgM6a2MdEw6rmWfVOIOc4GSg--d7mrX0B/image.png)

**AWS Console | CloudFormation Stack**
![](https://www.evernote.com/l/AAHMGAlD7OdL95oRQkmg5bb8dCffOzOMmcMB/image.png)


