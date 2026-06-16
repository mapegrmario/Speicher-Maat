#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Konfiguration und Konstanten für Speicher Maat"""
import os

VERSION = "1.0.0"
APP_NAME = "Speicher Maat"
AUTHOR = "Mario Peeß / Großenhain"
EMAIL = "mapegr@mailbox.org"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
AVATAR_PATH = os.path.join(ASSETS_DIR, "avatar.png")

FEHLER_LOG = os.path.join(LOGS_DIR, "fehler.log")
ANALYSE_LOG = os.path.join(LOGS_DIR, "analyse.log")

LC_ENV = {**os.environ, "LC_ALL": "C", "LANG": "C"}

HAFTUNGSAUSSCHLUSS = """
WICHTIGER HAFTUNGSAUSSCHLUSS:

Die Verwendung dieses Programms erfolgt auf eigene Gefahr.
Der Autor übernimmt keine Haftung für Datenverlust,
Hardwareschäden oder sonstige Schäden, die durch die
Nutzung dieser Software entstehen können.

Erstellen Sie immer Backups wichtiger Daten bevor Sie
Festplatten-Operationen durchführen!
"""

DRITTANBIETER = """
Dieses Programm nutzt folgende externe Tools:
- ddrescue - GNU Data Recovery Tool
- TestDisk/PhotoRec - Datenrettung
- rsync - Dateisynchronisation
- LVM2 - Logical Volume Manager
- mdadm - RAID Management
- shred/nwipe - Sicheres Löschen
"""
