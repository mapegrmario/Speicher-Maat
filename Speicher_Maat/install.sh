#!/bin/bash
# Installationsskript für Speicher Maat
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
APP_DIR="$HOME/Speicher_Maat"
VENV_DIR="$APP_DIR/venv"

if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}Dieses Skript sollte NICHT als root ausgeführt werden.${NC}"
    exit 1
fi

echo -e "${YELLOW}===================================================${NC}"
echo -e "${YELLOW}  Speicher Maat – Installation${NC}"
echo -e "${YELLOW}===================================================${NC}"
echo -e "Quelle:  $SCRIPT_DIR"
echo -e "Ziel:    $APP_DIR"
echo ""

# Python 3 prüfen
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}Python 3 ist nicht installiert.${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "Python: ${GREEN}$PYTHON_VERSION${NC} gefunden"
echo ""

# Optionale Systemtools prüfen
# FIX: lvm2 ist ein Paket, der Befehl heißt 'lvm'
echo -e "${YELLOW}Prüfe optionale Systemtools...${NC}"
declare -A TOOLS=(
    [ddrescue]="ddrescue"
    [rsync]="rsync"
    [testdisk]="testdisk"
    [photorec]="photorec"
    [shred]="shred"
    [nwipe]="nwipe"
    [mdadm]="mdadm"
    [lvm]="lvm2 (sudo apt install lvm2)"
)
for cmd in ddrescue rsync testdisk photorec shred nwipe mdadm lvm; do
    if command -v "$cmd" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $cmd"
    else
        label="${TOOLS[$cmd]:-$cmd}"
        echo -e "  ${RED}✗${NC} $label – nicht installiert (Funktion eingeschränkt)"
    fi
done
echo ""

# Verzeichnisse anlegen
mkdir -p "$APP_DIR/assets" "$APP_DIR/logs"

# Virtuelle Umgebung anlegen (nur wenn noch nicht vorhanden)
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Erstelle virtuelle Python-Umgebung...${NC}"
    python3 -m venv "$VENV_DIR"
else
    echo -e "${GREEN}Virtuelle Umgebung bereits vorhanden – wird übersprungen.${NC}"
fi

source "$VENV_DIR/bin/activate"
pip install --upgrade pip --quiet
pip install Pillow --quiet && \
    echo -e "  ${GREEN}✓${NC} Pillow (Avatar-Unterstützung)" || \
    echo -e "  ${RED}✗${NC} Pillow nicht installiert (Avatar deaktiviert)"
deactivate
echo ""

# FIX: Dateien nur kopieren wenn Quelle != Ziel
if [ "$SCRIPT_DIR" = "$APP_DIR" ]; then
    echo -e "${GREEN}Programmdateien bereits im Zielverzeichnis – kein Kopieren nötig.${NC}"
else
    echo -e "${YELLOW}Kopiere Programmdateien von $SCRIPT_DIR ...${NC}"
    for f in main.py config.py theme.py i18n.py logger.py utils.py widgets.py; do
        if [ -f "$SCRIPT_DIR/$f" ]; then
            cp "$SCRIPT_DIR/$f" "$APP_DIR/"
            echo -e "  ${GREEN}✓${NC} $f"
        else
            echo -e "  ${RED}✗${NC} $f nicht gefunden!"
        fi
    done
    for f in start.sh sudo_start.sh; do
        if [ -f "$SCRIPT_DIR/$f" ]; then
            cp "$SCRIPT_DIR/$f" "$APP_DIR/"
            chmod +x "$APP_DIR/$f"
            echo -e "  ${GREEN}✓${NC} $f"
        fi
    done
    if [ -d "$SCRIPT_DIR/assets" ]; then
        cp -r "$SCRIPT_DIR/assets/." "$APP_DIR/assets/"
        echo -e "  ${GREEN}✓${NC} assets/"
    fi
    [ -f "$SCRIPT_DIR/readme.md" ] && cp "$SCRIPT_DIR/readme.md" "$APP_DIR/"
fi

# Skripte ausführbar machen (auch bei In-Place-Installation)
chmod +x "$APP_DIR/start.sh" "$APP_DIR/sudo_start.sh" 2>/dev/null || true
echo ""

# Startmenüeintrag
MENU_DIR="$HOME/.local/share/applications"
mkdir -p "$MENU_DIR"
cat > "$MENU_DIR/speicher_maat.desktop" << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=Speicher Maat
GenericName=Disk Management Tool
Comment=Ergänzungs-Tool zu GParted & GNOME Disks
Exec=$APP_DIR/start.sh
Icon=$APP_DIR/assets/avatar.png
Terminal=false
Categories=System;Utility;
Path=$APP_DIR
StartupWMClass=speicher_maat
Keywords=disk;partition;backup;clone;lvm;raid;
EOL
chmod +x "$MENU_DIR/speicher_maat.desktop"
update-desktop-database "$MENU_DIR" 2>/dev/null || true

echo -e "${GREEN}===================================================${NC}"
echo -e "${GREEN}  Installation abgeschlossen!${NC}"
echo -e "${GREEN}===================================================${NC}"
echo -e "Starten:    bash $APP_DIR/start.sh"
echo -e "Mit Root:   bash $APP_DIR/sudo_start.sh"
echo ""
