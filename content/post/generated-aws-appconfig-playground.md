+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2020-10-20
description = ""
summary = " "
draft = false
slug = "aws-appconfig"
tags = ["aws","appconfig","configuration","deployment","lambda",]
title = "AWS AppConfig"
repoFullName = "pfeilbr/aws-appconfig-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-appconfig-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-appconfig-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-appconfig-playground</a>
</div>


learn [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html)

> create, manage, and quickly deploy application configurations. AWS AppConfig supports controlled deployments to applications of any size and includes built-in validation checks and monitoring. You can use AWS AppConfig with applications hosted on EC2 instances, AWS Lambda, containers, mobile applications, or IoT devices.



## Concepts

**Domain**

* Application (myapp)
* Environment (dev, test, demo, prod)
* Configuration Profile - versioned configuration data.  text, json, yaml, S3 object, SSM Document, SSM Parameter, CodePipeline
* Deployment - types: `AllAtOnce`, `Linear50PercentEvery30Seconds`, `Canary10Percent20Minutes`

**Functional**

* deploy configuration changes from a central location
* rules to validate your configuration. configurations that aren't valid can't be deployed.
    * validation types: JSON schema, Lambda. see [About validators](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-creating-configuration-and-profile-validators.html)


---

## Example(s)

get configuration via cli
```sh
aws appconfig get-configuration \
    --application 'app01' \
    --environment 'dev' \
    --configuration 'config-profile-01' \
    --client-id 'test' \
    appconfig.json

# view results in specified output file `appconfig.json`
cat appconfig.json
```

output

![](https://www.evernote.com/l/AAEqjn5qdblEL5J0kWjsMG2g4OkInAN-hOkB/image.png)

---

## AWS Console Screenshots


Configuration profile source types

![](https://www.evernote.com/l/AAFPtmY9U1tLhL_v42m3BOxd-jtaQ0ZYJBsB/image.png)

Example JSON configuration profile

![](https://www.evernote.com/l/AAG_2LdzxtpK6o_hfXg_hc2Q-ZfMkjGMCGkB/image.png)

Deployment Strategy Types

![](https://www.evernote.com/l/AAEujdNkJthBD7jwMEzwtF6qj0GctFCDsuoB/image.png)

Start Deployment

![](https://www.evernote.com/l/AAH80DpD0MpJILm3IYc6KpR9yPw3nt845c0B/image.png)

Deployment

![](https://www.evernote.com/l/AAGc3YJs7dhBWr2FLWxLN7yOycCdpbI2ybUB/image.png)



## Resources

* [AWS AppConfig Documentation](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html)
* [Deploying application configuration to serverless: introducing the AWS AppConfig Lambda extension](https://aws.amazon.com/es/blogs/mt/introducing-aws-appconfig-lambda-extension-deploying-application-configuration-serverless/) - blog post on how to use [AppConfig Lambda extension](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-integration-lambda-extensions.html)
* [AWS AppConfig integration with Lambda extensions](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-integration-lambda-extensions.html) -
* [sessions-with-aws-sam/appconfig-lambda-extensions/README.md](https://github.com/aws-samples/sessions-with-aws-sam/blob/master/appconfig-lambda-extensions/README.md) - good complete reference implementation on how to effectively use with lambda
* [sthulb/appconfig-demo](https://github.com/sthulb/appconfig-demo)




