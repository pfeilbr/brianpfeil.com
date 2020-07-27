+++
author = "Brian Pfeil"
categories = ["HTML", "playground"]
date = 2019-09-06
description = ""
summary = "learning AWS Polly"
draft = false
slug = "aws-polly"
tags = ["aws","polly","github",]
title = "AWS Polly"
repoFullName = "pfeilbr/aws-polly-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-polly-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/aws-polly-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-polly-playground</a>


learn [aws polly]() text-to-speech (TTS)

## Running

based on <https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/getting-started-browser.html#getting-started-browser-scenario>

update js code in [`polly.html`](polly.html) with the following

```js
AWS.config.region = '<YOUR_REGION>';
AWS.config.credentials = new AWS.CognitoIdentityCredentials({ IdentityPoolId: '<YOUR_IDENTITY_POOL_ID>' });
```

```sh
open polly.html
```


