#!/bin/bash
# start.sh – Speicher Maat starten

APP_DIR="$HOME/Speicher_Maat"
cd "$APP_DIR" || { echo "Verzeichnis $APP_DIR nicht gefunden!"; exit 1; }

if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 main.py
