+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2021-03-13
description = ""
summary = " "
draft = false
slug = "amazon-managed-workflows-for-apache-airflow"
tags = []
title = "Amazon Managed Workflows for Apache Airflow"
repoFullName = "pfeilbr/amazon-managed-workflows-for-apache-airflow-playground"
repoHTMLURL = "https://github.com/pfeilbr/amazon-managed-workflows-for-apache-airflow-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/amazon-managed-workflows-for-apache-airflow-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/amazon-managed-workflows-for-apache-airflow-playground</a>
</div>


learn [Amazon Managed Workflows for Apache Airflow](https://docs.aws.amazon.com/mwaa/index.html)

## Install Steps

1. create S3 bucket with versioning enabled
2. create VPC - this is where RDS Postgres for airflow data lives, the airflow web UI runs in a container here
3. create aiflow environment

## Notes

* you create named MWAA environments and they each have own configuration
* airflow ui exposed publically or private within VPC
* login to [airflow ui with IAM user](https://docs.aws.amazon.com/mwaa/latest/userguide/access-airflow-ui.html)
* can create [web login token](https://docs.aws.amazon.com/mwaa/latest/userguide/access-airflow-ui.html#call-mwaa-apis-web) via AWS CLI
* upload DAG .py files to `dag` path in S3
* run DAGs via airflow cli, REST endpoint, boto3
* invoke [DAG via lambda](https://docs.aws.amazon.com/mwaa/latest/userguide/samples-lambda.html)
* install additional deps by providing requirements.txt
* auto scales up and down via Apache Celery Executor by adding / removing worker containers as needed
* scale via number of workers, and environment class

## Airflow

**Plugins**

* Hooks: Hooks are basically python modules that enables tasks to access external platform, like AWS, AZURE, GCP and many more.
* Sensors: Sensors are python modules which are used to create watcher tasks(in the most basic sense), for example s3Sensor is used to create s3 file watcher task. A sensor stays in running state till a specific state appears.
* Operators: Operators are typically execution engines. Operators are used to create task that execute some process, based on the type of Operator. For example: PythonOperator can be used create a task that will run a specific python method.

**XCom**

* share small bits of data between tasks
* stored in airflow postgres db

## Example Environment Attributes

```json
{
    "Environment": {
        "AirflowConfigurationOptions": {},
        "AirflowVersion": "1.10.12",
        "Arn": "arn:aws:airflow:eu-west-1:xxxxxxxxxxxx:environment/airflow-blogpost-dublin",
        "CreatedAt": 1610632127.0,
        "DagS3Path": "dags",
        "EnvironmentClass": "mw1.medium",
        "ExecutionRoleArn": "arn:aws:iam:: xxxxxxxxxxxx:role/airflow-demo-mwaa-eks-iamrole",
        "LastUpdate": {
            "CreatedAt": 1611137820.0,
            "Status": "SUCCESS"
        },
        "LoggingConfiguration": {
            "DagProcessingLogs": {
                "CloudWatchLogGroupArn": "arn:aws:logs:: xxxxxxxxxxxx:log-group:airflow-ricsue-dublin-DAGProcessing",
                "Enabled": true,
                "LogLevel": "INFO"
            },
            "SchedulerLogs": {
                "CloudWatchLogGroupArn": "arn:aws:logs:: xxxxxxxxxxxx:log-group:airflow-ricsue-dublin-Scheduler",
                "Enabled": true,
                "LogLevel": "INFO"
            },
            "TaskLogs": {
                "CloudWatchLogGroupArn": "arn:aws:logs:: xxxxxxxxxxxx:log-group:airflow-ricsue-dublin-Task",
                "Enabled": true,
                "LogLevel": "INFO"
            },
            "WebserverLogs": {
                "CloudWatchLogGroupArn": "arn:aws:logs:: xxxxxxxxxxxx:log-group:airflow-ricsue-dublin-WebServer",
                "Enabled": true,
                "LogLevel": "INFO"
            },
            "WorkerLogs": {
                "CloudWatchLogGroupArn": "arn:aws:logs:: xxxxxxxxxxxx:log-group:airflow-ricsue-dublin-Worker",
                "Enabled": true,
                "LogLevel": "INFO"
            }
        },
        "MaxWorkers": 5,
        "Name": "ricsue-dublin",
        "NetworkConfiguration": {
            "SecurityGroupIds": [
                "sg-0c88ef4755c295zzz"
            ],
            "SubnetIds": [
                "subnet-0493dffd0282f4xxx",
                "subnet-08f416023356ffyyy"
            ]
        },
        "RequirementsS3Path": "requirements/requirements.txt",
        "ServiceRoleArn": "arn:aws:iam:: xxxxxxxxxxxx:role/aws-service-role/airflow.amazonaws.com/AWSServiceRoleForAmazonMWAA",
        "SourceBucketArn": "arn:aws:s3:::airflow-mybucket",
        "Status": "AVAILABLE",
        "Tags": {},
        "WebserverAccessMode": "PUBLIC_ONLY",
        "WebserverUrl": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee.c5.eu-west-1.airflow.amazonaws.com",
        "WeeklyMaintenanceWindowStart": "SUN:14:00"
    }
}
```

## Resources

* [Amazon Managed Workflows for Apache Airflow](https://docs.aws.amazon.com/mwaa/index.html)
* [Interacting with Amazon Managed Workflows for Apache Airflow via the command line](https://dev.to/aws/interacting-with-amazon-managed-workflows-for-apache-airflow-via-the-command-line-4e91)
* [AWS CLI Command Reference | mwaa](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/mwaa/index.html)
* [Airflow — Custom Plugins](https://medium.com/swlh/airflow-custom-plugins-38f0848b74c5)
* [Airflow XCOM : The Ultimate Guide](https://marclamberti.com/blog/airflow-xcom/)



