+++
author = "Brian Pfeil"
categories = ["TypeScript", "playground"]
date = 2021-04-23
description = ""
summary = " "
draft = false
slug = "aws-cloudformation-custom-resource-type"
tags = ["aws","cloudformation"]
title = "AWS CloudFormation Custom Resource Type"
repoFullName = "pfeilbr/aws-cloudformation-custom-resource-type-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-cloudformation-custom-resource-type-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-cloudformation-custom-resource-type-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-cloudformation-custom-resource-type-playground</a>
</div>


examples for creating CloudFormation extensions and specifically [CloudFormation Custom Resource Type](https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/what-is-cloudformation-cli.html)

> An extension is an artifact, registered in the CloudFormation Registry, which augments the functionality of CloudFormation in a native manner

> You can use the CloudFormation CLI to register extensions—both those you create yourself, as well as ones shared with you—with the CloudFormation registry. This enables you to use CloudFormation capabilities to create, provision, and manage these custom types in a safe and repeatable manner, just as you would any AWS resource

There are the following four types of CloudFormation extension mechanisms:

* [CloudFormation Custom Resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html)
* [CloudFormation Module](https://aws.amazon.com/blogs/mt/introducing-aws-cloudformation-modules/)
* [CloudFormation Custom Resource Types](https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-types.html)
* [CloudFormation Macros](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-macros.html)

## Example Custom Resource Types

* [`python-custom-resource-type-example`](https://github.com/pfeilbr/aws-cloudformation-custom-resource-type-playground/blob/master/python-custom-resource-type-example)
* [`typescript-custom-resource-type-example`](https://github.com/pfeilbr/aws-cloudformation-custom-resource-type-playground/blob/master/typescript-custom-resource-type-example)

## Notes

* [Custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) can be backed by lambda or [SNS topic](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources-sns.html#walkthrough-custom-resources-sns-adding-nonaws-resource)

## TODO

* Org::Service::WAFCDN -> CDK app containing
* API Gateway (custom auth token | or cloudformation security context identity) -> Step Fn -> create stack -> wait stack -> loop
* custom resource lambda handler is just a pass through to APIG provisioning the resources.
* store API Key in secrets manager and reference from cfn custom resource type property

```yaml
- Sid: DeleteAppRoles
  Effect: Allow
  Action:
    - wafcdn:*
  Resource: !Sub "arn:aws:cloudformation:${AWS::Region}:${AWS::AccountId}:type/resource/MyOrg-MyService-MyResource/*"
```

## Resources

* [User Guide for Extension Development](https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/what-is-cloudformation-cli.html)
* [Use Python to manage third-party resources in AWS CloudFormation | Amazon Web Services](https://aws.amazon.com/blogs/infrastructure-and-automation/using-python-to-create-aws-cloudformation-resource-providers/)
* [Learn Best Practices for Implementing AWS Lambda-backed Custom Resources with AWS CloudFormation](https://aws.amazon.com/premiumsupport/knowledge-center/best-practices-custom-cf-lambda/)
* [Writing an AWS CloudFormation Resource Provider in Python: Step by Step - Cloudar](https://www.cloudar.be/awsblog/writing-an-aws-cloudformation-resource-provider-in-python-step-by-step/)
* [CloudFormation Resource Providers - A Chicken and Egg Problem](https://garbe.io/blog/2020/02/24/cloudformation-resource-provider/)
* [Resolve the &quot;Resource timed out waiting for creation of physical resource&quot; error in AWS CloudFormation](https://aws.amazon.com/premiumsupport/knowledge-center/cloudformation-physical-resource-error/)
* [Deploying CloudFormation resource type](https://read.korzh.cloud/deploying-cloudformation-resource-type-64bfd5d14e6e)
