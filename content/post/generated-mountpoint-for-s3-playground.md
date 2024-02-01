+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2024-02-01
description = ""
summary = " "
draft = false
slug = "mountpoint-for-s3"
tags = ["s3","aws",]
title = "Mountpoint for S3"
repoFullName = "pfeilbr/mountpoint-for-s3-playground"
repoHTMLURL = "https://github.com/pfeilbr/mountpoint-for-s3-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/mountpoint-for-s3-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/mountpoint-for-s3-playground</a>
</div>


learn [Mountpoint for Amazon S3](https://github.com/awslabs/mountpoint-s3)

- does not support of posix file system apis
  - supports create, read, and delete files

## demo

```sh
# install Mountpoint for Amazon S3 client

# for amzn linux, centos, redhat
wget https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm
sudo yum install -y ./mount-s3.rpm

# or for debian

wget https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.deb
sudo apt-get install -y ./mount-s3.deb

# set credentials for `mount-s3` client to use
export $(printf "AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s AWS_SESSION_TOKEN=%s" \
$(aws --profile "PROFILE_NAME" sts assume-role \
--role-arn arn:aws:iam::xxxxxxxxxx:role/s3-full-access \
--role-session-name MySessionName \
--query "Credentials.[AccessKeyId,SecretAccessKey,SessionToken]" \
--output text))

# show all options
mount-s3 --help

# mount with no delete
mount-s3 <bucket name>  ~/mnt/s3

# mount with delete
mount-s3 --allow-delete "com.brianpfeil.scratch01" ~/mnt/s3

# unmount
sudo umount ~/mnt/s3

# `--allow-delete` - the corresponding object is immediately deleted from your S3 bucket.
# `--read-only` - forbid all mutating actions on your S3 bucket

```

## resources

- <https://github.com/awslabs/mountpoint-s3>
- [Configuring Mountpoint for Amazon S3](https://github.com/awslabs/mountpoint-s3/blob/main/doc/CONFIGURATION.md)


