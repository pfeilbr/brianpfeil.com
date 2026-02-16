+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2020-11-01
description = ""
summary = " "
draft = false
slug = "aws-database-migration-service"
tags = ["aws"]
title = "AWS Database Migration Service"
repoFullName = "pfeilbr/aws-database-migration-service-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-database-migration-service-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-database-migration-service-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-database-migration-service-playground</a>
</div>


## Concepts

AWS DMS connects to the source data store, reads the source data, and formats the data for consumption by the target data store. It then loads the data into the target data store

At a high level, when using AWS DMS you do the following:

* Create a replication server.
* Create source and target endpoints that have connection information about your data stores.
* Create one or more migration tasks to migrate data between the source and target data stores.

![](https://docs.aws.amazon.com/dms/latest/userguide/images/datarep-intro-rep-instance1.png)

A task can consist of three major phases:

* The full load of existing data
* The application of cached changes (change data capture, CDC)
* Ongoing replication


* Pricing - Pay for ec2 replication instances and log storage
---

## Resources

* [AWS Database Migration Service](https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html)
* [AWS Schema Conversion Tool](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_SchemaConversionTool.Installing.html)
