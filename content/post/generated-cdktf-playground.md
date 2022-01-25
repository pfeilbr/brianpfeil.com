+++
author = "Brian Pfeil"
categories = ["TypeScript", "playground"]
date = 2021-09-03
description = ""
summary = " "
draft = false
slug = "cdktf"
tags = ["aws","cdk","terraform",]
title = "CDKTF"
repoFullName = "pfeilbr/cdktf-playground"
repoHTMLURL = "https://github.com/pfeilbr/cdktf-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/cdktf-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/cdktf-playground</a>
</div>


learn cdktf.  based on [Build AWS Infrastructure with TypeScript](https://learn.hashicorp.com/tutorials/terraform/cdktf-build)

## Notes

* cdktf generates tf hcl json
* cdktf synth creates `cdktf.out`
* can use tf apply within a `cdktf.out/stacks/*` directory to deploy
* or let cdktf do both the synth and tf deploy

## Demo

```sh
cdktf init --template=typescript --local

# add aws provider to `cdktf.json` // "hashicorp/aws@~> 3.42"

# creates `.gen` folder which is codegend .ts
cdktf get

# edit `main.ts`

# deploy
cdktf deploy

# clean up
cdktf destroy
```

**Directory Structure**

![](https://www.evernote.com/l/AAGimu-wZYVBPoSWHzvmMRQVCtMkRE0DLMEB/image.png)

**Deploy Output**

![](https://www.evernote.com/l/AAEg6JEtPxJIo67G-wcFzSwLsaBDhB0XJY0B/image.png)

**Destroy Output**

![](https://www.evernote.com/l/AAEyX839eA1MEKGxcifO5JRrYcMGv_ibG58B/image.png)

## Resources

* [Write CDK for Terraform configurations](https://learn.hashicorp.com/collections/terraform/cdktf)



