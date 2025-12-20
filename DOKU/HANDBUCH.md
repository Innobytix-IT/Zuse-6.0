# 📘 ZUSE - Das offizielle Benutzerhandbuch
**Version:** 6.9 (Final Core)
**Stand:** Dezember 2025

---

## 👋 1. Willkommen bei Zuse

Zuse ist eine Programmiersprache, die entwickelt wurde, um **einfach** zu sein. Sie erlaubt es dir, in deiner Muttersprache zu programmieren (Deutsch, Englisch, Spanisch, etc.) und wächst mit deinen Fähigkeiten – vom ersten gezeichneten Quadrat bis zur Steuerung von Hardware.

### Die Philosophie
> **"Einfach, weil 'Einfach' einfach ist."**

---

## 🚀 2. Installation & Start

### Voraussetzungen
Zuse benötigt eine installierte **Python**-Version (3.x) auf deinem Computer.

### Starten der Entwicklungsumgebung (IDE)
Öffne den Zuse-Ordner und starte die Datei:
`zuse_studio.py`

*(Unter Windows meistens per Doppelklick oder über die Konsole mit `python zuse_studio.py`)*

---

## 🖥️ 3. Das Zuse Studio (Die IDE)

Das Studio ist deine Werkstatt. Hier sind die wichtigsten Funktionen:

### Die Toolbar (Leiste oben)
1.  **▶ START:** Führt dein aktuelles Programm aus.
2.  **⏹ STOP:** Bricht ein laufendes Programm ab.
3.  **💾 SAVE / 📂 LOAD:** Speichern und Laden von `.zuse` Dateien.
4.  **☑ GUI-Modus (Block):** **(WICHTIG!)**
    *   **Haken setzen:** Wenn dein Programm Fenster, Grafiken (Maler) oder Spiele (Snake) nutzt.
    *   **Haken entfernen:** Wenn dein Programm nur Text in der Konsole ausgibt oder im Hintergrund rechnet.
5.  **Modus:**
    *   **Lernen:** Sicherer Modus ("Sandbox"). Nur harmlose Befehle sind erlaubt. Perfekt für Anfänger.
    *   **Profi:** "God Mode". Zugriff auf das gesamte System (Dateien, Hardware, Internet).
6.  **Sprache:** Wähle hier die Sprache, in der du programmieren möchtest (z.B. `deutsch`). Der Editor passt die Farben (Highlighting) automatisch an.

---

## ✍️ 4. Programmieren in Zuse (Deutsch)

Hier lernst du die Grundlagen der deutschen Syntax.

---

