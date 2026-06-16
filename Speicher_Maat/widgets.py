#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Custom Widgets für Speicher Maat"""
import tkinter as tk
from tkinter import ttk
from theme import Theme
from i18n import i18n


class ModernButton(tk.Button):
    """Modern gestylter Button mit Hover-Effekt."""

    def __init__(self, parent, text="", command=None, **kwargs):
        kwargs.pop("padx", None)
        kwargs.pop("pady", None)
        kwargs.pop("font", None)
        kwargs.pop("relief", None)
        kwargs.pop("borderwidth", None)
        kwargs.pop("bg", None)
        kwargs.pop("fg", None)
        kwargs.pop("activebackground", None)

        super().__init__(parent, text=text, command=command,
                        relief="flat", borderwidth=0,
                        padx=15, pady=8,
                        font=("Ubuntu", 10, "bold"),
                        bg=Theme.PRIMARY, fg=Theme.TEXT_LIGHT,
                        activebackground=Theme.PRIMARY_LIGHT,
                        **kwargs)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, e):
        self.config(bg=Theme.PRIMARY_LIGHT)

    def _on_leave(self, e):
        self.config(bg=Theme.PRIMARY)


class Toast(tk.Toplevel):
    """Toast-Benachrichtigung, positioniert relativ zum Elternfenster."""
    def __init__(self, parent, message, msg_type="info", duration=3000):
        super().__init__(parent)
        self.withdraw()
        self.overrideredirect(True)
        colors = {
            "info":    (Theme.INFO,    Theme.TEXT_LIGHT),
            "success": (Theme.SUCCESS, Theme.TEXT_LIGHT),
            "warning": (Theme.WARNING, Theme.TEXT_LIGHT),
            "error":   (Theme.ERROR,   Theme.TEXT_LIGHT),
        }
        bg, fg = colors.get(msg_type, colors["info"])
        frame = tk.Frame(self, bg=bg, padx=20, pady=10)
        frame.pack()
        tk.Label(frame, text=message, bg=bg, fg=fg,
                font=("Ubuntu", 10)).pack()
        self.update_idletasks()
        # BUG-9 FIX: Position relativ zum Elternfenster (Multi-Monitor)
        try:
            px = parent.winfo_rootx()
            py = parent.winfo_rooty()
            pw = parent.winfo_width()
            ph = parent.winfo_height()
            x = px + pw - self.winfo_width() - 20
            y = py + ph - self.winfo_height() - 20
        except Exception:
            x = self.winfo_screenwidth() - self.winfo_width() - 20
            y = self.winfo_screenheight() - self.winfo_height() - 20
        self.geometry(f"+{x}+{y}")
        self.deiconify()
        if duration > 0:
            self.after(duration, self._safe_destroy)

    def _safe_destroy(self):
        try:
            self.destroy()
        except Exception:
            pass


class LogWidget(tk.Frame):
    """Log-Ausgabe-Widget mit Scrollbar und Kopier-Funktion."""
    def __init__(self, parent, height=10):
        super().__init__(parent)
        btn_bar = tk.Frame(self)
        btn_bar.pack(fill="x")
        ModernButton(btn_bar, text=i18n._("log_clear"),
                    command=self.clear, padx=10, pady=3).pack(side="right", padx=2)
        ModernButton(btn_bar, text=i18n._("log_copy"),
                    command=self._copy, padx=10, pady=3).pack(side="right", padx=2)

        # BUG-5 FIX: Scrollbar ZUERST packen, dann Text
        vsb = ttk.Scrollbar(self)
        vsb.pack(side="right", fill="y")

        self.text = tk.Text(self, height=height, wrap="word",
                           state="disabled", font=("Monospace", 9),
                           bg=Theme.BG_INPUT, yscrollcommand=vsb.set)
        self.text.pack(fill="both", expand=True, padx=0, pady=5)
        vsb.config(command=self.text.yview)

        # BUG-6 FIX: Linux X11 braucht Button-4/Button-5
        self.text.bind("<MouseWheel>",
                      lambda e: self.text.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.text.bind("<Button-4>",
                      lambda e: self.text.yview_scroll(-1, "units"))
        self.text.bind("<Button-5>",
                      lambda e: self.text.yview_scroll(1, "units"))

    def write(self, txt):
        self.text.configure(state="normal")
        self.text.insert(tk.END, txt)
        self.text.see(tk.END)
        self.text.configure(state="disabled")

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.configure(state="disabled")

    def _copy(self):
        content = self.text.get("1.0", tk.END).strip()
        self.text.clipboard_clear()
        self.text.clipboard_append(content)
        Toast(self, i18n._("log_copied"), "info", 1500)


class DiskSelector(tk.Frame):
    """Combobox zur Laufwerkauswahl mit Größenanzeige."""
    def __init__(self, parent, label="Laufwerk:", on_refresh=None):
        super().__init__(parent)
        tk.Label(self, text=label).pack(side="left", padx=(0, 6))
        self.var = tk.StringVar()
        self.cb = ttk.Combobox(self, textvariable=self.var,
                              state="readonly", width=28)
        self.cb.pack(side="left")
        self.info = tk.Label(self, text="", fg="gray")
        self.info.pack(side="left", padx=8)
        ModernButton(self, text=i18n._("btn_refresh"),
                    command=self.refresh, padx=10, pady=3).pack(side="left", padx=4)
        self._on_refresh = on_refresh
        self._sizes = {}

        # BUG-8 FIX: Binding einmalig im __init__, nicht bei jedem refresh()
        self.cb.bind("<<ComboboxSelected>>",
                    lambda e: self.info.config(text=self._sizes.get(self.var.get(), "")))
        self.refresh()

    def refresh(self):
        from utils import list_disks
        disks = list_disks()
        vals = [d[0] for d in disks]
        self._sizes = {d[0]: d[1] for d in disks}
        self.cb["values"] = vals
        if vals and not self.var.get():
            self.var.set(vals[0])
        if self.var.get() in self._sizes:
            self.info.config(text=self._sizes[self.var.get()])
        if self._on_refresh:
            self._on_refresh()

    def get(self):
        return self.var.get()
