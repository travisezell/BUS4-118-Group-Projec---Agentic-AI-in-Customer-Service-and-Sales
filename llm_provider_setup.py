from __future__ import annotations

import json
import os
from typing import Optional
from urllib.error import URLError
from urllib.request import Request, urlopen


def _apply_api_key_env(provider: str, api_key: Optional[str]) -> None:
    if not api_key or api_key.startswith("your_"):
        return
    if provider == "gemini":
        os.environ["GOOGLE_API_KEY"] = api_key
    elif provider == "openai":
        os.environ["OPENAI_API_KEY"] = api_key


def _validate_ollama_endpoint(base_url: str, model_name: str) -> None:
    base = base_url.rstrip("/")
    req = Request(f"{base}/api/tags", method="GET")

    try:
        with urlopen(req, timeout=5) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except URLError as exc:
        raise RuntimeError(
            "Cannot reach Ollama at "
            f"{base}. If you are in GitHub Codespaces, localhost points to the Codespace "
            "container, not your laptop. Run Ollama in the same environment, or set "
            "OLLAMA_BASE_URL to a reachable Ollama host."
        ) from exc

    available = {
        item.get("name", "")
        for item in payload.get("models", [])
        if isinstance(item, dict)
    }
    if model_name not in available:
        raise RuntimeError(
            f"Ollama is reachable at {base}, but model '{model_name}' is not installed. "
            "Run: ollama pull " + model_name
        )


def build_product_models(
    provider: str = "gemini",
    api_key: Optional[str] = None,
    model_name: Optional[str] = None,
    embedding_name: Optional[str] = None,
    ollama_base_url: str = "http://localhost:11434",
):
    """Return (chat_model, embedding_model, provider_name, model_name)."""
    provider_name = provider.strip().lower()
    _apply_api_key_env(provider_name, api_key)

    if provider_name == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

        chosen_model = model_name or "gemini-2.0-flash"
        chosen_embedding = embedding_name or "gemini-embedding-001"
        model = ChatGoogleGenerativeAI(
            model=chosen_model,
            temperature=0.0,
            max_output_tokens=256,
            timeout=20,
            max_retries=1,
        )
        embedding = GoogleGenerativeAIEmbeddings(model=chosen_embedding)
        return model, embedding, provider_name, chosen_model

    if provider_name == "openai":
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings

        chosen_model = model_name or "gpt-4o-mini"
        chosen_embedding = embedding_name or "text-embedding-3-small"
        model = ChatOpenAI(
            **{
                "model": chosen_model,
                "temperature": 0.0,
                "max_completion_tokens": 256,
                "timeout": 20,
                "max_retries": 1,
            }
        )
        embedding = OpenAIEmbeddings(model=chosen_embedding)
        return model, embedding, provider_name, chosen_model

    if provider_name == "ollama":
        from langchain_ollama import ChatOllama, OllamaEmbeddings

        chosen_model = model_name or "llama3.1:8b"
        chosen_embedding = embedding_name or "nomic-embed-text"
        _validate_ollama_endpoint(ollama_base_url, chosen_model)
        _validate_ollama_endpoint(ollama_base_url, chosen_embedding)
        model = ChatOllama(
            model=chosen_model,
            base_url=ollama_base_url,
            temperature=0.0,
        )
        embedding = OllamaEmbeddings(
            model=chosen_embedding,
            base_url=ollama_base_url,
        )
        return model, embedding, provider_name, chosen_model

    raise ValueError("provider must be one of: gemini, openai, ollama")


def build_chat_model(
    provider: str = "gemini",
    api_key: Optional[str] = None,
    model_name: Optional[str] = None,
    ollama_base_url: str = "http://localhost:11434",
):
    """Return (chat_model, provider_name, model_name)."""
    provider_name = provider.strip().lower()
    _apply_api_key_env(provider_name, api_key)

    if provider_name == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        chosen_model = model_name or "gemini-2.0-flash"
        model = ChatGoogleGenerativeAI(
            model=chosen_model,
            temperature=0.0,
            max_output_tokens=256,
            timeout=20,
            max_retries=1,
        )
        return model, provider_name, chosen_model

    if provider_name == "openai":
        from langchain_openai import ChatOpenAI

        chosen_model = model_name or "gpt-4o-mini"
        model = ChatOpenAI(
            **{
                "model": chosen_model,
                "temperature": 0.0,
                "max_completion_tokens": 256,
                "timeout": 20,
                "max_retries": 1,
            }
        )
        return model, provider_name, chosen_model

    if provider_name == "ollama":
        from langchain_ollama import ChatOllama

        chosen_model = model_name or "llama3.1:8b"
        _validate_ollama_endpoint(ollama_base_url, chosen_model)
        model = ChatOllama(
            model=chosen_model,
            base_url=ollama_base_url,
            temperature=0.0,
        )
        return model, provider_name, chosen_model

    raise ValueError("provider must be one of: gemini, openai, ollama")
