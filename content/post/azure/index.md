+++
title = "Azure"
slug = "azure"
author = "Brian Pfeil"
date = "2021-06-15"
lastmod = "2021-06-15"
draft = true
categories = []
tags = ["azure"]
summary = "short descriptions for key Azure services"

+++

# azure
* [Management](#management)
* [IAM](#iam)
    * [Service Principals](#service-principals)
    * [Roles](#roles)
    * [Role Assignments](#role-assignments)
    * [Resources](#resources)
* [Azure Policy](#azure-policy)
* [Azure Resource Manager (ARM)](#azure-resource-manager-arm)
    * [Resources](#resources-1)
* [Azure Blueprints](#azure-blueprints)
* [Blob Storage](#blob-storage)
    * [Resources](#resources-2)
* [Storage Queues](#storage-queues)
* [Service Bus Queues](#service-bus-queues)
* [Service Bus Topics](#service-bus-topics)
    * [Resources](#resources-3)
* [Event Grid](#event-grid)
    * [Resources](#resources-4)
* [Event Hub](#event-hub)
* [Cosmos DB](#cosmos-db)
* [SQL Database](#sql-database)
* [SQL Managed Instance](#sql-managed-instance)
* [Static Web Apps](#static-web-apps)
* [Functions](#functions)
    * [Resources](#resources-5)
* [Function Proxies](#function-proxies)
    * [Resources](#resources-6)
* [API Management (APIM)](#api-management-apim)
    * [Resources](#resources-7)
* [SignalR](#signalr)
    * [Resources](#resources-8)
* [Key Vault](#key-vault)
* [CDN](#cdn)
* [App Configuration](#app-configuration)
* [Data Factory](#data-factory)
* [Synapse Analytics](#synapse-analytics)
* [HDInsight](#hdinsight)
* [Databricks](#databricks)
* [Data Lake Analytics](#data-lake-analytics)
* [Logic Apps](#logic-apps)
    * [Resources](#resources-9)
* [Application Insights](#application-insights)
* [Cognitive Search](#cognitive-search)
* [Introducing Authentication](#introducing-authentication)
* [Azure AD Authentication Options for Users](#azure-ad-authentication-options-for-users)
* [Azure Cost Management + Billing documentation](#azure-cost-management--billing-documentation)

## Management

* Account -> [Management Groups] -> Subscriptions -> Resources Groups -> Resources
	* e.g. hierarchy in URI for Key Vault Resource `/subscriptions/8a1f586d-1032-4471-803a-25126ef17c42/resourceGroups/resource-group-01/providers/Microsoft.KeyVault/vaults/pfeilkeyvault01`
* Management Groups (enable enterprise governance) are optional but allow you to group subscriptions and apply policies at management group level that are inherited by all contained subscriptions. (e.g. only create storage accounts in a given geography)
* Billing done at Subscription level
* Resource groups - scope for applying role-based access control (RBAC) permissions

![](https://www.evernote.com/l/AAGdmzF3n3pDX7VmRSXndC7A8LQfnIKUgrYB/image.png)

* Regions
* Availability Zones
* Each Azure region is always paired with another region within the same geography.  provide reliable services and data redundancy

## IAM

* Azure AD - stories identities in directory and governs access to azure resources.
* Identity - the fact of being something or someone. e.g. Users, Applications, Servers.
* Authentication - process of verification of identity
* Authorization - process of ensuring that only authenticated identities get access to the resources for which they have been granted access.
* Access Management - process of controlling, verifying, tracking and managing access to authorized users and applications.

![](https://www.evernote.com/l/AAHeMR81MMZKRapGvhkxOYN71U8J8vRyXGIB/image.png)

* RBAC - role based access control
* Azure AD Roles - roles that allow admin access to global (tenant-level) settings and services. e.g. user and group admin, domain names, adding/removing user licenses, etc.
* Azure Roles - roles that define permissions to azure resources.
* Privileged Identity Management (PIM) - just in time access to elevated roles.  Eligible roles are assigned to a user.  That user can go into PIM to request access.  Duration and reason can be set when requesting and assuming the elevated role.


### Service Principals

> An Azure service principal is a security identity used by user-created apps, services, and automation tools to access specific Azure resources. Think of it as a 'user identity' (login and password or certificate) with a specific role, and tightly controlled permissions to access your resources. It only needs to be able to do specific things, unlike a general user identity. It improves security if you only grant it the minimum permissions level needed to perform its management tasks.

Similar to AWS IAM User

* create service principal in portal via **Azure AD | App registrations**

```sh
# create service principal
az ad sp create-for-rbac --name "http://service-principal-01"

# assign role
az role assignment create --assignee "00133c8e-a08e-490e-ae7c-872ea2debf1e" --role Contributor

# login
az login --service-principal -u <appid> --password {password-or-path-to-cert} --tenant {tenant}
```

### Roles

* permissions - read blob (`Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read`).  read storage queue (`Microsoft.Storage/storageAccounts/queueServices/queues/messages/read`)
* scopes - subscriptions or resource groups) where this role will be available for assignment.
* Azure RBAC scope covers management groups, subscriptions, resource groups, and resources
* Portal | Subscription | Access control (IAM) - assign / create / delete roles.

### Role Assignments

* process of attaching a role definition to a user, group, service principal, or managed identity at a particular scope for the purpose of granting access
* Role Definition (permissions) + Resource + Scope
* Can view / managed in portal via "Access control (IAM)" blade

### Resources

* [Role-Based Access Control | AZ-900 Episode 28 - Cheat Sheet](https://marczak.io/az-900/episode-28/cheat-sheet/)
* [Use Azure service principals with Azure CLI](https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli)
* [Create an Azure AD app & service principal in the portal - Microsoft identity platform](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal)
* [Securing Azure Services with Managed Identities](https://marczak.io/posts/2019/07/securing-websites-with-msi/)
* [Azure AD consent framework](https://docs.microsoft.com/en-us/azure/active-directory/develop/consent-framework) - describes process of grant permissions to an application and the user consent flow

## Azure Policy

* policies focus on resource properties
* e.g. only create resources where location is US.
* Policy Definitions - include ALLOW and DENY for singular check and singular effect
* Initiative - grouping of multiple policies
* can assign policy at the following scope levels:  management group, subscription, resource group
	* can add an exclusion scope that specifies where not to apply the policy
* show which resources are compliant and non-compliant with policies
* there are built-in policies and you can create you own custom policies

summary

![](https://www.evernote.com/l/AAETzFRSpUxFjJZ8bKruWXdUgPiHngXfQHEB/image.png)

azure portal view

![](https://www.evernote.com/l/AAGQ8QTauf1HzJkwmbdu1Iriu4wc1Y2KOQUB/image.png)

policy blocking resource creation

![](https://www.evernote.com/l/AAFcBSccmh9C8I1COF9IGonCSzPzH_yp3ssB/image.png)

## Azure Resource Manager (ARM)

* infrastructure-as-code with json
* parameters, variables, resources, outputs
* nested templates
* external templates.  reference via URL

### Resources

* [Azure/azure-quickstart-templates](https://github.com/Azure/azure-quickstart-templates)

## Azure Blueprints

similar to AWS Service Catalog

* helps with ensuring security and compliance
* Package of various Azure components (artifacts).  Resource Groups, ARM Templates, Policy Assignments, Role Assignments
* central repository for pre-approved patterns and solutions
* Blueprint Definitions - container for artifacts
* Blueprint Assignments - assign to resource group and it deploys artifacts to it
* supports versioning.

## Blob Storage

### Resources

* [Static website hosting in Azure Storage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-static-website)

## Storage Queues

* good for async worker processes
* 64 kb size limit on messages
* messages stored up to 7 days

## Service Bus Queues

* FIFO
* 256 KB - 1 MB message size
* duplicate detection (idempotent)
* supports in order and at-most-once delivery
* dead-letter queues
* message expiration

## Service Bus Topics

* topic and subscriptions support
* duplicate detection (idempotent)
* message TTL
* dead-letter queues

### Resources

* [Service Bus Explorer on the Azure portal is now available in preview](https://azure.microsoft.com/en-us/updates/sesrvice-bus-explorer/)

## Event Grid

* AWS EventBridge
* Publishers - built-in events from azure services.  custom events from own applications
* Event Sources - where the event happens. e.g. Azure Storage
* Topics - endpoint where the source sends events
	* System topics - built-in topics provided by Azure services such as Azure Storage, Azure Event Hubs, and Azure Service Bus
	* Custom topics - application and third-party topics
* Subscriptions - which events on a topic you're interested in receiving.  When creating the subscription, you provide an endpoint for handling the event

### Resources

* [Azure Resource Manager template samples - Event Grid - Azure Event Grid](https://docs.microsoft.com/en-us/azure/event-grid/template-samples)
* [Receive events from Azure Event Grid to an HTTP endpoint - Azure Event Grid](https://docs.microsoft.com/en-us/azure/event-grid/receive-events)

## Event Hub

* AWS Kinesis
* streaming
* partitions
* consumer groups, consumers
* listening streaming applications
* stream to blob storage (similar to aws firehose -> S3) as .avro files

* namespace -> hub

## Cosmos DB

* NoSQL
* multi-model / multiple interfaces - SQL, MongoDB, Cassandra, Tables, and Gremlin
* similar to AWS DynamoDB

## SQL Database

* PaaS Database Engine (not fully managed)
* handles upgrading, patching, backups, and monitoring, without user involvement
* similar to AWS RDS

## SQL Managed Instance

* ...

## Static Web Apps

* allows you to build modern web applications that automatically publish from changes made in GitHub.

## Functions

* triggers and bindings
* [Azure Durable Functions](https://docs.microsoft.com/en-us/azure/azure-functions/durable/) - lets you write stateful functions in a serverless compute environment.  Similar to AWS Step Functions, but implemented as language level library
* [custom handlers](https://docs.microsoft.com/en-us/azure/azure-functions/functions-custom-handlers) via binary that runs local http server

deploy function via zip file.  ensure correct [nodejs folder structure](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-node?tabs=v2#folder-structure)

```sh
az functionapp deployment source config-zip -g <resource_group> -n \
<app_name> --src <zip_file_path>
```

When http triggered function is [configured with Azure AD authentication](https://docs.microsoft.com/en-us/azure/app-service/configure-authentication-provider-aad?toc=/azure/azure-functions/toc.json), the identity information is in the
`req.headers`

Example

```json
"x-ms-client-principal-name": "brian.pfeil@gmail.com",
"x-ms-client-principal-id": "38d35c72-5a26-464c-bbb3-c4487a1d4779",
"x-ms-client-principal-idp": "aad",
```

### Resources

* [mspnp/serverless-reference-implementation](https://github.com/mspnp/serverless-reference-implementation) - great full-stack serverless reference
* [Zip push deployment for Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/deployment-zip-push)
* [JavaScript developer reference for Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-node)


## Function Proxies

* Proxies are defined inside a proxies.json configuration file at the root of the project. see following for details https://docs.microsoft.com/en-us/azure/azure-functions/functions-proxies#advanced-configuration
* allow us to define a single API surface for multiple function apps
* map a path (/something) to backend URL.  e.g. /hello -> https://durablefnsplayground01.azurewebsites.net/api/orchestrators/{functionName}?code=UD0/aY27zc3FPpjNjaAqMU73yVJuLB1tva3U9TaaWDAMzwEzg3qeVA==
* this way you don't need to expose code query string parameter
* you can map a path and hard code a response for mocking

### Resources

* [Work with proxies in Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-proxies)
* [Microsoft Azure Function Proxies in 5 Minutes](https://www.youtube.com/watch?v=NyysLRSJUmk)


## API Management (APIM)

* AWS API Gateway
* import OpenAPI /Swagger spec
* can import a function app as an API in API Management
* APIM product - contains one or more APIs as well as a usage quota and the terms of use. Once a product is published, developers can subscribe to the product and begin to use the product's APIs
* Subscriptions - developers who need to consume the published APIs must include a valid subscription key in HTTP requests when they make calls to those APIs
	* can be scoped to product, all APIs, or an individual API
	* need to provide `ocp-apim-subscription-key` header when calling
* [Policies]((https://docs.microsoft.com/en-us/azure/api-management/api-management-howto-policies)) - allow the publisher to change the behavior of the API through configuration.
	* specified in XML
	* Allow for request and response transformations.  Rate limiting.  Similar to AWS APIG request/response mapping templates.
* as of 2021-02-12 takes about 30 min to create API Management instance

### Resources

* [Import an Azure Function App as an API in API Management - Azure API Management](https://docs.microsoft.com/en-us/azure/api-management/import-function-app-as-api)
* [Policies in Azure API Management](https://docs.microsoft.com/en-us/azure/api-management/api-management-howto-policies)

## SignalR

* real-time application
* websocket, SSE (EventSource), HTTP long polling

### Resources

* [Enable automatic updates in a web application using Azure Functions and SignalR Service - Learn](https://docs.microsoft.com/en-us/learn/modules/automatic-update-of-a-webapp-using-azure-functions-and-signalr/)
* [MicrosoftDocs/mslearn-advocates.azure-functions-and-signalr](https://github.com/MicrosoftDocs/mslearn-advocates.azure-functions-and-signalr)

## Key Vault

* AWS Secrets Manager
* functions can have Key Vault references which make the secrets available in environment variables.  The secrets are also caches per function instance on startup

Example Secret

![](https://www.evernote.com/l/AAEIj8NWGyVPGZAIVI8hDdhhiJZYIgtZ3rAB/image.png)

## CDN

* CDN profile - collection of CDN endpoints

## App Configuration

* centralized service for management of application settings and feature flags
* supports key vault integration via references to the secrets stored in key vault
* integrates with event grid. emits events when App Configuration changes that you can subscribe and respond to
* e.g. A/B testing with percentages
* e.g. multiple apps use same settings like storage key

## Data Factory

* managed ETL
* concepts
	* Pipelines - outer container
	* Connections (Linked Services) - connection information for source(s) and sink(s) with credentials / keys
	* Dataset - file formats and schema
	* Activities - copy data, transform, etc.
	* Triggers - on-demand/manual (REST API), scheduled, tumbling windows, event based via event grid for blob storage for a pipeline run
	* Parameters - can be passed into pipeline and used with the various types.

## Synapse Analytics

* ...

## HDInsight

* Apache Spark , Apache Hadoop , Apache Kafka , Apache HBase , Apache Storm , and Machine Learning Services
* like AWS EMR

## Databricks

* spark, hadoop, and friends ...

## Data Lake Analytics

* ...

## Logic Apps

*  schedule, automate, and orchestrate tasks, business processes, and workflows when you need to integrate apps, data, systems, and services across enterprises or organizations

**Guidance**

The following flowchart summarizes the key questions to ask when you're considering using Logic Apps.

![](https://www.evernote.com/l/AAEbJ6SJWaBCLq0wvDqR_wsghtF9ClpKyJwB/image.png)

### Resources

* [Securing Logic App with Azure AD authentication using API Management](https://marczak.io/posts/2019/08/secure-logic-app-with-api-management/)
* [Workflow Definition Language schema reference - Azure Logic Apps](https://docs.microsoft.com/en-us/azure/logic-apps/logic-apps-workflow-definition-language)

## Application Insights

* author queries using [Kusto Query Language](https://docs.microsoft.com/en-us/azure/data-explorer/kql-quick-reference)

## Cognitive Search

* indexing
	* push model - upload json docs for indexing
	* pull model - point indexers where the content lives. e.g. azure blob storage
* querying - can include relevance tuning, autocomplete, synonym matching, fuzzy matching, pattern matching, filter, and sort.  spelling mistakes, geospatial queries, paging, highlighting.
* Skillset -  content type indexer for unstructured and structured content (docx, pdf, ).  predefined ones from Microsoft, or custom skills that you create.  e.g. text split skill, sentiment detection skill
	* document cracking - understand the contents of the document.  text, images, metadata, etc.
* portions of underlying tech is based on apache lucene

---

## Introducing Authentication

* OAuth 2.0 is specifically about authorization and permissions
* Open ID Connect (OIDC) is focused on authentication and built on OAuth 2.0.  Has strict JWT format that part of the spec.

* identity token
  * typically JWT
  * user claims - e.g. username, email
* access token
  * short lived (e.g. 1 hr)
  * typically JWT
  * scope
* refresh token
  * long life (e.g. 14 days)
  * can be used to request an access token without the user needing to login again

## Azure AD Authentication Options for Users

* Azure AD Connect - replicate objects in AD to Azure AD.  AD is the source of truth.

## Azure Cost Management + Billing documentation

* <https://docs.microsoft.com/en-us/azure/cost-management-billing/>
