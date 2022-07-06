+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2022-06-16
description = ""
summary = " "
draft = false
slug = "sagemaker-ground-truth"
tags = ["sagemaker","machine-learning",]
title = "SageMaker Ground Truth"
repoFullName = "pfeilbr/sagemaker-ground-truth-playground"
repoHTMLURL = "https://github.com/pfeilbr/sagemaker-ground-truth-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/sagemaker-ground-truth-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/sagemaker-ground-truth-playground</a>
</div>


learn SageMaker Ground Truth (GT) [Plus]

## Concepts

* Label Data - 
* **workforce** - the group of workers that you have selected to label your dataset. You can choose either the Amazon Mechanical Turk workforce, a vendor-managed workforce, or you can create your own private workforce to label or review your dataset
    > Each AWS account has access to a single private workforce per region, and the owner has the ability to create multiple private work teams within that workforce. A single private work team is used to complete a labeling job or human review task, or a job. You can assign each work team to a separate job or use a single team for multiple jobs. A single worker can be in more than one work team.

---

## SageMaker Ground Truth Plus

With SageMaker Ground Truth Plus, you receive a custom quote that is tailored to your specific use case and requirements. To get your customized quote, fill out the project requirement form.

SageMaker Ground Truth Plus is priced on a per label basis, which can be a bounding box, cuboid, key-value pair, etc.

Ground Truth Plus can be used for a variety of use cases, including computer vision, natural language processing, and speech recognition.

Amazon SageMaker Ground Truth Plus allows you to easily create high-quality training datasets without having to build labeling applications or manage labeling workforces on your own. Once you provide data along with labeling requirements, SageMaker Ground Truth Plus handles setting up the data labeling workflows and managing them on your behalf, in accordance with your requirements. From there, an expert workforce that is trained on a variety of machine learning (ML) tasks does data labeling. Ground Truth Plus uses ML techniques, including active-learning, pre-labeling, and machine validation. This increases the quality of the output dataset and decreases the data labeling costs. Ground Truth Plus provides transparency into your data labeling operations and quality management. With it, you can review the progress of training datasets across multiple projects, track project metrics, such as daily throughput, inspect labels for quality, and provide feedback on the labeled data. Ground Truth Plus can be used for a variety of use cases, including computer vision, natural language processing, and speech recognition.

Can the datasets be shared with amazon provided workforce 

> Ground Truth Plus does not support PHI, PCI or FedRAMP certified data, and you should not provide this data to Ground Truth Plus.

* request a pilot
* share data by creating bucket and applying bucket policy allowing GT aws account the bucket actions
  *  s3://your-bucket-name/ground-truth-plus/input/project-name/batch-name/..           
* create project team - cognito - up to 50 email addresses
  * Your team members receive an email inviting them to join the Ground Truth Plus project team as shown in the following image.
* Open the Project Portal
  * view status on batches
  * The portal allows your project team members and you to review a small sample set of the labeled objects for each batch.
* Accept or Reject Batches
  *  

---

Text Classification (Multi-label)

Use a multi-label text classification task when you want workers to group a piece of text into one or more classes by choosing one or more labels. When you create a multi-label text classification job, you can provide up to 50 labels for workers to choose from when classifying text. Workers must select at least one label, and can select as many labels as you provide. For example, if you provide 10 labels, the worker can select up to 10 labels for an object.

---

- cannot provision any GT resources via CloudFormation

---

## Create Labeling Job Python (Boto3)

```py
response = client.create_labeling_job(
    LabelingJobName="example-labeling-job",
    LabelAttributeName="label",
    InputConfig={
        'DataSource': {
            'S3DataSource': {
                'ManifestS3Uri': "s3://bucket/path/manifest-with-input-data.json"
            }
        },
        'DataAttributes': {
            'ContentClassifiers': [
                "FreeOfPersonallyIdentifiableInformation"|"FreeOfAdultContent",
            ]
        }
    },
    OutputConfig={
        'S3OutputPath': "s3://bucket/path/file-to-store-output-data",
        'KmsKeyId': "string"
    },
    RoleArn="arn:aws:iam::*:role/*",
    LabelCategoryConfigS3Uri="s3://bucket/path/label-categories.json",
    StoppingConditions={
        'MaxHumanLabeledObjectCount': 123,
        'MaxPercentageOfInputDatasetLabeled': 123
    },
    HumanTaskConfig={
        'WorkteamArn': "arn:aws:sagemaker:region:*:workteam/private-crowd/*",
        'UiConfig': {
            'UiTemplateS3Uri': "s3://bucket/path/custom-worker-task-template.html"
        },
        'PreHumanTaskLambdaArn': "arn:aws:lambda:us-east-1:432418664414:function:PRE-tasktype",
        'TaskKeywords': [
            "Images",
            "Classification",
            "Multi-label"
        ],
        'TaskTitle': "Multi-label image classification task",
        'TaskDescription': "Select all labels that apply to the images shown",
        'NumberOfHumanWorkersPerDataObject': 1,
        'TaskTimeLimitInSeconds': 3600,
        'TaskAvailabilityLifetimeInSeconds': 21600,
        'MaxConcurrentTaskCount': 1000,
        'AnnotationConsolidationConfig': {
            'AnnotationConsolidationLambdaArn': "arn:aws:lambda:us-east-1:432418664414:function:ACS-"
        },
    Tags=[
        {
            'Key': "string",
            'Value': "string"
        },
    ]
)
```

---

## Screenshots

![](https://www.evernote.com/l/AAGcVTijrCJEeJouTodX_sABPocEa2exypgB/image.png)

---

## Resources

* [Use Amazon SageMaker Ground Truth to Label Data](https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html)
* [Use Amazon SageMaker Ground Truth Plus to Label Data](https://docs.aws.amazon.com/sagemaker/latest/dg/gtp.html)
* [Getting Started with Amazon SageMaker Ground Truth Plus.](https://docs.aws.amazon.com/sagemaker/latest/dg/gtp-getting-started.html)
* [Build a custom data labeling workflow with Amazon SageMaker Ground Truth](https://aws.amazon.com/blogs/machine-learning/build-a-custom-data-labeling-workflow-with-amazon-sagemaker-ground-truth/)
* [Crowd HTML Elements Reference](https://docs.aws.amazon.com/sagemaker/latest/dg/sms-ui-template-reference.html)
* [aws-samples/amazon-sagemaker-ground-truth-task-uis](https://github.com/aws-samples/amazon-sagemaker-ground-truth-task-uis)
* [nitinaws/gt-custom-workflow](https://github.com/nitinaws/gt-custom-workflow)
* [aws-samples/sagemaker-ground-truth-label-training-data](https://github.com/aws-samples/sagemaker-ground-truth-label-training-data)
* [Create a Labeling Job (API) - Examples](https://docs.aws.amazon.com/sagemaker/latest/dg/sms-create-labeling-job-api.html#sms-create-labeling-job-api-examples) - python and aws cli examples



