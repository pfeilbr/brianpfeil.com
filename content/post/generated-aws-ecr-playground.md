+++
author = "Brian Pfeil"
categories = ["Dockerfile", "playground"]
date = 2018-11-13
description = ""
summary = " "
draft = false
slug = "aws-ecr"
tags = ["aws","ecr","playground",]
title = "AWS ECR"
repoFullName = "pfeilbr/aws-ecr-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-ecr-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-ecr-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-ecr-playground</a>
</div>


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


