+++
author = "Brian Pfeil"
categories = ["Dockerfile", "playground"]
date = 2022-01-17
description = ""
summary = " "
draft = false
slug = "aws-vscode-dev-container"
tags = ["aws",]
title = "AWS Vscode Dev Container"
repoFullName = "pfeilbr/aws-vscode-dev-container"
repoHTMLURL = "https://github.com/pfeilbr/aws-vscode-dev-container"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-vscode-dev-container" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-vscode-dev-container</a>
</div>


a vscode devcontainer for aws development

> Visual Studio Code Remote - Containers extension lets you use a Docker container as a full-featured development environment. It allows you to open any folder inside (or mounted into) a container and take advantage of Visual Studio Code's full feature set.

---

## Usage

To use this repo as a template for an AWS project

```sh
gh repo clone pfeilbr/aws-vscode-dev-container my-aws-project
cd my-aws-project
sam init
```

## Install into existing repo

```sh
mkdir -p .devcontainer
pushd .devcontainer
curl -O https://raw.githubusercontent.com/pfeilbr/aws-vscode-dev-container/master/.devcontainer/Dockerfile
curl -O https://raw.githubusercontent.com/pfeilbr/aws-vscode-dev-container/master/.devcontainer/devcontainer.json
curl -O https://raw.githubusercontent.com/pfeilbr/aws-vscode-dev-container/master/.devcontainer/postCreateCommand.sh
chmod +x postCreateCommand.sh
popd
```

## Login with AWS SSO

* see <https://gist.github.com/pahud/ba133985e1cf3531c09b5ea553a72739>

```sh
mkdir ~/.bin && cd $_
wget https://raw.githubusercontent.com/pahud/vscode/main/.devcontainer/bin/aws-sso-credential-process && \
chmod +x aws-sso-credential-process


aws configure set credential_process ${HOME}/.bin/aws-sso-credential-process
touch ~/.aws/credentials && chmod 600 $_
aws configure sso --profile default
```

---

## Configuration

```sh
# aws credentials are mounted into the guest container via `~/.aws`s
# source=/home/ec2-user/.aws,target=/root/.aws
``

---

## TODO

* ...

---

## Files

* [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json)
* [`.devcontainer/Dockerfile`](.devcontainer/Dockerfile)

---

## Resources

* [Developing inside a Container](https://code.visualstudio.com/docs/remote/containers)