### 4.1 Die erste Ausgabe
```text
AUSGABE "Hallo Welt!"
4.2 Variablen (Daten speichern)

Du musst keine Typen angeben. Zuse versteht das automatisch.

code
Text
download
content_copy
expand_less
name = "Manuel"
alter = 35
groesse = 1.80
liste = [1, 2, 3]
4.3 Entscheidungen (WENN / DANN)
code
Text
download
content_copy
expand_less
WENN alter > 18 DANN
    AUSGABE "Erwachsen"
SONST
    AUSGABE "Kind"
ENDE WENN
4.4 Schleifen (Wiederholungen)
code
Text
download
content_copy
expand_less
# Zählschleife
SCHLEIFE FÜR i IN [1, 2, 3] MACHE
    AUSGABE "Nummer: " + str(i)
ENDE SCHLEIFE

# Bedingte Schleife
SCHLEIFE SOLANGE alter < 100 MACHE
    alter = alter + 1
ENDE SCHLEIFE
4.5 Funktionen (Befehle selber bauen)
code
Text
download
content_copy
expand_less
DEFINIERE begruesse(name):
    AUSGABE "Hallo " + name
ENDE FUNKTION

begruesse("Anna")
🎨 5. Grafik & Spiele (Die Standard-Bibliothek)

Zuse bringt mächtige Werkzeuge mit, die dir viel Arbeit abnehmen. Wenn du oben "deutsch" auswählst, stehen diese Befehle automatisch bereit.

5.1 Der Maler (Schildkröten-Grafik)

Perfekt, um Programmieren zu lernen.

code
Text
download
content_copy
expand_less
# Erstellt einen Maler namens "pablo"
pablo = Maler()

pablo.farbe("rot")
pablo.dicke(5)

# Malt ein Quadrat
SCHLEIFE FÜR i IN [1, 2, 3, 4] MACHE
    pablo.gehe(100)
    pablo.drehe_rechts(90)
ENDE SCHLEIFE

Befehle: gehe(), zurueck(), drehe_links(), drehe_rechts(), stift_hoch(), stift_runter(), kreis(), farbe().

5.2 Fenster (Für Spiele & Apps)

Erstellt professionelle Programm-Fenster. Die Bibliothek kümmert sich automatisch um die technische Verwaltung.

code
Text
download
content_copy
expand_less
# Erstellt ein Fenster (Titel, Breite, Höhe)
spiel = Fenster("Mein Spiel", 400, 300)

# Erstellt eine Leinwand darin
leinwand = spiel.neue_leinwand("schwarz")

# Tastatur abfragen
DEFINIERE huepfen(event):
    AUSGABE "Hüpf!"
ENDE FUNKTION

spiel.taste_druecken("Leertaste", huepfen)

# Fenster offen halten
spiel.starte()
🔌 6. Profi-Modus & Hardware

Im Profi-Modus (oben im Studio auswählen) kannst du die Grenzen von Zuse sprengen und direkt auf Python-Module zugreifen.

Beispiel: Arduino steuern

Voraussetzung: pyfirmata muss auf dem PC installiert sein.

code
Text
download
content_copy
expand_less
# Zugriff auf Hardware-Bibliothek
BENUTZE pyfirmata

# Verbindung herstellen
board = pyfirmata.Arduino("COM3")

AUSGABE "Verbindung steht!"

# LED an Pin 13 einschalten
led = board.get_pin("d:13:o")
led.write(1)
🌍 7. Mehrsprachigkeit

Zuse spricht 6 Sprachen. Der Code funktioniert logisch immer gleich, nur die Wörter ändern sich.

Deutsch	Englisch	Spanisch	Portugiesisch	Französisch	Italienisch
WENN	IF	SI	SE	SI	SE
DANN	THEN	ENTONCES	ENTAO	ALORS	ALLORA
SCHLEIFE	LOOP	BUCLE	CICLO	BOUCLE	CICLO
Maler	Painter	Pintor	Pintor	Peintre	Pittore
Fenster	Window	Ventana	Janela	Fenetre	Finestra
⚠️ 8. Fehlerbehebung (FAQ)

F: Mein Fenster friert ein ("Keine Rückmeldung").
A: Du hast vergessen, den Haken bei "GUI-Modus (Block)" im Studio zu setzen. Grafik-Programme brauchen diesen Modus.

F: Fehlermeldung: "Sicherheits-Sperre: Modul ... nicht erlaubt".
A: Du versuchst ein Profi-Modul (wie os oder serial) zu laden, bist aber im "Lernen"-Modus. Schalte oben auf "Profi" um.

F: Mein Programm startet nicht, wenn ich die Sprache wechsele.
A: Drücke einmal auf STOP und dann wieder auf START. Zuse bereinigt den Speicher dann automatisch.

Viel Spaß beim Erschaffen!
Dein Zuse-Team

code
Code
download
content_copy
expand_less
---

### 2. Die Befehlsreferenz (`BEFEHLE.md`)

```markdown
# 📖 Zuse Befehls-Referenz (Version 6.9)

Diese Referenz gilt für die **deutsche Spracheinstellung**. In anderen Sprachen (Englisch, Spanisch etc.) ändert sich nur das Schlüsselwort (z.B. `WENN` -> `IF`), die Logik bleibt identisch.

## 1. Kern-Syntax (Schlüsselwörter)
Diese Befehle sind fest im **Parser** verankert und bilden das Gerüst der Sprache.

