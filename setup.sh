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

echo "Installing pinned dependencies..."
"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r "$ROOT_DIR/requirements.txt"

echo
if [[ -z "${GOOGLE_API_KEY:-}" ]]; then
  echo "Warning: GOOGLE_API_KEY is not set. The app will not work until it is configured."
fi

echo "Setup complete."
echo "Run the app with: $PYTHON_BIN $ROOT_DIR/app.py"
