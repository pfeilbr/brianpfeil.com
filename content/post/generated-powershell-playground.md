+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2020-10-12
description = ""
summary = " "
draft = false
slug = "powershell"
tags = ["powershell"]
title = "PowerShell"
repoFullName = "pfeilbr/powershell-playground"
repoHTMLURL = "https://github.com/pfeilbr/powershell-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/powershell-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/powershell-playground</a>
</div>


```sh
# connects to Azure with an authenticated account for use with cmdlets from the
# Az PowerShell modules
Connect-AzAccount

Get-AzADUser -ObjectId "user@example.com"| fl
```

## Resources

* [Installing PowerShell on macOS](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-core-on-macos)
* [Azure PowerShell documentation](https://docs.microsoft.com/en-us/powershell/azure)
* [Yes you can! Use PowerShell in MacOS to connect to Microsoft Azure](http://techgenix.com/powershell-in-macos/)
* [Microsoft Graph PowerShell Preview - Now on PowerShell Gallery](https://developer.microsoft.com/en-us/microsoft-365/blogs/microsoft-graph-powershell-preview-now-on-powershell-gallery/)

## Scratch

```sh

```
