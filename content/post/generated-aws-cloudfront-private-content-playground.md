+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2020-08-10
description = ""
summary = " "
draft = false
slug = "aws-cloudfront-private-content"
tags = ["aws","cloudfront",]
title = "AWS CloudFront Private Content"
repoFullName = "pfeilbr/aws-cloudfront-private-content-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-cloudfront-private-content-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-cloudfront-private-content-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-cloudfront-private-content-playground</a>
</div>


## Description

Explore options for serving private content via [CloudFront](https://aws.amazon.com/cloudfront/)

This infrastructure provisioning and deployment pipeline performs an atomic deploy of private static content from a github repo to a static site (Route 53 + ACM + WAF + Cognito Federated SSO to Auth0 SAML + CloudFront + S3) when a tag (release) is applied to the repo.

---

**Demo Private Static Site**

* <https://staging.allthecloudbits.com/> - pre-production protected by basic auth.  login with Username: user01, Password: password01
* <https://allthecloudbits.com/> - production protected by Cognito Federated SSO to Auth0 SAML.  login with Username: user01@example.com, Password: password01

---

## Prerequisites

* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) - [configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) with AWS credentials
* [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [jq](https://stedolan.github.io/jq/)
* [Docker](https://www.docker.com/products/docker-desktop)

---

## Infrastructure Provisioning Steps

1. manually create a [public route 53 hosted zone](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/AboutHZWorkingWith.html) for your domain name (e.g. `mydomain.com`)
2. update `DOMAIN_NAME` parameter in [`./run.sh`](./run.sh) with the hosted zone name 
3. provision aws resources `./run.sh deploy-infrastructure`
4. Check [ACM in AWS Console](https://console.aws.amazon.com/acm/home) to confirm Certificate validation via DNS validation has completed.  May need to add [DNS validation records to route 53 hosted zone](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html).
5. update pipeline variables
    * REGION - *default is us-east-1*
    * STACK_NAME - defined in [`./run.sh`](./run.sh)
    * AWS_ACCESS_KEY_ID - `AccessKey` output in `./tmp/${STACK_NAME}-outputs.json`
    * AWS_SECRET_ACCESS_KEY - `SecretKey` output in `./tmp/${STACK_NAME}-outputs.json`

## Website Content Publishing From Local Machine Steps

1. update website content in [`public`](public) directory
1. run one of the following deployment commands: 
    ```sh
    # format
    ./run.sh publish-content staging|prod [--blue-green-publish] [--apply-routing-rules] [--invalidate-cloudfront-cache]

    # example(s)

    # full blue/green deploy with routing rules and cloudfront cache invalidation
    ./run.sh publish-content staging --blue-green-publish --apply-routing-rules --invalidate-cloudfront-cache
    ./run.sh publish-content prod --blue-green-publish --apply-routing-rules --invalidate-cloudfront-cache

    # content only update to staging
    ./run.sh publish-content staging

    # content only update to production
    ./run.sh publish-content prod
    ```
  1. view changes @ <https://staging.mydomain.com> or <https://mydomain.com>
      ```sh
      ./run.sh open-website staging
      ./run.sh open-website production
      ```
  
## Website Content Publishing via Commit Steps

1. ensure you have `develop` branch checked out *(this corresponds to staging environment)*
1. update website content in [`public`](public) directory and push to github.
1. *(optional)* update redirect rules in [`routing-rules/routing-rules.txt`](routing-rules/routing-rules.txt)
1. push your commit(s) to remote (github)
1. publish will run.  can take up to 20 minutes to complete due CloudFront distribution update.
1. verify updated content by visiting <https://staging.mydomain.com>
1. to publish staging to production, checkout master branch and merge in develop
1. push your commit(s) to remote (github)
1. verify updated content by visiting <https://mydomain.com> and <https://www.mydomain.com>

## Deprovisioning

1. deprovision aws resources `./run.sh delete-infrastructure`
1. *(optional)* manually delete S3 website and CloudFront logs buckets.
    > these are not deleted because they still contain objects
1. *(optional)* run `./run.sh delete-infrastructure` **again** to permanently delete stack


---

## Demo

1. visit <https://allthecloudbits.com>
1. sign in with  Auth0 test user.  user01@example.com / password01

## Staging Docs

* `AWS::Cognito::UserPool` created first in order to provide required UserPoolId to SAML provider (Auth0), then `AWS::Cognito::UserPoolIdentityProvider` can be provisioned with SAML `MetadataURL` from SAML provider (Auth0)
    ![](https://www.evernote.com/l/AAEincsb5ZdDMYk3RRpRgQE4AmgqvpU5_b8B/image.png)
* Set AWS Secrets Manager Secrets.  CloudFront Key Pair Private Key.
* Set SSM parameter store itemsCloudFront Key Pair Id, Public Key.
* Debug SAML
    ![](https://www.evernote.com/l/AAEgpBPAJIZEobg-W98KcjGBQ_4zI1t-t1wB/image.png)
    ![](https://www.evernote.com/l/AAHkehP3TIFFTI-I8rh3nuiA13I7ze6shlAB/image.png)


---

## Detail Examples

### cognito login url

<https://allthecloudbits.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id=3al3r1fatr213ndvp2uoqcfgi9&redirect_uri=https://allthecloudbits.com/login/redirect/>

### cognito userinfo url

<https://allthecloudbits.auth.us-east-1.amazoncognito.com/oauth2/userInfo>

Example Usage

```sh
export ACCESS_TOKEN='eyJraWQiOiJqdzNzaUhDU2NxeWVhMnliKytkeHNNZXBnVk5JSE5Bc1pQVldKUVJPUW1BPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxM2VkODk4Ni1hZjc2LTQzYWYtOGU5Mi01ZDdjMzM1ODQ1MzEiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTFfUVVTTlhXc3hMX2F1dGgwIl0sInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1OTczMjM5ODgsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX1FVU05YV3N4TCIsImV4cCI6MTU5NzMyNzU4OCwiaWF0IjoxNTk3MzIzOTg4LCJ2ZXJzaW9uIjoyLCJqdGkiOiIwZTkzZWFiMi02YzIyLTQyMTctYWNmNC0xNGMzOGQ1NWY0NGYiLCJjbGllbnRfaWQiOiIzYWwzcjFmYXRyMjEzbmR2cDJ1b3FjZmdpOSIsInVzZXJuYW1lIjoiYXV0aDBfYXV0aDB8NWYzMjliNGY3M2VkYzEwMDNkNWY1ZDczIn0.X8cZNbyz8oF46MaO60gD9PDXuart0MvIqRNa7IjvbO5DuQM0uMMs6Xfb1ftcEk6iADjz-i8sEtzkd0AQXr-LdVLRLWTl7TQXICzppo2dOgRlK4HIY0RHktuDrCpciWaGmjFz35wKu0omqmzVSNFNv8Bdgv1peCeOvvQDnxeP4ewaHvpUVZbd3todkoytMoQSKBQ3DwepbHM79t_jluiamyPWzJtcHcMZ0Fdl5RQIg8_fsDq1ouuMaYfUESqpwyw0hQv39xL2VSU-RzfoS3oeqeHV85W1CMwc21t_mhTg1gYmYr7z2dTBFbYka60ip50ImEQgTrzne_hTFfiZwOD4QA'

curl -H "Authorization: Bearer ${ACCESS_TOKEN}" https://allthecloudbits.auth.us-east-1.amazoncognito.com/oauth2/userInfo
```

output
```json
{
    "sub": "13ed8986-af76-43af-8e92-5d7c33584531",
    "identities": "[{\"userId\":\"auth0|5f329b4f73edc1003d5f5d73\",\"providerName\":\"auth0\",\"providerType\":\"SAML\",\"issuer\":\"urn:svc.auth0.com\",\"primary\":true,\"dateCreated\":1597158755583}]",
    "email_verified": "false",
    "email": "user01@example.com",
    "username": "auth0_auth0|5f329b4f73edc1003d5f5d73"
}
```

### cognito logout url

<https://allthecloudbits.auth.us-east-1.amazoncognito.com/logout?response_type=token&client_id=3al3r1fatr213ndvp2uoqcfgi9&redirect_uri=https://allthecloudbits.com/login/logout.html>

---

### Auth0 SAML Configuration

```json
{
 "audience":  "urn:amazon:cognito:sp:us-east-1_QUSNXWsxL",
// "recipient": "http://foo",
"mappings": {
//   "user_id":     "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier",
  "email":       "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"
//   "name":        "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name",
//   "given_name":  "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname",
//   "family_name": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname",
//   "upn":         "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn",
//   "groups":      "http://schemas.xmlsoap.org/claims/Group"
}
// "createUpnClaim":       true,
// "passthroughClaimsWithNoMapping": true,
// "mapUnknownClaimsAsIs": false,
// "mapIdentities":        true,
// "signatureAlgorithm":   "rsa-sha1",
// "digestAlgorithm":      "sha1",
// "destination":          "http://foo",
// "lifetimeInSeconds":    3600,
// "signResponse":         false,
// "typedAttributes":      true,
// "includeAttributeNameFormat":  true,
// "nameIdentifierFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
// "nameIdentifierProbes": [
//   "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier",
//   "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress",
//   "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"
// ],
// "authnContextClassRef": "urn:oasis:names:tc:SAML:2.0:ac:classes:unspecified",
// "logout": {
//   "callback": "http://foo/logout",
//   "slo_enabled": true
// },
// "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
}
```

---

### tokens provided to application

```sh
https://allthecloudbits.com/login/#access_token=eyJraWQiOiJqdzNzaUhDU2NxeWVhMnliKytkeHNNZXBnVk5JSE5Bc1pQVldKUVJPUW1BPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxM2VkODk4Ni1hZjc2LTQzYWYtOGU5Mi01ZDdjMzM1ODQ1MzEiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTFfUVVTTlhXc3hMX2F1dGgwIl0sInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoib3BlbmlkIGVtYWlsIiwiYXV0aF90aW1lIjoxNTk3MTU5NzEzLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9RVVNOWFdzeEwiLCJleHAiOjE1OTcxNjMzMTMsImlhdCI6MTU5NzE1OTcxMywidmVyc2lvbiI6MiwianRpIjoiMTE0ZjU3ZWEtNGRkMy00NzU0LWJhN2ItODFmZGNlMGZmYTk2IiwiY2xpZW50X2lkIjoiM2FsM3IxZmF0cjIxM25kdnAydW9xY2ZnaTkiLCJ1c2VybmFtZSI6ImF1dGgwX2F1dGgwfDVmMzI5YjRmNzNlZGMxMDAzZDVmNWQ3MyJ9.K9tKXxDDoOPXa3CBrvGIPEUe2jP5CRf0AOL0_zhZgv9ej2kWU-gKcLLmIs9xkGwwCGciBAuI0pHugmCVYjWGYjw6UscZt54gszpKkAI0LS6Qxr5dzV9K-fC1ZbFLkrufj2xgWAmQ-un4RRcKBLUrog70WhlY5ABx-sHlVpPXAwXY9iiKaDL5NpiMFRFx4jgliulCkjCaSYYrhFzT2BP8iTpvRgvp4mhJ90AyvnFPNLrpJI6-jB_KtqGwIcS9rCCrJpA37n0qJ2KAwWm_BRJBx1_Gh3EzYdFQtfEJ8YCr3rh03zbZ-izvkqDknh49QTiYxR5MUqa16_BzBP8DqQGstQ&id_token=eyJraWQiOiJweElSWFRBMTBlakI3TUpBbnVLS0l1VHo1eTNCcFU4eTUxNUd3Y1lwSHg0PSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiZkpjcEl2U3Zia2Z5TVRSaVB6VVA4dyIsInN1YiI6IjEzZWQ4OTg2LWFmNzYtNDNhZi04ZTkyLTVkN2MzMzU4NDUzMSIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV9RVVNOWFdzeExfYXV0aDAiXSwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9RVVNOWFdzeEwiLCJjb2duaXRvOnVzZXJuYW1lIjoiYXV0aDBfYXV0aDB8NWYzMjliNGY3M2VkYzEwMDNkNWY1ZDczIiwibm9uY2UiOiJOdUFIUVZtZUhfT0FTWVRmREJwczJVLXZpNEl3VG5HYlNaUzdOUXVMVXhaSnBXSGxoVWc4TjlCMHltdEY3UE8yVHFxcHhXd0pKekNyWFFKZ1cxRFBueXRpNkhjVUV2dUh6NUctSW5uYk90akdYbktEcnNiTHRYRHBFOTRYLXBfMUk0RFRYUlNNeElGTnhEU0w0SGJma05IWkxxQVU1ZXJzcmUwWFlLVHNkNkkiLCJhdWQiOiIzYWwzcjFmYXRyMjEzbmR2cDJ1b3FjZmdpOSIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6ImF1dGgwfDVmMzI5YjRmNzNlZGMxMDAzZDVmNWQ3MyIsInByb3ZpZGVyTmFtZSI6ImF1dGgwIiwicHJvdmlkZXJUeXBlIjoiU0FNTCIsImlzc3VlciI6InVybjpzdmMuYXV0aDAuY29tIiwicHJpbWFyeSI6InRydWUiLCJkYXRlQ3JlYXRlZCI6IjE1OTcxNTg3NTU1ODMifV0sInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNTk3MTU5NzEzLCJleHAiOjE1OTcxNjMzMTMsImlhdCI6MTU5NzE1OTcxMywiZW1haWwiOiJ1c2VyMDFAZXhhbXBsZS5jb20ifQ.J_ALJGY73WT8iz8AEzMM1LCdZTgkZeJ21Dhm05eoZd0RbyI3iChHZhR7T7wqBMzFSDdhTBvqen1rGKlZXZ25JODTRFIDJEMQqxPr1oC-8j-X4l1futecOUKlMybMuOrf01uMmJKvh6HRqNagtK_2m3saOCNBrYQmw-bEkiqjLmSo6CMyJEcQfCiWUvZ-xaev7oXY1-8KUkrP_rf_Z5Mov0V2yluFk6UP39rCEr7qUz1aKqMElqQiBNIamfoi6rB3oPM4qth1v92w_u1zrdtuCNBPlWqoKglejXfykPvH3Rjus2yW3I1ILzPLTxkt7mcfBuyjYBKV_zRxsDRmN1yo0g&token_type=Bearer&expires_in=3600
```

*individual tokens broken out*

```sh
id_token=eyJraWQiOiJweElSWFRBMTBlakI3TUpBbnVLS0l1VHo1eTNCcFU4eTUxNUd3Y1lwSHg0PSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiMG02X2pacDh6U0RGVWZsSUYtb18yZyIsInN1YiI6IjEzZWQ4OTg2LWFmNzYtNDNhZi04ZTkyLTVkN2MzMzU4NDUzMSIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV9RVVNOWFdzeExfYXV0aDAiXSwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9RVVNOWFdzeEwiLCJjb2duaXRvOnVzZXJuYW1lIjoiYXV0aDBfYXV0aDB8NWYzMjliNGY3M2VkYzEwMDNkNWY1ZDczIiwiYXVkIjoiM2FsM3IxZmF0cjIxM25kdnAydW9xY2ZnaTkiLCJpZGVudGl0aWVzIjpbeyJ1c2VySWQiOiJhdXRoMHw1ZjMyOWI0ZjczZWRjMTAwM2Q1ZjVkNzMiLCJwcm92aWRlck5hbWUiOiJhdXRoMCIsInByb3ZpZGVyVHlwZSI6IlNBTUwiLCJpc3N1ZXIiOiJ1cm46c3ZjLmF1dGgwLmNvbSIsInByaW1hcnkiOiJ0cnVlIiwiZGF0ZUNyZWF0ZWQiOiIxNTk3MTU4NzU1NTgzIn1dLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTU5NzE3NjM4MywiZXhwIjoxNTk3MTc5OTgzLCJpYXQiOjE1OTcxNzYzODQsImVtYWlsIjoidXNlcjAxQGV4YW1wbGUuY29tIn0.HTAVp_VeZYnekdMgfFqiN2P4cEkY8R9T-T72omgaKU9k00-Nv_yCCrUGukzILO6_U0-UyBHhMPVu1EBByT3fKv9rtzB_5SvTLLeQhwj82ELX9_ZIrUNgVGj_bT1NCEOoLw6_HwF-hKX4gxiSiPgkOpxEsVwDLOjNAx7Jm2Bt49gZWB1DBrIsCBeIB3tEbW-2uf46eOKsJ9PilTJIY_ePLM1zr1QOal0FDUAqT44bQaEcKPKjSpYaAD4MVHnih3KDdLqoRzedJMeaIrTW8_eMODZ7GwniVcs0mDe5Z0D1wYC8iTajOtlyHEZHhAaDdw0YGvHdVWz8eGrLmVsCSdF7DA

&access_token=eyJraWQiOiJqdzNzaUhDU2NxeWVhMnliKytkeHNNZXBnVk5JSE5Bc1pQVldKUVJPUW1BPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxM2VkODk4Ni1hZjc2LTQzYWYtOGU5Mi01ZDdjMzM1ODQ1MzEiLCJjb2duaXRvOmdyb3VwcyI6WyJ1cy1lYXN0LTFfUVVTTlhXc3hMX2F1dGgwIl0sInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoib3BlbmlkIGVtYWlsIiwiYXV0aF90aW1lIjoxNTk3MTc2MzgzLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9RVVNOWFdzeEwiLCJleHAiOjE1OTcxNzk5ODMsImlhdCI6MTU5NzE3NjM4NCwidmVyc2lvbiI6MiwianRpIjoiZGMxMjZkMWQtMDFlNy00NWY2LThlZmQtMmViZjMyMzhkNTNkIiwiY2xpZW50X2lkIjoiM2FsM3IxZmF0cjIxM25kdnAydW9xY2ZnaTkiLCJ1c2VybmFtZSI6ImF1dGgwX2F1dGgwfDVmMzI5YjRmNzNlZGMxMDAzZDVmNWQ3MyJ9.UufAOCwINbVT9E_j61wOgjpkaSuLxWej2hOT26l8mQmCWidylKFVYlyb90ynxXuOoE2vMcWiwvlwla6vH1SCaV_LvSCpQLBoXueWj97S29XxBJBlUBo8AAe8i5es8D9kbSPuwjhfmC50KgumXZWOzANrU5jrfeCRMdqPPrllNnd_3yJQTlQuLXdB9vuao8VYj71Pbb2gUC945mKyluqidl-71Hkl0FmSr0Uvwf0ILZlUwzf7uu-aOVOnSuWlz5cFjbnWT9AEaAcFYkrYCx2OiSgUb-0vsLYN1RkBoi-ZfcHVERQek5lYDimt3MwetdhgLZ0Q2vlBA9V4chkfnE3aXw

&expires_in=3600

&token_type=Bearer
```

---

### setting signed cookies via server-side response

```json
{
    "response": {
        "status": "302",
        "statusDescription": "Found",
        "headers": {
            "set-cookie": [
                {
                    "key": "Set-Cookie",
                    "value": "CloudFront-Key-Pair-Id=APKAJK35MM4IQ2LXQOFA; domain=allthecloudbits.com; path=/; httpOnly=true"
                },
                {
                    "key": "Set-Cookie",
                    "value": "CloudFront-Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cCo6Ly9hbGx0aGVjbG91ZGJpdHMuY29tLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE1OTc0MTg1MDh9fX1dfQ__; domain=allthecloudbits.com; path=/; httpOnly=true"
                },
                {
                    "key": "Set-Cookie",
                    "value": "CloudFront-Signature=di-2bRnf~V9aUz2PzzEQ98TWvCKPeRhq~mu47Xjw5Mf358bidk2OYIF9i0aaFHUB4WSAEAtLnEnxyK~b~53Dvqt7L~VswPPE7PYfBKagC3yEUxv4NIowFrgSepI4uXeQSw2ri6jG9QKZVBnP5EPAh~QNlveFt-yUYILrKlozPa72YM6UVlxbfRWGgfcSH8bwf3Yj24CUXC4V7RzZxPlXCdIhlnNkSOzIlgFH~6pJpRuPV~etpbnZ6Pt6aIE09vynwLheYMBhet9VahevUV9U~Amj1SJpsQYLmHGx0GKo-9jJxhTaeNK3pz6OlCGYMUSPslFddjBcH1CVq5Ct8rWGaQ__; domain=allthecloudbits.com; path=/; httpOnly=true"
                }
            ],
            "location": [
                {
                    "key": "Location",
                    "value": "/"
                }
            ]
        }
    }
}
```

### expiring signed cookies via server-side response

```json
{
    "response": {
        "status": "200",
        "statusDescription": "OK",
        "headers": {
            "set-cookie": [
                {
                    "key": "Set-Cookie",
                    "value": "CloudFront-Key-Pair-Id=deleted; domain=allthecloudbits.com; path=/; httpOnly=true; expires=Thu, 01 Jan 1970 00:00:00 GMT"
                },
                {
                    "key": "Set-Cookie",
                    "value": "CloudFront-Policy=deleted; domain=allthecloudbits.com; path=/; httpOnly=true; expires=Thu, 01 Jan 1970 00:00:00 GMT"
                },
                {
                    "key": "Set-Cookie",
                    "value": "CloudFront-Signature=deleted; domain=allthecloudbits.com; path=/; httpOnly=true; expires=Thu, 01 Jan 1970 00:00:00 GMT"
                }
            ]
        },
        "body": "\n  <!DOCTYPE html>\n  <html lang=\"en\">\n  \n  <head>\n      <meta charset=\"UTF-8\">\n      <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n      <meta http-equiv=\"refresh\"\n          content=\"0; URL=https://allthecloudbits.auth.us-east-1.amazoncognito.com/logout?response_type=token&client_id=3al3r1fatr213ndvp2uoqcfgi9&redirect_uri=https://allthecloudbits.com/login/logout.html\" />\n      <title>logout redirect</title>\n  </head>\n  \n  <body>\n  </body>\n  \n  </html>  \n  "
    }
}
```

---

### Example Encoded SAML response from Auth0

```sh
PHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIElEPSJfMTAxODU3ZTIxMzJjZWUxZmQyYTMiICBWZXJzaW9uPSIyLjAiIElzc3VlSW5zdGFudD0iMjAyMC0wOC0xMlQxNzo1Njo1Ny42MDhaIiAgRGVzdGluYXRpb249Imh0dHBzOi8vbWFuYWdlLmF1dGgwLmNvbS90ZXN0ZXIvc2FtbHAiPjxzYW1sOklzc3VlciB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIj51cm46c3ZjLmF1dGgwLmNvbTwvc2FtbDpJc3N1ZXI+PHNhbWxwOlN0YXR1cz48c2FtbHA6U3RhdHVzQ29kZSBWYWx1ZT0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOnN0YXR1czpTdWNjZXNzIi8+PC9zYW1scDpTdGF0dXM+PHNhbWw6QXNzZXJ0aW9uIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphc3NlcnRpb24iIFZlcnNpb249IjIuMCIgSUQ9Il9DNzNUZ1VPUlRSdnp0SmhNQ0xuQmVKb05XVmZRQVFhYyIgSXNzdWVJbnN0YW50PSIyMDIwLTA4LTEyVDE3OjU2OjU3LjYwMFoiPjxzYW1sOklzc3Vlcj51cm46c3ZjLmF1dGgwLmNvbTwvc2FtbDpJc3N1ZXI+PFNpZ25hdHVyZSB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnIyI+PFNpZ25lZEluZm8+PENhbm9uaWNhbGl6YXRpb25NZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzEwL3htbC1leGMtYzE0biMiLz48U2lnbmF0dXJlTWV0aG9kIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnI3JzYS1zaGExIi8+PFJlZmVyZW5jZSBVUkk9IiNfQzczVGdVT1JUUnZ6dEpoTUNMbkJlSm9OV1ZmUUFRYWMiPjxUcmFuc2Zvcm1zPjxUcmFuc2Zvcm0gQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjZW52ZWxvcGVkLXNpZ25hdHVyZSIvPjxUcmFuc2Zvcm0gQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzEwL3htbC1leGMtYzE0biMiLz48L1RyYW5zZm9ybXM+PERpZ2VzdE1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvMDkveG1sZHNpZyNzaGExIi8+PERpZ2VzdFZhbHVlPkYvUW54N052RnB2SWVhMDRoSXovS214SkNUST08L0RpZ2VzdFZhbHVlPjwvUmVmZXJlbmNlPjwvU2lnbmVkSW5mbz48U2lnbmF0dXJlVmFsdWU+dUErRXdXT2dQbEU0eVZBZ0k4dW81bU53Tm4zRzU5Q2ZlRStaV0pmVHZEVXJwNXNaWHlYcDVheHlLZUVsU0ZnWCs4clRxYThtc010VnJWL1djS2pwZmlqUUdQTkZPY0o3OU5ldDIwTXFwNlJvUkZZb1ZOWEk5Zk54bnFtQ1dVWFpvc1hRRURrTUk5eGRZcmVHWnI0RkoyWEZZVHhESzIyd0RFbHgwUnJvY3N1V1N1alRzY0V2NzZlNmVReS91K3J4bHZta2loOWJBQ2JnVDh3VGdPVWVhTkU1YXdHMEhsTXcvaWovRkFneWZFTC9mb3Fqc3FXVXlTVlRoRGxDVzgrSEVvTzNJd3BOcjk5MnJnYXlCak4zYzc5alI4Tk1FUFYzdzgxYnR3SFR1M2RxaEx2ak9kbm9Md2VhZlZJeHphK3NiR2hZUHgxTTFSUUJVNjllUS9LVHNnPT08L1NpZ25hdHVyZVZhbHVlPjxLZXlJbmZvPjxYNTA5RGF0YT48WDUwOUNlcnRpZmljYXRlPk1JSUM5VENDQWQyZ0F3SUJBZ0lKUExqZlMwei9yR2tvTUEwR0NTcUdTSWIzRFFFQkN3VUFNQmd4RmpBVUJnTlZCQU1URFhOMll5NWhkWFJvTUM1amIyMHdIaGNOTVRjd09USXhNVE14TlRBeVdoY05NekV3TlRNeE1UTXhOVEF5V2pBWU1SWXdGQVlEVlFRREV3MXpkbU11WVhWMGFEQXVZMjl0TUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUEydWxlTTlwaHVkelU5S3VXZ2ZlZTlnQ3BpUE0rakdubHlkQjByU2lYZDBEdG5lckJRWC8vN2k3d1JTNGpKM2RlWWd3NVk5SWROTFJSZ3JXdVBRZWRSUDRGbXdRRGRxU2thTVJNdTNraDVHUHhkNGYrekxYaEduLzRPNm4ycGVBamkvQ21meGhQUW14b0xKU1VQeVhhWFNZQy95dWV6Z3NTT0IycG82N01RQW5uOGE0WTh6MVVjVE5uU2ExQmJsY2o5MGhvRFcvZ1VwK0poV2tIVFhHeGZObmNaMHpTK2FiQ0dLZE1WdUd5YnJSckFHOGtRWWpyQWVvZGlLejQ0ZWhmQTNNMmtQZVp4dGFVTFA4MTZxWCtrbFppaExsOVRDV2FocS9LQUJyYXE4VkR4NTRLSE9wbWVKUTFJRytUbjZ2SnZDeCtaSlBzVlVDWFdKd0tXazQ4RFFJREFRQUJvMEl3UURBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUIwR0ExVWREZ1FXQkJTR2xaem9sNlJJRlNJRGYrOWVUeVU0S0xjWnN6QU9CZ05WSFE4QkFmOEVCQU1DQW9Rd0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dFQkFLWTFMdm9heXVPeHJXZk55MXdoU2ZtK284bVVpVUQrb0VVUDdDbEVnUmExaTE0aE1QNldaSC9XV09sTnhLSmZHZWJDZWlLNFE5enhyUlZvbk14dkZ5NkFURFpaWnc4WFRzNTdpWmFXZmtCWHhaYXhjVmk1NHVTUlM1T0ZkVU1tSFY1d2FrTVhlTWtkcXhnTFZscUNvQVlOSm9WZUpSZU83dVp1REk2Q0R0aHhEVHNFcnVGcEpnMyt2SVMzVU1GeFRWaDdqeU5RQ2xuNUFhaDZSQVRob2ozdytQMExRQjl4YjAvV1ZBWUV4bmtSTFRSQXUxdkpwM3IwN2d0MVBJT2kxaE42dVhZSG9YT2RWNmtPRDZZWTUzNU1mb0FwVTNUT1RBbmovUm5yYVYvS2EwREp1YVZhdFNkaGpjT1U2NUZUcUxaN0FuVUlQQndEeDBjUXRqdDFPMWs9PC9YNTA5Q2VydGlmaWNhdGU+PC9YNTA5RGF0YT48L0tleUluZm8+PC9TaWduYXR1cmU+PHNhbWw6U3ViamVjdD48c2FtbDpOYW1lSUQgRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDpwZXJzaXN0ZW50Ij5hdXRoMHw1ZjMyOWI0ZjczZWRjMTAwM2Q1ZjVkNzM8L3NhbWw6TmFtZUlEPjxzYW1sOlN1YmplY3RDb25maXJtYXRpb24gTWV0aG9kPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6Y206YmVhcmVyIj48c2FtbDpTdWJqZWN0Q29uZmlybWF0aW9uRGF0YSBOb3RPbk9yQWZ0ZXI9IjIwMjAtMDgtMTJUMTg6NTY6NTcuNjAwWiIgUmVjaXBpZW50PSJodHRwczovL21hbmFnZS5hdXRoMC5jb20vdGVzdGVyL3NhbWxwIi8+PC9zYW1sOlN1YmplY3RDb25maXJtYXRpb24+PC9zYW1sOlN1YmplY3Q+PHNhbWw6Q29uZGl0aW9ucyBOb3RCZWZvcmU9IjIwMjAtMDgtMTJUMTc6NTY6NTcuNjAwWiIgTm90T25PckFmdGVyPSIyMDIwLTA4LTEyVDE4OjU2OjU3LjYwMFoiPjxzYW1sOkF1ZGllbmNlUmVzdHJpY3Rpb24+PHNhbWw6QXVkaWVuY2U+dXJuOmFtYXpvbjpjb2duaXRvOnNwOnVzLWVhc3QtMV9RVVNOWFdzeEw8L3NhbWw6QXVkaWVuY2U+PC9zYW1sOkF1ZGllbmNlUmVzdHJpY3Rpb24+PC9zYW1sOkNvbmRpdGlvbnM+PHNhbWw6QXV0aG5TdGF0ZW1lbnQgQXV0aG5JbnN0YW50PSIyMDIwLTA4LTEyVDE3OjU2OjU3LjYwMFoiIFNlc3Npb25JbmRleD0iX0NxT21UVWJTMkVQQnVkSWpzNTJ1ZjdPVnFCcmRUcHFQIj48c2FtbDpBdXRobkNvbnRleHQ+PHNhbWw6QXV0aG5Db250ZXh0Q2xhc3NSZWY+dXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFjOmNsYXNzZXM6dW5zcGVjaWZpZWQ8L3NhbWw6QXV0aG5Db250ZXh0Q2xhc3NSZWY+PC9zYW1sOkF1dGhuQ29udGV4dD48L3NhbWw6QXV0aG5TdGF0ZW1lbnQ+PHNhbWw6QXR0cmlidXRlU3RhdGVtZW50IHhtbG5zOnhzPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYSIgeG1sbnM6eHNpPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYS1pbnN0YW5jZSI+PHNhbWw6QXR0cmlidXRlIE5hbWU9Imh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL2VtYWlsYWRkcmVzcyIgTmFtZUZvcm1hdD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmF0dHJuYW1lLWZvcm1hdDp1cmkiPjxzYW1sOkF0dHJpYnV0ZVZhbHVlIHhzaTp0eXBlPSJ4czpzdHJpbmciPnVzZXIwMUBleGFtcGxlLmNvbTwvc2FtbDpBdHRyaWJ1dGVWYWx1ZT48L3NhbWw6QXR0cmlidXRlPjxzYW1sOkF0dHJpYnV0ZSBOYW1lPSJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy91cG4iIE5hbWVGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphdHRybmFtZS1mb3JtYXQ6dXJpIj48c2FtbDpBdHRyaWJ1dGVWYWx1ZSB4c2k6dHlwZT0ieHM6c3RyaW5nIj51c2VyMDFAZXhhbXBsZS5jb208L3NhbWw6QXR0cmlidXRlVmFsdWU+PC9zYW1sOkF0dHJpYnV0ZT48c2FtbDpBdHRyaWJ1dGUgTmFtZT0iaHR0cDovL3NjaGVtYXMuYXV0aDAuY29tL2lkZW50aXRpZXMvZGVmYXVsdC91c2VyX2lkIiBOYW1lRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXR0cm5hbWUtZm9ybWF0OnVyaSI+PHNhbWw6QXR0cmlidXRlVmFsdWUgeHNpOnR5cGU9InhzOnN0cmluZyI+NWYzMjliNGY3M2VkYzEwMDNkNWY1ZDczPC9zYW1sOkF0dHJpYnV0ZVZhbHVlPjwvc2FtbDpBdHRyaWJ1dGU+PHNhbWw6QXR0cmlidXRlIE5hbWU9Imh0dHA6Ly9zY2hlbWFzLmF1dGgwLmNvbS9pZGVudGl0aWVzL2RlZmF1bHQvcHJvdmlkZXIiIE5hbWVGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphdHRybmFtZS1mb3JtYXQ6dXJpIj48c2FtbDpBdHRyaWJ1dGVWYWx1ZSB4c2k6dHlwZT0ieHM6c3RyaW5nIj5hdXRoMDwvc2FtbDpBdHRyaWJ1dGVWYWx1ZT48L3NhbWw6QXR0cmlidXRlPjxzYW1sOkF0dHJpYnV0ZSBOYW1lPSJodHRwOi8vc2NoZW1hcy5hdXRoMC5jb20vaWRlbnRpdGllcy9kZWZhdWx0L2Nvbm5lY3Rpb24iIE5hbWVGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphdHRybmFtZS1mb3JtYXQ6dXJpIj48c2FtbDpBdHRyaWJ1dGVWYWx1ZSB4c2k6dHlwZT0ieHM6c3RyaW5nIj5Vc2VybmFtZS1QYXNzd29yZC1BdXRoZW50aWNhdGlvbjwvc2FtbDpBdHRyaWJ1dGVWYWx1ZT48L3NhbWw6QXR0cmlidXRlPjxzYW1sOkF0dHJpYnV0ZSBOYW1lPSJodHRwOi8vc2NoZW1hcy5hdXRoMC5jb20vaWRlbnRpdGllcy9kZWZhdWx0L2lzU29jaWFsIiBOYW1lRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXR0cm5hbWUtZm9ybWF0OnVyaSI+PHNhbWw6QXR0cmlidXRlVmFsdWUgeHNpOnR5cGU9InhzOmJvb2xlYW4iPmZhbHNlPC9zYW1sOkF0dHJpYnV0ZVZhbHVlPjwvc2FtbDpBdHRyaWJ1dGU+PHNhbWw6QXR0cmlidXRlIE5hbWU9Imh0dHA6Ly9zY2hlbWFzLmF1dGgwLmNvbS9jbGllbnRJRCIgTmFtZUZvcm1hdD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmF0dHJuYW1lLWZvcm1hdDp1cmkiPjxzYW1sOkF0dHJpYnV0ZVZhbHVlIHhzaTp0eXBlPSJ4czpzdHJpbmciPjB4M2U0elZGQ252SHdGN1VHVDJHWllVSGdBMFk2dEpvPC9zYW1sOkF0dHJpYnV0ZVZhbHVlPjwvc2FtbDpBdHRyaWJ1dGU+PHNhbWw6QXR0cmlidXRlIE5hbWU9Imh0dHA6Ly9zY2hlbWFzLmF1dGgwLmNvbS9jcmVhdGVkX2F0IiBOYW1lRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXR0cm5hbWUtZm9ybWF0OnVyaSI+PHNhbWw6QXR0cmlidXRlVmFsdWUgeHNpOnR5cGU9InhzOmFueVR5cGUiPlR1ZSBBdWcgMTEgMjAyMCAxMzoyMToxOSBHTVQrMDAwMCAoQ29vcmRpbmF0ZWQgVW5pdmVyc2FsIFRpbWUpPC9zYW1sOkF0dHJpYnV0ZVZhbHVlPjwvc2FtbDpBdHRyaWJ1dGU+PHNhbWw6QXR0cmlidXRlIE5hbWU9Imh0dHA6Ly9zY2hlbWFzLmF1dGgwLmNvbS9lbWFpbF92ZXJpZmllZCIgTmFtZUZvcm1hdD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmF0dHJuYW1lLWZvcm1hdDp1cmkiPjxzYW1sOkF0dHJpYnV0ZVZhbHVlIHhzaTp0eXBlPSJ4czpib29sZWFuIj50cnVlPC9zYW1sOkF0dHJpYnV0ZVZhbHVlPjwvc2FtbDpBdHRyaWJ1dGU+PHNhbWw6QXR0cmlidXRlIE5hbWU9Imh0dHA6Ly9zY2hlbWFzLmF1dGgwLmNvbS9uYW1lIiBOYW1lRm9ybWF0PSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXR0cm5hbWUtZm9ybWF0OnVyaSI+PHNhbWw6QXR0cmlidXRlVmFsdWUgeHNpOnR5cGU9InhzOnN0cmluZyI+dXNlcjAxQGV4YW1wbGUuY29tPC9zYW1sOkF0dHJpYnV0ZVZhbHVlPjwvc2FtbDpBdHRyaWJ1dGU+PHNhbWw6QXR0cmlidXRlIE5hbWU9Imh0dHA6Ly9zY2hlbWFzLmF1dGgwLmNvbS9uaWNrbmFtZSIgTmFtZUZvcm1hdD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmF0dHJuYW1lLWZvcm1hdDp1cmkiPjxzYW1sOkF0dHJpYnV0ZVZhbHVlIHhzaTp0eXBlPSJ4czpzdHJpbmciPnVzZXIwMTwvc2FtbDpBdHRyaWJ1dGVWYWx1ZT48L3NhbWw6QXR0cmlidXRlPjxzYW1sOkF0dHJpYnV0ZSBOYW1lPSJodHRwOi8vc2NoZW1hcy5hdXRoMC5jb20vcGljdHVyZSIgTmFtZUZvcm1hdD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmF0dHJuYW1lLWZvcm1hdDp1cmkiPjxzYW1sOkF0dHJpYnV0ZVZhbHVlIHhzaTp0eXBlPSJ4czpzdHJpbmciPmh0dHBzOi8vcy5ncmF2YXRhci5jb20vYXZhdGFyL2NjYzQ5ZjRkNThiMDQyOGIwZmFjZDc4YzNiODk4YmZhP3M9NDgwJmFtcDtyPXBnJmFtcDtkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZ1cy5wbmc8L3NhbWw6QXR0cmlidXRlVmFsdWU+PC9zYW1sOkF0dHJpYnV0ZT48c2FtbDpBdHRyaWJ1dGUgTmFtZT0iaHR0cDovL3NjaGVtYXMuYXV0aDAuY29tL3VwZGF0ZWRfYXQiIE5hbWVGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphdHRybmFtZS1mb3JtYXQ6dXJpIj48c2FtbDpBdHRyaWJ1dGVWYWx1ZSB4c2k6dHlwZT0ieHM6YW55VHlwZSI+V2VkIEF1ZyAxMiAyMDIwIDE3OjU2OjU3IEdNVCswMDAwIChDb29yZGluYXRlZCBVbml2ZXJzYWwgVGltZSk8L3NhbWw6QXR0cmlidXRlVmFsdWU+PC9zYW1sOkF0dHJpYnV0ZT48c2FtbDpBdHRyaWJ1dGUgTmFtZT0iaHR0cDovL3NjaGVtYXMuYXV0aDAuY29tL3VzZXJfaWQiIE5hbWVGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphdHRybmFtZS1mb3JtYXQ6dXJpIj48c2FtbDpBdHRyaWJ1dGVWYWx1ZSB4c2k6dHlwZT0ieHM6c3RyaW5nIj5hdXRoMHw1ZjMyOWI0ZjczZWRjMTAwM2Q1ZjVkNzM8L3NhbWw6QXR0cmlidXRlVmFsdWU+PC9zYW1sOkF0dHJpYnV0ZT48c2FtbDpBdHRyaWJ1dGUgTmFtZT0iaHR0cDovL3NjaGVtYXMuYXV0aDAuY29tL2lkZW50aWZpZXIiIE5hbWVGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDphdHRybmFtZS1mb3JtYXQ6dXJpIj48c2FtbDpBdHRyaWJ1dGVWYWx1ZSB4c2k6dHlwZT0ieHM6c3RyaW5nIj5hdXRoMHw1ZjMyOWI0ZjczZWRjMTAwM2Q1ZjVkNzM8L3NhbWw6QXR0cmlidXRlVmFsdWU+PC9zYW1sOkF0dHJpYnV0ZT48L3NhbWw6QXR0cmlidXRlU3RhdGVtZW50Pjwvc2FtbDpBc3NlcnRpb24+PC9zYW1scDpSZXNwb25zZT4=
```

### Decoded SAML response from Auth0

```xml
<samlp:Response xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" ID="_101857e2132cee1fd2a3"  Version="2.0" IssueInstant="2020-08-12T17:56:57.608Z"  Destination="https://manage.auth0.com/tester/samlp">
  <saml:Issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">urn:svc.auth0.com</saml:Issuer>
  <samlp:Status>
    <samlp:StatusCode Value="urn:oasis:names:tc:SAML:2.0:status:Success"/>
  </samlp:Status>
  <saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" Version="2.0" ID="_C73TgUORTRvztJhMCLnBeJoNWVfQAQac" IssueInstant="2020-08-12T17:56:57.600Z">
    <saml:Issuer>urn:svc.auth0.com</saml:Issuer>
    <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
      <SignedInfo>
        <CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
        <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
        <Reference URI="#_C73TgUORTRvztJhMCLnBeJoNWVfQAQac">
          <Transforms>
            <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
            <Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
          </Transforms>
          <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
          <DigestValue>F/Qnx7NvFpvIea04hIz/KmxJCTI=</DigestValue>
        </Reference>
      </SignedInfo>
      <SignatureValue>uA+EwWOgPlE4yVAgI8uo5mNwNn3G59CfeE+ZWJfTvDUrp5sZXyXp5axyKeElSFgX+8rTqa8msMtVrV/WcKjpfijQGPNFOcJ79Net20Mqp6RoRFYoVNXI9fNxnqmCWUXZosXQEDkMI9xdYreGZr4FJ2XFYTxDK22wDElx0RrocsuWSujTscEv76e6eQy/u+rxlvmkih9bACbgT8wTgOUeaNE5awG0HlMw/ij/FAgyfEL/foqjsqWUySVThDlCW8+HEoO3IwpNr992rgayBjN3c79jR8NMEPV3w81btwHTu3dqhLvjOdnoLweafVIxza+sbGhYPx1M1RQBU69eQ/KTsg==</SignatureValue>
      <KeyInfo>
        <X509Data>
          <X509Certificate>MIIC9TCCAd2gAwIBAgIJPLjfS0z/rGkoMA0GCSqGSIb3DQEBCwUAMBgxFjAUBgNVBAMTDXN2Yy5hdXRoMC5jb20wHhcNMTcwOTIxMTMxNTAyWhcNMzEwNTMxMTMxNTAyWjAYMRYwFAYDVQQDEw1zdmMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2uleM9phudzU9KuWgfee9gCpiPM+jGnlydB0rSiXd0DtnerBQX//7i7wRS4jJ3deYgw5Y9IdNLRRgrWuPQedRP4FmwQDdqSkaMRMu3kh5GPxd4f+zLXhGn/4O6n2peAji/CmfxhPQmxoLJSUPyXaXSYC/yuezgsSOB2po67MQAnn8a4Y8z1UcTNnSa1Bblcj90hoDW/gUp+JhWkHTXGxfNncZ0zS+abCGKdMVuGybrRrAG8kQYjrAeodiKz44ehfA3M2kPeZxtaULP816qX+klZihLl9TCWahq/KABraq8VDx54KHOpmeJQ1IG+Tn6vJvCx+ZJPsVUCXWJwKWk48DQIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBSGlZzol6RIFSIDf+9eTyU4KLcZszAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBAKY1LvoayuOxrWfNy1whSfm+o8mUiUD+oEUP7ClEgRa1i14hMP6WZH/WWOlNxKJfGebCeiK4Q9zxrRVonMxvFy6ATDZZZw8XTs57iZaWfkBXxZaxcVi54uSRS5OFdUMmHV5wakMXeMkdqxgLVlqCoAYNJoVeJReO7uZuDI6CDthxDTsEruFpJg3+vIS3UMFxTVh7jyNQCln5Aah6RAThoj3w+P0LQB9xb0/WVAYExnkRLTRAu1vJp3r07gt1PIOi1hN6uXYHoXOdV6kOD6YY535MfoApU3TOTAnj/RnraV/Ka0DJuaVatSdhjcOU65FTqLZ7AnUIPBwDx0cQtjt1O1k=</X509Certificate>
        </X509Data>
      </KeyInfo>
    </Signature>
    <saml:Subject>
      <saml:NameID Format="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent">auth0|5f329b4f73edc1003d5f5d73</saml:NameID>
      <saml:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">
        <saml:SubjectConfirmationData NotOnOrAfter="2020-08-12T18:56:57.600Z" Recipient="https://manage.auth0.com/tester/samlp"/>
      </saml:SubjectConfirmation>
    </saml:Subject>
    <saml:Conditions NotBefore="2020-08-12T17:56:57.600Z" NotOnOrAfter="2020-08-12T18:56:57.600Z">
      <saml:AudienceRestriction>
        <saml:Audience>urn:amazon:cognito:sp:us-east-1_QUSNXWsxL</saml:Audience>
      </saml:AudienceRestriction>
    </saml:Conditions>
    <saml:AuthnStatement AuthnInstant="2020-08-12T17:56:57.600Z" SessionIndex="_CqOmTUbS2EPBudIjs52uf7OVqBrdTpqP">
      <saml:AuthnContext>
        <saml:AuthnContextClassRef>urn:oasis:names:tc:SAML:2.0:ac:classes:unspecified</saml:AuthnContextClassRef>
      </saml:AuthnContext>
    </saml:AuthnStatement>
    <saml:AttributeStatement xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <saml:Attribute Name="http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:string">user01@example.com</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:string">user01@example.com</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/identities/default/user_id" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:string">5f329b4f73edc1003d5f5d73</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/identities/default/provider" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:string">auth0</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/identities/default/connection" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:string">Username-Password-Authentication</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/identities/default/isSocial" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:boolean">false</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/clientID" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:string">0x3e4zVFCnvHwF7UGT2GZYUHgA0Y6tJo</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/created_at" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:anyType">Tue Aug 11 2020 13:21:19 GMT+0000 (Coordinated Universal Time)</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/email_verified" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:boolean">true</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/name" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:string">user01@example.com</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/nickname" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:string">user01</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/picture" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:string">https://s.gravatar.com/avatar/ccc49f4d58b0428b0facd78c3b898bfa?s=480&amp;r=pg&amp;d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fus.png</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/updated_at" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:anyType">Wed Aug 12 2020 17:56:57 GMT+0000 (Coordinated Universal Time)</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/user_id" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:string">auth0|5f329b4f73edc1003d5f5d73</saml:AttributeValue>
      </saml:Attribute>
      <saml:Attribute Name="http://schemas.auth0.com/identifier" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:string">auth0|5f329b4f73edc1003d5f5d73</saml:AttributeValue>
      </saml:Attribute>
    </saml:AttributeStatement>
  </saml:Assertion>
</samlp:Response>
```

---

## TODO

* store id_token and refresh_token in local storage.  delete on logout
* add standard set of cw alarms for 4xx and 5xx thresholds.  make thresholds configurable via cfn params.  create cw dashboard from these.
* add architecture diagram to README.md
* remove `IncludeBody: true` from template.yaml
* package as Serverless Application Repository 
* package as [AWS Service Catalog](https://aws.amazon.com/servicecatalog/) product using CloudFormation.  See [AWS CloudFormation support for AWS Service Catalog products | AWS Management & Governance Blog](https://aws.amazon.com/blogs/mt/how-to-launch-secure-and-governed-aws-resources-with-aws-cloudformation-and-aws-service-catalog/)

## Completed

* ~~cognito federated sso to auth0 saml2. see [Set up Auth0 as a SAML Identity Provider with an Amazon Cognito User Pool](https://aws.amazon.com/premiumsupport/knowledge-center/auth0-saml-cognito-user-pool/)~~
* ~~configure CloudFront Error pages to redirect to cognito login URL~~
* ~~move `LambdaEdgeLoginFunction` out of template to individual directory and use SAM to deploy~~
* ~~DecodeVerifyJwtFunction is split into its own lambda due to lambda@edge code size constraints~~
* ~~customize cognito login hosted ui.  remove signup, etc.~~
* ~~`create-react-app`~~
* ~~add "logout" link that removes cloudfront signed cookies.  must do from server-side as client-side javascript can't access the cookies.  see [Correct way to delete cookies server-side](https://stackoverflow.com/questions/5285940/correct-way-to-delete-cookies-server-side#answer-53573622)~~
* ~~`src/lambda/login/index.js` - get `${DomainName}`, `DecodeVerifyJwtFunctionName`, `UserPoolClientId`, and CloudFront Key Pair Secrets paths from param store~~
* ~~remove unused secrets manager secrets~~
* ~~fix for `allthecloudbits.com/login/auth/`~~
  * ~~for  `/login/auth/` send 200 in response with html meta refresh/redirect tag to root / instead of 302. <head><meta http-equiv="refresh" content=1;url="<?=$url?>"></head>~~



---

## Resources

**Articles**

* [Node.js — Serve Private Content using AWS CloudFront](https://gosink.in/node-js-serve-private-content-using-aws-cloudfront/)
* [Serving Private Content Using Amazon CloudFront & AWS Lambda@Edge](https://aws.amazon.com/blogs/networking-and-content-delivery/serving-private-content-using-amazon-cloudfront-aws-lambdaedge/)
* [Authorization@Edge using cookies: Protect your Amazon CloudFront content from being downloaded by unauthenticated users](https://aws.amazon.com/blogs/networking-and-content-delivery/authorizationedge-using-cookies-protect-your-amazon-cloudfront-content-from-being-downloaded-by-unauthenticated-users/)
* [Authorization@Edge – How to Use Lambda@Edge and JSON Web Tokens to Enhance Web Application Security](https://aws.amazon.com/blogs/networking-and-content-delivery/authorizationedge-how-to-use-lambdaedge-and-json-web-tokens-to-enhance-web-application-security/)
* [Private static websites on S3 cheat sheet](https://stuartsandine.com/private-static-websites-on-s3/)
* [Can I host a static website on a private Amazon S3 bucket and then serve the website using CloudFront?](https://aws.amazon.com/premiumsupport/knowledge-center/s3-cloudfront-website-access/)
* [r/AWS | Access S3 static website from Intranet](https://www.reddit.com/r/aws/comments/bt6dlv/access_s3_static_website_from_intranet/)
* [How to use AWS.CloudFront.Signer in Lambda function](https://stackoverflow.com/questions/38305980/how-to-use-aws-cloudfront-signer-in-lambda-function)
* [How to Monitor Amazon CloudFront with CloudWatch](https://www.bluematador.com/blog/how-to-monitor-amazon-cloudfront-with-cloudwatch)


**Documentation**

* [AWS | Documentation | CloudFront | Overview of Serving Private Content](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-overview.html)
* [CloudFront | Using Signed Cookies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-signed-cookies.html)
* [Specifying the AWS Accounts That Can Create Signed URLs and Signed Cookies (Trusted Signers) - Amazon CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-trusted-signers.html)
* [Class: AWS.CloudFront.Signer | AWS SDK for JavaScript](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/CloudFront/Signer.html) - support for generating signed URLs and Cookies in node/js/ts

**Code**

* [aws-samples/cloudfront-authorization-at-edge](https://github.com/aws-samples/cloudfront-authorization-at-edge)
* [CloudFront Signed Cookies Keeping Session State for API Gateway Access](https://stackoverflow.com/questions/45250493/cloudfront-signed-cookies-keeping-session-state-for-api-gateway-access)
* [h-arora/aws-cloudfront-cookie-signer](https://github.com/h-arora/aws-cloudfront-cookie-signer)
* [pfeilbr/azure-pipelines-playground](https://github.com/pfeilbr/azure-pipelines-playground) - specifically CloudFormation template @ [azure-pipelines-playground/cfn-templates/resources.yaml](https://github.com/pfeilbr/azure-pipelines-playground/blob/master/cfn-templates/resources.yaml)
* [pfeilbr/aws-cognito-playground](https://github.com/pfeilbr/aws-cognito-playground)
* [pfeilbr/cognito-federated-to-salesforce-and-s3-presigned-url-playground](https://github.com/pfeilbr/cognito-federated-to-salesforce-and-s3-presigned-url-playground)


---

## Scratch

```sh

```






