# FILE: zuse_studio.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import io
from contextlib import redirect_stdout

# Zuse Module importieren
from translate import uebersetze_code
from language_loader import lade_sprache
from lexer import tokenize
from parser import Parser
from interpreter import Interpreter

class ZuseStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Zuse Studio - Der Code Baukasten")
        self.root.geometry("1000x700")
        
        # Aktuelle Einstellungen
        self.current_lang = "deutsch"
        self.file_path = None

        # --- LAYOUT ---
        # Haupt-Container
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)

        # 1. Toolbar (Oben)
        toolbar = tk.Frame(main_frame, bg="#ddd", height=40)
        toolbar.pack(fill="x", side="top")

        # Buttons in der Toolbar
        btn_run = tk.Button(toolbar, text="▶ Starten", bg="#90ee90", command=self.run_code)
        btn_run.pack(side="left", padx=5, pady=5)

        btn_save = tk.Button(toolbar, text="💾 Speichern", command=self.save_file)
        btn_save.pack(side="left", padx=5, pady=5)

        btn_load = tk.Button(toolbar, text="📂 Laden", command=self.load_file)
        btn_load.pack(side="left", padx=5, pady=5)

        # Sprach-Auswahl
        tk.Label(toolbar, text="Sprache:", bg="#ddd").pack(side="left", padx=(20, 5))
        self.lang_var = tk.StringVar(value="deutsch")
        self.combo_lang = ttk.Combobox(toolbar, textvariable=self.lang_var, state="readonly")
        self.combo_lang['values'] = self.get_available_languages()
        self.combo_lang.pack(side="left", padx=5)
        self.combo_lang.bind("<<ComboboxSelected>>", self.on_language_change)

        # 2. Lego-Leiste (Links) - Die "Bausteine"
        lego_frame = tk.Frame(main_frame, bg="#555", width=150)
        lego_frame.pack(fill="y", side="left")
        tk.Label(lego_frame, text="BAUSTEINE", bg="#555", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

        # Baustein-Buttons (Fügen Code ein)
        self.create_lego_btn(lego_frame, "WENN / DANN", "#ff9999", self.insert_if)
        self.create_lego_btn(lego_frame, "SCHLEIFE", "#99ccff", self.insert_loop)
        self.create_lego_btn(lego_frame, "AUSGABE", "#ffff99", self.insert_print)
        self.create_lego_btn(lego_frame, "KLASSE", "#cc99ff", self.insert_class)
        self.create_lego_btn(lego_frame, "FUNKTION", "#99ff99", self.insert_func)

        # 3. Editor Bereich (Mitte)
        self.editor = tk.Text(main_frame, font=("Consolas", 12), undo=True)
        self.editor.pack(fill="both", expand=True, side="left", padx=5, pady=5)

        # 4. Konsole (Unten) für Ausgaben
        console_frame = tk.Frame(root, height=150, bg="black")
        console_frame.pack(fill="x", side="bottom")
        tk.Label(console_frame, text="Konsole / Ausgabe:", bg="black", fg="white").pack(anchor="w")
        self.console = tk.Text(console_frame, height=8, bg="black", fg="#00ff00", font=("Consolas", 10))
        self.console.pack(fill="both", expand=True)

    def get_available_languages(self):
        """Scannt den sprachen/ Ordner"""
        langs = []
        path = os.path.join(os.path.dirname(__file__), "sprachen")
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.endswith(".json"):
                    langs.append(f.replace(".json", ""))
        return langs if langs else ["deutsch"]

    def create_lego_btn(self, parent, text, color, command):
        """Erstellt einen hübschen Knopf für die Bausteine"""
        btn = tk.Button(parent, text=text, bg=color, relief="raised", bd=3, command=command)
        btn.pack(fill="x", padx=5, pady=5)

    # --- LOGIK ---

    def on_language_change(self, event):
        new_lang = self.lang_var.get()
        if new_lang == self.current_lang:
            return
        
        # Code übersetzen
        code = self.editor.get("1.0", tk.END)
        try:
            translated = uebersetze_code(code, self.current_lang, new_lang)
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", translated)
            self.current_lang = new_lang
            self.log(f"Sprache gewechselt zu: {new_lang}")
        except Exception as e:
            messagebox.showerror("Fehler beim Übersetzen", str(e))
            self.lang_var.set(self.current_lang) # Zurücksetzen

    def run_code(self):
        self.console.delete("1.0", tk.END)
        code = self.editor.get("1.0", tk.END)
        
        # stdout umleiten, damit print() in der GUI landet
        f = io.StringIO()
        try:
            with redirect_stdout(f):
                # 1. Config laden
                config = lade_sprache(self.current_lang)
                # 2. Tokenize
                tokens = tokenize(code, config)
                # 3. Parse
                parser = Parser(tokens)
                ast = parser.parse()
                # 4. Interpretieren
                interpreter = Interpreter()
                interpreter.interpretiere(ast)
            
            output = f.getvalue()
            self.log(output)
            self.log("\n✅ Programm erfolgreich.")
        except Exception as e:
            self.log(f"\n❌ Fehler: {e}")

    def log(self, text):
        self.console.insert(tk.END, text)
        self.console.see(tk.END)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".zuse", filetypes=[("Zuse Dateien", "*.zuse")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.editor.get("1.0", tk.END))
            self.file_path = file_path
            self.log(f"Gespeichert unter: {file_path}\n")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Zuse Dateien", "*.zuse")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", f.read())
            self.file_path = file_path
            self.log(f"Geladen: {file_path}\n")

    # --- LEGO BAUSTEINE EINFÜGEN ---
    # Diese Funktionen fügen Templates ein, passend zur aktuellen Sprache
    
    def get_keywords(self):
        return lade_sprache(self.current_lang)

    def insert_if(self):
        kw = self.get_keywords()
        # Wir holen uns die Wörter aus der aktuellen Sprachdatei
        block = f'\n{kw.get("KW_WENN", "WENN")} (1 == 1) {kw.get("KW_DANN", "DANN")}\n    {kw.get("KW_AUSGABE", "AUSGABE")} "Ja"\n{kw.get("KW_ENDE_WENN", "ENDE WENN")}\n'
        self.editor.insert(tk.INSERT, block)

    def insert_loop(self):
        kw = self.get_keywords()
        block = f'\n{kw.get("KW_SCHLEIFE", "SCHLEIFE")} {kw.get("KW_SOLANGE", "SOLANGE")} (x < 10) {kw.get("KW_MACHE", "MACHE")}\n    {kw.get("KW_AUSGABE", "AUSGABE")} x\n{kw.get("KW_ENDE_SCHLEIFE", "ENDE SCHLEIFE")}\n'
        self.editor.insert(tk.INSERT, block)

    def insert_print(self):
        kw = self.get_keywords()
        block = f'\n{kw.get("KW_AUSGABE", "AUSGABE")} "Hallo Welt"\n'
        self.editor.insert(tk.INSERT, block)

    def insert_class(self):
        kw = self.get_keywords()
        block = f'\n{kw.get("KW_KLASSE", "KLASSE")} Name\n    {kw.get("KW_DEFINIERE", "DEFINIERE")} test()\n    {kw.get("KW_ENDE_FUNKTION", "ENDE FUNKTION")}\n{kw.get("KW_ENDE_KLASSE", "ENDE KLASSE")}\n'
        self.editor.insert(tk.INSERT, block)

    def insert_func(self):
        kw = self.get_keywords()
        block = f'\n{kw.get("KW_DEFINIERE", "DEFINIERE")} name()\n    {kw.get("KW_AUSGABE", "AUSGABE")} "Test"\n{kw.get("KW_ENDE_FUNKTION", "ENDE FUNKTION")}\n'
        self.editor.insert(tk.INSERT, block)

if __name__ == "__main__":
    root = tk.Tk()
    app = ZuseStudio(root)
    root.mainloop()