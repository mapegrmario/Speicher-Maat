# Speicher Maat v1.0

**Ergänzungs-Tool zu GParted & GNOME Disks**

---

## Beschreibung

Speicher Maat ist ein fortschrittliches Werkzeug für Festplatten- und Speicherverwaltung unter Linux. Es ergänzt bestehende Tools wie GParted um Funktionen, die dort nicht vorhanden sind.

## Funktionen

| Tab | Funktion |
|-----|----------|
| **Klonen & Backup** | Festplatten 1:1 klonen mit ddrescue oder dd |
| **Datenmigration** | Dateien/Verzeichnisse mit rsync synchronisieren |
| **Datenrettung** | TestDisk (Partitionen) und PhotoRec (Dateien) |
| **Sicher löschen** | shred (GNU) und nwipe mit mehrfachen Durchgängen |
| **LVM** | Logical Volume Management: erstellen und vergrößern |
| **RAID** | Software-RAID mit mdadm verwalten |
| **Einstellungen** | Sprache (DE/EN), Design, Log-Level |

## Systemvoraussetzungen

- **Betriebssystem:** Ubuntu, Linux Mint, LMDE, Fedora, openSUSE, Arch, MX Linux
- **Python:** 3.6 oder neuer
- **tkinter:** Für die grafische Oberfläche

## Optionale Systemtools

Das Programm erkennt automatisch, welche Tools installiert sind:

```
sudo apt install ddrescue rsync testdisk shred nwipe mdadm lvm2
# oder
sudo dnf install ddrescue rsync testdisk nwipe mdadm lvm2
# oder
sudo pacman -S ddrescue rsync testdisk nwipe mdadm lvm2
```

Optional (für Avatar-Anzeige):
```
pip install Pillow
```

## Installation

```bash
# Installationsskript ausführen (NICHT als root!)
bash install.sh
```

Das Skript:
- Erstellt eine virtuelle Python-Umgebung in `~/Speicher_Maat/venv`
- Kopiert alle Programmdateien
- Erstellt einen Startmenüeintrag

## Starten

```bash
# Normal (ohne Root)
~/Speicher_Maat/start.sh

# Mit Root-Rechten (empfohlen für Disk-Operationen)
~/Speicher_Maat/sudo_start.sh

# Direkt (aus dem Projektverzeichnis)
cd ~/Speicher_Maat
source venv/bin/activate
python3 main.py
```

## Tastenkürzel

| Kürzel | Funktion |
|--------|----------|
| `F1` | Hilfe öffnen |
| `Strg+Q` | Beenden |
| `Strg+R` | Status-Toast |

## Projektstruktur

```
Speicher_Maat/
├── main.py        # Hauptfenster & alle Tabs
├── config.py      # Konstanten & Pfade
├── theme.py       # Farben & Schriften
├── i18n.py        # DE/EN Übersetzungen
├── logger.py      # Logging-System
├── utils.py       # Hilfsfunktionen
├── widgets.py     # Wiederverwendbare Widgets
├── install.sh     # Installationsskript
├── start.sh       # Startskript
├── sudo_start.sh  # Start mit Root-Rechten
├── assets/
│   └── avatar.png
└── logs/
    ├── analyse.log
    └── fehler.log
```

## Wichtige Hinweise

> ⚠️ **Immer Backups erstellen** vor Disk-Operationen!  
> ⚠️ **Root-Rechte** sind für die meisten Funktionen erforderlich.  
> ⚠️ **Klonen/Löschen** ist unwiderruflich – Datenverlust möglich!

## Sprache

- **Deutsch** (Standard)
- **English**

Umschalten: Tab „Einstellungen" → Sprache

## Autor

**Mario Peeß**  
Großenhain  
E-Mail: mapegr@mailbox.org

## Lizenz

GPLv3 – Dieses Programm ist freie Software.

## Haftungsausschluss

Die Verwendung erfolgt auf eigene Gefahr. Der Autor übernimmt keine Haftung für Datenverlust oder Hardwareschäden, die durch die Nutzung dieser Software entstehen.
