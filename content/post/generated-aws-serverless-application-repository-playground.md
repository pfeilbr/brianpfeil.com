+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-10-14
description = ""
summary = "learn AWS Serverless Application Repository"
draft = false
slug = "aws-serverless-application-repository"
tags = ["aws","serverless","playground",]
title = "AWS Serverless Application Repository"
repoFullName = "pfeilbr/aws-serverless-application-repository-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-serverless-application-repository-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-serverless-application-repository-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-serverless-application-repository-playground</a>
</div>


learn [AWS Serverless Application Repository](https://docs.aws.amazon.com/en_pv/serverlessrepo)

## Example using SAM CLI

```sh
# define deployment bucket
BUCKET="sam-deploy-bucket-01"

# init sam app
sam init --runtime nodejs
cd sam-app

# " create a Lambda deployment package".
# add Metadata section to `template.yml`. see https://docs.aws.amazon.com/en_pv/serverlessrepo/latest/devguide/serverlessrepo-quick-start.html#serverlessrepo-quick-start-hello-world-package-app

# package
sam package \
    --template-file template.yaml \
    --output-template-file packaged.yaml \
    --s3-bucket $BUCKET

# publish to SAR.  will be private by default
sam publish \
    --template packaged.yaml \
    --region us-east-1

# create SAM app to consume SAR (embedded SAR)
# embed SAR (`Type: AWS::Serverless::Application`) in template.  see https://docs.aws.amazon.com/en_pv/serverless-application-model/latest/developerguide/serverless-sam-template.html#serverless-sam-template-application
touch embed-serverless-application.yaml

# package embedded app
sam package \
    --template-file embed-serverless-application.yaml \
    --output-template-file embed-serverless-application-packaged.yaml \
    --s3-bucket $BUCKET

# define name for stack
STACK_NAME="embed-serverless-application"

# deploy embedded app.  note usage of `CAPABILITY_AUTO_EXPAND` param
sam deploy --template-file ./embed-serverless-application-packaged.yaml --stack-name "$STACK_NAME" --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND

# two stacks are created.  the parent (sam-app/embed-serverless-application-packaged.yaml) and the emb embedded SAR (packaged.yaml)

# cleanup / remove stack(s)
aws cloudformation delete-stack --stack-name "$STACK_NAME"
```

SAR App in Console

![](https://www.evernote.com/l/AAHSgG3f8apCC5F6fvQ178_xBzILM6IP110B/image.png)

Nested CFN Stacks

![](https://www.evernote.com/l/AAHO3LiMwJ1MeKiiqKxCk4yW10qtVMdusyMB/image.png)

---

## Example using `aws serverlessrepo` CLI

> can also be done (and is preferred) via sam cli.  see above.

```sh
mkdir sar-cli-example
cd sar-cli-example

APP_NAME=myapp01

aws serverlessrepo list-applications

# create appliction
aws serverlessrepo create-application \
--author 'Brian Pfeil' \
--description $APP_NAME \
--name $APP_NAME \
--semantic-version 0.0.1 \
--template-body file://./s3-bucket-template.yaml

# fetch ApplicationId
APP_ID=$(aws serverlessrepo list-applications | jq --raw-output ".Applications[] | select(.Name == \"$APP_NAME\").ApplicationId")

# create request to create cfn template (async operation)
TEMPLATE_ID=$(aws serverlessrepo create-cloud-formation-template --application-id "$APP_ID" | jq --raw-output ".TemplateId")

# fetch the cfn template
TEMPLATE_URL=$(aws serverlessrepo get-cloud-formation-template --application-id "$APP_ID" --template-id "$TEMPLATE_ID" | jq --raw-output ".TemplateUrl")

# view cfn template
curl "$TEMPLATE_URL"

# delete app
aws serverlessrepo delete-application --application-id "$APP_ID"

```


