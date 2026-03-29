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
2. Use `GOOGLE_API_KEY` for Gemini, `OPENAI_API_KEY` for OpenAI, or use local Ollama with no cloud key.
3. Open this repository in GitHub Codespaces.
4. Open terminal in repo root and run:

```bash
bash scripts/setup_codespaces.sh
```

## Choose LLM Provider In Notebook
1. Open the model setup cell near the top of each notebook.
2. Keep exactly one provider block uncommented and keep the other two commented.
3. Gemini block: replace `your_gemini_api_key_here`.
4. OpenAI block: replace `your_openai_api_key_here`.
5. Ollama block: set `OLLAMA_BASE_URL` and make sure Ollama is running.
6. Run the setup cell before running the rest of the notebook.

## Ollama Local Setup
1. Install Ollama on your machine.
2. Start Ollama server.
3. Pull recommended models:

```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

4. In notebook setup cell, uncomment the Ollama block and comment out Gemini/OpenAI blocks.
5. Use `OLLAMA_BASE_URL="http://localhost:11434"` unless your Ollama server runs elsewhere.

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