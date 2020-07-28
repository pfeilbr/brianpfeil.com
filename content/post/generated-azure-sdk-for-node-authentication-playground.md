+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-05-10
description = ""
summary = "learn Azure SDK For Node Authentication"
draft = false
slug = "azure-sdk-for-node-authentication"
tags = ["azure","sdk","playground",]
title = "Azure SDK For Node Authentication"
repoFullName = "pfeilbr/azure-sdk-for-node-authentication-playground"
repoHTMLURL = "https://github.com/pfeilbr/azure-sdk-for-node-authentication-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/azure-sdk-for-node-authentication-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/azure-sdk-for-node-authentication-playground</a>
</div>


learn authentication methods for azure sdk for nodejs

## Service Principal Authentication

 > Based on [azure-sdk-for-node/Documentation/Authentication.md](https://github.com/Azure/azure-sdk-for-node/blob/master/Documentation/Authentication.md#service-principal-authentication)


1. `clientId`, `secret`, and `domain` are defined in `.env`.  Copy [`.env.sample`](.env.sample) to `.env` and populate with values via the following steps.
1. getting `clientId` and `domain`
    
    run `az ad sp list`

    ![](https://www.evernote.com/l/AAHU6ONDbO1KYIVV93m8-xaJWKd4r3SolgoB/image.png)

1. getting / creating secret

    navigate to **Portal | Azure Active Directory | App registrations**
    create new client secret if needed OR use existing
    ![](https://www.evernote.com/l/AAHlB4MduMBFjadlw1JlXT6hfMVn5OBBSIwB/image.png)


