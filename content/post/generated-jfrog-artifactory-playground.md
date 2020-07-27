+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2018-12-05
description = ""
summary = "experimenting with Jfrog Artifactory"
draft = false
slug = "jfrog-artifactory"
tags = ["github",]
title = "Jfrog Artifactory"
repoFullName = "pfeilbr/jfrog-artifactory-playground"
repoHTMLURL = "https://github.com/pfeilbr/jfrog-artifactory-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/jfrog-artifactory-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/jfrog-artifactory-playground</a>


learn [JFrog Artifactory](https://jfrog.com/artifactory/)

### Resources

* [CLI for JFrog Artifactory](https://www.jfrog.com/confluence/display/CLI/CLI+for+JFrog+Artifactory) docs

### Session

```sh
# install jfrog cli
npm install -g jfrog-cli-go

# configure artifactory server
jfrog rt c merck --url=https://artifacts.merck.com/artifactory --user=pfeilbr --password='PASSWORD_HERE'

# show details
jfrog rt c show merck

# Show all configured artifactory servers
jfrog rt c show

# use a predefined artifactory Server
jfrog rt use merck

# verify that Artifactory is accessible by sending an applicative ping to Artifactory
jfrog rt ping

# search a repo (`npm-firefly-dev` repo)
jfrog rt s npm-firefly-dev

# search a directory within a repo
jfrog rt s 'npm-firefly-dev/@firefly/test/*.*'

# upload file to repo including build name and number
jfrog rt u old.txt my-local-repo-01 --build-name=my-build-01 --build-number=1

# publish build (makes visible in "Builds" section of UI)
jfrog rt bp my-build-01 1
# see https://www.jfrog.com/confluence/display/CLI/CLI+for+JFrog+Artifactory#CLIforJFrogArtifactory-BuildIntegration-PublishingaBuild

```

### Running Local Artifactory Server with Docker

> see https://www.jfrog.com/confluence/display/RTF/Installing+with+Docker for details

```sh
# pull image
docker pull docker.bintray.io/jfrog/artifactory-oss:latest

# runs in background as daemon
docker run --name artifactory -d -p 8081:8081 docker.bintray.io/jfrog/artifactory-oss:latest

# open Artifactory UI in browser
open http://localhost:8081
```



