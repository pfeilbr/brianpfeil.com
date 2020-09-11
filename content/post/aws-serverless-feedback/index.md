+++
title = "AWS Serverless Feedback"
slug = "aws-serverless-feedback"
author = "Brian Pfeil"
date = "2020-09-11"
lastmod = "2020-09-11"
draft = true
categories = []
tags = ["aws", "serverless"]
summary = ""

+++

Feedback on serverless usage on AWS.  Based on working with and observations of the teams that leverage the set of AWS "serverless" services.  Feedback format is **Challenge** and **Suggestion** for a given topic, concept, service, or feature.


### Table of Contents

* [Serverless at AWS: General](#serverless-at-aws-general)
    * [Challenge: Skill Set / Developer Accessibility](#challenge-skill-set--developer-accessibility)
    * [Suggestion: Skill Set / Developer Accessibility](#suggestion-skill-set--developer-accessibility)
    * [Challenge: Developer Experience (DX)](#challenge-developer-experience-dx)
    * [Suggestion: Developer Experience (DX)](#suggestion-developer-experience-dx)
    * [Challenge: Cost Forecasting](#challenge-cost-forecasting)
    * [Suggestion: Cost Forecasting](#suggestion-cost-forecasting)
    * [Challenge: Non-AWS Core Enterprise Tools](#challenge-non-aws-core-enterprise-tools)
    * [Suggestion: Non-AWS Core Enterprise Tools](#suggestion-non-aws-core-enterprise-tools)
* [IAM](#iam)
    * [Challenge: Skill Set / Developer Accessibility](#challenge-skill-set--developer-accessibility-1)
    * [Suggestion: Skill Set / Developer Accessibility](#suggestion-skill-set--developer-accessibility-1)
* [CloudFormation](#cloudformation)
    * [Challenge: Deployment Time](#challenge-deployment-time)
    * [Suggestion: Deployment Time](#suggestion-deployment-time)
* [Lambda](#lambda)
    * [Challenge: Lambda or Container Decision](#challenge-lambda-or-container-decision)
    * [Suggestion: FaaS or Container Decision](#suggestion-faas-or-container-decision)
    * [Challenge: Cost vs. Performance Tuning](#challenge-cost-vs-performance-tuning)
    * [Suggestion: Cost vs. Performance Tuning](#suggestion-cost-vs-performance-tuning)
* [DynamoDB](#dynamodb)
    * [Challenge: Learning Curve](#challenge-learning-curve)
    * [Suggestion: Learning Curve](#suggestion-learning-curve)
* [Amplify CLI](#amplify-cli)
    * [Challenge: Enterprise Support](#challenge-enterprise-support)
    * [Suggestion: Enterprise Support](#suggestion-enterprise-support)
    * [Challenge: Uncomfortable Level of Magic](#challenge-uncomfortable-level-of-magic)
    * [Suggestion: Uncomfortable Level of Magic](#suggestion-uncomfortable-level-of-magic)
* [AppSync](#appsync)
    * [Challenge: GraphQL Centered Development Learning Curve](#challenge-graphql-centered-development-learning-curve)
    * [Suggestion: GraphQL Centered Development Learning Curve](#suggestion-graphql-centered-development-learning-curve)
* [API Gateway](#api-gateway)
    * [Challenge: Limited Service Support for HTTP API -> AWS Service Integrations](#challenge-limited-service-support-for-http-api---aws-service-integrations)
    * [Suggestion: Limited Service Support for HTTP API -> AWS Service Integrations](#suggestion-limited-service-support-for-http-api---aws-service-integrations)
    * [Challenge: VTL Mapping Templates](#challenge-vtl-mapping-templates)
    * [Suggestion: VTL Mapping Templates](#suggestion-vtl-mapping-templates)
* [EventBridge](#eventbridge)
    * [Challenge: Security Model](#challenge-security-model)
    * [Suggestion: Security Model](#suggestion-security-model)
    * [Challenge: Observability](#challenge-observability)
    * [Suggestion: Observability](#suggestion-observability)
    * [Challenge: Real-time and High Volume Event Rates](#challenge-real-time-and-high-volume-event-rates)
    * [Suggestion: Real-time and High Volume Event Rates](#suggestion-real-time-and-high-volume-event-rates)
* [X-Ray](#x-ray)
    * [Challenge: Effort to Enable](#challenge-effort-to-enable)
    * [Suggestion: Effort to Enable](#suggestion-effort-to-enable)
* [AWS Serverless Application Model (SAM)](#aws-serverless-application-model-sam)
    * [Challenge: Infrastructure Resource to Code Locality](#challenge-infrastructure-resource-to-code-locality)
    * [Suggestion: Infrastructure Resource to Code Locality](#suggestion-infrastructure-resource-to-code-locality)

---

### Serverless at AWS: General

#### Challenge: Skill Set / Developer Accessibility

Serverless skill set has less to do with coding and more knowing the capabilities of each service and how they can be integrated and composed together.  The role of the architect becomes central to building effective serverless solutions.  This is increasingly so, because the integrations between services are trending more towards configuration over code.

"Traditional" application developers see the next step as containers because it familiar / closer to what they're used to (long-lived processes running on an OS vs. a transient run-time environment).  It's hard to make the leap directly to serverless and bypass the containers and k8s space.

#### Suggestion: Skill Set / Developer Accessibility

This is where education / resources / etc. are the main tools.  Continue and accelerate the creation of content on the AWS blogs, twitch channel, youtube channels, podcasts, Developer Advocates on social media, etc.

Amplify suite of tools and services is helping in this area for easing the on-boarding those new to serverless development on AWS.



---

#### Challenge: Developer Experience (DX)

The path to "serverless" adoption has shifted from the foundational technologies being in place to improving developer experience.  Everyone is sold on serverless being the right thing, now it's enabling it's usage ad making accessible to the huge pool of developers who only have experience with "traditional" application development.

#### Suggestion: Developer Experience (DX)

SAM and Amplify tooling are quickly addressing the gaps.  Accelerate what's already being done.

---



#### Challenge: Cost Forecasting

Currently difficult to estimate cost with serverless solutions because usually composed of many services.  It's a good deal of effort to understand all the cost contributing dimensions across all the used services.  Then assemble.

#### Suggestion: Cost Forecasting

An "Cost Profiler" feature by exercising a solution while "recording" it, then extrapolating to give a cost per "user" transaction / time (for sustained transactions) / etc..  "Cost Profiler" similar to a performance profiler.

This has similarities and maybe could leverage X-Ray distributed traces + the already captured default CloudWatch metrics per service.

---

#### Challenge: Non-AWS Core Enterprise Tools

Building an effective CI/CD pipeline at a large enterprise involves leveraging non-enterprise tooling. For example, Bitbucket, Jenkins, and Artifactory.

This leads to "lowest common denominator" pipelines that don't meet the vision of CI/CD.  They are dependant on the availability of adapters/integrations/etc. for specific clouds that the cloud agnostic tools provide.

AWS has a corresponding solution for each of these that eases building a CI/CD pipeline when the target is AWS.  Integrated security via IAM threaded through all the service interactions is the biggest win as security is usually the sticking point.  We lose "potential" value as a result of using these non-AWS equivalents over the flexibility it provides the company to support it's current multi-cloud (aws+azure) position.


#### Suggestion: Non-AWS Core Enterprise Tools

This is driven by the "non all-in" stance of many large enterprises for multi-cloud.  More education in this area about explicitly acknowledging a single cloud approach for *given enterprise areas*, and understanding and documenting the cost to switch to a different cloud is enough to mitigate the "perceived" risk.

---

### IAM

#### Challenge: Skill Set / Developer Accessibility

Security is inherently hard and involves many complex entities and their relationships.  To be effective and successful on AWS, a customer needs to know this.  This is table stakes.  IAM continues to be the largest barrier to entry I see with AWS users.  It is necessary and robust, but a new concept to "traditional" developers.  The closest thing to it that many devs have experience with is RDBMS permissions.

#### Suggestion: Skill Set / Developer Accessibility

AWS is leveraging Amplify suite as an on-boarding mechanism for those new to AWS.  It currently "handles" all the IAM concerns via automation / codegen / etc.  Maybe helpful to add features that allow developers to take more ownership in this area.  Similar to what SAM CLI does with [AWS SAM Policy Templates](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-policy-templates.html)

---

### CloudFormation

#### Challenge: Deployment Time

A challenge I've observed with serverless development, is slowed down iterative workflow due to the length of time it takes for a CloudFormation deployment to run.  Developers are used to live reload level of speed to see dev changes reflected back to them.

#### Suggestion: Deployment Time

---

### Lambda

#### Challenge: Lambda or Container Decision

Lambda has grown to have a lot of features and configuration options.  Lambda feature set is converging towards Fargate and vice versa.  There is already a decision to be made on which to choose.  This convergence could make it even more unclear which to pick.  Or if one goes away and they are merged, the migration path.

#### Suggestion: FaaS or Container Decision

* More tools similar to [Well-Architected](https://aws.amazon.com/architecture/well-architected/) to help decide.
* Converge Lambda and Container functionality into single service

---

#### Challenge: Cost vs. Performance Tuning

The external community has solutions such as lambda power tuning to automate finding the right compute/memory configuration for a given applications priority balance between performance and cost.

#### Suggestion: Cost vs. Performance Tuning

AWS has all the information and metrics about the container environment through the duration of the run.  Would be nice to have this as a service.  Maybe "Lambda tuning suggestions" that is purely informational and someone has to take action to apply configuration changes.  This helps customers, but AWS also with it's own efficiency goals via underlying resource scheduling (e.g. scheduling, workload placement, container packing, etc.)

---

### DynamoDB

#### Challenge: Learning Curve

* the default serverless database.
* NoSQL does not have standards like the RDBMS and extended SQL family.  You are learning an AWS specific DB and how to interact with it via an API.  * There is no smoothing / accessibility layer like SQL.

This is a DB where to use effectively, you need to learn it.  I've observed devs try to lean on language/library/framework ORMs, but that only gets them so far.  In order to dev, debug, deploy, operationalize, and troubleshoot it, you need to learn it.

#### Suggestion: Learning Curve

Continue with tools like [NoSQL Workbench for DynamoDB GUI Client](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html) and education resources.

There is a lot of content on single table vs. multi-table design for a single application.  I've observed developers go down the "expert" path of single table design, but once it was operational and had to be supported, the support team has to learn the "advanced" single table concepts.  They made errors, etc., and we eventually split into multi-table design because it was more supportable.

---

### Amplify CLI

#### Challenge: Enterprise Support

Amplify in it's current form poses some challenges for use in enterprises.  This is due to the amount of automation around the creation of IAM resource types on behalf of the developer.  You need a large set of permissions to use including those to create new IAM resource types, which becomes an application partitioning/firewalling issue in shared accounts in addition to the increased security concerns around IAM.

#### Suggestion: Enterprise Support

Add various IAM role/policy/etc. parameters to configure.

It's aim to stay simple for the target audience may make this extra/advanced usage an product impedance mismatch, and therefore out of scope for the product.

---

#### Challenge: Uncomfortable Level of Magic

Amplify CLI is making AWS more accessible to "traditional" developers.  Makes it really easy to get started by automating all of the resource provisioning pieces.  Once you need to go outside the "happy path" / debug / troubleshoot / deal with IAM, etc., devs need to understand these concepts.  The amount of infrastructure code and source code it generates for the developer has the "feel" of too much magic.  All those extra artifacts that get checked into the repo makes it "feel" prone to breakage as the CLI evolves.

#### Suggestion: Uncomfortable Level of Magic

To address the users that want to break out of "beginner" mode on rails, and take more control of resource provisioning, allow the one-way "ejection" from Amplify CLI to SAM CLI.  Similar to what [create-react-app | npm run eject](https://create-react-app.dev/docs/available-scripts#npm-run-eject).  This enables a natural learning and skills transition for devs to take on and understand more AWS concepts, and therefore more effective us of the AWS platform.

---

### AppSync

#### Challenge: GraphQL Centered Development Learning Curve

Great service and there are clear benefits to graphql centric development.

There is a necessary steep learning curve inherent to graphql.  Many "new" concepts for devs to learn.  API, Schema, DataSource, Resolver, Resolver Function, Resolver Pipeline.  New graphql schema language to learn, and to use effectively, AWS specific schema directives.

Feels vendor lockin-y, but traded for the auto provisioned DB, configurable security (e.g. Cognito UserPools), generated client side code.

#### Suggestion: GraphQL Centered Development Learning Curve

Looking at other tech of the past and their evolution, community standardization around GraphQL managed services would be the next likely step.  The value AppSync provides is much more than graphql itself.  It builds on the benefit of the schema via tooling like Amplify CLI for strong typing, auto provision storage backend (AWS graphql directives), client-side code generation, etc.  All these things are AWS specific and don't yet have standards or a generalized community name.  Maybe they never will, and it's similar to DynamoDB as a unique only at AWS cloud differentiating super-service, but if not, AWS could be a part of that future body and drive standardization along with other cloud vendors.

---

### API Gateway

#### Challenge: Limited Service Support for HTTP API -> AWS Service Integrations

HTTP API -> AWS Service Integrations are great for simplified and removing lambda as a simple glue layer.  There is currently a limited set of services supported.

#### Suggestion: Limited Service Support for HTTP API -> AWS Service Integrations

Keep the momentum with adding service support.

---

#### Challenge: VTL Mapping Templates

I have observed with developers I've worked with that VTL mapping templates cause a lot of confusion.  Should they become a expert at VTL and put the logic to transform a payload in it?  Another legacy language to learn that has limited returns on investment.  Should they just do it in lambda with a language they are familiar with?  It "feels" like it's something that should not be exposed to customer and only used internally.  The Java-ness heritage of verbosity, and yet another language to learn and know, is an implementation detail/concern being surfaced to the customer.

#### Suggestion: VTL Mapping Templates

Phase out / deprecate usage.  Introduce a way to express via simplified, declarative only (no control constructs trying to be a general purpose programming language), yaml/json.

---

### [EventBridge](https://aws.amazon.com/eventbridge/)

EventBridge seems like it's on the way to being a centerpiece service of serverless solutions.  As core to serverless as lambda is.

#### Challenge: Security Model

The security model around events "feels" a bit off at the moment.  It almost feels like it's bypassing security.  If I can subscribe to events on a given bus, especially "default" account bus, I can access information coming from a whole host of services.  It similar to the sensitivity at which CloudTrail requires.  This sensitivity means more concerns around security, which limits adoption.

#### Suggestion: Security Model

It is covered by [IAM Policy Conditions](https://docs.aws.amazon.com/eventbridge/latest/userguide/policy-keys-eventbridge.html), but it doesn't feel like first class support.  Less than ideal DX.  IAM policy conditions is an already overloaded mechanism where concepts that don't cleanly fit into the Resources and Actions entity concepts are put.

The naive answer would be a new IAM concept, like "Events" and corresponding "Producers" and "Consumers" (Actions, Resources, Events, Producers, Consumers and Condition Keys for AWS Services).  Similar to Resources, Events could benefit from first class IAM entity concepts like Events, Producers, Consumers to align with developer expectations around event based systems.

---

#### Challenge: Observability

Events in general are challenging when it comes to observability.  EventBridge is no different.

#### Suggestion: Observability

* event retention per bus.  similar to kinesis 7 day max.
* native event replay / event time travel to help with dev debugging, app state transitions, event schema evolution.

---

#### Challenge: Real-time and High Volume Event Rates

Also some hook into the trend of client-side event based state solutions feels natural for EventBridge (e.g. [React Redux](https://react-redux.js.org/)).  Maybe it's in the form of a library that fits into Amplify since it's aligned to client-side web and mobile tech.

Given events in many systems can be high volume and high rates, exposing a native websocket API for the publishing and consumption of events would be helpful.  There are already projects in the community doing this, which validates the need for it.

#### Suggestion: Real-time and High Volume Event Rates

* native websocket api for high volume and real-time without having the added complexity of AppSync or API Gateway.

---

### [X-Ray](https://aws.amazon.com/xray/)

#### Challenge: Effort to Enable

Observability and distributed tracing is required for almost any serverless solution since there are many services involved.  This is the "serverless" version of a "traditional" stack trace and/or local application log.  These are essential tools for developers.

The following are friction points with the service:

* Instrumenting code with the x-ray sdk
* configuring to turn on/off in different way for each service *that supports it*
* having to understand and make decisions around sampling rates
* learning each services equivalent of a header to put a correlation/trace id in that doesn't interfere with the "core" payload, etc.

#### Suggestion: Effort to Enable

Ideally it would be on by default across all services, baked into each services pricing, and the customer would not have the choice to turn off.  These are plumbing level, distributed systems, "undifferentiated heavy lifting" types of concerns.  The ones AWS is best at handling.

The view is that aws runs all the services, and I as the customer shouldn't need to do anything, but use the services to get this visibility.    

---

### [AWS Serverless Application Model (SAM)](https://aws.amazon.com/serverless/sam/)

#### Challenge: Infrastructure Resource to Code Locality

The linkage from a SAM template to local code via a directory path/s3 location/etc. suffers the locality of code problem.  Infrastructure and code are clearly separated (you can do inline code up to char limit), when it should be converging and feel natural.  A future state being infrastructure usage as part of a solution feels like a first class concept of the language or a library where you offload language level single process control constructs to infrastructure that is distributed, scalable, and elastic (e.g. step fn, EventBridge, SNS, SQS, etc.).  To the point where I'm not thinking about the infrastructure at all.  I only express it through code.  Has a feeling of "shifting gears".

#### Suggestion: Infrastructure Resource to Code Locality

With the introduction of the [CDK](https://aws.amazon.com/cdk/), the lines between application code and infrastructure provisioning code is merging.  This "feels" like the more natural path for SAM to adopt the CDK style.

If you extend CDK to the next level of evolution in abstraction, it's a cloud specific programming language.  Infrastructure as a whole is "undifferentiated heavy lifting" and not of concern to an end user of a solution.  A current means to an end.  Something like "CloudScript"?, but already taken by MS :)


