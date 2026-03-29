#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Missing virtual environment. Run: bash setup.sh"
  exit 1
fi

if [[ -z "${GOOGLE_API_KEY:-}" ]]; then
  echo "GOOGLE_API_KEY is not set. Export it before running notebooks."
  exit 1
fi

export GEMINI_MODEL="${GEMINI_MODEL:-gemini-1.5-flash}"
echo "Using model: $GEMINI_MODEL"

NOTEBOOKS=(
  "code_03_XX Product QnA Agentic chatbot (1).ipynb"
  "code_04_XX Orders Chatbot with custom agent (1).ipynb"
  "code_06_XX Multi-agent chatbots with routing.ipynb"
)

for nb in "${NOTEBOOKS[@]}"; do
  echo "Executing: $nb"
  "$PYTHON_BIN" -m jupyter nbconvert \
    --to notebook \
    --execute "$ROOT_DIR/$nb" \
    --output "/tmp/${nb%.ipynb}.executed.ipynb" \
    --ExecutePreprocessor.timeout=1200
  echo "Done: $nb"
  echo
 done

echo "All notebooks executed successfully."
