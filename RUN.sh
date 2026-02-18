#!/bin/bash
# Quick start script - Just double click or run ./RUN.sh

cd "$(dirname "$0")"

echo "⚽ Football Betting Predictions"
echo "==============================="
echo ""
echo "Starting web interface..."
echo "Please wait..."
echo ""

source .venv/bin/activate
python3 app.py

# Will open at http://localhost:7860
