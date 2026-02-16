+++
author = "Brian Pfeil"
categories = ["Dockerfile", "playground"]
date = 2022-05-22
description = ""
summary = " "
draft = false
slug = "aws-parallel-cluster"
tags = ["aws","hpc"]
title = "AWS Parallel Cluster"
repoFullName = "pfeilbr/aws-parallel-cluster-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-parallel-cluster-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-parallel-cluster-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-parallel-cluster-playground</a>
</div>


learn [AWS ParallelCluster](https://docs.aws.amazon.com/parallelcluster/latest/ug/what-is-aws-parallelcluster.html).  formerly CfnCluster (“cloud formation cluster”)

> framework that deploys and maintains high performance computing clusters on Amazon Web Services (AWS). Developed by AWS, CfnCluster facilitates both quick start proof of concepts (POCs) and production deployments. CfnCluster supports many different types of clustered applications and can easily be extended to support different frameworks.

## Notes

*  distributed as a Python package and is installed using the Python pip package manager.
* supports [Slurm](https://docs.aws.amazon.com/parallelcluster/latest/ug/slurm-workload-manager-v3.html) and [AWS Batch](https://docs.aws.amazon.com/parallelcluster/latest/ug/awsbatchcli-v3.html) schedulers
* generates CloudFormation to create the cluster resources
    * CDK is used to generate templates
* head node - responsible for submitting and scheduling jobs
* compute node(s) - runs jobs
* AMI for head and compute nodes (ec2 instances)
    * AMI Name: aws-parallelcluster-3.1.4-amzn2-hvm-x86_64-202205121006 2022-05-12T10-09-45.467Z
    * AMI Locaiton: amazon/aws-parallelcluster-3.1.4-amzn2-hvm-x86_64-202205121006 2022-05-12T10-09-45.467Z
* When you use the awsbatch scheduler, the AWS ParallelCluster CLI commands for AWS Batch are automatically installed in the AWS ParallelCluster head node
    * [CLI commands for AWS Batch](https://docs.aws.amazon.com/parallelcluster/latest/ug/awsbatchcli-v3.html) - e.g. awsbsub, awsbqueues, etc.

## Demo

install, configure cluster, create cluster, submit job to cluster

```sh
python3 -m pip install "aws-parallelcluster" --upgrade --user

# verify install
pcluster version

# configure cluster. prompts for scheduler type, region, etc.
# when done `hello-world.yaml` is created
# and it creates the networking / vpc resources via a cfn stack (e.g. `parallelclusternetworking-pubpriv-20220522231401` stack)
# <https://github.com/aws/aws-parallelcluster/tree/release-3.0/cli/tests/pcluster/example_configs> for example
# cluster configuration files
# <https://docs.aws.amazon.com/parallelcluster/latest/ug/cluster-configuration-file-v3.html> - configuration files spec
pcluster configure --config hello-world.yaml

# create / provision the cluster (the networking/vpc resources already exist from previous `configure` command)
pcluster create-cluster --cluster-name hello-world --cluster-configuration hello-world.yaml

# login to cluster head node
pcluster ssh --cluster-name hello-world -i /path/to/keyfile.pem

# run the command sinfo to verify that your compute nodes are set up and configured.
sinfo

# create job to run (hello-job.sh)
cat << EOF > hello-job.sh
#!/bin/bash
sleep 30
echo "Hello World from $(hostname)"
EOF

# submit job
# this will create and ec2 compute instance on the fly
sbatch hello-job.sh

# view job in job queue
squeue

# once no job in queue a `.out` file will be created with results (STDOUT)
cat slurm-1.out

# clean up

# delete cluster compute nodes (this doesn't delete cluster head node)
pcluster delete-cluster-instances --cluster-name hello-world

# delete the cluster itself
# this terminates the head node and delete the cfn stack used to create the cluster
pcluster delete-cluster --cluster-name hello-world
```

## Screenshots

### EC2 instances

![](https://raw.githubusercontent.com/pfeilbr/aws-parallel-cluster-playground/main/ec2-instances.png)

## Resources

- [AWS ParallelCluster](https://docs.aws.amazon.com/parallelcluster/latest/ug/what-is-aws-parallelcluster.html)
- [aws/aws-parallelcluster](https://github.com/aws/aws-parallelcluster)
- [cfncluster.readthedocs.io](https://cfncluster.readthedocs.io/en/latest/)
- [AWS services used by AWS ParallelCluster](https://docs.aws.amazon.com/parallelcluster/latest/ug/aws-services-v3.html)
- [AWS Services used in CfnCluster](https://cfncluster.readthedocs.io/en/latest/aws_services.html#aws-services)
- [Running your first job on AWS ParallelCluster](https://docs.aws.amazon.com/parallelcluster/latest/ug/tutorials-running-your-first-job-on-version-3.html)
- [Cluster configuration file](https://docs.aws.amazon.com/parallelcluster/latest/ug/cluster-configuration-file-v3.html)
- [aws-parallelcluster/cli/tests/pcluster/example_configs/](https://github.com/aws/aws-parallelcluster/tree/release-3.0/cli/tests/pcluster/example_configs) - example cluster configuration files
- [AWS ParallelCluster CLI commands](https://docs.aws.amazon.com/parallelcluster/latest/ug/commands-v3.html)
- [Slurm Workload Manager - Documentation](https://slurm.schedmd.com/documentation.html)
