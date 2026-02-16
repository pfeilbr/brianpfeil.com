+++
author = "Brian Pfeil"
categories = ["Jupyter Notebook", "playground"]
date = 2020-10-05
description = ""
summary = " "
draft = false
slug = "boto3"
tags = ["boto","python"]
title = "Boto3"
repoFullName = "pfeilbr/boto3-playground"
repoHTMLURL = "https://github.com/pfeilbr/boto3-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/boto3-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/boto3-playground</a>
</div>


learn [boto3](https://github.com/boto/boto3), the Amazon Web Services (AWS) SDK for Python

## Concepts

**Clients** provide a low-level interface to AWS whose methods map close to 1:1 with service APIs. All service operations are supported by clients. Clients are generated from a JSON service definition file.

**Resources** represent an object-oriented interface to Amazon Web Services (AWS). They provide a higher-level abstraction than the raw, low-level calls made by service clients. To use resources, you invoke the resource() method of a Session and pass in a service name:

**Session** manages state about a particular configuration. By default, a session is created for you when needed. However, it's possible and recommended that in some scenarios you maintain your own session. Sessions typically store the following:

* Credentials
* AWS Region
* Other configurations related to your profile


**Collection** provides an iterable interface to a group of resources. A collection seamlessly handles pagination for you, making it possible to easily iterate over all items from all pages of data.


**Paginators**

Some AWS operations return results that are incomplete and require subsequent requests in order to attain the entire result set. The process of sending subsequent requests to continue where a previous request left off is called pagination.  Paginators are a feature of boto3 that act as an abstraction over the process of iterating over an entire result set of a truncated API operation.

---

## Developing

```sh
# install virtual env and dependencies
pipenv install

# (optional) install additional pip package
pipenv install <package>

# activate python virtual env (optional)
pipenv shell

# run on change
make dev

# --- running via jupyter notebook ---

# in vscode
# click on `main.ipynb`.  this will automatically start jupyter notebook and connect
# ctrl+enter to run cell
# ctrl+space for intellisense
# see [How to use Pipenv with Jupyter and VSCode](https://towardsdatascience.com/how-to-use-pipenv-with-jupyter-and-vscode-ae0e970df486)

# manually run jupyter notebook
pipenv run jupyter notebook

# access via browser manually (auto opens via above command)
open http://localhost:8888/tree

# convert notebook to python.  generates `main_notebook.py`
jupyter nbconvert --to script main.ipynb --output main_notebook
```

## Notes

for vscode, install [Pylance&#32;-&#32;Visual&#32;Studio&#32;Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension

## Resources

* [Boto3 documentation](https://boto3.readthedocs.io/)
* [boto/boto3](https://github.com/boto/boto3)
* [boto3-stubs](https://pypi.org/project/boto3-stubs/) - for code completion
* [Working with Jupyter Notebooks in Visual Studio Code](https://code.visualstudio.com/docs/python/jupyter-support)
* [How to use Pipenv with Jupyter and VSCode](https://towardsdatascience.com/how-to-use-pipenv-with-jupyter-and-vscode-ae0e970df486)
* [Big Upgrades are coming to VSCode Jupyter Notebooks](https://towardsdatascience.com/vscode-jupyter-notebooks-are-getting-an-upgrade-cc9aaaefc744)
