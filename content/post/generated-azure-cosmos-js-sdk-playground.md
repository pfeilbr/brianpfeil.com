+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-05-08
description = ""
summary = " "
draft = false
slug = "azure-cosmos-js-sdk"
tags = ["azure","javascript","sdk",]
title = "Azure Cosmos JS SDK"
repoFullName = "pfeilbr/azure-cosmos-js-sdk-playground"
repoHTMLURL = "https://github.com/pfeilbr/azure-cosmos-js-sdk-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/azure-cosmos-js-sdk-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/azure-cosmos-js-sdk-playground</a>
</div>


learn [azure cosmos db javascript sdk](https://github.com/azure/azure-cosmos-js).

## Running

1. provision resources
    ```sh
    # create group
    az group create --name group01 --location "East US"

    # create cosmos db account
    az group deployment create \
    --name cosmosdbaccountdeployment01 \
    --resource-group group01 \
    --template-file arm-templates/azure-cosmos-db-account.json \
    --parameters name="account01" location="eastus" locationName="East US" defaultExperience="DocumentDB"
    ```
1. copy `.env.sample` to `.env` and populate with your information from **Keys**
![](https://www.evernote.com/l/AAG3s-Zs6VRIPa7fvjL6KuMP03bCj8nDKhYB/image.png)
1. run `npm start`


