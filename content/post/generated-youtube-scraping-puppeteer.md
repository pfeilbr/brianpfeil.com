+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2020-04-16
description = ""
summary = " "
draft = false
slug = "youtube-scraping-with-puppeteer"
tags = ["puppeteer","nodejs","youtube","scraping"]
title = "YouTube Scraping with Puppeteer"
repoFullName = "pfeilbr/youtube-scraping-puppeteer"
repoHTMLURL = "https://github.com/pfeilbr/youtube-scraping-puppeteer"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/youtube-scraping-puppeteer" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/youtube-scraping-puppeteer</a>
</div>


example of using [Puppeteer](https://pptr.dev/) Chrome browser automation to scrape youtube content

see [`src/index.js`](https://github.com/pfeilbr/youtube-scraping-puppeteer/blob/master/src/index.js)

## Running

```sh
# install
npm install

# run
npm start

# output is stored as a json file for each channel in the `data/` directory
# create csv from json using `jq`
cat data/AmazonWebServices-channel-videos.json | jq -r '.[] | [.title, .url] | @csv' > data/AmazonWebServices-channel-videos.csv
cat data/AWSwebinars-channel-videos.json | jq -r '.[] | [.title, .url] | @csv' > data/AWSwebinars-channel-videos.csv
```
