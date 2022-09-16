+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2021-04-09
description = ""
summary = " "
draft = false
slug = "aws-well-architected"
tags = ["aws","aws-well-architected","architecture",]
title = "AWS Well-Architected"
repoFullName = "pfeilbr/aws-well-architected-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-well-architected-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-well-architected-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-well-architected-playground</a>
</div>


deep dive on all things AWS Well-Architected

## Key Points

* consistent pre-launch review process against AWS best practices
* helps you understand the pros and cons of decisions you make while building systems
* review process is a conversation and not an audit.  working together to improve. practical advice.
* goal is not to have "perfect" architecture from the start. identify areas for improvement and choose a couple that delivery the most value
* AWS does not provide prescriptive guidance on how to perform the review.  WA tool is the closest.
* concepts: Pillars -> Design Principles -> Questions
* enables: learn -> measure -> improve iterative cycle
* input: answer questions, output: improvement plan (PDF reports)
* learning / education - can be used as standalone tool solely for learning what the best practices are
* milestone - record the state of a workload for given point in time. e.g. original design, design review, v1, v2

## Use Cases

* learning best practices for the cloud
* technology governance
* portfolio management - inventory of workloads, historical decisions made, risks, highlights where to invest

## Well-Architected Framework

> The AWS Well-Architected Framework helps you to design and operate a reliable, secure, efficient, and cost-efficient systems on AWS. It also helps you constantly measure your architecture against best practices and provides you an opportunity to improve your architecture.

### 5 Pillars

* Operational Excellence
* Security
* Reliability
* Performance Efficiency
* Cost Optimization

### Review Process

> The review process describes in high-level terms, how the assessment of the principles should be done. For AWS, this should be a lightweight process, which is taking rather hours, instead of days and it should be repeated multiple times across the architecture lifecycle. AWS states that it is important to have a conversation (not an audit) and a “blame-free approach” during the review and it is also important to involve the right people. The results of the conversations should be a list of issues that can then be prioritized based on the business context and that can be formulated into a set of actions that help to improve the overall customer experience of the architecture.

## Well-Architected Tool

AWS Console Tool that steps a user through the Well-Architected Review Process

### Well-Architected Alternate Renditions

Consuming the WA PDFs or web content can be a bit challenging with navigation.  The WA questions, resources, etc. are available as `json` via the AWS WA Console Tool with some scraping.  This creates alternate renditions based on this data.

* Run [`aws-well-architected-reformat/main.js`](aws-well-architected-reformat/main.js) to generate a reformatted and condensed version of WA.
    ```sh
    cd aws-well-architected-reformat
    node main.js > ../aws-well-architected-condensed.md
    ```
* see alternate rendition at [`aws-well-architected-condensed.md`](aws-well-architected-condensed.md)
* See [`aws-well-architected-reformat/data`](aws-well-architected-reformat/data) for the question data as `json` for each lens.

**Notes on pulling data via AWS Console**

```sh
# aws console request format
POST https://console.aws.amazon.com/wellarchitected/api/apiservice
{"method":"GET","path":"/workloads/4cfa14fe4a9d351afc9975cfdcb434af/lensReviews/wellarchitected/answers","region":"us-east-1","headers":{"Content-Type":"application/json","Accept":"application/json"},"params":{"PillarId":"operationalExcellence","MaxResults":50,"Locale":"en"}}

# helpful Resources on right sidebar example
https://wa.aws.amazon.com/TypeII/en/foundationaltechnicalreview/foundationaltechnicalreview.sec_q1.helpful-resources.en.html

```

### Feature Request

> Custom lenses have been added.  See [Custom lenses](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses-custom.html)

One area where there is a gap for an enterprises are all the company specific policies, standards, and best practices that are additive and need to be addressed on top of AWS.  These types of questions and guidance would need to happen outside of WA Tool.

A feature to define custom lenses - a customer defined lens.  This way the single WA Tool could be the method for review facilitation, improvement reporting and maintaining history.

### Custom Lens

template JSON file for creating custom lens

```json
{
  "schemaVersion": "2021-11-01",
  "name": "Replace with lens name",
  "description": "Replace with your description",
  "pillars": [
    {
      "id": "pillar_id_1",
      "name": "Pillar 1",
      "questions": [
        {
          "id": "pillar_1_q1",
          "title": "My first question",
          "description": "Description isn't a necessary property here for a question, but it might help your lens users.",
          "choices": [
            {
              "id": "choice1",
              "title": "Best practice #1",
              "helpfulResource": {
                "displayText": "It's recommended that you include a helpful resource text and URL for each choice for your users.",
                "url": "https://aws.amazon.com"
              },
              "improvementPlan": {
                "displayText": "You must have improvement plans per choice. It's optional whether or not to have a corresponding URL."
              }
            },
            {
              "id": "choice2",
              "title": "Best practice #2",
              "helpfulResource": {
                "displayText": "It's recommended that you include a helpful resource text and URL for each choice for your users.",
                "url": "https://aws.amazon.com"
              },
              "improvementPlan": {
                "displayText": "You must have improvement plans per choice. It's optional whether or not to have a corresponding URL."
              }
            }
          ],
          "riskRules": [
            { "condition": "choice1 && choice2", "risk": "NO_RISK" },
            { "condition": "choice1 && !choice2", "risk": "MEDIUM_RISK" },
            { "condition": "default", "risk": "HIGH_RISK" }
          ]
        }
      ]
    }
  ]
}

```

## Key Visuals

<img src="https://www.evernote.com/l/AAGT8fHSJRtGV4338tvJ0FHMvbb_vfTh7qkB/image.png" alt="WA Tool Features" width="50%" />

<img src="https://www.evernote.com/l/AAE0ZIXQoM5KYK9TUKsBpNZ_dSQ_x27Ti_0B/image.png" alt="General Design Principles" width="50%" />

<img src="https://www.evernote.com/l/AAGxCfQWxsZMDZLQC9dqcm-EJRgkM3jsNlwB/image.png" alt="Intent of WA Review" width="50%" />

<img src="https://www.evernote.com/l/AAF2yN9IdGZOS6_CoSnpzjc0nWOru88e4a0B/image.png" alt="Review Benefits" width="50%" />

<img src="https://www.evernote.com/l/AAEqVMFtRnJBMp-iX7F3Y8eLLIu3kV6ruvQB/image.png" alt="" width="50%" />

## Resources

* [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected)
* [Documentation | AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
* [The Review Process - AWS Well-Architected Framework](https://wa.aws.amazon.com/wat.thereviewprocess.wa-review.en.html)
* [AWS Well Architected framework: A Complete Checklist](https://www.rapyder.com/blogs/aws-well-architected-framework-checklist/)
* [AWS Well-Architected Framework Cheatsheet | Cloud Noon](https://cloudnoon.com/blog/aws/aws-well-architected-framework-cheatsheet/)
* [AWS Well-Architected Tool: Custom lenses](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses-custom.html)
* [Announcing AWS Well-Architected Custom Lenses: Extend the Well-Architected Framework with Your Internal Best Practices](https://aws.amazon.com/blogs/aws/well-architected-custom-lenses-internal-best-practices/)
* [Customize Well-Architected Reviews using Custom Lenses and the AWS Well-Architected Tool](https://aws.amazon.com/blogs/mt/customize-well-architected-reviews-using-custom-lenses-and-the-aws-well-architected-tool/)
* [Custom lenses](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses-custom.html)



