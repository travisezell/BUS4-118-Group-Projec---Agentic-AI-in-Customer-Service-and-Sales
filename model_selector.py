from __future__ import annotations

import os
from typing import Iterable

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool


@tool
def _model_probe_tool(text: str) -> str:
    """Small no-op tool used to verify model tool-calling compatibility."""
    return f"probe:{text}"


def _default_candidates() -> list[str]:
    preferred = os.getenv("GEMINI_MODEL", "").strip()
    defaults = [
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ]
    if preferred:
        return [preferred] + [m for m in defaults if m != preferred]
    return defaults


def select_best_gemini_model(
    candidates: Iterable[str] | None = None,
    require_tools: bool = True,
    temperature: float = 0.0,
    max_output_tokens: int = 256,
    debug: bool = True,
):
    """
    Return (model, model_name) for the first healthy model.

    Health check:
    1) plain invoke works
    2) if require_tools=True, bind_tools path also works

    Token control:
    - max_output_tokens limits response length to reduce per-call token usage.
    """
    model_names = list(candidates) if candidates is not None else _default_candidates()
    errors: list[str] = []

    for name in model_names:
        try:
            llm = ChatGoogleGenerativeAI(
                model=name,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
            )

            # Basic reachability probe.
            _ = llm.invoke("Reply with exactly OK")

            if require_tools:
                # Tool-binding probe to catch model compatibility issues early.
                tool_llm = llm.bind_tools([_model_probe_tool])
                _ = tool_llm.invoke("Reply with exactly OK")

            if debug:
                print(f"Using model: {name}")
            return llm, name
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: {exc}")
            if debug:
                print(f"Model failed: {name} -> {exc}")

    joined = "\n".join(errors)
    raise RuntimeError(
        "No compatible Gemini model is available. Tried:\n" + joined
    )
