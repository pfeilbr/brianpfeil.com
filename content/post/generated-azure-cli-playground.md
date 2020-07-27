+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2019-05-14
description = ""
summary = "experimenting with Azure CLI"
draft = false
slug = "azure-cli"
tags = ["azure","cli","playground",]
title = "Azure CLI"
repoFullName = "pfeilbr/azure-cli-playground"
repoHTMLURL = "https://github.com/pfeilbr/azure-cli-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/azure-cli-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/azure-cli-playground</a>
-->


azure cli usage examples

```sh
# version info
az -v

# help
az -h

# interactive login
az login

# log in with a service principal using client secret.
az login --service-principal -u http://azure-cli-2019-05-09-16-09-40 -p '[CLIENT_SECRET_HERE]' --tenant brianpfeilgmail.onmicrosoft.com

az logout

az account show
az account show | jq '.tenantId'

az account list
az account get-access-token

az account list-locations

# list account fields in table format
az account list --output table --query '[].{Name:name, SubscriptionId:id, TenantId:tenantId}'


# details of signed in user
az ad signed-in-user show

# ad
az ad -h

# ad service principals
az ad sp -h

# create a service principal and configure its access to Azure
az ad sp create-for-rbac

# list service principals
az ad sp list

# list role assignments for service principal
az role assignment list --assignee 'http://azure-cli-2019-05-09-16-09-40'

# list role assignments for user (user sign-in name)
az role assignment list --assignee 'dev01@brianpfeilgmail.onmicrosoft.com'

# list role assignments for user (object id)
az role assignment list --assignee '38d35c72-5a26-464c-bbb3-c4487a1d4779'

# create resource group
az group create --name "group01" --location eastus

# list resource group names
az group list | jq '.[].name'

# delete resource group
az group delete --name "group01"

# deploy arm template examples
az group deployment create --name "my-deployment-01" --resource-group "my-resource-group-01"   --template-file template.json --parameters @parameters.json

az group deployment create   --name cosmosdbaccountdeployment01   --resource-group group01   --template-file azure-cosmos-db-account.json   --parameters name="account01" location="eastus" locationName="East US" defaultExperience="DocumentDB"

# interactive/repl mode.  immediately exits / doesn't work as of 2019-05-14
az interactive


# list all resources
az resource list

az role assignment list

az role definition list

az role definition list --custom-role-only true --output json | jq '.[] | {"roleName":.roleName, "roleType":.roleType}'
az role definition list | jq '.[].description'

# list storage account
az storage account list | jq '.[].name'
```


