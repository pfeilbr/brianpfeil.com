 +++
author = "Brian Pfeil"
categories = ["aws"]
date = 2020-03-29T09:40:13-04:00
description = "short descriptions for key AWS Services"
draft = false
slug = "aws-services"
tags = ["aws"]
title = "AWS Services"
summary = "short descriptions for key AWS Services"

+++

# AWS Services

The following services are commonly used for AWS solutions.  Each service specifies key considerations and features per service for architecture and design.

- [Serverless Services](#serverless-services)
- [Serverless Benefits](#serverless-benefits)
- [Relevant Patterns](#relevant-patterns)
- [Deployment Types](#deployment-types)
- [Networking and Content Delivery](#networking-and-content-delivery)
  - [VPC](#vpc)
  - [ELB/ALB](#elbalb)
  - [PrivateLink / VPC Endpoint](#privatelink--vpc-endpoint)
  - [Route 53](#route-53)
  - [Cloud Map](#cloud-map)
  - [Global Accelerator](#global-accelerator)
  - [CloudFront](#cloudfront)
  - [API Gateway](#api-gateway)
  - [AppSync](#appsync)
- [Compute](#compute)
  - [EC2](#ec2)
  - [ECS](#ecs)
  - [ECR](#ecr)
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
  - [Storage Gateway](#storage-gateway)
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
  - [AppFlow](#appflow)
  - [Step Functions](#step-functions)
  - [SNS](#sns)
  - [SQS](#sqs)
  - [SES](#ses)
  - [EventBridge](#eventbridge)
  - [Kinesis](#kinesis)
- [Analytics](#analytics)
  - [Kinesis Data Analytics](#kinesis-data-analytics)
  - [Pinpoint](#pinpoint)
  - [EMR](#emr)
  - [Data Pipelines](#data-pipelines)
  - [Glue](#glue)
  - [Glue DataBrew](#glue-databrew)
  - [Athena](#athena)
  - [QuickSight](#quicksight)
  - [Lake Formation](#lake-formation)
- [Management & Governance](#management--governance)
  - [Well-Architected Framework](#well-architected-framework)
  - [Control Tower](#control-tower)
  - [Organizations](#organizations)
  - [CloudFormation](#cloudformation)
  - [Serverless Application Repository (SAR)](#serverless-application-repository-sar)
  - [Service Catalog](#service-catalog)
  - [Config](#config)
  - [AppConfig](#appconfig)
  - [CloudWatch Logs](#cloudwatch-logs)
  - [CloudWatch Events (see EventBridge)](#cloudwatch-events-see-eventbridge)
  - [CloudWatch Insights](#cloudwatch-insights)
  - [CloudWatch Metrics](#cloudwatch-metrics)
  - [CloudWatch Alarms](#cloudwatch-alarms)
  - [CloudWatch Synthetics (Canaries)](#cloudwatch-synthetics-canaries)
  - [CloudTrail](#cloudtrail)
  - [Proton](#proton)
- [Developer Tools](#developer-tools)
  - [Cloud9](#cloud9)
  - [CodeCommit](#codecommit)
  - [CodeBuild](#codebuild)
  - [CodeDeploy](#codedeploy)
  - [CodePipeline](#codepipeline)
  - [CodeArtifact](#codeartifact)
  - [X-Ray](#x-ray)
  - [AWS CLI](#aws-cli)
  - [Amplify](#amplify)
  - [SAM (Serverless Application Model)](#sam-serverless-application-model)
  - [CDK](#cdk)
  - [AWS SDKs](#aws-sdks)
- [Migration & Transfer](#migration--transfer)
  - [AWS DataSync](#aws-datasync)
  - [AWS DMS (Database Migration Service)](#aws-dms-database-migration-service)
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
  - [Kendra](#kendra)
- [Security, Identity, and Compliance](#security-identity-and-compliance)
  - [IAM](#iam)
  - [Cognito](#cognito)
  - [Secrets Manager](#secrets-manager)
  - [WAF](#waf)
  - [Certificate Manager (ACM)](#certificate-manager-acm)
  - [KMS](#kms)
  - [Directory Service](#directory-service)
- [Media Services](#media-services)
  - [Amazon Interactive Video Service](#amazon-interactive-video-service)

## Serverless Services

- [Route53](#route53)
- [Global Accelerator](#global-accelerator)
- [WAF](#waf)
- [Cognito](#cognito)
- [CloudFront](#cloudfront)
- [API Gateway](#api-gateway)
- [AppSync](#appsync)
- [Amplify](#amplify)
- [Lambda](#lambda)
- [DynamoDB](#dynamodb)
- [S3](#s3)
- [SNS](#sns)
- [SQS](#sqs)
- [SES](#ses)
- [Kinesis](#kinesis)
- [EventBridge](#eventbridge)
- [Step Functions](#step-functions)
- [Athena](#athena)
- [SSM Parameter Store](#ssm-parameter-store)
- [Secrets Manager](#secrets-manager)
- [AppConfig](#appconfig)
- [AWS Config](#aws-config)
- [CloudWatch Synthetics (Canaries)](#cloudwatch-synthetics-canaries)
- [CloudWatch Metrics and Alarms](#cloudwatch-metrics-and-alarms)
- [CloudWatch Logs](#cloudwatch-logs)
- [CloudFormation](#cloudformation)
- [Serverless Application Repository (SAR)](#serverless-application-repository-sar)
- [SAM (Serverless Application Model)](#sam-serverless-application-model)
- [CDK](#cdk)
- [X-Ray](#x-ray)

## Serverless Benefits

* less things to own
* less/no ops
* costs - pay-per-use
* elastic / limits scaling concerns
* deliver value quicker
* scale teams / org fit
* durability/resiliency - services built-in replication across AZs or regions
* every service has soft limits for protection

---

## Relevant Patterns

* event sourcing
* circuit breaker - trip circuit to prevent downstream systems overload
* load shedding - prevent backlog buildup
* handle poison messages - prevent kinesis and dynamo streams from progressing
* prevent distributed transactions.  e.g. lambda send job to SQS and stores status in dynamodb.  break it up.  lambda put job status in dynamo -> dynamo stream -> lambda send job to SQS
* strangler - migrate from monolith to serverless.  e.g. DB - run RDS and dynamodb in parallel and update both for a period of time

---

## Deployment Types

* all-at-once
* blue/green
* canary - traffic shift percentages with metrics
* linear - changing the amount of traffic split to the new version incrementally according to a percentage that is provided when configured.

---

## Networking and Content Delivery

### VPC

* virtual private cloud
* Subnets, route tables, internet gateways, elastic ips, nat gateways, network ACLs, security groups, prefix lists

### ELB/ALB

* Elastic Load Balancing (TCP)

* ALB application load balancer  — Layer 7 (HTTP/HTTPS traffic), Flexible
* NLB network load balancer — Layer 4 (TLS/TCP/UDP traffic), Static IPs
* CLB classic load balancer — Layer 4/7 (HTTP/TCP/SSL traffic), Legacy, Avoid

* The NLB forwards requests whereas the ALB examines the contents of the HTTP request header to determine where to route the request. So, the ALB is performing content based routing.

### PrivateLink / VPC Endpoint

* connect to AWS services from VPC without going through internet
* enables you to privately connect your VPC to supported AWS services and VPC endpoint services powered by PrivateLink without requiring an internet gateway, NAT device, VPN connection, or AWS Direct Connect connection
* gateway endpoint - S3 and DynamoDB.  via VPC route table.
    * gateway that you specify as a target for a route in your route table for traffic destined to a supported AWS service
* interface endpoint - all other services.  via DNS resolver for VPC/subnets
    * an elastic network interface with a private IP address from the IP address range of your subnet that serves as an entry point for traffic destined to a supported service

### Route 53

* managed DNS
* main service for reliability / DR
* public and private domains (hosted zones)
* route to aws services - CloudFront, API Gateway, ELB, RDS, S3 bucket, EC2, VPC Interface Endpoint
* record sets, TTL
* health checks
* load balancing via DNS
* routing policies - latency Based Routing, Geo DNS, Geoproximity, and Weighted Round Robin
* domain registration
* geo routing, geoproximity routing
* alias record type (aws specific.  used for root/bare/naked domains)
* [AWS Route53 — Cheat Sheet(In 2 Minutes)](https://medium.com/@kumargaurav1247/aws-route53-cheat-sheet-in-2-minutes-ada9b7f0fcb)

### Cloud Map

* name and discover your cloud resources via API or DNS

### Global Accelerator

* uses the highly available and congestion-free AWS global network to direct internet traffic from your users to your applications on AWS
* fixed entry point to your applications through static IP addresses
* allocates static Anycast IP addresses that are globally unique for your application and do not change

### CloudFront

* CDN
* POP / edge servers - traffic over AWS global infrastructure
* price classes
* ACM for TLS/SSL certs
* cache policies.  cookie, headers, querystring, TTLs configs
* [origin access identity](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)
* origin custom headers
* signed URLs or cookies
* origin groups - primary origin and a second origin to failover to
* custom error responses - http error codes mapped to response page paths
* georestrictions
* lambda@edge - headers only requests, rewrite URLs, server-side rendering (SSR), auth, etc.
* cache invalidations
* non GET HTTP methods support.  must explicitly turn on support for PUT, POST, PATCH, etc.
* WAF association
* can point to Object Lambda Access Point

### API Gateway

* REST API vs HTTP API (cost).  see [Choosing between HTTP APIs and REST APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html)
* edge (cloudfront) and regional endpoints
* API Keys
* caching (memcached) (fixes cost based on time / no pay per use)
* API Keys
* Usage Plans / quotas
* client certificates - ensure requests to backend are from APIG
* throttles
* with WAF in front, you can set up rate-based rules to specify the number of web requests that are allowed by each client IP in a trailing, continuously updated, 5-minute period.  *no API Key required for this*
* timeout - 29s
* request (POST) payload limits (10 MB).  no response size limits. (tested with proxy integration for 200 MB video file download)
* auth - cognito, JWT, IAM (aws sigv4), custom lambda auth
* OpenAPI / Swagger specs for payload validation
* service integrations - no need for lambda glue in middle
* velocity templates (vtl) - request/response mapping
* custom domains
* private endpoints
* websockets
* lambda integration.  point to lambda alias for deployments.
* stages
* mock integrations / responses

### AppSync

* GraphQL managed service
* integrates with Amazon DynamoDB, Amazon Elasticsearch, and Amazon Lambda
* resolvers
* resolver mapping templates via velocty (vtl)
* Real-time subscriptions
* aws specific graphql schema [`@directives`](https://docs.amplify.aws/cli/graphql-transformer/directives) for model (ddb), auth (cognito),
* GraphiQL
* javascript for vtl coming (2021-03-28)

---

## Compute

### EC2

* AMI
* elastic IPs
* ASGs (launch templates)
* UserData - script to run on instance start
* EC2 metadata service

### ECS

* containers
* task definitions
* EFS or EBS for persistent storage
    * EFS is recommended.  Can be mounted by multiple ECS tasks for parallel access
    * EBS can be used but is tied to un hosting EC2 instance. No fargate.

### ECR

* container registry
* concepts
    * Registry - can create image repositories in your registry and store images in them
    * Authorization token - client must authenticate to Amazon ECR registries as an AWS user before it can push and pull images
    * Repository - contains your Docker images, Open Container Initiative (OCI) images, and OCI compatible artifacts
    * Repository policy - can control access to your repositories and the images within them with repository policies
    * Image - push and pull container images to your repositories
        * can use them in ECS task definitions and EKS pod specifications
* ECR public
* resource-based permissions using AWS IAM
*

### Fargate

* containers
* task definitions
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

* PaaS with language runtime + docker containers
* heroku-like

### Lambda

* synchronous vs asynchronous vs poll based/stream processing (poll based is sync. via event-source mappings)
* memory - single knob for memory and CPU
* DLQ
* lambda destinations (only for async invokes)
* reserved concurrency - concurrency allocated for a specific function. e.g. i always want fn X to be able to run 10 lambda invokes concurrently
* provisioned concurrency - pre-warmed lambda instances / no cold starts.  good for latency sensitive needs
    * can optionally use auto scaling to adjust on based on metrics and/or schedule.
    * will spill over to on-demand scaling (lambda default)
    * Provisioned Concurrency comes out of your regional concurrency limit
* concurrent executions (throttles) - 1000 per account
* timeout - 15min
    * set code timeouts based on remaining invocation time provided in context
* burst concurrency - 500 - 3000
* burst - 500 new instances / min
* poll based options (kinesis, dynamodb, SQS)
    * on-failure destination (SNS or SQS)
    * retry attempts
    * max age of record - use to implement load shedding (prioritize newer messages)
    * split batch on error
    * concurrent batches per shard
* APIG -> lambda
* ALB -> lambda
* service integrations - [Using AWS Lambda with other services - AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html)
* [lambda private endpoints](https://aws.amazon.com/blogs/aws/new-use-aws-privatelink-to-access-aws-lambda-over-private-aws-network/) - access lambda from VPC without going over internet
* [Lambda Extensions](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-extensions-api.html) - executables in /opt/extensions that conform to the [Lambda Extensions API](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-extensions-api.html)
* [Container Images](https://docs.aws.amazon.com/lambda/latest/dg/lambda-images.html)
  * [Runtime interface clients](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-images.html#runtimes-api-client)
    * runtime interface client in your container image manages the interaction between Lambda and your function code
    * Lambda provides an open source runtime interface client for each of the supported Lambda runtimes. e.g. node.js, python, etc.
  * [Lambda Runtime Interface Emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator/)
    * allows customers to locally test their Lambda function packaged as a container image
    * web-server that converts HTTP requests to JSON events and maintains functional parity with the Lambda Runtime API
  * max image size: 10 GB
* [AWS Lambda Operator Guide](https://docs.aws.amazon.com/lambda/latest/operatorguide/intro.html)
### Lambda@Edge

* feature of Amazon CloudFront that lets you run code closer to users of your application, which improves performance and reduces latency

---

## Storage

### S3

* object/blob storage
* versioned buckets
* presigned URLs for private content (download or upload)
* [S3 batch operations](https://docs.aws.amazon.com/AmazonS3/latest/dev/batch-ops-basics.html)
* S3 select
* [batch operations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/batch-ops-basics.html) - perform operation on list of objects specified in manifest.  e.g. lambda, copy, etc.
* storage classes
* lifecycle rules - moving between storage tiers for cost savings
* access points - managing data access at scale, access points are unique hostnames, enforce distinct permissions and network controls for any request made through the access point, scale to many applications accessing bucket with own set of permissions.
    * addresses pain point- Managing access to this shared bucket requires a single bucket policy that controls access for dozens to hundreds of applications with different permission levels
    * [Multi-Region access points](https://aws.amazon.com/blogs/aws/s3-multi-region-access-points-accelerate-performance-availability/)
* S3 event notifications - notification destinations are SNS, SQS, lambda
* replication - cross-region, same-region
* [S3 object lambda](https://aws.amazon.com/blogs/aws/introducing-amazon-s3-object-lambda-use-your-code-to-process-data-as-it-is-being-retrieved-from-s3/) - process data retrieved from S3 with lambda before returning it to an application. lambda calls [`writeGetObjectResponse`](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/S3.html#writeGetObjectResponse-property) to send modified object contents back to `GET` request.  Create S3 Access Point, then Object Lambda Access Point.

### Glacier

* low cost/long-term object/blob storage

### EFS (Elastic File System)

* elastic file system for Linux-based workloads for use with AWS Cloud services and on-premises resources.
* can mount as NFS v4
* e.g. shared file system.  many EC2 instances can mount same efs file system.
* can mount to lambda local filesystem

### FSx for Windows File Server

* fully managed native windows file system
* SMB, NTFS, AD integration

### Storage Gateway

* NFS or SMB interface to S3, FSx, volume/tape gateways
* compute runs on once of following: ec2, kvm, VMware, Hyper-V, or appliance
* if SMB, need to [Configuring Microsoft Active Directory access](https://docs.aws.amazon.com/filegateway/latest/files3/CreatingAnSMBFileShare.html#configure-SMB-file-share-AD-access)
* VPC support.  network traffic between compute and AWS Service goes over VPC endpoint
* VPC endpoint enabled, all VPC endpoint communication from your gateway to AWS services occurs through the public service endpoint using your VPC in AWS
* Creating a VPC endpoint for Storage Gateway
### EBS

* block level storage volumes for use with EC2 instances. EBS volumes behave like raw, unformatted block devices

### Transfer

* SFTP to S3
* enables the transfer of files directly into and out of S3 using SFTP

---

## Database

### DynamoDB

* concepts - tables, items, queries, scans, indexes
* global tables - for resilient active-active architectures
* DAX - DynamoDB Accelerator - in memory cache in front
* GSI (Global Secondary Indexes), LSI (Local Secondary Indexes)
* transactions
* throttles
* point-in-time recovery (PITR)
* streams - 24hr data retention.  poison messages (retry until success - can cause backlog)
* partition key - distribute data among nodes to minimize hot partitions
* TTL - can the data be removed automatically
* parallelization factor for DDB streams processed by lambda
* single table designs
* fine grained item (`dynamodb:LeadingKeys`) and attribute level IAM (`dynamodb:Attributes`).  enables multi-tenant isolation.
* [Amazon DynamoDB Encryption Client](https://docs.aws.amazon.com/dynamodb-encryption-client/latest/devguide/what-is-ddb-encrypt.html)
* [PartiQL - A SQL-Compatible Query Language for Amazon DynamoDB - Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html)
* [dynamodb table export to s3](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DataExport.html)

### DocumentDB (MongoDB compatibility)

### RDS

* Aurora, PostgreSQL, MySql, MariaDB, Oracle, SQL Sever
* DB Instance (contains 1 or more dbs), Instance Classes (compute+memory), Instance Storage
* HA Multi-AZ

### Redshift

* managed data warehouse service
* RA3 instances - Scale compute and storage independently for fast query performance and lower costs
* UDFs - lambda backed

### ElastiCache

* managed redis and memcached

### ElasticSearch

* cluster
* kibana - integrated with IAM
* IAM for granular es api operations

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

### AppFlow

* managed integration (ETL) service
* securely transfer data between SaaS applications (Salesforce, Marketo, Slack, etc.), and AWS services (S3, Redshift, EventBridge, etc.)
* concepts - flow, source, destination, flow trigger (on demand, event, schedule), map fields from source to destination (formula transforms, value validations), filters (determine records to transfer)
* Flow notifications - flow start|complete|deactivated events sent to CloudWatch Events/EventBridge (`"source": "aws.appflow"`)
* security
    * encryption at rest - connection data stored in secrets manger using AWS managed or Customer managed CMK
    * Encryption in Transit (TLS 1.2) - choose either an AWS managed CMK or a customer managed CMK. When executing a flow, Amazon AppFlow stores data temporarily in an intermediate S3 bucket and encrypts it using this key. This intermediate bucket is deleted after 24 hours, using a bucket lifecycle policy.
* [Actions defined by Amazon AppFlow](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonappflow.html#amazonappflow-actions-as-permissions)

### Step Functions

* Standard Workflows vs Express Workflows
* orchestration with many built-in integrations to aws services
* [Step Functions AWS SDK Service Integrations](https://aws.amazon.com/blogs/aws/now-aws-step-functions-supports-200-aws-services-to-enable-easier-workflow-automation/)
* saga pattern for rollback
* parallel map opportunities - run tasks in parallel
* [service integrations](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html#welcome-integrations) - request/response, run a job (`.sync`), callback with task token (`.waitForTaskToken`)

### SNS

* pub/sub
* message filtering with subscription
* push notifications
* standard topic
    * at least once delivery
    * best effort ordering - ensure downstream consumers are idempotent
* FIFO topic
    * strict ordering
    * Strict deduplication: Duplicate messages aren't delivered.
    * Deduplication happens within a 5-minute interval, from the message publish time.
* fan out
* subscription filters
* destination types
    * SQS
    * lambda
    * http/s
    * mobile push notifications
    * SMS messages
    * email
* DLQ configuration
* KMS encryption

### SQS

* managed message queuing service
* batch size - batch fails as unit
* visibility timeout - set to 6x lambda timeout
* message retention period
* delivery delay - max 15min
* types - standard vs FIFO
    * standard - at least once delivery.  need to ensure idempotent
    * FIFO - strict ordering.  exactly-once processing
* alarm on queue depth
* KMS encryption
* [DLQ](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html) for redrive for messages that can't be delivered to target SQS queue

### SES

* send or receive emails
* verify domain (DNS txt) and/or email addresses (confirmation email) - verify that you own the email address or domain that you plan to send from
* understand [Service quotas](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/quotas.html)
* max message size - 10 MB per message (after base64 encoding).
* sending identity - domain or an email address
* send emails via SMTP or API (AWS CLI, [AWS SDK](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/SES.html#sendEmail-property))
* connect to a URL that provides an endpoint for the Amazon SES API or SMTP interface (e.g. email-smtp.us-east-1.amazonaws.com:587)
* DKIM support - DKIM works by adding a digital signature to the headers of an email message. This signature can then be validated against a public cryptographic key that is located in the organization's DNS record
* SPF support - SPF establishes a method for receiving mail servers to verify that incoming email from a domain was sent from a host authorized by that domain’s administrators
* IAM to control user access to email sending (e.g. `ses:SendEmail`)
* Configuration sets - groups of rules that you can apply to the emails you send using Amazon SES.  can publish email sending events to CWL, Firehose, SNS
* Event types - Send, Reject, Delivery, Bounce, Complaint, Click  Open  Rendering Failure
* store inbound emails in S3
* trigger lambdas based on inbound emails
* publish your email sending events to CWLs or kinesis firehose
* Sending personalized email via email templates.  templates contain placeholder values.  based on Handlebars template system
* list management
    * customers can manage their own mailing lists, known as contact lists.
    * can create topics, associate topic preferences to a contact and specify `OPT_[IN|OUT]` for the topic.
* Global Suppression List
    * includes a global suppression list. When any Amazon SES customer sends an email that results in a hard bounce, Amazon SES adds the email address that produced the bounce to a global suppression list. The global suppression list is global in the sense that it applies to all Amazon SES customers. In other words, if a different customer attempts to send an email to an address that's on the global suppression list, Amazon SES accepts the message, but doesn't send it, because the email address is suppressed.
    * enabled by default for all Amazon SES accounts. You can't disable it.
* reputation dashboard to track bounce and complaint rates
* Dedicated IP Addresses
* IP pool management – If you lease dedicated IP addresses to use with Amazon SES, you can create groups of these addresses, called dedicated IP pools. You can then associate these dedicated IP pools with configuration sets
* SES sandbox - all new accounts.
    * only send mail to verified email addresses and domains
    * only send mail from verified email addresses and domains
    * send a maximum of 200 messages per 24-hour period
    * send a maximum of 1 message per second
* need to [request production access](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html?icmpid=docs_ses_console) to move out of sandbox
* VPC endpoint support - see [New – Amazon Simple Email Service (SES) for VPC Endpoints](https://aws.amazon.com/blogs/aws/new-amazon-simple-email-service-ses-for-vpc-endpoints/)

### EventBridge

* pub/sub with many built-in integrations
* integrate with external SaaS or any custom application
* bus-to-bus routing within same account + region, x-account, and x-region.
* dlq for eb rules.  if fails to deliver to target, goes in sqs queue
* e.g. can log all events in account including CloudTrail to CloudWatch Log Group
* put events - 2400 requests per second per region
* AWS service rule [targets](https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-targets.html)
* at-least-once event delivery to targets (ensure idempotent behavior)
* no ordering guarantees
* [schema registry](https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-schemas.html) - helps with managing and versioning event schemas for evolution.  Codegen code for handling events in various languages.  can auto discover schemas by observing events on the bus.  based on json schema
* invocation quota -  4500 requests per second per region (invocation is an event matching a rule and being sent on to the rule’s targets)
* DLQ
* EventBridge resource policies
* archive and replay events
* IAM - resource-based and identity-based policies.  owner of EB resources (bus, rules, etc.) is an AWS root account.
* supports sending and recieving events across accounts
* [SaaS Partner Integrations](https://docs.aws.amazon.com/eventbridge/latest/userguide/create-partner-event-bus.html)

### Kinesis

* collect, process, and analyze real-time, streaming data
* kafka alternative
* partition key
* shard count
* ordering guaranteed for messages per shard
* [dynamic partitioning](https://aws.amazon.com/about-aws/whats-new/2021/08/introducing-dynamic-partitioning-amazon-kinesis-data-firehose/) - continuously partition streaming data in Kinesis Data Firehose using keys within data like “customer_id” or “transaction_id” and deliver data grouped by these keys into corresponding Amazon Simple Storage Service (Amazon S3) prefixes
* lambda - lambda polls per shard
    * batch size
    * batch window
    * parallelization factor
        * Concurrent batches per shard – Process multiple batches from the same shard concurrently.
    * enhanced fan-out via AWS::Kinesis::StreamConsumer.  each consumer gets 2 MiB per second for every shard you subscribe to.  can subscribe a max of 5 consumers per stream.
    * Starting position - Latest, Trim horizon, At timestamp
    * On-failure destination
    * Retry attempts
    * Maximum age of record – The maximum age of a record that Lambda sends to your function.
    * Split batch on error
* poison messages (retry until success - can cause backlog)
* KMS
* aggregate multiple records into one while staying under size limits to increase throughput. see <https://github.com/awslabs/kinesis-aggregation>
* no autoscaling around shards.  requires management/ops.  consider SQS first as there's less to manage and see if it can meet the need

---

## Analytics

### Kinesis Data Analytics

analyze streaming data with SQL

* real-time analysis
* supports SQL applications (aws specific) and apache flink applications
* concepts - application, input steam -> application code (SQL statements) -> output stream
* time based windows.  tumbling windows.
* pump

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
* data sources - S3, RDS, JDBC, dynamodb, mongodb, documentdb
* data targets - S3, RDS, JDBC, mongodb, documentdb
* jobs
* job types - Spark, Streaming ETL (kinesis, kafka via spark structured streaming (micro batches)), and Python shell
    * python shell job start-up time - 7-30 secs (based on usage observations)
* languages - [py]spark and scala
* concepts - Data Catalog, Classifier, Connection, Crawler, Database, Table, Dynamic Frame (extend spark RDD), Job, Transform, Trigger (time based or event)
* glue notebook (Jupyter/Zeppelin) - interactive development and testing of your ETL scripts on a development endpoint
* partitions
* AWS Data Wrangler - excellent integration library to use with glue via python shell jobs

### Glue DataBrew

* visual data preparation service
* extract, clean, normalize, transform, combine, data at scale
* target audience: non-technical Data Analyst
* serverless.  pay for what you use
* concepts
  * datasets
  * recipes - steps to apply/take on dataset
  * job - recipe + dataset run
  * project - visual workspace for working with data interactively.  can apply changes and visually see the results in UI.  you specify a sampling of the data to work with.

![](https://www.evernote.com/l/AAG7ZKzRRblBGakFLIWEBGTrsChbY2sRNlkB/image.png)

### Athena

* serverless querying of S3 data
* federated query - run SQL queries across data stored in relational, non-relational, object, and custom data sources.
* CTAS - create table as select
* query S3 data in place.  pay per query / data accessed.
* integrated with glue catalog
* Presto is underlying tech

### QuickSight

### Lake Formation

---

## Management & Governance

### Well-Architected Framework

* describes the key concepts, design principles, and architectural best practices for designing and running workloads in the cloud
* 5 pillars - Operational Excellence, Security, Reliability, Performance, Cost Optimization
* Well-Architected Tool - provides guidance by answer questions
* Lens - serverless, analytics, ML, SaaS, etc.

### Control Tower

set up and govern a new, secure multi-account AWS environment.  builders can provision new AWS accounts in a few clicks, while you have peace of mind knowing your accounts conform to your company-wide policies

### Organizations

* account management service that lets you consolidate multiple AWS accounts into an organization that you create and centrally manage.

### CloudFormation

* declarative provisioning of AWS infrastructure/resource
* parameters, mappings, conditionals
* intrinsic functions
* nested stacks
* stack drift
* stacksets - deploy stack to multiple regions.  For DR, active-active, etc.
* max resources declared in stack (500)
* [custom resources]
(https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) - backed by lambda
* [macros](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-macros.html) - lambda performs the template processing / transform
* modules - package resource configurations for inclusion across stack templates, in a transparent, manageable, and repeatable way

### Serverless Application Repository (SAR)

> enables teams, organizations, and individual developers to find, deploy, publish, share, store, and easily assemble serverless architectures

* any cfn can be used for SAR app
* iam for access to SAR app

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
* Service Actions - enable end users to perform operational tasks, troubleshoot issues, run approved commands, or request permissions in AWS Service Catalog via SSM docs.

### Config

* monitor, notify, quarantine, remediate based on resource changes.
* RDK - rule development kit.  Config triggers lambda on resource changes.
* AWS Config is a service that enables you to assess, audit, and evaluate the configurations of your AWS resources. Config continuously monitors and records your AWS resource configurations and allows you to automate the evaluation of recorded configurations against desired configurations.
* define rules that get evaluated when any change is made (e.g. resource provisioned)
* conformance - collection of Config rules and remediation actions. portable.  can be applied across multiple accounts and regions
* there are aws managed rules that are part of the service and you can define custom ones via lambda

### AppConfig

* feature flags, Update applications without interruptions, Control deployment of changes across your application
* a capability of AWS Systems Manager, to create, manage, and quickly deploy application configurations. AppConfig supports controlled deployments to applications of any size and includes built-in validation checks and monitoring. You can use AppConfig with applications hosted on EC2 instances, AWS Lambda, containers, mobile applications, or IoT devices.
* JSON Schema Validators - ensure that new or updated configuration settings conform to the best practices required by your application
* e.g. a JSON doc with application configuration can be sourced from S3, parameter store

### CloudWatch Logs

* centralize the logs from all of your systems, applications, and AWS services that you use, in a single, highly scalable service
* concepts - log groups, log streams
* subscriptions - real-time feed of log events from CloudWatch Logs (Kinesis `[stream|firehose]`, elasticsearch, Lambda)
* [Creating Metrics From Log Events Using Filters](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/MonitoringLogData.html)
* encrypt with KMS

### CloudWatch Events (see [EventBridge]())

* cron triggers

### CloudWatch Insights

* query log groups
* [CWL Query Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)

### CloudWatch Metrics

* time series data
* metric - time-ordered set of data points that are published to CloudWatch
* concepts - namespace, dimensions (name/value pairs), units (Bytes, Seconds, Count, and Percent), time stamp, resolution (granularity)
* statistics - sum, max, min, average, sample count, percentile (pNN) (metric data aggregations over specified periods of time)
* metrics retention
* Dashboards - for Visualizations
* [Creating Metrics From Log Events Using Filters](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/MonitoringLogData.html)
* [Embedded Metric Format](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Generation.html) - generate metrics from structured (json) log messages


### CloudWatch Alarms

* notify via email, SNS topics
* create a CloudWatch alarm that watches a single CloudWatch metric or the result of a math expression based on CloudWatch metrics
* An alarm watches a single metric over a specified time period, and performs one or more specified actions, based on the value of the metric relative to a threshold over time. The action is a notification sent to an Amazon SNS topic or an Auto Scaling policy. You can also add alarms to dashboards.
* composite alarms
* Alarm States - OK, ALARM, INSUFFICIENT_DATA (missing data points)

### CloudWatch Synthetics (Canaries)

*  supports monitoring your REST APIs, URLs, and website content every minute, 24x7, and alerts you when your application endpoints don’t behave as expected.
* Node.js or python based.  bundles in Puppeteer + Chromium to the runtime
* can also used in any workloads requiring general browser automation
* creates several CloudWatch metrics in `CloudWatchSynthetics` namespace
* CloudFormation support via [`AWS::Synthetics::Canary`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html)

> create canaries, configurable scripts that run on a schedule, to monitor your endpoints and APIs. Canaries follow the same routes and perform the same actions as a customer, which makes it possible for you to continually verify your customer experience even when you don't have any customer traffic on your applications. By using canaries, you can discover issues before your customers do.

### CloudTrail

* logs all recording AWS API and Management Console actions to S3
* can query via Athena

### Proton

* self-serve for platform enabling teams
* enables the standardization of cross cutting concerns for microservices based solutions (composition of many microservices).
* e.g. the following is needed for each microservice and should be consistent/aligned with standards and best practices: compute, DNS, load balancing, code deployment pipeline, monitoring and alarms
* similar goals as [Netflix's Spinnaker](https://spinnaker.io/)

k8s ecosystem

---

## Developer Tools

### Cloud9

* cloud/browser based compute environment and IDE.
* dev machine (ec2 amzn linux) in the cloud with browser based IDE and terminal

### CodeCommit

* fully-managed source control service that hosts secure Git-based repositories

### CodeBuild

* managed build service
* provides prepackaged build environments
* continuous integration service that compiles source code, runs tests, and produces software packages
* like Jenkins, Travis, CircleCI
* concepts - build project - environment (linux/windows, container image to use, etc.),
* [`buildspec.yml`](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html) - phases, env vars, artifacts
* can be used to run ad-hoc workloads over lambda when need to run longer than 15 min

### CodeDeploy

* automates software deployments to a variety of compute services such as Amazon EC2, AWS Fargate, AWS Lambda, and your on-premises servers

### CodePipeline

* continuous delivery service that helps you automate your release pipelines
* orchestrates CodeBuild and CodeDeploy
* sources: github, CodeCommit, S3

### CodeArtifact

* fully managed software artifact repository service that makes it easy for organizations of any size to securely store, publish, and share packages used in their software development process
* artifactory competitor

### X-Ray

* distributed tracing
* instrument code
* similar to zipkin, jaeger

### AWS CLI

* `~/.aws/[config|credentials]`
* `--generate-cli-skeleton` - e.g. `aws codebuild start-build --generate-cli-skeleton > build.json` -> `aws codebuild start-build --cli-input-json file://start-build.json`

### Amplify

* CLI to provision resources (Auth (cogntio), API (API Gateway), GraphQL (AppSync), Storage (S3, DynamoDB))
* client-side javascript/typescript, iOS, Android libraries and UI components
* Amplify Console.  CI/CD static site hosting.

### SAM (Serverless Application Model)

* higher-level cfn resource types (transformed via cfn macro on backend)
* SAM CLI
* local development features via docker (apig endpoint

### CDK

* express resources using general purpose programming languages (ts/js/python/java/C#)
* constructs - cfn (L1), CDK (L2), pattern/solution (L3)
* synth to cfn
* cloud assemblies - cfn + source code, docker images, assets (s3)
* aspects - ability to visit each node/resource in stack and apply changes
* Application -> Stacks -> Constructs
* [Runtime context](https://docs.aws.amazon.com/cdk/latest/guide/context.html#context_example)
* `[tf|k8s]` CDKsnc
* jsii - core/foundational tech for multi-language/polyglot support.  bind any language to underlying typescript implementation.
* CDK pipelines for CI/CD

### AWS SDKs

* built in retries, timeouts
* can configure timeouts (e.g. `AWS.config.update({maxRetries: 2, httpOptions: { timeout: 2 * 1000, connectTimeout: 3 * 1000, },})`)

---

## Migration & Transfer

### AWS DataSync

copy data between NFS, SMB, S3, EFS, FSx

**concepts**

* transfer types
  * Data transfer between self-managed storage and AWS
    * need to install an agent that can access self-managed storage
  * Data transfer between AWS storage services
    * no need to install an agent

* agent
  * VM that runs the sync software.
  * can run on EC2 or hypervisors (VMware ESXi, KVM, and Microsoft Hyper-V hypervisors)


* scheduled transfers

Data transfer between self-managed storage and AWS

![](https://docs.aws.amazon.com/datasync/latest/userguide/images/DataSync-chart-on-prem.png)

Data transfer between AWS storage services

![](https://docs.aws.amazon.com/datasync/latest/userguide/images/DataSync-chart-agentless.png)

[![image](https://www.awsgeek.com/AWS-DataSync/AWS-DataSync.jpg)](https://www.awsgeek.com/AWS-DataSync/)
### AWS DMS (Database Migration Service)

- migrate RDBS, data warehouses, nosql dbs, etc. in cloud, between combos of cloud and on-prem
- it's a server (EC2) in the cloud that runs replication software (replication engine).  [DMS replication instance types](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_ReplicationInstance.Types.html)
- create source and target connections
- schedule task on server to move data
- pay-as-you-go model
- data at rest is encrypted
- SSL / TLS encrypts data in -flight
- HA with multi-AZ deployment
- can provision DMS resources using CloudFormation.
- migration types: one-time, ongoing replication (CDC)
- AWS DMS doesn't perform schema or code conversion
	- you can use the AWS Schema Conversion Tool (AWS SCT)
- create endpoints to access source or target data store.
- endpoint properties
	- Endpoint type – Source or target.
	- Engine type – Type of database engine, such as Oracle or PostgreSQL..
	- Server name – Server name or IP address that AWS DMS can reach.
	- Port – Port number used for database server connections.
	- Encryption – Secure Socket Layer (SSL) mode, if SSL is used to encrypt the connection.
	- Credentials – User name and password for an account with the required access rights.
- At a high level, when using AWS DMS you do the following:
  - Create a replication server.
  - Create source and target endpoints that have connection information about your data stores.
  - Create one or more migration tasks to migrate data between the source and target data stores.
- A replication task can consist of three major phases:
  - The full load of existing data
  - The application of cached changes
  - Ongoing replication
- > At the start of the ongoing replication phase, a backlog of transactions generally causes some lag between the source and target databases. The migration eventually reaches a steady state after working through this backlog of transactions.
- > If your migration is heterogeneous (between two databases that use different engine types), you can use the AWS Schema Conversion Tool (AWS SCT) to generate a complete target schema for you.
- Depending on the Amazon EC2 instance class you select, your replication instance comes with either 50 GB or 100 GB of data storage
- public and private replication instances
	- You use a private instance when both source and target databases are in the same network that is connected to the replication instance's VPC. The network can be connected to the VPC by using a VPN, AWS Direct Connect, or VPC peering.
- DMS Replication Process
   ![](https://docs.aws.amazon.com/dms/latest/userguide/images/datarep-Welcome.png)
- Replication
  ![](https://docs.aws.amazon.com/dms/latest/userguide/images/datarep-intro-rep-instance1.png)
  ![](https://docs.aws.amazon.com/dms/latest/userguide/images/datarep-intro-rep-task1.png)

---
## Machine Learning

### SageMaker

* build, train, and deploy machine learning models
* prebuilt containers for common machine learning frameworks—such as Tensorflow, Pytorch, and MxNet
* provides a suite of built-in algorithms (via docker containers)
* can provide custom containers
* model serving endpoints
* jupyter notebooks
* SageMaker notebook instance is a machine learning (ML) compute instance running the Jupyter Notebook App

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

### Kendra

* intelligent search service (ML powered)
* concepts - index, documents (html, pdf, word, ppt, txt), data sources (S3, confluence, OneDrive, etc.), query
* point indexer to files in S3
* pre-built faceted search UI component (web based)
* supports [custom data sources](https://docs.aws.amazon.com/kendra/latest/dg/data-source-custom.html). e.g. salesforce attachments data source
* can create custom document attributes
* developer and enterprise editions

---

## Security, Identity, and Compliance

### IAM

* terms - Resources, Identities, Entities, Principals (person or application)
* authentication, authorization
* actions and operations on resources
* policy docs - AWS managed policies, Customer managed policies, Inline policies
* Identity-based and resource-based policies
* identities - users, groups, roles
* STS - temp security credentials
* assume role
* identity federation - Federated users and roles (via OIDC, SAML2, Cognito)
* [Attribute-based access control (ABAC)](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html) - defines permissions based on attributes (tags)
* [permission boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html)
* sigv4 requests
* account root user
* MFA
* IAM Access Analyzer - validate policies, generate policies (based on CT logs, role or user, and timeframe)

### Cognito

* UserPool
* IdentityPool - exchange UserPool.Identity for temporary IAM credentials
    * unauthenticated and authenticated roles
* Built-in IdP Providers - amazon, google, twitter, facebook.
* Federation - OIDC, SAML
* API Gateway authorizer
* provided login UIs

### Secrets Manager

### WAF

* web application firewall
* associate with ALB, CloudFront, API Gateway

### Certificate Manager (ACM)

* provision, manage, and deploy public and private Secure Sockets Layer/Transport Layer Security (SSL/TLS) certificates for use with AWS services and your internal connected resources.

### KMS

* key management service

### Directory Service

* provides multiple ways to set up and run Amazon Cloud Directory, Amazon Cognito, and Microsoft AD with other AWS services. Amazon Cloud Directory provides a highly scalable directory store for your application’s multihierarchical data. Amazon Cognito helps you create a directory store that authenticates your users either through your own user pools or through federated identity providers. AWS Directory Service for Microsoft Active Directory (Enterprise Edition), also known as Microsoft AD, enables your directory-aware workloads and AWS resources to use a managed Active Directory in the AWS Cloud.

---

## Media Services

### Amazon Interactive Video Service

> Amazon Interactive Video Service (Amazon IVS) is a managed live streaming solution that is quick and easy to set up, and ideal for creating interactive video experiences. Send your live streams to Amazon IVS using standard streaming software like Open Broadcaster Software (OBS) and the service does everything you need to make low-latency live video available to any viewer around the world, letting you focus on building interactive experiences alongside the live video.