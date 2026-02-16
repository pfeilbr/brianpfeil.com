+++
author = "Brian Pfeil"
categories = ["Python", "playground"]
date = 2021-02-19
description = ""
summary = " "
draft = false
slug = "aws-glue-pyspark-fetch-databases-and-tables-metadata"
tags = ["aws","glue","spark","python"]
title = "AWS Glue Pyspark Fetch Databases and Tables Metadata"
repoFullName = "pfeilbr/aws-glue-pyspark-fetch-databases-and-tables-metadata-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-glue-pyspark-fetch-databases-and-tables-metadata-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-glue-pyspark-fetch-databases-and-tables-metadata-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-glue-pyspark-fetch-databases-and-tables-metadata-playground</a>
</div>


example AWS Glue pyspark job script that fetches all the catalog databases and tables metadata.

see [`main.py`](https://github.com/pfeilbr/aws-glue-pyspark-fetch-databases-and-tables-metadata-playground/blob/master/main.py)

* first method uses [spark sql](https://spark.apache.org/sql/)
* second method uses [python boto3 Glue client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html) to interact with [Glue API](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api.html) directly



## Notes

ensure `--enable-glue-datacatalog` is enabled for glue job to allow spark sql to access metadata catalog

![](https://www.evernote.com/l/AAG3O9zQGjhBQYiqT7_owkUm9K-UXd0bMCEB/image.png)

Glue Console Script View

![](https://www.evernote.com/l/AAG2b5Bdis5KFbt6ijxtySgIG7e2P8jPE0UB/image.png)

