+++
author = "Brian Pfeil"
categories = ["HTML", "playground"]
date = 2018-10-21
description = ""
summary = " "
draft = false
slug = "build-a-serverless-web-app-with-lambda-api-gateway-s3-dynamodb-and-cognito"
tags = ["serverless","lambda","s3","dynamodb","cognito","aws","api-gateway"]
title = "Build a Serverless Web App with Lambda, API Gateway, S3, DynamoDB and Cognito"
repoFullName = "pfeilbr/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito"
repoHTMLURL = "https://github.com/pfeilbr/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito</a>
</div>


* based on [Serverless Web Application Workshop](https://github.com/aws-samples/aws-serverless-workshops/blob/master/WebApplication/README.md) and [Build a Serverless Web Application](https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/)
* good example showing cognito registration, verification, and signin with S3 static website
    * see [`src/1_StaticWebHosting/website/js/cognito-auth.js`](https://github.com/pfeilbr/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/blob/master/src/1_StaticWebHosting/website/js/cognito-auth.js) for details register, verify, signin
        * `WildRydes.authToken` method
        ![](https://www.evernote.com/l/AAHZxEdxOZtIdLlWyw2Qkz5qyv4K_UGkRKAB/image.png)
        * authorized API Gateway request
        ![](https://www.evernote.com/l/AAElbTXGfHhK5ZyctvX55_Za4AUKChN7uIEB/image.png)

    > NOTE: web in browser cognito SDK stores identity (JWT token) information in `localStorage`.  This is what allows maintaining session credentials across page reloads.
