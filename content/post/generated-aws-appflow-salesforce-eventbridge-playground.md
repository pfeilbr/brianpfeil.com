+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2020-08-27
description = ""
summary = " "
draft = false
slug = "aws-appflow-salesforce-eventbridge"
tags = ["aws","appflow","salesforce","eventbridge"]
title = "AWS AppFlow Salesforce EventBridge"
repoFullName = "pfeilbr/aws-appflow-salesforce-eventbridge-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-appflow-salesforce-eventbridge-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-appflow-salesforce-eventbridge-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-appflow-salesforce-eventbridge-playground</a>
</div>


[AWS AppFlow](https://aws.amazon.com/appflow/) example of salesforce event -> AppFlow -> EventBridge -> CloudWatch Logs.  Followed steps in [Building Salesforce integrations with Amazon EventBridge and Amazon AppFlow | Amazon Web Services](https://aws.amazon.com/blogs/compute/building-salesforce-integrations-with-amazon-eventbridge/) post.

## Notes

* observed low latency - AppFlow flow runs within 2 seconds of event being generated in salesforce.
* only fields specified in mapping are passed to EventBridge as properties of `detail`.
* [Private Amazon AppFlow flows](https://docs.aws.amazon.com/appflow/latest/userguide/private-flows.html) is available for salesforce that uses AWS PrivateLink to route data over AWS infrastructure without exposing it to the public internet

## Screenshot Tour

Turn on Change Data Capture for the relevant objects in salesforce
![](https://www.evernote.com/l/AAFmryV0UxVKY5eprjjdQ-_4IgJG7JvB5AAB/image.png)

Error when CDC is not turned on in salesforce for the object
![](https://www.evernote.com/l/AAEDjQW7qIpJ7azu59MIH05tvwqdqYOjrbsB/image.png)

AppFlow leverages already installed/available "Amazon AppFlow Embedded Login App" Connected App in salesforce

![](https://www.evernote.com/l/AAEyS5AOJn9F8pnZVMiV0Up7f5ydSNPApQwB/image.png)

![](https://www.evernote.com/l/AAGR_pfFpElDa4WwFTLoHEtGhpPxDKREPnoB/image.png)

![](https://www.evernote.com/l/AAEG72PQcHlNhrTqGdsmhe0DrtStP8VuCnE)

![](https://www.evernote.com/l/AAH8LLu9mOVJar3EgvmDvSsLrEA4yFQehs8B/image.png)

Run History
![](https://www.evernote.com/l/AAFPHkqjr_FJ1qtyysG35f8dO4wyIHz3DywB/image.png)

Event in CloudWatch Logs
![](https://www.evernote.com/l/AAFpH1Az7IlBUavypLjw4LahE90ppWrjy0AB/image.png)

AppFlow Mapping
![](https://www.evernote.com/l/AAEG72PQcHlNhrTqGdsmhe0DrtStP8VuCnEB/image.png)

## Resources

* [Building Salesforce integrations with Amazon EventBridge and Amazon AppFlow | Amazon Web Services](https://aws.amazon.com/blogs/compute/building-salesforce-integrations-with-amazon-eventbridge/)
