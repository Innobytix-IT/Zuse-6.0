# FILE: zuse_studio.py
# VERSION: 6.8 (Smart Run & Pre-Flight Check)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import sys
import threading
import queue
import re
import json
import traceback

# Pfad-Setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from language_loader import lade_sprache
    from lexer import tokenize
    from parser import Parser
    from interpreter import Interpreter
    try: from translate import uebersetze_code
    except: uebersetze_code = None
except ImportError as e:
    messagebox.showerror("Boot Error", f"Module fehlen: {e}")
    sys.exit(1)

class ZuseEditorWidget(tk.Frame):
    def __init__(self, master, studio_ref, **kwargs):
        super().__init__(master, **kwargs)
        self.studio = studio_ref
        self.text_font = ("Consolas", 12)
        
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.on_scroll)
        self.scrollbar.pack(side="right", fill="y")
        
        self.linenumbers = tk.Text(self, width=4, padx=4, takefocus=0, border=0,
                                   background="#333", foreground="#888",
                                   state="disabled", font=self.text_font)
        self.linenumbers.pack(side="left", fill="y")
        
        self.text = tk.Text(self, font=self.text_font, undo=True, yscrollcommand=self.on_text_scroll)
        self.text.pack(side="left", fill="both", expand=True)
        
        self.text.tag_configure("keyword", foreground="#FFA500", font=(self.text_font[0], self.text_font[1], "bold")) 
        self.text.tag_configure("string", foreground="#98C379") 
        self.text.tag_configure("comment", foreground="#7F848E") 
        self.text.tag_configure("number", foreground="#56B6C2") 
        self.text.tag_configure("definition", foreground="#61AFEF", font=(self.text_font[0], self.text_font[1], "bold")) 
        
        self.text.bind("<KeyRelease>", self.on_content_changed)
        self.text.bind("<MouseWheel>", self.on_text_scroll_event)
        
        self.update_linenumbers()

    def on_scroll(self, *args):
        self.text.yview(*args)
        self.linenumbers.yview(*args)

    def on_text_scroll(self, *args):
        self.scrollbar.set(*args)
        self.linenumbers.yview_moveto(args[0])
    
    def on_text_scroll_event(self, event):
        self.linenumbers.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_content_changed(self, event=None):
        self.update_linenumbers()
        self.highlight_syntax()

    def update_linenumbers(self):
        line_count = self.text.get('1.0', tk.END).count('\n')
        if line_count == 0: line_count = 1
        lines = "\n".join(str(i) for i in range(1, line_count + 1))
        self.linenumbers.config(state="normal")
        self.linenumbers.delete("1.0", tk.END)
        self.linenumbers.insert("1.0", lines)
        self.linenumbers.config(state="disabled")
        self.linenumbers.yview_moveto(self.text.yview()[0])

    def highlight_syntax(self):
        code = self.text.get("1.0", tk.END)
        for tag in ["keyword", "string", "comment", "number", "definition"]:
            self.text.tag_remove(tag, "1.0", tk.END)
            
        lang_config = lade_sprache(self.studio.current_lang)
        keywords = list(lang_config.values())
        keywords.sort(key=len, reverse=True)
        
        kw_pattern = r'\b(' + '|'.join(re.escape(k) for k in keywords) + r')\b'
        self.apply_regex(kw_pattern, "keyword")
        self.apply_regex(r'"[^"]*"', "string")
        self.apply_regex(r'#.*', "comment")
        self.apply_regex(r'\b\d+\b', "number")
        
        kw_def = lang_config.get("KW_DEFINIERE", "DEFINIERE")
        kw_class = lang_config.get("KW_KLASSE", "KLASSE")
        def_pattern = rf'(?:{re.escape(kw_def)}|{re.escape(kw_class)})\s+([A-Za-z_][A-Za-z0-9_]*)'
        for match in re.finditer(def_pattern, code):
            start_idx = f"1.0 + {match.start(1)} chars"
            end_idx = f"1.0 + {match.end(1)} chars"
            self.text.tag_add("definition", start_idx, end_idx)

    def apply_regex(self, pattern, tag):
        code = self.text.get("1.0", tk.END)
        for match in re.finditer(pattern, code):
            start_idx = f"1.0 + {match.start()} chars"
            end_idx = f"1.0 + {match.end()} chars"
            self.text.tag_add(tag, start_idx, end_idx)

class ZuseStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Zuse Studio 6.8 - Smart Run Edition")
        self.root.geometry("1100x800")
        self.current_lang = "deutsch"
        
        self.output_queue = queue.Queue()
        self.input_request_queue = queue.Queue()
        self.active_interpreter = None
        
        main = tk.Frame(root, bg="#eee"); main.pack(fill="both", expand=True)
        
        bar = tk.Frame(main, bg="#ccc", height=40); bar.pack(fill="x", side="top")
        
        btn_run = tk.Button(bar, text="▶ START", bg="#8f8", command=self.run_decider)
        btn_run.pack(side="left", padx=5, pady=5)
        
        btn_stop = tk.Button(bar, text="⏹ STOP", bg="#f88", command=self.stop_thread)
        btn_stop.pack(side="left", padx=5)
        
        tk.Button(bar, text="💾 SAVE", command=self.save).pack(side="left", padx=5)
        tk.Button(bar, text="📂 LOAD", command=self.load).pack(side="left", padx=5)
        
        self.gui_mode_var = tk.BooleanVar(value=False)
        chk = tk.Checkbutton(bar, text="GUI-Modus (Block)", variable=self.gui_mode_var, bg="#ccc")
        chk.pack(side="left", padx=10)

        tk.Label(bar, text="| Modus:", bg="#ccc").pack(side="left", padx=5)
        self.mode_var = tk.StringVar(value="Profi")
        self.cb_mode = ttk.Combobox(bar, textvariable=self.mode_var, values=["Profi", "Lernen"], state="readonly", width=8)
        self.cb_mode.pack(side="left", padx=5)
        
        tk.Label(bar, text="| Sprache:", bg="#ccc").pack(side="left", padx=5)
        self.lang_var = tk.StringVar(value="deutsch")
        self.cb_lang = ttk.Combobox(bar, textvariable=self.lang_var, values=self.get_langs(), state="readonly")
        self.cb_lang.pack(side="left")
        if uebersetze_code:
            self.cb_lang.bind("<<ComboboxSelected>>", self.translate_view)

        self.editor = ZuseEditorWidget(main, self)
        self.editor.pack(fill="both", expand=True, side="left", padx=5, pady=5)
        
        self.cons = tk.Text(root, height=10, bg="#222", fg="#0f0", font=("Consolas", 11))
        self.cons.pack(fill="x", side="bottom")

        self.root.after(100, self.check_queues)

    def get_langs(self):
        d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprachen")
        if not os.path.exists(d): return ["deutsch"]
        return [f.replace(".json","") for f in os.listdir(d) if f.endswith(".json")]

    def check_queues(self):
        try:
            while True:
                msg = self.output_queue.get_nowait()
                self.cons.insert("end", str(msg) + "\n")
                self.cons.see("end")
        except queue.Empty: pass
        
        try:
            req = self.input_request_queue.get_nowait()
            prompt, modus, container, evt = req
            if modus == 'zahl': res = simpledialog.askfloat("Eingabe", prompt)
            else: res = simpledialog.askstring("Eingabe", prompt)
            container['value'] = res if res is not None else ""
            evt.set()
        except queue.Empty: pass

        self.root.after(100, self.check_queues)

    def stop_thread(self):
        if self.active_interpreter:
            self.active_interpreter.running = False
            self.output_queue.put("\n[STOP SIGNAL SENT]\n")

    # --- NEU: INTELLIGENTE CODE ANALYSE ---
    def check_gui_usage(self, code):
        """Prüft grob, ob der Code grafische Elemente nutzt."""
        # Liste der verdächtigen Wörter in allen Sprachen
        gui_keywords = [
            'tkinter', 'turtle',  # Module
            'Maler', 'Fenster',   # DE
            'Painter', 'Window',  # EN
            'Pintor', 'Janela',   # ES/PT
            'Peintre', 'Fenetre', # FR
            'Pittore', 'Finestra' # IT
        ]
        
        # Einfacher Regex-Check auf Wortgrenzen
        for kw in gui_keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', code):
                return True
        return False

    def run_decider(self):
        """Entscheidet intelligent über den Start"""
        code = self.editor.text.get("1.0", tk.END)
        needs_gui = self.check_gui_usage(code)
        is_gui_mode = self.gui_mode_var.get()
        
        # FALL 1: Code braucht GUI, aber Haken fehlt -> ALARM!
        if needs_gui and not is_gui_mode:
            messagebox.showerror("Sicherheits-Stopp", 
                "Dein Programm nutzt grafische Elemente (Fenster/Maler)!\n\n"
                "Bitte aktiviere die Checkbox 'GUI-Modus (Block)',\n"
                "sonst stürzt das Studio ab.")
            return # Start abbrechen

        # FALL 2: Code braucht KEINE GUI, aber Haken ist gesetzt -> HINWEIS
        if not needs_gui and is_gui_mode:
            if not messagebox.askyesno("Hinweis", 
                "Dein Programm scheint keine Grafik zu nutzen.\n"
                "Der GUI-Modus wird das Studio blockieren.\n\n"
                "Trotzdem fortfahren?"):
                return # Abbruch durch User

        # Wenn wir hier sind, ist alles okay.
        self.cons.delete("1.0", tk.END)
        self.cons.insert("end", "Starte Programm...\n")
        lang = self.current_lang
        
        if self.gui_mode_var.get():
            self.output_queue.put("[INFO] GUI-Modus aktiv. Studio wartet...")
            self.root.after(100, lambda: self._execute_logic(code, lang, threaded=False))
        else:
            t = threading.Thread(target=self._execute_logic, args=(code, lang, True))
            t.daemon = True
            t.start()
    # --------------------------------------

    def _interpreter_input_callback(self, prompt, modus):
        if threading.current_thread() is threading.main_thread():
             if modus == 'zahl': return simpledialog.askfloat("Eingabe", prompt) or 0
             return simpledialog.askstring("Eingabe", prompt) or ""
        
        evt = threading.Event()
        container = {'value': None}
        self.input_request_queue.put((prompt, modus, container, evt))
        evt.wait()
        return container['value']

    def _execute_logic(self, code, lang, threaded=True):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            lib_path = os.path.join(base_path, "bibliothek", f"{lang}.zuse")
            
            final_code = code
            start_line_offset = 1 
            ist_lernmodus = (self.mode_var.get() == "Lernen")

            # Bibliothek laden
            if os.path.exists(lib_path):
                try:
                    with open(lib_path, "r", encoding="utf-8") as f:
                        lib_code = f.read()
                        lib_lines = lib_code.count('\n') + 2 
                        start_line_offset = 1 - lib_lines 
                        final_code = lib_code + "\n\n" + code
                except Exception as e:
                    self.output_queue.put(f"[Warnung] Lib Fehler: {e}")

            conf = lade_sprache(lang)
            tokens = tokenize(final_code, conf, start_line=start_line_offset)
            parser = Parser(tokens)
            ast = parser.parse()
            
            self.active_interpreter = Interpreter(
                output_callback=self.output_queue.put,
                input_callback=self._interpreter_input_callback,
                safe_mode=ist_lernmodus 
            )
            
            # --- ENV INJECTION ---
            self.active_interpreter.global_env.set("__UMGEBUNG__", "STUDIO")
            # ---------------------
            
            self.active_interpreter.interpretiere(ast)
            
            self.output_queue.put("[Programm beendet]")
        except Exception as e:
            self.output_queue.put(f"Fehler: {e}")
            import traceback
            traceback.print_exc() 
        finally:
            self.active_interpreter = None

    def translate_view(self, event):
        new_l = self.lang_var.get()
        if new_l == self.current_lang: return

        # 1. Alte Sprache merken
        old_l = self.current_lang
        
        # 2. FIX: Sofort umschalten, egal was passiert
        self.current_lang = new_l
        
        # 3. Highlighting anpassen
        self.editor.highlight_syntax()

        # 4. Versuch zu übersetzen
        if uebersetze_code:
            code = self.editor.text.get("1.0", tk.END)
            if len(code.strip()) > 0:
                try:
                    res = uebersetze_code(code, old_l, new_l)
                    self.editor.text.delete("1.0", tk.END)
                    self.editor.text.insert("1.0", res)
                    
                    self.editor.highlight_syntax() 
                    self.editor.update_linenumbers()
                except Exception as e:
                    print(f"[Info] Auto-Übersetzung übersprungen: {e}")
    
    def save(self):
        p = filedialog.asksaveasfilename(defaultextension=".zuse")
        if p: 
            with open(p,"w",encoding="utf-8") as f: f.write(self.editor.text.get("1.0", tk.END))
    
    def load(self):
        p = filedialog.askopenfilename()
        if p:
            with open(p,"r",encoding="utf-8") as f: 
                self.editor.text.delete("1.0", tk.END); 
                self.editor.text.insert("1.0", f.read())
                
                self.editor.highlight_syntax()
                self.editor.update_linenumbers()

if __name__ == "__main__":
    root = tk.Tk()
    ZuseStudio(root)
    root.mainloop()