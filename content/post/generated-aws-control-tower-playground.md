+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2019-10-17
description = ""
summary = " "
draft = false
slug = "aws-control-tower"
tags = ["aws",]
title = "AWS Control Tower"
repoFullName = "pfeilbr/aws-control-tower-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-control-tower-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-control-tower-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-control-tower-playground</a>
</div>


learn [AWS Control Tower](https://aws.amazon.com/controltower/)

> AWS Control Tower provides the easiest way to set up and govern a secure, compliant, multi-account AWS environment based on best practices established by working with thousands of enterprises. With AWS Control Tower, end users on your distributed teams can provision new AWS accounts quickly. Meanwhile your central cloud administrators will know that all accounts are aligned with centrally established, company-wide compliance policies.

---

## Notes

Control Tower is the composition of many AWS services

* [AWS SSO](https://docs.aws.amazon.com/en_pv/singlesignon/index.html) - integrated with Microsoft AD on-prem and cloud/azure
* [Organizations](https://docs.aws.amazon.com/en_pv/organizations/index.html)
    * [Service Control Policies](https://docs.aws.amazon.com/en_pv/organizations/latest/userguide/orgs_manage_policies_scp.html) - central control over the maximum available permissions for all accounts in your organization, allowing you to ensure your accounts stay within your organization’s access control guidelines
* Guardrails - two kinds of guardrails exist: preventive (block) and detective (after the fact notification of non-compliance)
    * implemented as [AWS Config](https://docs.aws.amazon.com/en_pv/config/index.html) - monitor for compliance
* [Service Catalog](https://docs.aws.amazon.com/servicecatalog/) - self-service provisioning of cloud products

## Resources

* [AWS Control Tower Documentation](https://docs.aws.amazon.com/en_pv/controltower/index.html)
* [AWS re:Inforce 2019: Using AWS Control Tower to Govern Multi-Account AWS Environments (GRC313-R)](https://www.youtube.com/watch?v=2t-VkWt0rKk) (video)
* [Using AWS Control Tower to govern multi-account AWS environments at scale - GRC313-R - AWS re:Inforce 2019](https://www.slideshare.net/AmazonWebServices/using-aws-control-tower-to-govern-multiaccount-aws-environments-at-scale-grc313r-aws-reinforce-2019)(slides)
* [AWS Control Tower is now generally available](https://aws.amazon.com/about-aws/whats-new/2019/06/aws-control-tower-is-now-generally-available/)


