+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2019-07-03
description = ""
summary = "learning AWS Codebuild Local"
draft = false
slug = "aws-codebuild-local"
tags = ["aws","codebuild","github",]
title = "AWS Codebuild Local"
repoFullName = "pfeilbr/aws-codebuild-local-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-codebuild-local-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/aws-codebuild-local-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-codebuild-local-playground</a>


## Resources

* [Announcing Local Build Support for AWS CodeBuild](https://aws.amazon.com/blogs/devops/announcing-local-build-support-for-aws-codebuild/)

## Running

```sh
# build CodeBuild image locally 
git clone https://github.com/aws/aws-codebuild-docker-images.git
cd aws-codebuild-docker-images/ubuntu/standard/2.0
docker build -t aws/codebuild/standard:2.0 .

# pull  CodeBuild local agent
docker pull amazon/aws-codebuild-local:latest --disable-content-trust=false

# cd to directory containing `buildspec.yml`
# NOTE: script was previously downloaded to `~/bin/codebuild_build.sh`
cd basic-01
codebuild_build.sh -i 'aws/codebuild/standard:2.0' -a 'artifact-output' -c

```




