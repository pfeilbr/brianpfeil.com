+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2017-07-18
description = ""
summary = " "
draft = false
slug = "aws-kinesis"
tags = ["aws","kinesis","playground",]
title = "AWS Kinesis"
repoFullName = "pfeilbr/aws-kinesis-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-kinesis-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-kinesis-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-kinesis-playground</a>
</div>


learn [aws kinesis](https://aws.amazon.com/documentation/kinesis/)

## example session

1. create kinesis stream
    ![](http://static-screenshots-01.s3-website-us-east-1.amazonaws.com/Amazon_Kinesis_Streams_Management_Console_1F1EA557.png)

2. create lambda (logs stream event)
    ![](http://static-screenshots-01.s3-website-us-east-1.amazonaws.com/handler_ts_—_serverless-typescript-webpack-playground_1F1EA52A.png)

3. kinesis stream triggers lambda
    ![](http://static-screenshots-01.s3-website-us-east-1.amazonaws.com/Lambda_Management_Console_1F1EA508.png)

4. put a record to kinesis stream via cli
    ![](http://static-screenshots-01.s3-website-us-east-1.amazonaws.com/1__pfeilbr_ifa102990____dev__zsh__and_README_md_—_aws-kinesis-playground_1F1EA586.png)

5. get shard iterator via cli
    ![](http://static-screenshots-01.s3-website-us-east-1.amazonaws.com/1__pfeilbr_ifa102990____dev__zsh__1F1EA648.png)

6. get records via cli

    ![](http://static-screenshots-01.s3-website-us-east-1.amazonaws.com/1__pfeilbr_ifa102990____dev__zsh__and_README_md_—_aws-kinesis-playground_1F1EA675.png))

7. view event in lambda cloudwatch logs
![](http://static-screenshots-01.s3-website-us-east-1.amazonaws.com/CloudWatch_Management_Console_1F1EA4E8.png)






