+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2017-05-21
description = ""
summary = "experimenting with AWS Cognito"
draft = false
slug = "aws-cognito"
tags = ["aws","cognito","github",]
title = "AWS Cognito"
repoFullName = "pfeilbr/aws-cognito-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-cognito-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/aws-cognito-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-cognito-playground</a>


**Table of Contents**

<!-- TOC -->

- [aws-cognito-playground](#aws-cognito-playground)
    - [Cognito | Using the Built-in Sign-up and Sign-in Webpages](#cognito--using-the-built-in-sign-up-and-sign-in-webpages)
        - [API Gateway | Use Amazon Cognito User Pools](#api-gateway--use-amazon-cognito-user-pools)
        - [Verify ID and Access Tokens](#verify-id-and-access-tokens)
        - [Auth0 SAML IdP](#auth0-saml-idp)
            - [Auth0 Config](#auth0-config)
            - [Cognito Config](#cognito-config)
        - [Salesforce as Identity Provider (sign into app with salesforce credentials)](#salesforce-as-identity-provider-sign-into-app-with-salesforce-credentials)

<!-- /TOC -->

---

- learn cognito using the [Amazon Cognito Identity SDK for JavaScript](https://github.com/aws/amazon-cognito-identity-js)
- see [Tutorial: Integrating User Pools for JavaScript Apps](http://docs.aws.amazon.com/cognito/latest/developerguide/tutorial-integrating-user-pools-javascript.html) from AWS docs.
- see [Live Coding with AWS: API Authentication with Amazon Cognito](https://www.youtube.com/watch?v=TowcW1aTDqE) youtube video for detailed walkthrough
- see [API Authentication with Amazon Cognito](https://gist.github.com/jfaerman/abc31d2fefca6701e87a9e3a9e885c18) gist for links to relevant resources and documentation
- see `authenticateIdentityPool()` method in <https://github.com/awslabs/aws-cognito-apigw-angular-auth/blob/master/src/app/aws.service.ts> for detailed example
- see post [Part 2: Building a Serverless Architecture with AWS](https://blog.rackspace.com/part-2-building-serverless-architecture-aws)

`index.js` - example signup, confirm, and authenticate with federated identity

> rename `.env.example` to `.env` and update with _your_ values

---

## Cognito | Using the Built-in Sign-up and Sign-in Webpages

**Example Login Pages**

response_type=code for the authentication code grant

<https://com-brianpfeil-test-01.auth.us-east-1.amazoncognito.com/login?response_type=code&client_id=5uol3m3jk3bqn39jrsjvhaooqp&redirect_uri=https%3A%2F%2Flocalhost>

<https://myapp-user-pool.auth.us-east-1.amazoncognito.com/login?response_type=code&client_id=1l4tbhvki3sb8jjpcu3depj4t6&redirect_uri=http%3A%2F%2Flocalhost%3A3000>

implicit code grant where response_type=token

<https://com-brianpfeil-test-01.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id=5uol3m3jk3bqn39jrsjvhaooqp&redirect_uri=https%3A%2F%2Flocalhost>

example return values to callback URL

```
id_token=eyJraWQiOiJ...
access_token=eyJraWQ...
expires_in=3600
token_type=Bearer
```

- `id_token` can be used for API gateway endpoint having cognito authorizer (http header: `Authorization: <id_token>`)
- `id_token` can be used to retrieve credentials from STS Web Identity Federation using the Amazon Cognito Identity service
  - see see <https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/CognitoIdentityCredentials.html>
- you can also manually [Decode and verify Amazon Cognito JWT tokens](https://github.com/awslabs/aws-support-tools/tree/master/Cognito/decode-verify-jwt)
  - https://cognito-idp.us-east-1.amazonaws.com/us-east-1_CvO5f15cV/.well-known/jwks.json

example callback URL

https://localhost/#id_token=eyJraWQiOiJlMXd2TlwvVG9ZaVBhXC91RmtlbGlsUDE0ZTkzbU12UU52a1Y1VDRlY0lLazg9IiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoibFpERjFSZmxEbXB4S1lOeHFZTzNIQSIsInN1YiI6IjRhY2JmZGZkLTExOGUtNDJhMi1hZTY0LTZjM2UzNjI3YmQ1OSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfQ3ZPNWYxNWNWIiwicGhvbmVfbnVtYmVyX3ZlcmlmaWVkIjp0cnVlLCJjb2duaXRvOnVzZXJuYW1lIjoicGZlaWxiciIsImF1ZCI6IjV1b2wzbTNqazNicW4zOWpyc2p2aGFvb3FwIiwiZXZlbnRfaWQiOiJiNDhmN2M2Zi04NDgxLTExZTgtYWMxZC02MTIwMzliOGJmY2UiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTUzMTI1NTMyNSwicGhvbmVfbnVtYmVyIjoiKzEyMTU4NzIyNzkxIiwiZXhwIjoxNTMxMjU4OTI1LCJpYXQiOjE1MzEyNTUzMjUsImVtYWlsIjoiYnJpYW4ucGZlaWxAZ21haWwuY29tIn0.fVScj-3EKuYswxPkX3VXHcc50JegnJ09VDQ5xENQYDkZGFHmtjh8p_VKdcvgXtNmym3X1UUkAgaiMl_DVkp0Qa48-d4QD06tER_Paw7osmuFtSKchpyiXeZLBwWZy76eTNfUuAx1B9_qjKLr1s3Pyr4cXCozbk1Xn-p7SUyTjH4_IXfaXHQdELCw2KpeI_O64hG1A523k8oC01iz_1xXOliLzUPsj28b1L-1kGOxkgprfhscJNgFxB0PjmUvbZdEzQedOQKThiKGc1aJUIL06HWfzDxMhQfI6nME3WmMJNP7J7Ub8L1wLrrbKsRqEB9ubyyNlnMtALXCyXvziZaYOQ&access_token=eyJraWQiOiJ2MmxaeDNwdFpFUjVEbk9OWGhaSEZoSlIra3VqVGFIbHN6V2YxVFwvU0VIbz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI0YWNiZmRmZC0xMThlLTQyYTItYWU2NC02YzNlMzYyN2JkNTkiLCJldmVudF9pZCI6ImI0OGY3YzZmLTg0ODEtMTFlOC1hYzFkLTYxMjAzOWI4YmZjZSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1MzEyNTUzMjUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0N2TzVmMTVjViIsImV4cCI6MTUzMTI1ODkyNSwiaWF0IjoxNTMxMjU1MzI1LCJ2ZXJzaW9uIjoyLCJqdGkiOiIyZWRmNmFiZi1hNDVhLTQ2NDItYmM2NS05YjI3OWEyNzc3NzciLCJjbGllbnRfaWQiOiI1dW9sM20zamszYnFuMzlqcnNqdmhhb29xcCIsInVzZXJuYW1lIjoicGZlaWxiciJ9.T7oBdRLZXPIdmc8hRcg2xsDoJO-izBvg6nB-htxdYwdTD11WPXrcj9-IcTpsICiBAeOchUnXGzL5nSSG9bXhsXgjGZS6NmnOvccGwyvShgiKWl4Gw6sD_hau4eIbfFc67WL3qwE74sHU3b02EZGpc-Uco9fPj3ospMNAv9-ZnPw_1Dc7-N2o6_n9D_xtHLFdvwe_5OlOlKnEPlLKLg5vLJ2kB-m0YXLBzFZqk1M9yDxT1kAR4SYYnBzGj4JnmWMn6t5vyGyMC_y4YLmh8mIHOpxcZVJEsprf3y3ZBq8uOCvVsyJh1OJW7akkGV6m0E9aqgTPyauLUiZ_HEGPMPIRNA&expires_in=3600&token_type=Bearer

Screenshot

![](https://www.evernote.com/l/AAHj4QS6nTlDALfWlb0_i-9DPC7OLDRU3bcB/image.png)

- see [Using the Built-in Sign-up and Sign-in Webpages](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-integration.html) for setup details

**Login Page Example**

![](https://www.evernote.com/l/AAHW-OmcBZ9E3oDyvfHgDVDzTsL-f6iod48B/image.png)

---

**Screenshots**

Setting the IAM roles that are used for authenticated and unauthenticated users in the pool
![](https://www.evernote.com/l/AAGx7ZIzoK5MJZWDltK1na1guDzYwoysMIQB/image.png)

Auth role having full access to API Gateway and S3 for example access
![](https://www.evernote.com/l/AAGHQx657FBGybtmhsLUtPxqI6RPhLMZ5t0B/image.png)

---

### API Gateway | Use Amazon Cognito User Pools

- see [http://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-integrate-with-cognito.html](http://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-integrate-with-cognito.html) docs

Create cognito user pool authorizer in API Gateway (named cognito-auth-01 in this case)
![](https://www.evernote.com/l/AAGu3Lt9gyRIzLHHftwlExRQZk3aMBK2IhoB/image.png)

Set authorization ona resource to the cognito user pool authorizer (cognito-auth-01 in this case)
![](https://www.evernote.com/l/AAGfJ087Y2VDu5p-7Ns6y9M8eVzfTg4Ce94B/image.png)

Get the cognito identity token

> run `index.js:authenticateUser()` function

![](https://www.evernote.com/l/AAGt9Ly7TfBGnqfw_QlOCe6hwd1WCvSRj_oB/image.png)

Make request to endpoint with Authorization header set to cognito identity token
![](https://www.evernote.com/l/AAFt4R7k8K1O1rQJ-QfmMxrTG2qVTpqnnesB/image.png)

**NOTE**: remeber cognito identity token expires and can be refreshed

### Verify ID and Access Tokens

[AWS Cognito What is the way to verify the ID and access tokens sent by clients to my application](https://stackoverflow.com/questions/52036292/aws-cognito-what-is-the-way-to-verify-the-id-and-access-tokens-sent-by-clients-t)


---

### Auth0 SAML IdP

visit <https://com-brianpfeil-test-01.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id=5uol3m3jk3bqn39jrsjvhaooqp&redirect_uri=https%3A%2F%2Flocalhost>

![](https://www.evernote.com/l/AAE5xJKluNxPC44pRUGDaq-ntPw0LiQfVWoB/image.png)

#### Auth0 Config

![](https://www.evernote.com/l/AAFaMMC1WN1KTYjxxQpnrD8kGSs62E-zkYUB/image.png)

![](https://www.evernote.com/l/AAF_QL0BLEJNJJ_Cz7QKFACB_kBeyBamWYUB/image.png)

![](https://www.evernote.com/l/AAHnESDjepJAQqlaQfupIYpfjYsFVPUkiU8B/image.png)

#### Cognito Config

![](https://www.evernote.com/l/AAE7WHUog99DNrCqgYEs1l_PGi26FJQ509IB/image.png)

![](https://www.evernote.com/l/AAEehPNRFnlD2LOFMhWrmoqMShn4Bx8NW5cB/image.png)

![](https://www.evernote.com/l/AAH1WiGayk9Crq4sSf0PlDrQq-184WbQA_wB/image.png)

![](https://www.evernote.com/l/AAFopinNv4xKiY0rDpwMrSro2k13PGzRaCEB/image.png)

---

### Salesforce as Identity Provider (sign into app with salesforce credentials)

- Follow [Adding OIDC Identity Providers to a User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-oidc-idp.html) instructions
- Test via <https://com-brianpfeil-test-01.auth.us-east-1.amazoncognito.com/login?response_type=code&client_id=5uol3m3jk3bqn39jrsjvhaooqp&redirect_uri=https%3A%2F%2Flocalhost>
- login with `brian.pfeil@gmail.com` salesforce account

**Salesforce Configuration**

Custom Domain

![](https://www.evernote.com/l/AAGVYhKsrnJBeaAr55CVnhQbrxPA7lO2oIsB/image.png)

Connected App

![](https://www.evernote.com/l/AAEduS6ozeZGELmv7f4TGa6anYManigXqFsB/image.png)

![](https://www.evernote.com/l/AAFqd0Bu1nVHkYRn6Uc895G-h0gmIvqcQxYB/image.png)

![](https://www.evernote.com/l/AAEne7U_34pE7YLSpFs4gLgCarFlUYrWkJcB/image.png)

_Manage App_

![](https://www.evernote.com/l/AAFXQYOqJqVGS6wIw8_VJnZYX815bpX9xJoB/image.png)

![](https://www.evernote.com/l/AAEWAVq4pu1E2YYFGO_lrbvY9_UvHTW9tMkB/image.png)

**Cognito Configuration**

perfomed with `test-01` User Pool for `brian.pfeil@gmail.com` aws account

App Clients

![](https://www.evernote.com/l/AAELqWpapBFDhZn5pQnhTei4WjP48pDtDIEB/image.png)

User Pool Domain
![](https://www.evernote.com/l/AAG8goqlv2RNYqMW8m6qv4T9nDmtUiiuWkMB/image.png)

OIDC Provider
![](https://www.evernote.com/l/AAE7_Zrc-9lOGbM9naJHtTFw0vzW4Dpy29cB/image.png)

![](https://www.evernote.com/l/AAHr9evjotVPAJ1gSz6CfeSek9zLoSNR43cB/image.png)

![](https://www.evernote.com/l/AAHvLawiqmhM_4Wd4vJpzMQOjmDFX7M7Ut8B/image.png)

Attribute Mapping

![](https://www.evernote.com/l/AAFBL6oFtmhDSLIi7sUy7qP82QzKNQYZQwgB/image.png)

**Login Example**

Login form

![](https://www.evernote.com/l/AAGGl5swYB1A7KoARlWhoVKuo6_jfrS1Qs0B/image.png)

Grant access

![](https://www.evernote.com/l/AAGGTc6xqI5EpK_nuiDo9KtdXMwcQLalA8AB/image.png)

Code grant returned

![](https://www.evernote.com/l/AAH7nUTTy6BKcJym_mg6SiZ2BXx7Py7SpbIB/image.png)

User created in User Pool

![](https://www.evernote.com/l/AAF7KCSeBahBpYqBZBeVYVEULJ_m9xF-NIwB/image.png)



