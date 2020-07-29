+++
title = "Serverless Architecture: Key Service Considerations"
slug = "serverless-architecture-key-considerations-per-service"
author = "Brian Pfeil"
date = "2020-07-20"
lastmod = "2020-07-28"
draft = false
categories = ["architecture", "aws", "serverless"]
tags = ["architecture", "aws", "serverless"]
summary = "Key service considerations and configuration options for a serverless architecture"

+++

A serverless architecture is "typically" composed of many services.  The following 
covers the key considerations and configuration options for the *most common* AWS services leveraged for serverless architectures.

---

<!-- TOC -->

- [Relevant Patterns](#relevant-patterns)
- [Lambda](#lambda)
- [SNS](#sns)
- [SQS](#sqs)
- [Kinesis](#kinesis)
- [EventBridge](#eventbridge)
- [DynamoDB](#dynamodb)
- [Step Functions](#step-functions)
- [API Gateway](#api-gateway)
- [CloudFront](#cloudfront)
- [Route53](#route53)
- [Global Accelerator](#global-accelerator)
- [WAF](#waf)

<!-- /TOC -->

---

### Relevant Patterns

common cloud native patterns to consider in the context of serverless architectures <u>of scale</u>

* event sourcing
* circuit breaker - trip circuit to prevent downstream systems overload
* [load shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/) - prevent backlog buildup
* handle poison messages - prevent kinesis and dynamodb streams from progressing
* prevent distributed transactions.  e.g. lambda send job to SQS and stores status in dynamodb.  break it up.  lambda put job status in dynamo -> dynamo stream -> lambda send job to SQS

---

### [Lambda](https://aws.amazon.com/lambda/)

* synchronous vs asynchronous vs poll based (poll based is sync) - impacts automatic retries, stuck messages due to poison message, etc.
  * see [Understanding the Different Ways to Invoke Lambda Functions](https://aws.amazon.com/blogs/architecture/understanding-the-different-ways-to-invoke-lambda-functions/)
* if lambda is strictly a glue passthrough for API Gateway to call a backend AWS service, look to use [API Gateway Service Proxies](https://lumigo.io/blog/the-why-when-and-how-of-api-gateway-service-proxies/) to remove lambda.  simpler/cheaper/etc.
* memory
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


### [SNS](https://aws.amazon.com/sns/)

* fan out to address scale
* [KMS](https://aws.amazon.com/kms/) to encrypt payloads

### [SQS](https://aws.amazon.com/sqs/)

* batch size - batch fails as unit
* visibility timeout - set to 6x lambda timeout
* message retention period
* delivery delay - max 15min
* types - standard vs FIFO
    * standard - at least once delivery.  need to ensure idempotent
* alarm on queue depth
* KMS

### [Kinesis](https://aws.amazon.com/kinesis/)

* partition key - choose wisely as order is guaranteed per shard and pk determines the shard the message lands on
* poison messages (retry until success - can cause backlog)
* [KMS](https://aws.amazon.com/kms/) to encrypt payloads
* enhanced fan-out via AWS::Kinesis::StreamConsumer.  each consumer gets 2 MiB per second for every shard you subscribe to.  can subscribe a max of 5 consumers per stream.

### [EventBridge](https://aws.amazon.com/eventbridge/)

* put events - 2400 requests per second per region
* invocation [quota](https://docs.aws.amazon.com/eventbridge/latest/userguide/cloudwatch-limits-eventbridge.html) -  4500 requests per second per region (invocation is an event matching a rule and being sent on to the rule’s targets)

### [DynamoDB](https://aws.amazon.com/dynamodb/)

* global tables - for resilient active-active architectures
* throttles
* streams - 24hr data retention.  poison messages (retry until success - can cause backlog)
* partition key - distribute data among nodes to minimize hot partitions
* TTL - can the data be removed automatically

### [Step Functions](https://aws.amazon.com/step-functions/)

* Standard Workflows vs [Express Workflows](https://aws.amazon.com/about-aws/whats-new/2019/12/introducing-aws-step-functions-express-workflows/)
* [saga](https://theburningmonk.com/2017/07/applying-the-saga-pattern-with-aws-lambda-and-step-functions/) pattern for rollback
* [parallel map](https://aws.amazon.com/blogs/aws/new-step-functions-support-for-dynamic-parallelism/) opportunities - run tasks in parallel

### [API Gateway](https://aws.amazon.com/api-gateway/)

* REST API vs [HTTP API](https://aws.amazon.com/blogs/compute/announcing-http-apis-for-amazon-api-gateway/) ([cheaper](https://aws.amazon.com/api-gateway/pricing/))
* [caching](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html) - fixed cost based on time / no pay per use
* throttles
* timeout - 29s
* auth - cognito, JWT, IAM (aws sigv4), custom lambda auth
* OpenAPI specs for payload validation
* service proxies - no need for lambda glue in middle
* custom domains
* websockets

### [CloudFront](https://aws.amazon.com/cloudfront/)

* [origin access identity](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html) to force traffic through CloudFront and removes direct access to S3 website domain URL
* [signed URLs or cookies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html)
* lambda@edge - headers only requests, rewrite URLs, server-side rendering (SSR), auth, etc.
* cache invalidations
* non GET HTTP methods support.  must explicitly turn on support for PUT, POST, PATCH, etc.
* WAF in front

### [Route53](https://aws.amazon.com/route53/)

* [Geoproximity routing](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html#routing-policy-geoproximity) for global solutions serving multiple regions

### [Global Accelerator](https://aws.amazon.com/global-accelerator/)

> uses the AWS global network to optimize the path from your users to your applications, improving the performance of your traffic by as much as 60%

### [WAF](https://aws.amazon.com/waf/)

* can put in front of API Gateway or CloudFront
* API Gateway provides overlapping functionality with WAF.  Need to determine the appropriate service to use.
