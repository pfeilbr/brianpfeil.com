+++
author = "Brian Pfeil"
categories = ["HTML", "playground"]
date = 2019-09-06
description = ""
summary = " "
draft = false
slug = "aws-polly"
tags = ["aws","polly"]
title = "AWS Polly"
repoFullName = "pfeilbr/aws-polly-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-polly-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-polly-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-polly-playground</a>
</div>


learn [aws polly]() text-to-speech (TTS)

## Running

based on <https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/getting-started-browser.html#getting-started-browser-scenario>

update js code in [`polly.html`](https://github.com/pfeilbr/aws-polly-playground/blob/master/polly.html) with the following

```js
AWS.config.region = '<YOUR_REGION>';
AWS.config.credentials = new AWS.CognitoIdentityCredentials({ IdentityPoolId: '<YOUR_IDENTITY_POOL_ID>' });
```

```sh
open polly.html
```
