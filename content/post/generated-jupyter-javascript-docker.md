+++
author = "Brian Pfeil"
categories = ["Jupyter Notebook", "playground"]
date = 2019-01-16
description = "docker image for running jupyter notebooks with javascript (Node.js) code"
summary = " "
draft = false
slug = "jupyter-javascript-docker"
tags = ["jupyter","docker","javascript"]
title = "Jupyter JavaScript Docker"
repoFullName = "pfeilbr/jupyter-javascript-docker"
repoHTMLURL = "https://github.com/pfeilbr/jupyter-javascript-docker"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/jupyter-javascript-docker" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/jupyter-javascript-docker</a>
</div>


docker image for running [jupyter notebooks](https://jupyter.org/) with javascript code via the [IJavascript](https://github.com/n-riesco/ijavascript)  javascript kernel

**Build and Run**

```sh
# build and run (server)
docker build -t pfeilbr/jupyter-javascript . && docker run -v $PWD:/tmp/working -w=/tmp/working -p 8888:8888 --rm pfeilbr/jupyter-javascript

# build and run (interactive bash session)
docker build -t pfeilbr/jupyter-javascript . && docker run -v $PWD:/tmp/working -w=/tmp/working -p 8888:8888 --rm -it pfeilbr/jupyter-javascript bash -i

# remove `--rm` to persist changes made to the image

# push to docker hub
docker push pfeilbr/jupyter-javascript
```

**Example Package Usage**

[`example-package/examples.ipynb`](https://github.com/pfeilbr/jupyter-javascript-docker/blob/master/example-package/examples.ipynb)

**Notebook Screenshot(s)**

![](https://www.evernote.com/l/AAFEfmgSpR9EoJgKwwGedCsiqu4nCeQBPUoB/image.png)
