+++
author = "Brian Pfeil"
categories = ["aws"]
date = 2020-03-29T09:40:13-04:00
description = ""
draft = false
slug = "aws-services"
tags = ["aws"]
title = "AWS Services"
summary = "short descriptions for key AWS Services"

+++

> A quick reference for key AWS services and what they do

<!-- TOC -->

- [Networking and Content Delivery](#networking-and-content-delivery)
  - [VPC](#vpc)
  - [ELB/ALB](#elbalb)
  - [VPC Endpoint](#vpc-endpoint)
  - [Route 53](#route-53)
  - [Cloud Map](#cloud-map)
  - [Global Accelerator](#global-accelerator)
  - [CloudFront](#cloudfront)
  - [API Gateway](#api-gateway)
  - [AppSync](#appsync)
- [Compute](#compute)
  - [EC2](#ec2)
  - [ECS](#ecs)
  - [Fargate](#fargate)
  - [Batch](#batch)
  - [EKS](#eks)
  - [LightSail](#lightsail)
  - [Elastic Beanstalk](#elastic-beanstalk)
  - [Lambda](#lambda)
  - [Lambda@Edge](#lambdaedge)
- [Storage](#storage)
  - [S3](#s3)
  - [Glacier](#glacier)
  - [EFS (Elastic File System)](#efs-elastic-file-system)
  - [FSx for Windows File Server](#fsx-for-windows-file-server)
  - [EBS](#ebs)
  - [Transfer](#transfer)
- [Database](#database)
  - [DynamoDB](#dynamodb)
  - [DocumentDB (MongoDB compatibility)](#documentdb-mongodb-compatibility)
  - [RDS](#rds)
  - [Redshift](#redshift)
  - [ElastiCache](#elasticache)
  - [ElasticSearch](#elasticsearch)
  - [Neptune](#neptune)
  - [Timestream](#timestream)
  - [Cloud Directory](#cloud-directory)
  - [SSM Parameter Store](#ssm-parameter-store)
- [Application Integration](#application-integration)
  - [Step Functions](#step-functions)
  - [SNS](#sns)
  - [SQS](#sqs)
  - [EventBridge](#eventbridge)
  - [Kinesis](#kinesis)
- [Analytics](#analytics)
  - [Kinesis Data Analytics](#kinesis-data-analytics)
  - [Pinpoint](#pinpoint)
  - [EMR](#emr)
  - [Data Pipelines](#data-pipelines)
  - [Glue](#glue)
  - [Athena](#athena)
  - [QuickSight](#quicksight)
  - [Lake Formation](#lake-formation)
- [Management & Governance](#management--governance)
  - [Control Tower](#control-tower)
  - [Organizations](#organizations)
  - [CloudFormation](#cloudformation)
  - [Service Catalog](#service-catalog)
  - [Config](#config)
  - [CloudWatch Logs](#cloudwatch-logs)
    - [Resources](#resources)
  - [CloudWatch Events](#cloudwatch-events)
  - [CloudWatch Insights](#cloudwatch-insights)
  - [CloudWatch Metrics](#cloudwatch-metrics)
    - [Resources](#resources-1)
  - [CloudWatch Alarms](#cloudwatch-alarms)
  - [CloudTrail](#cloudtrail)
- [Developer Tools](#developer-tools)
  - [Cloud9](#cloud9)
  - [CodeCommit](#codecommit)
  - [CodeBuild](#codebuild)
  - [CodeDeploy](#codedeploy)
  - [CodePipeline](#codepipeline)
  - [X-Ray](#x-ray)
  - [Amplify](#amplify)
- [Machine Learning](#machine-learning)
  - [SageMaker](#sagemaker)
  - [Comprehend](#comprehend)
  - [Polly](#polly)
  - [Rekognition](#rekognition)
  - [Textract](#textract)
  - [Translate](#translate)
  - [Transcribe](#transcribe)
  - [Forecast](#forecast)
  - [Personalize](#personalize)
  - [Lex](#lex)
- [Security, Identity, and Compliance](#security-identity-and-compliance)
  - [IAM](#iam)
  - [Cognito](#cognito)
  - [Secrets Manager](#secrets-manager)
  - [WAF](#waf)
  - [Firewall Manager](#firewall-manager)
  - [Certificate Manager (ACM)](#certificate-manager-acm)
  - [KMS](#kms)
  - [Directory Service](#directory-service)

<!-- /TOC -->

---

## Networking and Content Delivery

### VPC

* virtual private cloud
* Subnets, route tables, internet gateways, elastic ips, nat gateways, network ACLs, security groups

### ELB/ALB

* elastic (TCP) | application load balancer (http layer 7)

### VPC Endpoint

* connect to AWS services from VPC without going through internet
* enables you to privately connect your VPC to supported AWS services and VPC endpoint services powered by PrivateLink without requiring an internet gateway, NAT device, VPN connection, or AWS Direct Connect connection
* gateway endpoint - S3 and DynamoDB.  via VPC route table.
    * gateway that you specify as a target for a route in your route table for traffic destined to a supported AWS service
* interface endpoint - all other services.  via DNS resolver for VPC/subnets
    * an elastic network interface with a private IP address from the IP address range of your subnet that serves as an entry point for traffic destined to a supported service

### Route 53

* managed DNS
* domain registration
* DNS / hosted zones
* Traffic Flow makes it easy for you to manage traffic globally through a variety of routing types, including Latency Based Routing, Geo DNS, Geoproximity, and Weighted Round Robin

### Cloud Map

* name and discover your cloud resources via API or DNS

### Global Accelerator

* uses the highly available and congestion-free AWS global network to direct internet traffic from your users to your applications on AWS
* fixed entry point to your applications through static IP addresses
* allocates static Anycast IP addresses that are globally unique for your application and do not change

### CloudFront

* CDN
* edge / PoP locations.  traffic over AWS global infrastructure
* [Restricting Access to Amazon S3 Content by Using an Origin Access Identity](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)

### API Gateway

* edge (cloudfront) and regional endpoints
* API Keys
* Usage Plans / quotas
* websockets
* custom domains

### AppSync

* GraphQL managed service
* integrates with Amazon DynamoDB, Amazon Elasticsearch, and Amazon Lambda
* Real-time subscriptions

---

## Compute

### EC2

### ECS

* containers

### Fargate

* containers
* run containers without having to manage servers or clusters

### Batch

* run batch computing jobs using containers
* concepts: Compute Environments (compute), Job Queues, Job Definitions (docker image), Jobs (things that run)

### EKS

* managed Kubernetes

### LightSail

* Virtual servers, storage, databases, and networking for a low, predictable price.
* backed by EC2, but easier to use
* similar to DigitalOcean

### Elastic Beanstalk

### Lambda

### Lambda@Edge

* feature of Amazon CloudFront that lets you run code closer to users of your application, which improves performance and reduces latency

---

## Storage

### S3

* object/blob storage

### Glacier

* low cost/long-term object/blob storage

### EFS (Elastic File System)

* elastic file system for Linux-based workloads for use with AWS Cloud services and on-premises resources.
* can mount as NFS v4
* e.g. shared file system.  many EC2 instances can mount same efs file system.

### FSx for Windows File Server

* fully managed native windows file system
* SMB, NTFS, AD integration

### EBS

* block level storage volumes for use with EC2 instances. EBS volumes behave like raw, unformatted block devices

### Transfer

* SFTP to S3
* enables the transfer of files directly into and out of S3 using SFTP

---

## Database

### DynamoDB

### DocumentDB (MongoDB compatibility)

### RDS

* Aurora, PostgreSQL, MySql, MariaDB, Oracle, SQL Sever

### Redshift

* managed data warehouse service

### ElastiCache

* redis and memcached

### ElasticSearch

### Neptune

* graph database. query languages Apache TinkerPop Gremlin and SPARQL (RDF)

### Timestream

* time series database
* InfluxDB, Prometheus, Riak

### Cloud Directory

* cloud-native directory that can store hundreds of millions of application-specific objects with multiple relationships and schemas

### SSM Parameter Store

* Systems Manager Parameter Store provides secure, hierarchical storage for configuration data management and secrets management

---

## Application Integration

### Step Functions

orchestration with many built-in integrations to aws services

### SNS

* pub/sub
* message filtering with subscription
* push notifications

### SQS

* managed message queuing service

### EventBridge

* pub/sub with many built-in integrations
* integrate with external SaaS or any custom application
* e.g. can log all events in account including CloudTrail to CloudWatch Log Group

### Kinesis

* collect, process, and analyze real-time, streaming data
* kafka alternative

---

## Analytics

### Kinesis Data Analytics

analyze streaming data with SQL

### Pinpoint

usage, customer, and engagement analytics

### EMR

hadoop, spark, and friends

### Data Pipelines

data processing workloads

> AWS Data Pipeline, you can regularly access your data where it’s stored, transform and process it at scale, and efficiently transfer the results to AWS services such as Amazon S3, Amazon RDS, Amazon DynamoDB, and Amazon EMR.

### Glue

* catalog / metadata (hive metadata catalog)
* crawlers autodiscover schema
* [py]spark and scala

### Athena

* query S3 data in place.  pay per query / data accessed.
* integrated with glue catalog
* Presto

### QuickSight

### Lake Formation

---

## Management & Governance

### Control Tower

set up and govern a new, secure multi-account AWS environment.  builders can provision new AWS accounts in a few clicks, while you have peace of mind knowing your accounts conform to your company-wide policies

### Organizations

* account management service that lets you consolidate multiple AWS accounts into an organization that you create and centrally manage.

### CloudFormation

* declarative provisioning of AWS infrastructure/resource

### Service Catalog

* create and manage catalogs of IT services that are approved for use on AWS
* concepts:
    * products are cloudformation templates
    * portfolio is collection of products
        * access to portfolios is via IAM users, groups, roles
    * IT administrator creates products and portfolios and grants access
    * End user accesses products and deploys them
* approved self-service products from Solution Factory
    * e.g. Oracle RDS DB with all security, tags, etc. in place
    * e.g. static web site. S3 + CloudFormation + WAF + ACM (certificate) + Route 53 (hosted zone, domain)

### Config

* AWS Config is a service that enables you to assess, audit, and evaluate the configurations of your AWS resources. Config continuously monitors and records your AWS resource configurations and allows you to automate the evaluation of recorded configurations against desired configurations.
* define rules that get evaluated when any change is made (e.g. resource provisioned)
* there are aws managed rules that are part of the service and you can define custom ones via lambda

### CloudWatch Logs

* centralize the logs from all of your systems, applications, and AWS services that you use, in a single, highly scalable service

#### Resources

* [CloudWatch Metric Filters](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html) - define custom metrics based on a pattern matched to log streams in a log group.
* [Simplified Time-Series Analysis with Amazon CloudWatch Contributor Insights](https://aws.amazon.com/blogs/aws/simplified-time-series-analysis-with-amazon-cloudwatch-contributor-insights/) - generate metrics from CWL data (JSON or CLF formats)

### CloudWatch Events

* cron triggers

### CloudWatch Insights

query log groups

### CloudWatch Metrics

* A metric represents a time-ordered set of data points that are published to CloudWatch

#### Resources

* [Building an Amazon CloudWatch Dashboard Outside of the AWS Management Console](https://aws.amazon.com/blogs/devops/building-an-amazon-cloudwatch-dashboard-outside-of-the-aws-management-console/) - display CloudWatch dashboard outside of AWS Console.  You specify the dashboard in JSON and it returns a binary image

### CloudWatch Alarms

* notify via email, SNS topics
* create a CloudWatch alarm that watches a single CloudWatch metric or the result of a math expression based on CloudWatch metrics
* An alarm watches a single metric over a specified time period, and performs one or more specified actions, based on the value of the metric relative to a threshold over time. The action is a notification sent to an Amazon SNS topic or an Auto Scaling policy. You can also add alarms to dashboards.

### CloudTrail

* logs all recording AWS API and Management Console actions to S3
* can query via Athena

---

## Developer Tools

### Cloud9

* cloud/browser based compute environment and IDE.
* dev machine (ec2 amzn linux) in the cloud with browser based IDE and terminal

### CodeCommit

* fully-managed source control service that hosts secure Git-based repositories

### CodeBuild

* continuous integration service that compiles source code, runs tests, and produces software packages
* like Jenkins, Travis, CircleCI

### CodeDeploy

* automates software deployments to a variety of compute services such as Amazon EC2, AWS Fargate, AWS Lambda, and your on-premises servers

### CodePipeline

* continuous delivery service that helps you automate your release pipelines
* orchestrates CodeBuild and CodeDeploy
* sources: github, CodeCommit, S3

### X-Ray

* distributed tracing
* instrument code
* similar to zipkin, jaeger

### Amplify

---

## Machine Learning

### SageMaker

* build, train, and deploy machine learning models

### Comprehend

* NLP (natural language processing)
* By utilizing NLP, you can extract important phrases, sentiment, syntax, key entities such as brand, date, location, person, etc., and the language of the text
* find insights and relationships in text
* use case e.g.: gauge whether customer sentiment is positive, neutral, negative, or mixed based on the feedback you receive via support calls, emails, social media, and other online channels

### Polly

* text-to-speech (TTS)
* supports MP3, Vorbis, and raw PCM audio stream formats
* Neural Text-to-Speech (NTTS) voices

### Rekognition

* API to analyze any image or video file
* identify the objects, people, text, scenes, and activities, as well as detect any inappropriate content.

### Textract

* extracts text and data from scanned documents
* supports PNG, JPEG, and PDF formats. For synchronous APIs, you can submit images either as an S3 object or as a byte array. For asynchronous APIs, you can submit S3 objects

### Translate

* neural machine translation service for translating text to and from English across a breadth of supported languages

### Transcribe

* audio to text
* transcription services for your audio files. It uses advanced machine learning technologies to recognize spoken words and transcribe them into text.

### Forecast

* managed deep learning service for time-series forecasting. By providing Amazon Forecast with historical time-series data, you can predict future points in the series. 

### Personalize

* create individualized recommendations for customers using their applications
* e.g. use cases
    * Personalized recommendations
    * Similar items
    * Personalized re-ranking i.e. re-rank a list of items for a user
    * Personalized promotions/notifications

### Lex

* conversational interfaces into any application using voice and text. Amazon Lex provides the advanced deep learning functionalities of automatic speech recognition (ASR) for converting speech to text, and natural language understanding (NLU) to recognize the intent of the text
* chat bots

---

## Security, Identity, and Compliance

### IAM

### Cognito

### Secrets Manager

### WAF

* web application firewall
* associate with CloudFront, ALB, API Gateway

### Firewall Manager

* centrally configure and manage firewall rules across accounts and applications (enterprise)
* e.g. create firewall manager policy that states all CloudFront and ALB instances across accounts must use a specific WebACL.
    * you can use tags to specify which CF and ALB instances to apply the RuleGroup to
* can automatically apply WebACL to CF and/or ALB instances or only notify "out of compliance"
* aws config must be enabled and running in each account.  this detects CF and ALB changes.


### Certificate Manager (ACM)

* provision, manage, and deploy public and private Secure Sockets Layer/Transport Layer Security (SSL/TLS) certificates for use with AWS services and your internal connected resources. 

### KMS

* key management service

### Directory Service

* provides multiple ways to set up and run Amazon Cloud Directory, Amazon Cognito, and Microsoft AD with other AWS services. Amazon Cloud Directory provides a highly scalable directory store for your application’s multihierarchical data. Amazon Cognito helps you create a directory store that authenticates your users either through your own user pools or through federated identity providers. AWS Directory Service for Microsoft Active Directory (Enterprise Edition), also known as Microsoft AD, enables your directory-aware workloads and AWS resources to use a managed Active Directory in the AWS Cloud.

