+++
author = "Brian Pfeil"
categories = ["Dockerfile", "playground"]
date = 2022-07-01
description = ""
summary = " "
draft = false
slug = "aws-alb-to-lambda"
tags = ["aws","lambda",]
title = "AWS ALB to Lambda"
repoFullName = "pfeilbr/aws-alb-to-lambda-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-alb-to-lambda-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-alb-to-lambda-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-alb-to-lambda-playground</a>
</div>


learn ALB to Lambda integration

## Notes

- AWS provided DNSName for the ALB is of the format `xxxxxxx.us-east-1.elb.amazonaws.com`
- the ALB DNSName does not provide SSL termination by default
- you cannot request a certificate for the ALB DNSName (`xxxxxxx.us-east-1.elb.amazonaws.com`) via ACM
- if you own the domain, you can request a certificate (e.g. `alb01.allthecloudbits.com`) via ACM and have it automatically validated via route 53 CNAME record (see [DomainValidationOptions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainvalidationoptions))
    > In order for a AWS::CertificateManager::Certificate to be provisioned and validated in CloudFormation automatically, the `DomainName` property needs to be identical to one of the `DomainName` property supplied in DomainValidationOptions, if the ValidationMethod is **DNS**. Failing to keep them like-for-like will result in failure to create the domain validation records in Route53.
- you can specify a single certificate for your `AWS::ElasticLoadBalancingV2::Listener` via the [`AWS::ElasticLoadBalancingV2::Listener Certificate`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificate.html) property.  If you need multipe certificates, use [`AWS::ElasticLoadBalancingV2::ListenerCertificate`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html)

## Demo

> based on [alexcasalboni/template.yml](https://gist.github.com/alexcasalboni/9f118ac10a59a5c4eb6bfd75d0a65773) - AWS ALB - AWS Lambda integration with CloudFormation (YAML)
> includes a custom domain name CNAME'd to the ALB hostname with ACM cert for https

lambda function code is inlined in [`template.yaml`](template.yaml)

```sh
# deploy stack
sam deploy

# check our ALB andpoint
curl http://aws-a-myLoa-MFYJ9QBS4CCL-673155384.us-east-1.elb.amazonaws.com

# output:
# <h1>Hello from Lambda via ALB</h1><pre><code>{
#   "requestContext": {
#     "elb": {
#       "targetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:529276214230:targetgroup/aws-a-myTar-1OF41QMSUR19N/c81f17d663a5ef3a"
#     }
#   },
#   "httpMethod": "GET",
#   "path": "/",
#   "queryStringParameters": {},
#   "headers": {
#     "accept": "*/*",
#     "host": "aws-a-myLoa-MFYJ9QBS4CCL-673155384.us-east-1.elb.amazonaws.com",
#     "user-agent": "curl/7.79.1",
#     "x-amzn-trace-id": "Root=1-62bf13a2-7ec6c217009df4474336906d",
#     "x-forwarded-for": "100.11.104.251",
#     "x-forwarded-port": "80",
#     "x-forwarded-proto": "http"
#   },
#   "body": "",
#   "isBase64Encoded": false
# }</code></pre>

# check path based listener (`/api/*`)
curl http://aws-a-myLoa-MFYJ9QBS4CCL-673155384.us-east-1.elb.amazonaws.com/api/hello

# output:
# <h1>Hello from Lambda via ALB</h1><pre><code>{
#   "requestContext": {
#     "elb": {
#       "targetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:529276214230:targetgroup/aws-a-myTar-1OF41QMSUR19N/c81f17d663a5ef3a"
#     }
#   },
#   "httpMethod": "GET",
#   "path": "/api/hello",
#   "queryStringParameters": {},
#   "headers": {
#     "accept": "*/*",
#     "host": "aws-a-myLoa-MFYJ9QBS4CCL-673155384.us-east-1.elb.amazonaws.com",
#     "user-agent": "curl/7.79.1",
#     "x-amzn-trace-id": "Root=1-62bf27ec-5b6861564ac9b30938dd1e67",
#     "x-forwarded-for": "100.11.104.251",
#     "x-forwarded-port": "80",
#     "x-forwarded-proto": "http"
#   },
#   "body": "",
#   "isBase64Encoded": false
# }</code></pre>       

# check our custom domain
curl http://alb01.allthecloudbits.com

# check our custom domain https endpoint
curl https://alb01.allthecloudbits.com


# clean up
sam delete --no-prompts
```

![](https://www.evernote.com/l/AAFKcNmrSp9LmromFVQwcH5E6g6vEBMCVfsB/image.png)

![](https://www.evernote.com/l/AAHZyI_kncBHdIAJSo7CUt2-cZkVikQ1vSwB/image.png)

## Resources

- [alexcasalboni/template.yml](https://gist.github.com/alexcasalboni/9f118ac10a59a5c4eb6bfd75d0a65773) - AWS ALB - AWS Lambda integration with CloudFormation (YAML)
- [Lambda functions as targets for Application Load Balancers](https://aws.amazon.com/blogs/networking-and-content-delivery/lambda-functions-as-targets-for-application-load-balancers/)
- [Application Load Balancer can now Invoke Lambda Functions to Serve HTTP(S) Requests](https://aws.amazon.com/about-aws/whats-new/2018/11/alb-can-now-invoke-lambda-functions-to-serve-https-requests/)
- [One Load Balancer to rule them all](https://blog.deleu.dev/one-load-balancer-to-rule-them-all/)
- [How do I associate multiple ACM SSL or TLS certificates with Application Load Balancer using CloudFormation?](https://aws.amazon.com/premiumsupport/knowledge-center/cloudformation-ssl-tls-certificates-alb/)
- [AWS::ElasticLoadBalancingV2::LoadBalancer](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html)
- [AWS::ElasticLoadBalancingV2::Listener](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html)
- [AWS::ElasticLoadBalancingV2::ListenerCertificate](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html)
- [AWS::ElasticLoadBalancingV2::ListenerRule](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html)
- [AWS::ElasticLoadBalancingV2::TargetGroup](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html)


