# LLM Provider Setup

Use this file as the single source of truth for notebook model setup.

Simple rule:
- In Codespaces, use `gemini` or `openai`.
- Use `ollama` only when running notebooks locally on your laptop.

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
Run this only when executing notebooks locally on your laptop.

Install and run Ollama, then pull models:

```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

## 5) Common errors
- `429 RESOURCE_EXHAUSTED`: cloud quota issue on your API key/project.
- Connection error with Ollama: make sure you are running notebook + Ollama in the same local environment.
