+++
title = "{{ replace (replace .Name "-" " ") (now.Format "2006 01 02 ") "" | title }}"
slug = "{{ .Name }}"
author = "Brian Pfeil"
date = "{{ now.Format "2006-01-02" }}"
lastmod = "{{ now.Format "2006-01-02" }}"
draft = true
categories = []
tags = []
summary = ""

+++