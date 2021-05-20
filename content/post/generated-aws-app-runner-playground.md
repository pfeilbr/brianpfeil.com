+++
author = "Brian Pfeil"
categories = ["Python", "playground"]
date = 2021-05-19
description = ""
summary = " "
draft = false
slug = "aws-app-runner"
tags = ["aws","containers",]
title = "AWS App Runner"
repoFullName = "pfeilbr/aws-app-runner-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-app-runner-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-app-runner-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-app-runner-playground</a>
</div>


learn [AWS App Runner](https://aws.amazon.com/blogs/containers/introducing-aws-app-runner/)
## Comments

* good service to get users *"closer"* to serverless on eases the onboarding to AWS for solutions
* less knobs/options to turn/get wrong
* it's [cheap](https://aws.amazon.com/apprunner/pricing/), but not as cheap as lambda.
* public only endpoints for now
* similar goals and roadmap as [GCP Cloud Run](https://cloud.google.com/run) *(AWS is playing catch-up)*
* [More choices](https://twitter.com/jrhunt/status/1394797751880208384?s=20) for containers and potentially confusing for customers (*container options menu is getting pretty big*)

---
## Notes

* prefer App Runner AWS managed container runtimes (e.g. [Node](https://docs.aws.amazon.com/apprunner/latest/dg/service-source-code-nodejs.html) and [Python](https://docs.aws.amazon.com/apprunner/latest/dg/service-source-code-python.html)).  Similar to lambda, ElasticBeanstalk, CloudFoundry, Heroku, etc.
* App Runner product manager said the managed container runtimes as based on elastic beanstalk. (source video - [AWS App Runner Workshop](https://www.youtube.com/watch?v=97Ua6Gv_HSo))
* aws takes care of / not your responsibility
    * load balanced
    * autoscale
    * no clusters
* [App Runner configuration file (`apprunner.yaml`)](https://docs.aws.amazon.com/apprunner/latest/dg/config-file.html) -
* connect directly to github
* config options
    * health check config
    * cpu, memory
    * instance role
    > see [Create a source code repository service](https://docs.aws.amazon.com/apprunner/latest/api/API_CreateService.html#API_CreateService_Example_1) for all options
* custom domain support
* [Node](https://docs.aws.amazon.com/apprunner/latest/dg/service-source-code-nodejs.html) and [Python](https://docs.aws.amazon.com/apprunner/latest/dg/service-source-code-python.html) managed container runtimes to start.  Planned to support and follow order of [lambda supported runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html).
* public endpoints only (as of 2021-05-18) - see [roadmap](https://github.com/aws/apprunner-roadmap/projects/1) [`#1`](https://github.com/aws/apprunner-roadmap/issues/1), [`#2`](https://github.com/aws/apprunner-roadmap/issues/2) for private endpoints and access to VPC resources.

---
## Pricing

> You are charged for the compute and memory resources used by your application. In addition, if you automate your deployments, you will pay a set monthly fee for each application that covers all automated deployments for that month. If you opt to deploy from source code, you will pay a build fee for the amount of time it takes App Runner to build a container from your source code.

---
## Demo

```sh
mkdir hello-app-runner
touch apprunner.yaml

# install venv and deps
pipenv install

# run locally
pipenv run python app.py

# deploy
SERVICE_NAME="hello-app-runner-01"
aws apprunner create-service --service-name ${SERVICE_NAME} \
    --source-configuration file://apprunner.yaml
```

---
## Resources

* [Introducing AWS App Runner](https://aws.amazon.com/blogs/containers/introducing-aws-app-runner/)
* [Hello AWS App Runner](https://www.youtube.com/watch?v=HJsULvSJWes) - youtube
* [AWS App Runner Workshop](https://www.youtube.com/watch?v=97Ua6Gv_HSo) - youtube.  good details on roadmap.  aws tech pm is a part of it.
* [Documentation | AWS App Runner](https://docs.aws.amazon.com/apprunner/latest/dg/what-is-apprunner.html)
* [aws-containers/apprunnerworkshop](https://github.com/aws-containers/apprunnerworkshop)
* [apprunner-roadmap](https://github.com/aws/apprunner-roadmap/projects/1) - vote up issues important to your needs
* [aws-containers/hello-app-runner](https://github.com/aws-containers/hello-app-runner)
* [AWS App Runner API Reference](https://docs.aws.amazon.com/apprunner/latest/api/Welcome.html)
* [Pricing](https://aws.amazon.com/apprunner/pricing/)

<!--
---
tags: ["aws", "app-runner", "containers"]
summary: "learn AWS App Runner"
---
-->



