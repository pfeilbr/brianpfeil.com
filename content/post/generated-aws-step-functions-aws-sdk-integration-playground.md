+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2021-10-15
description = ""
summary = " "
draft = false
slug = "aws-step-functions-aws-sdk-integration"
tags = ["aws","sdk","step-functions",]
title = "AWS Step Functions AWS SDK Integration"
repoFullName = "pfeilbr/aws-step-functions-aws-sdk-integration-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-step-functions-aws-sdk-integration-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-step-functions-aws-sdk-integration-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-step-functions-aws-sdk-integration-playground</a>
</div>


learn [AWS Step Functions AWS SDK Integrations](https://aws.amazon.com/blogs/aws/now-aws-step-functions-supports-200-aws-services-to-enable-easier-workflow-automation/).  Provides direct integration with 200+ AWS services

## Demo

Based on [Gather Amazon S3 bucket info using AWS SDK service integrations - AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-gather-s3-bucket-info-using-aws-sdk-service-integrations.html).

Deploy [`example01.yaml`](example01.yaml) stack

> NOTE: `ResultSelector` added to `ListBuckets` to hard code an array containing a single bucket to reduce amount of processing.

```sh

PROFILE="admin"
REGION="us-east-1"
STACK_NAME="aws-step-functions-aws-sdk-integration-playground"

aws cloudformation deploy \
    --profile "${PROFILE}" \
    --region "${REGION}" \
    --stack-name "${STACK_NAME}" \
    --template-file example01.yaml \
    --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND"

# execute step fn
aws stepfunctions start-execution \
  --state-machine-arn "arn:aws:states:us-east-1:529276214230:stateMachine:Gather-S3-Bucket-Info-Standard" \
  --input "{}"

```

Example Execution

![](https://www.evernote.com/l/AAFhqIDrJbpPYKPSBVNGpo2CMpzgcJbKL-4B/image.png)

## Resources

* [AWS Step Functions adds support for over 200 AWS Services with AWS SDK Integration](https://aws.amazon.com/about-aws/whats-new/2021/09/aws-step-functions-200-aws-sdk-integration/)
* [Now — AWS Step Functions Supports 200 AWS Services To Enable Easier Workflow Automation | Amazon Web Services](https://aws.amazon.com/blogs/aws/now-aws-step-functions-supports-200-aws-services-to-enable-easier-workflow-automation/)
* [AWS SDK service integrations - AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/supported-services-awssdk.html)


