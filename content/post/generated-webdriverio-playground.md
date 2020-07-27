+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2015-08-20
description = ""
summary = "learn Webdriverio"
draft = false
slug = "webdriverio"
tags = ["github",]
title = "Webdriverio"
repoFullName = "pfeilbr/webdriverio-playground"
repoHTMLURL = "https://github.com/pfeilbr/webdriverio-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/webdriverio-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/webdriverio-playground</a>


# Running Selenium Standalone Server (Preferred / lighter weight)

1. Start selenium Standalone server

```sh
# run the following in it's own shell and leave running
$ java -jar selenium-server/selenium-server-standalone-2.53.0.jar
```

2. Run script

```sh
$ node index.js
```

# Running Selenium Hub and Node(s) Using Docker

1. start hub (clients connect to this)

		$ docker run -d -P --name selenium-hub -e GRID_TIMEOUT=10000 selenium/hub

2. start chrome node (hub delegates work to it)

		$ docker run -d --link selenium-hub:hub selenium/node-chrome

Get host and port for "selenium-hub" container and use them in your client.

![](http://static-content-01.s3-website-us-east-1.amazonaws.com//Kitematic_1B862C7B.png)

Example client config

```js
var options = {
	host: "192.168.99.100",
	port: 32768,
	desiredCapabilities: {
		browserName: 'chrome'
	}
};
```

see [`index.js`](index.js)



