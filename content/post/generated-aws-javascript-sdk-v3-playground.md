+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2020-10-26
description = ""
summary = " "
draft = false
slug = "aws-javascript-sdk-v3"
tags = ["aws","sdk","javascript",]
title = "AWS JavaScript SDK V3"
repoFullName = "pfeilbr/aws-javascript-sdk-v3-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-javascript-sdk-v3-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-javascript-sdk-v3-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-javascript-sdk-v3-playground</a>
</div>


learn AWS JavaScript SDK v3

* [`index.js`](index.js)
* [`index.test.js`](index.test.js)

---

## New Features

### v3 Commands

>  commands for each AWS Service package to enable you to perform operations for that AWS Service. After you install an AWS Service, you can browse the available commands in your project's node-modules/@aws-sdk/client-PACKAGE_NAME/commands folder

### middleware stack

> can use a new middleware stack to control the lifecycle of an operation call

> Each middleware stage in the stack calls the next middleware stage after making any changes to the request object. This also makes debugging issues in the stack much easier, because you can see exactly which middleware stages were called leading up to the error.

**Use Cases**

* debugging
* logging
* request updates
* instrumentation

**Example middleware `args`**

`DynamoDB` `ListTablesCommand`

```js
{
      middlewareStack: {
        add: [Function: add],
        addRelativeTo: [Function: addRelativeTo],
        clone: [Function: clone],
        use: [Function: use],
        remove: [Function: remove],
        removeByTag: [Function: removeByTag],
        concat: [Function: concat],
        applyToStack: [Function: cloneTo],
        resolve: [Function: resolve]
      },
      input: {},
      request: HttpRequest {
        method: 'POST',
        hostname: 'dynamodb.us-east-1.amazonaws.com',
        port: undefined,
        query: {},
        headers: {
          'Content-Type': 'application/x-amz-json-1.0',
          'X-Amz-Target': 'DynamoDB_20120810.ListTables',
          'user-agent': 'aws-sdk-nodejs-v3-@aws-sdk/client-dynamodb/1.0.0-rc.2 darwin/v12.16.1',
          'content-length': '2'
        },
        body: '{}',
        protocol: 'https:',
        path: '/'
      }
    }
```

---

## Running

```sh
# run tests that exercise new features
npm run test -- --watch
```

## Resources

* [aws/aws-sdk-js-v3](https://github.com/aws/aws-sdk-js-v3)
* [AWS SDK for JavaScript | Developer Guide for SDK Version 3](https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/welcome.html)
* [Modular AWS SDK for JavaScript – Release Candidate](https://aws.amazon.com/blogs/developer/modular-aws-sdk-for-javascript-release-candidate/)


