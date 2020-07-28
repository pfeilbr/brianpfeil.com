+++
author = "Brian Pfeil"
categories = ["TypeScript", "playground"]
date = 2018-04-30
description = ""
summary = " "
draft = false
slug = "graphql"
tags = ["graphql","playground",]
title = "GraphQL"
repoFullName = "pfeilbr/graphql-playground"
repoHTMLURL = "https://github.com/pfeilbr/graphql-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/graphql-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/graphql-playground</a>
</div>


project to learn and experiment with [graphql](https://graphql.org/) using [Apollo](https://www.apollographql.com/)

## server

- location - `src/server'
- entrypoint - `src/server/index.ts`
- dev (reload on change) - `npm run dev`
- run - `npm start`

## client

- location - `src/client'
- entrypoint - `src/client/App.tsx`
- run - `npm start`

> ensure server is running on port 3000

## Examples

Run via GraphiQL @ <http://localhost:3000/graphiql>

```js
query {
  books {
    id,
    title,
    author
  }
}

mutation {
  createBook(title: "How To", author: "John Doe") {
    id,
    title
    author
  }
}

subscription onBookAdded {
  bookAdded {
    id
    title
    author
  }
}
```

## Screenshots

subscriptiion push over websocket

![](https://www.evernote.com/l/AAEb4fvY3TtOUK1cIiahAMyfy3Hg1dv2l60B/image.png)

## Scratch

```



```



