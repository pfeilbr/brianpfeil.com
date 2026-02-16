+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2021-01-29
description = ""
summary = " "
draft = false
slug = "azure-arm"
tags = ["azure"]
title = "Azure ARM"
repoFullName = "pfeilbr/azure-arm-playground"
repoHTMLURL = "https://github.com/pfeilbr/azure-arm-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/azure-arm-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/azure-arm-playground</a>
</div>


```sh
RESOURCE_GROUP_NAME="armplayground01"

# create resource group
az group create --name "${RESOURCE_GROUP_NAME}" --location eastus

# deploy arm outputs example
az deployment group create \
    --name "my-deployment-01" --resource-group "${RESOURCE_GROUP_NAME}" \
    --template-file "templates/outputs.azuredeploy.json" \
    --parameters @templates/outputs.parameters.json

```
