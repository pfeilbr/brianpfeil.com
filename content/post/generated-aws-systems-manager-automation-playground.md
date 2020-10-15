+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2020-10-02
description = ""
summary = " "
draft = false
slug = "aws-systems-manager-automation"
tags = ["aws",]
title = "AWS Systems Manager Automation"
repoFullName = "pfeilbr/aws-systems-manager-automation-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-systems-manager-automation-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-systems-manager-automation-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-systems-manager-automation-playground</a>
</div>


learn [AWS Systems Manager Automation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html)

**SSM Automation document**

* contains one or more steps that run in sequential order
* Each step is built around a single action
* Output from one step can be used as input in a later step
* json or yaml documents

## Resources

* [AWS Systems Manager Automation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html)
* [Custom Automation document samples](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-document-samples.html)
* [Automation actions reference](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-actions.html) - actions that you can specify in an AWS Systems Manager Automation document
    * [aws:executeScript – Run a script](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-action-executeScript.html) - runtimes: python3.6 | python3.7 | PowerShell Core 6.0, as of 2020-10-02 max duration of 10 min (600 secs)
    * [aws:executeAwsApi – Call and run AWS API actions](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-action-executeAwsApi.html)
* [Walkthrough: Using Automation with Jenkins](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-jenkins.html)
* [ceshihao/ssm-public-documents](https://github.com/ceshihao/ssm-public-documents) - example ssm automation documents


