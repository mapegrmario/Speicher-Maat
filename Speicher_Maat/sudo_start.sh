#!/bin/bash
# sudo_start.sh – Speicher Maat mit Root-Rechten starten (via pkexec)

APP_DIR="$HOME/Speicher_Maat"
cd "$APP_DIR"

if [ -d "venv" ]; then
    PYTHON="$APP_DIR/venv/bin/python3"
else
    PYTHON="python3"
fi

# Q-8 FIX: Variablen in Anführungszeichen
pkexec env \
    DISPLAY="$DISPLAY" \
    XAUTHORITY="$XAUTHORITY" \
    HOME="$HOME" \
    PATH="$PATH" \
    "$PYTHON" "$APP_DIR/main.py"
