+++
author = "Brian Pfeil"
categories = ["Java", "playground"]
date = 2019-08-14
description = ""
summary = "learning Intellij Maven App"
draft = false
slug = "intellij-maven-app"
tags = ["github",]
title = "Intellij Maven App"
repoFullName = "pfeilbr/intellij-maven-app-playground"
repoHTMLURL = "https://github.com/pfeilbr/intellij-maven-app-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/intellij-maven-app-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/intellij-maven-app-playground</a>


example of IntelliJ Maven App

## Resources

* [Apache Maven Assembly Plugin / Usage](https://maven.apache.org/plugins/maven-assembly-plugin/usage.html)
---

```sh
# clean
mvn clean

# package with all dependencies and make .jar executable
# see `pom.xml` for details
mvn package

# run jar
java -jar ./target/app01-1.0-SNAPSHOT-jar-with-dependencies.jar
```


