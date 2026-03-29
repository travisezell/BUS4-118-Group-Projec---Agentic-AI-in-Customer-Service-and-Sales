# BUS4-118 Group Project: Agentic AI in Customer Service and Sales

## What This Repo Is
This project builds a Golf Gear Pro customer-service chatbot using LangGraph.

It has:
- Product Q&A agent (RAG + price lookup)
- Order agent (order lookup + status update)
- Refund agent (policy lookup)
- Router agent (routes each message to the right specialist)

## Files You Actually Run
- `code_03_XX Product QnA Agentic chatbot (1).ipynb`: product agent
- `code_04_XX Orders Chatbot with custom agent (1).ipynb`: order + refund agents
- `code_06_XX Multi-agent chatbots with routing.ipynb`: router + multi-agent flow

## Requirements
- Use this repository in GitHub Codespaces.
- Set `GOOGLE_API_KEY` in your Codespaces secrets.

## Teammate Quick Start (Codespaces)
1. Open this workspace in GitHub Codespaces.
2. Open terminal in repo root and run:

```bash
bash scripts/setup_codespaces.sh
```

3. Open any notebook (`.ipynb`) and choose kernel `Python (.venv BUS4)`.

4. Run notebooks in this order:
- `code_03_XX Product QnA Agentic chatbot (1).ipynb`
- `code_04_XX Orders Chatbot with custom agent (1).ipynb`
- `code_06_XX Multi-agent chatbots with routing.ipynb`

Notes:
- This setup works in VS Code notebooks and browser Jupyter notebooks.
- If you want browser Jupyter, run `source .venv/bin/activate && jupyter notebook`.
- If no API key is set, notebook/chat runs will fail until `GOOGLE_API_KEY` is provided.

## Current Architecture
`Router` classifies user input into one route:
- `PRODUCT` -> Product agent
- `ORDER` -> Order agent
- `REFUND` -> Refund agent
- `SMALLTALK` -> small talk response
- `END` -> stop

Each specialist uses tools and memory (`MemorySaver`) with thread-based conversation state.


## Data
- `data/golf_products.csv`
- `data/golf_orders.csv`
- `data/store_policies.txt`

## Team
BUS4-118S Section 02 - Group Project
Travis Ezell - All Coding 