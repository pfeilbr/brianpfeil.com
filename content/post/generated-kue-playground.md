+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2014-06-13
description = ""
summary = "learning Kue"
draft = false
slug = "kue"
tags = ["github",]
title = "Kue"
repoFullName = "pfeilbr/kue-playground"
repoHTMLURL = "https://github.com/pfeilbr/kue-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/kue-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/kue-playground</a>


Playground for learning / playing with [Kue](https://github.com/learnboost/kue).  Kue is a priority job queue for node.

## Running

	redis-server # start redis server
	node index.js -m process # run job processor
	node index.js -m create # run job creator in another terminal

View the Kue web ui at <http://localhost:3000>


