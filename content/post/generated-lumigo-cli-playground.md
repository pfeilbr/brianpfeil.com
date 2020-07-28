+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2020-07-17
description = ""
summary = " "
draft = false
slug = "lumigo-cli"
tags = ["cli",]
title = "Lumigo CLI"
repoFullName = "pfeilbr/lumigo-cli-playground"
repoHTMLURL = "https://github.com/pfeilbr/lumigo-cli-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/lumigo-cli-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/lumigo-cli-playground</a>
</div>


learn [lumigo-CLI](https://github.com/lumigo-io/lumigo-cli), A collection of helpful commands for working with AWS Lambda.

## Example Usage

```sh
# display contents of gzipped cloudfront log file to stdout
# see S3 SQL reference @  https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-glacier-select-sql-reference-select.html
lumigo-cli s3-select-batch \
  --region="us-east-1" \
  --bucket="com.brianpfeil.cloudfront.logs" \
  --prefix="brianpfeil.com/E2IL5HY5XTHLNW.2019-09-17-21.66bbda6b.gz" \
  --expression="SELECT * FROM S3Object s" \
  --fileType="CSV" \
  --compressionType="GZIP"

# list Lambda functions in ALL regions
lumigo-cli list-lambda
```


