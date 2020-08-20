+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2020-08-18
description = ""
summary = " "
draft = false
slug = "graphviz"
tags = ["tools","diagram","architecture",]
title = "Graphviz"
repoFullName = "pfeilbr/graphviz-playground"
repoHTMLURL = "https://github.com/pfeilbr/graphviz-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/graphviz-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/graphviz-playground</a>
</div>


learn [Graphviz - Graph Visualization Software](https://graphviz.org/)

* [`example01.dot`](example01.dot)

### Developing

```sh
# vscode "Graphviz Interactive Preview" extension was not working with images
# use the following to create .png image on .dot file change
# open vscode in split view with .dot in one and .png in the other.
# .png view will refresh when the file is updated.
fswatch -o example01.dot | xargs -n1 -I{} dot -Tpng example01.dot -oexample01.png
```

---

## Screenshots

vscode example with ["Graphviz Interactive Preview"](https://marketplace.visualstudio.com/items?itemName=tintinweb.graphviz-interactive-preview)

![](https://www.evernote.com/l/AAFUwF0MxjZOepisRfe4x3PcKd3Xrb3fxRIB/image.png)

## Resources

* [Graphviz&#32;Interactive&#32;Preview&#32;-&#32;Visual&#32;Studio&#32;Marketplace](https://marketplace.visualstudio.com/items?itemName=tintinweb.graphviz-interactive-preview)
* [Create diagrams with code using Graphviz](https://ncona.com/2020/06/create-diagrams-with-code-using-graphviz/)


