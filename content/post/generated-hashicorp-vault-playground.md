+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2021-05-04
description = ""
summary = " "
draft = false
slug = "hashicorp-vault"
tags = ["secrets-management","security",]
title = "Hashicorp Vault"
repoFullName = "pfeilbr/hashicorp-vault-playground"
repoHTMLURL = "https://github.com/pfeilbr/hashicorp-vault-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/hashicorp-vault-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/hashicorp-vault-playground</a>
</div>


learn [HashiCorp Vault](https://www.vaultproject.io/)

## Notes

* [`iam` and `ec2` auth methods](https://www.vaultproject.io/docs/auth/aws)
* [`iam`](https://registry.terraform.io/modules/hashicorp/vault/aws/latest/examples/vault-iam-auth) uses [`sts:GetCallerIdentity`](http://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html) under the hood
    * vault server receives request with attributes to construct sigv4 and issues the request to AWS STS
    * AWS STS API endpoint is wide open / available to anyone.  No auth required to issue request to it.
* vault roles map/bind to aws roles - vault roles add additional capabilities (e.g. leases, finer grain policies, etc.).  new layer to manage


<img src="https://www.evernote.com/l/AAG3agZoWcFMHZGFnmwz_sexgSHK8PLUYiAB/image.png" alt="" width="75%" />

## Demo

```sh
# install macOS (single golang binary)
brew tap hashicorp/tap
brew install hashicorp/tap/vault


# start in-memory server
vault server -dev

# set env vars
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN="s.uObLGyypsT6LWnxNaKNurYaV" # ok to expose for demo. ephemeral for in-memoery dev

# confirm connectivity / env vars / server running
vault status

# put secret
vault kv put secret/hello foo=bar

# get secret (json output)
vault kv get -format=json secret/hello

# delete secret
vault kv delete secret/hello

# list secrets engines
vault secrets list -format=json

# enable aws secrets engine
vault secrets enable -path=aws aws

# make aws keys available to env
export AWS_ACCESS_KEY_ID=<aws_access_key_id>
export AWS_SECRET_ACCESS_KEY=<aws_secret_key>

# configure AWS secrets engine
vault write aws/config/root \
    access_key=$AWS_ACCESS_KEY_ID \
    secret_key=$AWS_SECRET_ACCESS_KEY \
    region=us-east-1

# create role
vault write aws/roles/my-role \
        credential_type=iam_user \
        policy_document=-<<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1426528957000",
      "Effect": "Allow",
      "Action": [
        "ec2:*"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
EOF

# generate access key pair for role
# creates an IAM user with the policy inlined.
# e.g. arn:aws:iam::529276214230:user/vault-root-my-role-1620146368-5005
vault read aws/creds/my-role


```

---

## Screenshots


### Example IAM User Created by Vault

<img src="https://www.evernote.com/l/AAFNNpCfW7xIsYWi7x6TTmY69U_ROWohxloB/image.png" alt="" width="50%" />

---

## Resources

* [Vault Tutorials - HashiCorp Learn](https://learn.hashicorp.com/vault)
* [Getting Started | Vault - HashiCorp Learn](https://learn.hashicorp.com/collections/vault/getting-started)
* [HTTP API: Libraries | Vault by HashiCorp](https://www.vaultproject.io/api/libraries)
* [AWS - Auth Methods | Vault by HashiCorp](https://www.vaultproject.io/docs/auth/aws)
* [hashicorp/vault-lambda-extension](https://github.com/hashicorp/vault-lambda-extension) - utilizes the AWS Lambda Extensions API to help your Lambda function read secrets from your Vault deployment
* [https://registry.terraform.io/modules/hashicorp/vault/aws/latest/examples/vault-iam-auth](https://registry.terraform.io/modules/hashicorp/vault/aws/latest/examples/vault-iam-auth)
* [Serverless lambda with vault — Avoiding committing your passwords](https://medium.com/@rondineli.gomes.araujo/serverless-lambda-with-vault-avoiding-commit-your-passwords-e15a2fa0b5a1)


