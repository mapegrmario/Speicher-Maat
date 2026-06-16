# Speicher Maat v1.0 – Code-Analyse
**Datum:** 2026-06-15  
**Analysiert von:** Claude Sonnet 4.6  
**Dateien:** config.py, main.py, widgets.py, utils.py, logger.py, i18n.py, theme.py, install.sh

---

## KRITISCHE BUGS (führen zu Fehlfunktionen)

### BUG-1 · main.py L17-18: VERSION & LC_ENV doppelt definiert
```python
from config import VERSION, ...   # Import aus config.py (korrekt)
VERSION = "1.0.0"                 # ÜBERSCHREIBT den Import!
LC_ENV  = {**os.environ, ...}    # ÜBERSCHREIBT config.LC_ENV!
```
→ **Fix:** Beide Zeilen aus main.py löschen.

### BUG-2 · BaseTab._run_async: self._proc wird nie gesetzt
```python
proc = subprocess.Popen(...)    # lokale Variable
# self._proc = proc ← FEHLT!
```
→ `stop_process()` prüft `self._proc`, der immer `None` bleibt → Stop funktioniert nie.  
→ **Fix:** `self._proc = proc` nach dem Popen-Aufruf einfügen.

### BUG-3 · LVMTab._status: 3× _run_async in Schleife → nur 1 läuft
```python
for cmd in [[pvs...], [vgs...], [lvs...]]:
    self._run_async(cmd, self.log)  # ← 2. + 3. Aufruf findet _running=True
```
→ pvs läuft, vgs + lvs zeigen Toast "Operation läuft bereits".  
→ **Fix:** Sequentielle Ausführung via Thread oder on_done-Kaskade.

### BUG-4 · LVMTab._create: subprocess.run() im Main-Thread (via after)
```python
def run_seq(idx=0):
    r = subprocess.run(cmd, ...)   # blockiert GUI-Thread!
self.after(0, run_seq)
```
→ Jeder LVM-Befehl friert die GUI ein.  
→ **Fix:** run_seq in eigenem Thread ausführen (threading.Thread).

### BUG-5 · LogWidget: Scrollbar nach Text gepackt → falsch positioniert
```python
self.text.pack(fill="both", expand=True, ...)   # belegt gesamte Breite
vsb = ttk.Scrollbar(...)
vsb.pack(side="right", fill="y")                # kein Platz mehr!
```
→ Scrollbar erscheint unter dem Text, nicht rechts davon.  
→ **Fix:** Scrollbar VOR dem Text-Widget packen.

### BUG-6 · LogWidget: MouseWheel-Binding funktioniert auf Linux X11 nicht
```python
self.text.bind("<MouseWheel>", ...)  # ← Windows/macOS only!
```
→ Linux X11 sendet `<Button-4>` (hoch) und `<Button-5>` (runter).  
→ **Fix:** Alle 3 Bindings (MouseWheel + Button-4 + Button-5) setzen.

### BUG-7 · install.sh: cd ins Ziel vor find → kopiert aus leerem Verzeichnis
```bash
mkdir -p "$APP_DIR" && cd "$APP_DIR"
find . -maxdepth 1 -name "*.py" -exec cp {} "$APP_DIR/" \;  # find im ZIEL!
```
→ Das Skript kopiert aus dem bereits leeren Zielverzeichnis nach sich selbst.  
→ **Fix:** SCRIPT_DIR=$(dirname "$(realpath "$0")") verwenden.

---

## MITTLERE BUGS (schlechtes Verhalten)

### BUG-8 · DiskSelector.refresh(): Binding akkumuliert bei jedem Refresh
```python
def refresh(self):
    self.cb.bind("<<ComboboxSelected>>", lambda ...)  # IMMER neues Binding!
```
→ Nach n Refreshs laufen n Callbacks auf jede Auswahl.  
→ **Fix:** Binding im __init__ setzen, nicht in refresh().

### BUG-9 · MigrateTab._migrate: Flag -H doppelt gesetzt
```python
flags = ["-aHAXv", ...]     # -H schon drin!
if self.hardlinks.get():
    flags.append("-H")       # ← doppelt
```
→ rsync bekommt zweimal -H, harmlos aber ein Zeichen für Logikfehler.  
→ **Fix:** -H aus -aHAXv entfernen; nur per Checkbox steuern.

