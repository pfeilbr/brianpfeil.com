+++
author = "Brian Pfeil"
categories = ["Python", "playground"]
date = 2017-11-10
description = ""
summary = " "
draft = false
slug = "serverless-python"
tags = ["serverless","python",]
title = "Serverless Python"
repoFullName = "pfeilbr/serverless-python-playground"
repoHTMLURL = "https://github.com/pfeilbr/serverless-python-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/serverless-python-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/serverless-python-playground</a>
</div>


experiment with the [serverless framework](https://serverless.com/framework/) using python

based on <https://serverless.com/blog/serverless-python-packaging/>

**session**

```sh
# install `serverless framework` if not already installed
npm install serverless -g

# create serverless python project
serverless create --template aws-python3  --name numpy-test --path numpy-test

cd numpy-test

# create isolated virtualenv
virtualenv venv --python=python3
touch handler.py
code .
# add code for `handler.py`

# activate virtualenv
source venv/bin/activate

# run to test
python handler.py

pip install numpy

# save dependencies
pip freeze > requirements.txt
cat requirements.txt

# install dependencies (don't need to execute if starting from scratch)
pip install -r requirements.txt

python handler.py
npm init --force

# add serverless `serverless-python-requirements` plugin
npm install --save serverless-python-requirements

# deploy
sls deploy

# invoke lambda and output log
sls invoke -f numpy --log

# cleanup
sls remove
```


