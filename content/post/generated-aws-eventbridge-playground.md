+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2020-05-19
description = ""
summary = " "
draft = false
slug = "aws-eventbridge"
tags = ["aws","eventbridge","playground",]
title = "AWS Eventbridge"
repoFullName = "pfeilbr/aws-eventbridge-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-eventbridge-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-eventbridge-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-eventbridge-playground</a>
</div>


learn [AWS EventBridge](https://aws.amazon.com/eventbridge/)

```sh
# put events on default event bus
aws events put-events --entries file://sample-events/my-custom-app-events.json
```

## Resources

* <https://github.com/jbesw/s3-to-lambda/blob/master/eventbridge/README.md> - examples using `AWS::Events::Rule` in SAM to map event sources to targets (e.g. lambda, kinesis, etc.)


