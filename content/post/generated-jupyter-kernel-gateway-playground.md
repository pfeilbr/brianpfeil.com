+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-01-19
description = ""
summary = "learning Jupyter Kernel Gateway"
draft = false
slug = "jupyter-kernel-gateway"
tags = ["jupyter","github",]
title = "Jupyter Kernel Gateway"
repoFullName = "pfeilbr/jupyter-kernel-gateway-playground"
repoHTMLURL = "https://github.com/pfeilbr/jupyter-kernel-gateway-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/jupyter-kernel-gateway-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/jupyter-kernel-gateway-playground</a>


learn [Jupyter Kernel Gateway](https://jupyter-kernel-gateway.readthedocs.io/en/latest/index.html)

### Development

```sh
# build image
docker build -t pfeilbr/jupyter-kernel-gateway .

# run
docker run -it --rm -p 8888:8888 pfeilbr/jupyter-kernel-gateway

# view swagger json
open http://0.0.0.0:8888/api/swagger.json

# expose to public internet
ngrok http 8888

# view in swagger ui
open https://petstore.swagger.io

# enter https://NGROK_HOST/api/swagger.json in explore
# e.g.
#   https://0278ef82.ngrok.io/api/swagger.json

# needed to add CORS params in `docker-stacks-image/Dockerfile` `CMD` statement

# running `browser-client-example.js` in chrome DevTools
open http://0.0.0.0:8888/api/swagger.json
# open DevTools and run code in Sources | Snippets

# push docker image
docker push pfeilbr/jupyter-kernel-gateway
```

### Screenshots

![](https://www.evernote.com/l/AAHBAoPzt9NOyLDDhg90a4FkOcrCBAs7vz4B/image.png)


