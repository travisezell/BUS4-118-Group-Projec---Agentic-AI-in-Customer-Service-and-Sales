# BUS4-118 Group Project: Agentic AI in Customer Service and Sales
> Note: This project was primarily developed and tested on the
> `ollama-defaults` branch using a local Ollama model.
## What This Repo Is
This project builds a Golf Gear Pro customer-service chatbot using LangGraph.

It has:
- Product Q&A agent (RAG + price lookup)
- Order agent (order lookup + status update)
- Refund agent (policy lookup)
- Router agent (routes each message to the right specialist)


## Running the Chatbot

This project can be run with cloud LLM APIs (OpenAI / Google) **or** fully
locally with Ollama.

### Recommended: Local Ollama (no API cost)

The LangGraph agents make multiple tool calls and multi‑turn passes through
the router and supervisor graphs, which can burn through API tokens very
quickly with cloud providers. To avoid that, the version used for development
runs entirely on a local Ollama model.

- Checkout the `ollama-defaults` branch:
  - `git checkout ollama-defaults`  # or: git switch ollama-defaults
- Install dependencies:
  - `pip install -r requirements.txt`
- Make sure Ollama is running locally (for example with `llama3.1:8b`)
- Run the notebooks:
  - `code_03_XX-Product-QnA-Agentic-chatbot-1.ipynb`
  - `code_04_XX-Orders-Chatbot-with-custom-agent-1.ipynb`
  - `code_06_XX-Multi-agent-chatbots-with-routing.ipynb`

On the `ollama-defaults` branch, `llm_provider_setup.py` is already configured
to use Ollama as the provider, so no API key is required.

### Optional: Cloud provider

If you want to use OpenAI or Google instead of Ollama, switch back to the
main branch and set the provider + API key in `llm_provider_setup.py`.
Be aware that long multi‑agent conversations with tools will consume tokens
and may incur cost.

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
