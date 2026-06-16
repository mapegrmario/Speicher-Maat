#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Logging-System für Speicher Maat"""
import os
import datetime
from config import FEHLER_LOG, ANALYSE_LOG, LOGS_DIR

class AppLogger:
    def __init__(self):
        os.makedirs(LOGS_DIR, exist_ok=True)
        self.fehler_file = FEHLER_LOG
        self.analyse_file = ANALYSE_LOG
        self._write_analyse("=" * 60)
        self._write_analyse(f"Speicher Maat gestartet: {datetime.datetime.now()}")
        self._write_analyse("=" * 60)

    def _write_analyse(self, message):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.analyse_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass

    def _write_fehler(self, message):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.fehler_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass

    def info(self, message):
        self._write_analyse(f"INFO: {message}")

    def error(self, message, exception=None):
        error_msg = f"ERROR: {message}"
        if exception:
            error_msg += f" | Exception: {exception}"
        self._write_fehler(error_msg)
        self._write_analyse(error_msg)

    def warning(self, message):
        self._write_analyse(f"WARNING: {message}")

    def action(self, action_type, details):
        self._write_analyse(f"ACTION: {action_type} | {details}")

logger = AppLogger()
