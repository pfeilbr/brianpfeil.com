+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2021-04-06
description = ""
summary = " "
draft = false
slug = "api-gateway-private-endpoints"
tags = ["aws","api-gateway","vpc","network",]
title = "API Gateway Private Endpoints"
repoFullName = "pfeilbr/api-gateway-private-endpoints-playground"
repoHTMLURL = "https://github.com/pfeilbr/api-gateway-private-endpoints-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/api-gateway-private-endpoints-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/api-gateway-private-endpoints-playground</a>
</div>


learn API Gateway private endpoints

![](https://www.evernote.com/l/AAGwfzGWmcBKyavQg5roa4luW4ud_iUkA_wB/image.png)
## Setup Steps

configure API Gateway private endpoint that leverages HTTP proxy integration.  Test via lambda with VPC config that issues HTTP GET request to vpc endpoint.

**Notes**

* supported on REST API endpoints (not HTTP API at the time 2021-04-05)
* be sure to re-deploy API for policy changes
* check security groups
* check VPC endpoint policy
* check lambda VPC config and security groups

---

**API Gateway resource policy**

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "execute-api:Invoke",
            "Resource": "arn:aws:execute-api:us-east-1:529276214230:scheqe4ymi/*",
            "Condition": {
                "StringNotEquals": {
                    "aws:sourceVpce": "vpce-02b487f2d021986fb"
                }
            }
        },
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "execute-api:Invoke",
            "Resource": "arn:aws:execute-api:us-east-1:529276214230:scheqe4ymi/*"
        }
    ]
}
```

> note the `Deny` + `Allow` combination*

---

**Lambda test code**

```javascript
const https = require('https');

exports.handler =  (event, context, callback) => {
   // https://scheqe4ymi.execute-api.us-east-1.amazonaws.com/prod
    var options = {
      host: 'vpce-02b487f2d021986fb-yl0hav78.execute-api.us-east-1.vpce.amazonaws.com',
      path: '/prod/index.html',
      method: 'GET',
      port: 443,
      headers: {
          'Host':'scheqe4ymi.execute-api.us-east-1.amazonaws.com'
      }
    };

    const cb = function(response) {
      let str = '';
      response.on('data', function (chunk) {
        str += chunk;
      });
      response.on('end', function () {
        console.log(str);
        const response = {
            statusCode: 200,
            body: JSON.stringify(str),
        };
        callback(null, response)
        return response;
      });
    }

    https.request(options, cb).end();
}
```

> note the `Host` header that allows for the request to be routed
## Screenshots

![vpc endpoint](https://www.evernote.com/l/AAH6tr5RhgxNK61jSXvjZo7cmQMffnGKCi8B/image.png)

![vpc endpoint policy](https://www.evernote.com/l/AAEXuCeCfH1Fkq5M_JSsdQoZiKA3GW4R22wB/image.png)

![allowed vpc endpoint ids to api gateway](https://www.evernote.com/l/AAGVD-ntdc5BubphIWrF-86BSTmUc3JhDeAB/image.png)

## Resources

* [Introducing Amazon API Gateway Private Endpoints | Amazon Web Services](https://aws.amazon.com/blogs/compute/introducing-amazon-api-gateway-private-endpoints/)
* [How do I troubleshoot issues connecting to an API Gateway private API endpoint?](https://aws.amazon.com/premiumsupport/knowledge-center/api-gateway-private-endpoint-connection)


