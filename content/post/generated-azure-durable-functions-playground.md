+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2021-02-05
description = ""
summary = " "
draft = false
slug = "azure-durable-functions"
tags = ["azure",]
title = "Azure Durable Functions"
repoFullName = "pfeilbr/azure-durable-functions-playground"
repoHTMLURL = "https://github.com/pfeilbr/azure-durable-functions-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/azure-durable-functions-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/azure-durable-functions-playground</a>
</div>


learn Azure [Durable Functions](https://docs.microsoft.com/en-us/azure/azure-functions/durable/)

## Running

```sh
LOCATION=eastus
BASE_NAME=durable-fns-playground-01
RESOURCE_GROUP="${BASE_NAME}"
STORAGE_ACCOUNT=$(echo $BASE_NAME | sed -e 's/-//g')
FUNCTION_APP=$(echo $BASE_NAME | sed -e 's/-//g')

# create resource group
az group create \
    --name "${RESOURCE_GROUP}" \
    --location "${LOCATION}"

# create storage account
az storage account create \
    --name "${STORAGE_ACCOUNT}" \
    --location "${LOCATION}" \
    --resource-group "${RESOURCE_GROUP}" \
    --sku "Standard_LRS"

# create function app in azure
az functionapp create \
    --resource-group "${RESOURCE_GROUP}" \
    --consumption-plan-location "${LOCATION}" \
    --runtime "node" \
    --runtime-version 12 \
    --functions-version 3 \
    --name "${FUNCTION_APP}" \
    --storage-account "${STORAGE_ACCOUNT}"

# create functions
# DurableFunctionsHTTPstarter is HTTP endpoint that invokes DurableFunctionsOrchestrator
# which then calls DurableFunctionsActivity multiple time with different parameters

func new -t "Durable Functions HTTP starter" -l javascript -n DurableFunctionsHTTPstarter
func new -t "Durable Functions orchestrator" -l javascript -n DurableFunctionsOrchestrator
func new -t "Durable Functions activity" -l javascript -n DurableFunctionsActivity

# deploy
func azure functionapp publish "${FUNCTION_APP}"

# get function all base URL
FUNCTION_APP_URL="https://$(az functionapp show -g ${RESOURCE_GROUP} -n ${FUNCTION_APP} --query defaultHostName -o tsv)/api"

# pull down app settings for running locally
func azure functionapp fetch-app-settings "${FUNCTION_APP}"

# run locally
func start

# trigger durable function
curl 'http://localhost:7071/api/orchestrators/DurableFunctionsOrchestrator'

# async execution - output
#
# {
#   "id": "20f2ddc1e34543379efc49a09962dfc5",
#   "statusQueryGetUri": "http://localhost:7071/runtime/webhooks/durabletask/instances/20f2ddc1e34543379efc49a09962dfc5?taskHub=DurableFunctionsHub&connection=Storage&code=CODE",
#   "sendEventPostUri": "http://localhost:7071/runtime/webhooks/durabletask/instances/20f2ddc1e34543379efc49a09962dfc5/raiseEvent/{eventName}?taskHub=DurableFunctionsHub&connection=Storage&code=CODE",
#   "terminatePostUri": "http://localhost:7071/runtime/webhooks/durabletask/instances/20f2ddc1e34543379efc49a09962dfc5/terminate?reason={text}&taskHub=DurableFunctionsHub&connection=Storage&code=CODE",
#   "rewindPostUri": "http://localhost:7071/runtime/webhooks/durabletask/instances/20f2ddc1e34543379efc49a09962dfc5/rewind?reason={text}&taskHub=DurableFunctionsHub&connection=Storage&code=CODE",
#   "purgeHistoryDeleteUri": "http://localhost:7071/runtime/webhooks/durabletask/instances/20f2ddc1e34543379efc49a09962dfc5?taskHub=DurableFunctionsHub&connection=Storage&code=CODE"
# }

# fetch `statusQueryGetUri`
curl 'http://localhost:7071/runtime/webhooks/durabletask/instances/20f2ddc1e34543379efc49a09962dfc5?taskHub=DurableFunctionsHub&connection=Storage&code=CODE'

# {
#     "name": "DurableFunctionsOrchestrator",
#     "instanceId": "20f2ddc1e34543379efc49a09962dfc5",
#     "runtimeStatus": "Completed",
#     "input": null,
#     "customStatus": null,
#     "output": [
#         "Hello Tokyo!",
#         "Hello Seattle!",
#         "Hello London!"
#     ],
#     "createdTime": "2021-02-04T21:33:29Z",
#     "lastUpdatedTime": "2021-02-04T21:33:30Z"
# }

# ---

# start in own terminal
# Show interactive streaming logs for an Azure-hosted Function App
func azure functionapp logstream "${FUNCTION_APP}"

# trigger durable function
curl "${FUNCTION_APP_URL}/orchestrators/DurableFunctionsOrchestrator?code=CODE"

# async execution - output
#
# {
#   "id": "7501819801f942ebaed9289e87420cbd",
#   "statusQueryGetUri": "https://durablefnsplayground01.azurewebsites.net/runtime/webhooks/durabletask/instances/7501819801f942ebaed9289e87420cbd?taskHub=DurableFunctionsHub&connection=Storage&code=CODE",
#   "sendEventPostUri": "https://durablefnsplayground01.azurewebsites.net/runtime/webhooks/durabletask/instances/7501819801f942ebaed9289e87420cbd/raiseEvent/{eventName}?taskHub=DurableFunctionsHub&connection=Storage&code=CODE",
#   "terminatePostUri": "https://durablefnsplayground01.azurewebsites.net/runtime/webhooks/durabletask/instances/7501819801f942ebaed9289e87420cbd/terminate?reason={text}&taskHub=DurableFunctionsHub&connection=Storage&code=CODE",
#   "rewindPostUri": "https://durablefnsplayground01.azurewebsites.net/runtime/webhooks/durabletask/instances/7501819801f942ebaed9289e87420cbd/rewind?reason={text}&taskHub=DurableFunctionsHub&connection=Storage&code=CODE",
#   "purgeHistoryDeleteUri": "https://durablefnsplayground01.azurewebsites.net/runtime/webhooks/durabletask/instances/7501819801f942ebaed9289e87420cbd?taskHub=DurableFunctionsHub&connection=Storage&code=CODE"
# }

# fetch `statusQueryGetUri`
curl "https://durablefnsplayground01.azurewebsites.net/runtime/webhooks/durabletask/instances/7501819801f942ebaed9289e87420cbd?taskHub=DurableFunctionsHub&connection=Storage&code=CODE"
# {
#     "name": "DurableFunctionsOrchestrator",
#     "instanceId": "7501819801f942ebaed9289e87420cbd",
#     "runtimeStatus": "Completed",
#     "input": null,
#     "customStatus": null,
#     "output": [
#         "Hello Tokyo!",
#         "Hello Seattle!",
#         "Hello London!"
#     ],
#     "createdTime": "2021-02-04T20:55:25Z",
#     "lastUpdatedTime": "2021-02-04T20:55:26Z"
# }

# query function logs
read -r -d '' QUERY << EOM
traces
| project timestamp, message
| where timestamp > ago(24h)
| limit 10
EOM

az monitor app-insights query \
    --app 'cd03d419-0bba-410e-ac3f-d7e934c027f1' \
    --analytics-query "${QUERY}"


# output
#
# {
#   "tables": [
#     {
#       "columns": [
#         {
#           "name": "timestamp",
#           "type": "datetime"
#         },
#         {
#           "name": "message",
#           "type": "string"
#         }
#       ],
#       "name": "PrimaryResult",
#       "rows": [
#         [
#           "2021-02-04T20:56:04.3256227Z",
#           "Host Status: {\r\n  \"id\": \"durablefnsplayground01\",\r\n  \"state\": \"Running\",\r\n  \"version\": \"3.0.15193.0\",\r\n  \"versionDetails\": \"3.0.15193 Commit hash: 75da1ebed23b08b39c8c3c20b3ea687813c0acdf\",\r\n  \"platformVersion\": \"91.0.7.116\",\r\n  \"instanceId\": \"00d386aeb51a3d5098651c58f61ffb53a9b1a656ea9e9b0dd570b9834cdc3d4f\",\r\n  \"computerName\": \"DW0-HR0-3-17\",\r\n  \"processUptime\": 145740,\r\n  \"extensionBundle\": {\r\n    \"id\": \"Microsoft.Azure.Functions.ExtensionBundle\",\r\n    \"version\": \"1.5.0\"\r\n  }\r\n}"
#         ],
#         [
#           "2021-02-04T20:56:05.4099623Z",
#           "Host Status: {\r\n  \"id\": \"durablefnsplayground01\",\r\n  \"state\": \"Running\",\r\n  \"version\": \"3.0.15193.0\",\r\n  \"versionDetails\": \"3.0.15193 Commit hash: 75da1ebed23b08b39c8c3c20b3ea687813c0acdf\",\r\n  \"platformVersion\": \"91.0.7.116\",\r\n  \"instanceId\": \"00d386aeb51a3d5098651c58f61ffb53a9b1a656ea9e9b0dd570b9834cdc3d4f\",\r\n  \"computerName\": \"DW0-HR0-3-17\",\r\n  \"processUptime\": 146826,\r\n  \"extensionBundle\": {\r\n    \"id\": \"Microsoft.Azure.Functions.ExtensionBundle\",\r\n    \"version\": \"1.5.0\"\r\n  }\r\n}"
#         ],
#         ...

```

## Resources

* [Azure Durable Functions documentation](https://docs.microsoft.com/en-us/azure/azure-functions/durable/)


