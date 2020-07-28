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
    DEVELOPER_PROVIDER_NAME=com.brianpfeil.app01

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
        "Token": "eyJraWQiOiJ1cy1lYXN0LTExIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy1lYXN0LTE6YWVjYjU4YTgtMjc3Ni00NDMxLTk3OGMtZDYzOTVlMWI1Mzc5IiwiYXVkIjoidXMtZWFzdC0xOjMzNWMxZjQ0LTg3YzktNGJiZC1hMzE0LTkzYjQ3ZDkxZmFkZCIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwiY29tLmJyaWFucGZlaWwuYXBwMDEiLCJjb20uYnJpYW5wZmVpbC5hcHAwMTp1cy1lYXN0LTE6MzM1YzFmNDQtODdjOS00YmJkLWEzMTQtOTNiNDdkOTFmYWRkOjAwMyJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImV4cCI6MTU2OTUyMzg3NSwiaWF0IjoxNTY5NTIyOTc1fQ.F6ST-AQWETHUAAR7JM-IU1ZIFLDEVL9ZBNM49WDOL_RXLLCYEY2KYUICHSGYLERD4WWLHWEJG-AOHFMMS0DUXT-UANA3BENUFFZWWSBAYVD0N2BHCLHZG7PURTRKRDN2XRFGDGQQ2PIMURMWAIPSB0ZCM-EXMSV-QAGOGKE5C2QR0P91BICL_LB1OQRTF9VXANPEMFFSAMZED776WHKR8ZMP7NTXZBMRE453QFW7VGVNKV3KJDTAKSRVZJS6YVW7BXY74_OQUJCFF9KWXJSMTEBNOIMHEFI3LJ25HSDDJ4LMLBGODD_ET4PPSUORIVLGW4UQ-7PJYHCAYTBDV0MXAQ",
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
        "Token": "eyJraWQiOiJ1cy1lYXN0LTExIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy1lYXN0LTE6YWVjYjU4YTgtMjc3Ni00NDMxLTk3OGMtZDYzOTVlMWI1Mzc5IiwiYXVkIjoidXMtZWFzdC0xOjMzNWMxZjQ0LTg3YzktNGJiZC1hMzE0LTkzYjQ3ZDkxZmFkZCIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwiY29tLmJyaWFucGZlaWwuYXBwMDEiLCJjb20uYnJpYW5wZmVpbC5hcHAwMTp1cy1lYXN0LTE6MzM1YzFmNDQtODdjOS00YmJkLWEzMTQtOTNiNDdkOTFmYWRkOjAwMyJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImV4cCI6MTU2OTUyNDg5OCwiaWF0IjoxNTY5NTIzOTk4fQ.S8JRKAALQZV0FT0GX6WDBE2EZUH2UPHIJLQ1AX9_PQBXLDM4V7UFFVUDXMHGHMZ2T4VMC6R2ILUJATYO05EIKB4HKWPEHSJWHAT8ZUQ9MRVEZ4KJFAY-7ER4LCGKN8MW-ZTZWQRPXUAYGP3RHQFYDV7FGJCJ3GE-MTTCBGXRAY_0H8NNOQE2F1WRO0KPE-Q-8GXF2P89WGFM9FAHZYOBV0FCZYOH8LCAZ7CKQJQ6FO8NYIAQDXDWFJM5-SLMPRYJLBIW88PBLO00ASOP5OGTHFD61JJCUUXFDRB6UTUGM-RUNILJRCTZB5_AB0FXS2YWAG2YZ3_JOFPWDLL-FNQ2UA",
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


