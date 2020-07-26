+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2019-05-18
description = ""
summary = "learning Azure Kubernetes Service Aks"
draft = false
slug = "azure-kubernetes-service-aks"
tags = ["azure","kubernetes","github",]
title = "Azure Kubernetes Service Aks"
repoFullName = "pfeilbr/azure-kubernetes-service-aks-playground"
repoHTMLURL = "https://github.com/pfeilbr/azure-kubernetes-service-aks-playground"
truncated = true

+++


learn azure kubernetes service

## Running

```sh
# create resource group
az group create --name "pfeilbr-aks-01" --location eastus

# create cluster
az aks create \
    --resource-group "pfeilbr-aks-01" \
    --name "pfeilbr-aks-01" \
    --node-count 1 \
    --location eastus \
    --enable-addons monitoring \
    --generate-ssh-keys

# set connectivity to cluster for kubectl
az aks get-credentials --resource-group "pfeilbr-aks-01" --name "pfeilbr-aks-01"

# list cluster nodes
kubectl get nodes

# deploy
kubectl apply -f azure-vote.yaml

# monitor deployment progress
kubectl get service azure-vote-front --watch

# open "EXTERNAL-IP" in browser to view webapp

# delete cluster
az group delete --name "pfeilbr-aks-01" --yes --no-wait
```

![](https://www.evernote.com/l/AAHFfcVhlCJNT5rYgPkVTwZ4NL5x57QaNd0B/image.png)
