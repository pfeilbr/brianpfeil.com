+++
author = "Brian Pfeil"
categories = ["Dockerfile", "playground"]
date = 2022-08-02
description = ""
summary = " "
draft = false
slug = "amazon-redshift-serverless"
tags = ["serverless","aws","db","redshift"]
title = "Amazon Redshift Serverless"
repoFullName = "pfeilbr/amazon-redshift-serverless-playground"
repoHTMLURL = "https://github.com/pfeilbr/amazon-redshift-serverless-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/amazon-redshift-serverless-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/amazon-redshift-serverless-playground</a>
</div>


learn [Amazon Redshift Serverless](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-serverless.html)

> Amazon Redshift Serverless makes it convenient for you to run and scale analytics without having to provision and manage data warehouse clusters.
> Amazon Redshift automatically provisions and scales data warehouse capacity to deliver fast performance for demanding and unpredictable workloads. You pay only for the capacity that you use.

---

## Concepts

- **Namespace** - collection of database objects and users. The storage-related namespace groups together schemas, tables, users, or AWS Key Management Service keys for encrypting data.
- **Workgroup** - a collection of compute resources. The compute-related workgroup groups together compute resources like RPUs, VPC subnet groups, and security groups.
  - Other resources that are grouped under workgroups include access and usage limits. 


---

## Demo

```sh
psql -h workgroup01.529276214230.us-east-1.redshift-serverless.amazonaws.com -d sample_data_dev -p 5439 -U uadmin

# create user
CREATE USER user01 with password 'Password01' createdb connection limit 30;

# redshift serverless costs per day in USD
select
  trunc(start_time) "Day",
  sum(compute_seconds)/60/60 * 0.375
from sys_serverless_usage
group by trunc(start_time)
order by 1

# login as `user01`
psql -h workgroup01.529276214230.us-east-1.redshift-serverless.amazonaws.com -d sample_data_dev -p 5439 -U user01

# list databases
\l

# use database
\c sample_data_dev

# run query
select * from tpcds.customer limit 10;
```

---

## Screenshots

Serverless Dashboard

![](https://www.evernote.com/l/AAHY-S8I96hAJquRTaAMHb0Ccwdnfez0DswB/image.png)

Namespace

![](https://www.evernote.com/l/AAG2ksR6WLlHGry3HOdVwaKbynPJMMqpQOYB/image.png)

Workgroup

![](https://www.evernote.com/l/AAHfsGYT4M1GgJ6uCpT-Gdwj6dsSy2Fv3a0B/image.png)

Workgroup Limits

![](https://www.evernote.com/l/AAFOtFmBDHRFA4wW4SDgJ6PhyyOKJC--cRMB/image.png)

Data backup

![](https://www.evernote.com/l/AAGmQk_lH3dLBqwPVfr93tjXePiSyIpPSVYB/image.png)

Snapshot

![](https://www.evernote.com/l/AAGf2PLKjqBJnL4z22AhKwcGnh5vToq6kG0B/image.png)

Recovery point

![](https://www.evernote.com/l/AAEHSBSKSYJCUb5agUI6Kxi4Q_HVOnGhvNEB/image.png)

---

## Resources

- [Amazon Redshift Serverless](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-serverless.html)
- [Amazon Redshift Serverless – Now Generally Available with New Capabilities](https://aws.amazon.com/blogs/aws/amazon-redshift-serverless-now-generally-available-with-new-capabilities/)

