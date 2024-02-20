+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2024-02-20
description = ""
summary = " "
draft = false
slug = "apache-kafka"
tags = ["streaming",]
title = "Apache Kafka"
repoFullName = "pfeilbr/apache-kafka-playground"
repoHTMLURL = "https://github.com/pfeilbr/apache-kafka-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/apache-kafka-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/apache-kafka-playground</a>
</div>


learn [APACHE KAFKA](https://kafka.apache.org/)

Kafka three key capabilities:

1. To **publish** (write) and **subscribe to** (read) streams of events, including continuous import/export of your data from other systems.
2. To **store** streams of events durably and reliably for as long as you want.
3. To **process** streams of events as they occur or retrospectively.

## concepts

### [KAFKA CONNECT](https://kafka.apache.org/documentation/#connect)

tool for scalably and reliably streaming data between Apache Kafka and other systems. It makes it simple to quickly define _connectors_ that move large collections of data into and out of Kafka.

### [KAFKA STREAMS](https://kafka.apache.org/36/documentation/streams/)

client library for building real-time applications, where the input and/or output data is stored in Kafka clusters. Kafka Streams combines the simplicity of writing and deploying standard Java and Scala applications on the client side with the benefits of Kafka's server-side cluster technology to make these applications highly scalable, elastic, fault-tolerant, distributed, and much more

<https://github.com/apache/kafka/blob/3.6/streams/examples/src/main/java/org/apache/kafka/streams/examples/wordcount/WordCountDemo.java>

## resources

- [kafka introduction](https://kafka.apache.org/intro)
- [APACHE KAFKA QUICKSTART](https://kafka.apache.org/quickstart)


