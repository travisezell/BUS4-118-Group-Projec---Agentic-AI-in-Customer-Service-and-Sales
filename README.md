# BUS4-118 Group Project: Agentic AI in Customer Service and Sales

## Overview
A multi-agent AI chatbot for **Golf Gear Pro**, an online golf equipment store. Built with LangChain, LangGraph, and Google Gemini, the system routes customer inquiries to specialized agents — each with a personality inspired by HAL 9000 (polite, competent, and just a touch condescending).

## Agents
| Agent | Notebook | What It Handles |
|-------|----------|-----------------|
| **Product Agent** | `code_03` | Golf product features, specs, pricing, and recommendations via RAG + pricing tool |
| **Order Agent** | `code_04` | Order lookups and status updates using `golf_orders.csv` |
| **Refund Agent** | `code_04` | Return/refund policy questions using hardcoded store policies |
| **Router Agent** | `code_06` | Receives all user input and routes to the correct specialist agent |

## Key Features
- **3 distinct inquiry types**: product Q&A, order management, refund/return policies
- **Conversation memory**: LangGraph `MemorySaver` preserves context across turns (e.g., "How much does it cost?" remembers which product you asked about)
- **LLM-based routing**: Router agent classifies each message and dispatches to the right specialist
- **Snarky HAL 9000 persona**: Every agent is helpful but can't resist a dry observation about your golf game

## Data Files
| File | Description |
|------|-------------|
| `data/golf_products.csv` | Product catalog: drivers, irons, balls, bags, gloves with prices and specs |
| `data/golf_orders.csv` | Sample orders with status tracking |
| `data/store_policies.txt` | Golf Gear Pro return, refund, shipping, and cancellation policies |

## Setup Instructions

### 1. Open in GitHub Codespaces (recommended)
1. Click the green **Code** button at the top of this repo
2. Click the **Codespaces** tab
3. Click **Create codespace on main**
4. Wait ~1 minute for the environment to load

### 2. Add your Google API key
- Go to [Google AI Studio](https://aistudio.google.com/app/apikeys) and create a free API key
- In GitHub, go to **Settings → Codespaces → Secrets** and add a secret named `GOOGLE_API_KEY`
- Make sure to give it access to this repository

## Running the Notebooks
Open each notebook and click **Run All**. Run them in order:
1. `code_03_XX Product QnA Agentic chatbot (1).ipynb` — sets up product agent
2. `code_04_XX Orders Chatbot with custom agent (1).ipynb` — sets up order + refund agents
3. `code_06_XX Multi-agent chatbots with routing.ipynb` — wires up the router and runs demos

## Interactive Chat App (Optional)
For a visual demo, run the Gradio chat interface:
```bash
pip install gradio
python app.py
```
This launches a web-based chat UI where you can talk to the router agent directly — much easier to demo than scrolling through notebook cells.

## Project Structure
```
├── code_03_XX Product QnA Agentic chatbot (1).ipynb   # Product agent
├── code_04_XX Orders Chatbot with custom agent (1).ipynb  # Order + refund agents
├── code_06_XX Multi-agent chatbots with routing.ipynb  # Router + multi-turn demo
├── app.py                                              # Gradio chat interface
├── data/
│   ├── golf_products.csv
│   ├── golf_orders.csv
│   └── store_policies.txt
└── README.md
```

## Architecture
```
User Input
    │
    ▼
┌─────────┐
│  Router  │ ← LLM classifies: PRODUCT / ORDER / REFUND / SMALLTALK
└────┬─────┘
     │
     ├──→ Product Agent  (RAG + pricing tool)
     ├──→ Order Agent    (CSV lookup + status update)
     ├──→ Refund Agent   (policy lookup tool)
     └──→ Small Talk     (HAL-flavored greeting)
```

## Team
BUS4-118S Section 02 — Group Project