| Befehl | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| **Ausgabe & Eingabe** | | |
| `AUSGABE <Wert>` | Gibt Text oder Zahlen in der Konsole aus. | `AUSGABE "Hallo"` |
| `EINGABE_TEXT(<Frage>)` | Fragt den Benutzer nach einem Text (String). | `name = EINGABE_TEXT("Name?")` |
| `EINGABE_ZAHL(<Frage>)` | Fragt den Benutzer nach einer Zahl (Integer/Float). | `alter = EINGABE_ZAHL("Alter?")` |
| **Logik & Bedingungen** | | |
| `WENN <Bedingung> DANN` | Startet eine Bedingung. | `WENN x > 5 DANN` |
| `SONST` | Alternative, wenn die Bedingung nicht zutrifft. | `SONST` |
| `ENDE WENN` | Beendet den Bedingungs-Block. | `ENDE WENN` |
| `wahr` / `falsch` | Booleans (Wahrheitswerte). | `läuft = wahr` |
| **Schleifen** | | |
| `SCHLEIFE FÜR <Var> IN <Liste> MACHE` | Wiederholt für jedes Element einer Liste. | `SCHLEIFE FÜR i IN [1,2,3] MACHE` |
| `SCHLEIFE SOLANGE <Bedingung> MACHE` | Wiederholt, solange die Bedingung wahr ist. | `SCHLEIFE SOLANGE x < 10 MACHE` |
| `ENDE SCHLEIFE` | Beendet den Schleifen-Block. | `ENDE SCHLEIFE` |
| **Funktionen** | | |
| `DEFINIERE <Name>(<Params>):` | Erstellt eine neue Funktion. | `DEFINIERE hallo(name):` |
| `ERGEBNIS IST <Wert>` | Gibt einen Wert aus einer Funktion zurück (Return). | `ERGEBNIS IST x + y` |
| `ENDE FUNKTION` | Beendet die Funktions-Definition. | `ENDE FUNKTION` |
| `AKTION` (oder `AKTION():`) | Erstellt eine anonyme Funktion (Lambda), wichtig für Buttons. | `cmd = AKTION(): starte()` |
| `GLOBAL <Name>` | Macht eine Variable in einer Funktion global verfügbar. | `GLOBAL punktestand` |
| **Objektorientierung** | | |
| `KLASSE <Name>:` | Definiert eine neue Klasse. | `KLASSE Hund:` |
| `KLASSE <Name>(<Eltern>):` | Definiert eine Klasse mit Vererbung. | `KLASSE Dackel(Hund):` |
| `DEFINIERE ERSTELLE(...):` | Der Konstruktor. Wird beim Erzeugen aufgerufen. | `DEFINIERE ERSTELLE(name):` |
| `MEIN` | Referenz auf die eigene Instanz (wie `self` / `this`). | `MEIN.name = name` |
| `ELTERN` | Zugriff auf Methoden der Elternklasse (super). | `ELTERN.ruf()` |
| `ENDE KLASSE` | Beendet die Klassen-Definition. | `ENDE KLASSE` |
| **Fehlerbehandlung** | | |
| `VERSUCHE` | Startet einen Block, in dem Fehler auftreten dürfen. | `VERSUCHE` |
| `FANGE` | Fängt den Fehler ab, damit das Programm nicht abstürzt. | `FANGE` |
| `ENDE VERSUCHE` | Beendet den Fehler-Block. | `ENDE VERSUCHE` |
| **Module** | | |
| `BENUTZE <Modul> ALS <Alias>` | Lädt ein externes Modul oder eine Bibliothek. | `BENUTZE math ALS m` |

---

## 2. Eingebaute Funktionen (Global)
Diese Funktionen sind im **Interpreter** (`std_funcs`) definiert und stehen immer zur Verfügung.

| Funktion | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `str(wert)` | Wandelt eine Zahl in Text um. | `t = str(42)` |
| `int(wert)` | Wandelt Text/Kommazahl in eine ganze Zahl um. | `z = int("10")` |
| `float(wert)` | Wandelt Text in eine Kommazahl um. | `k = float("3.5")` |
| `len(objekt)` | Gibt die Länge einer Liste oder eines Textes zurück. | `l = len("Hallo")` |
| `typ(objekt)` | Gibt den Datentyp zurück (z.B. "str", "int"). | `t = typ(42)` |
| `liste()` | Erstellt eine leere Liste `[]`. | `l = liste()` |
| `dict()` | Erstellt ein leeres Wörterbuch `{}`. | `d = dict()` |
| `eval(code)` | Führt Python-Code als String aus (Mächtig!). | `res = eval("10 + 5")` |

---

## 3. Standard-Bibliothek: Grafik (`KLASSE Maler`)
Diese Befehle stehen zur Verfügung, wenn `pablo = Maler()` erstellt wurde (Turtle-Grafik).
*Voraussetzung:* `BENUTZE deutsch` (oder Spracheinstellung im Studio).

