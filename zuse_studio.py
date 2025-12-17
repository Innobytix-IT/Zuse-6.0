# FILE: zuse_studio.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import sys
import threading
import queue

# Sicherstellen, dass Module gefunden werden
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from translate import uebersetze_code
    from language_loader import lade_sprache
    from lexer import tokenize
    from parser import Parser
    from interpreter import Interpreter
except ImportError as e:
    messagebox.showerror("Boot Error", f"Module fehlen: {e}")
    sys.exit(1)

class ZuseStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Zuse Studio 6.0 - God Mode Edition")
        self.root.geometry("1100x800")
        self.current_lang = "deutsch"
        
        # Queues für Thread-Kommunikation
        self.output_queue = queue.Queue()
        self.input_request_queue = queue.Queue()
        
        self.active_interpreter = None
        
        # UI Aufbau
        main = tk.Frame(root, bg="#eee"); main.pack(fill="both", expand=True)
        
        # Toolbar
        bar = tk.Frame(main, bg="#ccc", height=40); bar.pack(fill="x", side="top")
        
        btn_run = tk.Button(bar, text="▶ START", bg="#8f8", command=self.run_thread)
        btn_run.pack(side="left", padx=5, pady=5)
        
        btn_stop = tk.Button(bar, text="⏹ STOP", bg="#f88", command=self.stop_thread)
        btn_stop.pack(side="left", padx=5)
        
        tk.Button(bar, text="💾 SAVE", command=self.save).pack(side="left", padx=5)
        tk.Button(bar, text="📂 LOAD", command=self.load).pack(side="left", padx=5)
        
        tk.Label(bar, text="Sprache:", bg="#ccc").pack(side="left", padx=10)
        self.lang_var = tk.StringVar(value="deutsch")
        self.cb_lang = ttk.Combobox(bar, textvariable=self.lang_var, values=self.get_langs(), state="readonly")
        self.cb_lang.pack(side="left")
        self.cb_lang.bind("<<ComboboxSelected>>", self.translate_view)

        # Editor
        self.text = tk.Text(main, font=("Consolas", 12), undo=True)
        self.text.pack(fill="both", expand=True, side="left", padx=5, pady=5)
        
        # Console
        self.cons = tk.Text(root, height=10, bg="#222", fg="#0f0", font=("Consolas", 11))
        self.cons.pack(fill="x", side="bottom")

        # Polling Loop starten
        self.root.after(100, self.check_queues)

    def get_langs(self):
        d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprachen")
        if not os.path.exists(d): return ["deutsch"]
        return [f.replace(".json","") for f in os.listdir(d) if f.endswith(".json")]

    def check_queues(self):
        """Prüft auf Nachrichten und Input-Requests"""
        # 1. Output (nicht blockierend)
        try:
            while True:
                msg = self.output_queue.get_nowait()
                self.cons.insert("end", msg + "\n")
                self.cons.see("end")
        except queue.Empty: pass
        
        # 2. Input Requests (Dialog im GUI Thread öffnen)
        try:
            req = self.input_request_queue.get_nowait()
            # req ist (prompt, modus, result_container, event)
            prompt, modus, container, evt = req
            
            # Dialog öffnen
            if modus == 'zahl':
                res = simpledialog.askfloat("Eingabe", prompt)
            else:
                res = simpledialog.askstring("Eingabe", prompt)
            
            # Ergebnis speichern und Event setzen
            container['value'] = res if res is not None else ""
            evt.set()
            
        except queue.Empty: pass

        self.root.after(100, self.check_queues)

    def stop_thread(self):
        if self.active_interpreter:
            self.active_interpreter.running = False
            self.cons.insert("end", "\n[STOP SIGNAL SENT]\n")

    def run_thread(self):
        self.cons.delete("1.0", tk.END)
        self.cons.insert("end", "Starte Programm...\n")
        
        code = self.text.get("1.0", tk.END)
        lang = self.current_lang
        
        t = threading.Thread(target=self._execute_logic, args=(code, lang))
        t.daemon = True
        t.start()

    def _interpreter_input_callback(self, prompt, modus):
        """Wird vom Interpreter-Thread aufgerufen. Blockiert, bis GUI antwortet."""
        evt = threading.Event()
        container = {'value': None}
        
        # Request in Queue legen
        self.input_request_queue.put((prompt, modus, container, evt))
        
        # Warten bis GUI fertig
        evt.wait()
        return container['value']

    def _execute_logic(self, code, lang):
        try:
            # 1. Pfade bestimmen für Standard-Bibliothek
            base_path = os.path.dirname(os.path.abspath(__file__))
            lib_path = os.path.join(base_path, "bibliothek", f"{lang}.zuse")
            
            # 2. Bibliothek laden (falls vorhanden) und vor den User-Code kleben
            final_code = code
            if os.path.exists(lib_path):
                try:
                    with open(lib_path, "r", encoding="utf-8") as f:
                        lib_code = f.read()
                        # Wir fügen die Bibliothek VOR den User-Code ein
                        final_code = lib_code + "\n\n" + code
                except Exception as e:
                    self.output_queue.put(f"[Warnung] Konnte Bibliothek '{lang}.zuse' nicht laden: {e}")

            # 3. Sprache laden und Parsen (nutzt final_code)
            conf = lade_sprache(lang)
            tokens = tokenize(final_code, conf) 
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Interpreter Instanz mit Callbacks
            self.active_interpreter = Interpreter(
                output_callback=self.output_queue.put,
                input_callback=self._interpreter_input_callback
            )
            self.active_interpreter.interpretiere(ast)
            
            self.output_queue.put("[Programm beendet]")
        except Exception as e:
            self.output_queue.put(f"Fehler: {e}")
        finally:
            self.active_interpreter = None

    def translate_view(self, event):
        new_l = self.lang_var.get()
        if new_l == self.current_lang: return
        code = self.text.get("1.0", tk.END)
        try:
            res = uebersetze_code(code, self.current_lang, new_l)
            self.text.delete("1.0", tk.END); self.text.insert("1.0", res)
            self.current_lang = new_l
        except Exception as e: messagebox.showerror("Error", str(e))

    def save(self):
        p = filedialog.asksaveasfilename(defaultextension=".zuse")
        if p: 
            with open(p,"w",encoding="utf-8") as f: f.write(self.text.get("1.0", tk.END))
    
    def load(self):
        p = filedialog.askopenfilename()
        if p:
            with open(p,"r",encoding="utf-8") as f: 
                self.text.delete("1.0", tk.END); self.text.insert("1.0", f.read())

if __name__ == "__main__":
    root = tk.Tk()
    ZuseStudio(root)
    root.mainloop()