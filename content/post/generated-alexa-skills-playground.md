+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2018-05-17
description = ""
summary = "experimenting with Alexa Skills"
draft = false
slug = "alexa-skills"
tags = ["playground",]
title = "Alexa Skills"
repoFullName = "pfeilbr/alexa-skills-playground"
repoHTMLURL = "https://github.com/pfeilbr/alexa-skills-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/alexa-skills-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/alexa-skills-playground</a>
-->


## [sage](skills/sage) skill

data driven skill.  modify `config.js` then deploy

> NOTE: `skills/sage/lambda/custom/config.js` is generated.  do not edit directly!

```sh
# build
cd skills/sage/lambda/custom
npm install

# deploy
cd skills/sage
npm run deploy
```

* `npm build` generates `models/en-US.json` and `lambda/custom/config.js`
* `scripts/run` performs file generation

---

## Development Workflow

```sh
# configure ask cli
ask init

# create new skill
ask new

# clone an existing skill
ask clone --skill-id amzn1.ask.skill.1aee9e3d-ec1c-4e07-8239-19fea42c3036

# deploy
ask deploy
```

---

## Payload Examples

LaunchRequest Payload Example (simplified)

```json
{
    "type": "LaunchRequest",
    "requestId": "amzn1.echo-api.request.310bdf96-793a-4e14-b586-e8f680ffe52f",
    "timestamp": "2018-05-15T17:32:42Z",
    "locale": "en-US",
    "shouldLinkResultBeReturned": false
}
```

LaunchRequest Payload Example (full)

```json
{
    "requestEnvelope": {
        "version": "1.0",
        "session": {
            "new": true,
            "sessionId": "amzn1.echo-api.session.314b8ce7-06d6-4cd5-8822-7644d2f5a799",
            "application": {
                "applicationId": "amzn1.ask.skill.1aee9e3d-ec1c-4e07-8239-19fea42c3036"
            },
            "user": {
                "userId": "amzn1.ask.account.AFPKUMM66XYI7MZMSUYLSGUUJDILTGYDXEMEL2WFFLEIG2TIQIE3NSIDODHS7VW2UKCA4EYR2QQS6QDZA5FAKMIQI5ASRRAEEXMNFMF6KSYQYM6YSVZ4UGU52L3SMJ3T73LOQPSFYBTIUQRPBLOFFQPEGIW35AP2FMQP5IP55QR4M6LZ2RGEEHNORLF6GWJOD3VSZIQGNLIC4MI"
            }
        },
        "context": {
            "AudioPlayer": {
                "playerActivity": "IDLE"
            },
            "Display": {
                "token": ""
            },
            "System": {
                "application": {
                    "applicationId": "amzn1.ask.skill.1aee9e3d-ec1c-4e07-8239-19fea42c3036"
                },
                "user": {
                    "userId": "amzn1.ask.account.AFPKUMM66XYI7MZMSUYLSGUUJDILTGYDXEMEL2WFFLEIG2TIQIE3NSIDODHS7VW2UKCA4EYR2QQS6QDZA5FAKMIQI5ASRRAEEXMNFMF6KSYQYM6YSVZ4UGU52L3SMJ3T73LOQPSFYBTIUQRPBLOFFQPEGIW35AP2FMQP5IP55QR4M6LZ2RGEEHNORLF6GWJOD3VSZIQGNLIC4MI"
                },
                "device": {
                    "deviceId": "amzn1.ask.device.AEOU6OLEMMGRPZDLADWRH5FELI7QBDGR4XXXM2EGU53EJQWESEUGNQF7WZKY3SUJFR2SFLQ7DB2KUJ4QAXTYH2DJGWR3K36SPOIGNFVPTFHPHN34LBW234VMAU5IM5PJUFYCAI3QHPTUBAXZT6VIBPFBMXXX3BLQFNRO3IJ6WFVXBPDFAKRP6",
                    "supportedInterfaces": {
                        "AudioPlayer": {},
                        "Display": {
                            "templateVersion": "1.0",
                            "markupVersion": "1.0"
                        }
                    }
                },
                "apiEndpoint": "https://api.amazonalexa.com",
                "apiAccessToken": "<REMOVED>"
            }
        },
        "request": {
            "type": "LaunchRequest",
            "requestId": "amzn1.echo-api.request.310bdf96-793a-4e14-b586-e8f680ffe52f",
            "timestamp": "2018-05-15T17:32:42Z",
            "locale": "en-US",
            "shouldLinkResultBeReturned": false
        }
    },
    "context": {
        "callbackWaitsForEmptyEventLoop": true,
        "logGroupName": "/aws/lambda/aws-serverless-repository-alexaskillskitnodejsfact-6CKGX2O4QCIR",
        "logStreamName": "2018/05/15/[$LATEST]239394be80f1496387bc6961cede7161",
        "functionName": "aws-serverless-repository-alexaskillskitnodejsfact-6CKGX2O4QCIR",
        "memoryLimitInMB": "128",
        "functionVersion": "$LATEST",
        "invokeid": "f8d0e1c0-5865-11e8-9638-0df1b13913aa",
        "awsRequestId": "f8d0e1c0-5865-11e8-9638-0df1b13913aa",
        "invokedFunctionArn": "arn:aws:lambda:us-east-1:529276214230:function:aws-serverless-repository-alexaskillskitnodejsfact-6CKGX2O4QCIR"
    },
    "attributesManager": {},
    "responseBuilder": {},
    "serviceClientFactory": {
        "apiConfiguration": {
            "apiClient": {},
            "apiEndpoint": "https://api.amazonalexa.com",
            "authorizationValue": "<REMOVED>"
        }
    }
}
```