| Methode | Beschreibung | Parameter |
| :--- | :--- | :--- |
| `ERSTELLE()` | Erstellt Leinwand, setzt Reset (Anti-Zombie). | (Keine) |
| `gehe(schritte)` | Bewegt den Maler vorwärts. | Zahl (Pixel) |
| `zurueck(schritte)` | Bewegt den Maler rückwärts. | Zahl (Pixel) |
| `drehe_rechts(grad)` | Dreht den Maler nach rechts. | Zahl (Grad, 0-360) |
| `drehe_links(grad)` | Dreht den Maler nach links. | Zahl (Grad, 0-360) |
| `stift_hoch()` | Hebt den Stift (kein Zeichnen beim Bewegen). | (Keine) |
| `stift_runter()` | Senkt den Stift (Zeichnen aktiv). | (Keine) |
| `farbe(f)` | Setzt die Malfarbe. Erkennt deutsche Namen ("rot", "blau"...) und Hex-Codes. | Text ("rot", "#FF0000") |
| `dicke(d)` | Setzt die Strichstärke. | Zahl |
| `kreis(radius)` | Malt einen Kreis mit Radius r. | Zahl |
| `fertig()` | Beendet das Zeichnen (Formalität). | (Keine) |

---

## 4. Standard-Bibliothek: GUI (`KLASSE Fenster`)
Diese Befehle stehen zur Verfügung, wenn `win = Fenster(...)` erstellt wurde.
*Die Klasse entscheidet automatisch zwischen `Tk` und `Toplevel`.*

| Methode | Beschreibung | Parameter |
| :--- | :--- | :--- |
| `ERSTELLE(titel, b, h)` | Erstellt ein leeres Fenster. | Text, Zahl, Zahl |
| `neue_leinwand(farbe)` | Erstellt eine Zeichenfläche im Fenster. Gibt das Canvas-Objekt zurück. | Text (Farbe) |
| `taste_druecken(taste, aktion)` | Führt eine Funktion aus, wenn Taste gedrückt wird. | Text ("Links", "Leertaste"), Funktionsname |
| `nach_zeit(ms, funktion)` | Führt Funktion nach X Millisekunden aus (Timer/Loop). | Zahl (ms), Funktionsname |
| `setze_titel(text)` | Ändert den Fenstertitel (z.B. für Punkte). | Text |
| `schliessen()` | Schließt das Fenster. | (Keine) |
| `starte()` | Hält das Fenster offen (Mainloop). | (Keine) |

---

## 5. Standard-Bibliothek: Hilfsfunktionen
Direkt verfügbar über `BENUTZE deutsch`.

| Funktion | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `zufallszahl(min, max)` | Gibt eine zufällige ganze Zahl zurück. | `wuerfel = zufallszahl(1, 6)` |
| `warte(sekunden)` | Pausiert das Programm. | `warte(2)` |

---

## 6. Operatoren (Mathematik & Vergleich)

| Operator | Bedeutung |
| :--- | :--- |
| `+` | Plus (oder Text zusammenfügen) |
| `-` | Minus |
| `*` | Mal |
| `/` | Geteilt |
| `^` | Hoch (Potenz, z.B. 2^3 = 8) |
| `%` | Modulo (Rest bei Division) |
| `==` | Ist gleich |
| `!=` | Ist ungleich |
| `<` / `>` | Kleiner / Größer |
| `<=` / `>=` | Kleiner gleich / Größer gleich |
| `[` ... `]` | Liste erstellen | `x = [1, 2]` |
| `{` ... `}` | Dictionary erstellen | `x = {"a": 1}` |
| `objekt.attribut` | Zugriff auf Methoden oder Variablen eines Objekts. |

---

## 7. Profi-Modus (Hardware & System)
Wenn der Modus im Studio auf "Profi" steht, sind **alle** Python-Module importierbar.

**Beispiele:**
*   `BENUTZE pyfirmata` (Arduino Steuerung)
*   `BENUTZE serial` (Serielle Schnittstelle)
*   `BENUTZE os` (Dateisystem)
*   `BENUTZE time` (Zeitfunktionen)
*   `BENUTZE math` (Erweiterte Mathematik wie Sinus/Cosinus)