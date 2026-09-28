+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-07-08
description = ""
summary = " "
draft = false
slug = "aws-rekognition"
tags = ["aws"]
title = "AWS Rekognition"
repoFullName = "pfeilbr/aws-rekognition-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-rekognition-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-rekognition-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-rekognition-playground</a>
</div>


learn [AWS Rekognition](https://docs.aws.amazon.com/rekognition/)

see [`src/examples.js`](https://github.com/pfeilbr/aws-rekognition-playground/blob/master/src/examples.js)

## Prerequisites

* [AWS default credentials](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html) available to call Rekognition API
* install imagemagick, graphicsmagick, and ghostscript (for fonts) for labelling image

    ```sh
    brew install imagemagick
    brew install graphicsmagick
    brew install ghostscript
    ```

## Example Labelled Image Using [`detectLabels`](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/Rekognition.html#detectLabels-property) API

**Source**
![](https://raw.githubusercontent.com/pfeilbr/aws-rekognition-playground/master/assets/images/city-street.jpg)

**Labelled**
![](https://raw.githubusercontent.com/pfeilbr/aws-rekognition-playground/master/assets/images/city-street.jpg-labelled.jpg)


## Example Labelled Image Using [`detectText`](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/Rekognition.html#detectText-property) API

**Source**
![](https://raw.githubusercontent.com/pfeilbr/aws-rekognition-playground/master/assets/images/book-cover.jpg)

**Labelled**
![](https://raw.githubusercontent.com/pfeilbr/aws-rekognition-playground/master/assets/images/book-cover.jpg-labelled.jpg)


## Running

```sh
npm install
npm start
```

---

## Video Label Detection Example via CLI

```sh
# start (it's async)
aws rekognition start-label-detection --video "S3Object={Bucket=rekognition-playground,Name=SampleVideo_1280x720_1mb.mp4}"

# output
{
    "JobId": "2c9b387607977af21c0839f177bf7034ce1bcd5139810b533dea3deb6361f348"
}

# in progress
aws rekognition get-label-detection  --job-id "2c9b387607977af21c0839f177bf7034ce1bcd5139810b533dea3deb6361f348"

# output
{
    "Labels": [],
    "LabelModelVersion": "2.0",
    "JobStatus": "IN_PROGRESS"
}

# completed
aws rekognition get-label-detection  --job-id "2c9b387607977af21c0839f177bf7034ce1bcd5139810b533dea3deb6361f348"

# output
{
    "Labels": [
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 89.929931640625, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 69.0970458984375, 
                "Parents": [
                    {
```

*… 3753 more lines — see the [full README](https://github.com/pfeilbr/aws-rekognition-playground#readme).*
