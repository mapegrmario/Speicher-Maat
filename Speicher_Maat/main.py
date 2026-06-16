#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Speicher Maat – Hauptprogramm
Ergänzungs-Tool zu GParted & GNOME Disks
"""
import os
import subprocess
import threading
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from config import VERSION, APP_NAME, AVATAR_PATH, HAFTUNGSAUSSCHLUSS, DRITTANBIETER
from theme import Theme
from i18n import i18n
from logger import logger
from utils import run_in_terminal, check_root
from widgets import ModernButton, Toast, LogWidget, DiskSelector


class BaseTab(ttk.Frame):
    """Basisklasse für alle Tabs mit asynchroner Befehlsausführung."""
    def __init__(self, notebook, tab_id):
        super().__init__(notebook)
        self.notebook   = notebook
        self.tab_id     = tab_id
        self._running   = False
        self._proc      = None  # BUG-2 FIX: korrekte Initialisierung

    def _run_async(self, cmd, log_widget, on_done=None, env=None):
        """Führt einen Befehl asynchron im Hintergrund-Thread aus."""
        if self._running:
            Toast(self, i18n._("msg_running"), "warning")
            return
        self._running = True
        log_widget.clear()
        lc_env = {**os.environ, "LC_ALL": "C", "LANG": "C"}
        log_widget.write(f"$ {' '.join(cmd)}\n")

        def worker():
            try:
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True, bufsize=1,
                    env=env or lc_env)
                self._proc = proc  # BUG-2 FIX: proc in self._proc speichern
                for line in proc.stdout:
                    self.after(0, lambda l=line: log_widget.write(l))
                proc.wait()
                rc = proc.returncode
                if rc == 0:
                    msg = "\n" + i18n._("msg_completed") + "\n"
                    self.after(0, lambda: Toast(self, i18n._("msg_completed"), "success"))
                else:
                    msg = f"\nFehler (Code {rc})\n"
                    self.after(0, lambda: Toast(self, i18n._("msg_failed"), "error"))
                self.after(0, lambda: log_widget.write(msg))
                if on_done:
                    self.after(0, on_done)
            except FileNotFoundError as e:
                self.after(0, lambda: log_widget.write(f"\nBefehl nicht gefunden: {e}\n"))
            except Exception as e:
                self.after(0, lambda: log_widget.write(f"\nFehler: {e}\n"))
                logger.error(f"Command failed: {cmd}", e)
            finally:
                self._proc = None
                self.after(0, lambda: setattr(self, "_running", False))

        threading.Thread(target=worker, daemon=True).start()

    def stop_process(self):
        """Laufenden Prozess beenden."""
        if self._proc:
            self._proc.terminate()
            self._proc = None
            self._running = False


# ---------------------------------------------------------------------------
# Klonen-Tab
# ---------------------------------------------------------------------------
class CloneTab(BaseTab):
    def __init__(self, nb):
        super().__init__(nb, "clone")
        nb.add(self, text=i18n._("tab_clone"))
        self._build()

    def _build(self):
        f1 = ttk.LabelFrame(self, text=i18n._("clone_title"), padding=10)
        f1.pack(fill="x", padx=10, pady=10)

        tk.Label(f1, text=i18n._("label_source")).grid(row=0, column=0, sticky="w", pady=5)
        self.src = DiskSelector(f1, label="")
        self.src.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(f1, text=i18n._("label_target")).grid(row=1, column=0, sticky="w", pady=5)
        self.dst = DiskSelector(f1, label="")
        self.dst.grid(row=1, column=1, sticky="w", pady=5)

        self.rescue_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(f1, text=i18n._("clone_ddrescue"),
                       variable=self.rescue_var).grid(row=2, column=1, sticky="w")

        ModernButton(f1, text=i18n._("clone_start"),
                    command=self._clone).grid(row=3, column=1, pady=10, sticky="w")

        tk.Label(self, text=i18n._("label_output")).pack(anchor="w", padx=10)
        self.log = LogWidget(self, height=10)
        self.log.pack(fill="both", expand=True, padx=10, pady=10)

    def _clone(self):
        src = self.src.get()
        dst = self.dst.get()
        if not src or not dst:
            Toast(self, i18n._("clone_select"), "warning")
            return
        if src == dst:
            Toast(self, i18n._("clone_same"), "error")
            return
        msg = i18n._("clone_confirm").format(src=src, dst=dst)
        if not messagebox.askyesno(i18n._("msg_confirm"), msg):
            return
        if self.rescue_var.get() and shutil.which("ddrescue"):
            cmd = ["ddrescue", "-d", "-r3", src, dst, "/tmp/ddrescue.log"]
        else:
            cmd = ["dd", f"if={src}", f"of={dst}", "bs=4M",
                   "conv=fsync", "status=progress"]
        self._run_async(cmd, self.log)


# ---------------------------------------------------------------------------
# Migrations-Tab
# ---------------------------------------------------------------------------
class MigrateTab(BaseTab):
    def __init__(self, nb):
        super().__init__(nb, "migrate")
        nb.add(self, text=i18n._("tab_migrate"))
        self._build()

    def _build(self):
        f = ttk.LabelFrame(self, text=i18n._("migrate_title"), padding=10)
        f.pack(fill="x", padx=10, pady=10)

        def browse(entry):
            d = filedialog.askdirectory(title=i18n._("label_source"))
            if d:
                entry.delete(0, tk.END)
                entry.insert(0, d)

        tk.Label(f, text=i18n._("label_source")).grid(row=0, column=0, sticky="w", pady=4)
        pf1 = tk.Frame(f)
        pf1.grid(row=0, column=1, sticky="w", pady=4)
        self.src = ttk.Entry(pf1, width=42)
        self.src.pack(side="left")
        ModernButton(pf1, text="...", command=lambda: browse(self.src),
                    padx=10, pady=3).pack(side="left", padx=4)

        tk.Label(f, text=i18n._("label_target")).grid(row=1, column=0, sticky="w", pady=4)
        pf2 = tk.Frame(f)
        pf2.grid(row=1, column=1, sticky="w", pady=4)
        self.dst = ttk.Entry(pf2, width=42)
        self.dst.pack(side="left")
        ModernButton(pf2, text="...", command=lambda: browse(self.dst),
                    padx=10, pady=3).pack(side="left", padx=4)

        opts = tk.Frame(f)
        opts.grid(row=2, column=1, sticky="w", pady=6)
        self.delete    = tk.BooleanVar()
        self.dryrun    = tk.BooleanVar()
        self.hardlinks = tk.BooleanVar(value=True)
        ttk.Checkbutton(opts, text=i18n._("migrate_mirror"),
                       variable=self.delete).pack(side="left", padx=(0, 12))
        ttk.Checkbutton(opts, text=i18n._("migrate_dryrun"),
                       variable=self.dryrun).pack(side="left", padx=(0, 12))
        ttk.Checkbutton(opts, text=i18n._("migrate_hardlinks"),
                       variable=self.hardlinks).pack(side="left")

        ModernButton(f, text=i18n._("btn_start"),
                    command=self._migrate, padx=15, pady=8).grid(
                    row=3, column=1, sticky="w", pady=8)

        tk.Label(self, text=i18n._("label_output")).pack(anchor="w", padx=10)
        self.log = LogWidget(self, height=12)
        self.log.pack(fill="both", expand=True, padx=10, pady=10)

    def _migrate(self):
        src = self.src.get().strip()
        dst = self.dst.get().strip()
        if not src or not dst:
            Toast(self, i18n._("migrate_select"), "warning")
            return
        if not os.path.isdir(src):
            Toast(self, i18n._("migrate_src_missing").format(path=src), "error")
            return
        if not os.path.isdir(dst):
            Toast(self, i18n._("migrate_dst_missing").format(path=dst), "error")
            return
        # BUG-9 FIX: -aAXv (ohne H), Hardlink per Checkbox steuern
        flags = ["-aAXv", "--progress"]
        if self.hardlinks.get():
            flags.append("-H")
        if self.delete.get():
            flags.append("--delete")
        if self.dryrun.get():
            flags.append("--dry-run")
        cmd = ["rsync"] + flags + [src.rstrip("/") + "/", dst]
        self._run_async(cmd, self.log)


# ---------------------------------------------------------------------------
# Datenrettungs-Tab
# ---------------------------------------------------------------------------
class RecoveryTab(BaseTab):
    def __init__(self, nb):
        super().__init__(nb, "recovery")
        nb.add(self, text=i18n._("tab_recovery"))
        self._build()

    def _build(self):
        tk.Label(self, text=i18n._("recovery_info"), justify="left",
                fg=Theme.WARNING, font=("Ubuntu", 9)).pack(anchor="w",
                padx=10, pady=(10, 0))

        f1 = ttk.LabelFrame(self, text=i18n._("recovery_td_title"), padding=10)
        f1.pack(fill="x", padx=10, pady=10)
        tk.Label(f1, text=i18n._("recovery_td_desc"),
                justify="left", fg=Theme.TEXT_MUTED).pack(anchor="w")
        pf = tk.Frame(f1)
        pf.pack(fill="x", pady=6)
        tk.Label(pf, text=i18n._("label_device_opt")).pack(side="left")
        self.td_disk = DiskSelector(pf, label="")
        self.td_disk.pack(side="left", padx=8)
        self.td_no_disk = tk.BooleanVar()
        ttk.Checkbutton(pf, text=i18n._("recovery_no_disk"),
                       variable=self.td_no_disk).pack(side="left")
        ModernButton(f1, text=i18n._("recovery_testdisk"),
                    command=self._testdisk, padx=15, pady=8).pack(anchor="w", pady=4)

        f2 = ttk.LabelFrame(self, text=i18n._("recovery_pr_title"), padding=10)
        f2.pack(fill="x", padx=10, pady=(0, 10))
        tk.Label(f2, text=i18n._("recovery_pr_desc"),
                justify="left", fg=Theme.TEXT_MUTED).pack(anchor="w")
        pf2 = tk.Frame(f2)
        pf2.pack(fill="x", pady=6)
        tk.Label(pf2, text=i18n._("label_device_opt")).pack(side="left")
        self.pr_disk = DiskSelector(pf2, label="")
        self.pr_disk.pack(side="left", padx=8)
        ModernButton(f2, text=i18n._("recovery_photorec"),
                    command=self._photorec, padx=15, pady=8).pack(anchor="w", pady=4)

        f3 = ttk.LabelFrame(self, text=i18n._("recovery_boot_title"), padding=10)
        f3.pack(fill="x", padx=10, pady=(0, 10))
        pf3 = tk.Frame(f3)
        pf3.pack(fill="x", pady=4)
        tk.Label(pf3, text=i18n._("label_disk")).pack(side="left")
        self.boot_disk = DiskSelector(pf3, label="")
        self.boot_disk.pack(side="left", padx=8)
        ModernButton(f3, text=i18n._("recovery_grub"),
                    command=self._grub, padx=15, pady=8).pack(anchor="w", pady=4)

        self.log = LogWidget(self, height=8)
        self.log.pack(fill="both", expand=True, padx=10, pady=10)

    def _testdisk(self):
        if not shutil.which("testdisk"):
            Toast(self, i18n._("recovery_td_missing"), "error")
            return
        disk = "" if self.td_no_disk.get() else self.td_disk.get()
        cmd = f"testdisk {disk}" if disk else "testdisk"
        run_in_terminal(cmd, "TestDisk")
        self.log.write("TestDisk wurde gestartet.\n")

    def _photorec(self):
        if not shutil.which("photorec"):
            Toast(self, i18n._("recovery_pr_missing"), "error")
            return
        disk = self.pr_disk.get()
        cmd = f"photorec {disk}" if disk else "photorec"
        run_in_terminal(cmd, "PhotoRec")
        self.log.write("PhotoRec wurde gestartet.\n")

    def _grub(self):
        disk = self.boot_disk.get()
        if not disk:
            Toast(self, i18n._("msg_disk_select"), "warning")
            return
        msg = i18n._("recovery_grub_confirm").format(disk=disk)
        if not messagebox.askyesno(i18n._("recovery_grub_title"), msg):
            return
        self._run_async(["grub-install", disk], self.log)


# ---------------------------------------------------------------------------
# Wipe-Tab
# ---------------------------------------------------------------------------
class WipeTab(BaseTab):
    def __init__(self, nb):
        super().__init__(nb, "wipe")
        nb.add(self, text=i18n._("tab_wipe"))
        self._build()

    def _build(self):
        f = ttk.LabelFrame(self, text=i18n._("wipe_title"), padding=10)
        f.pack(fill="x", padx=10, pady=10)

        pf = tk.Frame(f)
        pf.grid(row=0, column=0, columnspan=2, sticky="w", pady=4)
        tk.Label(pf, text=i18n._("label_disk")).pack(side="left")
        self.disk = DiskSelector(pf, label="")
        self.disk.pack(side="left", padx=8)

        tk.Label(f, text=i18n._("label_method")).grid(row=1, column=0, sticky="w", pady=4)
        self.method = tk.StringVar(value="shred")
        mf = tk.Frame(f)
        mf.grid(row=1, column=1, sticky="w", pady=4)
        for val, lbl in [("shred", "shred (GNU coreutils)"),
                         ("nwipe", "nwipe (sicherer, interaktiv)")]:
            state = "normal" if shutil.which(val) else "disabled"
            ttk.Radiobutton(mf, text=lbl, variable=self.method,
                           value=val, state=state).pack(side="left", padx=(0, 12))

        self.shred_frame = ttk.LabelFrame(f, text="shred-Optionen", padding=6)
        self.shred_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=6)
        of = tk.Frame(self.shred_frame)
        of.pack(fill="x")
        tk.Label(of, text=i18n._("label_passes")).pack(side="left")
        self.passes = ttk.Spinbox(of, from_=1, to=35, width=5)
        self.passes.set(3)
        self.passes.pack(side="left", padx=8)
        self.zero = tk.BooleanVar(value=True)
        ttk.Checkbutton(of, text=i18n._("wipe_zero"),
                       variable=self.zero).pack(side="left", padx=8)
        self.verbose = tk.BooleanVar(value=True)
        ttk.Checkbutton(of, text=i18n._("wipe_verbose"),
                       variable=self.verbose).pack(side="left")

        self.method.trace_add("write", self._toggle_opts)

        tk.Label(f, text=i18n._("wipe_warning"),
                fg=Theme.ERROR, font=("Ubuntu", 9, "bold")).grid(
                row=3, column=0, columnspan=2, pady=8)

        # Q-3 FIX: "LÖSCHEN STARTEN" + i18n-Key
        ModernButton(f, text=i18n._("wipe_start"),
                    command=self._wipe, padx=15, pady=8).grid(
                    row=4, column=0, columnspan=2, pady=4)

        self.log = LogWidget(self, height=12)
        self.log.pack(fill="both", expand=True, padx=10, pady=10)

    def _toggle_opts(self, *_):
        state = "normal" if self.method.get() == "shred" else "disabled"
        for child in self.shred_frame.winfo_children():
            try:
                child.config(state=state)
            except Exception:
                pass

    def _wipe(self):
        disk = self.disk.get()
        if not disk:
            Toast(self, i18n._("wipe_select"), "warning")
            return
        # Q-10 FIX: Ein einziger, klar formulierter Bestätigungs-Dialog
        msg = i18n._("wipe_msg1").format(disk=disk)
        if not messagebox.askyesno(i18n._("wipe_confirm1"), msg, icon="warning"):
            return
        if self.method.get() == "shred":
            cmd = ["shred", "-v", "-n", str(self.passes.get())]
            if self.zero.get():
                cmd.append("-z")
            cmd.append(disk)
            self._run_async(cmd, self.log)
        else:
            run_in_terminal(f"nwipe {disk}", "nwipe - Sicheres Löschen")
            self.log.write("nwipe wurde gestartet.\n")


# ---------------------------------------------------------------------------
# LVM-Tab
# ---------------------------------------------------------------------------
class LVMTab(BaseTab):
    def __init__(self, nb):
        super().__init__(nb, "lvm")
        nb.add(self, text=i18n._("tab_lvm"))
        self._build()

    def _build(self):
        sf = ttk.LabelFrame(self, text="LVM-Status", padding=6)
        sf.pack(fill="x", padx=10, pady=10)
        ModernButton(sf, text=i18n._("lvm_status_btn"),
                    command=self._status, padx=15, pady=8).pack(anchor="w")

        cf = ttk.LabelFrame(self, text=i18n._("lvm_create_title"), padding=10)
        cf.pack(fill="x", padx=10, pady=(0, 5))

        fields = [
            (i18n._("lvm_pv_label"), "pv"),
            (i18n._("lvm_vg_label"), "vg"),
            (i18n._("lvm_lv_label"), "lv"),
            (i18n._("lvm_size_label"), "lv_size"),
        ]
        self._lvm_vars = {}
        for i, (lbl, key) in enumerate(fields):
            tk.Label(cf, text=lbl).grid(row=i, column=0, sticky="w", pady=3, padx=(0, 8))
            e = ttk.Entry(cf, width=32)
            e.grid(row=i, column=1, sticky="w", pady=3)
            self._lvm_vars[key] = e

        tk.Label(cf, text=i18n._("lvm_fs_label")).grid(row=4, column=0, sticky="w", pady=3)
        self.lvm_fs = ttk.Combobox(cf,
                                  values=["(keins)", "ext4", "xfs", "btrfs", "fat32"],
                                  state="readonly", width=16)
        self.lvm_fs.set("ext4")
        self.lvm_fs.grid(row=4, column=1, sticky="w", pady=3)

        ModernButton(cf, text=i18n._("lvm_create_btn"),
                    command=self._create, padx=15, pady=8).grid(
                    row=5, column=1, sticky="w", pady=8)

        ef = ttk.LabelFrame(self, text=i18n._("lvm_extend_title"), padding=10)
        ef.pack(fill="x", padx=10, pady=(0, 5))
        pf = tk.Frame(ef)
        pf.pack(fill="x")
        tk.Label(pf, text=i18n._("lvm_lv_path")).pack(side="left")
        self.lv_path = ttk.Entry(pf, width=28)
        self.lv_path.pack(side="left", padx=8)
        tk.Label(pf, text=i18n._("lvm_ext_size")).pack(side="left")
        self.lv_ext = ttk.Entry(pf, width=10)
        self.lv_ext.insert(0, "+5G")
        self.lv_ext.pack(side="left", padx=8)
        self.resize_fs = tk.BooleanVar(value=True)
        ttk.Checkbutton(pf, text=i18n._("lvm_resize_fs"),
                       variable=self.resize_fs).pack(side="left")
        ModernButton(ef, text=i18n._("lvm_extend_btn"),
                    command=self._extend, padx=15, pady=8).pack(anchor="w", pady=6)

        self.log = LogWidget(self, height=10)
        self.log.pack(fill="both", expand=True, padx=10, pady=10)

    def _status(self):
        """BUG-3 FIX: Sequentiell pvs → vgs → lvs mit Trennzeile."""
        if self._running:
            Toast(self, i18n._("msg_running"), "warning")
            return
        self.log.clear()
        lc_env = {**os.environ, "LC_ALL": "C", "LANG": "C"}
        cmds = [
            (["pvs", "--units", "g"],),
            (["vgs", "--units", "g"],),
            (["lvs", "--units", "g"],),
        ]

        def run_all():
            for (cmd,) in cmds:
                try:
                    r = subprocess.run(cmd, capture_output=True, text=True, env=lc_env)
                    output = (r.stdout or "") + (r.stderr or "")
                    self.after(0, lambda out=output: self.log.write(out + "\n"))
                except Exception as e:
                    self.after(0, lambda ex=e: self.log.write(f"Fehler: {ex}\n"))
            self.after(0, lambda: setattr(self, "_running", False))

        self._running = True
        threading.Thread(target=run_all, daemon=True).start()

    def _create(self):
        v = {k: e.get().strip() for k, e in self._lvm_vars.items()}
        if not all(v.values()):
            Toast(self, i18n._("lvm_fill_all"), "warning")
            return
        cmds = [
            ["pvcreate", v["pv"]],
            ["vgcreate", v["vg"], v["pv"]],
            ["lvcreate", "-L", v["lv_size"], "-n", v["lv"], v["vg"]],
        ]
        fs = self.lvm_fs.get()
        lv_dev = f"/dev/{v['vg']}/{v['lv']}"
        if fs and fs != "(keins)":
            mkfs_map = {
                "ext4":  ["mkfs.ext4", "-F", lv_dev],
                "xfs":   ["mkfs.xfs",  "-f", lv_dev],
                "btrfs": ["mkfs.btrfs", "-f", lv_dev],
                "fat32": ["mkfs.vfat", "-F32", lv_dev],
            }
            if fs in mkfs_map:
                cmds.append(mkfs_map[fs])

        if self._running:
            Toast(self, i18n._("msg_running"), "warning")
            return
        self.log.clear()
        lc_env = {**os.environ, "LC_ALL": "C", "LANG": "C"}

        # BUG-4 FIX: Sequentiell in eigenem Thread, nicht im Main-Thread
        def run_seq():
            self._running = True
            for cmd in cmds:
                self.after(0, lambda c=cmd: self.log.write(f"$ {' '.join(c)}\n"))
                try:
                    r = subprocess.run(cmd, capture_output=True, text=True, env=lc_env)
                    out = (r.stdout or "") + (r.stderr or "")
                    self.after(0, lambda o=out: self.log.write(o))
                    if r.returncode != 0:
                        err = i18n._("lvm_err").format(cmd=" ".join(cmd))
                        self.after(0, lambda e=err: self.log.write(e))
                        break
                except Exception as e:
                    self.after(0, lambda ex=e: self.log.write(f"\n{ex}\n"))
                    break
            else:
                done = i18n._("lvm_done")
                self.after(0, lambda: self.log.write(done))
                self.after(0, lambda: Toast(self, i18n._("msg_completed"), "success"))
            self.after(0, lambda: setattr(self, "_running", False))

        threading.Thread(target=run_seq, daemon=True).start()

    def _extend(self):
        lv  = self.lv_path.get().strip()
        ext = self.lv_ext.get().strip()
        if not lv or not ext:
            Toast(self, i18n._("lvm_fill_path"), "warning")
            return
        cmd = ["lvextend", "-L", ext, lv]
        on_done = self._resize_fs_after if self.resize_fs.get() else None
        self._run_async(cmd, self.log, on_done=on_done)

    def _resize_fs_after(self):
        """BUG-10 FIX: FS-Typ prüfen und passendes Resize-Tool wählen."""
        lv = self.lv_path.get().strip()
        try:
            r = subprocess.run(["blkid", "-o", "value", "-s", "TYPE", lv],
                              capture_output=True, text=True)
            fs_type = r.stdout.strip().lower()
        except Exception:
            fs_type = "ext4"
        if fs_type in ("ext2", "ext3", "ext4"):
            self._run_async(["resize2fs", lv], self.log)
        elif fs_type == "xfs":
            self._run_async(["xfs_growfs", lv], self.log)
        elif fs_type == "btrfs":
            self._run_async(["btrfs", "filesystem", "resize", "max", lv], self.log)
        else:
            Toast(self, f"Kein Resize-Tool für FS-Typ: {fs_type}", "warning")


# ---------------------------------------------------------------------------
# RAID-Tab
# ---------------------------------------------------------------------------
class RAIDTab(BaseTab):
    def __init__(self, nb):
        super().__init__(nb, "raid")
        nb.add(self, text=i18n._("tab_raid"))
        self._build()

    def _build(self):
        sf = ttk.LabelFrame(self, text=i18n._("raid_status_title"), padding=6)
        sf.pack(fill="x", padx=10, pady=10)
        bf = tk.Frame(sf)
        bf.pack(anchor="w")
        ModernButton(bf, text="/proc/mdstat",
                    command=self._mdstat, padx=15, pady=8).pack(side="left", padx=(0, 8))
        tk.Label(bf, text=i18n._("raid_detail_label")).pack(side="left")
        self.detail_dev = ttk.Entry(bf, width=10)
        self.detail_dev.insert(0, "md0")
        self.detail_dev.pack(side="left", padx=4)
        ModernButton(bf, text=i18n._("raid_detail_btn"),
                    command=self._detail, padx=15, pady=8).pack(side="left", padx=4)

        cf = ttk.LabelFrame(self, text=i18n._("raid_create_title"), padding=10)
        cf.pack(fill="x", padx=10, pady=(0, 5))

        tk.Label(cf, text=i18n._("raid_devs_label")).grid(
            row=0, column=0, sticky="w", pady=3)
        self.devs = ttk.Entry(cf, width=42)
        self.devs.grid(row=0, column=1, sticky="w", pady=3)

        tk.Label(cf, text=i18n._("raid_level_label")).grid(
            row=1, column=0, sticky="w", pady=3)
        self.level = ttk.Combobox(cf, values=["0", "1", "5", "6", "10"],
                                 state="readonly", width=8)
        self.level.set("1")
        self.level.grid(row=1, column=1, sticky="w", pady=3)

        tk.Label(cf, text=i18n._("raid_name_label")).grid(
            row=2, column=0, sticky="w", pady=3)
        self.md_name = ttk.Entry(cf, width=12)
        self.md_name.insert(0, "md0")
        self.md_name.grid(row=2, column=1, sticky="w", pady=3)

        bf2 = tk.Frame(cf)
        bf2.grid(row=3, column=1, sticky="w", pady=8)
        ModernButton(bf2, text=i18n._("raid_create_btn"),
                    command=self._create, padx=15, pady=8).pack(side="left", padx=(0, 8))
        ModernButton(bf2, text=i18n._("raid_stop_btn"),
                    command=self._stop, padx=15, pady=8).pack(side="left")

        self.log = LogWidget(self, height=12)
        self.log.pack(fill="both", expand=True, padx=10, pady=10)

    def _mdstat(self):
        self._run_async(["cat", "/proc/mdstat"], self.log)

    def _detail(self):
        dev = f"/dev/{self.detail_dev.get().strip()}"
        self._run_async(["mdadm", "--detail", dev], self.log)

    def _create(self):
        devs  = self.devs.get().split()
        level = self.level.get()
        md    = f"/dev/{self.md_name.get().strip() or 'md0'}"
        min_d = {"0": 2, "1": 2, "5": 3, "6": 4, "10": 4}
        if len(devs) < min_d.get(level, 2):
            msg = i18n._("raid_min_devs").format(level=level, n=min_d.get(level, 2))
            Toast(self, msg, "warning")
            return
        msg = i18n._("raid_confirm").format(level=level, md=md, devs=" ".join(devs))
        if not messagebox.askyesno(i18n._("raid_create_title"), msg):
            return
        cmd = ["mdadm", "--create", md, "--level", level,
               "--raid-devices", str(len(devs))] + devs
        self._run_async(cmd, self.log)

    def _stop(self):
        md = f"/dev/{self.detail_dev.get().strip()}"
        msg = i18n._("raid_stop_confirm").format(md=md)
        if not messagebox.askyesno(i18n._("raid_stop_btn"), msg):
            return
        self._run_async(["mdadm", "--stop", md], self.log)


# ---------------------------------------------------------------------------
# Einstellungen-Tab (Q-1 FIX: als Tab statt Toplevel)
# ---------------------------------------------------------------------------
class SettingsTab(ttk.Frame):
    def __init__(self, nb):
        super().__init__(nb)
        nb.add(self, text=i18n._("tab_settings"))
        self._build()

    def _build(self):
        f = ttk.LabelFrame(self, text=i18n._("settings_general"), padding=15)
        f.pack(fill="x", padx=30, pady=20)

        # Sprache
        tk.Label(f, text=i18n._("settings_language")).grid(
            row=0, column=0, sticky="w", pady=8)
        self.lang_var = tk.StringVar(value="Deutsch")
        lang_combo = ttk.Combobox(f, textvariable=self.lang_var,
                                 values=["Deutsch", "English"],
                                 state="readonly", width=20)
        lang_combo.grid(row=0, column=1, sticky="w", pady=8)
        lang_combo.bind("<<ComboboxSelected>>", self._change_lang)

        # BUG-11 FIX: Theme-Combobox korrekt mit textvariable verknüpft
        tk.Label(f, text=i18n._("settings_theme")).grid(
            row=1, column=0, sticky="w", pady=8)
        self.theme_var = tk.StringVar(value="Soft Green (Hell)")
        ttk.Combobox(f, textvariable=self.theme_var,
                    values=["Soft Green (Hell)"],
                    state="readonly", width=20).grid(
                    row=1, column=1, sticky="w", pady=8)
        tk.Label(f, text="(Dark Mode in Entwicklung)",
                fg=Theme.TEXT_MUTED, font=("Ubuntu", 8)).grid(
                row=1, column=2, sticky="w", padx=8)

        # Log-Level
        tk.Label(f, text=i18n._("settings_log_level")).grid(
            row=2, column=0, sticky="w", pady=8)
        self.log_level_var = tk.StringVar(value="INFO")
        ttk.Combobox(f, textvariable=self.log_level_var,
                    values=["INFO", "WARNING", "ERROR"],
                    state="readonly", width=20).grid(
                    row=2, column=1, sticky="w", pady=8)

    def _change_lang(self, event):
        lang_map = {"Deutsch": "de", "English": "en"}
        i18n.set_language(lang_map.get(self.lang_var.get(), "de"))
        Toast(self, i18n._("settings_lang_changed"), "info")


# ---------------------------------------------------------------------------
# Hilfe-Tab (Q-1 FIX: als Tab statt Toplevel)
# ---------------------------------------------------------------------------
class HelpTab(ttk.Frame):
    def __init__(self, nb):
        super().__init__(nb)
        nb.add(self, text=i18n._("tab_help"))
        self._build()

    def _build(self):
        text = tk.Text(self, wrap="word", font=("Ubuntu", 10),
                      bg=Theme.BG_INPUT, padx=20, pady=20)
        text.pack(fill="both", expand=True, padx=10, pady=10)
        vsb = ttk.Scrollbar(self, command=text.yview)
        vsb.place(relx=1, rely=0, relheight=1, anchor="ne")
        text.configure(yscrollcommand=vsb.set)
        text.insert("1.0", i18n._("help_content"))
        text.configure(state="disabled")
        text.bind("<Button-4>", lambda e: text.yview_scroll(-1, "units"))
        text.bind("<Button-5>", lambda e: text.yview_scroll(1, "units"))


# ---------------------------------------------------------------------------
# Über-Tab (Q-1 FIX: als Tab statt Toplevel)
# ---------------------------------------------------------------------------
class AboutTab(ttk.Frame):
    def __init__(self, nb):
        super().__init__(nb)
        nb.add(self, text=i18n._("tab_about"))
        self._build()

    def _build(self):
        # Avatar
        avatar_frame = tk.Frame(self, bg=Theme.BG_MAIN, height=120)
        avatar_frame.pack(fill="x")
        avatar_frame.pack_propagate(False)
        try:
            if os.path.exists(AVATAR_PATH):
                from PIL import Image, ImageTk
                img   = Image.open(AVATAR_PATH).resize((90, 90))
                photo = ImageTk.PhotoImage(img)
                lbl   = tk.Label(avatar_frame, image=photo, bg=Theme.BG_MAIN)
                lbl.image = photo
                lbl.pack(pady=15)
            else:
                # Q-7 FIX: Emoji-Fallback auch ohne PIL sichtbar
                tk.Label(avatar_frame, text="🚢", font=("Ubuntu", 40),
                        bg=Theme.BG_MAIN).pack(pady=15)
        except ImportError:
            # Q-7 FIX: text="" war unsichtbar!
            tk.Label(avatar_frame, text="🚢", font=("Ubuntu", 40),
                    bg=Theme.BG_MAIN).pack(pady=15)

        canvas = tk.Canvas(self, bg=Theme.BG_MAIN, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        vsb = ttk.Scrollbar(self, command=canvas.yview)
        vsb.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=vsb.set)
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        inner = tk.Frame(canvas, bg=Theme.BG_MAIN)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        tk.Label(inner, text=APP_NAME, font=("Ubuntu", 20, "bold"),
                bg=Theme.BG_MAIN, fg=Theme.PRIMARY).pack(pady=(10, 0))
        tk.Label(inner, text=f"{i18n._('about_version')} {VERSION}",
                bg=Theme.BG_MAIN, fg=Theme.TEXT_MUTED).pack()
        tk.Label(inner, text="", bg=Theme.BG_MAIN).pack()

        info = (
            (i18n._("about_author"), "Mario Peeß / Großenhain"),
            (i18n._("about_email"),  "mapegr@mailbox.org"),
        )
        for label, value in info:
            row = tk.Frame(inner, bg=Theme.BG_MAIN)
            row.pack(fill="x", padx=30, pady=2)
            tk.Label(row, text=f"{label}:", bg=Theme.BG_MAIN,
                    fg=Theme.TEXT_MUTED, width=10, anchor="w").pack(side="left")
            tk.Label(row, text=value, bg=Theme.BG_MAIN,
                    fg=Theme.TEXT_MAIN).pack(side="left")

        tk.Label(inner, text="", bg=Theme.BG_MAIN).pack()

        # Haftungsausschluss
        tk.Label(inner, text=i18n._("about_disclaimer"),
                bg=Theme.BG_MAIN, fg=Theme.TEXT_MAIN,
                font=("Ubuntu", 10, "bold")).pack(anchor="w", padx=30)
        tk.Label(inner, text=HAFTUNGSAUSSCHLUSS.strip(), justify="left",
                bg=Theme.BG_CARD, fg=Theme.TEXT_MUTED, font=("Ubuntu", 9),
                padx=15, pady=10, relief="solid", borderwidth=1,
                wraplength=520).pack(fill="x", padx=30, pady=8)

        # Drittanbieter
        tk.Label(inner, text=i18n._("about_third_party"),
                bg=Theme.BG_MAIN, fg=Theme.TEXT_MAIN,
                font=("Ubuntu", 10, "bold")).pack(anchor="w", padx=30)
        tk.Label(inner, text=DRITTANBIETER.strip(), justify="left",
                bg=Theme.BG_MAIN, fg=Theme.TEXT_MUTED,
                font=("Ubuntu", 8)).pack(anchor="w", padx=30, pady=5)


# ---------------------------------------------------------------------------
# Hauptfenster
# ---------------------------------------------------------------------------
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{VERSION}")
        self.geometry("1050x720")
        self.minsize(820, 600)
        self.configure(bg=Theme.BG_MAIN)
        self._setup_style()
        self._create_menu()
        self._create_ui()
        if not check_root():
            self.after(500, lambda: Toast(self, i18n._("msg_root_warn"), "warning", 5000))
        logger.info("Anwendung gestartet")

    def _setup_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TNotebook.Tab", padding=[15, 8], font=("Ubuntu", 10))
        style.configure("TLabelFrame", padding=10)
        style.configure("TLabelFrame.Label", font=("Ubuntu", 11, "bold"))
        style.configure("TEntry", padding=4)

    def _create_menu(self):
        menubar   = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_separator()
        file_menu.add_command(label=i18n._("menu_exit"), command=self._quit)
        menubar.add_cascade(label=i18n._("menu_file"), menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label=i18n._("menu_help"),
                             command=self._go_help, accelerator="F1")
        help_menu.add_command(label=i18n._("menu_about"),
                             command=self._go_about)
        menubar.add_cascade(label=i18n._("menu_help"), menu=help_menu)

        self.config(menu=menubar)
        self.bind("<F1>",        lambda e: self._go_help())
        self.bind("<Control-q>", lambda e: self._quit())
        self.bind("<Control-r>", lambda e: Toast(self, i18n._("msg_refreshed"), "info"))

    def _create_ui(self):
        header = tk.Frame(self, bg=Theme.PRIMARY, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=f"⚓  {APP_NAME}",
                font=("Ubuntu", 17, "bold"),
                bg=Theme.PRIMARY, fg=Theme.TEXT_LIGHT).pack(pady=17)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=8, pady=8)

        CloneTab(self.nb)
        MigrateTab(self.nb)
        RecoveryTab(self.nb)
        WipeTab(self.nb)
        LVMTab(self.nb)
        RAIDTab(self.nb)
        SettingsTab(self.nb)
        HelpTab(self.nb)
        AboutTab(self.nb)

        self.status_lbl = tk.Label(
            self,
            text=f"{APP_NAME} v{VERSION}  |  Für Partitionierung: GParted verwenden",
            bg=Theme.BG_MAIN, fg=Theme.TEXT_MUTED,
            anchor="w", padx=10, pady=4)
        self.status_lbl.pack(fill="x")

    def _go_help(self):
        for idx in range(self.nb.index("end")):
            if self.nb.tab(idx, "text") == i18n._("tab_help"):
                self.nb.select(idx)
                break

    def _go_about(self):
        for idx in range(self.nb.index("end")):
            if self.nb.tab(idx, "text") == i18n._("tab_about"):
                self.nb.select(idx)
                break

    def _quit(self):
        if messagebox.askyesno(APP_NAME, i18n._("msg_quit")):
            logger.info("Anwendung beendet")
            self.destroy()


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
