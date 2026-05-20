#!/usr/bin/env bash
set -e

python3 --version 2>&1 || { echo "Error: Python 3 is required"; exit 1; }

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

pip install --upgrade pip -q
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Copied .env.example to .env — fill in your API_ID, API_HASH, and PHONE before running."
    else
        echo "No .env found — create one with API_ID, API_HASH, and PHONE."
    fi
fi

if [ -z "$SESSION_STRING" ] && [ ! -f "session.session" ]; then
    echo ""
    echo "Warning: no Telethon session found."
    echo "  Run locally:  python export_session.py"
    echo "  Then set SESSION_STRING=<output> in your cloud environment."
fi

echo ""
echo "Setup complete."
echo "  List chats:      python extract.py --list"
echo "  Extract messages: python extract.py --chat 3 --limit 200"
