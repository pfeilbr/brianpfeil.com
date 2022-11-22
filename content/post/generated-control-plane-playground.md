+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2022-11-11
description = ""
summary = " "
draft = false
slug = "control-plane"
tags = []
title = "Control Plane"
repoFullName = "pfeilbr/control-plane-playground"
repoHTMLURL = "https://github.com/pfeilbr/control-plane-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/control-plane-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/control-plane-playground</a>
</div>


learn [Control Plane](https://controlplane.com/)

## General

- multi-cloud (aws, azure, gcp)
- costs - compute, memory and egress are passed along to customer
- move off of platfrom team.
- checking latency 10xs per sec
- health check - multi-cloud for everything.  resilient.
- dns is 2 major providers - rt 53, constellex
- graphana under the covers
- control plane can use oidc connect for aws identity ([Creating OpenID Connect (OIDC) identity providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html))
- reduced complexity for eng teams
- agent (ec2 instance) needs to run in vpc
  - creates a wiregaurd connection to hub.controlplane.com
  - agent can run on a local server
- secrets management is built in
- cli and tf provider (verified)

## Concepts

- Org - strictly isolated bounded context that encapsulates all the resources managed by Control Plane
- Global Virtual Cloud (GVC) - defines a set of cloud providers and their locations.
- Workloads - you specify a container image.  this is the unit of deployment.
- Policy - governs resource access within an org to a set of principals. It enables fine-grained authorization rules to define the minimum amount of permissions required when accessing resources of the platform.
- Principal Types
  - supports 4 principal types.
    - Users
    - Service Accounts
    - Groups
    - Identity
- Accessing Cloud Resources
- Erik - director of cust success

## IAM Roles

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CreateRoles",
      "Effect": "Allow",
      "Action": [
        "iam:CreatePolicy",
        "iam:UpdateAssumeRolePolicy",
        "iam:DetachRolePolicy",
        "iam:TagRole",
        "iam:UpdateRoleDescription",
        "iam:DeletePolicy",
        "iam:CreateRole",
        "iam:DeleteRole",
        "iam:AttachRolePolicy",
        "iam:UpdateRole",
        "iam:PutRolePolicy",
        "iam:TagPolicy"
      ],
      "Resource": "*"
    }
  ]
}
```

trust policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::957753459089:user/controlplane-driver",
          "arn:aws:iam::957753459089:role/controlplane-driver"
        ]
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "merck-dev-01"
        }
      }
    }
  ]
}
```

## Demo


```sh
# cli usage only for the deployment of resources


```

## Questions

- recommendation for secrets storage (api keys, db creds, etc.)
  - "secrets" concept 
- is there an iac solution for provisioning workload?  what is used for "repeatability"

## Resources

- [Control Plane](https://controlplane.com/)
- <https://docs.controlplane.com/>
- <https://registry.terraform.io/providers/controlplane-com/cpln/latest>


