+++
author = "Brian Pfeil"
categories = ["Dockerfile", "playground"]
date = 2017-11-11
description = ""
summary = " "
draft = false
slug = "aws-ecs"
tags = ["aws","ecs",]
title = "AWS ECS"
repoFullName = "pfeilbr/aws-ecs-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-ecs-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-ecs-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-ecs-playground</a>
</div>


learn [AWS ECS](https://aws.amazon.com/documentation/ecs/)

## Examples

### [`ecs-fargate-load-balanced-http-service-example`](ecs-fargate-load-balanced-http-service-example/)

example ECS Fargate private (vpc only access) load balanced (internal ALB) http service (nginx)

### [`ecs-fargate-task-example`](ecs-fargate-task-example/)

example ECS Fargate nodejs task that is manually run

### [`ecs-cli-example`](ecs-cli-example/)

example using `ecs-cli` to serve simple docker compose nodejs web app

## Notes

- [Fargate Task CPU and memory](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html#fargate-tasks-size)
  - min cpu: 256 (.25 vCPU), max cpu: 4096 (4 vCPU)
  - min mem: 512 MiB, max mem: 30 GB
- [`AWS::ECS::TaskDefinition.ExecutionRoleArn`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-executionrolearn) - role that grants the Amazon ECS container agent permission to make AWS API calls on your behalf.  For example, permission to pull ECR images and create log streams.  See [Amazon ECS task execution IAM role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html).  The `arn:aws:iam::${AWS::AccountId}:role/ecsTaskExecutionRole` role is available by default.
- [`AWS::ECS::TaskDefinition.TaskRoleArn`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-taskrolearn) - role that grants containers in the task permission to call AWS APIs on your behalf.  e.g. access S3, secrets manager, etc.  See [IAM roles for tasks](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html)
- [`AWS::ECS::Service.Role`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-role) - no need to specify in typical use case.  *Amazon ECS uses the service-linked role named AWSServiceRoleForECS to enable Amazon ECS to call AWS APIs on your behalf.* see [Service-linked role for Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using-service-linked-roles.h)
- [`AWS::ECS::Service.NetworkConfiguration`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-service.html#cfn-ecs-service-networkconfiguration) - required for task definitions that use the awsvpc network mode to receive their own elastic network interface, and it is not supported for other network modes
- [`AWS::ECS::Service.NetworkConfiguration.AwsvpcConfiguration.AssignPublicIp`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html#cfn-ecs-service-awsvpcconfiguration-assignpublicip) - Whether the task's elastic network interface receives a public IP address. The default value is DISABLED. (DISABLED | ENABLED)


