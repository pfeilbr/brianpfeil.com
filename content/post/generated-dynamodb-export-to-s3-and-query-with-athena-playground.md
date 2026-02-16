+++
author = "Brian Pfeil"
categories = ["Shell", "playground"]
date = 2020-11-11
description = ""
summary = " "
draft = false
slug = "dynamodb-export-to-s3-and-query-with-athena"
tags = ["dynamodb","s3","aws","athena"]
title = "DynamoDB Export to S3 and Query with Athena"
repoFullName = "pfeilbr/dynamodb-export-to-s3-and-query-with-athena-playground"
repoHTMLURL = "https://github.com/pfeilbr/dynamodb-export-to-s3-and-query-with-athena-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/dynamodb-export-to-s3-and-query-with-athena-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/dynamodb-export-to-s3-and-query-with-athena-playground</a>
</div>


example exporting dynamodb table to S3 and then querying via athena

## Files

* [`template.yaml`](https://github.com/pfeilbr/dynamodb-export-to-s3-and-query-with-athena-playground/blob/master/template.yaml)
* [`main.sh`](https://github.com/pfeilbr/dynamodb-export-to-s3-and-query-with-athena-playground/blob/master/main.sh)
* [`example-export/`](https://github.com/pfeilbr/dynamodb-export-to-s3-and-query-with-athena-playground/blob/master/example-export) - example contents of export (copied from S3)

## Running

```sh
sam deploy --guided
# note: seed data is generated as part of deploy via cfn custom resource `Custom::SeedData`
# which triggers a lambda which populates the dynamodb table

# update `STACK_NAME` variable in ./main.sh
# run export table to s3 script
./main.sh

aws dynamodb list-exports # in progress
```

```json
{
    "ExportSummaries": [
        {
            "ExportArn": "arn:aws:dynamodb:us-east-1:529276214230:table/dynamodb-export-to-s3-and-query-with-athena-playground-v2-MyTable-1WGSJ3W2WJWPK/export/01605130432834-8a918b87",
            "ExportStatus": "IN_PROGRESS"
        }
    ]
}
```

```sh
aws dynamodb list-exports # completed
```
```json
{
    "ExportSummaries": [
        {
            "ExportArn": "arn:aws:dynamodb:us-east-1:529276214230:table/dynamodb-export-to-s3-and-query-with-athena-playground-v2-MyTable-1WGSJ3W2WJWPK/export/01605130432834-8a918b87",
            "ExportStatus": "COMPLETED"
        }
    ]
}
```

Example export file contents (line delimited json items)

`gzcat example-export/demo_prefix/AWSDynamoDB/01605130432834-8a918b87/data/vajn3deidy4svdja3fgej2ynay.json.gz`

```json
{"Item":{"pk":{"S":"pk001-1605121017583"},"sk":{"S":"sk001"}}}
{"Item":{"pk":{"S":"pk002-1605121017583"},"sk":{"S":"sk002"}}}
```

**Access Exported Data in S3 via Athena**

```sql
-- Create external table in athena pointing to exported S3 data
CREATE EXTERNAL TABLE IF NOT EXISTS ddb_exported_table (
  Item struct <pk:struct<S:string>,
               sk:struct<S:string>>
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://dynamodb-export-to-s3-and-query-with-exportbucket-103kukqwmab7n/demo_prefix/AWSDynamoDB/01605130432834-8a918b87/data/'
TBLPROPERTIES ( 'has_encrypted_data'='true');

-- issues SELECT query
SELECT
    Item.pk.S as pk,
    Item.sk.S as sk
FROM ddb_exported_table
```

Screenshot from Athena Console

![](https://www.evernote.com/l/AAH1H1K1GLJAp72MXnQvHCiOBLxptt9FkrYB/image.png)

## Resources

* [New – Export Amazon DynamoDB Table Data to Your Data Lake in Amazon S3, No Code Writing Required](https://aws.amazon.com/blogs/aws/new-export-amazon-dynamodb-table-data-to-data-lake-amazon-s3/)
* [Now you can export your Amazon DynamoDB table data to your data lake in Amazon S3 to perform analytics at any scale](https://aws.amazon.com/about-aws/whats-new/2020/11/now-you-can-export-your-amazon-dynamodb-table-data-to-your-data-lake-in-amazon-s3-to-perform-analytics-at-any-scale/)
* [Exporting DynamoDB table data to Amazon S3](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DataExport.html)
* [AWS CloudFormation custom resource creation with Python, AWS Lambda, and crhelper](https://aws.amazon.com/blogs/infrastructure-and-automation/aws-cloudformation-custom-resource-creation-with-python-aws-lambda-and-crhelper/)

