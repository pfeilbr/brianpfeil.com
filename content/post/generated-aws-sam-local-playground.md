+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2019-08-16
description = ""
summary = "learning AWS SAM Local"
draft = false
slug = "aws-sam-local"
tags = ["aws","sam","github",]
title = "AWS SAM Local"
repoFullName = "pfeilbr/aws-sam-local-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-sam-local-playground"
truncated = true

+++


learn [aws-sam-local](https://github.com/awslabs/aws-sam-local)

### session
```sh
cd examples/hello-world

sam local invoke "HelloWorld" -e event.json
echo '{"name": "Brian" }' | sam local invoke "HelloWorld"

# debugging
# ensure launch.json localRoot is set to directory where index.js or code exists
# e.g. "localRoot": "${workspaceRoot}/examples/hello-world"
sam local invoke -e event.json -d 5858 HelloWorld

# set breakpoints in code (vscode)
# then run debug in vscode

# package
# NOTE: bucket must exist (`aws s3 mb s3://sam-deploy-bucket-01`)
sam package --template-file template.yaml --s3-bucket sam-deploy-bucket-01 --output-template-file packaged.yaml

# deploy
sam deploy --template-file packaged.yaml --stack-name sam-hello-world-v0 --capabilities CAPABILITY_IAM

# invoke
# NOTE: you'll need to lookup the "full" function name
aws lambda invoke --function-name "sam-hello-world-v1-HelloWorld-L8DLT50DZNIJ" --payload '{"name": "brian"}' output.log; cat output.log

# view logs
sam logs -n HelloWorld --stack-name sam-hello-world-v1

# ---

# invoke lambda via api gateway example
cd examples/api-event-source

# local development
sam local start-api
curl http://127.0.0.1:3000/

# package
# NOTE: bucket must exist (`aws s3 mb s3://sam-deploy-bucket-01`)
sam package --template-file template.yaml --s3-bucket sam-deploy-bucket-01 --output-template-file packaged.yaml

# deploy
sam deploy --template-file packaged.yaml --stack-name api-event-source-v1 --capabilities CAPABILITY_IAM
```

### Resources

* [AWS Serverless Application Model (AWS SAM) Documentation](https://docs.aws.amazon.com/serverless-application-model/index.html)
