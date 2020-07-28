+++
author = "Brian Pfeil"
categories = ["Python", "playground"]
date = 2019-08-07
description = ""
summary = " "
draft = false
slug = "pipenv"
tags = []
title = "Pipenv"
repoFullName = "pfeilbr/pipenv-playground"
repoHTMLURL = "https://github.com/pfeilbr/pipenv-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/pipenv-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/pipenv-playground</a>
</div>


learn [pipenv](https://github.com/pypa/pipenv)

> Pipenv is a tool that aims to bring the best of all packaging worlds (bundler, composer, npm, cargo, yarn, etc.) to the Python world. Windows is a first-class citizen, in our world.

> It automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your Pipfile as you install/uninstall packages. It also generates the ever-important Pipfile.lock, which is used to produce deterministic builds.

* based on <https://docs.python-guide.org/dev/virtualenvs/>

### Usage

```sh
# install
pip3 install pipenv

# create directory
cd ~/tmp
mkdir pipenv-playground
cd pipenv-playground

# install dependency
pipenv install requests

# write some code that uses the dependency
touch main.py

# run it using the created virtualenv
pipenv run python main.py

# can also specify `python3` explicitly
pipenv run python3 main.py

# try with jupyter notebook
cd ..
mkdir jupyter-notebook-playground
cd jupyter-notebook-playground
pipenv install jupyter
pipenv run jupyter notebook

# try with jupyterlab
pipenv install jupyterlab
pipenv run jupyter lab
```


