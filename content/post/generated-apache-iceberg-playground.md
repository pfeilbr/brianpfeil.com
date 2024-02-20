+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2024-02-13
description = ""
summary = " "
draft = false
slug = "apache-iceberg"
tags = ["db","spark","glue","emr",]
title = "Apache Iceberg"
repoFullName = "pfeilbr/apache-iceberg-playground"
repoHTMLURL = "https://github.com/pfeilbr/apache-iceberg-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/apache-iceberg-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/apache-iceberg-playground</a>
</div>


learn [Apache Iceberg](https://iceberg.apache.org/)

> Iceberg is a high-performance format for huge analytic tables. Iceberg brings the reliability and simplicity of SQL tables to big data, while making it possible for engines like Spark, Trino, Flink, Presto, Hive and Impala to safely work with the same tables, at the same time.


## concepts

- data lakehouse - data architecture that blends a data lake and data warehouse together

### data layer

- stores the actual data of the table and is primarily made up of the data files themselves, though also included are delete files and puffin files.
- Iceberg is file-format agnostic and currently supports Apache Parquet, Apache ORC, and Apache Avro
  - parquet is the most common underlying file format
- delete files - track which records in the dataset have been deleted
  - can either be a copy of the old file with the changes reflected in a new copy of it (called copy-on-write) or it can be a new file that only has the changes written, which then engines reading the data coalesce (called merge-on-read). 
  - two ways to identify a given row that needs to be removed from the logical dataset when an engine reads the dataset: either identify the row by its exact position in the dataset or identify the row by the values of one or more fields of the row.
    - positional delete files - denote what rows have been logically deleted
    - equality delete files - denote what rows have been logically deleted
- puffin file format - stores statistics and indexes about the data in the table that improve the performance of an even broader range of queries than the statistics stored in the data files and metadata files.

### metadata layer

- tree structure that tracks the data files and metadata about them as well as the operations that made them.
- made up of three file types, all of which are stored in data lake storage: manifest files, manifest lists, and metadata files
- enabling core features like time travel and schema evolution.
- Manifest files - keep track of files in the data layer (i.e., data files, delete files, and puffin files) as well as additional details and statistics about each file.
- manifest file keeps track of a subset of the data files. They contain information such as details about partition membership, record count, and lower and upper bounds of columns, that is used to improve efficiency and performance while reading the data from these data files.

### catalog

- central place where you go to find the current location of the current metadata pointer is the Iceberg catalog
- Within the catalog, there is a reference or pointer for each table to that table’s current metadata file.

---

## Diagrams

![iceberg architecture](https://www.evernote.com/shard/s1/sh/81d7554d-fa1c-4d1a-be1a-833b9df0cde3/u6hQptJNtZ33s_9_ZQlIalR4jICF6OteU-hx_8syAlDZuxG7Bmi4PuBA6Q/deep/0/image.png)

![parquet file architecture](https://www.evernote.com/shard/s1/sh/f4c5dc81-6f51-4635-8389-0fdd821afe5d/a0BbhK8nNbPYCKhMWtdAIcuTpUNpJqQrn9id2C1-TX2vmo_bUgqqYzK2Xg/deep/0/image.png)

![](https://www.evernote.com/shard/s1/sh/b749264e-d0ab-4592-8bf4-bb7b4ced5d24/yzCbADgRw2DFzIKviadqG2DDYWwg6gLsEb6bqGaxhEHOx0XAITrdMfv8TA/deep/0/image.png)

## resources

- [Apache Iceberg](https://iceberg.apache.org/)
- [Apache Iceberg: The Definitive Guide](https://learning.oreilly.com/library/view/apache-iceberg-the/9781098148614)


