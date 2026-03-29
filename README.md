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
- Use GitHub Codespaces for this project.
- GitHub account with access to this repository.
- Gemini API key set as `GOOGLE_API_KEY`.

## Setup And Run
1. Open this repository in a GitHub Codespace.
2. Open a terminal in the repo root and run:

```bash
python3 -m venv .venv && \
source .venv/bin/activate && \
python -m pip install --upgrade pip && \
python -m pip install -r requirements.txt && \
python -m ipykernel install --sys-prefix --name bus4-venv --display-name "Python (.venv BUS4)" && \
export GOOGLE_API_KEY="your_api_key_here" && \
jupyter notebook
```

3. In Jupyter or VS Code, choose kernel `Python (.venv BUS4)`.

4. Run notebooks in this order:
- `code_03_XX Product QnA Agentic chatbot (1).ipynb`
- `code_04_XX Orders Chatbot with custom agent (1).ipynb`
- `code_06_XX Multi-agent chatbots with routing.ipynb`

If no API key is set, notebook/chat runs will fail until `GOOGLE_API_KEY` (or `GEMINI_API_KEY`) is provided.

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