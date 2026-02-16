+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2023-01-27
description = ""
summary = " "
draft = false
slug = "amazon-opensearch-serverless"
tags = ["serverless","opensearch"]
title = "Amazon OpenSearch Serverless"
repoFullName = "pfeilbr/amazon-opensearch-serverless-playground"
repoHTMLURL = "https://github.com/pfeilbr/amazon-opensearch-serverless-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/amazon-opensearch-serverless-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/amazon-opensearch-serverless-playground</a>
</div>


## notes

- removes need to configure, manage, or scale OpenSearch clusters
- collection - group of indices representing a specific workload or use case.  two collection types - time series and search
- capacity is managed for you. you create a collection, then you query and index data using the same OpenSearch APIs as before
- Serverless compute capacity is measured in OpenSearch Compute Units (OCUs). Each OCU is a combination of 6 GiB of memory and corresponding virtual CPU (vCPU), as well as data transfer to S3
- decouples compute and storage.  separates the indexing (ingest) components from the search (query) components, with S3 as the primary data storage for indexes. can scale search and index functions independently of each other and independently of the indexed data in S3.
- costs - charged for the following components:
  - data ingestion compute
  - search and query compute
  - storage retained in S3
- billed for a minimum of 4 OCUs for the first collection in your account


![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*yXzV6O4EwUnFPl5i.png)

> Amazon OpenSearch Serverless architecture. Source: docs.aws.amazon.com

---

## demo

creates opensearch serverless collection, network policy, access policy, and iam user

[`template.yaml`](https://github.com/pfeilbr/amazon-opensearch-serverless-playground/blob/master/template.yaml) - based on [Using AWS CloudFormation to create Amazon OpenSearch Serverless collections](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-cfn.html)

```sh
sam deploy
```

---

## screenshots

![sam deploy output](https://www.evernote.com/l/AAFv_zdV95FOn4beVOGkIr1UzNcgxg1RtrQB/image.png)

---

## resources

- [Amazon OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html)
- [CloudFormation | Amazon OpenSearch Serverless](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_OpenSearchServerless.html)
- [Build a search application with Amazon OpenSearch Serverless](https://aws.amazon.com/blogs/big-data/build-a-search-application-with-amazon-opensearch-serverless/)
- [Using AWS CloudFormation to create Amazon OpenSearch Serverless collections](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-cfn.html)
- [Amazon OpenSearch goes Serverless!](https://medium.com/kreuzwerker-gmbh/amazon-opensearch-goes-serverless-4bc7813d5930)
