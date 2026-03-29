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
1. Set at least one key in Codespaces secrets for this repository.
2. Use `GOOGLE_API_KEY` for Gemini or `OPENAI_API_KEY` for OpenAI.
3. Open this repository in GitHub Codespaces.
4. Open terminal in repo root and run:

```bash
bash scripts/setup_codespaces.sh
```

## LLM Setup Reference
Use [SETUP_LLM.md](SETUP_LLM.md) for provider setup details.

## Choose LLM Provider In Notebook
1. Open the model setup cell near the top of each notebook.
2. In Codespaces, set `PROVIDER` to `gemini` or `openai`.
3. Set `API_KEY` to the matching cloud key.
4. Run the setup cell before running the rest of the notebook.

## Ollama (Local Only)
Use Ollama when running notebooks locally on your laptop, not in Codespaces.

1. Install and start Ollama on your laptop.
2. Pull recommended models:

```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

3. Run the repo locally and set `PROVIDER = "ollama"`.
4. Keep `OLLAMA_BASE_URL="http://localhost:11434"` unless you changed it.

## Run Notebooks
1. Open any notebook (`.ipynb`) and choose kernel `Python (.venv BUS4)`.
2. Run notebooks in this order:
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