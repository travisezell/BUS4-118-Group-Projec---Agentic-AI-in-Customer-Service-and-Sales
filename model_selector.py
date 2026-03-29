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
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash",
    ]
    if preferred:
        return [preferred] + [m for m in defaults if m != preferred]
    return defaults


def select_best_gemini_model(
    candidates: Iterable[str] | None = None,
    require_tools: bool = True,
    temperature: float = 0.0,
    max_output_tokens: int = 256,
    request_timeout: float = 20.0,
    max_retries: int = 1,
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
                timeout=request_timeout,
                max_retries=max_retries,
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
    lowered = joined.lower()

    diagnostics: list[str] = []
    if "resource_exhausted" in lowered or "quota exceeded" in lowered or " 429 " in lowered:
        diagnostics.append(
            "Detected quota/rate-limit failure (429 RESOURCE_EXHAUSTED). "
            "Verify your Gemini API quota/billing and retry after cooldown."
        )
    if "not_found" in lowered or " is not found" in lowered:
        diagnostics.append(
            "Detected unavailable/deprecated model name(s). "
            "Update GEMINI_MODEL or candidates to currently supported models."
        )

    diagnostic_text = ""
    if diagnostics:
        diagnostic_text = "\n\nDiagnostics:\n- " + "\n- ".join(diagnostics)

    raise RuntimeError(
        "No compatible Gemini model is available. Tried:\n" + joined + diagnostic_text
    )
