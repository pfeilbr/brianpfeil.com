+++
author = "Brian Pfeil"
categories = ["Shell", "playground"]
date = 2020-02-10
description = ""
summary = "learn Bash Script Date and Time"
draft = false
slug = "bash-script-date-and-time"
tags = ["bash","playground",]
title = "Bash Script Date and Time"
repoFullName = "pfeilbr/bash-script-date-and-time-playground"
repoHTMLURL = "https://github.com/pfeilbr/bash-script-date-and-time-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/bash-script-date-and-time-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/bash-script-date-and-time-playground</a>
</div>


examples of working with formatted dates in bash including time operations such as adding time

see [`main.sh`](main.sh)

## Running

```sh
chmod a+x main.sh 
fswatch -o main.sh  | xargs -n1 -I{} sh main.sh
```


