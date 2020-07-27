+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2019-01-31
description = ""
summary = "learning Pivotal Cloud Foundry"
draft = false
slug = "pivotal-cloud-foundry"
tags = ["github",]
title = "Pivotal Cloud Foundry"
repoFullName = "pfeilbr/pivotal-cloud-foundry-playground"
repoHTMLURL = "https://github.com/pfeilbr/pivotal-cloud-foundry-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/pivotal-cloud-foundry-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/pivotal-cloud-foundry-playground</a>
-->


learn [Pivotal Cloud Foundry](https://pivotal.io/platform)

### Resources

* [PCF on your Local Workstation with PCF Dev](https://pivotal.io/platform/pcf-tutorials/getting-started-with-pivotal-cloud-foundry-dev/introduction) tutorial
* [Cloud Foundry Documentation](https://docs.cloudfoundry.org/)
* [Why Yes, Cloud Foundry IS Like Your Own Heroku!](https://www.cloudfoundry.org/blog/yes-cloud-foundry-like-heroku/)

---

### Example Apps

see `README.md` in subdirectories of [apps/](apps)

---

### Notes

* [stacks](https://docs.cloudfoundry.org/devguide/deploy-apps/stacks.html) is a prebuilt root file system (rootfs) that supports a specific operating system
(https://docs.cloudfoundry.org/devguide/deploy-apps/stacks.html)
    > e.g. cflinuxfs3: The Linux cflinuxfs3 stack is derived from Ubuntu Bionic 18.04.
* uses [buildpacks](https://docs.cloudfoundry.org/buildpacks/understand-buildpacks.html) to support different languages/run-times (based on heroku buildpack scheme). buildpacks are layered on top of stacks
* supports [Deploy an App with Docker](https://docs.cloudfoundry.org/devguide/deploy-apps/push-docker.html)
* [Restaging](https://docs.cloudfoundry.org/devguide/deploy-apps/start-restart-restage.html#restage-your-app) your app stops your app and restages it, by compiling a new droplet and starting it.
* [Task](https://docs.cloudfoundry.org/devguide/using-tasks.html): A task is an app or script whose code is included as part of a deployed app, but runs independently in its own container.



---

### `cf` cli session

```sh
cf help

# install PCF Dev <https://pivotal.io/pcf-dev>
./pcfdev-v0.30.0+PCF1.11.0-osx

# start environment (VM, etc).  takes ~5 mins.
cf dev start

# To begin using PCF Dev, please run:
#    cf login -a https://api.local.pcfdev.io --skip-ssl-validation
# Apps Manager URL: https://apps.local.pcfdev.io
# Admin user => Email: admin / Password: admin
# Regular user => Email: user / Password: pass

cf login -a https://api.local.pcfdev.io --skip-ssl-validation

# web UI
open https://apps.local.pcfdev.io
# login: admin/admin

cd ~/dev

# fetch sample
git clone https://github.com/cloudfoundry-samples/spring-music
cd spring-music

# build
./gradlew assemble

# deploy app
cf push --hostname spring-music

# show logs
cf logs spring-music --recent

# stream logs
cf logs spring-music

# view app resources
cf app spring-music

# show app ENV
cf env spring-music

# run a task (simple `ls`)
cf run-task spring-music "ls" --name my-task

# view task output
cf logs spring-music --recent

# list tasks for an app (running, failed, succeeded)
cf tasks spring-music

# cancel a task
cf terminate-task spring-music TASK-ID

# stop app
cf stop spring-music

# show routes
cf routes

# stop environment (VMs, etc.)
cf dev stop
```

---

### Screenshots

**login**

![](https://www.evernote.com/l/AAGhjcTEI_pPJLX9dYtKP6XUfQ2Pi7hF990B/image.png)




