+++
author = "Brian Pfeil"
categories = ["Jupyter Notebook", "playground"]
date = 2024-01-14
description = ""
summary = " "
draft = false
slug = "instructor"
tags = ["ai","llm","python",]
title = "Instructor"
repoFullName = "pfeilbr/instructor-playground"
repoHTMLURL = "https://github.com/pfeilbr/instructor-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/instructor-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/instructor-playground</a>
</div>


learn [Instructor](https://jxnl.github.io/instructor/)

> Structured extraction in Python, powered by llms, designed for simplicity, transparency, and control.

see [`main.ipynb`](./main.ipynb)

## demo

```bash
# set local version of python for *this* shell
pyenv local 3.12

# create virtual environment with local version of python
python -m venv .venv

# activate environment
source ./.venv/bin/activate

# upgrade pip
pip install --upgrade pip

# install requirements
pip install -r requirements.txt

# freeze requirements
pip freeze > requirements.txt

# open main.ipynb in vscode
code main.ipynb

# OR open main.ipynb in `juypter lab`
juypter lab

# open http://localhost:8888/lab in browser
```

## resources

- <https://jxnl.github.io/instructor/>
- https://github.com/jxnl/instructor


