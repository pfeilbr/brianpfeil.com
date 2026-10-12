+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2019-09-26
description = ""
summary = " "
draft = false
slug = "aws-cognito-developer-authenticated-identities"
tags = ["aws","cognito",]
title = "AWS Cognito Developer Authenticated Identities"
repoFullName = "pfeilbr/aws-cognito-developer-authenticated-identities-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-cognito-developer-authenticated-identities-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-cognito-developer-authenticated-identities-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-cognito-developer-authenticated-identities-playground</a>
</div>


learn [Developer Authenticated Identities (Identity Pools)](https://docs.aws.amazon.com/cognito/latest/developerguide/developer-authenticated-identities.html)

> With developer authenticated identities, you can register and authenticate users via your own existing authentication process, while still using Amazon Cognito to synchronize user data and access AWS resources.

## Example using AWS CLI

1. Add custom authentication provider (`DEVELOPER_PROVIDER_NAME`) to your identity pool via "Edit identity pool" UI

    ![](https://www.evernote.com/l/AAF_NlVpnfROCK-Jim33jq2iewvgWWp6LW8B/image.png)

1. setup shell variables

    ```sh
    IDENTITY_POOL_ID="us-east-1:335c1f44-87c9-4bbd-a314-93b47d91fadd"
    DEVELOPER_PROVIDER_NAME=com.example.app01

    # this is YOUR applications userid
    DEVELOPER_PROVIDER_USERID=003
    ```

1. create identity

    ```sh
    aws cognito-identity get-open-id-token-for-developer-identity --identity-pool-id $IDENTITY_POOL_ID --logins "$DEVELOPER_PROVIDER_NAME=$DEVELOPER_PROVIDER_USERID"
    ```

    example output
    ```json
    {
        "Token": "<JWT redacted>",
        "IdentityId": "us-east-1:aecb58a8-2776-4431-978c-d6395e1b5379"
    }
    ```

1. get token

    ```sh
    aws cognito-identity get-open-id-token-for-developer-identity --identity-pool-id $IDENTITY_POOL_ID --identity-id  $IDENTITY_ID --logins "$DEVELOPER_PROVIDER_NAME=$DEVELOPER_PROVIDER_USERID"
    ```

    example output
    ```json
    {
        "Token": "<JWT redacted>",
        "IdentityId": "us-east-1:aecb58a8-2776-4431-978c-d6395e1b5379"
    }    
    ```

1. get credentials

    ```sh
    aws cognito-identity get-credentials-for-identity --identity-id $IDENTITY_ID --logins "cognito-identity.amazonaws.com=$TOKEN"
    ```

    example output

    ```json
    {
        "Credentials": {
            "SecretKey": "REDACTED",
            "SessionToken": "REDACTED",
            "Expiration": 1569527701.0,
            "AccessKeyId": "REDACTED"
        },
        "IdentityId": "us-east-1:aecb58a8-2776-4431-978c-d6395e1b5379"
    }
    ```

    > NOTE: `--logins cognito-identity.amazonaws.com=`.  See <https://aws.amazon.com/blogs/mobile/understanding-amazon-cognito-authentication-part-4-enhanced-flow/>

    > When using an Amazon Cognito token with GetCredentialsForIdentity, you use the key cognito-identity.amazonaws.com in the logins parameter. 

1. You can now use `AccessKeyId`, `SecretKey`, and `SessionToken` to access AWS resources.

### Resources

* [Developer Authenticated Identities (Identity Pools)](https://docs.aws.amazon.com/cognito/latest/developerguide/developer-authenticated-identities.html)
* [Understanding Amazon Cognito Authentication Part 2: Developer Authenticated Identities](https://aws.amazon.com/blogs/mobile/understanding-amazon-cognito-authentication-part-2-developer-authenticated-identities/)


