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

## Setup (Codespaces)
1. Set `GOOGLE_API_KEY` in Codespaces secrets for this repository.
2. Open this repository in GitHub Codespaces.
3. Open terminal in repo root and run:

```bash
bash scripts/setup_codespaces.sh
```

## Run Notebooks
Open any notebook (`.ipynb`) and choose kernel `Python (.venv BUS4)`.

Run notebooks in this order:
- `code_03_XX Product QnA Agentic chatbot (1).ipynb`
- `code_04_XX Orders Chatbot with custom agent (1).ipynb`
- `code_06_XX Multi-agent chatbots with routing.ipynb`

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