#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ ! -d ".venv" ]]; then
	echo "Creating virtual environment (.venv)..."
	python3 -m venv .venv
else
	echo "Using existing virtual environment (.venv)..."
fi

source .venv/bin/activate

echo "Installing/updating dependencies..."
python -m pip install -r requirements.txt

echo "Registering notebook kernel..."
python -m ipykernel install --sys-prefix --name bus4-venv --display-name "Python (.venv BUS4)"

echo "Setup complete."
echo "Open any .ipynb and select kernel: Python (.venv BUS4)"
