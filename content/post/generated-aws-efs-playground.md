+++
author = "Brian Pfeil"
categories = ["Python", "playground"]
date = 2022-07-31
description = ""
summary = " "
draft = false
slug = "aws-efs"
tags = ["aws"]
title = "AWS EFS"
repoFullName = "pfeilbr/aws-efs-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-efs-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-efs-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-efs-playground</a>
</div>


learn [Amazon Elastic File System (EFS)](https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html)

## Notes

* the client mounting the EFS FS (e.g. ec2, lambda, etc.) must be in the same VPC and subnet of the `AWS::EFS::MountTarget`
* for EC2 - `ec2-user` uid=1000, gid=1000.  this can be used for `AWS::EFS::AccessPoint.PosixUser` and `AWS::EFS::AccessPoint.RootDirectory` properties
* for lambda - uid=1001, gid=1001

---
## Demo

```sh
# deploy
# note if `MyFunctionWithEfs` fails because efs mount point not created, re-run deploy and ensure
# `disable_rollback = true` in `samconfig.toml`
# note the outputs and use to populate the env vars below
sam deploy

export FILESYSTEM_ID="fs-09a044741cf632443"
export MOUNT_TARGET_DNS="${FILESYSTEM_ID}.efs.us-east-1.amazonaws.com"
export MOUNT_TARGET_IP="172.30.4.9"
export MOUNT_POINT="/home/ec2-user/efs-mount-point"
export ACCESS_POINT_ID="fsap-01514965758e980b3  "
export ACCESS_POINT_MOUNT_POINT="/home/ec2-user/efs-access-point-mount-point-01"
export ACCESS_POINT_ARN="arn:aws:elasticfilesystem:us-east-1:529276214230:access-point/fsap-01514965758e980b3"

# ssh into ec2 instance within the *same VPC and subnet* of EFS mount target(s)
ssh ec2-user@dev01.brianpfeil.com

# install EFS mount helper
sudo yum install amazon-efs-utils

# *** mount and use efs mount target example ***

# make mount dir
mkdir "${MOUNT_POINT}"

# mount with any of the following

# by efs dns hostname
sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport $MOUNT_TARGET_DNS:/ "${MOUNT_POINT}"

# by efs ip address
sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport $MOUNT_TARGET_IP:/  "${MOUNT_POINT}"

# by using `amazon-efs-utils` package
sudo mount -t efs "${FILESYSTEM_ID}" "${MOUNT_POINT}/"


cd "${MOUNT_POINT}"

# change perms so others can add files
sudo chmod go+rw .

# create file
echo hello > a.txt

# move to parent directory
cd ..

# unmount
sudo umount "${MOUNT_POINT}"

# re-mount
sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport $MOUNT_TARGET_DNS:/ "${MOUNT_POINT}"

# view files created
ls "${MOUNT_POINT}"

# *** Mounting a file system using an access point example ***
mkdir "${ACCESS_POINT_MOUNT_POINT}"
sudo mount -t efs -o tls,accesspoint=${ACCESS_POINT_ID} ${FILESYSTEM_ID}: "${ACCESS_POINT_MOUNT_POINT}"

cd "${ACCESS_POINT_MOUNT_POINT}"
echo hello > a.txt
cd ..
sudo umount "${ACCESS_POINT_MOUNT_POINT}"

# re-mount filesystem (not the access point.  this is the root)
sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport $MOUNT_TARGET_DNS:/ "${MOUNT_POINT}"

# list the file created within the access point (the /myefs directory)
ls "${MOUNT_POINT}/myefs"

# *** lambda mount and write to efs example ***

# trigger lambda which will write file to `/mnt/efs/a.txt` which maps to  `myefs-lambda/a.txt` in efs
curl https://gwx70rb0q1.execute-api.us-east-1.amazonaws.com/Prod/
# output: {"output": "/mnt/efs contents\n\n['a.txt']"}

# re-mount filesystem in ec2 (not the access point.  this is the root)
sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport $MOUNT_TARGET_DNS:/ "${MOUNT_POINT}"

# view contents of file written by lambda
cat efs-mount-point/myefs-lambda/a.txt 
# output: hello from lambda

# clean up
sam delete --no-prompts
```

## Resources

- [Amazon Elastic File System (EFS)](https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html)
