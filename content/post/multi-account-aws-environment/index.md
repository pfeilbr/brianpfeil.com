+++
title = "Multi-Account AWS Environment"
slug = "multi-account-aws-environment"
author = "Brian Pfeil"
date = "2021-04-29"
lastmod = "2021-04-29"
draft = false
categories = []
tags = ["aws", "governance", "management"]
summary = " "

+++

Multi-Account AWS Environment options.

## [AWS Landing Zone](https://aws.amazon.com/solutions/implementations/aws-landing-zone/)

In short, it a collection of AWS accounts and other mechanisms to establish guardrails within those accounts.

Created as part of [AWS Solutions Library](https://aws.amazon.com/solutions/).

> AWS Landing Zone is currently in Long-term Support and will not receive any additional features

Should now use [AWS Control Tower](https://aws.amazon.com/controltower/)

* zip file with CloudFormation templates
* builds accounts types
* enables AWS Config, apply config rules
* enables CloudTrail
* enables SSO and AD connector
* Builds Account Vending Machine - self-service portal using Service Catalog to allow devs to request accounts, which are then created via CodePipeline

### Core Accounts

The following landing zone managed accounts are created as part of landing zone

* Log Archive - consolidated log files
* Security - creates auditor (read-only) and administrator (full-access) cross-account roles from a Security account to all AWS Landing Zone managed accounts.  Also master Amazon GuardDuty account
* Shared services - AD, DNS, LDAP
* Sandbox Accounts - devs can experiment / PoCs/ etc.
* Business Unit accounts - dev, test, prod workloads

## [AWS Control Tower](https://aws.amazon.com/controltower/)

* Better packaged and managed AWS Landing Zone.  AWS Landing Zone as a first class AWS service.
* Functions as a pre-baked layer of abstraction on top of AWS Organizations, AWS Config, CloudTrail, CloudFormation, and a few other services
* All in AWS Console.  No IaC for it.

### Control Tower Landing Zone Creating

<img src="https://www.evernote.com/l/AAHzUuao8-xBY7THr-S8jMHCuWoZ6xAImO4B/image.png" alt="" width="100%" />

<img src="https://www.evernote.com/l/AAF68UnbRtpBc7gngxxQ8H4gp97py7vUgHgB/image.png" alt="" width="100%" />

### Service Catalog | Create Control Tower Manged Account

<img src="https://www.evernote.com/l/AAFeQwzHYGhCIb2AhcWz6E3nmiEVXWejih0B/image.png" alt="" width="100%" />

<img src="https://www.evernote.com/l/AAFLSYmR7RlGVI2aMQccrD6MUDJVjhGoPQUB/image.png" alt="" width="100%" />

## [superwerker](https://github.com/superwerker/superwerker)

* Opinionated layer on top of Control Tower.
* Automates the setup of an AWS Cloud environment with prescriptive best practices.

## [AWS Organization Formation](https://github.com/org-formation/org-formation-cli)

* Infrastructure as Code (IaC) tool for AWS Organizations.
* Implemented using CloudFormation Custom Resource Types (providers) which then orchestrate and call the relevant AWS APIs

## Resources

* [AWS Control Tower](https://aws.amazon.com/controltower/)
* [Customizations for AWS Control Tower | Implementations | AWS Solutions](https://aws.amazon.com/solutions/implementations/customizations-for-aws-control-tower/)
* [AWS Organizations](https://docs.aws.amazon.com/organizations/index.html)
* [superwerker](https://github.com/superwerker/superwerker)
* [AWS Organization Formation](https://github.com/org-formation/org-formation-cli)
* [AWS CONTROL TOWER - How to Automate Landing Zone deployment with AWS Control Tower | Detailed DEMO](https://www.youtube.com/watch?v=1124VPrQiWo)