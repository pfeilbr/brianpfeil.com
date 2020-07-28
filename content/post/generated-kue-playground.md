+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2014-06-13
description = ""
summary = "learn Kue"
draft = false
slug = "kue"
tags = ["playground",]
title = "Kue"
repoFullName = "pfeilbr/kue-playground"
repoHTMLURL = "https://github.com/pfeilbr/kue-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/kue-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/kue-playground</a>
</div>


Playground for learning / playing with [Kue](https://github.com/learnboost/kue).  Kue is a priority job queue for node.

## Running

	redis-server # start redis server
	node index.js -m process # run job processor
	node index.js -m create # run job creator in another terminal

View the Kue web ui at <http://localhost:3000>


