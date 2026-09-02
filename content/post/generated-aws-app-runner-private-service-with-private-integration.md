+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2023-09-15
description = ""
summary = " "
draft = false
slug = "aws-app-runner-private-service-with-private-integration"
tags = ["aws"]
title = "AWS App Runner Private Service with Private Integration"
repoFullName = "pfeilbr/aws-app-runner-private-service-with-private-integration"
repoHTMLURL = "https://github.com/pfeilbr/aws-app-runner-private-service-with-private-integration"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-app-runner-private-service-with-private-integration" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-app-runner-private-service-with-private-integration</a>
</div>


based on [KarlDeux/arps](https://github.com/KarlDeux/arps)

- 

## Demo

```sh
export AWS_PROFILE="hub01-admin"
export STACK_NAME=aws-app-runner-private-service-with-private-integration
export REGION=us-east-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

sam build --use-container

sam deploy --guided
sam deploy

aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --region $REGION \
  --query 'Stacks[0].Outputs' \
  > stack-outputs.json

# get default vpc id
export DEFAULT_VPC_ID=$(aws ec2 describe-vpcs --region $REGION  --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text)

aws ec2 describe-subnets --filters "Name=vpc-id,Values=${DEFAULT_VPC_ID}" --query "Subnets[].SubnetId" --output text


sam delete --no-prompts

aws cloudformation delete-stack --stack-name $STACK_NAME

# login to ecr from docker
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

docker build -t hello-world-express .
docker run -p 8000:8000 hello-world-express
docker tag hello-world-express:latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$STACK_NAME
docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$STACK_NAME
docker pull "${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${STACK_NAME}:latest"


# deployment and event logs
/aws/apprunner/code-based-private-endpoint-1/58b5e70db6aa4481b6cf42ca0c38b5f9/service

# application logs
/aws/apprunner/private-endpoint-1/cc0078056c7d48ab9b434dfcadc796f3/application

# test the enpoint.  this public apig endpoint calls a lambda fn in vpc that calls private app runner services
watch curl https://r4d8inqs3m.execute-api.us-east-1.amazonaws.com/Prod/test

# pause all services
json_data=$(cat aws-app-runner-list-services.json)

# Get the length of the array within the "ServiceSummaryList" property
length=$(echo $json_data | jq '.ServiceSummaryList | length')

# Loop over each element in the array
for (( i=0; i<$length; i++ )); do
  # Extract the object at index $i within the "ServiceSummaryList" array
  object=$(echo $json_data | jq -c ".ServiceSummaryList[$i]")

  # Extract the 'ServiceName' field from the object
  service_name=$(echo $object | jq -r '.ServiceName')
  service_id=$(echo $object | jq -r '.ServiceId')
  service_arn=$(echo $object | jq -r '.ServiceArn')

  # Print out the ServiceName
  echo "Pausing ServiceName: $service_name"
  aws apprunner pause-service --service-arn "${service_arn}"
done

```

- log types - event logs (`/aws/apprunner/code-based-private-endpoint-1/ba93db338128426481f912edc4d493c1/service/events`), deployment logs (`/aws/apprunner/code-based-private-endpoint-1/ba93db338128426481f912edc4d493c1/service/deployment/<deployment_id>`), application logs

## TODO

- private service only accessible via VPC
- private integration only accessible via VPC. e.g. RDS DB in private subnet
- testing - apig -> lambda with VPC access/config to test private app runner service.  this is a lot easier than running ec2 in a VPC

## screenshots

![App Runner Console | Services](https://www.evernote.com/shard/s1/sh/88efe5b9-2026-479a-805a-45eeaa8f5116/Wc9AM0uP5TzkoAvsdQD4qJRt9y_uFS_5ud-qPN7RyZ8C61qiPJy0ThTTSQ/deep/0/image.png)

![App Runner Console | Service Detail View](https://www.evernote.com/shard/s1/sh/7b8db5c2-c94b-4816-b8ea-44b793009a70/79hssC8rmg7EKpAcAIfULgZAMUNIRX7LCQWeBLBaQd3F1eMWNt-zTJDGzQ/deep/0/image.png)

![App Runner Console | Service Detail View | Deployment Logs](https://www.evernote.com/shard/s1/sh/6a3a5d1e-4f33-4aa8-bbc9-7ea09028c664/fQLL1ac2vuxEmKIYW8mzvmsUQ8Ke2SMY0stWe6g2u2v9cega-Q9picndVQ/deep/0/image.png)

![](https://www.evernote.com/shard/s1/sh/9fd913ef-76ea-46bc-97d4-4a2c8e8ac988/iu3nUqPrG6gHYybuZ1uJMpoKgoE1JAzB6FSpBQfIbMnj1PfSfDdiCAJf4w/deep/0/image.png)

![CloudWatch Service and Application Log Groups](https://www.evernote.com/shard/s1/sh/6ba3c250-3a77-4d6c-824c-40a27ab97450/533D1VwdCbYQulF-DlkD12tNLVhbb0HYFC8K76L5M1Q_O6DtPMl5U0mm1g/deep/0/image.png)

## Resources

- [KarlDeux/arps](https://github.com/KarlDeux/arps)
- [Image-based service](https://docs.aws.amazon.com/apprunner/latest/dg/service-source-image.html) - container image (docker)
- [Code-based service](https://docs.aws.amazon.com/apprunner/latest/dg/service-source-code.html) - source code and a supported runtime ([managed platforms](https://docs.aws.amazon.com/apprunner/latest/dg/service-source-code.html#service-source-code.managed-platforms).  e.g. python, node.js, java, .net, php, ruby, go)
- [configuration file](https://docs.aws.amazon.com/apprunner/latest/dg/config-file.html) ([`apprunner.yaml`](https://docs.aws.amazon.com/apprunner/latest/dg/config-file-examples.html)).
- [Enabling Private endpoint for incoming traffic](https://docs.aws.amazon.com/apprunner/latest/dg/network-pl.html)
- [AWS::AppRunner::VpcIngressConnection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html) - associate your App Runner service to an Amazon VPC endpoint
- [AWS::AppRunner::VpcIngressConnection.DomainName](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcingressconnection.html#DomainName-fn::getatt). build URL with `!Sub https://${AppRunnerService1VpcIngressConnection.DomainName}`
- [AWS::EC2::VPCEndpoint](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html) with `ServiceName: !Sub "com.amazonaws.${AWS::Region}.apprunner.requests"`
- see [KarlDeux/arps/template.yaml](https://github.com/KarlDeux/arps/blob/master/template.yaml) for full example.
- [Enabling VPC access for outgoing traffic](https://docs.aws.amazon.com/apprunner/latest/dg/network-vpc.html)
- [AWS::AppRunner::VpcConnector](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apprunner-vpcconnector.html)
- [Using Amazon ECR with the AWS CLI](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html)
- [How do I connect to my Amazon RDS for PostgreSQL or Amazon Aurora PostgreSQL using IAM authentication?](https://repost.aws/knowledge-center/rds-postgresql-connect-using-iam)
