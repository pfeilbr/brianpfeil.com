+++
author = "Brian Pfeil"
categories = ["{{ .Repo.GetLanguage }}", "{{ .Category }}"]
date = {{ .Date }}
description = "{{ .Description }}"
summary = " "
draft = false
slug = "{{ .Slug }}"
tags = [{{range $i, $val := .Tags}}{{if $i}},{{end}}"{{$val}}"{{end}}]
title = "{{ .Title }}"
repoFullName = "{{ .Repo.GetFullName }}"
repoHTMLURL = "{{ .Repo.GetHTMLURL }}"
truncated = true
{{- if eq .Category "project" }}

# A finished project lives on its /projects/ page, which shows this README
# under "Under the hood" and redirects the old /post/ URL. So this file is
# never listed or rendered on its own.
[build]
  list = "never"
  render = "never"
{{- end }}

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="{{ .Repo.GetHTMLURL }}" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;{{ .Repo.GetFullName }}</a>
</div>

{{ .MarkdownBody }}
