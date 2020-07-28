+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-05-13
description = ""
summary = " "
draft = false
slug = "azure-js-cognitive-services"
tags = ["azure","javascript",]
title = "Azure JS Cognitive Services"
repoFullName = "pfeilbr/azure-js-cognitive-services-playground"
repoHTMLURL = "https://github.com/pfeilbr/azure-js-cognitive-services-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/azure-js-cognitive-services-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/azure-js-cognitive-services-playground</a>
</div>


learn [azure cognitive services](https://docs.microsoft.com/en-us/azure/cognitive-services/)

**Examples**

`runHandwrittenOCRForURL()` - uses computer vision `batchReadFile` API to perform handwritten OCR on a image of a form (image sourced from public URL).

## Resources

- [cognitive-services/computer-vision docs](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/)

## Running
 
1. Create new cognitive services computer vision resource  
    run `az login`, then `npm run provision`  
    OR via portal
    ![](https://www.evernote.com/l/AAHErRlR-tFBJbb6x-JKpZTcsQpxXyx4KAAB/image.png)
1. Copy [`.env.sample`](.env.sample) to `.env` and populate with values via the following steps.
1. `CLIENT_ID`, `DOMAIN`
    ![](https://www.evernote.com/l/AAExoADr6tVHoLj4lOD_58FCSWmWAelxCrMB/image.png)
1. SUBSCRIPTION_ID
    ![](https://www.evernote.com/l/AAGdlioOXwpHEoGofH2nL-PJAIIOWlkvoiQB/image.png)
1. `COGNITIVE_SERVICES_ENDPOINT`
    ![](https://www.evernote.com/l/AAETKioZuRpHD48_sa7nDTP5A-5zla0Oew0B/image.png)
1. `COGNITIVE_SERVICES_KEY`
    ![](https://www.evernote.com/l/AAHdTNN4abtGmq5ZKgwh2vD6uOURbM6mhHwB/image.png)
1. run `npm start`



