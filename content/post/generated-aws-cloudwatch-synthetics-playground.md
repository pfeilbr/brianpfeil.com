+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2023-09-06
description = ""
summary = " "
draft = false
slug = "aws-cloudwatch-synthetics"
tags = ["aws","cloudwatch"]
title = "AWS CloudWatch Synthetics"
repoFullName = "pfeilbr/aws-cloudwatch-synthetics-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-cloudwatch-synthetics-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-cloudwatch-synthetics-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-cloudwatch-synthetics-playground</a>
</div>


learn [CloudWatch Synthetics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html)

> You can use Amazon CloudWatch Synthetics to create canaries, configurable scripts that run on a schedule, to monitor your endpoints and APIs. Canaries follow the same routes and perform the same actions as a customer, which makes it possible for you to continually verify your customer experience even when you don't have any customer traffic on your applications.

## notes

* supports monitoring your REST APIs, URLs, and website content every minute, 24x7, and alerts you when your application endpoints don’t behave as expected.
* Node.js or python based.  bundles in Puppeteer + Chromium to the runtime
* trigger types - cron (1 min smallest freq), run once
* [can run in VPC](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_VPC.html)
* can also used in any workloads requiring general browser automation
* creates several [CloudWatch metrics in `CloudWatchSynthetics` namespace](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_metrics.html)
* EventBridge support.  See [monitoring canary events with Amazon EventBridge](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitoring-events-eventbridge.html)
* CloudFormation support via [`AWS::Synthetics::Canary`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html)
* if your handler has an error (e.g. `throws Error(..)`) that is not caught it counts as a failed canary

* e.g. [`Canary: Type: 'AWS::Synthetics::Canary'`](https://github.com/awslabs/aws-well-architected-labs/blob/main/static/Reliability/300_Fault_Isolation_with_Shuffle_Sharding/Code/regular.yaml#L575)
* e.g. [`CanaryAlarm: Type: AWS::CloudWatch::Alarm`](https://github.com/aws-samples/aws-reinvent-trivia-game/blob/master/canaries/template.yaml#L55)
* e.g. [`CanaryRole: Type: 'AWS::IAM::Role'`](https://github.com/awslabs/aws-well-architected-labs/blob/main/static/Reliability/300_Fault_Isolation_with_Shuffle_Sharding/Code/regular.yaml#L524)

## resources

- [CloudWatch Synthetics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html)
- [CloudWatch metrics published by canaries](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_metrics.html)
- [AWS::Synthetics::Canary](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html)
- [aws-reinvent-trivia-game/canaries](https://github.com/aws-samples/aws-reinvent-trivia-game/blob/master/canaries/README.md)
- <https://github.com/awslabs/aws-well-architected-labs/blob/main/static/Reliability/300_Fault_Isolation_with_Shuffle_Sharding/Code/regular.yaml#L575> - example cloudformation template
