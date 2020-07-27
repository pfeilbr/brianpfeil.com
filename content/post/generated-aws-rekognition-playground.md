+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-07-08
description = ""
summary = "learning AWS Rekognition"
draft = false
slug = "aws-rekognition"
tags = ["aws","github",]
title = "AWS Rekognition"
repoFullName = "pfeilbr/aws-rekognition-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-rekognition-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/aws-rekognition-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-rekognition-playground</a>
-->


learn [AWS Rekognition](https://docs.aws.amazon.com/rekognition/)

see [`src/examples.js`](src/examples.js)

## Prerequisites

* [AWS default credentials](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html) available to call Rekognition API
* install imagemagick, graphicsmagick, and ghostscript (for fonts) for labelling image

    ```sh
    brew install imagemagick
    brew install graphicsmagick
    brew install ghostscript
    ```

## Example Labelled Image Using [`detectLabels`](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/Rekognition.html#detectLabels-property) API

**Source**
![](assets/images/city-street.jpg)

**Labelled**
![](assets/images/city-street.jpg-labelled.jpg)


## Example Labelled Image Using [`detectText`](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/Rekognition.html#detectText-property) API

**Source**
![](assets/images/book-cover.jpg)

**Labelled**
![](assets/images/book-cover.jpg-labelled.jpg)


## Running

```sh
npm install
npm start
```

---

## Video Label Detection Example via CLI

```sh
# start (it's async)
aws rekognition start-label-detection --video "S3Object={Bucket=rekognition-playground,Name=SampleVideo_1280x720_1mb.mp4}"

# output
{
    "JobId": "2c9b387607977af21c0839f177bf7034ce1bcd5139810b533dea3deb6361f348"
}

# in progress
aws rekognition get-label-detection  --job-id "2c9b387607977af21c0839f177bf7034ce1bcd5139810b533dea3deb6361f348"

# output
{
    "Labels": [],
    "LabelModelVersion": "2.0",
    "JobStatus": "IN_PROGRESS"
}

# completed
aws rekognition get-label-detection  --job-id "2c9b387607977af21c0839f177bf7034ce1bcd5139810b533dea3deb6361f348"

# output
{
    "Labels": [
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 89.929931640625, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 69.0970458984375, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Rodent"
                    }
                ], 
                "Name": "Bunny"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 51.81949234008789, 
                "Parents": [
                    {
                        "Name": "Wildlife"
                    }, 
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Deer"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 83.59092712402344, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 50.83674621582031, 
                "Parents": [], 
                "Name": "Green"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 83.93998718261719, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.92662048339844, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Moss"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 63.28266906738281, 
                "Parents": [], 
                "Name": "Outdoors"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 60.88518524169922, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Pet"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 90.28629302978516, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 69.0970458984375, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Rodent"
                    }
                ], 
                "Name": "Rabbit"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 69.0970458984375, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Rodent"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 71.99913787841797, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Tree"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 82.74295806884766, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Vegetation"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 58.27427291870117, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Wildlife"
            }
        }, 
        {
            "Timestamp": 0, 
            "Label": {
                "Instances": [], 
                "Confidence": 67.73959350585938, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 91.4648666381836, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 52.55938720703125, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Rodent"
                    }
                ], 
                "Name": "Bunny"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 53.18073654174805, 
                "Parents": [
                    {
                        "Name": "Wildlife"
                    }, 
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Deer"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 81.07315826416016, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 82.8969955444336, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.91206359863281, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Moss"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.965728759765625, 
                "Parents": [], 
                "Name": "Nature"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 68.73519897460938, 
                "Parents": [], 
                "Name": "Outdoors"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.99771499633789, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Pet"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 89.0054931640625, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 52.55938720703125, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Rodent"
                    }
                ], 
                "Name": "Rabbit"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 61.68227767944336, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Rodent"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 74.91455078125, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Tree"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 82.96375274658203, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Vegetation"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 60.77254104614258, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Wildlife"
            }
        }, 
        {
            "Timestamp": 200, 
            "Label": {
                "Instances": [], 
                "Confidence": 74.65026092529297, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.01680755615234, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 59.57973098754883, 
                "Parents": [
                    {
                        "Name": "Wildlife"
                    }, 
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Deer"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 78.3232650756836, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 83.4029541015625, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 52.54331588745117, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Moss"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 60.17965316772461, 
                "Parents": [], 
                "Name": "Nature"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 69.8688735961914, 
                "Parents": [], 
                "Name": "Outdoors"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 87.0956802368164, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.15915298461914, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Rodent"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 74.54655456542969, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Tree"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 80.760009765625, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Vegetation"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 65.61725616455078, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Wildlife"
            }
        }, 
        {
            "Timestamp": 400, 
            "Label": {
                "Instances": [], 
                "Confidence": 80.25843048095703, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.0205078125, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.57878875732422, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Wildlife"
                    }
                ], 
                "Name": "Deer"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 74.01980590820312, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 82.74808502197266, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 51.89423751831055, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Moss"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.12575149536133, 
                "Parents": [], 
                "Name": "Nature"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 66.46729278564453, 
                "Parents": [], 
                "Name": "Outdoors"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 83.74144744873047, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.528724670410156, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Rodent"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 69.28874206542969, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Tree"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 74.46104431152344, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Vegetation"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 61.98466873168945, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Wildlife"
            }
        }, 
        {
            "Timestamp": 600, 
            "Label": {
                "Instances": [], 
                "Confidence": 85.43339538574219, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.25353240966797, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 52.10648727416992, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Wildlife"
                    }
                ], 
                "Name": "Deer"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 75.25298309326172, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.252071380615234, 
                "Parents": [
                    {
                        "Name": "Nature"
                    }, 
                    {
                        "Name": "Outdoors"
                    }
                ], 
                "Name": "Land"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 83.48870086669922, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.91990280151367, 
                "Parents": [], 
                "Name": "Nature"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 63.378013610839844, 
                "Parents": [], 
                "Name": "Outdoors"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 82.87625885009766, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.5538330078125, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Rodent"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 65.29582977294922, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Tree"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 70.30518341064453, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Vegetation"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.97867965698242, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Wildlife"
            }
        }, 
        {
            "Timestamp": 800, 
            "Label": {
                "Instances": [], 
                "Confidence": 90.27912139892578, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 1000, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.98469543457031, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 1000, 
            "Label": {
                "Instances": [], 
                "Confidence": 76.76435089111328, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 1000, 
            "Label": {
                "Instances": [], 
                "Confidence": 84.5231704711914, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 1000, 
            "Label": {
                "Instances": [], 
                "Confidence": 62.500648498535156, 
                "Parents": [], 
                "Name": "Outdoors"
            }
        }, 
        {
            "Timestamp": 1000, 
            "Label": {
                "Instances": [], 
                "Confidence": 83.34005737304688, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 1000, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.20842361450195, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Rodent"
            }
        }, 
        {
            "Timestamp": 1000, 
            "Label": {
                "Instances": [], 
                "Confidence": 64.69285583496094, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Tree"
            }
        }, 
        {
            "Timestamp": 1000, 
            "Label": {
                "Instances": [], 
                "Confidence": 71.41803741455078, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Vegetation"
            }
        }, 
        {
            "Timestamp": 1000, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.289005279541016, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Wildlife"
            }
        }, 
        {
            "Timestamp": 1000, 
            "Label": {
                "Instances": [], 
                "Confidence": 90.80029296875, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 1200, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.2735366821289, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 1200, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.429866790771484, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Rodent"
                    }
                ], 
                "Name": "Bunny"
            }
        }, 
        {
            "Timestamp": 1200, 
            "Label": {
                "Instances": [], 
                "Confidence": 79.42290496826172, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 1200, 
            "Label": {
                "Instances": [], 
                "Confidence": 84.56671905517578, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 1200, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.960243225097656, 
                "Parents": [], 
                "Name": "Outdoors"
            }
        }, 
        {
            "Timestamp": 1200, 
            "Label": {
                "Instances": [], 
                "Confidence": 83.51371002197266, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 1200, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.429866790771484, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Rodent"
                    }
                ], 
                "Name": "Rabbit"
            }
        }, 
        {
            "Timestamp": 1200, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.429866790771484, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Rodent"
            }
        }, 
        {
            "Timestamp": 1200, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.99834060668945, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Tree"
            }
        }, 
        {
            "Timestamp": 1200, 
            "Label": {
                "Instances": [], 
                "Confidence": 68.27635192871094, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Vegetation"
            }
        }, 
        {
            "Timestamp": 1200, 
            "Label": {
                "Instances": [], 
                "Confidence": 89.07957458496094, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 91.85724639892578, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.245033264160156, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.461219787597656, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Rodent"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bunny"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 80.37769317626953, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 51.644439697265625, 
                "Parents": [], 
                "Name": "Green"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 81.59090423583984, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 50.62571716308594, 
                "Parents": [], 
                "Name": "Outdoors"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 51.50884246826172, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Pet"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 83.59095764160156, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.461219787597656, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Rodent"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Rabbit"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.461219787597656, 
                "Parents": [
                    {
                        "Name": "Mammal"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Rodent"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 52.90790939331055, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Tree"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 69.43914031982422, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Vegetation"
            }
        }, 
        {
            "Timestamp": 1400, 
            "Label": {
                "Instances": [], 
                "Confidence": 85.9814453125, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 1600, 
            "Label": {
                "Instances": [], 
                "Confidence": 92.43132019042969, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 1600, 
            "Label": {
                "Instances": [], 
                "Confidence": 64.58529663085938, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 1600, 
            "Label": {
                "Instances": [], 
                "Confidence": 77.15897369384766, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 1600, 
            "Label": {
                "Instances": [], 
                "Confidence": 72.95342254638672, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 1600, 
            "Label": {
                "Instances": [], 
                "Confidence": 52.87014389038086, 
                "Parents": [], 
                "Name": "Outdoors"
            }
        }, 
        {
            "Timestamp": 1600, 
            "Label": {
                "Instances": [], 
                "Confidence": 50.35053634643555, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Pet"
            }
        }, 
        {
            "Timestamp": 1600, 
            "Label": {
                "Instances": [], 
                "Confidence": 78.85031127929688, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 1600, 
            "Label": {
                "Instances": [], 
                "Confidence": 52.71328353881836, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Tree"
            }
        }, 
        {
            "Timestamp": 1600, 
            "Label": {
                "Instances": [], 
                "Confidence": 67.42894744873047, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Vegetation"
            }
        }, 
        {
            "Timestamp": 1600, 
            "Label": {
                "Instances": [], 
                "Confidence": 86.85175323486328, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 1800, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.09008026123047, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 1800, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.34907206892967224, 
                            "Top": 0.08466745913028717, 
                            "Left": 0.18098066747188568, 
                            "Height": 0.7858670353889465
                        }, 
                        "Confidence": 87.56869506835938
                    }
                ], 
                "Confidence": 76.05467224121094, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 1800, 
            "Label": {
                "Instances": [], 
                "Confidence": 70.30843353271484, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 1800, 
            "Label": {
                "Instances": [], 
                "Confidence": 62.480037689208984, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 1800, 
            "Label": {
                "Instances": [], 
                "Confidence": 72.11174774169922, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 1800, 
            "Label": {
                "Instances": [], 
                "Confidence": 57.063655853271484, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Vegetation"
            }
        }, 
        {
            "Timestamp": 1800, 
            "Label": {
                "Instances": [], 
                "Confidence": 89.28423309326172, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 2000, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.03936004638672, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 2000, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.733070373535156, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Beak"
            }
        }, 
        {
            "Timestamp": 2000, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.358623743057251, 
                            "Top": 0.051293861120939255, 
                            "Left": 0.1617140769958496, 
                            "Height": 0.8379018306732178
                        }, 
                        "Confidence": 92.25386810302734
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.7171964049339294, 
                            "Top": 0.07636002451181412, 
                            "Left": 0.18950828909873962, 
                            "Height": 0.8369417190551758
                        }, 
                        "Confidence": 79.23548889160156
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.27733245491981506, 
                            "Top": 0.002237256383523345, 
                            "Left": 0.0026457428466528654, 
                            "Height": 0.359114408493042
                        }, 
                        "Confidence": 69.28044128417969
                    }
                ], 
                "Confidence": 87.71780395507812, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 2000, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.62752914428711, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 2000, 
            "Label": {
                "Instances": [], 
                "Confidence": 52.03357696533203, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 2000, 
            "Label": {
                "Instances": [], 
                "Confidence": 62.13314437866211, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 2000, 
            "Label": {
                "Instances": [], 
                "Confidence": 59.2055778503418, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 2000, 
            "Label": {
                "Instances": [], 
                "Confidence": 82.38220977783203, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 2200, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.34841918945312, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 2200, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.2954216003418, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Beak"
            }
        }, 
        {
            "Timestamp": 2200, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.35335078835487366, 
                            "Top": 0.05790714547038078, 
                            "Left": 0.15636315941810608, 
                            "Height": 0.8401352167129517
                        }, 
                        "Confidence": 93.80805206298828
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.7027698755264282, 
                            "Top": 0.06268657743930817, 
                            "Left": 0.22604236006736755, 
                            "Height": 0.8820430040359497
                        }, 
                        "Confidence": 79.38104248046875
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.12301671504974365, 
                            "Top": 0.08307760953903198, 
                            "Left": 0.0, 
                            "Height": 0.2910917401313782
                        }, 
                        "Confidence": 67.13511657714844
                    }
                ], 
                "Confidence": 92.72528076171875, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 2200, 
            "Label": {
                "Instances": [], 
                "Confidence": 71.46737670898438, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 2200, 
            "Label": {
                "Instances": [], 
                "Confidence": 51.77077865600586, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 2200, 
            "Label": {
                "Instances": [], 
                "Confidence": 82.10325622558594, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 2400, 
            "Label": {
                "Instances": [], 
                "Confidence": 94.62578582763672, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 2400, 
            "Label": {
                "Instances": [], 
                "Confidence": 60.21943664550781, 
                "Parents": [
                    {
                        "Name": "Bird"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Beak"
            }
        }, 
        {
            "Timestamp": 2400, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.35887837409973145, 
                            "Top": 0.06843113154172897, 
                            "Left": 0.14393199980258942, 
                            "Height": 0.8300164341926575
                        }, 
                        "Confidence": 95.54167938232422
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.6892942190170288, 
                            "Top": 0.08313678950071335, 
                            "Left": 0.2348754107952118, 
                            "Height": 0.8645190596580505
                        }, 
                        "Confidence": 73.23546600341797
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.2922210097312927, 
                            "Top": 0.006060568615794182, 
                            "Left": 0.0026990175247192383, 
                            "Height": 0.3458782136440277
                        }, 
                        "Confidence": 70.34931945800781
                    }
                ], 
                "Confidence": 93.9428482055664, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 2400, 
            "Label": {
                "Instances": [], 
                "Confidence": 73.18048858642578, 
                "Parents": [
                    {
                        "Name": "Bird"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 2400, 
            "Label": {
                "Instances": [], 
                "Confidence": 50.8458366394043, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 2400, 
            "Label": {
                "Instances": [], 
                "Confidence": 84.690673828125, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 2600, 
            "Label": {
                "Instances": [], 
                "Confidence": 94.66659545898438, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 2600, 
            "Label": {
                "Instances": [], 
                "Confidence": 64.99951934814453, 
                "Parents": [
                    {
                        "Name": "Bird"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Beak"
            }
        }, 
        {
            "Timestamp": 2600, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.3687349259853363, 
                            "Top": 0.07353333383798599, 
                            "Left": 0.1337471306324005, 
                            "Height": 0.8266903162002563
                        }, 
                        "Confidence": 94.13199615478516
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.6544439196586609, 
                            "Top": 0.11645308881998062, 
                            "Left": 0.2392454445362091, 
                            "Height": 0.8009392619132996
                        }, 
                        "Confidence": 66.88501739501953
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.27630096673965454, 
                            "Top": 0.0037734773941338062, 
                            "Left": 0.0016699910629540682, 
                            "Height": 0.3773573935031891
                        }, 
                        "Confidence": 59.929168701171875
                    }
                ], 
                "Confidence": 93.93486785888672, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 2600, 
            "Label": {
                "Instances": [], 
                "Confidence": 71.29080200195312, 
                "Parents": [
                    {
                        "Name": "Bird"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 2600, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.107154846191406, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 2600, 
            "Label": {
                "Instances": [], 
                "Confidence": 84.884765625, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 2800, 
            "Label": {
                "Instances": [], 
                "Confidence": 94.47773742675781, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 2800, 
            "Label": {
                "Instances": [], 
                "Confidence": 64.99027252197266, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Beak"
            }
        }, 
        {
            "Timestamp": 2800, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.38219374418258667, 
                            "Top": 0.0916653499007225, 
                            "Left": 0.12020987272262573, 
                            "Height": 0.7875498533248901
                        }, 
                        "Confidence": 93.746337890625
                    }
                ], 
                "Confidence": 93.69722747802734, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 2800, 
            "Label": {
                "Instances": [], 
                "Confidence": 50.03854751586914, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 2800, 
            "Label": {
                "Instances": [], 
                "Confidence": 70.23558044433594, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 2800, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.43981170654297, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 2800, 
            "Label": {
                "Instances": [], 
                "Confidence": 79.4557876586914, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 3000, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.83204650878906, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 3000, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.40727233886719, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Beak"
            }
        }, 
        {
            "Timestamp": 3000, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.3897032141685486, 
                            "Top": 0.08954781293869019, 
                            "Left": 0.11494585126638412, 
                            "Height": 0.7958506941795349
                        }, 
                        "Confidence": 92.31681823730469
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.6983879804611206, 
                            "Top": 0.09777429699897766, 
                            "Left": 0.21733859181404114, 
                            "Height": 0.8366428017616272
                        }, 
                        "Confidence": 70.86040496826172
                    }
                ], 
                "Confidence": 93.1003189086914, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 3000, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.9047966003418, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 3000, 
            "Label": {
                "Instances": [], 
                "Confidence": 64.41144561767578, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 3000, 
            "Label": {
                "Instances": [], 
                "Confidence": 62.5224609375, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 3000, 
            "Label": {
                "Instances": [], 
                "Confidence": 50.769561767578125, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Waterfowl"
            }
        }, 
        {
            "Timestamp": 3000, 
            "Label": {
                "Instances": [], 
                "Confidence": 77.5377426147461, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 3200, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.4638900756836, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 3200, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.41419991850852966, 
                            "Top": 0.0762210413813591, 
                            "Left": 0.10949432849884033, 
                            "Height": 0.8263728022575378
                        }, 
                        "Confidence": 92.80986785888672
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.716448187828064, 
                            "Top": 0.07755652815103531, 
                            "Left": 0.20436832308769226, 
                            "Height": 0.8662547469139099
                        }, 
                        "Confidence": 65.755615234375
                    }
                ], 
                "Confidence": 92.78094482421875, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 3200, 
            "Label": {
                "Instances": [], 
                "Confidence": 62.132137298583984, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 3200, 
            "Label": {
                "Instances": [], 
                "Confidence": 57.85761642456055, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 3200, 
            "Label": {
                "Instances": [], 
                "Confidence": 67.59366607666016, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 3200, 
            "Label": {
                "Instances": [], 
                "Confidence": 53.58717727661133, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Waterfowl"
            }
        }, 
        {
            "Timestamp": 3200, 
            "Label": {
                "Instances": [], 
                "Confidence": 71.5042495727539, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 3400, 
            "Label": {
                "Instances": [], 
                "Confidence": 92.79534912109375, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 3400, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.4154813885688782, 
                            "Top": 0.07800661772489548, 
                            "Left": 0.11423929035663605, 
                            "Height": 0.822206437587738
                        }, 
                        "Confidence": 92.5831298828125
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.7635012865066528, 
                            "Top": 0.10048328340053558, 
                            "Left": 0.1485721319913864, 
                            "Height": 0.832586407661438
                        }, 
                        "Confidence": 64.7535171508789
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.3332541882991791, 
                            "Top": 0.0031649908050894737, 
                            "Left": 0.0, 
                            "Height": 0.39897918701171875
                        }, 
                        "Confidence": 63.40528869628906
                    }
                ], 
                "Confidence": 92.79534912109375, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 3400, 
            "Label": {
                "Instances": [], 
                "Confidence": 61.568965911865234, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 3400, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.528438568115234, 
                "Parents": [
                    {
                        "Name": "Bird"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 3400, 
            "Label": {
                "Instances": [], 
                "Confidence": 64.99581146240234, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 3400, 
            "Label": {
                "Instances": [], 
                "Confidence": 51.52910614013672, 
                "Parents": [], 
                "Name": "Water"
            }
        }, 
        {
            "Timestamp": 3400, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.16550827026367, 
                "Parents": [
                    {
                        "Name": "Bird"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Waterfowl"
            }
        }, 
        {
            "Timestamp": 3400, 
            "Label": {
                "Instances": [], 
                "Confidence": 63.12147903442383, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 3600, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.00226593017578, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 3600, 
            "Label": {
                "Instances": [], 
                "Confidence": 57.59740447998047, 
                "Parents": [
                    {
                        "Name": "Water"
                    }
                ], 
                "Name": "Aquatic"
            }
        }, 
        {
            "Timestamp": 3600, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.39586177468299866, 
                            "Top": 0.09188465774059296, 
                            "Left": 0.11620678752660751, 
                            "Height": 0.8037567138671875
                        }, 
                        "Confidence": 92.49174499511719
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.7152539491653442, 
                            "Top": 0.08323486894369125, 
                            "Left": 0.2065276801586151, 
                            "Height": 0.8613862991333008
                        }, 
                        "Confidence": 63.56003189086914
                    }
                ], 
                "Confidence": 93.00226593017578, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 3600, 
            "Label": {
                "Instances": [], 
                "Confidence": 66.82272338867188, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 3600, 
            "Label": {
                "Instances": [], 
                "Confidence": 52.20016860961914, 
                "Parents": [], 
                "Name": "Legend of Zelda"
            }
        }, 
        {
            "Timestamp": 3600, 
            "Label": {
                "Instances": [], 
                "Confidence": 51.27878952026367, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 3600, 
            "Label": {
                "Instances": [], 
                "Confidence": 68.2894058227539, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 3600, 
            "Label": {
                "Instances": [], 
                "Confidence": 51.18978500366211, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Sea Life"
            }
        }, 
        {
            "Timestamp": 3600, 
            "Label": {
                "Instances": [], 
                "Confidence": 59.10639572143555, 
                "Parents": [], 
                "Name": "Water"
            }
        }, 
        {
            "Timestamp": 3600, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.734310150146484, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Waterfowl"
            }
        }, 
        {
            "Timestamp": 3600, 
            "Label": {
                "Instances": [], 
                "Confidence": 58.78702926635742, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 3800, 
            "Label": {
                "Instances": [], 
                "Confidence": 94.29412078857422, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 3800, 
            "Label": {
                "Instances": [], 
                "Confidence": 61.6994514465332, 
                "Parents": [
                    {
                        "Name": "Water"
                    }
                ], 
                "Name": "Aquatic"
            }
        }, 
        {
            "Timestamp": 3800, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.3951866924762726, 
                            "Top": 0.11749797314405441, 
                            "Left": 0.11840298026800156, 
                            "Height": 0.7652148604393005
                        }, 
                        "Confidence": 93.82617950439453
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.7300499081611633, 
                            "Top": 0.08484145253896713, 
                            "Left": 0.19536180794239044, 
                            "Height": 0.8607867956161499
                        }, 
                        "Confidence": 70.83800506591797
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.33079493045806885, 
                            "Top": 0.004325739573687315, 
                            "Left": 0.0, 
                            "Height": 0.3973473012447357
                        }, 
                        "Confidence": 60.03199005126953
                    }
                ], 
                "Confidence": 89.16603088378906, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 3800, 
            "Label": {
                "Instances": [], 
                "Confidence": 68.32997131347656, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 3800, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.55190658569336, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 3800, 
            "Label": {
                "Instances": [], 
                "Confidence": 68.33173370361328, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 3800, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.37184524536133, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Sea Life"
            }
        }, 
        {
            "Timestamp": 3800, 
            "Label": {
                "Instances": [], 
                "Confidence": 63.10999298095703, 
                "Parents": [], 
                "Name": "Water"
            }
        }, 
        {
            "Timestamp": 3800, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.42851257324219, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Waterfowl"
            }
        }, 
        {
            "Timestamp": 3800, 
            "Label": {
                "Instances": [], 
                "Confidence": 66.54654693603516, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 4000, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.92424011230469, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 4000, 
            "Label": {
                "Instances": [], 
                "Confidence": 60.050777435302734, 
                "Parents": [
                    {
                        "Name": "Water"
                    }
                ], 
                "Name": "Aquatic"
            }
        }, 
        {
            "Timestamp": 4000, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.38773655891418457, 
                            "Top": 0.12097299098968506, 
                            "Left": 0.12352852523326874, 
                            "Height": 0.7628968954086304
                        }, 
                        "Confidence": 93.34445190429688
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.7438606023788452, 
                            "Top": 0.11014620214700699, 
                            "Left": 0.15275272727012634, 
                            "Height": 0.8042365312576294
                        }, 
                        "Confidence": 66.38320922851562
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.33265557885169983, 
                            "Top": 0.0027915106620639563, 
                            "Left": 0.0, 
                            "Height": 0.3603067696094513
                        }, 
                        "Confidence": 66.176025390625
                    }
                ], 
                "Confidence": 87.69349670410156, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 4000, 
            "Label": {
                "Instances": [], 
                "Confidence": 65.20291900634766, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 4000, 
            "Label": {
                "Instances": [], 
                "Confidence": 60.93068313598633, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 4000, 
            "Label": {
                "Instances": [], 
                "Confidence": 68.37018585205078, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 4000, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.07685089111328, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Sea Life"
            }
        }, 
        {
            "Timestamp": 4000, 
            "Label": {
                "Instances": [], 
                "Confidence": 60.50196838378906, 
                "Parents": [], 
                "Name": "Water"
            }
        }, 
        {
            "Timestamp": 4000, 
            "Label": {
                "Instances": [], 
                "Confidence": 74.234130859375, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 4200, 
            "Label": {
                "Instances": [], 
                "Confidence": 94.10073852539062, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 4200, 
            "Label": {
                "Instances": [], 
                "Confidence": 63.6142463684082, 
                "Parents": [
                    {
                        "Name": "Water"
                    }
                ], 
                "Name": "Aquatic"
            }
        }, 
        {
            "Timestamp": 4200, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.3899807929992676, 
                            "Top": 0.11104846745729446, 
                            "Left": 0.13585709035396576, 
                            "Height": 0.7780617475509644
                        }, 
                        "Confidence": 69.82188415527344
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.7412311434745789, 
                            "Top": 0.07028910517692566, 
                            "Left": 0.1845070868730545, 
                            "Height": 0.8762639164924622
                        }, 
                        "Confidence": 61.936519622802734
                    }
                ], 
                "Confidence": 86.78479766845703, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 4200, 
            "Label": {
                "Instances": [], 
                "Confidence": 61.21832275390625, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 4200, 
            "Label": {
                "Instances": [], 
                "Confidence": 63.98245620727539, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 4200, 
            "Label": {
                "Instances": [], 
                "Confidence": 50.86898422241211, 
                "Parents": [
                    {
                        "Name": "Bird"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 4200, 
            "Label": {
                "Instances": [], 
                "Confidence": 65.02304077148438, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 4200, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.770111083984375, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Sea Life"
            }
        }, 
        {
            "Timestamp": 4200, 
            "Label": {
                "Instances": [], 
                "Confidence": 63.6142463684082, 
                "Parents": [], 
                "Name": "Water"
            }
        }, 
        {
            "Timestamp": 4200, 
            "Label": {
                "Instances": [], 
                "Confidence": 81.00969696044922, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 4400, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.77033233642578, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 4400, 
            "Label": {
                "Instances": [], 
                "Confidence": 68.46247863769531, 
                "Parents": [
                    {
                        "Name": "Water"
                    }
                ], 
                "Name": "Aquatic"
            }
        }, 
        {
            "Timestamp": 4400, 
            "Label": {
                "Instances": [], 
                "Confidence": 57.74924087524414, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Beak"
            }
        }, 
        {
            "Timestamp": 4400, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.30696171522140503, 
                            "Top": 0.144287109375, 
                            "Left": 0.22396674752235413, 
                            "Height": 0.7462866306304932
                        }, 
                        "Confidence": 86.27051544189453
                    }
                ], 
                "Confidence": 86.7204818725586, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 4400, 
            "Label": {
                "Instances": [], 
                "Confidence": 60.02400207519531, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 4400, 
            "Label": {
                "Instances": [], 
                "Confidence": 62.43345260620117, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 4400, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.2487907409668, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 4400, 
            "Label": {
                "Instances": [], 
                "Confidence": 66.2137680053711, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 4400, 
            "Label": {
                "Instances": [], 
                "Confidence": 58.16676712036133, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Sea Life"
            }
        }, 
        {
            "Timestamp": 4400, 
            "Label": {
                "Instances": [], 
                "Confidence": 68.46247863769531, 
                "Parents": [], 
                "Name": "Water"
            }
        }, 
        {
            "Timestamp": 4400, 
            "Label": {
                "Instances": [], 
                "Confidence": 85.66663360595703, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 4600, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.82898712158203, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 4600, 
            "Label": {
                "Instances": [], 
                "Confidence": 67.83256530761719, 
                "Parents": [
                    {
                        "Name": "Water"
                    }
                ], 
                "Name": "Aquatic"
            }
        }, 
        {
            "Timestamp": 4600, 
            "Label": {
                "Instances": [], 
                "Confidence": 59.0078239440918, 
                "Parents": [
                    {
                        "Name": "Bird"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Beak"
            }
        }, 
        {
            "Timestamp": 4600, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.3058396279811859, 
                            "Top": 0.13702332973480225, 
                            "Left": 0.2092207968235016, 
                            "Height": 0.7735120058059692
                        }, 
                        "Confidence": 89.72554016113281
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.17597775161266327, 
                            "Top": 0.003950765356421471, 
                            "Left": 0.15447595715522766, 
                            "Height": 0.19859127700328827
                        }, 
                        "Confidence": 72.09510040283203
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.31234344840049744, 
                            "Top": 0.007410896942019463, 
                            "Left": 0.002845072653144598, 
                            "Height": 0.3882608711719513
                        }, 
                        "Confidence": 70.87576293945312
                    }
                ], 
                "Confidence": 87.15044403076172, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 4600, 
            "Label": {
                "Instances": [], 
                "Confidence": 53.97991943359375, 
                "Parents": [
                    {
                        "Name": "Plant"
                    }
                ], 
                "Name": "Grass"
            }
        }, 
        {
            "Timestamp": 4600, 
            "Label": {
                "Instances": [], 
                "Confidence": 61.05377197265625, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 4600, 
            "Label": {
                "Instances": [], 
                "Confidence": 57.4560661315918, 
                "Parents": [
                    {
                        "Name": "Bird"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 4600, 
            "Label": {
                "Instances": [], 
                "Confidence": 60.12495803833008, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 4600, 
            "Label": {
                "Instances": [], 
                "Confidence": 60.812286376953125, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Sea Life"
            }
        }, 
        {
            "Timestamp": 4600, 
            "Label": {
                "Instances": [], 
                "Confidence": 67.83256530761719, 
                "Parents": [], 
                "Name": "Water"
            }
        }, 
        {
            "Timestamp": 4600, 
            "Label": {
                "Instances": [], 
                "Confidence": 87.4284439086914, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 4800, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.2036361694336, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 4800, 
            "Label": {
                "Instances": [], 
                "Confidence": 64.24736785888672, 
                "Parents": [
                    {
                        "Name": "Water"
                    }
                ], 
                "Name": "Aquatic"
            }
        }, 
        {
            "Timestamp": 4800, 
            "Label": {
                "Instances": [], 
                "Confidence": 61.71356964111328, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Beak"
            }
        }, 
        {
            "Timestamp": 4800, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.30193066596984863, 
                            "Top": 0.14368638396263123, 
                            "Left": 0.20988507568836212, 
                            "Height": 0.7614515423774719
                        }, 
                        "Confidence": 92.7527847290039
                    }, 
                    {
                        "BoundingBox": {
                            "Width": 0.31587615609169006, 
                            "Top": 0.007122527342289686, 
                            "Left": 0.002042448613792658, 
                            "Height": 0.38757696747779846
                        }, 
                        "Confidence": 62.651546478271484
                    }
                ], 
                "Confidence": 90.06462860107422, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 4800, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.28676986694336, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 4800, 
            "Label": {
                "Instances": [], 
                "Confidence": 62.933197021484375, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 4800, 
            "Label": {
                "Instances": [], 
                "Confidence": 56.79875564575195, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 4800, 
            "Label": {
                "Instances": [], 
                "Confidence": 55.53575897216797, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Sea Life"
            }
        }, 
        {
            "Timestamp": 4800, 
            "Label": {
                "Instances": [], 
                "Confidence": 64.24736785888672, 
                "Parents": [], 
                "Name": "Water"
            }
        }, 
        {
            "Timestamp": 4800, 
            "Label": {
                "Instances": [], 
                "Confidence": 86.41097259521484, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 5000, 
            "Label": {
                "Instances": [], 
                "Confidence": 93.97762298583984, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 5000, 
            "Label": {
                "Instances": [], 
                "Confidence": 68.58273315429688, 
                "Parents": [
                    {
                        "Name": "Water"
                    }
                ], 
                "Name": "Aquatic"
            }
        }, 
        {
            "Timestamp": 5000, 
            "Label": {
                "Instances": [], 
                "Confidence": 64.67484283447266, 
                "Parents": [
                    {
                        "Name": "Bird"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Beak"
            }
        }, 
        {
            "Timestamp": 5000, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.3098117709159851, 
                            "Top": 0.17863719165325165, 
                            "Left": 0.21030397713184357, 
                            "Height": 0.7127665281295776
                        }, 
                        "Confidence": 93.915283203125
                    }
                ], 
                "Confidence": 90.92428588867188, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 5000, 
            "Label": {
                "Instances": [], 
                "Confidence": 52.265533447265625, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Mammal"
            }
        }, 
        {
            "Timestamp": 5000, 
            "Label": {
                "Instances": [], 
                "Confidence": 64.71392822265625, 
                "Parents": [
                    {
                        "Name": "Bird"
                    }, 
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 5000, 
            "Label": {
                "Instances": [], 
                "Confidence": 54.23300552368164, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 5000, 
            "Label": {
                "Instances": [], 
                "Confidence": 59.28446578979492, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Sea Life"
            }
        }, 
        {
            "Timestamp": 5000, 
            "Label": {
                "Instances": [], 
                "Confidence": 68.58273315429688, 
                "Parents": [], 
                "Name": "Water"
            }
        }, 
        {
            "Timestamp": 5000, 
            "Label": {
                "Instances": [], 
                "Confidence": 85.9736099243164, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }, 
        {
            "Timestamp": 5200, 
            "Label": {
                "Instances": [], 
                "Confidence": 94.2772216796875, 
                "Parents": [], 
                "Name": "Animal"
            }
        }, 
        {
            "Timestamp": 5200, 
            "Label": {
                "Instances": [], 
                "Confidence": 64.10331726074219, 
                "Parents": [
                    {
                        "Name": "Water"
                    }
                ], 
                "Name": "Aquatic"
            }
        }, 
        {
            "Timestamp": 5200, 
            "Label": {
                "Instances": [], 
                "Confidence": 67.0080337524414, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Beak"
            }
        }, 
        {
            "Timestamp": 5200, 
            "Label": {
                "Instances": [
                    {
                        "BoundingBox": {
                            "Width": 0.38834601640701294, 
                            "Top": 0.17760764062404633, 
                            "Left": 0.22096411883831024, 
                            "Height": 0.7267040610313416
                        }, 
                        "Confidence": 83.2437973022461
                    }
                ], 
                "Confidence": 91.10344696044922, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Bird"
            }
        }, 
        {
            "Timestamp": 5200, 
            "Label": {
                "Instances": [], 
                "Confidence": 66.91466522216797, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }, 
                    {
                        "Name": "Bird"
                    }
                ], 
                "Name": "Penguin"
            }
        }, 
        {
            "Timestamp": 5200, 
            "Label": {
                "Instances": [], 
                "Confidence": 52.75025939941406, 
                "Parents": [], 
                "Name": "Plant"
            }
        }, 
        {
            "Timestamp": 5200, 
            "Label": {
                "Instances": [], 
                "Confidence": 57.49009323120117, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Sea Life"
            }
        }, 
        {
            "Timestamp": 5200, 
            "Label": {
                "Instances": [], 
                "Confidence": 64.10331726074219, 
                "Parents": [], 
                "Name": "Water"
            }
        }, 
        {
            "Timestamp": 5200, 
            "Label": {
                "Instances": [], 
                "Confidence": 84.29118347167969, 
                "Parents": [
                    {
                        "Name": "Animal"
                    }
                ], 
                "Name": "Zoo"
            }
        }
    ], 
    "LabelModelVersion": "2.0", 
    "JobStatus": "SUCCEEDED", 
    "VideoMetadata": {
        "Format": "QuickTime / MOV", 
        "FrameRate": 25.0, 
        "Codec": "h264", 
        "DurationMillis": 5280, 
        "FrameHeight": 720, 
        "FrameWidth": 1280
    }
}
```


