+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2017-11-11
description = ""
summary = " "
draft = false
slug = "aws-ecs"
tags = ["aws","ecs",]
title = "AWS ECS"
repoFullName = "pfeilbr/aws-ecs-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-ecs-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-ecs-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-ecs-playground</a>
</div>


learn [AWS ECS](https://aws.amazon.com/documentation/ecs/)

### Session Steps

> following steps are based on <http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_tutorial.html>

```sh
# configure ecs-cli
ecs-cli configure profile --profile-name ecs-cluster-01 --access-key <YOUR KEY> --secret-key <YOUR SECRET>
ecs-cli configure --cluster cluster01 --region us-east-1 --config-name cluster01

# create 1 node cluster
ecs-cli up --keypair brianpfeil --capability-iam --size 1 --instance-type t2.micro

# create node app
cd simple-node
docker build -t pfeilbr/simple-node .
docker push pfeilbr/simple-node

# NOTE: pfeilbr/simple-node docker image is referenced by docker-compose.yml

ecs-cli compose up
ecs-cli ps # shows ip and port.  see https://www.evernote.com/l/AAET15kkH-dNhoxA67iDXzzSmR6DBjWtC00B/image.png
open http://34.237.144.74 # see https://www.evernote.com/l/AAE7iN32poNDwJTGe6T8QYX875Rz4jbJwHYB/image.png
ecs-cli compose down

# make changes to server.js

# rebuild image
docker build -t pfeilbr/simple-node .

# test locally
docker run -p 49160:8080 -d pfeilbr/simple-node

# open locally
open http://localhost:49160

# push
docker push pfeilbr/simple-node

# make changes to docker-compose.yml if neccessary
ecs-cli compose up

# scale cluster to 2 nodes
ecs-cli scale --capability-iam --size 2

# scale simple-node across 2 nodes
ecs-cli compose scale 2

# create a service.  defaults to 1 task.
# if task dies, service will automatically restart it
# e.g. try /kill path of web app, which calls process.exit(1).  
# it will start a new container instance within a few seconds
ecs-cli compose service up # be sure to run "ecs-cli compose down" first

# delete service
ecs-cli compose service down

# delete cluster
ecs-cli down --force

```

### Resources

* [Installing the Amazon ECS CLI](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_installation.html)
* [Configuring the Amazon ECS CLI](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_Configuration.html)
* [Amazon ECS CLI Tutorial](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_tutorial.html)
* [Dockerizing a Node.js web app](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)



