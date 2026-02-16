+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2021-04-02
description = ""
summary = " "
draft = false
slug = "api-gateway-service-integrations-for-http-apis"
tags = ["aws","api-gateway","eventbridge","cloudwatch","integration"]
title = "API Gateway Service Integrations for HTTP APIs"
repoFullName = "pfeilbr/api-gateway-service-integrations-for-http-apis-playground"
repoHTMLURL = "https://github.com/pfeilbr/api-gateway-service-integrations-for-http-apis-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/api-gateway-service-integrations-for-http-apis-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/api-gateway-service-integrations-for-http-apis-playground</a>
</div>


Example API Gateway service integration with EventBridge with [SAM](https://aws.amazon.com/serverless/sam/)

`API Gateway -> EventBridge -> CloudWatch Log Group`

## Running


```sh
cd eventbridge

# deploy
sam deploy --guided

# run following to given eventbridge rule permissions to write to log group
# can not create resource-based policy for Log Group via cfn
# see https://stackoverflow.com/questions/49242010/how-to-define-resource-policy-for-cloudwatch-logs-with-cloudformation
aws logs put-resource-policy \
    --region us-east-1 \
    --policy-name eventbridge-rule-to-logs \
    --policy-document '{ "Version": "2012-10-17", "Statement": [ {
        "Effect": "Allow", "Principal": { "Service": "events.amazonaws.com" },
        "Action":[ "logs:CreateLogStream", "logs:PutLogEvents" ],
        "Resource" : "arn:aws:logs:*:*:log-group:*" } ] }'

# send event to api gateway endpoint
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"detail":"{\"action\": \"withdrawal\", \"amount\": 100}"}' \
  https://8djn9e18ej.execute-api.us-east-1.amazonaws.com

# response: {"Entries":[{"EventId":"11555ee7-774f-e922-1022-46401bbe5f9b"}],"FailedEntryCount":0}

# view event in log group
aws logs tail "apigateway-http-api-service-integration/EventBus"

# response
# 2021-04-02T23:47:46+00:00 ca4b84fb-60f2-302d-b6ce-90338469d249 {"version":"0","id":"11555ee7-774f-e922-1022-46401bbe5f9b","detail-type":"MyDetailType","source":"demo","account":"529276214230","time":"2021-04-02T23:47:46Z","region":"us-east-1","resources":[],"detail":{"action":"withdrawal","amount":100}}

# cleanup
STACK_NAME="apig-svc-int-eb-cwl-01"
aws cloudformation delete-stack --stack-name $STACK_NAME
aws cloudformation wait stack-delete-complete --stack-name $STACK_NAME

```

## Screenshots

![aws logs tail output](https://www.evernote.com/l/AAGhwN9HdzBDQr8btg1JnU21bsyETK67NF8B/image.png)

![cloudwatch logs output](https://www.evernote.com/l/AAGNPTlsbFVPGJD5rauZvWI9f0BmOqN2MtEB/image.png)


## Resources

* [Working with AWS service integrations for HTTP APIs - Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-aws-services.html)

