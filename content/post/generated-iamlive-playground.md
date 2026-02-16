+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2021-12-02
description = ""
summary = " "
draft = false
slug = "iamlive"
tags = ["aws","iam"]
title = "Iamlive"
repoFullName = "pfeilbr/iamlive-playground"
repoHTMLURL = "https://github.com/pfeilbr/iamlive-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/iamlive-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/iamlive-playground</a>
</div>


learn [iann0036/iamlive](https://github.com/iann0036/iamlive) - cli tool to *Generate an IAM policy from AWS calls using client-side monitoring (CSM) or embedded proxy*

## Demo

### CSM Mode (Client-side monitoring mode) Example with AWS CLI

```sh
# run in CSM mode example and generate policy from aws cli
# can add `--output-file iamlive-policy-output.json` to save generated policy in file
iamlive --set-ini

# run the following in another shell
aws s3 ls s3://com.brianpfeil.scratch01
```

![](https://www.evernote.com/l/AAGpI2UD7ldEYZs7Kv4Uo_48n1eX6UJ158kB/image.png)

---

### Proxy Mode Example with AWS CLI

```sh
# run in proxy  mode example and generate policy from aws cli
iamlive --set-ini --mode proxy

# run the following in another shell
export AWS_CA_BUNDLE=~/.iamlive/ca.pem
export HTTP_PROXY=http://127.0.0.1:10080
export HTTPS_PROXY=http://127.0.0.1:10080

```

![](https://www.evernote.com/l/AAFtqiFxwE9BGY9heMsWQedo93hOf-d4v14B/image.png)

---

### CSM Mode (Client-side monitoring mode) Example with [AWS SDK for JavaScript v2](https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/welcome.html)

see [`index.js`](https://github.com/pfeilbr/iamlive-playground/blob/master/index.js)

```sh
# run in CSM mode example and generate policy from aws cli
iamlive --set-ini

# run the following in another shell

# install node deps
npm install

# run nodejs script that uses `aws-sdk`
node index.js

```

![](https://www.evernote.com/l/AAFIuQirVhBCp7Hb991ciQsp3g35jsHKvhcB/image.png)

---

## Resources

* [iann0036/iamlive](https://github.com/iann0036/iamlive)
