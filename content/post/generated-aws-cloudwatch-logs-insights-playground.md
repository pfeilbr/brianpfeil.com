+++
author = "Brian Pfeil"
categories = ["Shell", "playground"]
date = 2020-10-30
description = ""
summary = " "
draft = false
slug = "aws-cloudwatch-logs-insights"
tags = ["aws","cloudwatch"]
title = "AWS CloudWatch Logs Insights"
repoFullName = "pfeilbr/aws-cloudwatch-logs-insights-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-cloudwatch-logs-insights-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-cloudwatch-logs-insights-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-cloudwatch-logs-insights-playground</a>
</div>


learn [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)

## Running Example Query via AWS CLI

see [`main.sh`](https://github.com/pfeilbr/aws-cloudwatch-logs-insights-playground/blob/master/main.sh)

```sh
# run script containing query
./main.sh
# OR
# re-run on change
make dev
```

## Example Queries

```sh
fields @timestamp, detail.eventSource, detail.eventName, @message
| sort @timestamp desc
| limit 100


fields @timestamp, detail.eventSource, detail.eventName, @message
| filter detail.eventSource = "logs.amazonaws.com"
| sort @timestamp desc
| limit 100


fields @timestamp, detail.requestParameters.bucketName, detail.eventSource, detail.eventName, @message
| filter detail.eventSource like /s3.amazonaws.com/
| sort @timestamp desc
| limit 100

# sts assume role CloudTrail events
fields @timestamp, source, `detail.eventName`, detail.requestParameters.roleArn, detail.userIdentity.userName, @message
| filter detail.eventSource = 'sts.amazonaws.com'
| sort @timestamp desc

# CodePipeline pipeline and stage change events
fields @timestamp, `detail-type`, detail.pipeline, detail.stage, detail.state, @message
| filter source = 'aws.codepipeline'
| sort @timestamp desc


```

## Resources

* [CloudWatch Logs Insights Query Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)
* [Sample Queries - Amazon CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-examples.html)
