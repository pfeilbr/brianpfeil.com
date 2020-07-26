+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2017-09-09
description = ""
summary = "learning Jupyter"
draft = false
slug = "jupyter"
tags = ["jupyter","github",]
title = "Jupyter"
repoFullName = "pfeilbr/jupyter-playground"
repoHTMLURL = "https://github.com/pfeilbr/jupyter-playground"
truncated = true

+++


learn and experiment with [jupyter](http://jupyter.org/) notebooks

## [jupyterlab](https://github.com/jupyterlab/jupyterlab) (early preview as of this - 2017-09-09)

```sh
# install
conda install -c conda-forge jupyterlab

# run
jupyter lab

# notebook server now running @ http://localhost:8888
```

**screenshots**

![](https://www.evernote.com/l/AAGQllPjiA5Oe4vmdCFYv5OR0i59KLGupXoB/image.png)

![](https://www.evernote.com/l/AAE03lHOtuRDX4Flxj33p8Lrxjab350GANAB/image.png)

## jupyter notebook (classic UI)

```sh
# run
jupyter notebook
```

**screenshots**

![](https://www.evernote.com/l/AAESPeQa1u1PFa73VSOrmP2wRw4uJ8CARi4B/image.png)

## [jupyter qtconsole](https://qtconsole.readthedocs.io/en/stable/index.html)

> The Qt console is a very lightweight application that largely feels like a terminal, but provides a number of enhancements only possible in a GUI, such as inline figures, proper multi-line editing with syntax highlighting, graphical calltips, and much more. The Qt console can use any Jupyter kernel.

```sh
# install
conda install qtconsole
conda install pyqt

# run
jupyter qtconsole
```

**screenshots**

![](https://www.evernote.com/l/AAG_J_WaXklPBJxd_gS1-8JvTLMnu0Z6RcMB/image.png)

## IJavascript Kernel

IJavascript is a Javascript kernel (node.js) for the Jupyter notebook

```sh
# install
npm install -g ijavascript

# registers the IJavascript kernel with Jupyter
ijsinstall
```

**screenshots**

![](https://www.evernote.com/l/AAFzQ-qoH-dIc5661TFz2RRk2hIekySeDs0B/image.png)

![](https://www.evernote.com/l/AAG5nUlw2dBIgqnqNfJyuJ6Gc7DZoo-EbaUB/image.png)
