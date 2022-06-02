+++
author = "Brian Pfeil"
categories = ["Dockerfile", "playground"]
date = 2022-06-01
description = ""
summary = " "
draft = false
slug = "emr-serverless"
tags = ["emr","serverless",]
title = "EMR Serverless"
repoFullName = "pfeilbr/emr-serverless-playground"
repoHTMLURL = "https://github.com/pfeilbr/emr-serverless-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/emr-serverless-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/emr-serverless-playground</a>
</div>


learn [EMR Serverless](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html)

> provides a serverless runtime environment that simplifies the operation of analytics applications that use the latest open source frameworks, such as Apache Spark and Apache Hive. With EMR Serverless, you don’t have to configure, optimize, secure, or operate clusters to run applications with these frameworks.

## general flow

1. create application
1. start application
   - > your application is setup to start with pre-initialized capacity of 1 Spark driver and 1 Spark executor. Your application is by default configured to start when jobs are submitted and stop when the application is idle for more than 15 minutes. 
1. submit application jobs. e.g. spark or hive

## Demo

```sh
# deploy template.yaml
sam deploy --guided

aws emr-serverless get-application \
    --application-id 00f1du6284vksm09
{
    "application": {
        "applicationId": "00f1du6284vksm09",
        "name": "spark-3.2",
        "arn": "arn:aws:emr-serverless:us-east-1:529276214230:/applications/00f1du6284vksm09",
        "releaseLabel": "emr-6.6.0",
        "type": "Spark",
        "state": "CREATED",
        "stateDetails": "",
        "createdAt": "2022-06-02T20:09:49.041000+00:00",
        "updatedAt": "2022-06-02T20:09:49.667000+00:00",
        "tags": {
            "tag-on-create-key": "tag-on-create-value"
        },
        "autoStartConfiguration": {
            "enabled": true
        },
        "autoStopConfiguration": {
            "enabled": true,
            "idleTimeoutMinutes": 15
        }
    }
}

aws s3 cp s3://us-east-1.elasticmapreduce/emr-containers/samples/wordcount/scripts/wordcount.py s3://emr-serverless-playground-scriptbucket-1fl6snd6viqk6/scripts/

APPLICATION_ID="00f1du6284vksm09"
EXECUTION_ROLE_ARN="arn:aws:iam::529276214230:role/EMRServerless_Job_Execution_Role"
BUCKET_NAME="emr-serverless-playground-scriptbucket-1fl6snd6viqk6"
aws emr-serverless start-job-run \
    --application-id $APPLICATION_ID \
    --execution-role-arn $EXECUTION_ROLE_ARN \
    --job-driver '{
        "sparkSubmit": {
          "entryPoint": "s3://emr-serverless-playground-scriptbucket-1fl6snd6viqk6/scripts/wordcount.py",
          "entryPointArguments": ["s3://emr-serverless-playground-scriptbucket-1fl6snd6viqk6/emr-serverless-spark/output"],
          "sparkSubmitParameters": "--conf spark.executor.cores=1 --conf spark.executor.memory=4g --conf spark.driver.cores=1 --conf spark.driver.memory=4g --conf spark.executor.instances=1"
        }
    }'
# output
{
    "applicationId": "00f1du6284vksm09",
    "jobRunId": "00f1e0i4fr44ra01",
    "arn": "arn:aws:emr-serverless:us-east-1:529276214230:/applications/00f1du6284vksm09/jobruns/00f1e0i4fr44ra01"
}

JOB_RUN_ID="00f1e0i4fr44ra01"
aws emr-serverless get-job-run \
    --application-id $APPLICATION_ID \
    --job-run-id $JOB_RUN_ID

# output
{
    "jobRun": {
        "applicationId": "00f1du6284vksm09",
        "jobRunId": "00f1e0i4fr44ra01",
        "arn": "arn:aws:emr-serverless:us-east-1:529276214230:/applications/00f1du6284vksm09/jobruns/00f1e0i4fr44ra01",
        "createdBy": "arn:aws:sts::529276214230:assumed-role/AWSReservedSSO_AWSAdministratorAccess_af1bdd24238208b5/pfeilbr",
        "createdAt": "2022-06-02T22:22:36.221000+00:00",
        "updatedAt": "2022-06-02T22:28:06.614000+00:00",
        "executionRole": "arn:aws:iam::529276214230:role/EMRServerless_Job_Execution_Role",
        "state": "SUCCESS",
        "stateDetails": "",
        "releaseLabel": "emr-6.6.0",
        "jobDriver": {
            "sparkSubmit": {
                "entryPoint": "s3://emr-serverless-playground-scriptbucket-1fl6snd6viqk6/scripts/wordcount.py",
                "entryPointArguments": [
                    "s3://emr-serverless-playground-scriptbucket-1fl6snd6viqk6/emr-serverless-spark/output"
                ],
                "sparkSubmitParameters": "--conf spark.executor.cores=1 --conf spark.executor.memory=4g --conf spark.driver.cores=1 --conf spark.driver.memory=4g --conf spark.executor.instances=1"
            }
        },
        "tags": {},
        "totalResourceUtilization": {
            "vCPUHour": 0.066,
            "memoryGBHour": 0.331,
            "storageGBHour": 1.322
        }
    }
}

JOB_RUN_LOGS="s3://$BUCKET_NAME/emr-serverless-spark/logs/applications/$APPLICATION_ID/jobs/$JOB_RUN_ID"
```

