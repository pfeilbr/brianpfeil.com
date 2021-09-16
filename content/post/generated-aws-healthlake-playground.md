+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2021-09-16
description = ""
summary = " "
draft = false
slug = "aws-healthlake"
tags = ["aws",]
title = "AWS Healthlake"
repoFullName = "pfeilbr/aws-healthlake-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-healthlake-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-healthlake-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-healthlake-playground</a>
</div>


learn [Health Data Lake and Healthcare Analytics - Amazon HealthLake - Amazon Web Services](https://aws.amazon.com/healthlake/)

## Concepts

* DataStore
	* data is encrypted at rest
		> Customers can choose an AWS owned KMS key or a Customer-managed KMS key when creating a Data Store.
	* encrypted in transit
		> Amazon HealthLake uses TLS 1.2 to encrypt data in transit through the public endpoint and through backend services.
* [import data](https://docs.aws.amazon.com/healthlake/latest/devguide/healthlake-examples-cli.html) (line delimited json record - .ldjson) from S3 bucket
	* where each line consists of a valid FHIR resource
* query data using Create, Read, Update, Delete functions via provided REST endpoint for a given DataStore
* use [FHIR search](https://docs.aws.amazon.com/healthlake/latest/devguide/using-search-healthlake.html)
	> After the data is ingested, it is indexed using Amazon ES, which makes the data searchable.
* [Integrated medical natural language processing (NLP)](https://docs.aws.amazon.com/healthlake/latest/devguide/integrated-medical-nlp.html)
	* the NLP results are automatically included in the results for a returned `DocumentReference` resource type.  No separate actions/etc. required.
	> Amazon HealthLake automatically integrates with natural language processing (NLP) for the DocumentReference resource type. The integrated medical NLP output is provided as an extension to the existing DocumentReference resource. The integration involves reading the text data within the resource, and then calling the following integrated medical NLP operations: DetectEntities-V2, InferICD10-CM, and InferRxNorm.
* export data to S3
	> Amazon HealthLake enables you to bulk export your files to an Amazon S3 bucket. Use either the console or start-fhir-export-job to begin an export job. Afterwards, you can use describe-fhir-export-job to monitor the status of the job and discover its properties. After the export job is complete, the data can then be visualized using AWS Quicksight or accessed by other AWS services.
* VPC endpoint (PrivateLink) support
	> You can establish a private connection between your VPC and Amazon HealthLake by creating an interface VPC endpoint. Interface VPC endpoints are powered by AWSPrivateLink

## Examples

```sh
# https://docs.aws.amazon.com/healthlake/latest/devguide/healthlake-examples-cli.html
​aws healthlake create-fhir-datastore \
    --datastore-type-version R4 \
    --preload-data-config PreloadDataType="SYNTHEA" \
    --datastore-name "FhirTestDatastore"
```


## Resources

* [Paging Doctor Cloud! Amazon HealthLake Is Now Generally Available | Amazon Web Services](https://aws.amazon.com/blogs/aws/paging-doctor-cloud-amazon-healthlake-is-now-generally-available/)
* [Amazon HealthLake Workshop](https://amazon-healthlake.workshop.aws/)
* <https://www.hl7.org/fhir/patient-examples.html#> - FHIR examples



