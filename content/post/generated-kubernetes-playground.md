+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2016-10-18
description = ""
summary = "learning Kubernetes"
draft = false
slug = "kubernetes"
tags = ["kubernetes","github",]
title = "Kubernetes"
repoFullName = "pfeilbr/kubernetes-playground"
repoHTMLURL = "https://github.com/pfeilbr/kubernetes-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/kubernetes-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/kubernetes-playground</a>
-->


learn kubernetes.  based on tutorial at <http://kubernetes.io/docs/tutorials/kubernetes-basics>

### Install and start [minikube](https://github.com/kubernetes/minikube)

```sh
$ cd ~/tmp
$ curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.11.0/minikube-darwin-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/

# verify install
$ minikube version

# start
$ minikube start
```

> minikube VMs, etc. are stored in `~/.minikube`


```sh
$ tree ~/.minikube

.
├── addons
├── apiserver.crt
├── apiserver.key
├── ca.crt
├── ca.key
├── ca.pem
├── cache
│   ├── iso
│   │   └── minikube-0.7.iso
│   └── localkube
├── cert.pem
├── certs
│   ├── ca-key.pem
│   ├── ca.pem
│   ├── cert.pem
│   └── key.pem
├── config
├── key.pem
└── machines
    ├── minikube
    │   ├── boot2docker.iso
    │   ├── config.json
    │   ├── disk.vmdk
    │   ├── id_rsa
    │   ├── id_rsa.pub
    │   └── minikube
    │       ├── Logs
    │       │   └── VBox.log
    │       ├── minikube.vbox
    │       └── minikube.vbox-prev
    ├── server-key.pem
    └── server.pem
```

### REST API

start proxy to allow access

```sh
$ kubectl proxy
```

Access API

```sh
$ curl http://127.0.0.1:8001/api
```

```json
{
  "kind": "APIVersions",
  "versions": [
    "v1"
  ],
  "serverAddressByClientCIDRs": [
    {
      "clientCIDR": "0.0.0.0/0",
      "serverAddress": "10.0.2.15:8443"
    }
  ]
}
```

* visit API endpoint at <http://127.0.0.1:8001/api>
* visit kubernetes-dashboard at <http://127.0.0.1:8001/api/v1/proxy/namespaces/kube-system/services/kubernetes-dashboard/#/workload?namespace=default>

## Accessing Services

The cluster ip address as exposed to host machine can be obtained via

```sh
$ kubectl cluster-info
```

![](http://static-content-01.s3-website-us-east-1.amazonaws.com/1__kubectl_proxy__kubectl__1DB53603.png)



