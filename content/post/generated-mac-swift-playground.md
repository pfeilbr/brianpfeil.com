+++
author = "Brian Pfeil"
categories = ["Swift", "playground"]
date = 2014-06-05
description = ""
summary = "learning Mac Swift"
draft = false
slug = "mac-swift"
tags = ["mac","github",]
title = "Mac Swift"
repoFullName = "pfeilbr/mac-swift-playground"
repoHTMLURL = "https://github.com/pfeilbr/mac-swift-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/mac-swift-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/mac-swift-playground</a>
-->


<div style="clear: both"></div>

## [Swift](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language) Playground

Swift playground for exploring the [swift programming language](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language)

## Playground Specific Functions

There are a set of functions that enable the code you write to interact with the plaground UI.  For example, you can display a UIView live.  The ```XCPlayground``` module provides these functions

```
XCPSetExecutionShouldContinueIndefinitely(continueIndefinitely:Bool)
```

Allows async code to run.  For example, ```dispatch_*``` calls and networking.

```
XCPCaptureValue(identifier: String, value:AnyObject)
```

Displays the value in the view pane with the identifier as the title

```
XCPShowView(identifier: String, view: NSView)
```

Display the provided view in the view pane with the identifier as the title


