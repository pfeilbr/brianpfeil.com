+++
author = "Brian Pfeil"
categories = ["TypeScript", "playground"]
date = 2017-05-21
description = ""
summary = "learn AWS Cloudwatch"
draft = false
slug = "aws-cloudwatch"
tags = ["aws","playground",]
title = "AWS Cloudwatch"
repoFullName = "pfeilbr/aws-cloudwatch-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-cloudwatch-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-cloudwatch-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-cloudwatch-playground</a>
</div>


## CloudWatch Metrics

see JavaScript API examples at [src/main.ts](src/main.ts)

**Run Examples**

`npm run test`

## CloudWatch Logs

**Concepts**

- group contains streams
- stream contains events
- event is a log line

**aws cli examples**

```sh
aws logs describe-log-groups

# all lambda functions
aws logs describe-log-groups --log-group-name-prefix /aws/lambda

# streams for a specific lambda function
aws logs describe-log-streams --log-group-name /aws/lambda/consent-hub-api-dev-consentDefinition

# fetch all events for a specific stream
aws logs get-log-events --log-group-name /aws/lambda/consent-hub-api-dev-consentDefinition --log-stream-name '2017/03/17/[$LATEST]cc78c1c997ff45fb85011a0c3abb178d'
```

**CloudWatch Insights CLI Example**

```sh
# times are specified in epoch
# see https://www.epochconverter.com/
aws logs start-query \
--log-group-name '/aws/events/all-events-01' \
--start-time '1578531600' \
--end-time '1578618000' \
--query-string 'fields @timestamp, @message | sort @timestamp desc | limit 20'

{
    "queryId": "c9b7d9e8-b32f-486d-a436-6ce43db8d54c"
}

aws logs get-query-results --query-id 'c9b7d9e8-b32f-486d-a436-6ce43db8d54c'

{
    "status": "Complete", 
    "statistics": {
        "recordsMatched": 68.0, 
        "recordsScanned": 68.0, 
        "bytesScanned": 107681.0
    }, 
    "results": [
        [
            {
                "field": "@timestamp", 
                "value": "2020-01-09 16:29:26.000"
            }, 
            {
                "field": "@message", 
                "value": "{\"version\":\"0\",\"id\":\"6d59ca00-2144-0ec7-ff0f-1990f3929072\",\"detail-type\":\"AWS API Call via CloudTrail\",\"source\":\"aws.cloudformation\",\"account\":\"529276214230\",\"time\":\"2020-01-09T16:29:26Z\",\"region\":\"us-east-1\",\"resources\":[],\"detail\":{\"eventVersion\":\"1.05\",\"userIdentity\":{\"type\":\"IAMUser\",\"principalId\":\"AIDAJO5XRTLUILQNKZVSE\",\"arn\":\"arn:aws:iam::529276214230:user/admin\",\"accountId\":\"529276214230\",\"accessKeyId\":\"ASIAXWO2SDPLOKK7GENS\",\"userName\":\"admin\",\"sessionContext\":{\"attributes\":{\"mfaAuthenticated\":\"false\",\"creationDate\":\"2020-01-09T16:28:29Z\"}},\"invokedBy\":\"signin.amazonaws.com\"},\"eventTime\":\"2020-01-09T16:29:26Z\",\"eventSource\":\"cloudformation.amazonaws.com\",\"eventName\":\"DeleteStack\",\"awsRegion\":\"us-east-1\",\"sourceIPAddress\":\"100.11.96.70\",\"userAgent\":\"signin.amazonaws.com\",\"requestParameters\":{\"stackName\":\"arn:aws:cloudformation:us-east-1:529276214230:stack/my-sam-app01/b3d67b30-32ec-11ea-b778-0afe492705d7\"},\"responseElements\":null,\"requestID\":\"1f303924-8097-4684-bb81-1e8366818e88\",\"eventID\":\"b7bd4f10-6ef6-4931-9254-5c4588cd0b4a\",\"eventType\":\"AwsApiCall\"}}"
            }, 
            {
                "field": "@ptr", 
                "value": "CmMKKgomNTI5Mjc2MjE0MjMwOi9hd3MvZXZlbnRzL2FsbC1ldmVudHMtMDEQBxI1GhgCBd/UPAoAAAAAOW7swAAF4XVHwAAAAaIgASjwxI7Z+C0w8MSO2fgtOAFA0whI9DJQ+yQQABgB"
            }
        ], 
        ...
    ]
}
```



