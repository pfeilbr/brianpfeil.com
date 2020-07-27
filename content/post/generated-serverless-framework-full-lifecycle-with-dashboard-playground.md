+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-08-20
description = ""
summary = "experimenting with Serverless Framework Full Lifecycle With Dashboard"
draft = false
slug = "serverless-framework-full-lifecycle-with-dashboard"
tags = ["serverless","github",]
title = "Serverless Framework Full Lifecycle With Dashboard"
repoFullName = "pfeilbr/serverless-framework-full-lifecycle-with-dashboard-playground"
repoHTMLURL = "https://github.com/pfeilbr/serverless-framework-full-lifecycle-with-dashboard-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/serverless-framework-full-lifecycle-with-dashboard-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/serverless-framework-full-lifecycle-with-dashboard-playground</a>

# serverless-framework-full-lifecycle-with-dashboard-playground

learn and understand how [Serverless Framework – Now, Full Lifecycle](https://serverless.com/blog/serverless-now-full-lifecycle/) works.  This allows serverless to instrument code, send cloudwatch logs to the serverless SaaS.  This allows serverless to provide the [Serverless Dashboard](https://serverless.com/framework/docs/dashboard/) features

---

**Running `serverless` from cli to create project**

![](https://www.evernote.com/l/AAGMIc4-FIJCSZXUtSiZZqr-jnavut4x_A0B/image.png)

The `service`, `app`, and `org` top-level properties added to `serverless.yml` enable serverless full lifecycle / dashboard

```yaml
service: serverless-with-dashboard-playground-01
app: serverless-with-dashboard-playground-01
org: pfeilbr
```

![](https://www.evernote.com/l/AAH9J_9FRfFGH7uiu2JonnyeBowUC_-cU0kB/image.png)

To disable, add the following to `serverless.yml`

```yaml
custom:
  enterprise:
    collectLambdaLogs: false
```

Serverless framework creates a role during the deploy. This allows for the cloudwatch log group logs to be sent to serverless SaaS app.  e.g. `arn:aws:iam::529276214230:role/serverless-with-dashboard-EnterpriseLogAccessIamRo-19SDI69RM1KJ4`

![](https://www.evernote.com/l/AAFnznpUKxhHjIXCHwFwzUcmYXBdiLCgln0B/image.png)

inline policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:FilterLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:us-east-1:529276214230:log-group:/aws/lambda/serverless-with-dashboard-playground-01-dev-hello:*"
            ],
            "Effect": "Allow"
        }
    ]
}
```

trust relationship
> trust serverless aws account `802587217904`
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::802587217904:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "ServerlessEnterprise-LGGXBmZw2Z47MmWq6b"
        }
      }
    }
  ]
}
```

**Instrumented/wrapped Code Example**

On deploy, serverless instruments/wraps your code/handlers.  You don't see this locally in your codebase.  You only see on the deployment side in AWS.

![](https://www.evernote.com/l/AAHPyNZCdhlEwbjGnpVNd1Qr8IiEHLdfRB4B/image.png)

embedded/bundled serverless SDK
![](https://www.evernote.com/l/AAEWGJxVG6BCFY7nuiFMRRdiEeBOaC-ACjoB/image.png)


**`SERVERLESS_ENTERPRISE` wrapped log example**

serverless hooks logging to stdout and stderr via `serverlessSDK`.  This allows it to log structured JSON logs to cloudwatch logs with the prefix `SERVERLESS_ENTERPRISE`.  This logging is additional, the `console.log`s are logged independently.

![](https://www.evernote.com/l/AAGXImGSXy5ATKrP5-qDPHT3RMs7OfMMj9wB/image.png)

To see the log group subscription details

`aws logs describe-subscription-filters --log-group-name '/aws/lambda/serverless-with-dashboard-playground-01-dev-hello'`

```json
{
    "subscriptionFilters": [
        {
            "filterPattern": "?\"REPORT RequestId: \" ?\"SERVERLESS_ENTERPRISE\"",
            "filterName": "serverless-with-dashboard-playground-01-dev-CloudWatchLogsSubscriptionFilterHelloLogGroup-1SAKWRFMW5JHE",
            "creationTime": 1566318781436,
            "logGroupName": "/aws/lambda/serverless-with-dashboard-playground-01-dev-hello",
            "destinationArn": "arn:aws:logs:us-east-1:802587217904:destination:LGGXBmZw2Z47MmWq6b#VlGYyRJNfvVVgHf8y1#serverless-with-dashboard-playground-01#dev",
            "distribution": "ByLogStream"
        }
    ]
}
```

It sends logs to the serverless AWS account (`802587217904`).  The `destinationArn: arn:aws:logs:us-east-1:802587217904:destination:LGGXBmZw2Z47MmWq6b#VlGYyRJNfvVVgHf8y1#serverless-with-dashboard-playground-01#dev` is a [kinesis stream](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CreateDestination.html) within the serverless AWS account.

This is done via [Cross-Account Log Data Sharing with Subscriptions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CrossAccountSubscriptions.html)

---

**Serverless Dashboard | Views**

![](https://www.evernote.com/l/AAGYJOJTHApN_JpkCV9-zdcb715b6wEMRboB/image.png)

"safeguard policies" are evaluated on `serverless deploy`
![](https://www.evernote.com/l/AAHh34xEDRZPMZvdU3OB9gTRjZGuTcfWavsB/image.png)

![](https://www.evernote.com/l/AAHPvh8KYGtDzp-FJpeJJkD9YQMDlMoV_ZkB/image.png)

![](https://www.evernote.com/l/AAEQi7li2WpL-4bLb1_Ot_Gu582YPZrYh5oB/image.png)

![](https://www.evernote.com/l/AAFGw-o8o3VJP5LHwE3xALCQtHh-0MvopoYB/image.png)

![](https://www.evernote.com/l/AAHb32bKNhNB47q-tjd9FcBhpH4x0q0TXwMB/image.png)

![](https://www.evernote.com/l/AAHv-DCGUmxCG6nBhHqcJWf7WY15kUwoX8cB/image.png)

![](https://www.evernote.com/l/AAFSDTovX61GYqcknC4dRdTFafjVuAvuWFIB/image.png)

![](https://www.evernote.com/l/AAGF3ML-wkFM1bPRMMGiUtvsKzXxGmI1E3gB/image.png)

![](https://www.evernote.com/l/AAHY5jTZcXpLPJJwKhIsKWgRblpvrmHgXlsB/image.png)

Send notifications (e.g. email)

![](https://www.evernote.com/l/AAGxGtV1-idIoKXzkqvTi4PMf-zWDtoNMRcB/image.png)

![](https://www.evernote.com/l/AAEfN4z9jZZFVaDVyiQOBU1-FP9kIwZnmnEB/image.png)

---

## Resources

* [reddit | Serverless Framework now supports full lifecycle on AWS](https://www.reddit.com/r/aws/comments/cghxro/serverless_framework_now_supports_full_lifecycle/)


