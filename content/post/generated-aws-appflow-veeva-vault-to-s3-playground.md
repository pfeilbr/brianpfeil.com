+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2020-09-08
description = ""
summary = " "
draft = false
slug = "aws-appflow-veeva-vault-to-s3"
tags = ["aws","appflow","s3"]
title = "AWS AppFlow Veeva Vault to S3"
repoFullName = "pfeilbr/aws-appflow-veeva-vault-to-s3-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-appflow-veeva-vault-to-s3-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-appflow-veeva-vault-to-s3-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-appflow-veeva-vault-to-s3-playground</a>
</div>


[AWS AppFlow](https://aws.amazon.com/appflow/) example of Veeva Vault data -> AppFlow -> S3.

## Notes

* no events from Vault.  only poll / query existing data manually/on demand or schedule.
    ![](https://www.evernote.com/l/AAF3BbJNMHdIaLNUl9hNZAHO8Zr3e7bSZ1MB/image.png)
* at the time (2020-09-08) EventBridge was not available as a destination.
  * available destinations: redshift, s3, salesforce

## Screenshot Tour

veeva vault data source general information

![](https://www.evernote.com/l/AAE4K0xTZj9ISLsONEom0QqFaIaMVLrjUnsB/image.png)

![](https://www.evernote.com/l/AAHUtXCllmhCcL9GDEM3niCGEzB9JgG-3OsB/image.png)

veeva vault org

![](https://www.evernote.com/l/AAGxHwv8cW9MeIDr3Cz9Duqg7wr5Oj6ukrkB/image.png)


veeva vault connection

![](https://www.evernote.com/l/AAHRq_vW-vNLlIsvbObynfHTqtZdZz1Q1gAB/image.png)

source -> destination

![](https://www.evernote.com/l/AAFCvNEVU0BN-YZKQZibgPJBqJzrMcfs0LEB/image.png)

mapping

![](https://www.evernote.com/l/AAFUFvxxDcVJJLSOtBohXBcELSRI6VQrC7cB/image.png)

![](https://www.evernote.com/l/AAGCQd2v2sVAe4sOxBweWzz-O6iZdj93ENYB/image.png)

created

![](https://www.evernote.com/l/AAHfQEEVKGFNVbg_ir7aBoxYBVwjhYcpDZkB/image.png)


run history

![](https://www.evernote.com/l/AAEW45w_DDJIgbJm_ucY-uMGAxoohGZ8AwwB/image.png)

data landed in s3

![](https://www.evernote.com/l/AAE_dm6okTFHs6TCPnRfFcmAdBo-yIVHs7YB/image.png)

![](https://www.evernote.com/l/AAFejlfQEE1J1LfEmGJ-hra2Tn3FRWgKzVsB/image.png)

## Resources

* [AppFlow Saas Applications | Veeva Vault](https://aws.amazon.com/appflow/integrations/#Veeva)
* [https://developer.veevavault.com/](https://developer.veevavault.com/)
