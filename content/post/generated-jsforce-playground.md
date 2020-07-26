+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2014-06-12
description = ""
summary = "learning Jsforce"
draft = false
slug = "jsforce"
tags = ["github",]
title = "Jsforce"
repoFullName = "pfeilbr/jsforce-playground"
repoHTMLURL = "https://github.com/pfeilbr/jsforce-playground"
truncated = true

+++


Area to learn and play with [JSForce](http://jsforce.github.io/).  [index.js]() contains the code.

### `migrator.js`

migrates salesforce metadata from a source org to a target org

To Run

```sh
$ ./node_modules/.bin/babel-node migrator.js
```

### `sharing-rules-operations.js`

created country code firewall criteria based sharing rules

To Run

```sh
$ ./node_modules/.bin/babel-node sharing-rules-operations.js
```


### `account-fetcher.js`

**Developing**

```sh
$ DEBUG=account* nodemon -e js account-fetcher.js
```

