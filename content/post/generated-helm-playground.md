+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2023-02-17
description = ""
summary = " "
draft = false
slug = "helm"
tags = ["kubernetes"]
title = "Helm"
repoFullName = "pfeilbr/helm-playground"
repoHTMLURL = "https://github.com/pfeilbr/helm-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/helm-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/helm-playground</a>
</div>


learn [Helm](https://helm.sh/) - The package manager for Kubernetes

## concepts

- similar to apt, yum, homebrew, but for k8s
- Helm is the only package manager specifically for Kubernetes applications. You can package your applications as a Helm Chart, and then install, update, and roll back your Kubernetes applications using Helm.
- a vanilla k8s app deployment consists of several yaml files to describe the k8s artifacts in a declarative manner.

> Helm is a tool that allows you to create deployment templates. This template is called a helm chart, which consists of the yaml files that look more or less like a regular k8s yaml file but have some variables in them. Those variables can be defined through an additional values.yaml file.

## helm chart dir structure

- `Chart.yaml` - top-level chart metadata. e.g. name, version, etc.
- `values.yaml` - declare variables here that are used in the `templates/*.yaml` files

```sh
$ helm create demo
Creating demo
$ tree demo
demo
├── Chart.yaml
├── charts
├── templates
│   ├── NOTES.txt
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── service.yaml
│   ├── serviceaccount.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml
```

## resources

- [Helm: Quickstart Guide](https://helm.sh/docs/intro/quickstart/)
- [Kubernetes and Helm in a Nutshell](https://motius.de/insights/kubernetes-and-helm-in-a-nutshell/)
- [Helm Charts: Kubernetes Tutorial and Examples](https://www.containiq.com/post/helm-charts)
- [ArtifactHUB](https://artifacthub.io/) - Find, install and publish Kubernetes packages
