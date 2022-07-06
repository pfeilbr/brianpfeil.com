+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2022-07-01
description = ""
summary = " "
draft = false
slug = "rstudio-on-sagemaker"
tags = ["sagemaker","machine-learning",]
title = "RStudio On SageMaker"
repoFullName = "pfeilbr/rstudio-on-sagemaker-playground"
repoHTMLURL = "https://github.com/pfeilbr/rstudio-on-sagemaker-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/rstudio-on-sagemaker-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/rstudio-on-sagemaker-playground</a>
</div>


learn [RStudio on Amazon SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/rstudio-use.html)

## Notes

- fully managed and self-serve RStudio solution.  elimiinates administrative overhead.
- access to scalable AWS resources
- provides R users with native environment  withing SageMaker
- direct access to all tools SageMaker offers (via [reticulate](https://rstudio.github.io/reticulate/))
- fully integrated with SageMaker ecosystem.  e.g. Access to SageMaker Built-In Algorithms
- browser based RStudio workbench
- launch RStudio app w/in SageMaker Domain
- launch RStudio session
  - select ec2 instance type
- session has user home directory backed by s3
- installed R pkgs are preserved in home dir
- every session uses same home dir
- develop shiny apps, etc. plumber apis
- [R reticulate package](https://rstudio.github.io/reticulate/) offers integration with python for working with SM easily from R
  - import py package and ref from r variable. proxies calls from r to py
- coming soon
  - custom images for RStudio Workbench
  - RStudio Connect managed by SageMaker
    > RStudio Connect is a publishing platform for the work your teams create in R and Python. RStudio Connect allows you to share the following, and more, in one convenient place: Shiny applications. R Markdown reports. Plumber APIs.

## Screenshots

Launch RStudio from SM Domain

![](https://www.evernote.com/l/AAEQHPKHaTBJH5f8xVyX8qzRdh65ba_5xEQB/image.png)

---

Creating new session in Studio Workbench

![](https://www.evernote.com/l/AAFiri3so4hHYan2WCQTTIFktPIZf1j5XGcB/image.png)

---

Workbench UI

![](https://www.evernote.com/l/AAFT-nHBCUNErZJbVv_lPkzRFRImmnOpRhQB/image.png)

---

Shiny App Example

![](https://www.evernote.com/l/AAGIHWXIq2RPT7soWcQPYCp1shS4kM9a7vsB/image.png)

---

Plumber API Example

![](https://www.evernote.com/l/AAG7J_MsAshIo7HV5nIh7ixB-uuHWDohF1wB/image.png)

---

R Integration with Boto3 SageMaker package via [R reticulate package](https://rstudio.github.io/reticulate/)

![](https://www.evernote.com/l/AAG1nRkNGV9N6J2xhqGpFEej26prpF95ht4B/image.png)

---

Running SageMaker Training Job from R

![](https://www.evernote.com/l/AAFTYyt6bNpKLbWsgrUtzY7jKcNohpyPkSAB/image.png)

---

Deploying SageMaker Real-time Predication API Endpoint

![](https://www.evernote.com/l/AAEElKknxDlLPJeb4gP0-sadaFbmh2uuOPwB/image.png)

---

## Resources

- [Announcing Fully Managed RStudio on Amazon SageMaker for Data Scientists](https://aws.amazon.com/blogs/aws/announcing-fully-managed-rstudio-on-amazon-sagemaker-for-data-scientists/)
- [Use RStudio on Amazon SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/rstudio-use.html)
- [Using RStudio on Amazon SageMaker: Questions from the Community](https://www.rstudio.com/blog/using-rstudio-on-amazon-sagemaker-faq/)
- [James Blair | Using RStudio on Amazon SageMaker | RStudio](https://www.youtube.com/watch?v=fmgSVRWgXDg) - good video with demo
- [blairj09-talks/rstudio-sagemaker-webinar](https://github.com/blairj09-talks/rstudio-sagemaker-webinar) - slides from [James Blair | Using RStudio on Amazon SageMaker | RStudio](https://www.youtube.com/watch?v=fmgSVRWgXDg) video.  direct link [slides.pdf](https://github.com/blairj09-talks/rstudio-sagemaker-webinar/blob/main/slides/slides.pdf)
- [aws/amazon-sagemaker-examples/r_examples/](https://github.com/aws/amazon-sagemaker-examples/tree/main/r_examples)


