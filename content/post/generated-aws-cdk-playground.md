+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-07-11
description = ""
summary = " "
draft = false
slug = "aws-cdk"
tags = ["aws","cdk"]
title = "AWS CDK"
repoFullName = "pfeilbr/aws-cdk-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-cdk-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-cdk-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-cdk-playground</a>
</div>


learn [AWS Cloud Development Kit (CDK)](https://docs.aws.amazon.com/cdk/latest/guide/home.html)

see [`kitchen-sink/README.md`](https://github.com/pfeilbr/aws-cdk-playground/blob/master/kitchen-sink/README.md)
## Description

* express resources using general purpose programming languages (ts/js/python/java/C#)
* constructs - construct levels 1, 2, 3.  cfn (L1), CDK (L2), pattern/solution (L3)
* synth to cfn
* cloud assemblies - cfn + source code, docker images, assets (s3)
* [aspects](https://docs.aws.amazon.com/cdk/latest/guide/aspects.html) - ability to visit each node/resource in stack and apply changes
* Application -> Stacks -> Constructs
* [Parameters](https://docs.aws.amazon.com/cdk/latest/guide/parameters.html) - cfn parameters.  can pass in via `cdk synth`.
* [Runtime context](https://docs.aws.amazon.com/cdk/latest/guide/context.html#context_example) - key-value pairs that can be associated with a stack or construct.  Can only be `string` values (kind of like parameters)
* `[tf|k8s]` CDKs
* jsii - core/foundational tech for multi-language/polyglot support.  bind any language to underlying typescript implementation.
* CDK pipelines for CI/CD
* [Custom Logical Names](https://github.com/aws-samples/aws-cdk-examples/blob/master/typescript/custom-logical-names/README.md) - shows how to hook into an provide own resource names.  Can be used for IAM policies based on resource name `prefixes`
* Usage with Permissions Boundaries - [class PermissionsBoundary · AWS CDK](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-iam.PermissionsBoundary.html). e.g. `PermissionsBoundary.of(this).apply(permissionsBoundariesPolicy);`


## Key Files and Directories

* `bin` - entry point to CDK app.  imports 1 or more stacks from `lib` folder
* `lib/*-stack.*` - define stacks here which contain constructs
* `cdk.json` - cdk configuration
* `test` - unit/integration/e2e tests
* `cdk.out` - CDK assembly / synth output (cfn, assets, etc.)

## Common Areas

* `@aws-cdk/core - App, Stack, Stack.account, Stack.region, Stack.tags, Stack.terminationProtection, Construct, Duration, CfnOutput`
* `lambda.Function`, `lambda.Code.fromAsset`, `lambda.Code.fromInline`
* `@aws-cdk/aws-iam - Role, User, Group, PolicyStatement`


---

## Common Steps
```sh
# init cdk app
cdk init app --language javascript
cdk init app --language typescript

# list stacks in the app
cdk list

# [optional] build for ts -> js.  not required for js
npm run build

# synthesize to cfn (`cdk.out`)
cdk synth

# run tests
npm test

# compare the specified stack with the deployed stack
cdk diff

# deploy
cdk deploy

# force deploy, no prompt
cdk deploy  --force --require-approval never

# delete
cdk destroy [STACKS..]

```

---
## CDK Internals

Details on the inner workings of CDK.
### CDK Tree

Core of CDK is based on tree structure similar to the DOM.

* `node: ConstructNode` - accessed via `this.node` - root of the tree.
* `node.children`
* `node.findChild(id: string)` - search for child in tree with `id`.  `new s3.Bucket(this, "Assets")`.  `"Assets"` is the `id`.
* `node.tryFindChild(id: string)` - same as `findChild` but won't throw if `id` doesn't exist.  Will return `undefined`.
* `node.defaultChild` - reference to primary level 1 construct (`Cfn*`)
* common L1 construct methods
    * `overrideLogicalId`
    * `addOverride(propertyPath, value)` - e.g. `cfnBucket.addOverride("Properties.BucketName", "my-bucket-name-01")`
        * need to use for cfn attributes that are outside of the `Properties`.  e.g. `DeletionPolicy`
        * add bucket name to `Metadata` - `cfnBucket.addOverride("Metadata.BucketName", cfnBucket.ref)`
    * `addDeletionOverride(propertyPath)` - remove a property.  e.g. `cfnBucket.addDeletionOverride("Properties.BucketName")`
    * `addPropertyOverride(propertyPath)` - `cfnBucket.addPropertyOverride("Properties.BucketName", "my-bucket-name-01")`

* all `Fn::GetAtt` return values can be accessed via a property named `Att${Return Value Name}`. e.g. `cfnBucket.AttArn`, `cfnBucket.AttDomainName`
### CDK Path

* every resource defined in CDK tree has a path
* `this.node.path` - concatenation of path traversal to the node in the CDK tree. (e.g. `MyStack/Assets`)
* this path is added to the `Metadata` property for each resource in cfn.

### CDK Identifiers

* Logical ID - used in cfn template. scoped within stack.  calculated using CDK path (sanitized id (no stack id) + hash)
* Unique ID - uniquely identify resource within CDK application. scoped within CDK application, which may be composed of multiple stacks. sanitized id (including stack) + hash

<img src="https://www.evernote.com/l/AAEqngqx1ZlJOJObL2Oe3eHqFcwiW_SaRfcB/image.png" alt="CDK Identifiers Calculation Image" width="50%" />

---

### Common CDK Snippets

* [@aws-cdk/core module](https://docs.aws.amazon.com/cdk/api/latest/docs/core-readme.html)
* [@aws-cdk/aws-iam module](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-iam-readme.html) - key module

```js

// durations
Duration.seconds(300)   // 5 minutes
Duration.minutes(5)     // 5 minutes
Duration.hours(1)       // 1 hour
Duration.days(7)        // 7 days
Duration.parse('PT5M')  // 5 minutes

// sizes
Size.kibibytes(200) // 200 KiB
Size.mebibytes(5)   // 5 MiB
Size.gibibytes(40)  // 40 GiB
Size.tebibytes(200) // 200 TiB
Size.pebibytes(3)   // 3 PiB

// create secret
const secret = SecretValue.secretsManager('secretId', {
  jsonField: 'password', // optional: key of a JSON field to retrieve (defaults to all content),
  versionId: 'id',       // optional: id of the version (default AWSCURRENT)
  versionStage: 'stage', // optional: version stage name (default AWSCURRENT)
});

// get default VPC
const vpc = ec2.Vpc.fromLookup(stack, 'VPC', {
  // This imports the default VPC but you can also
  // specify a 'vpcName' or 'tags'.
  isDefault: true,
});

// custom resource
const fn = new lambda.Function(this, 'MyProvider', functionProps);

new CustomResource(this, 'MyResource', {
  serviceToken: fn.functionArn,
});

// OR

const serviceToken = CustomResourceProvider.getOrCreate(this, 'Custom::MyCustomResourceType', {
  codeDirectory: `${__dirname}/my-handler`,
  runtime: CustomResourceProviderRuntime.NODEJS_12_X,
  description: "Lambda function created by the custom resource provider",
});

new CustomResource(this, 'MyResource', {
  resourceType: 'Custom::MyCustomResourceType',
  serviceToken: serviceToken
});

// bastion host
const host = new ec2.BastionHostLinux(this, 'BastionHost', { vpc });


```

---
## Resources

* [AWS CDK · AWS CDK Reference Documentation](https://docs.aws.amazon.com/cdk/api/latest/)
* [Infrastructure-as-Code | Constructs | AWS Solutions](https://aws.amazon.com/solutions/constructs/)
* [awslabs/aws-solutions-constructs](https://github.com/awslabs/aws-solutions-constructs)
* [aws-samples/aws-cdk-examples](https://github.com/aws-samples/aws-cdk-examples)
* [aws/constructs](https://github.com/aws/constructs/blob/master/README.md) - Constructs Programming Model
* [panacloud-modern-global-apps/full-stack-serverless-cdk](https://github.com/panacloud-modern-global-apps/full-stack-serverless-cdk)
* [github | search | "filename:cdk.json"](https://github.com/search?l=&q=filename%3Acdk.json&type=code)
* [Exploring CDK Internals](https://www.youtube.com/watch?v=X8G3G3SnCuI)
* [Working with the AWS CDK Explorer - AWS Toolkit for VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/cdk-explorer.html)
