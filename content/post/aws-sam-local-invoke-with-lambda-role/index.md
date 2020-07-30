+++
title = "AWS SAM Local Invoke with Lambda Role"
slug = "aws-sam-local-invoke-with-lambda-role"
author = "Brian Pfeil"
date = "2020-07-30"
lastmod = "2020-07-30"
draft = false
categories = ["aws", "sam", "lambda"]
tags = ["aws", "sam", "lambda"]
summary = "Running lambda locally with SAM in the lambda role security context"

+++

[AWS Serverless Application Model](https://aws.amazon.com/serverless/sam/) (SAM) allows you to develop and test your lambda backed API Gateway endpoints locally via [sam local start-api](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-start-api.html).  By default, your function is invoked with the default credentials you have configured for the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).  If your function accesses other AWS services, it may encounter permission issues.  It's ideal to have your lambda run under as close to the same security context locally as it would when deployed.  In the example below, lambda sends a message to a SQS worker queue.  The permissions for the queue are configured to allow the lambda role to send a message to it.  The following details how to achieve this.

### Allowing Our Lambda Role to be Assumed

In our scenario, we have a local user profile named `admin` stored in `~/.aws/credentials`

```
[admin]
aws_access_key_id     = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

This user needs to be able to assume our `my-lambda-role` role.  We define the following **Role Trust** policy to enable:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::xxxxxxxxxxxx:user/admin"
      },
      "Action": "sts:AssumeRole"
    }
  ]

```

### Configure Assume Role via AWS CLI

Next we need to configure the AWS CLI to assume a role.  We can do so by adding the following to `~/.aws/config`

```
# ~/.aws/config

[profile my-lambda-role]
role_arn = arn:aws:iam::xxxxxxxxxxxx:role/my-lambda-role
source_profile = admin
output = json
region = us-east-1
```

Note the `source_profile = admin` line.  This identifies the profile in `~/.aws/credentials` that will be used to assume the role.

> See [How do I assume an IAM role using the AWS CLI?](https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/) for full details on options.

We can test with the following:

```sh
aws --profile my-lambda-role sts get-caller-identity
```

If successful, the response will look like.

```json
{
    "UserId": "AROAXWO2SDPLLBS55Q345:botocore-session-1596129185",
    "Account": "xxxxxxxxxxxx",
    "Arn": "arn:aws:sts::529276214230:assumed-role/my-lambda-role/botocore-"
}
```

### Running SAM Local

The SQS queue URL is provided to the lambda via an environment variable.  This is defined in the SAM template

`template.yaml`

```yaml
Environment:
    Variables:
        QUEUE_URL: !Ref Queue
```

We need `QUEUE_URL` to be available to our function running locally.  To do that we can create an environment variable .json file and pass as a parameter for sam local to use.

`env-vars.json`

```json
{
    "Parameters": {
        "QUEUE_URL": "https://sqs.us-east-1.amazonaws.com/xxxxxxxxxxxx/aws-sam-golang-example-Queue-Q12J860AETTS"
    }
}
```


We can now start the local SAM API server and test our endpoint

```sh
sam local start-api --profile my-lambda-role --env-vars env-vars.json

curl -X POST http://127.0.0.1:3000/job -d '{"name": "my job"}'
```

### Conclusion

We've seen how to run a lambda locally with the same security context as when deployed.  SAM provides a great development workflow to allow quick iterations.  The local environment provided via docker tries to be as true to AWS itself, but you should always test a fully deployed solution.

One point to note, you must have the AWS resources your lambda is interacting with provisioned.  For example, the SQS queue must exist.  SAM does not provide a locally running SQS service.




