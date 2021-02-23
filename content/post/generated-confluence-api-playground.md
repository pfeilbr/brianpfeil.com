+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2017-04-04
description = ""
summary = " "
draft = true
slug = "confluence-api"
tags = ["cms","javascript","api",]
title = "Confluence API"
repoFullName = "pfeilbr/confluence-api-playground"
repoHTMLURL = "https://github.com/pfeilbr/confluence-api-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/confluence-api-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/confluence-api-playground</a>
</div>


* [Confluence Cloud REST API Reference](https://docs.atlassian.com/confluence/REST/latest/)

**Examples**

```sh

# get space info
GET https://share.merck.com/rest/api/space/SHAR

# get page content
GET https://share.merck.com/rest/api/content?spaceKey=SHAR&title=Account+360&expand=space,body.view,version,container

# get user
GET https://share.merck.com/rest/api/user?username=pfeilbr

```



