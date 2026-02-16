+++
author = "Brian Pfeil"
categories = ["Python", "playground"]
date = 2021-09-13
description = ""
summary = " "
draft = false
slug = "hugging-face"
tags = ["machine-learning","nlp","python"]
title = "Hugging Face"
repoFullName = "pfeilbr/hugging-face-playground"
repoHTMLURL = "https://github.com/pfeilbr/hugging-face-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/hugging-face-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/hugging-face-playground</a>
</div>


learn [hugging face](https://huggingface.co/) transformers (transfer learning)

based on [Hugging Face Transformers Package &#8211; What Is It and How To Use It - KDnuggets](https://www.kdnuggets.com/2021/02/hugging-face-transformer-basics.html)


Transformers is an opinionated library built for:

* NLP researchers and educators seeking to use/study/extend large-scale transformers models
* hands-on practitioners who want to fine-tune those models and/or serve them in production
* engineers who just want to download a pretrained model and use it to solve a given NLP task.

## Demo

```sh
pipenv install
pipenv install transformers
pipenv install tensorflow

# test install
python -c "from transformers import pipeline; print(pipeline('sentiment-analysis')('we love you'))"

# note first run will download the [pipeline] model (potentially time consuming) on first run
pipenv run python main.py
```

![](https://www.evernote.com/l/AAGJ7GymnFRD87nLrwZ1ehn0FHn-GnjiqicB/image.png)

## Resourcces

* [Hugging Face – The AI community building the future.](https://huggingface.co/)
* [Hugging Face Transformers Package &#8211; What Is It and How To Use It - KDnuggets](https://www.kdnuggets.com/2021/02/hugging-face-transformer-basics.html)
* [Hosting Hugging Face models on AWS Lambda for serverless inference | Amazon Web Services](https://aws.amazon.com/blogs/compute/hosting-hugging-face-models-on-aws-lambda/)
