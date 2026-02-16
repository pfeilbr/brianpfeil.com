+++
author = "Brian Pfeil"
categories = ["Dockerfile", "playground"]
date = 2022-01-23
description = ""
summary = " "
draft = false
slug = "aws-rds"
tags = ["aws","rds"]
title = "AWS RDS"
repoFullName = "pfeilbr/aws-rds-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-rds-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-rds-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-rds-playground</a>
</div>


explore [AWS RDS](https://aws.amazon.com/rds/)

## Demo

see [`template.yaml`](https://github.com/pfeilbr/aws-rds-playground/blob/master/template.yaml)

```sh
# initial deploy with SAM
sam deploy --guided

# subsequent deploys with SAM (no prompt)
sam deploy
```

## Resources

* [Amazon Relational Database Service Documentation](https://docs.aws.amazon.com/rds/index.html)