---

IntentRequest Payload Example (simplified)

```json
{
    "type": "IntentRequest",
    "requestId": "amzn1.echo-api.request.7bfbb240-78c3-4622-b255-53a8dcc34376",
    "timestamp": "2018-05-15T17:34:12Z",
    "locale": "en-US",
    "intent": {
        "name": "GetNewFactIntent",
        "confirmationStatus": "NONE"
    }
}
```

IntentRequest Payload Example (full)

```json
{
    "requestEnvelope": {
        "version": "1.0",
        "session": {
            "new": true,
            "sessionId": "amzn1.echo-api.session.204f5c22-869d-406e-bd59-9d866477cfcc",
            "application": {
                "applicationId": "amzn1.ask.skill.1aee9e3d-ec1c-4e07-8239-19fea42c3036"
            },
            "user": {
                "userId": "amzn1.ask.account.AFPKUMM66XYI7MZMSUYLSGUUJDILTGYDXEMEL2WFFLEIG2TIQIE3NSIDODHS7VW2UKCA4EYR2QQS6QDZA5FAKMIQI5ASRRAEEXMNFMF6KSYQYM6YSVZ4UGU52L3SMJ3T73LOQPSFYBTIUQRPBLOFFQPEGIW35AP2FMQP5IP55QR4M6LZ2RGEEHNORLF6GWJOD3VSZIQGNLIC4MI"
            }
        },
        "context": {
            "AudioPlayer": {
                "playerActivity": "IDLE"
            },
            "Display": {
                "token": ""
            },
            "System": {
                "application": {
                    "applicationId": "amzn1.ask.skill.1aee9e3d-ec1c-4e07-8239-19fea42c3036"
                },
                "user": {
                    "userId": "amzn1.ask.account.AFPKUMM66XYI7MZMSUYLSGUUJDILTGYDXEMEL2WFFLEIG2TIQIE3NSIDODHS7VW2UKCA4EYR2QQS6QDZA5FAKMIQI5ASRRAEEXMNFMF6KSYQYM6YSVZ4UGU52L3SMJ3T73LOQPSFYBTIUQRPBLOFFQPEGIW35AP2FMQP5IP55QR4M6LZ2RGEEHNORLF6GWJOD3VSZIQGNLIC4MI"
                },
                "device": {
                    "deviceId": "amzn1.ask.device.AEOU6OLEMMGRPZDLADWRH5FELI7QBDGR4XXXM2EGU53EJQWESEUGNQF7WZKY3SUJFR2SFLQ7DB2KUJ4QAXTYH2DJGWR3K36SPOIGNFVPTFHPHN34LBW234VMAU5IM5PJUFYCAI3QHPTUBAXZT6VIBPFBMXXX3BLQFNRO3IJ6WFVXBPDFAKRP6",
                    "supportedInterfaces": {
                        "AudioPlayer": {},
                        "Display": {
                            "templateVersion": "1.0",
                            "markupVersion": "1.0"
                        }
                    }
                },
                "apiEndpoint": "https://api.amazonalexa.com",
                "apiAccessToken": "<REMOVED>"
            }
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "amzn1.echo-api.request.7bfbb240-78c3-4622-b255-53a8dcc34376",
            "timestamp": "2018-05-15T17:34:12Z",
            "locale": "en-US",
            "intent": {
                "name": "GetNewFactIntent",
                "confirmationStatus": "NONE"
            }
        }
    },
    "context": {
        "callbackWaitsForEmptyEventLoop": true,
        "logGroupName": "/aws/lambda/aws-serverless-repository-alexaskillskitnodejsfact-6CKGX2O4QCIR",
        "logStreamName": "2018/05/15/[$LATEST]239394be80f1496387bc6961cede7161",
        "functionName": "aws-serverless-repository-alexaskillskitnodejsfact-6CKGX2O4QCIR",
        "memoryLimitInMB": "128",
        "functionVersion": "$LATEST",
        "invokeid": "2e99cd8c-5866-11e8-ac6c-091c252114f4",
        "awsRequestId": "2e99cd8c-5866-11e8-ac6c-091c252114f4",
        "invokedFunctionArn": "arn:aws:lambda:us-east-1:529276214230:function:aws-serverless-repository-alexaskillskitnodejsfact-6CKGX2O4QCIR"
    },
    "attributesManager": {},
    "responseBuilder": {},
    "serviceClientFactory": {
        "apiConfiguration": {
            "apiClient": {},
            "apiEndpoint": "https://api.amazonalexa.com",
            "authorizationValue": "<REMOVED>"
        }
    }
}
```


