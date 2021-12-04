+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2017-08-31
description = ""
summary = " "
draft = false
slug = "aws-kms"
tags = ["aws","kms",]
title = "AWS KMS"
repoFullName = "pfeilbr/aws-kms-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-kms-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-kms-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-kms-playground</a>
</div>


learn how to use kms to encrypt and decrypt data

see [`index.js`](index.js)

## KMS Key Policies

* Key policies are the primary way to control access to AWS KMS keys. Every KMS key must have exactly one key policy. The statements in the key policy document determine who has permission to use the KMS key and how they can use it. 
* Every KMS key must have exactly one key policy
* Each key policy is effective only in the Region that hosts the KMS key.
* IAM policies by themselves are not sufficient to allow access to a KMS key, though you can use them in combination with a key policy.
* In a key policy, you use "*" for the resource, which effectively means "this KMS key." A key policy applies only to the KMS key it is attached to.

via [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)

The following is needed to grant access to a key via an IAM policy.  For example, the following would need to exist on the key policy.
Then you would need to grant access to the key via say a policy attached to a role.

> Allows the AWS account (root user) 111122223333 full access to the KMS key, and thus enables IAM policies in the account to allow access to the KMS key.

```json
    {
      "Sid": "Enable IAM policies",
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::111122223333:root"},
      "Action": "kms:*",
      "Resource": "*"
    },
```

## Resources

* [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)


