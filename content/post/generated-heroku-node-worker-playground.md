+++
author = "Brian Pfeil"
categories = ["HTML", "playground"]
date = 2020-07-13
description = ""
summary = " "
draft = false
slug = "heroku-node-worker"
tags = ["heroku"]
title = "Heroku Node Worker"
repoFullName = "pfeilbr/heroku-node-worker-playground"
repoHTMLURL = "https://github.com/pfeilbr/heroku-node-worker-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/heroku-node-worker-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/heroku-node-worker-playground</a>
</div>


example of running a long lived worker process on heroku that is not a web app/server

## Prerequisites

* [heroku](https://heroku.com) account
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

## Running 

```sh
# clone
git clone https://github.com/pfeilbr/heroku-node-worker-playground.git

# change to root directory
cd heroku-node-worker-playground

# create heroku app
heroku create

# >>> make changes to `worker.js`, install packages, etc.

# test locally
npm run worker

# commit changes
git commit -a -m "my awesome changes"

# deploy / push changes to heroku
git push heroku master # if worker is already running, this push will kill it and start the new one

# run worker only / stop web dyno
heroku ps:scale web=0 worker=1

# verify running
heroku ps

# view logs
heroku logs -t

# stop worker
heroku ps:scale worker=0

# start worker
heroku ps:scale worker=1
```

## Resources

* [Background Jobs in Node.js with Redis](https://devcenter.heroku.com/articles/node-redis-workers)
* [Run Non-web Java Dynos on Heroku](https://devcenter.heroku.com/articles/run-non-web-java-processes-on-heroku)
