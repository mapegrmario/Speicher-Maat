#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Theme und Styling für Speicher Maat – Soft Green Theme"""
import tkinter.font as tkfont


class Theme:
    PRIMARY       = "#2D5A4A"
    PRIMARY_LIGHT = "#4A7C6F"
    PRIMARY_DARK  = "#1A3C32"
    SECONDARY     = "#5B8C7A"
    ACCENT        = "#7FB069"
    BG_MAIN       = "#F5F7F6"
    BG_CARD       = "#FFFFFF"
    BG_INPUT      = "#FAFBFA"
    TEXT_MAIN     = "#2C3E38"
    TEXT_MUTED    = "#7A8B85"
    TEXT_LIGHT    = "#FFFFFF"
    SUCCESS       = "#4CAF50"
    WARNING       = "#FF9800"
    ERROR         = "#F44336"
    INFO          = "#2196F3"
    BORDER        = "#D1D9D6"
    BORDER_FOCUS  = "#4A7C6F"

    # Q-6 FIX: Tkinter akzeptiert nur eine Schriftfamilie – Fallback-Logik
    @staticmethod
    def get_font_family():
        """Beste verfügbare Schriftart ermitteln."""
        try:
            available = tkfont.families()
            for name in ("Ubuntu", "DejaVu Sans", "Liberation Sans",
                         "Noto Sans", "Sans"):
                if name in available:
                    return name
        except Exception:
            pass
        return "sans-serif"


# Wird einmalig beim Import aufgelöst
FONT_FAMILY = Theme.get_font_family()
