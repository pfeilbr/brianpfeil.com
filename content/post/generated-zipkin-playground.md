+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-08-21
description = ""
summary = " "
draft = false
slug = "zipkin"
tags = []
title = "Zipkin"
repoFullName = "pfeilbr/zipkin-playground"
repoHTMLURL = "https://github.com/pfeilbr/zipkin-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/zipkin-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/zipkin-playground</a>
</div>


learn [zipkin](https://zipkin.io/) the distributed tracing system


## Prerequisites

* docker

## Running

running zipkin server and viewing web ui

```sh
# run zipkin server (NOTE: this is non-blocking and will return)
docker run -d -p 9411:9411 openzipkin/zipkin

# open zipkin web ui
open http://localhost:9411/zipkin/
```

![](https://www.evernote.com/l/AAFl4da2EO1HQIyW4dUAv1wh1UFCpp88Yo8B/image.png)

running a web app with frontend and backend the sends traces to zipkin server.  see `frontend.js` for how code is instrumented to send traces to zipkin server.

```sh
# download zipkin javascript example
curl -LO https://github.com/openzipkin/zipkin-js-example/archive/master.zip
unzip master.zip

cd zipkin-js-example-master/web

# install dependencies
npm install

# had to run the following also.  this make be fixed
npm install node-fetch

# in `frontend.js` change `const {wrapAxios} = require("zipkin-instrumentation-axiosjs");`
# to `const wrapAxios = require("zipkin-instrumentation-axiosjs");`

# create bundle
npm run browserify

# run frontend and backend
DEBUG=true npm start
```

![](https://www.evernote.com/l/AAHVKM_tPYZGM4GibI-48ZR5dpJ22VG-PqcB/image.png)


```sh
# open app.  displays datetime and sends traces to zipkin sever.
open http://localhost:8081
```

![](https://www.evernote.com/l/AAF5drM4g8lIt4O395T9U0v4laR3OCPhN40B/image.png)

```sh
# now open zipkin web ui to view traces
open http://localhost:9411/zipkin/

# click the [Find Traces] button
```

![](https://www.evernote.com/l/AAH-0Lm2GqBHzLAD4bHSCLHlm3tzemyyjPIB/image.png)

![](https://www.evernote.com/l/AAGEdSFRciVPXr9S54kitexX9RZzct9j7w0B/image.png)

view JSON trace data by clickint the `[JSON]` button
![](https://www.evernote.com/l/AAGw7YDQejVCJrUr79X3LLtIUOM6T4fDJIAB/image.png)

```json
[
  {
    "traceId": "9ee01dfbbba1a5f2",
    "parentId": "f107fa7e6a7f29db",
    "id": "15f42a92f26d5a19",
    "kind": "SERVER",
    "name": "get /api",
    "timestamp": 1566397279334946,
    "duration": 1509626,
    "localEndpoint": {
      "serviceName": "backend",
      "ipv4": "192.168.1.14"
    },
    "tags": {
      "http.path": "/api",
      "http.status_code": "200"
    },
    "shared": true
  },
  {
    "traceId": "9ee01dfbbba1a5f2",
    "parentId": "f107fa7e6a7f29db",
    "id": "15f42a92f26d5a19",
    "kind": "CLIENT",
    "name": "get",
    "timestamp": 1566397279301452,
    "duration": 1542392,
    "localEndpoint": {
      "serviceName": "frontend"
    },
    "tags": {
      "http.path": "/api",
      "http.status_code": "200"
    }
  },
  {
    "traceId": "9ee01dfbbba1a5f2",
    "parentId": "9ee01dfbbba1a5f2",
    "id": "f107fa7e6a7f29db",
    "name": "pay-me",
    "timestamp": 1566397279295227,
    "duration": 1552644,
    "localEndpoint": {
      "serviceName": "frontend"
    }
  },
  {
    "traceId": "9ee01dfbbba1a5f2",
    "id": "9ee01dfbbba1a5f2",
    "kind": "SERVER",
    "name": "get /",
    "timestamp": 1566397279276961,
    "duration": 1572319,
    "localEndpoint": {
      "serviceName": "frontend",
      "ipv4": "192.168.1.14"
    },
    "tags": {
      "http.path": "/",
      "http.status_code": "200"
    }
  }
]
```


