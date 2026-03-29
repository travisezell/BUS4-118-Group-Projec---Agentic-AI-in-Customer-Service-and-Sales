#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is not installed." >&2
  exit 1
fi

if [[ ! -d "$VENV_DIR" ]]; then
  echo "Creating virtual environment in .venv..."
  python3 -m venv "$VENV_DIR"
fi

# If a stale venv exists without pip, recreate it cleanly.
if ! "$PYTHON_BIN" -m pip --version >/dev/null 2>&1; then
  echo "Existing .venv is missing pip; recreating .venv..."
  rm -rf "$VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

echo "Installing pinned dependencies..."
"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r "$ROOT_DIR/requirements.txt"

echo
echo "Setup complete."
echo "Run notebooks in order:"
echo "  1) code_03_XX Product QnA Agentic chatbot (1).ipynb"
echo "  2) code_04_XX Orders Chatbot with custom agent (1).ipynb"
echo "  3) code_06_XX Multi-agent chatbots with routing.ipynb"
