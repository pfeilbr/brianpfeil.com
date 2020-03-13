+++
author = "Brian Pfeil"
categories = ["nodejs", "docker", "elastic beanstalk", "aws"]
date = 2015-03-25T19:06:15Z
description = ""
draft = false
slug = "dockerized-nodejs-app-on-elastic-beanstalk-example"
tags = ["nodejs", "docker", "elastic beanstalk", "aws"]
title = "Dockerized Node.js App on Elastic Beanstalk Example"

+++




Example of developing and deploying a [dockerized]((https://www.docker.com/)) [Node.js](https://nodejs.org/) app to [Elastic Beanstalk](http://aws.amazon.com/elasticbeanstalk/)

> source on Github at [pfeilbr/Elastic-Beanstalk-Docker-Node.js-Example](https://github.com/pfeilbr/Elastic-Beanstalk-Docker-Node.js-Example)

## Local Development Workflow

1. Edit code. e.g. `index.js`
2. Build image

	```
	$ docker build --tag="pfeilbr/eb-docker-node-example" .
	```

3. Run

	```
	$ docker run -p 80:80 -it -rm -name eb-docker-node-example pfeilbr/eb-docker-node-example
	```

4. Get docker host ip *(optional.  only if using [boot2docker](http://boot2docker.io/))*

	```
	$ boot2docker ip
	```

5. Open browser to `http://<boot2docker ip>`

## Initial Deployment

1. Init git repo

	```
	$ git init .
	```

2. Add files to repo 

	```
	$ git add .
	```

3. Commit changes

	```
	$ git commit -m "init"
	```

4. Create eb app

	```
	$ eb init # populate details
	```

	> Populate all details

5. Create environment for app

	```
	$ eb create dev-env
	```

	> **IMPORTANT** Must immediately update the ec2 instance with tags so it doesn't get terminated.  Enable termination protection on the ec2 instance.

**Output**

![](http://note.io/1ETb45Y)


## Deploying Updates

1. Modify code and test via [Local Development Workflow]
2. Commit changes

	```
	$ git commit -a -m "my updates"
	```

3. Deploy to eb

	```
	$ eb deploy
	```

> NOTE: Takes between 3-5 min to deploy changes

**Output**

![](http://note.io/1FFQXuL)

## Establish Interactive Bash Shell in Running Docker Container

1. ssh into ec2 docker host server

	```
	$ eb ssh
	```

2. Get container name

	```
	$ sudo docker ps # save off name of container
	```

3. Connect/attach with an interactive bash session

	```
	$ sudo docker exec -i -t <container name> bash
	```

**Example Session with Output**

![](http://note.io/1CYSlIH)