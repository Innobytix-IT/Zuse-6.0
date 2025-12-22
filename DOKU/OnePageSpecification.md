# Zuse 6.x – One‑Page Specification

## Ziel

Zuse 6.0 ist eine **mehrsprachige, textbasierte Programmiersprache**, deren **natürliche Sprache der Keywords austauschbar** ist, ohne Semantik, AST oder Laufzeit zu verändern. Sie trennt strikt **Oberflächensyntax** (Landessprache) von **kanonischer Sprachrepräsentation**.

---

## Kernidee

* **Kanonische Sprache**: Alle Sprachkonstrukte werden intern über feste Schlüssel (`KW_WENN`, `KW_FANGE`, …) repräsentiert.
* **Sprach-Mapping**: Natürliche Sprachen sind externe Konfigurationen (JSON), die kanonische Schlüssel auf konkrete Wörter abbilden.
* **AST‑Stabilität**: Parser und Interpreter arbeiten ausschließlich mit kanonischen Symbolen.
* **Übersetzbarkeit**: Quellcode kann verlustfrei zwischen Landessprachen übersetzt werden.

---

## Architektur

**Pipeline**

1. **Language Loader** lädt Sprach‑Mapping (z. B. `deutsch.json`).
2. **Lexer** erkennt Keywords anhand des Mappings und erzeugt Tokens mit kanonischen Typen.
3. **Parser** erzeugt einen sprachunabhängigen **AST**.
4. **Interpreter** führt den AST aus (semantisch invariant).
5. **Studio/IDE** erlaubt Live‑Übersetzung und Ausführung.

**Trennung der Ebenen**

* Oberfläche: natürliche Sprache
* Syntax: kanonische Tokens
* Semantik: AST + Interpreter

---

## Sprachmerkmale

* **Imperativ & objektorientiert** (Klassen, Methoden, Vererbung, `SELBST`, `ELTERN`).
* **Kontrollstrukturen**: `WENN/SONST`, Schleifen (`SOLANGE`, `FÜR`), Fehlerbehandlung (`VERSUCHE/FANGE`).
* **Funktionen & Lambdas**.
* **Datenstrukturen**: Listen, Dictionaries, Slicing.
* **Ein-/Ausgabe**: text/zahl.
* **Python‑Bridge (God Mode)**: Zugriff auf Python‑Module und ‑Objekte.

---

## Mehrsprachigkeit

* **Beliebige Anzahl von Landessprachen** über JSON‑Dateien.
* **Kein Neu‑Parsen** der Semantik beim Sprachwechsel.
* **Deterministische Übersetzung** zwischen Sprachen (kanonische Zwischenschicht).

---

## Laufzeit & Sicherheit

* **Sandbox‑Interpreter** mit kontrolliertem Modulimport.
* **Rekursionstiefen‑Limit**.
* **Thread‑sichere GUI‑Integration** (nicht blockierende Eingaben).

---

## Design‑Prinzipien

* Sprachneutraler Kern
* Erweiterbarkeit statt Monolith
* Lesbarkeit vor Kürze
* Bildung & Exploration als Primärziel

---

## Abgrenzung

* Keine reine Keyword‑Übersetzung: **kanonischer Sprachkernel**.
* Keine visuelle Sprache: **vollwertige Textsprache**.
* Keine Editor‑Lokalisierung: **sprachliche Semantik bleibt identisch**.

---

## Einsatzgebiete

* Bildung & Lehre in der Muttersprache
* Mehrsprachige Teams & Dokumentation
* Sprach‑ und Compilerforschung
* Rapid Prototyping mit Python‑Ökosystem

---

## Status

* Funktionsfähiger Interpreter & IDE
* Mehrsprachige Syntax produktiv
* Weiterentwicklung: Spezifikation, Tests, Tooling
---
## Ausblick für die Zukunft 

Zuse soll in Zukunft weiter ausgebaut werden so das es auf auch auf weiteren Programmiersprachen aufsetzen kann. 

Dieses Konzept nennen wir:  
"double multilingual"

<img width="800" height="810" alt="image" src="https://github.com/user-attachments/assets/4f2eaad8-9a04-4fc3-8a67-aadbfec8988e" />


