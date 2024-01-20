+++
author = "Brian Pfeil"
categories = ["Jupyter Notebook", "playground"]
date = 2023-10-19
description = ""
summary = " "
draft = false
slug = "amazon-bedrock"
tags = ["aws","ai","genai","llm",]
title = "Amazon Bedrock"
repoFullName = "pfeilbr/amazon-bedrock-playground"
repoHTMLURL = "https://github.com/pfeilbr/amazon-bedrock-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/amazon-bedrock-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/amazon-bedrock-playground</a>
</div>


learn [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide)

## demo

```sh
pipenv install

# login for boto3 credentials
aws sso login --profile root-AWSAdministratorAccess
```

- visit [`main.ipynb`](./main.ipynb)
- in vscode select `.venv` kernel in top right

---

run jupyter lab UI

```sh
pipenv run jupyter lab
# open http://localhost:8888/lab
```

## Concepts

### Foundation Models

### Custom models

#### [Continued Pre-training model](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html#pre-training)

> allows you to train a model with new unlabeled data. Use continued pre-training to teach a model new domain knowledge that's not already present in the base models. You can train a model with private data, such as business documents, that are not publically available for training large language models. Additionally, you can continue to improve the model by retraining the model with more unlabeled data as it becomes available.

#### [Fine-Tuning model](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html#fine-tuning)

> allows you to improve a model's performance on specific tasks. By providing a training dataset of labeled examples related to a specific task, you help the model learn the task it's supposed to carry out.

### Model customization job

> A model customization job is a process that takes a base model and trains it with your data to create a custom model. You can use a model customization job to create a custom model from a base model that's provided by Amazon Bedrock or a custom model that you've already created.

1. upload a training dataset and, optionally, a validation dataset to Amazon S3 and provide the Amazon S3 bucket path to the model customization job
1. After you complete a model customization job, you can purchase Provisioned Throughput (see Provisioned Throughput) for the customized model so that you can use the model for inference using the InvokeModel or InvokeModelWithResponseStream API operations. 

### Model Provisioned Throughput

> When you configure Provisioned Throughput for a model, you receive a level of throughput at a fixed cost.

> You can use Provisioned Throughput with Amazon and third-party base models, and with customized models.

### Multimodal Embeddings model

e.g. [Amazon Titan Multimodal Embeddings model](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-multiemb-models.html)

> searching images by text, image, or a combination of text and image. Designed for high accuracy and fast responses, this model is an ideal choice for search and recommendations use cases.

see [Multimodal RAG example](https://github.com/aws-samples/amazon-bedrock-samples/tree/main/multimodal/rag) with code at  [1_multimodal_rag.ipynb](https://github.com/aws-samples/amazon-bedrock-samples/blob/main/multimodal/rag/1_multimodal_rag.ipynb)

### Knowledge base for Amazon Bedrock

managed [Retrieval Augmented Generation (RAG)](https://www.promptingguide.ai/techniques/rag) 

**Steps**

1. create data source (e.g. s3 bucket with pdf docs)
2. select embedding model (e.g. Amazon Titan G1 Embeddings - Text)
3. create and select a vector database (e.g. OpenSearch)
4. ingest data sources into knowledge base
5. test knowledge base - send queries and see the responses

### Agents

[Build a Foundation Model (FM) powered customer service bot with agents for Amazon Bedrock](https://github.com/aws-samples/amazon-bedrock-samples/tree/main/agents/agentsforbedrock-retailagent) - good example

**TL;DR** model that uses OpenAPI schema backed by Lambda function that defines the business logic for the action that your agent will carry out

**Steps**

- select model (e.g. )
- define action groups
- add knowledge base (optional)


**Action Groups** 

- Action groups define the tasks that you want your agent to help customers carry out
- Action groups are mapped to an AWS Lambda function and related API schema to perform API calls.
- Knowledge bases provide a repository of information that the agent can query to answer customer queries and improve its generated responses.

- Action group consists of the following components that you set up
  - OpenAPI schema that define the APIs that your action group should call. Your agent uses the API schema to determine the fields it needs to elicit from the customer to populate for the API request.
  - A Lambda function that defines the business logic for the action that your agent will carry out.


## Resources

- <https://docs.aws.amazon.com/bedrock/latest/userguide>
- [Amazon Bedrock Base model IDs (on-demand throughput)](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids-arns.html)
- [Amazon Bedrock base model IDs (provisioned throughput)](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput-models.html)
- [aws-samples/amazon-bedrock-samples](https://github.com/aws-samples/amazon-bedrock-samples)
- [Build a Foundation Model (FM) powered customer service bot with agents for Amazon Bedrock](https://github.com/aws-samples/amazon-bedrock-samples/tree/main/agents/agentsforbedrock-retailagent)


