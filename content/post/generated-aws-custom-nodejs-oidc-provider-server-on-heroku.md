+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-07-31
description = ""
summary = " "
draft = false
slug = "aws-custom-node.js-oidc-provider-server-on-heroku"
tags = ["aws","nodejs","heroku","iam","oidc"]
title = "AWS Custom Node.js OIDC Provider Server on Heroku"
repoFullName = "pfeilbr/aws-custom-nodejs-oidc-provider-server-on-heroku"
repoHTMLURL = "https://github.com/pfeilbr/aws-custom-nodejs-oidc-provider-server-on-heroku"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-custom-nodejs-oidc-provider-server-on-heroku" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-custom-nodejs-oidc-provider-server-on-heroku</a>
</div>


example of a custom nodejs OIDC provider server running on heroku for use as a custom AWS OIDC identity provider.

* Uses the [node-oidc-provider](https://github.com/panva/node-oidc-provider) npm package.
* based on [node-oidc-provider-example/00-oidc-minimal/README.md](https://github.com/panva/node-oidc-provider-example/blob/master/00-oidc-minimal/README.md)


**Demo Overview**

1. User logs into a web app with any username and password
1. It returns an `id_token` (JWT) in the URL
1. The `id_token` is used in the AWS STS `assume-role-with-web-identity` call to get temporary credentials which can be used to access AWS services

### Deploy OIDC Server to Heroku

1. If git not initialized, init it
    ```sh
    git init
    ```

1. Create a heroku app  
    ```bash
    heroku create --addons securekey,heroku-redis:hobby-dev
    ```
    ![](https://www.evernote.com/l/AAHlRnEvKuhCaIRToznvD5N1UYxRmu9rDC0B/image.png)

1. Enable (experimental) runtime-dyno-metadata
    ```bash
    heroku labs:enable runtime-dyno-metadata
    ```
    ![](https://www.evernote.com/l/AAEe2gZGiLxITLq9aidUWnsiy1S-mXa5Ru0B/image.png)

1. Commit to your local repo  
    ```bash
    git add .
    git commit -a -m 'my initial commit'
    ```

1. Deploy to heroku  
    ```bash
    git push heroku master
    ```

1. see your openid-configuration
    ```bash
    heroku open '/.well-known/openid-configuration' # to see your openid-configuration
    ```
    ![](https://www.evernote.com/l/AAH9MlAdEdlDb7ZUxrEabpIANWYnZ4U-_CgB/image.png)

### Create OIDC Identity Provider in AWS Console

1. Visit [IAM | Identity providers](https://console.aws.amazon.com/iam/home?region=us-east-1#/providers)
1. Click `[Create Provider]` button
1. Enter
    ```sh
    Provider Type: "OpenID Connect"

    # base URL of server
    Provider URL: https://fast-atoll-98810.herokuapp.com
    
    # this should match `client_id` in `src/index.js`
    Audience: foo
    ```
    ![](https://www.evernote.com/l/AAGhRArxfixOfbF249EkftA2N-zAKrKH1i8B/image.png)

1. Click `[Next]`
    ![](https://www.evernote.com/l/AAEnle1U-idHR68ZFsEoOwZdWrUf57KriDAB/image.png)

1. Click `[Create]`
    ![](https://www.evernote.com/l/AAF0xujrLZtGlqN55u6qtI3h0yzk5fhD_E4B/image.png)

1. Visit [IAM | Roles](https://console.aws.amazon.com/iam/home?region=us-east-1#/roles) and click `[Create Role]` button

1. Select `Web Identity` and select the `Identity provider` and `Audience` you specified in previous steps.
    ![](https://www.evernote.com/l/AAH_jVgAkeJO5L2K4uA-rJIIeC3NC3FiI0UB/image.png)

1. Specify permissions
    ![](https://www.evernote.com/l/AAEis9B1oNZLAqxl-RNwG1Q_UVdbLP0lPlkB/image.png)

1. Give the role a name (e.g. `custom-oidc-role-example-01`)
    note role ARN.  e.g. `arn:aws:iam::529276214230:role/custom-oidc-role-example-01`
    ![](https://www.evernote.com/l/AAEis9B1oNZLAqxl-RNwG1Q_UVdbLP0lPlkB/image.png)

    ![](https://www.evernote.com/l/AAEI-_h4KrhEDKAojtRY38L_EJ5CSh1Ww1IB/image.png)

    ![](https://www.evernote.com/l/AAHrxTgJ6SlKrKHdAVWz8mx8mqU92pR75k8B/image.png)

### Login to Custom App and Get Temporary Security Credentials via [`assume-role-with-web-identity`](https://docs.aws.amazon.com/cli/latest/reference/sts/assume-role-with-web-identity.html)

1. Visit login URL and enter **any** username and password
    ```sh
    heroku open '/auth?client_id=foo&response_type=id_token&scope=openid&nonce=123'
    ```
    ![](https://www.evernote.com/l/AAEHWD2T2gJMLpIgAe4QGlAP9XsfAfFmTm0B/image.png)

1. Click `[Sign-in]` button
    ![](https://www.evernote.com/l/AAFdkdeiejxGXKZyImsDLnbClCKoCaTA2NoB/image.png)

1. Click `[Continue]` button
    > note the `id_token` in the URL.  This is the JWT Token we pass to `assume-role-with-web-identity`
    ![](https://www.evernote.com/l/AAGOfSagDqVJ6qQVXelbN31Nwd4kO0MOQdgB/image.png)

1. Call `assume-role-with-web-identity` with role-arn, role-session-name (can be anything), and web-identity-token (`id_token` from step above)
    ```sh
    aws sts assume-role-with-web-identity \
    --role-arn 'arn:aws:iam::529276214230:role/custom-oidc-role-example-01' \
    --role-session-name 'user01' \
    --web-identity-token '<id_token>'
    ```
    ![](https://www.evernote.com/l/AAHLkadFw_JCn4GeTFuA3hnPNfDLWLRyOEEB/image.png)

1. You can now use `AccessKeyId`, `SecretAccessKey`, and `SessionToken` in the response to access AWS services with the permissions provided by the `custom-oidc-role-example-01` role

1. As an example, see [Creating a URL that Enables Federated Users to Access the AWS Management Console (Custom Federation Broker)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-custom-url.html)

1. To programmatically create URL, see [Example Code Using Python](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-custom-url.html#STSConsoleLink_programPython)


