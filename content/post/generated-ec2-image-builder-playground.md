+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2022-05-25
description = ""
summary = " "
draft = false
slug = "ec2-image-builder"
tags = ["aws","ec2"]
title = "EC2 Image Builder"
repoFullName = "pfeilbr/ec2-image-builder-playground"
repoHTMLURL = "https://github.com/pfeilbr/ec2-image-builder-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/ec2-image-builder-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/ec2-image-builder-playground</a>
</div>


learn [EC2 Image Builder](https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html)

> EC2 Image Builder is a fully managed AWS service that makes it easier to automate the creation, management, and deployment of customized, secure, and up-to-date server images that are pre-installed and pre-configured with software and settings to meet specific IT standards.

> AWS Systems Manager Agent (SSM Agent) is Amazon software that runs on Amazon Elastic Compute Cloud (Amazon EC2) instances, edge devices, and on-premises servers and virtual machines (VMs). SSM Agent makes it possible for Systems Manager to update, manage, and configure these resources. The agent processes requests from the Systems Manager service in the AWS Cloud, and then runs them as specified in the request. SSM Agent then sends status and execution information back to the Systems Manager service by using the Amazon Message Delivery Service (service prefix: ec2messages).

---

## Process to Build AMI

1. select base AMI (e.g. amazon linux 2, a custom AMI).  must have SSM agent installed.
1. select IAM role that is used as instance profile for EC2 build process and test process
1. select amazon provided build components or specify your own build components
    - amazon provided e.g. correto
    - custom - defined via yaml with steps.  e.g. step types - bash, executable
1. select amazon provided tests or specify own custom tests
1. specify build schedule - manual, schedule builder, CRON 
1. specify which regions to publish the resulting ami to
1. can be shared with account, organization ou, whole organization

---

## Process to Build Docker Image

1. select base container image.  e.g. aws maanged images, an image in ECR, docker hub image
1. select IAM role that is used as instance profile for EC2 build process and test process
1. select amazon provided build components or specify your own build components
   - amazon provided e.g. correto
    - custom - defined via yaml with steps.  e.g. step types - bash, executable
1. select amazon provided tests or specify own custom tests
1. specify build schedule - manual, schedule builder, CRON 
1. specify Dockerfile template
1. the target ECR repository to store the image

---

## AWS Systems Manager Agent (SSM Agent)

> AWS Systems Manager Agent (SSM Agent) is Amazon software that runs on Amazon Elastic Compute Cloud (Amazon EC2) instances, edge devices, and on-premises servers and virtual machines (VMs). SSM Agent makes it possible for Systems Manager to update, manage, and configure these resources. The agent processes requests from the Systems Manager service in the AWS Cloud, and then runs them as specified in the request. SSM Agent then sends status and execution information back to the Systems Manager service by using the Amazon Message Delivery Service (service prefix: ec2messages).

---

## [AWS Task Orchestrator and Executor (AWSTOE) component manager](https://docs.aws.amazon.com/imagebuilder/latest/userguide/toe-component-manager.html)

> application to orchestrate complex workflows, modify system configurations, and test your systems without writing code. This application uses a declarative document schema. Because it is a standalone application, it does not require additional server setup. It can run on any cloud infrastructure and on premises.

* single golang binary that can validate and run AWSTOE components documents (yaml)

**`hello-world-linux.yml`**

example AWSTOE components document

```yaml
name: Hello World
description: This is hello world testing document for Linux.
schemaVersion: 1.0
phases:
  - name: build
    steps:
      - name: HelloWorldStep
        action: ExecuteBash
        inputs:
          commands:
            - echo 'Hello World from the build phase.'
  - name: validate
    steps:
      - name: HelloWorldStep
        action: ExecuteBash
        inputs:
          commands:
            - echo 'Hello World from the validate phase.'
  - name: test
    steps:
      - name: HelloWorldStep
        action: ExecuteBash
        inputs:
          commands:
            - echo 'Hello World from the test phase.'
```

see [Get started with AWSTOE](https://docs.aws.amazon.com/imagebuilder/latest/userguide/toe-get-started.html)

```sh
# validate
awstoe validate --documents hello-world-linux.yml

# run all phases
# a local directory named `TOE*` is created for the run and includes detailed logs
awstoe run --documents hello-world-linux.yml

# run single phase
awstoe run --documents hello-world-linux.yml --phases build
```

* a local directory named `TOE*` is created for the run and includes detailed logs
* see [`TOE_2022-05-25_14-01-45_UTC-0_3699d6f5-dc33-11ec-9989-00224820200b`](https://github.com/pfeilbr/ec2-image-builder-playground/blob/master/TOE_2022-05-25_14-01-45_UTC-0_3699d6f5-dc33-11ec-9989-00224820200b)

![](https://www.evernote.com/l/AAHVWa578E9A9IKjdBoT13JdAYqkfCKNUDAB/image.png)

---

## Resources

- [EC2 Image Builder](https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html)
- [Youtube - AWS re:Invent 2019: NEW LAUNCH! EC2 Image Builder: Virtual machine images made easy (CMP214-R1)](https://www.youtube.com/watch?v=9XFuRq0R8nk)
- [AWS Task Orchestrator and Executor component manager](https://docs.aws.amazon.com/imagebuilder/latest/userguide/toe-component-manager.html) - runs image builder and codebuild yaml files
- [Get started with AWSTOE](https://docs.aws.amazon.com/imagebuilder/latest/userguide/toe-get-started.html)
