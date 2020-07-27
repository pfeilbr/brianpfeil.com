+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2016-11-04
description = ""
summary = "learning Heroku Container"
draft = false
slug = "heroku-container"
tags = ["heroku","github",]
title = "Heroku Container"
repoFullName = "pfeilbr/heroku-container-playground"
repoHTMLURL = "https://github.com/pfeilbr/heroku-container-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/heroku-container-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/heroku-container-playground</a>


Learn heroku container support.  Based on Heroku [Container Registry and Runtime](https://devcenter.heroku.com/articles/container-registry-and-runtime) article

```sh

# install container support
heroku plugins:install heroku-container-registry

# login to registry
heroku container:login

# build
docker build -t my-nodejs-app .

# run
docker run -it --rm -p 8000:8000 --name my-running-app my-nodejs-app
# visit http://localhost:8000

# create heroku app
heroku create

# push.  NOTE: app name of "stormy-badlands-73151" will be different
heroku container:push web --app stormy-badlands-73151

# check that it is up and running
heroku ps --app stormy-badlands-73151

# visit in browser
heroku open --app stormy-badlands-73151

# update flow

# make change to `server.js`
# build and push
heroku container:push web --app stormy-badlands-73151
```



