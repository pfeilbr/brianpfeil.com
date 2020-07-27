+++
author = "Brian Pfeil"
categories = ["Shell", "playground"]
date = 2020-02-10
description = ""
summary = "learning Bash Script Date And Time"
draft = false
slug = "bash-script-date-and-time"
tags = ["bash","github",]
title = "Bash Script Date And Time"
repoFullName = "pfeilbr/bash-script-date-and-time-playground"
repoHTMLURL = "https://github.com/pfeilbr/bash-script-date-and-time-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/bash-script-date-and-time-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/bash-script-date-and-time-playground</a>


examples of working with formatted dates in bash including time operations such as adding time

see [`main.sh`](main.sh)

## Running

```sh
chmod a+x main.sh 
fswatch -o main.sh  | xargs -n1 -I{} sh main.sh
```


