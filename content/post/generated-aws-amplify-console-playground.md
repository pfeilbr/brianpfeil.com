+++
author = "Brian Pfeil"
categories = ["CSS", "playground"]
date = 2019-09-09
description = ""
summary = " "
draft = false
slug = "aws-amplify-console"
tags = ["aws","amplify","playground",]
title = "AWS Amplify Console"
repoFullName = "pfeilbr/aws-amplify-console-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-amplify-console-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-amplify-console-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-amplify-console-playground</a>
</div>


learn [AWS Amplify Console](https://docs.aws.amazon.com/amplify/latest/userguide/welcome.html)

> AWS Amplify Console is a continuous delivery and hosting service for modern web applications. The AWS Amplify Console simplifies the deployment of your application front end and backend. Connect to your code repository and your front end and backend are deployed in a single workflow, on every code commit.

**Flow**

1. You specify a source (github, bitbucket, gitlab, S3, zip file upload).
2. On code change (commit), it checks out the code to a CodeBuild project.  Runs your build, test, [backend] deploy, etc.
3. Deploys static web assets (.html, .js, .css, images) to S3 to be served with CloudFront
4. Verifies deployment by visiting root site URL with various deveice form factors (iPhone, iPad, desktop) and taking screenshots.

Build settings are defined in [`amplify.yml`](amplify.yml).  See [Configuring Build Settings](https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html) for YML Specification Syntax.

---

set amplify service role.  codebuild env will assume this role and commands will execute in this context.
![](https://www.evernote.com/l/AAGKI4wgfUZB7YtWVDmqTmfg9YEzYSa4L38B/image.png)

showing assumed role in codebuild env
![](https://www.evernote.com/l/AAFxwKOPnvJLYb7DpmMr5vF7wLiU-xHSxUQB/image.png)

Update SAM deploy bucket policy to allow amplify service (`amplify.amazonaws.com`) to read/write to bucket.
![](https://www.evernote.com/l/AAHR9UMPba1ExLJ3iyLjgFUXFRWfOZhHP-0B/image.png)

Custom Domain configuration

![](https://www.evernote.com/l/AAF1AkVJrulEaqzahfCSFkXqjg48rR0uAyMB/image.png)

App running on custom domain <https://amplify-master.minote.net/>
![](https://www.evernote.com/l/AAGOQ8JEMwZEyKLvrvI8DHNtjnK2FR-Y9RUB/image.png)

## Resources

* [Amplify Console | Getting Started](https://aws.amazon.com/amplify/console/getting-started/)
* [aws-amplify/amplify-console](https://github.com/aws-amplify/amplify-console)


