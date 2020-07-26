+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2020-07-16
description = ""
summary = "learning AWS Interactive Video Service"
draft = false
slug = "aws-interactive-video-service"
tags = ["aws","github",]
title = "AWS Interactive Video Service"
repoFullName = "pfeilbr/aws-interactive-video-service-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-interactive-video-service-playground"
truncated = true

+++


* learn [Amazon Interactive Video Service](https://aws.amazon.com/ivs/)
* based on [Getting Started with Amazon Interactive Video Service](https://docs.aws.amazon.com/ivs/latest/userguide/GSIVS.html)

## Running

```sh
# create channel via https://docs.aws.amazon.com/ivs/latest/userguide/GSIVS.html

# streaming an existing video via ffmpeg
VIDEO_FILEPATH="/Users/pfeilbr/Downloads/tailer.mp4" # fortnite game trailer
STREAM_KEY="sk_us-east-1_LvBpPyJZzkix_yMQ6LPLZ7PDr6dYsI0zqM4H2oZTL31"
INGEST_ENDPOINT="0f426742eaf2.global-contribute.live-video.net"
ffmpeg -re -stream_loop -1 -i $VIDEO_FILEPATH -r 30 -c:v libx264 -pix_fmt yuv420p -profile:v main -preset veryfast -x264opts "nal-hrd=cbr:no-scenecut" -minrate 3000 -maxrate 3000 -g 60 -c:a aac -b:a 160k -ac 2 -ar 44100 -f flv rtmps://$INGEST_ENDPOINT/app/$STREAM_KEY

# view in AWS Console | Amazon IVS | Live Channels
```

## Screenshots

![](https://www.evernote.com/l/AAFa7oChA05JpI0i9PC5gj-l648GvLF3BIgB/image.png)

![](https://www.evernote.com/l/AAGmb02aSWRIUa6ENjw3AJr6FUfxuhHyknsB/image.png)

![](https://www.evernote.com/l/AAEIUY_5Tn5PFL-iZ12eO22sNENgY2XQSi4B/image.png)

## Resources

* [Introducing Amazon Interactive Video Service (Amazon IVS)](https://aws.amazon.com/about-aws/whats-new/2020/07/introducing-amazon-ivs/)
* [Amazon Interactive Video Service – Add Live Video to Your Apps and Websites](https://aws.amazon.com/blogs/aws/amazon-interactive-video-service-add-live-video-to-your-apps-and-websites/)
* [Amazon Interactive Video | Docs](https://docs.aws.amazon.com/ivs/latest/userguide/what-is.html)

