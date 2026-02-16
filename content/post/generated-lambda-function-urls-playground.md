+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2022-04-09
description = ""
summary = " "
draft = false
slug = "lambda-function-urls"
tags = ["lambda","aws","http"]
title = "Lambda Function Urls"
repoFullName = "pfeilbr/lambda-function-urls-playground"
repoHTMLURL = "https://github.com/pfeilbr/lambda-function-urls-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/lambda-function-urls-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/lambda-function-urls-playground</a>
</div>


learn [Lambda function URLs](https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html)

## Notes

- > Function URLs are best for use cases where you must implement a single-function microservice with a public endpoint that doesn’t require the advanced functionality of API Gateway, such as request validation, throttling, custom authorizers, custom domain names, usage plans, or caching.
- Function URL format `https://<url-id>.lambda-url.<region>.on.aws`
- removes the 29s API Gateway limitation.  your fn can take 15 min to respond and there is no timeout
- [unexpected function URL caching can cause issues](https://twitter.com/marcinph/status/1511995646953377792?s=20&t=DtKC3pq7lms95Y0J3w3_XA)
- > You can throttle the rate of requests that your Lambda function processes through a function URL by configuring reserved concurrency. Reserved concurrency limits the number of maximum concurrent invocations for your function. Your function's maximum request rate per second (RPS) is equivalent to 10 times the configured reserved concurrency. For example, if you configure your function with a reserved concurrency of 100, then the maximum RPS is 1,000.
- can limit invocations via lambda condiation keys
  - [AWS Lambda - Permissions - Policy conditions](https://docs.aws.amazon.com/lambda/latest/dg/lambda-api-permissions-ref.html#authorization-conditions)
  - [Condition keys for AWS Lambda](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awslambda.html#awslambda-policy-keys)
  - [aws:SourceIp](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-sourceip) - can limit lambda invocation by source ip address


## Demo

see [`template.yaml`](https://github.com/pfeilbr/lambda-function-urls-playground/blob/master/template.yaml)

```
# deploy
sam deploy --guided

# access lambda url
curl https://klm4pgp5qacvq52o4zptf6avei0cuczb.lambda-url.us-east-1.on.aws/
```

![](https://www.evernote.com/l/AAF76pWkKC1OwaUEnrtqZHFPIhVe0G07S3EB/image.png)

## Resources

- [Lambda function URLs](https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html)
- [Announcing AWS Lambda Function URLs: Built-in HTTPS Endpoints for Single-Function Microservices](https://aws.amazon.com/blogs/aws/announcing-aws-lambda-function-urls-built-in-https-endpoints-for-single-function-microservices/)
- [Adding a function URL to a CloudFormation template](https://docs.aws.amazon.com/lambda/latest/dg/urls-configuration.html#urls-cfn)
- [SCP to prevent people from creating open Lambda URLs](https://twitter.com/ben11kehoe/status/1511857782298882050?s=20&t=DtKC3pq7lms95Y0J3w3_XA)
- [use case discussion](https://twitter.com/ben11kehoe/status/1512115496761536512?s=20&t=DtKC3pq7lms95Y0J3w3_XA)

