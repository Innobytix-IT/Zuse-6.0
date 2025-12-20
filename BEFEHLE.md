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