+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2017-08-17
description = ""
summary = "learning AWS CloudFront"
draft = false
slug = "aws-cloudfront"
tags = ["aws","cloudfront","playground",]
title = "AWS CloudFront"
repoFullName = "pfeilbr/aws-cloudfront-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-cloudfront-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/aws-cloudfront-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-cloudfront-playground</a>
-->


steps to create a cloudfront distribution from s3 bucket with static website hosting turned on

1. create bucket and turn static website hosting on
    ![](https://www.evernote.com/l/AAGuAvyI8SdGOo37QxXYPzdRKRig484YSFQB/image.png)

2. create cloudfront distribution and select orgin bucket
    ![](https://www.evernote.com/l/AAFYupRz2OZAfZcv0FomCTLMd297l2IZsr8B/image.png)

3. set CNAME in cloudfront distribution
    ![](https://www.evernote.com/l/AAHTEItPLUFCBakChbIDhiim7uMTy5GiOaoB/image.png)

4. create CNAME in registrar ([hover](https://hover.com) in this case)for cloudfront distribution
    ![](https://www.evernote.com/l/AAGgnPPYq-9Iv6RBI8rP9cEBmt8qOzq2BvEB/image.png)

5. view content via friendly CNAME URL and cloudfront dist URL ![](https://www.evernote.com/l/AAFmBADWlBBNt5W6TVktvBMvo89jSKT6NSIB/image.png)


