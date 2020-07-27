+++
author = "Brian Pfeil"
categories = ["Python", "playground"]
date = 2015-06-05
description = ""
summary = "learning Spark"
draft = false
slug = "spark"
tags = ["spark","playground",]
title = "Spark"
repoFullName = "pfeilbr/spark-playground"
repoHTMLURL = "https://github.com/pfeilbr/spark-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/spark-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/spark-playground</a>
-->


Project to learn and experiment with the [Spark](https://spark.apache.org) cluster computing system.

## Setup

spark installed at `~/dev/spark-2.2.0-bin-hadoop2.7` and is part of `PATH` in `.bash_profile`

	export SPARK_HOME=~/dev/spark-2.2.0-bin-hadoop2.7
	export PATH=$SPARK_HOME/bin:$PATH

## Running an example

	$ spark-submit dataframes-and-sql-examples.py

## Docker

	$ docker run -i -t -P --name spark -v /Users/pfeilbr/Dropbox/mac01/Users/brianpfeil/projects/spark-playground:/src sequenceiq/spark:latest bash

## Resources

* [Spark Documentation](https://spark.apache.org/docs/latest/)



