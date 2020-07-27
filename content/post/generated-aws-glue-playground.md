+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-07-09
description = ""
summary = "experimenting with AWS Glue"
draft = false
slug = "aws-glue"
tags = ["aws","glue","github",]
title = "AWS Glue"
repoFullName = "pfeilbr/aws-glue-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-glue-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/aws-glue-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-glue-playground</a>


learn and experiment with [aws glue](https://aws.amazon.com/glue/)

## Running ["Python Shell"](https://docs.aws.amazon.com/glue/latest/dg/add-job-python.html) Job

### Local Running/Testing of Script

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/python3-shell-job-example.py
```

### Running/Submitting Python Shell Job

```sh
cp .env.sample .env
# modify .env for your environment

# following submits the job (scripts/python3-shell-job-example.py)
node src/job-runner.js run-python-shell-script scripts/python3-shell-job-example.py
```

## Steps to Run [`scripts/example-notebook-script-01.py`](scripts/example-notebook-script-01.py) in SageMaker notebook

see [`scripts/example-notebook-script-01.py`](scripts/example-notebook-script-01.py)

1. upload data.csv to S3
1. create glue crawler for data.csv which results in a table in glue database being created
    > you can verify by previewing the data in athena
1. create aws glue Dev Endpoint
    > no need to specify ssh key
1. create SageMaker notebook
    > SageMaker notebook works just like Zepplin notebook, but less setup steps.
1. open SageMaker notebook and past in code from [`scripts/example-notebook-script-01.py`](scripts/example-notebook-script-01.py)



