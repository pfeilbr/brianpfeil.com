+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-05-10
description = ""
summary = " "
draft = false
slug = "python-2.x-websocket-client"
tags = ["python"]
title = "Python 2.X WebSocket Client"
repoFullName = "pfeilbr/python-2.x-websocket-client-playground"
repoHTMLURL = "https://github.com/pfeilbr/python-2.x-websocket-client-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/python-2.x-websocket-client-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/python-2.x-websocket-client-playground</a>
</div>


learn python [websocket-client](https://github.com/websocket-client/websocket-client) module

## prerequisites

- python 2.x
- node.js: for local websocket server. code is from https://glitch.com/~socketio-basic.  uses [ws: a Node.js WebSocket library](https://github.com/websockets/ws)
- virtualenv: `pip install virtualenv` or `sudo pip install virtualenv`

## running

```sh
# server (node.js) - run in own terminal (blocking)
cd src/server
npm i
npm start

# client - run in separate terminal
cd src/client
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python client.py
```

example run

![](https://www.evernote.com/l/AAFaIvf7mthMmJO0Q4o62USTYJES2wvIXCsB/image.png)
