+++
author = "Brian Pfeil"
categories = ["HTML", "playground"]
date = 2021-04-05
description = ""
summary = " "
draft = false
slug = "cfn-diagram"
tags = ["cloudformation","diagram","tools"]
title = "CFN Diagram"
repoFullName = "pfeilbr/cfn-diagram-playground"
repoHTMLURL = "https://github.com/pfeilbr/cfn-diagram-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/cfn-diagram-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/cfn-diagram-playground</a>
</div>


learn [cfn-diagram](https://github.com/mhlabs/cfn-diagram)

> CLI tool to visualise CloudFormation/SAM/CDK templates as diagrams.

## Usage

```sh
# install
npm i -g @mhlabs/cfn-diagram

# draw.io render
cfn-dia draw.io --template-file CloudFrontS3WebsiteCdkStack.template.yaml \
    --output-file CloudFrontS3WebsiteCdkStack.drawio

# html render
cfn-dia html --template-file CloudFrontS3WebsiteCdkStack.template.yaml \
    --output-path CloudFrontS3WebsiteCdkStack-html
```

## Screenshots

![draw.io view in vscode](https://www.evernote.com/l/AAHOsXnnj4pIvKxyM_FrMsRFhlzkXpZ8gJAB/image.png)

![draw.io view in vscode - hover resource for details](https://www.evernote.com/l/AAGRXpA0ux5B75sYfg9yRmbXZ6y4oRJJJ-IB/image.png)

![html view](https://www.evernote.com/l/AAGeo4YVPvdAYY3xn-jZe7I3E5NCIS6lorUB/image.png)

## Notes

* good starting point.  generate draw.io to get all resources and icons, then modify from there.
* allows for filtering by resource types to eliminate resources that may not be needed.
* works by importing cfn template into CDK.  CDK allows to treat as graph for traversal and inspection

## Resources

* [mhlabs/cfn-diagram](https://github.com/mhlabs/cfn-diagram)
* [How (and Why) You Need To Start Generating Your Serverless Infrastructure Diagrams | Ready, Set, Cloud!](https://www.readysetcloud.io/blog/allen.helton/how-and-why-you-need-to-start-generating-your-diagrams/)
