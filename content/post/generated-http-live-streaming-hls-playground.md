+++
author = "Brian Pfeil"
categories = ["HTML", "playground"]
date = 2020-03-23
description = ""
summary = "experimenting with HTTP Live Streaming HLS"
draft = false
slug = "http-live-streaming-hls"
tags = ["github",]
title = "HTTP Live Streaming HLS"
repoFullName = "pfeilbr/http-live-streaming-hls-playground"
repoHTMLURL = "https://github.com/pfeilbr/http-live-streaming-hls-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/http-live-streaming-hls-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/http-live-streaming-hls-playground</a>


example of creating an HTTP Live Stream video stream from an h.264 video file.

### Prerequisites

* download and install "HTTP Live Streaming Tools" from https://developer.apple.com/download/more/?=HLS (binaries are installed to `/usr/local/bin`)
    > need to login with apple developer account

### Running

```sh
# create segments for HTTP Live Streaming from media file
mediafilesegmenter \
  -f ./public \
  ./assets/video/SampleVideo_1280x720_10mb.mp4

cd public
python -m SimpleHTTPServer 8000
open http://localhost:8000/
```

* [`public/index.html`](public/index.html) - include js code for video playback
* [`assets/video/SampleVideo_1280x720_10mb.mp4`](assets/video/SampleVideo_1280x720_10mb.mp4) - sample video

### Resources

* [How can I play a m3u8 (file) video using the HTML5 <video> element?](https://stackoverflow.com/questions/41014197/how-can-i-play-a-m3u8-file-video-using-the-html5-video-element)
* [sample-videos.com](https://www.sample-videos.com/)
* [HTTP Live Streaming](https://en.wikipedia.org/wiki/HTTP_Live_Streaming)