### BUG-10 · LVMTab._resize_fs_after: resize2fs nur für ext4
```python
self._run_async(["resize2fs", lv], self.log)  # scheitert bei xfs, btrfs!
```
→ Für xfs: `xfs_growfs`, für btrfs: `btrfs filesystem resize max`.  
→ **Fix:** FS-Typ ermitteln und passendes Tool wählen.

### BUG-11 · SettingsDialog: Theme + Log-Level ohne Funktion
```python
ttk.Combobox(f, values=["Soft Green (Hell)", "Dark Mode"], ...)
# kein textvariable, kein command → wirkungslos
```
→ Benutzer ändert Einstellung, nichts passiert.  
→ **Fix:** textvariable + Callback implementieren oder aus der UI entfernen.

---

## QUALITÄTSMÄNGEL / VERBESSERUNGSVORSCHLÄGE

### Q-1 · Regel 7 Verletzung: 3 externe Toplevel-Fenster
`AboutDialog`, `HelpDialog`, `SettingsDialog` sind alle `tk.Toplevel`.  
→ Besser als Tabs im Hauptnotebook integrieren.

### Q-2 · ~40 hardcoded deutsche Strings außerhalb i18n
Beispiele: "Ausgabe:", "Bitte Quelle und Ziel wählen", "LOESCHEN STARTEN",
"TestDisk - Partitionen wiederherstellen", alle RecoveryTab-Texte, ...  
→ Alle Strings in i18n.py aufnehmen.

### Q-3 · Tippfehler: "LOESCHEN STARTEN" (L334)
Fehlende Umlaut-Kodierung.  
→ **Fix:** "LÖSCHEN STARTEN"

### Q-4 · 11 i18n-Keys definiert aber nie benutzt
about_author, about_email, about_version, app_title, btn_refresh,
btn_stop, label_disk, msg_error, msg_info, msg_success, msg_warning  
→ Entweder verwenden oder entfernen.

### Q-5 · Unbenutzte Imports in main.py
`import sys, re, json` → werden nirgends verwendet.  
→ Entfernen für saubereren Code.

### Q-6 · Theme.FONT_FAMILY als CSS-Syntax (ungültig für tkinter)
```python
FONT_FAMILY = "Segoe UI, Ubuntu, sans-serif"  # ← CSS, nicht tkinter!
```
→ tkinter akzeptiert nur eine Schriftfamilie.  
→ **Fix:** Fallback-Logik implementieren oder nur "Ubuntu" setzen.

### Q-7 · AboutDialog: PIL-Fehler zeigt leeres Label
```python
except ImportError:
    tk.Label(avatar_frame, text="", ...)  # text="" → unsichtbares Label!
```
→ **Fix:** `text="🚢"` als Fallback (wie im else-Zweig).

### Q-8 · sudo_start.sh: Variablen ohne Anführungszeichen
```bash
pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY ...
# ↑ sollte "$DISPLAY" "$XAUTHORITY" sein
```

### Q-9 · Toast positioniert sich immer am Bildschirmrand
Auf Multi-Monitor-Setups erscheint der Toast auf dem falschen Monitor.  
→ **Fix:** Position relativ zum Elternfenster berechnen.

### Q-10 · WipeTab: Zwei Bestätigungs-Dialoge in Folge ist schlechte UX
Ein einziger, gut formulierter Dialog reicht; zwei wirken als Test der Geduld.

### Q-11 · LVMTab: Status zeigt pvs/vgs/lvs im selben LogWidget ohne Trenner
Ausgabe fließt ineinander, kein Abstand zwischen den drei Befehlen.  
→ **Fix:** Trennzeile zwischen den Ausgaben.

### Q-12 · Kein fehler.log vorhanden (nur analyse.log in ZIP)
config.py definiert FEHLER_LOG, logger.py schreibt dorthin, aber die Datei
fehlt im Lieferumfang (kein Problem zur Laufzeit, da os.makedirs).

---

## ZUSAMMENFASSUNG

| Kategorie | Anzahl |
|-----------|--------|
| Kritische Bugs | 7 |
| Mittlere Bugs | 4 |
| Qualitätsmängel | 12 |
| **Gesamt** | **23** |

