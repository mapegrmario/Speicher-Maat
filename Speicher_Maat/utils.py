#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hilfsfunktionen für Speicher Maat"""
import os
import json
import subprocess
import shutil
from config import LC_ENV

def fmt_size(b):
    if not b:
        return "—"
    for u in ("B", "KiB", "MiB", "GiB", "TiB"):
        if b < 1024:
            return f"{b:.1f} {u}"
        b /= 1024
    return f"{b:.1f} PiB"

def list_disks():
    try:
        r = subprocess.run(
            ["lsblk", "-J", "-o", "NAME,SIZE,TYPE", "--bytes"],
            capture_output=True, text=True, env=LC_ENV)
        data = json.loads(r.stdout)
        result = []
        for dev in data.get("blockdevices", []):
            if dev.get("type") == "disk":
                size = int(dev.get("size", "0"))
                result.append((f"/dev/{dev['name']}", fmt_size(size)))
        return result
    except Exception:
        return []

def find_terminal():
    for t in ("xterm", "gnome-terminal", "xfce4-terminal",
              "konsole", "mate-terminal", "lxterminal"):
        if shutil.which(t):
            return t
    return None

def run_in_terminal(cmd_str, title=""):
    term = find_terminal()
    if not term:
        return False
    if term == "xterm":
        full = ["xterm", "-T", title or "Speicher Maat",
                "-geometry", "120x40", "-e",
                f"bash -c '{cmd_str}; echo; echo Fertig - Enter druecken; read'"]
    elif term == "gnome-terminal":
        full = ["gnome-terminal", "--title", title or "Speicher Maat",
                "--", "bash", "-c", f"{cmd_str}; echo; echo 'Fertig - Enter druecken'; read"]
    else:
        full = [term, "-e", f"bash -c '{cmd_str}; echo; read'"]
    subprocess.Popen(full)
    return True

def check_root():
    return os.geteuid() == 0