## Notes

- unlike EMR the EC2 instances backing EMR-Serverless applications/jobs are not visible to the customer / fully managed (e.g. not visible in the customer EC2 console)
- [Type](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-type) - Spark or HIVE
- [ReleaseLabel](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-releaselabel) - EMR release version associated with the application.  see [Release versions](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/release-versions.html)
- EMR Serverless is a Regional service
- [Job run states](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/job-states.html)
- [Spark examples](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/jobs-spark.html#spark-examples)
- [Hive job examples](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/jobs-hive.html#hive-examples)
- [Using Python libraries with EMR Serverless](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/using-python-libraries.html)
- [Submitting jobs from Airflow](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/using-airflow.html)

## Resource Types

- application - `arn:${Partition}:emr-serverless:${Region}:${Account}:/applications/${ApplicationId}`
- jobRun `arn:${Partition}:emr-serverless:${Region}:${Account}:/applications/${ApplicationId}/jobruns/${JobRunId}`

## AWS CLI Support

```sh
# create application
aws emr-serverless create-application \
  --type HIVE \
  --name serverless-demo \
  --release-label "emr-6.6.0" \
  --initial-capacity '{
        "DRIVER": {
            "workerCount": 1,
            "resourceConfiguration": {
                "cpu": "2vCPU",
                "memory": "4GB",
                "disk": "30gb"
            }
        },
        "TEZ_TASK": {
            "workerCount": 10,
            "resourceConfiguration": {
                "cpu": "4vCPU",
                "memory": "8GB",
                "disk": "30gb"
            }
        }
    }' \
    --maximum-capacity '{
        "cpu": "400vCPU",
        "memory": "1024GB",
        "disk": "1000GB"
    }'

# start application
# your application is setup to start with pre-initialized capacity of 1 Spark driver and 1 Spark executor. Your application is by default configured to start when jobs are submitted and stop when the application is idle for more than 15 minutes.
aws emr-serverless start-application \
    --application-id $APPLICATION_ID

# submit hive job
aws emr-serverless start-job-run \
    --application-id $APPLICATION_ID \
    --execution-role-arn $JOB_ROLE_ARN \
    --job-driver '{
        "hive": {
            "initQueryFile": "s3://'${S3_BUCKET}'/code/hive/create_table.sql",
            "query": "s3://'${S3_BUCKET}'/code/hive/extreme_weather.sql",
            "parameters": "--hiveconf hive.exec.scratchdir=s3://'${S3_BUCKET}'/hive/scratch --hiveconf hive.metastore.warehouse.dir=s3://'${S3_BUCKET}'/hive/warehouse"
        }
    }' \
    --configuration-overrides '{
        "applicationConfiguration": [
            {
                "classification": "hive-site",
                "properties": {
                    "hive.driver.cores": "2",
                    "hive.driver.memory": "4g",
                    "hive.tez.container.size": "8192",
                    "hive.tez.cpu.vcores": "4"
                }
            }
        ],
        "monitoringConfiguration": {
            "s3MonitoringConfiguration": {
                "logUri": "s3://'${S3_BUCKET}'/hive-logs/"
            }
        }
    }'
```

## CloudFormation Support

[AWS::EMRServerless::Application](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html)

example `AWS::EMRServerless::Application` usage in cfn

- <https://github.com/aws-samples/emr-serverless-samples/blob/main/cloudformation/emr_serverless_spark_app.yaml#L6>
- <https://github.com/aws-samples/emr-serverless-samples/blob/main/cloudformation/emr_serverless_full_deployment.yaml#L61>

## AWS Console Screenshots

![](https://www.evernote.com/l/AAEj8OzU8ExBuqoCxCyUHu2FYNHsxHfbmZ0B/image.png)

![](https://www.evernote.com/l/AAH8fqtRIHlP6LCbGaVp9ngkM7SZXWXz-iMB/image.png)

![](https://www.evernote.com/l/AAH0lS5-luNKPLe90F9saH8sgYXDac8sdHoB/image.png)

![](https://www.evernote.com/l/AAHM7sq2O4NJbIvDO70SoQY9YAqMaDkfBrEB/image.png)

## Resources

- [EMR Serverless](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html)
- [Amazon EMR Serverless Now Generally Available – Run Big Data Applications without Managing Servers](https://aws.amazon.com/blogs/aws/amazon-emr-serverless-now-generally-available-run-big-data-applications-without-managing-servers/)
- [aws-samples/emr-serverless-samples](https://github.com/aws-samples/emr-serverless-samples)
- [AWS::EMRServerless::Application](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html)
- [Actions, resources, and condition keys for Amazon EMR Serverless](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonemrserverless.html)


