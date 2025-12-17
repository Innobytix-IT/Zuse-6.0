# FILE: interpreter.py (Version ZUSE 6.0 GOD MODE)
import time
import math
import random
import datetime
import threading
import tkinter
import importlib # <--- WICHTIG: Für dynamische Imports

# Standard-Module, die immer da sein sollen (Aliases)
ALLOWED_MODULES = {
    'mathe': math,
    'zufall': random,
    'zeit': time,
    'datum': datetime,
    'tkinter': tkinter
}

class ZuseError(Exception):
    pass

class Environment:
    def __init__(self, parent=None, variables=None):
        self.vars = variables if variables is not None else {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise ZuseError(f"Variable '{name}' nicht definiert.")

    def set(self, name, value):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent and self.parent.has_recursive(name):
            self.parent.set(name, value)
        else:
            self.vars[name] = value

    def define(self, name, value):
        self.vars[name] = value

    def has_recursive(self, name):
        if name in self.vars: return True
        if self.parent: return self.parent.has_recursive(name)
        return False
        
    def delete(self, name):
        if name in self.vars:
            del self.vars[name]

    def copy(self):
        return Environment(parent=self)

class ZuseFunction:
    def __init__(self, name, parameter, body, definition_env, owner_class=None):
        self.name = name
        self.parameter = parameter
        self.body = body
        self.definition_env = definition_env 
        self.is_lambda = isinstance(body, dict)
        self.owner_class = owner_class
        self.bound_instance = None 

class ZuseClassWrapper:
    def __init__(self, ast_node, env):
        self.ast = ast_node
        self.env = env 

class ZuseInstance:
    def __init__(self, class_wrapper, interpreter_ref):
        self._class_wrapper = class_wrapper
        self._class_name = class_wrapper.ast['name']
        self._attributes = {}
        self._interpreter = interpreter_ref

    def get_attr(self, name):
        if name in self._attributes:
            return self._attributes[name]
        return None

    def set_attr(self, name, val):
        self._attributes[name] = val

    def find_method(self, method_name, start_class_wrapper=None):
        curr_wrapper = start_class_wrapper or self._class_wrapper
        
        while curr_wrapper:
            ast = curr_wrapper.ast
            for m in ast['methoden']:
                if m['name'] == method_name:
                    return m, curr_wrapper.env, curr_wrapper 
            
            parent_name = ast.get('elternklasse')
            if parent_name:
                try:
                    parent_wrapper = curr_wrapper.env.get(parent_name)
                    if not isinstance(parent_wrapper, ZuseClassWrapper):
                        raise ZuseError(f"'{parent_name}' ist keine Klasse.")
                    curr_wrapper = parent_wrapper
                except ZuseError:
                    return None, None, None
            else:
                curr_wrapper = None
        return None, None, None

class Interpreter:
    def __init__(self, output_callback=print, input_callback=input):
        self.global_env = Environment()
        
        std_funcs = {
            'str': lambda x: str(x),
            'int': lambda x: int(float(x)),
            'float': lambda x: float(x),
            'len': lambda x: len(x),
            'typ': lambda x: type(x).__name__,
            'liste': lambda: [],
            'dict': lambda: {},
            'eval': lambda x: eval(x)
        }
        for k, v in std_funcs.items():
            self.global_env.define(k, v)

        self.output_callback = output_callback
        self.input_callback = input_callback
        self.running = True
        self.recursion_depth = 0
        self.MAX_RECURSION = 1000

    def print_out(self, text):
        self.output_callback(str(text))

    def input_in(self, prompt, modus):
        return self.input_callback(prompt, modus)

    def _python_bridge_wrapper(self, zuse_func):
        def bridge(*p_args):
            return self._call_function(zuse_func, list(p_args), zuse_func.definition_env)
        return bridge

    def _prepare_python_args(self, args, kwargs):
        new_args = []
        for a in args:
            if isinstance(a, ZuseFunction):
                new_args.append(self._python_bridge_wrapper(a))
            else:
                new_args.append(a)
        
        new_kwargs = {}
        for k, v in kwargs.items():
            if isinstance(v, ZuseFunction):
                new_kwargs[k] = self._python_bridge_wrapper(v)
            else:
                new_kwargs[k] = v
        return new_args, new_kwargs

    def interpretiere(self, ast):
        try:
            if ast['type'] != 'PROGRAMM': raise ZuseError("Ungültiger AST-Startknoten")
            
            for anweisung in ast['body']:
                if not self.running: break
                self.execute_node(anweisung, self.global_env)
                    
        except ZuseError as e:
            self.print_out(f"Laufzeitfehler: {e}")
        except RecursionError:
            self.print_out("Kritischer Fehler: Maximale Rekursionstiefe überschritten.")
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.print_out(f"Systemfehler: {e}")

    def execute_node(self, node, env):
        if not node or not self.running: return
        
        self.recursion_depth += 1
        if self.recursion_depth > self.MAX_RECURSION:
            self.recursion_depth -= 1
            raise ZuseError("Maximale Rekursionstiefe erreicht.")

        try:
            typ = node.get('type')

            if typ == 'ZUWEISUNG':
                wert = self.evaluiere_ausdruck(node['wert'], env)
                ziel = node['ziel']
                
                if ziel['type'] == 'VARIABLE':
                    name = ziel['name']
                    try:
                        is_global = env.get('__globals__')
                        if is_global and name in is_global:
                            self.global_env.vars[name] = wert
                        else:
                            env.set(name, wert)
                    except ZuseError:
                        env.define(name, wert)

                elif ziel['type'] == 'ATTRIBUT_ZUGRIFF':
                    obj = self.evaluiere_ausdruck(ziel['objekt'], env)
                    if isinstance(obj, ZuseInstance):
                        obj.set_attr(ziel['attribut'], wert)
                    else:
                        try: setattr(obj, ziel['attribut'], wert)
                        except: raise ZuseError(f"Kann Attribut '{ziel['attribut']}' nicht setzen.")
                
                elif ziel['type'] == 'INDEX_ZUGRIFF':
                    obj = self.evaluiere_ausdruck(ziel['objekt'], env)
                    idx = self.evaluiere_ausdruck(ziel['index'], env)
                    try: obj[idx] = wert
                    except Exception as e: raise ZuseError(f"Fehler bei Index-Zuweisung: {e}")
                
                else:
                    raise ZuseError(f"Ungültiges Zuweisungsziel: {ziel['type']}")

            elif typ == 'FUNKTIONS_DEFINITION':
                func = ZuseFunction(node['name'], node['parameter'], node['body'], env)
                env.define(node['name'], func)
            
            elif typ == 'KLASSEN_DEFINITION':
                wrapper = ZuseClassWrapper(node, env)
                env.define(node['name'], wrapper)

            elif typ == 'GLOBAL_ANWEISUNG':
                try: globals_set = env.get('__globals__')
                except:
                    globals_set = set()
                    env.define('__globals__', globals_set)
                globals_set.add(node['name'])
                if node['name'] not in self.global_env.vars:
                    self.global_env.define(node['name'], None)

            elif typ == 'WENN_ANWEISUNG':
                for bedingung_node, block in node['faelle']:
                    if self.evaluiere_ausdruck(bedingung_node, env):
                        for a in block:
                            res = self.execute_node(a, env)
                            if res: return res
                        return
                if node.get('sonst_koerper'):
                    for a in node['sonst_koerper']:
                        res = self.execute_node(a, env)
                        if res: return res

            elif typ == 'SCHLEIFE_SOLANGE':
                while self.running and self.evaluiere_ausdruck(node['bedingung'], env):
                    for a in node['koerper']:
                        res = self.execute_node(a, env)
                        if res: return res

            elif typ == 'SCHLEIFE_FÜR':
                iter_obj = self.evaluiere_ausdruck(node['liste'], env)
                var_name = node['variable']
                try: iterator = iter(iter_obj)
                except TypeError: raise ZuseError("Objekt ist nicht iterierbar.")
                
                old_val = None
                existed = env.has_recursive(var_name)
                if existed: old_val = env.get(var_name)

                try:
                    for el in iterator:
                        if not self.running: break
                        env.set(var_name, el)
                        for a in node['koerper']:
                            res = self.execute_node(a, env)
                            if res: return res
                finally:
                    if existed: env.set(var_name, old_val)
                    else: env.delete(var_name)

            elif typ == 'VERSUCHE_ANWEISUNG':
                try:
                    for a in node['versuche_block']: self.execute_node(a, env)
                except Exception:
                    for a in node['fange_block']: self.execute_node(a, env)

            elif typ == 'AUSGABE_ANWEISUNG':
                val = self.evaluiere_ausdruck(node['wert'], env)
                self.print_out(val)

            elif typ == 'ERGEBNIS_ANWEISUNG':
                return ('RÜCKGABE', self.evaluiere_ausdruck(node['wert'], env))

            elif typ == 'IMPORT_ANWEISUNG':
                mod_name = node['modul']
                alias = node['alias']
                
                # --- UNIVERSAL IMPORT (GOD MODE) ---
                if mod_name in ALLOWED_MODULES:
                    env.define(alias, ALLOWED_MODULES[mod_name])
                else:
                    try:
                        # Versuche das Modul dynamisch aus der Python-Umgebung zu laden
                        imported_module = importlib.import_module(mod_name)
                        env.define(alias, imported_module)
                    except ImportError:
                        raise ZuseError(f"Modul '{mod_name}' nicht gefunden (auch nicht in Python).")
                    except Exception as e:
                        raise ZuseError(f"Fehler beim Import von '{mod_name}': {e}")
                # -----------------------------------

            elif typ in ['FUNKTIONS_AUFRUF', 'METHODEN_AUFRUF']:
                self.evaluiere_ausdruck(node, env)

        finally:
            self.recursion_depth -= 1

    def evaluiere_ausdruck(self, node, env):
        typ = node.get('type')

        if typ == 'ZAHL_LITERAL': 
            val = node['wert']
            return float(val) if '.' in val else int(val)
        if typ == 'STRING_LITERAL': return node['wert'][1:-1]
        if typ == 'LISTEN_LITERAL': return [self.evaluiere_ausdruck(e, env) for e in node['elemente']]
        if typ == 'DICT_LITERAL': return {self.evaluiere_ausdruck(k,env): self.evaluiere_ausdruck(v,env) for k,v in node['paare']}
        
        if typ == 'VARIABLE':
            name = node['name']
            if name == 'SELBST': 
                try: return env.get('SELBST')
                except: raise ZuseError("'SELBST' ist hier nicht definiert.")
            if name == 'wahr': return True
            if name == 'falsch': return False
            try: return env.get(name)
            except ZuseError: raise ZuseError(f"Variable '{name}' nicht definiert.")
            
        if typ == 'ELTERN_ZUGRIFF':
            try:
                inst = env.get('SELBST')
                return {'type': 'ELTERN_PROXY', 'instance': inst}
            except: raise ZuseError("'ELTERN' nur innerhalb von Methoden gültig.")

        if typ == 'BINÄRER_AUSDRUCK':
            l = self.evaluiere_ausdruck(node['links'], env)
            r = self.evaluiere_ausdruck(node['rechts'], env)
            op = node['operator']
            try:
                if op == '+': return (str(l)+str(r)) if (isinstance(l,str) or isinstance(r,str)) else l+r
                if op == '-': return l - r
                if op == '*': return l * r
                if op == '/': return l / r
                if op == '^': return l ** r
                if op == '%': return l % r
                if op == '==': return l == r
                if op == '!=': return l != r
                if op == '>': return l > r
                if op == '<': return l < r
                if op == '>=': return l >= r
                if op == '<=': return l <= r
            except Exception as e: raise ZuseError(f"Rechenfehler: {e}")

        if typ == 'UNAER_MINUS':
            return -self.evaluiere_ausdruck(node['wert'], env)

        if typ == 'SLICING':
            obj = self.evaluiere_ausdruck(node['objekt'], env)
            start = self.evaluiere_ausdruck(node['start'], env) if node['start'] else None
            ende = self.evaluiere_ausdruck(node['ende'], env) if node['ende'] else None
            return obj[start:ende]

        if typ == 'INDEX_ZUGRIFF':
            obj = self.evaluiere_ausdruck(node['objekt'], env)
            idx = self.evaluiere_ausdruck(node['index'], env)
            try: return obj[idx]
            except Exception: raise ZuseError(f"Ungültiger Index-Zugriff auf {idx}")

        if typ == 'ATTRIBUT_ZUGRIFF':
            obj = self.evaluiere_ausdruck(node['objekt'], env)
            attr = node['attribut']
            if isinstance(obj, ZuseInstance):
                val = obj.get_attr(attr)
                if val is not None:
                    return val
                
                method_def, def_env, owner = obj.find_method(attr)
                if method_def:
                    func = ZuseFunction(method_def['name'], method_def['parameter'], method_def['body'], def_env, owner_class=owner)
                    func.bound_instance = obj
                    return func

                raise ZuseError(f"Attribut oder Methode '{attr}' nicht gefunden.")
            
            try: return getattr(obj, attr)
            except: raise ZuseError(f"Attribut '{attr}' nicht gefunden.")

        if typ == 'LAMBDA_ERSTELLUNG':
            return ZuseFunction("lambda", node['params'], {'type': 'ERGEBNIS_ANWEISUNG', 'wert': node['body']}, env)

        if typ == 'FUNKTIONS_AUFRUF':
            func_obj = self.evaluiere_ausdruck({'type': 'VARIABLE', 'name': node['name']}, env)
            args = [self.evaluiere_ausdruck(a, env) for a in node['args']]
            kwargs = {k: self.evaluiere_ausdruck(v, env) for k, v in node['kwargs']}
            
            if callable(func_obj) and not isinstance(func_obj, (ZuseFunction, ZuseClassWrapper)):
                args, kwargs = self._prepare_python_args(args, kwargs)

            return self._call_function(func_obj, args, env, kwargs=kwargs)

        if typ == 'METHODEN_AUFRUF':
            obj_eval = self.evaluiere_ausdruck(node['objekt'], env)
            args = [self.evaluiere_ausdruck(a, env) for a in node['args']]
            kwargs = {k: self.evaluiere_ausdruck(v, env) for k, v in node['kwargs']}
            
            if isinstance(obj_eval, dict) and obj_eval.get('type') == 'ELTERN_PROXY':
                inst = obj_eval['instance']
                try: current_class_ctx = env.get('__class_context__')
                except: raise ZuseError("'ELTERN' kann nur innerhalb einer Klasse verwendet werden.")

                parent_name = current_class_ctx.ast.get('elternklasse')
                if not parent_name: raise ZuseError("Klasse hat keine Elternklasse.")

                try: parent_wrapper = current_class_ctx.env.get(parent_name)
                except: raise ZuseError(f"Elternklasse '{parent_name}' nicht gefunden.")

                method_def, def_env, owner = inst.find_method(node['methode'], start_class_wrapper=parent_wrapper)
                if not method_def: raise ZuseError(f"Methode '{node['methode']}' in Elternklasse nicht gefunden.")
                
                func = ZuseFunction(method_def['name'], method_def['parameter'], method_def['body'], def_env, owner_class=owner)
                return self._call_function(func, args, env, self_obj=inst, kwargs=kwargs)

            elif isinstance(obj_eval, ZuseInstance):
                method_def, def_env, owner = obj_eval.find_method(node['methode'])
                if not method_def: raise ZuseError(f"Methode '{node['methode']}' nicht gefunden.")
                
                func = ZuseFunction(method_def['name'], method_def['parameter'], method_def['body'], def_env, owner_class=owner)
                return self._call_function(func, args, env, self_obj=obj_eval, kwargs=kwargs)

            elif isinstance(obj_eval, ZuseClassWrapper):
                if node['methode'] == 'ERSTELLE':
                    return self._call_function(obj_eval, args, env, kwargs=kwargs)
                else:
                    raise ZuseError(f"Statische Methode '{node['methode']}' auf Klasse '{obj_eval.ast['name']}' nicht gefunden. Meintest du 'ERSTELLE'?")

            else:
                args, kwargs = self._prepare_python_args(args, kwargs)
                try: return getattr(obj_eval, node['methode'])(*args, **kwargs)
                except Exception as e: raise ZuseError(f"Externer Aufruf fehlgeschlagen: {e}")

        if typ == 'EINGABE_AUFRUF':
            prompt = str(self.evaluiere_ausdruck(node['prompt'], env))
            val = self.input_in(prompt, node['modus'])
            if node['modus'] == 'zahl':
                try:
                    f = float(val)
                    return int(f) if f.is_integer() else f
                except: return 0
            return val

        return None

    def _call_function(self, func, args, caller_env, self_obj=None, kwargs=None):
        if kwargs is None: kwargs = {}

        if isinstance(func, ZuseFunction):
            local_env = Environment(parent=func.definition_env)
            for i, param in enumerate(func.parameter):
                if i < len(args): local_env.define(param, args[i])
            
            for k, v in kwargs.items():
                local_env.define(k, v)

            if func.bound_instance:
                self_obj = func.bound_instance

            if self_obj: local_env.define('SELBST', self_obj)
            
            if func.owner_class:
                local_env.define('__class_context__', func.owner_class)

            if func.is_lambda:
                res = self.execute_node(func.body, local_env)
                return res[1] if res else None
            else:
                for stmt in func.body:
                    res = self.execute_node(stmt, local_env)
                    if res and res[0] == 'RÜCKGABE': return res[1]
                return None
        
        if isinstance(func, ZuseClassWrapper):
            inst = ZuseInstance(func, self)
            constr, c_env, owner = inst.find_method('ERSTELLE')
            if constr:
                c_func = ZuseFunction('ERSTELLE', constr['parameter'], constr['body'], c_env, owner_class=owner)
                self._call_function(c_func, args, caller_env, self_obj=inst, kwargs=kwargs)
            return inst

        if callable(func):
            args, kwargs = self._prepare_python_args(args, kwargs)
            return func(*args, **kwargs)

        raise ZuseError(f"Objekt '{func}' ist nicht aufrufbar.")