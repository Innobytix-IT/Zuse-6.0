# ZUSE 🖥️
> **"Einfach weil 'Einfach' einfach ist."**

![Version](https://img.shields.io/badge/Version-6.9_Final_Core-blue) ![Language](https://img.shields.io/badge/Made_with-Python-yellow) ![Status](https://img.shields.io/badge/Status-Stable-green)

**Zuse** ist eine objektorientierte, interpretierte Programmiersprache, die entwickelt wurde, um die Barriere zwischen "Lern-Sprachen" (wie Scratch) und "Profi-Sprachen" (wie Python/C++) zu durchbrechen.

Sie ermöglicht Programmierung in der Muttersprache (DE, EN, ES, PT, FR, IT) und bietet einen nahtlosen Übergang von einfacher Grafik-Programmierung zur Steuerung komplexer Hardware.

---

## 🚀 Features

*   **🌍 Multilingual:** Der Interpreter versteht 6 Sprachen nativ (Deutsch, Englisch, Spanisch, Portugiesisch, Französisch, Italienisch).
*   **🛡️ Dual Mode:**
    *   **Lern-Modus:** Sandbox-Umgebung für Kinder/Anfänger (nur sichere Befehle).
    *   **Profi-Modus ("God Mode"):** Vollständiger Zugriff auf die Python-Runtime (inkl. Hardware-Steuerung).
*   **🧠 Environment Aware:** Zuse erkennt automatisch, ob es in der IDE oder als Standalone-Anwendung läuft und passt das Fenster-Management dynamisch an.
*   **🎨 Zuse Studio:** Eine eigene IDE mit Syntax-Highlighting, Live-Übersetzer und GUI-Block-Modus.

---

## 🛠️ System-Architektur

Zuse basiert auf einer **3-Schichten-Architektur**:

### 1. Der Kern (Interpreter)
Die Engine (`interpreter.py`) basiert auf Python. Sie verfügt über einen **Smart Import Mechanismus**, der verhindert, dass Sprachbibliotheken doppelt geladen werden, und erkennt Konstruktoren sprachübergreifend (`ERSTELLE`, `NEW`, `CREAR`...).

### 2. Die IDE (Zuse Studio)
Das Studio (`zuse_studio.py`) ist Thread-Safe und verfügt über eine **Pre-Flight-Check**-Logik. Sie warnt den Nutzer vor dem Start, wenn grafische Befehle genutzt werden, aber der notwendige GUI-Modus nicht aktiviert ist.

### 3. Die Standard-Bibliothek (Smart Layer)
Die `.zuse`-Dateien im Ordner `bibliothek/` sind intelligente Wrapper.
*   **Beispiel `KLASSE Fenster`:** Kapselt `tkinter`. Entscheidet automatisch, ob ein `tk.Tk()` (Standalone) oder ein `tk.Toplevel()` (Studio) erstellt wird und erzwingt im Studio den Tastatur-Fokus (`grab_set`).
*   **Beispiel `KLASSE Maler`:** Kapselt `turtle`. Beinhaltet einen "Anti-Zombie-Fix" (`clearscreen` + `_RUNNING=True`), um Abstürze bei Neustarts zu verhindern.

---

## 📚 Syntax Beispiele (Deutsch)

### Hallo Welt & Logik
```text
text = "Hallo Zuse"
zahl = 42

WENN zahl > 10 DANN
    AUSGABE text
SONST
    AUSGABE "Zahl ist klein"
ENDE WENN
```

### Schleifen
```text
SCHLEIFE FÜR i IN [1, 2, 3] MACHE
    AUSGABE "Durchlauf: " + str(i)
ENDE SCHLEIFE
```

### Objektorientierung
```text
KLASSE Roboter:
    DEFINIERE ERSTELLE(name):
        MEIN.name = name
    ENDE FUNKTION

    DEFINIERE hallo():
        AUSGABE "Ich bin " + MEIN.name
    ENDE FUNKTION
ENDE KLASSE

r1 = Roboter("ZuseBot")
r1.hallo()
```

### Grafik (Der Maler)
```text
BENUTZE deutsch
pablo = Maler()

pablo.farbe("blau")
pablo.dicke(5)

SCHLEIFE FÜR i IN [1, 2, 3, 4] MACHE
    pablo.gehe(100)
    pablo.drehe_rechts(90)
ENDE SCHLEIFE
```

---

## 🕹️ Nutzung

### Starten der IDE
```bash
python zuse_studio.py
```

### Ausführen eines Programms (Standalone)
```bash
python main.py mein_skript.zuse deutsch
```

---

## 🔌 Hardware & Deployment

Dank des **Profi-Modus** kann Zuse direkt auf Hardware zugreifen.

**Beispiel: Arduino steuern**
```text
BENUTZE pyfirmata
board = pyfirmata.Arduino("COM3")
led = board.get_pin("d:13:o")
led.write(1)
```

**Aktuelle Projekte:**
*   **PeugeotDash Car-PC:** Ein Shutdown-Controller, dessen Logik in Zuse geschrieben ist.

---

## 🗺️ Roadmap (Zuse 2.0 Vision)

*   [x] **v1.0 (v6.9):** Stabiler Interpreter, IDE, Bibliotheken (DE/EN/ES/PT/FR/IT).
*   [ ] **v2.0:** Entwicklung einer **Intermediate Representation (IR)** und eines Transpilers nach **JavaScript**, um Zuse-Programme direkt im Browser (WebAssembly/JS) auszuführen (Ziel: PWA Pilger-App).

---

**Architekt:** Manuel Person  
**Lizenz:** Open Source
```