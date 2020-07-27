+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2018-02-03
description = ""
summary = "experimenting with AWS Emr"
draft = false
slug = "aws-emr"
tags = ["aws","emr","github",]
title = "AWS Emr"
repoFullName = "pfeilbr/aws-emr-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-emr-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/aws-emr-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-emr-playground</a>


examples of using aws-emr. hive, pig, spark, etc.

## Dynamodb Export/Import to/from S3 Examples

```sql
-- link hive table to dynamodb table
CREATE EXTERNAL TABLE hiveLogTable (id string, data string)
STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler' 
TBLPROPERTIES ("dynamodb.table.name" = "log", 
"dynamodb.column.mapping" = "id:id,data:data");

-- query dynamodb table using hive SQL
SELECT * FROM hiveLogTable;

-- export dynamodb table to s3
INSERT OVERWRITE DIRECTORY 's3://com.brianpfeil.scratch/emr/dynamodb/export/table/log/' SELECT * 
FROM hiveLogTable;

-- create export table that will be comma delimited
CREATE EXTERNAL TABLE s3_export(id string, data string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
LOCATION 's3://com.brianpfeil.scratch/emr/dynamodb/export/table/log/';

-- export dynamodb table to s3 as comman delimited file (csv)
INSERT OVERWRITE TABLE s3_export SELECT * FROM hiveLogTable;

-- link hive table to s3 path
CREATE EXTERNAL TABLE s3_import(id string, data string)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
LOCATION 's3://com.brianpfeil.scratch/emr/dynamodb/export/table/log/';

-- import csv data from s3 into dynamodb table
INSERT OVERWRITE TABLE hiveLogTable SELECT * FROM s3_import;
```


