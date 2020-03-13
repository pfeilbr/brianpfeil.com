+++
author = "Brian Pfeil"
categories = ["golang", "atom"]
date = 2015-12-02T13:54:15Z
description = ""
draft = false
slug = "atom-golang-support"
tags = ["golang", "atom"]
title = "Atom Golang Setup"

+++


I've recently switched to [Atom](https://atom.io) from [Sublime Text](http://www.sublimetext.com/) for web development.  The transition was relatively painless since many of the keyboard shortcuts and capabilities are the same in.  I really enjoy usig Atom and want to have that same experience with programming in [Go](https://golang.org/).  This documents my Go setup in Atom.

### Install and Configuration Steps

1. Install [go-plus](https://github.com/joefitzgerald/go-plus)
2. Set the go-plus `GOPATH` setting

	![](http://static-content-01.s3-website-us-east-1.amazonaws.com//Settings_-__Users_pfeilbr_go_src_github_com_pfeilbr_go-gorilla-mux-playground_-_Atom_1C0E5214.png)

	> Ideally the Atom application process should have `GOPATH` in its `ENV` and you shouldn't have to set this.

3. Install atom [build](https://atom.io/packages/build)
4. Set build `Panel Visibility` setting to `Keep Visible`

	![](http://static-content-01.s3-website-us-east-1.amazonaws.com//Screenshot_12_1_15__5_12_PM_1C0E52F8.png)

4. Add `.atom-build.json` to root of your project directory

```json
{
  "cmd": "$GOROOT/bin/go run {FILE_ACTIVE}",
  "shell": true,
  "env": {
    "GOROOT": "/usr/local/go",
    "GOPATH": "/Users/pfeilbr/go"
  }
}
```

![](http://static-content-01.s3-website-us-east-1.amazonaws.com//Screenshot_12_1_15__5_05_PM_1C0E513F.png)


### Keyboard Shortcuts

* `cmd-alt-b` - run current file
* `cmd-alt-g` - goto definition
* `ctrl-space` - code completion
