+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2022-01-07
description = ""
summary = " "
draft = false
slug = "aws-assume-role-using-custom-oidc-provider"
tags = ["aws","iam","oidc",]
title = "AWS Assume Role Using Custom OIDC Provider"
repoFullName = "pfeilbr/aws-assume-role-using-custom-oidc-provider-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-assume-role-using-custom-oidc-provider-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-assume-role-using-custom-oidc-provider-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-assume-role-using-custom-oidc-provider-playground</a>
</div>


Goal is to [assume an AWS role](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) via a custom OIDC provider.  It is based on a trust relationship between the OIDC provider and AWS account.  Allows assume role without credentials.

## Jenkins OIDC Provider

Enable assume Role directly from Jenkin using a Jenkins OIDC provider in the target AWS account (no IAM User credentials / access key/secret).

provide similar service for Jenkins as the following for gh actions [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials)
see also [AWS federation comes to GitHub Actions](https://awsteele.com/blog/2021/09/15/aws-federation-comes-to-github-actions.html)


1. create jenkins OIDC provider server.  see [pfeilbr/aws-custom-nodejs-oidc-provider-server-on-heroku](https://github.com/pfeilbr/aws-custom-nodejs-oidc-provider-server-on-heroku)
1. create a jenkins OIDC provider in AWS account (`AWS::IAM::OIDCProvider`)
1. jenkins job at start creates token (guid) and persists it - e.g. `JENKINS_ID_TOKEN_REQUEST_TOKEN` (github actions is called `ACTIONS_ID_TOKEN_REQUEST_TOKEN`)
   * e.g could be persisted to service at https://vstoken.jenkins.merck.com (https://vstoken.jenkins.merck.com/.well-known/openid-configuration)
1. jenkins job issues assume role passing in `JENKINS_ID_TOKEN_REQUEST_TOKEN` - see <https://github.com/aws-actions/configure-aws-credentials/blob/master/index.js#L93>

* <https://github.com/aws-actions/configure-aws-credentials/blob/master/index.js>
* <https://github.com/aws-actions/configure-aws-credentials/blob/master/index.js#L268> - where `ACTIONS_ID_TOKEN_REQUEST_TOKEN` is used
* [Secure Communication Between Actions and App](https://github.community/t/secure-communication-between-actions-and-app/201330)

```yaml
  JenkinsOidc:
    Type: AWS::IAM::OIDCProvider
    Condition: CreateOIDCProvider
    Properties:
      Url: https://vstoken.jenkins.merck.com
      ClientIdList: 
        - sts.amazonaws.com
      ThumbprintList:
        - a031c46782e6e6c662c2c87c76da9aa62ccabd8e
```

* "sub" (Subject) Claim The "sub" (subject) claim identifies the principal that is the subject of the JWT
  * e.g. for github actions it's `repo:aidansteele/aws-federation-github-actions:ref:refs/heads/main`
* "aud" (Audience) Claim The "aud" (audience) claim identifies the recipients that the JWT is intended for.
  * e.g. for github actions it's the repo url like `https://github.com/aidansteele`

## Resources

* [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials)
* [AWS federation comes to GitHub Actions](https://awsteele.com/blog/2021/09/15/aws-federation-comes-to-github-actions.html)
* [pfeilbr/aws-custom-nodejs-oidc-provider-server-on-heroku](https://github.com/pfeilbr/aws-custom-nodejs-oidc-provider-server-on-heroku)
* [Secure Communication Between Actions and App](https://github.community/t/secure-communication-between-actions-and-app/201330)
* [Deploy on AWS using Bitbucket Pipelines OpenID Connect](https://support.atlassian.com/bitbucket-cloud/docs/deploy-on-aws-using-bitbucket-pipelines-openid-connect/)
* [Bitbucket / Ben Kehoe Twitter Thread](https://twitter.com/revbingo/status/1485319472395268104?s=21)



