+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2016-03-18
description = ""
summary = "learning Node Odata"
draft = false
slug = "node-odata"
tags = ["github",]
title = "Node Odata"
repoFullName = "pfeilbr/node-odata-playground"
repoHTMLURL = "https://github.com/pfeilbr/node-odata-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/node-odata-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/node-odata-playground</a>
-->

## node-odata-playground

This is an example of a custom OData 4.0 provider that can be consumed by
salesforce [Lightning Connect](https://developer.salesforce.com/trailhead/en/lightning_connect/lightning_connect_introduction)

### Setup

```sh
$ npm install
```

### Running

```sh
$ node custom-odata-provider-example.js

# run ngrok to expose local server publicly
$ ngrok 1337
```

OData Endpoints you can visit

* <http://localhost:1337>
* <http://localhost:1337/$metadata>
* <http://localhost:1337/$metadata#PIMSProduct>
* <http://localhost:1337/PIMSProduct?$count=false>
* <http://localhost:1337/todos?$count=false>

Using `brian.pfeil.1@gmail.com` salesforce org.

**Screenshots**

**Query Example**

![](http://static-content-01.s3-website-us-east-1.amazonaws.com/Screenshot_3_17_16__5_15_PM_1C9B5623.png)

**External Data Source**

![](http://static-content-01.s3-website-us-east-1.amazonaws.com/External_Data_Source__Test___Salesforce_-_Developer_Edition_1C9B56D1.png)

**External Object**

![](http://static-content-01.s3-website-us-east-1.amazonaws.com/External_Object__todos___Salesforce_-_Developer_Edition_1C9B56F9.png)

**Filter Criteria / Where Clause**

![](http://static-content-01.s3-website-us-east-1.amazonaws.com/SoqlX___Brian_Pfeil__brian_pfeil_1_gmail_com_on_na15__and_node-odata-playground_—_node_custom-odata-provider-example_js_—_80×24_and_custom-odata-provider-example_js_—__Users_pfeilbr_Dropbox_mac01_Users_brianpfeil_projects_node-odata-playgro_1C9B5794.png)



