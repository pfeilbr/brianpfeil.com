+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2019-08-05
description = ""
summary = "experimenting with Neo4j"
draft = false
slug = "neo4j"
tags = ["neo4j","github",]
title = "Neo4j"
repoFullName = "pfeilbr/neo4j-playground"
repoHTMLURL = "https://github.com/pfeilbr/neo4j-playground"
truncated = true

+++

<a href="https://github.com/pfeilbr/neo4j-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/neo4j-playground</a>


learn [neo4j](https://neo4j.com) graph database


## Example Session

```sh
# update
brew update

# install
brew install neo4j

# add neo4j binaries to path
export PATH="$PATH:/usr/local/Cellar/neo4j/3.5.8/bin"

# start server
neo4j start

# open web ui
open http://localhost:7474/

# it'll prompt for password on first time
# user and password is neo4j
# you then need to change the password

# open neo4j shell (Cypher Shell)
cypher-shell -u neo4j -p PASSWORD

# create nodes in shell
CREATE (p:Person {name:'brian'});
CREATE (p:Person {name:'tricia'});

# create relationship
MATCH (brian:Person {name:'brian'})
MATCH (tricia:Person {name:'tricia'})
CREATE (brian)-[:IS_MARRIED_TO]->(tricia)
CREATE (tricia)-[:IS_MARRIED_TO]->(brian);

# query `IS_MARRIED_TO` relationship
MATCH (p1:Person)-[rel:IS_MARRIED_TO]->(p2:Person)
RETURN p1 AS spouse1, p2 AS spouse2;


# clean up: delete all nodes and relationships
MATCH (n)
DETACH DELETE n;

# exit shell
:exit

# stop server
neo4j stop
```

---

**Web UI**

![](https://www.evernote.com/l/AAEzw2ySyp5Jv7e6bDQQrJocVkLMHq_l994B/image.png)

---

## Resources

* [neo4j documentation](https://neo4j.com/docs/)



