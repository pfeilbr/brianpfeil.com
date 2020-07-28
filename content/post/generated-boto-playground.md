+++
author = "Brian Pfeil"
categories = ["Python", "playground"]
date = 2017-10-30
description = ""
summary = " "
draft = false
slug = "boto"
tags = ["boto",]
title = "Boto"
repoFullName = "pfeilbr/boto-playground"
repoHTMLURL = "https://github.com/pfeilbr/boto-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/boto-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/boto-playground</a>
</div>


learn and experiment with [Boto 3 / AWS SDK for Python](https://github.com/boto/boto3) 

**Initial setup**

```sh
git clone <this repo>

# ensure python 3.x
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip install boto3
pip install -U python-dotenv

# save dependencies
pip freeze > requirements.txt
```

**Running**

```sh
# setup virtualenv
source venv/bin/activate
pip install -r requirements.txt

# run script
python s3-example.py

# exit virtualenv / deactivate
deactivate
```


