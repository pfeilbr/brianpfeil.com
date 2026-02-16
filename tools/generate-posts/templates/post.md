+++
author = "Brian Pfeil"
categories = ["{{ .Repo.GetLanguage }}", "playground"]
date = {{ .Repo.GetCreatedAt.Format "2006-01-02" }}
description = ""
summary = " "
draft = false
slug = "{{ .Slug }}"
tags = [{{range $i, $val := .Tags}}{{if $i}},{{end}}"{{$val}}"{{end}}]
title = "{{ .Title }}"
repoFullName = "{{ .Repo.GetFullName }}"
repoHTMLURL = "{{ .Repo.GetHTMLURL }}"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="{{ .Repo.GetHTMLURL }}" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;{{ .Repo.GetFullName }}</a>
</div>

{{ .MarkdownBody }}
