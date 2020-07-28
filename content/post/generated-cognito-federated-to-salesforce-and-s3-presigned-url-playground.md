+++
author = "Brian Pfeil"
categories = ["HTML", "playground"]
date = 2019-06-13
description = ""
summary = " "
draft = false
slug = "cognito-federated-to-salesforce-and-s3-presigned-url"
tags = ["cognito","salesforce",]
title = "Cognito Federated To Salesforce and S3 Presigned URL"
repoFullName = "pfeilbr/cognito-federated-to-salesforce-and-s3-presigned-url-playground"
repoHTMLURL = "https://github.com/pfeilbr/cognito-federated-to-salesforce-and-s3-presigned-url-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/cognito-federated-to-salesforce-and-s3-presigned-url-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/cognito-federated-to-salesforce-and-s3-presigned-url-playground</a>
</div>


## Login with Cognito Federated to Salesforce Example

* see [`index.html`](index.html)
* see `~/Dropbox/notes/static-s3-cognito-authentication.md` on local machine also for greater detail on setup

```sh
# local dev
# start server.  serves static files from current directory '.'.  listens on ssl 443
sudo node server.js
open https://localhost

# on s3
open https://pfeil-static-site-01.s3.amazonaws.com/index.html

# on cloudfront
open https://d3tz189emgpc7c.cloudfront.net/index.html

# copy updated file to s3
aws s3 cp index.html s3://pfeil-static-site-01/index.html
# invalidate cloudfront dist after copy

# if any login issues
# clear site data for https://pfeil-dev-ed.my.salesforce.com in chrome dev tools
```

## Pre-signed URL Example

* see [`index.js`](index.js)
* `node index.js` outputs pre-signed url. (uses ~/.aws/credentials and pre-signed URL generated under that users context/permission)
* PUT / upload file to S3 via `curl -X PUT -T hello.txt -L '<pre-signed url>'`




