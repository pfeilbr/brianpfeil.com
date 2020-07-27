+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2020-05-19
description = ""
summary = "learning AWS Eventbridge"
draft = false
slug = "aws-eventbridge"
tags = ["aws","eventbridge","github",]
title = "AWS Eventbridge"
repoFullName = "pfeilbr/aws-eventbridge-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-eventbridge-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/aws-eventbridge-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-eventbridge-playground</a>


learn [AWS EventBridge](https://aws.amazon.com/eventbridge/)

```sh
# put events on default event bus
aws events put-events --entries file://sample-events/my-custom-app-events.json
```

## Resources

* <https://github.com/jbesw/s3-to-lambda/blob/master/eventbridge/README.md> - examples using `AWS::Events::Rule` in SAM to map event sources to targets (e.g. lambda, kinesis, etc.)


