+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2020-10-01
description = ""
summary = " "
draft = false
slug = "s3-access-points"
tags = ["s3","aws",]
title = "S3 Access Points"
repoFullName = "pfeilbr/s3-access-points-playground"
repoHTMLURL = "https://github.com/pfeilbr/s3-access-points-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/s3-access-points-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/s3-access-points-playground</a>
</div>


learn [S3 Access Points](https://aws.amazon.com/s3/features/access-points/)

> Be sure to review [Access points restrictions and limitations](https://docs.aws.amazon.com/AmazonS3/latest/dev/access-points-restrictions-limitations.html) before considering for a use case.

## Feature Overview

* Access points are unique hostnames
* enforce distinct permissions and network controls for any request made through the access point.
* Customers with shared data sets scale access for hundreds of applications by creating individualized access points with names and permissions customized for each application.
* access point can be restricted to a VPC to firewall S3 data access within customers’ private networks
* AWS Service Control Policies can be used to ensure all access points are VPC restricted.
* no longer have to manage a single, complex bucket policy with hundreds of different permission rules that need to be written, read, tracked, and audited. With S3 Access Points, you can now create application-specific access points permitting access to shared data sets with policies tailored to the specific application.

## Example

### Policy

limit access to `partner-01` role

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllObjectActions",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::529276214230:role/partner-01"
            },
            "Action": "s3:*Object",
            "Resource": ["arn:aws:s3:us-east-1:529276214230:accesspoint/partner-01-read-write/object/*"]
        }
    ]
}
```

**Access Point Hostname**

<https://partner-01-read-write-529276214230.s3-accesspoint.us-east-1.amazonaws.com>

### Example Usage

```sh
# get `a.c` using `partner-01` role
aws --profile partner-01 s3api get-object --key a.c --bucket 'arn:aws:s3:us-east-1:529276214230:accesspoint/partner-01-read-write' -
```

## Resources

* [S3 | Access Points](https://aws.amazon.com/s3/features/access-points/)
* [Easily Manage Shared Data Sets with Amazon S3 Access Points](https://aws.amazon.com/blogs/aws/easily-manage-shared-data-sets-with-amazon-s3-access-points/)
* [Access points restrictions and limitations](https://docs.aws.amazon.com/AmazonS3/latest/dev/access-points-restrictions-limitations.html)
* [Amazon S3 Access Points - Tutorials Dojo](https://tutorialsdojo.com/amazon-s3-access-points/)

## Screenshots

**get via access point example**

![](https://www.evernote.com/l/AAEIrh66-vdOzK64ivOI8xfAt-faNQtoD7oB/image.png)

**access point details**

![](https://www.evernote.com/l/AAEnQBgUUfFEv4dIUyMwL-HP-8Hg1Wy9fB4B/image.png)

**access point policy**

![](https://www.evernote.com/l/AAFROvTnHs9FfqI5GuYJL3wzurnVtZMLHa0B/image.png)

**`partner-01` role** _(requires S3 read permissions)_

![](https://www.evernote.com/l/AAHGcyrA7vNGfrBQQy1AvkTFK0K8DzBVQt4B/image.png)

## Scratch

```sh
cd ~/tmp
aws s3 cp a.c s3://s3-access-points-playground/

# verify assume role works
aws --profile partner-01 sts get-caller-identity

aws --profile partner-01 s3api get-object --key a.c --bucket 'arn:aws:s3:us-east-1:529276214230:accesspoint/partner-01-read-write' -

aws --profile partner-01 sts get-caller-identity

```



