+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-09-18
description = ""
summary = " "
draft = false
slug = "serverless-lambda-layers"
tags = ["serverless","lambda","playground",]
title = "Serverless Lambda Layers"
repoFullName = "pfeilbr/serverless-lambda-layers-playground"
repoHTMLURL = "https://github.com/pfeilbr/serverless-lambda-layers-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/serverless-lambda-layers-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/serverless-lambda-layers-playground</a>
</div>


learn lambda layers with serverless framework

## Running

see [`serverless.yml`](serverless.yml) and [`index.js`](index.js)

> layers are applied in order, meaning last layer in array is applied last and will overwrite any common files in other layers.

```sh

# install deps
npm i

# run via local packages sls
npm run sls -- deploy

# invoke and view logs
npm run sls -- invoke --function hello --log
```

![](https://www.evernote.com/l/AAFsMFGUI8dB5LcruXVZSdIMEVGMsxFDoE4B/image.png)

![](https://www.evernote.com/l/AAEMx_FKalVN8YYr1pF_9gpeC_vlpaAkNVAB/image.png)

## Resources

* [serverless docs | AWS - Layers](https://serverless.com/framework/docs/providers/aws/guide/layers/)
* [Part 2 — Create Lambda Layers with Serverless Framework and Offline support](https://medium.com/appgambit/part-2-create-lambda-layers-with-serverless-framework-and-offline-support-ad2a5a8dabfb)



