+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2017-01-17
description = ""
summary = " "
draft = false
slug = "ethereum"
tags = ["playground",]
title = "Ethereum"
repoFullName = "pfeilbr/ethereum-playground"
repoHTMLURL = "https://github.com/pfeilbr/ethereum-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/ethereum-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/ethereum-playground</a>
</div>


learn and experiment with [Ethereum](https://www.ethereum.org/) decentralized blockchain based platform

## TODO

* walk all the testnet transaction and get counts of the addresses to see which addresses produce the most transactions
* walk all testnet transactions and plot transaction count over time for the top X% of addresses that produce the most transactions

## Files and Directories of Interest

**Production**

```sh
~/Library/Ethereum
~/Library/Ethereum/geth/chaindata
```

**TEST-NET**

```sh
~/Library/Ethereum/testnet
~/Library/Ethereum/testnet/geth/chaindata
```

## Ethereum Wallet

Ethereum Wallet Screenshot

![](http://static-screenshots-01.s3-website-us-east-1.amazonaws.com/Ethereum_Wallet_1E2DB8EC.png)

## [Geth](https://github.com/ethereum/go-ethereum/wiki/geth) CLI

command line interface for running a full ethereum node

```sh
# attach to existing geth instance (e.g. Ethereum Wallet GUI app's geth instance). opens up a javascript repl
geth attach

# js console
geth console

# open testnet console
geth --testnet console
```

## Ethereum Block Explorer

* production - <https://etherscan.io/>
* testnet - <https://testnet.etherscan.io/>

## [Ethereum Javascript API](https://github.com/ethereum/web3.js)

* [Web3 JavaScript Ðapp API](https://github.com/ethereum/wiki/wiki/JavaScript-API)
* [web3.js](https://github.com/ethereum/web3.js) npm module



