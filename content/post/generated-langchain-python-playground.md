+++
author = "Brian Pfeil"
categories = ["Jupyter Notebook", "playground"]
date = 2023-05-25
description = ""
summary = " "
draft = false
slug = "langchain-python"
tags = ["python","llm","genai"]
title = "LangChain Python"
repoFullName = "pfeilbr/langchain-python-playground"
repoHTMLURL = "https://github.com/pfeilbr/langchain-python-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/langchain-python-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/langchain-python-playground</a>
</div>


learn [LangChain (python)](https://python.langchain.com/)

## concepts


- **Agents** - use an LLM to determine which actions to take and in what order. An action can either be using a tool and observing its output, or returning to the user.

the llm is used to select the tool to use

`langchain/agents/agent.py` - `_call` method has main logic
`langchain/agents/types.py`
`langchain/agents/mrkl/prompt.py`
`langchain/agents/**/*prompt.py` - these contain all the prompts for different agents

## demo

```sh
pipenv shell
export OPENAI_API_KEY=...
export SERPAPI_API_KEY=...
jupyter lab
# visit `main.ipynb`
```

## resources

- [langchain-python](https://python.langchain.com/)
- [LangChain AI Handbook](https://www.pinecone.io/learn/langchain/) - great resource
