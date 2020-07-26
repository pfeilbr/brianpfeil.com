+++
author = "Brian Pfeil"
categories = ["Dockerfile", "playground"]
date = 2018-11-13
description = ""
summary = "learning AWS Ecr"
draft = false
slug = "aws-ecr"
tags = ["aws","ecr","github",]
title = "AWS Ecr"
repoFullName = "pfeilbr/aws-ecr-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-ecr-playground"
truncated = true

+++


* learn Amazon Elastic Container Registry
* [Docker Basics for Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-basics.html) tutorial

### Session

```sh
cd ~/projects
mkdir aws-ecr-playground
code aws-ecr-playground
touch Dockerfile
touch README.md
docker build -t hello-world .
touch .gitignore
docker build -t hello-world .
docker-machine ip
docker run -p 80:80 hello-world
docker-machine ip
aws ecr create-repository --repository-name hello-world
docker tag hello-world 529276214230.dkr.ecr.us-east-1.amazonaws.com/hello-world
$(aws ecr get-login --no-include-email)
docker push 529276214230.dkr.ecr.us-east-1.amazonaws.com/hello-world
```
