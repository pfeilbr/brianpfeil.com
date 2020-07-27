+++
author = "Brian Pfeil"
categories = ["Jupyter Notebook", "playground"]
date = 2017-09-24
description = ""
summary = "learning Deep And Machine Learning"
draft = false
slug = "deep-and-machine-learning"
tags = ["github",]
title = "Deep And Machine Learning"
repoFullName = "pfeilbr/deep-and-machine-learning-playground"
repoHTMLURL = "https://github.com/pfeilbr/deep-and-machine-learning-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/deep-and-machine-learning-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/deep-and-machine-learning-playground</a>


docker image + jupyter notebook UI for learning and experimenting with deep and machine learning.

docker image based on <https://github.com/floydhub/dl-docker> - All-in-one Docker image for Deep Learning

docker hub image @ <https://hub.docker.com/r/pfeilbr/deep-and-machine-learning/>

## Running

```sh
docker run -it -p 8888:8888 -p 6006:6006 -v /Users/brianpfeil/projects/deep-and-machine-learning-playground:/root/sharedfolder pfeilbr/deep-and-machine-learning:v2 bash

# this lands you at a bash prompt in the container
# start jupyter
jupyter notebook

# open browser to http://localhost:8888/
```

## To save container changes

for example to save software installs (e.g. apache mxnet was added to image)

```sh
# list images to find commit id
docker ps -a

# commit changes
# docker commit 5b4a6fb7117b pfeilbr/deep-and-machine-learning:TAG
# e.g. 
docker commit 5b4a6fb7117b pfeilbr/deep-and-machine-learning:v2

# push new image to docker hub
# docker push pfeilbr/deep-and-machine-learning:TAG
# e.g.
docker push pfeilbr/deep-and-machine-learning:v2
```



