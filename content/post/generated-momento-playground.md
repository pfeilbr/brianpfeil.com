+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2023-08-24
description = ""
summary = " "
draft = false
slug = "momento"
tags = ["cache","db"]
title = "Momento"
repoFullName = "pfeilbr/momento-playground"
repoHTMLURL = "https://github.com/pfeilbr/momento-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/momento-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/momento-playground</a>
</div>


learn and experiment with [Momento](https://www.gomomento.com/)

## general

- currently support cache and topic resource types
- simple pay-as-you-go pricing model by data trasfered
- gRPC for efficient communication with server

## demo

see [`index.js`](https://github.com/pfeilbr/momento-playground/blob/master/index.js)


```sh
cp .env.sample .env
# edit .env to include youe `MOMENTO_AUTH_TOKEN`

npm install
npm start
```

## resources

- [Momento](https://www.gomomento.com/)
- <https://docs.momentohq.com/>
- [Service Limits](https://docs.momentohq.com/manage/limits)
