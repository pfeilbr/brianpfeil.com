+++
author = "Brian Pfeil"
categories = ["HCL", "playground"]
date = 2019-11-05
description = ""
summary = " "
draft = false
slug = "terraform"
tags = ["infrastructure-as-code","aws",]
title = "Terraform"
repoFullName = "pfeilbr/terraform-playground"
repoHTMLURL = "https://github.com/pfeilbr/terraform-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/terraform-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/terraform-playground</a>
</div>


learn and experiment with [Terraform](https://www.terraform.io/)

followed Packer [GETTING STARTED](https://www.terraform.io/intro/getting-started/install.html) docs

---

* Execution Plans - describing what it will do and asks for your approval before making any infrastructure changes. This allows you to review changes before Terraform creates, updates, or destroys infrastructure.
* Resource Graph - Terraform builds a resource graph and creates or modifies non-dependent resources in parallel.

### Resources

* represent infrastructure objects
* each resource type is implemented by a provider, which is a plugin for Terraform that offers a collection of resource types
* Meta-Arguments
  * `depends_on`
  * `count` - creates that many instances of the resource or module
  * `for_each` - value is a map or a set of strings, Terraform will create one instance for each member of that map or set
  * [`provider`](https://www.terraform.io/docs/language/meta-arguments/resource-provider.html) - use to override tf default provider. e.g. you want to change the region for a given resource
  * `lifecycle`
  * `provisioner` and `connection`

#### Syntax

```
resource TYPE NAME {
    BODY
}
```

---

### Data Sources

---

## Terraform Language

* use hcl or json to declare
* Blocks - containers for other content and usually represent the configuration of some kind of object
* Arguments - assign a value to a name
* Expressions - represent a value, either literally or by referencing and combining other values

---

## State

- by default state is stored locally in `*.tfstate` file (the default backend)
- when multiple people or clients are collaborating on infra via tf, state can be stored in a remote backend
	- e.g. state for aws can be stored in S3 and a dynamodb table is used for locking when the state is shared amongst many people and/or systems
	```tf
	terraform {
	  backend "s3" {
	    # Replace this with your bucket name!
	    bucket         = "terraform-up-and-running-state"
	    key            = "global/s3/terraform.tfstate"
	    region         = "us-east-2"

	    # Replace this with your DynamoDB table name!
	    dynamodb_table = "terraform-up-and-running-locks"
	    encrypt        = true
	  }
	}
	```
- *Workspaces* - allow you to store your Terraform state in multiple, separate, named workspaces

## CLI

```sh
# plan
terraform plan

# apply
terraform apply -auto-approve

# validate
terraform validate

# show outputs
terraform output
```

## Resources

* [Terraform Language Documentation](https://www.terraform.io/docs/language/index.html)
* [Terraform | AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
* [Terraform Registry](https://registry.terraform.io/browse/providers)



