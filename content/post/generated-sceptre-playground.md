+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2021-11-06
description = ""
summary = " "
draft = false
slug = "sceptre"
tags = ["cloudformation","infrastructure-as-code"]
title = "Sceptre"
repoFullName = "pfeilbr/sceptre-playground"
repoHTMLURL = "https://github.com/pfeilbr/sceptre-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/sceptre-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/sceptre-playground</a>
</div>


learn [sceptre](https://sceptre.cloudreach.com/), a tool to drive cloudformation

* [StackGroup Config](https://sceptre.cloudreach.com/latest/docs/stack_group_config.html) - [`config/dev/config.yaml`](https://github.com/pfeilbr/sceptre-playground/blob/master/my-sceptre-project/config/dev/config.yaml) - project_code, region, profile, etc.
* [Stack Config](https://sceptre.cloudreach.com/latest/docs/stack_config.html) - [`config/dev/template.yaml`](https://github.com/pfeilbr/sceptre-playground/blob/master/my-sceptre-project/config/dev/template.yaml) - config for specific stack.  e.g. stack params, template_path, dependencies, hooks, etc.
* Stack - [`templates/template.yaml`](https://github.com/pfeilbr/sceptre-playground/blob/master/my-sceptre-project/templates/template.yaml)

## Demo

via [Get Started &mdash; Sceptre 2.6.3 documentation](https://sceptre.cloudreach.com/2.6.3/docs/get_started.html)

```sh
# install cli
pipx install sceptre

# create new project
sceptre new project my-sceptre-project

cd my-sceptre-project

# create stack
sceptre create dev/template.yaml

# show stack outputs
sceptre --ignore-dependencies list outputs dev/template.yaml

# update stack
sceptre update dev/template.yaml

# delete stack
sceptre delete dev/template.yaml
```

## Resources

* [sceptre](https://sceptre.cloudreach.com/)
* [GitHub - Sceptre/sceptre: Build better AWS infrastructure](https://github.com/Sceptre/sceptre)
* [Introduction to Sceptre: An AWS Cloudformation Orchestration Tool](https://engineering.carsguide.com.au/introduction-to-sceptre-an-aws-cloudformation-orchestration-tool-4b8453c0ae81)
