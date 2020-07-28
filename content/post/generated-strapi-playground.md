+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2020-07-10
description = ""
summary = " "
draft = false
slug = "strapi"
tags = []
title = "Strapi"
repoFullName = "pfeilbr/strapi-playground"
repoHTMLURL = "https://github.com/pfeilbr/strapi-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/strapi-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/strapi-playground</a>
</div>


learn [strapi](https://strapi.io/), the open-source headless CMS

## Prerequisites

* [docker desktop](https://www.docker.com/products/docker-desktop)

## Session

```sh
# create app
npx create-strapi-app my-project --quickstart

# local docker install / run via https://strapi.io/documentation/v3.x/installation/docker.html

# pull
docker-compose pull

# run
docker-compose up -d

# open web ui
open http://localhost:1337/admin
```

## Screenshots

![](https://www.evernote.com/l/AAH957Jw0WVBx5AIat1ulOIsv87pCNGk2DUB/image.png)

## Resources

* [Strapi Documentation](https://strapi.io/documentation/)


