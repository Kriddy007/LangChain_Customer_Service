# LangChain Customer Service Agent

A conversational AI agent built with LangChain and Groq that handles customer service queries with memory and tool calling.

## What it does

- Maintains conversation history across multiple messages
- Automatically decides which tool to use based on the query
- Gives complete, context-aware responses

## Tools

| Tool | Trigger | What it does |
|---|---|---|
| check_refund_status | Transaction ID (TXN001 etc.) | Returns current refund status |
| get_account_status | Account ID (ACC001 etc.) | Returns current account status |

## Setup

```bash
pip install langchain langchain-groq langchain-core
```

Add your Groq API key in the LLM setup cell. Get a free key at https://console.groq.com

```bash
python langchain-customer-agent.py
```

## Sample Output
