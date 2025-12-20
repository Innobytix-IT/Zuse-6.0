# FILE: main.py
from language_loader import lade_sprache
from lexer import tokenize
from parser import Parser
from interpreter import Interpreter
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Benutzung: python main.py <datei.zuse> [sprache]")
        print("Beispiel: python main.py spiel.zuse deutsch")
        sys.exit(1)

    dateiname = sys.argv[1]
    # Standard-Sprache ist deutsch, falls nichts angegeben wird
    sprache = sys.argv[2] if len(sys.argv) > 2 else "deutsch"

    if not os.path.exists(dateiname):
        print(f"Fehler: Datei '{dateiname}' nicht gefunden.")
        sys.exit(1)

    try:
        # 1. Benutzer-Code laden
        with open(dateiname, 'r', encoding='utf-8') as f:
            user_code = f.read()

        # 2. Bibliothek suchen und laden (genau wie im Studio)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        lib_path = os.path.join(base_dir, "bibliothek", f"{sprache}.zuse")
        
        final_code = user_code
        
        if os.path.exists(lib_path):
            try:
                with open(lib_path, 'r', encoding='utf-8') as f:
                    lib_code = f.read()
                    # Wir kleben die Bibliothek VOR den Benutzer-Code
                    final_code = lib_code + "\n\n" + user_code
            except Exception as e:
                print(f"Warnung: Konnte Standard-Bibliothek nicht laden: {e}")
        
        # 3. Ausführen
        config = lade_sprache(sprache)
        tokens = tokenize(final_code, config)
        parser = Parser(tokens)
        ast = parser.parse()
        
        interpreter = Interpreter(output_callback=print)
        interpreter.interpretiere(ast)

    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()