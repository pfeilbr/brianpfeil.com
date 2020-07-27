+++
author = "Brian Pfeil"
categories = ["Java", "playground"]
date = 2015-08-26
description = ""
summary = "experimenting with Gradle"
draft = false
slug = "gradle"
tags = ["playground",]
title = "Gradle"
repoFullName = "pfeilbr/gradle-playground"
repoHTMLURL = "https://github.com/pfeilbr/gradle-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/gradle-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/gradle-playground</a>
-->


Project to learn and explore the [gradle](https://gradle.org/) build automation tool.

Each subdirectory contains an example

### Gradle Daemon

Dramatically speeds up tasks.  See [Gradle Daemon](https://docs.gradle.org/2.6/userguide/gradle_daemon.html) docs.

**TL;DR**

Can enable view the following

```
touch ~/.gradle/gradle.properties && echo "org.gradle.daemon=true" >> ~/.gradle/gradle.properties
```

---

### Basics

**Show Tasks**

	gradle tasks


---

### helloworld

This is a simple example showing how to run a task and print to stdout.

To Run

	$ gradle helloworld

---

### command-line-app

**Init gradle**

	$ mkdir command-line-app
	$ cd command-line-app
	$ gradle init --type java-library

This creates the gradle files and default directory structure for a `java-library`

**Create a jar**

	$ gradle uploadArchives

> outputs jar to `repos/`

![](http://static-content-01.s3-website-us-east-1.amazonaws.com//command-line-app_—_bash_—_80×24_1B8E0BEA.png)

Run via

	$ java -cp repos/command-line-app-1.0.jar Main

	or

	$ java -jar repos/command-line-app-1.0.jar

The `application` plugin enables you to run the app via `gradle run`.  You need to add the following to `build.gradle`.

```
apply plugin: 'application'
mainClassName = 'Main'
```

![](http://static-content-01.s3-website-us-east-1.amazonaws.com//command-line-app_—_bash_—_80×24_1B8E0B91.png)



