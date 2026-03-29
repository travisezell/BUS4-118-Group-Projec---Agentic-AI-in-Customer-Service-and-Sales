# LLM Provider Setup

Use this file as the single source of truth for notebook model setup.

## 1) Install dependencies
Run from repo root:

```bash
bash scripts/setup_codespaces.sh
```

## 2) Pick one provider per notebook run
- `gemini`
- `openai`
- `ollama`

## 3) In each notebook setup cell
Set these values at the top of the cell:

```python
PROVIDER = "gemini"  # "gemini" | "openai" | "ollama"
API_KEY = "your_key_here"  # use real key for gemini/openai; set None for ollama
MODEL_NAME = None  # optional override
OLLAMA_BASE_URL = "http://localhost:11434"  # only for ollama
```

Notes:
- Gemini uses `GOOGLE_API_KEY`.
- OpenAI uses `OPENAI_API_KEY`.
- Ollama runs locally and does not need cloud API keys.

## 4) Ollama local prerequisites
Install and run Ollama, then pull models:

```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

Important for Codespaces:
- In GitHub Codespaces, `http://localhost:11434` points to the Codespace container, not your laptop.
- If Ollama runs on your laptop, use a reachable host URL in `OLLAMA_BASE_URL`, or run Ollama in the same environment as the notebook.

## 5) Common errors
- `429 RESOURCE_EXHAUSTED`: cloud quota issue on your API key/project.
- Connection error with Ollama: verify server is running and reachable from where the notebook is running.
