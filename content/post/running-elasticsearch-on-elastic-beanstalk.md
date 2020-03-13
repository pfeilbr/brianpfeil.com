+++
author = "Brian Pfeil"
categories = ["docker", "elastic beanstalk", "aws", "elastic search"]
date = 2015-03-25T21:25:09Z
description = ""
draft = false
image = "/images/2015/03/es.jpeg"
slug = "running-elasticsearch-on-elastic-beanstalk"
tags = ["docker", "elastic beanstalk", "aws", "elastic search"]
title = "Running Elasticsearch on AWS Elastic Beanstalk"

+++


> **TL;DR** code on github @ [pfeilbr/Elastic-Beanstalk-Dockerrun.aws.json-Example](https://github.com/pfeilbr/Elastic-Beanstalk-Dockerrun.aws.json-Example)

This article will show you the steps to run [elasticsearch](https://www.elastic.co/) on [AWS Elastic Beanstalk](http://aws.amazon.com/elasticbeanstalk/). This example uses the [elasticsearch docker image](https://registry.hub.docker.com/_/elasticsearch/) as an example.  Once running you can visit `http://<beanstalk domain>/?pretty` an you will see the root elastic search JSON response.

## Initial Deployment

1. Modify `Dockerrun.aws.json` for your needs.

	> [Dockerrun.aws.json](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker_image.html#create_deploy_docker_image_dockerrun) reference

2. Commit changes to repo

	```
	$ git commit -a -m "changes"
	```

	> assumes `Dockerrun.aws.json` has already been added to repo.  if not, `git add .`

3. Create eb app

	```
	$ eb init # populate details
	```

	> NOTE: select Docker.  Populate all details

4. Create environment for app

	```
	$ eb create dev-env
	```

	> **IMPORTANT** Must immediately update the ec2 instance with tags so it doesn't get terminated.  Enable termination protection on the ec2 instance.

## Deploying Updates

1. Modify `Dockerrun.aws.json` for your needs.
2. Commit changes

	```
	$ git commit -a -m "my updates"
	```

3. Deploy to eb

	```
	$ eb deploy
	```

> NOTE: Takes between 3-5 min to deploy changes

## Notes

Port mapping details specific to aws beanstalk

![](http://note.io/1xzEypO)
