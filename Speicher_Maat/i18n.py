#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Internationalisierung - Deutsch/Englisch"""

TRANSLATIONS = {
    "de": {
        "app_title":        "Speicher Maat",
        "menu_file":        "Datei",
        "menu_help":        "Hilfe",
        "menu_settings":    "Einstellungen",
        "menu_about":       "Über",
        "menu_exit":        "Beenden",
        "tab_clone":        "Klonen & Backup",
        "tab_migrate":      "Datenmigration",
        "tab_recovery":     "Datenrettung",
        "tab_wipe":         "Sicher löschen",
        "tab_lvm":          "LVM",
        "tab_raid":         "RAID",
        "tab_about":        "Über",
        "tab_help":         "Hilfe",
        "tab_settings":     "Einstellungen",
        "btn_start":        "Starten",
        "btn_stop":         "Stopp",
        "btn_refresh":      "Aktualisieren",
        "btn_close":        "Schließen",
        "label_source":     "Quelle:",
        "label_target":     "Ziel:",
        "label_disk":       "Laufwerk:",
        "label_output":     "Ausgabe:",
        "label_method":     "Methode:",
        "label_passes":     "Durchgänge:",
        "label_device_opt": "Laufwerk (optional):",
        "log_clear":        "Leeren",
        "log_copy":         "Kopieren",
        "log_copied":       "In Zwischenablage kopiert",
        # Clone
        "clone_title":      "Festplatte klonen (ddrescue)",
        "clone_ddrescue":   "ddrescue (sicherer, empfohlen)",
        "clone_start":      "Klonen starten",
        "clone_select":     "Bitte Quelle und Ziel wählen",
        "clone_same":       "Quelle und Ziel müssen unterschiedlich sein!",
        "clone_confirm":    "Quelle: {src}\nZiel: {dst}\n\nALLE DATEN AUF DEM ZIEL WERDEN GELÖSCHT!",
        # Migrate
        "migrate_title":        "Dateien übertragen (rsync)",
        "migrate_mirror":       "Spiegel (--delete)",
        "migrate_dryrun":       "Trockenlauf",
        "migrate_hardlinks":    "Hardlinks erhalten (-H)",
        "migrate_select":       "Bitte Quell- und Zielverzeichnis angeben",
        "migrate_src_missing":  "Quellverzeichnis nicht gefunden: {path}",
        "migrate_dst_missing":  "Zielverzeichnis nicht gefunden: {path}",
        # Recovery
        "recovery_testdisk":    "TestDisk starten",
        "recovery_photorec":    "PhotoRec starten",
        "recovery_grub":        "GRUB installieren",
        "recovery_td_title":    "TestDisk - Partitionen wiederherstellen",
        "recovery_td_desc":     "Stellt gelöschte Partitionen wieder her.\nRepariert Bootsektoren und Partitionstabellen.",
        "recovery_pr_title":    "PhotoRec - Dateien wiederherstellen",
        "recovery_pr_desc":     "Stellt verlorene Dateien aus dem freien Speicher wieder her.\nZielverzeichnis muss auf einer ANDEREN Partition liegen!",
        "recovery_boot_title":  "Bootsektor reparieren",
        "recovery_no_disk":     "Ohne Vorgabe starten",
        "recovery_grub_confirm": "GRUB auf {disk} installieren?",
        "recovery_grub_title":  "GRUB installieren",
        "recovery_td_missing":  "testdisk nicht installiert. sudo apt install testdisk",
        "recovery_pr_missing":  "photorec nicht installiert. sudo apt install testdisk",
        "recovery_info":        "TestDisk und PhotoRec sind interaktive Terminal-Programme.\nSie werden in einem eigenen Terminal-Fenster gestartet.\nBitte WICHTIGE DATEN vorher sichern!",
        # Wipe
        "wipe_title":       "Laufwerk sicher überschreiben",
        "wipe_warning":     "UNWIDERRUFLICH - alle Daten werden gelöscht!",
        "wipe_start":       "LÖSCHEN STARTEN",
        "wipe_select":      "Bitte Laufwerk wählen",
        "wipe_zero":        "Abschließend mit Nullen (-z)",
        "wipe_verbose":     "Fortschritt anzeigen (-v)",
        "wipe_confirm1":    "Löschen bestätigen",
        "wipe_msg1":        "Laufwerk: {disk}\nALLE DATEN WERDEN UNWIDERRUFLICH GELÖSCHT!\nSind Sie WIRKLICH sicher?",
        # LVM
        "lvm_status_btn":   "Status aktualisieren",
        "lvm_create_title": "LVM erstellen (PV → VG → LV)",
        "lvm_extend_title": "Logical Volume vergrößern",
        "lvm_pv_label":     "Physical Volume (z.B. /dev/sdb):",
        "lvm_vg_label":     "Volume Group Name (z.B. myvg):",
        "lvm_lv_label":     "Logical Volume Name (z.B. data):",
        "lvm_size_label":   "Größe (z.B. 10G, 500M):",
        "lvm_fs_label":     "Dateisystem formatieren:",
        "lvm_lv_path":      "LV-Pfad (z.B. /dev/myvg/data):",
        "lvm_ext_size":     "Größe (z.B. +5G):",
        "lvm_resize_fs":    "Dateisystem anpassen",
        "lvm_extend_btn":   "Vergrößern",
        "lvm_create_btn":   "LVM erstellen",
        "lvm_fill_all":     "Bitte alle Felder ausfüllen",
        "lvm_fill_path":    "LV-Pfad und Größe angeben",
        "lvm_done":         "\nLVM vollständig erstellt.\n",
        "lvm_err":          "\nFehler bei: {cmd}\n",
        # RAID
        "raid_status_title": "RAID-Status",
        "raid_create_title": "RAID erstellen (mdadm)",
        "raid_devs_label":   "Devices (leerzeichen-getrennt):",
        "raid_level_label":  "RAID-Level:",
        "raid_name_label":   "MD-Device-Name:",
        "raid_create_btn":   "RAID erstellen",
        "raid_stop_btn":     "RAID stoppen",
        "raid_detail_btn":   "anzeigen",
        "raid_detail_label": "Details für:",
        "raid_min_devs":     "RAID-{level} benötigt mindestens {n} Devices!",
        "raid_confirm":      "RAID-{level} auf {md}\nDevices: {devs}\nFortfahren?",
        "raid_stop_confirm": "RAID {md} stoppen?",
        # Settings
        "settings_title":       "Einstellungen",
        "settings_language":    "Sprache:",
        "settings_theme":       "Design:",
        "settings_log_level":   "Log-Level:",
        "settings_general":     "Allgemein",
        "settings_lang_changed":"Sprache geändert – Neustart erforderlich",
        # About
        "about_title":      "Über Speicher Maat",
        "about_version":    "Version",
        "about_author":     "Autor",
        "about_email":      "E-Mail",
        "about_disclaimer": "Haftungsausschluss",
        "about_third_party":"Drittanbieter",
        # Help
        "help_title":       "Hilfe",
        # Messages
        "msg_confirm":      "Bestätigung erforderlich",
        "msg_error":        "Fehler",
        "msg_success":      "Erfolgreich",
        "msg_warning":      "Warnung",
        "msg_info":         "Information",
        "msg_running":      "Eine Operation läuft bereits",
        "msg_completed":    "Abgeschlossen",
        "msg_failed":       "Fehler aufgetreten",
        "msg_root_warn":    "Root-Rechte empfohlen!",
        "msg_refreshed":    "Aktualisiert",
        "msg_quit":         "Wirklich beenden?",
        "msg_disk_select":  "Bitte Laufwerk wählen",
        # Help content
        "help_content": """\
Speicher Maat – Hilfe

Dieses Tool ergänzt GParted und GNOME Disks um fortgeschrittene Funktionen:

KLONEN & BACKUP
  Klont Festplatten 1:1 mit ddrescue (empfohlen) oder dd.
  ddrescue ist fehlertolerant und ideal für defekte Laufwerke.

DATENMIGRATION
  Überträgt Verzeichnisse mit rsync.
  • Spiegel-Modus (--delete): Ziel wird identisch zur Quelle.
  • Trockenlauf: Zeigt was passieren würde, ohne zu kopieren.

DATENRETTUNG
  • TestDisk: Gelöschte Partitionen und Bootsektoren reparieren.
  • PhotoRec: Dateien aus freiem Speicher wiederherstellen.
  → Beide starten in einem eigenen Terminalfenster.

SICHER LÖSCHEN
  • shred: Überschreibt Daten mehrfach (GNU coreutils).
  • nwipe: Interaktives Tool mit NIST-konformen Verfahren.

LVM – LOGICAL VOLUME MANAGEMENT
  Erstellt und vergrößert LVM-Volumes.

RAID
  Erstellt und verwaltet Software-RAID mit mdadm.

TASTENKÜRZEL
  F1          Hilfe öffnen
  Strg+Q      Beenden
  Strg+R      Aktualisieren

Für detaillierte Anleitungen siehe README.md
""",
    },

    "en": {
        "app_title":        "Speicher Maat",
        "menu_file":        "File",
        "menu_help":        "Help",
        "menu_settings":    "Settings",
        "menu_about":       "About",
        "menu_exit":        "Exit",
        "tab_clone":        "Clone & Backup",
        "tab_migrate":      "Data Migration",
        "tab_recovery":     "Data Recovery",
        "tab_wipe":         "Secure Wipe",
        "tab_lvm":          "LVM",
        "tab_raid":         "RAID",
        "tab_about":        "About",
        "tab_help":         "Help",
        "tab_settings":     "Settings",
        "btn_start":        "Start",
        "btn_stop":         "Stop",
        "btn_refresh":      "Refresh",
        "btn_close":        "Close",
        "label_source":     "Source:",
        "label_target":     "Target:",
        "label_disk":       "Disk:",
        "label_output":     "Output:",
        "label_method":     "Method:",
        "label_passes":     "Passes:",
        "label_device_opt": "Disk (optional):",
        "log_clear":        "Clear",
        "log_copy":         "Copy",
        "log_copied":       "Copied to clipboard",
        # Clone
        "clone_title":      "Clone Disk (ddrescue)",
        "clone_ddrescue":   "ddrescue (safer, recommended)",
        "clone_start":      "Start Cloning",
        "clone_select":     "Please select source and target",
        "clone_same":       "Source and target must be different!",
        "clone_confirm":    "Source: {src}\nTarget: {dst}\n\nALL DATA ON TARGET WILL BE DELETED!",
        # Migrate
        "migrate_title":        "Transfer Files (rsync)",
        "migrate_mirror":       "Mirror (--delete)",
        "migrate_dryrun":       "Dry Run",
        "migrate_hardlinks":    "Preserve Hardlinks (-H)",
        "migrate_select":       "Please specify source and target directory",
        "migrate_src_missing":  "Source directory not found: {path}",
        "migrate_dst_missing":  "Target directory not found: {path}",
        # Recovery
        "recovery_testdisk":    "Start TestDisk",
        "recovery_photorec":    "Start PhotoRec",
        "recovery_grub":        "Install GRUB",
        "recovery_td_title":    "TestDisk – Restore Partitions",
        "recovery_td_desc":     "Recovers deleted partitions.\nRepairs boot sectors and partition tables.",
        "recovery_pr_title":    "PhotoRec – Recover Files",
        "recovery_pr_desc":     "Recovers lost files from free disk space.\nTarget directory must be on a DIFFERENT partition!",
        "recovery_boot_title":  "Repair Boot Sector",
        "recovery_no_disk":     "Start without preset",
        "recovery_grub_confirm":"Install GRUB on {disk}?",
        "recovery_grub_title":  "Install GRUB",
        "recovery_td_missing":  "testdisk not installed. sudo apt install testdisk",
        "recovery_pr_missing":  "photorec not installed. sudo apt install testdisk",
        "recovery_info":        "TestDisk and PhotoRec are interactive terminal programs.\nThey will be started in a separate terminal window.\nPlease back up IMPORTANT DATA first!",
        # Wipe
        "wipe_title":       "Secure Wipe Disk",
        "wipe_warning":     "IRREVERSIBLE – all data will be deleted!",
        "wipe_start":       "START WIPING",
        "wipe_select":      "Please select a disk",
        "wipe_zero":        "Final zero pass (-z)",
        "wipe_verbose":     "Show progress (-v)",
        "wipe_confirm1":    "Confirm Deletion",
        "wipe_msg1":        "Disk: {disk}\nALL DATA WILL BE IRREVERSIBLY DELETED!\nAre you REALLY sure?",
        # LVM
        "lvm_status_btn":   "Refresh Status",
        "lvm_create_title": "Create LVM (PV → VG → LV)",
        "lvm_extend_title": "Extend Logical Volume",
        "lvm_pv_label":     "Physical Volume (e.g. /dev/sdb):",
        "lvm_vg_label":     "Volume Group Name (e.g. myvg):",
        "lvm_lv_label":     "Logical Volume Name (e.g. data):",
        "lvm_size_label":   "Size (e.g. 10G, 500M):",
        "lvm_fs_label":     "Format filesystem:",
        "lvm_lv_path":      "LV path (e.g. /dev/myvg/data):",
        "lvm_ext_size":     "Size (e.g. +5G):",
        "lvm_resize_fs":    "Resize filesystem",
        "lvm_extend_btn":   "Extend",
        "lvm_create_btn":   "Create LVM",
        "lvm_fill_all":     "Please fill in all fields",
        "lvm_fill_path":    "Enter LV path and size",
        "lvm_done":         "\nLVM created successfully.\n",
        "lvm_err":          "\nError in: {cmd}\n",
        # RAID
        "raid_status_title": "RAID Status",
        "raid_create_title": "Create RAID (mdadm)",
        "raid_devs_label":   "Devices (space-separated):",
        "raid_level_label":  "RAID Level:",
        "raid_name_label":   "MD Device Name:",
        "raid_create_btn":   "Create RAID",
        "raid_stop_btn":     "Stop RAID",
        "raid_detail_btn":   "show",
        "raid_detail_label": "Details for:",
        "raid_min_devs":     "RAID-{level} requires at least {n} devices!",
        "raid_confirm":      "RAID-{level} on {md}\nDevices: {devs}\nProceed?",
        "raid_stop_confirm": "Stop RAID {md}?",
        # Settings
        "settings_title":       "Settings",
        "settings_language":    "Language:",
        "settings_theme":       "Theme:",
        "settings_log_level":   "Log Level:",
        "settings_general":     "General",
        "settings_lang_changed":"Language changed – restart required",
        # About
        "about_title":      "About Speicher Maat",
        "about_version":    "Version",
        "about_author":     "Author",
        "about_email":      "E-Mail",
        "about_disclaimer": "Disclaimer",
        "about_third_party":"Third Party",
        # Help
        "help_title":       "Help",
        # Messages
        "msg_confirm":      "Confirmation Required",
        "msg_error":        "Error",
        "msg_success":      "Success",
        "msg_warning":      "Warning",
        "msg_info":         "Information",
        "msg_running":      "Operation already in progress",
        "msg_completed":    "Completed",
        "msg_failed":       "Operation failed",
        "msg_root_warn":    "Root privileges recommended!",
        "msg_refreshed":    "Refreshed",
        "msg_quit":         "Really quit?",
        "msg_disk_select":  "Please select a disk",
        # Help content
        "help_content": """\
Speicher Maat – Help

This tool extends GParted and GNOME Disks with advanced features:

CLONE & BACKUP
  Clones disks 1:1 using ddrescue (recommended) or dd.
  ddrescue is fault-tolerant, ideal for failing drives.

DATA MIGRATION
  Transfers directories using rsync.
  • Mirror mode (--delete): Target becomes identical to source.
  • Dry run: Shows what would happen without copying.

DATA RECOVERY
  • TestDisk: Repair deleted partitions and boot sectors.
  • PhotoRec: Recover files from free disk space.
  → Both launch in a dedicated terminal window.

SECURE WIPE
  • shred: Overwrites data multiple times (GNU coreutils).
  • nwipe: Interactive tool with NIST-compliant methods.

LVM – LOGICAL VOLUME MANAGEMENT
  Create and extend LVM volumes.

RAID
  Create and manage software RAID with mdadm.

SHORTCUTS
  F1          Open Help
  Ctrl+Q      Quit
  Ctrl+R      Refresh

For detailed guides see README.md
""",
    }
}


class I18n:
    def __init__(self):
        self.current_lang = "de"

    def set_language(self, lang):
        if lang in TRANSLATIONS:
            self.current_lang = lang

    def get(self, key):
        return TRANSLATIONS[self.current_lang].get(key, key)

    def _(self, key):
        return self.get(key)


i18n = I18n()
