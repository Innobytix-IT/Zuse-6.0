# FILE: parser.py (Version ZUSE 4.5 KWARGS)

class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t['type'] != 'KOMMENTAR']
        self.pos = 0

    def aktuelles_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else {'type': 'EOF'}

    def gehe_weiter(self):
        self.pos += 1

    def peek_token(self, offset=1):
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else {'type': 'EOF'}

    def erwarte(self, typ, value=None):
        tok = self.aktuelles_token()
        if tok['type'] != typ:
            raise RuntimeError(f"Syntaxfehler Zeile {tok.get('line','?')}: Erwartet '{typ}', gefunden '{tok['type']}' ({tok.get('value')})")
        if value and tok.get('value') != value:
            if typ == 'KEYWORD' and tok.get('value') == value: pass
            else: raise RuntimeError(f"Syntaxfehler Zeile {tok.get('line','?')}: Erwartet '{value}', gefunden '{tok.get('value')}'")
        self.gehe_weiter()
        return tok

    def ist_kw(self, canonical_key):
        t = self.aktuelles_token()
        return t['type'] == 'KEYWORD' and t['value'] == canonical_key

    def parse(self):
        anweisungen = []
        while self.aktuelles_token()['type'] != 'EOF':
            if self.aktuelles_token()['type'] == 'NEUEZEILE':
                self.gehe_weiter(); continue
            anweisungen.append(self.parse_anweisung())
        return {'type': 'PROGRAMM', 'body': anweisungen}

    def parse_anweisung(self):
        token = self.aktuelles_token()

        if token['type'] == 'KEYWORD':
            val = token['value']
            if val == 'KW_DEFINIERE': return self.parse_funktions_definition()
            if val == 'KW_KLASSE':    return self.parse_klassen_definition()
            if val == 'KW_VERSUCHE':  return self.parse_versuche_anweisung()
            if val == 'KW_AUSGABE':   return self.parse_ausgabe_anweisung()
            if val == 'KW_ERGEBNIS':  return self.parse_ergebnis_anweisung()
            if val == 'KW_WENN':      return self.parse_wenn_anweisung()
            if val == 'KW_SCHLEIFE':  return self.parse_schleife_anweisung()
            if val == 'KW_BENUTZE':   return self.parse_import_anweisung()
            if val == 'KW_GLOBAL':    return self.parse_global_anweisung()

        if token['type'] == 'NAME' or (token['type'] == 'KEYWORD' and token['value'] in ['KW_SELBST', 'KW_ELTERN']):
            expr = self.parse_ausdruck()
            
            if self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] == '=':
                self.gehe_weiter()
                wert = self.parse_ausdruck()
                valid_types = ['VARIABLE', 'ATTRIBUT_ZUGRIFF', 'INDEX_ZUGRIFF', 'ATTRIBUT_ZUWEISUNG']
                if expr['type'] not in valid_types:
                    raise RuntimeError(f"Syntaxfehler Zeile {token.get('line')}: Ungültiges Ziel für Zuweisung.")
                return {'type': 'ZUWEISUNG', 'ziel': expr, 'wert': wert}
            return expr

        return self.parse_ausdruck()

    def parse_klassen_definition(self):
        self.erwarte('KEYWORD', 'KW_KLASSE')
        name = self.erwarte('NAME').get('value')
        
        elternklasse = None
        if self.aktuelles_token()['type'] == 'KLAMMER_AUF':
            self.gehe_weiter()
            elternklasse = self.erwarte('NAME').get('value')
            self.erwarte('KLAMMER_ZU')
        
        if self.aktuelles_token()['type'] == 'DOPPELPUNKT': self.gehe_weiter()
        self.erwarte('NEUEZEILE')
        
        methoden = []
        while not self.ist_kw('KW_ENDE_KLASSE'):
            if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
            if self.ist_kw('KW_DEFINIERE'): methoden.append(self.parse_funktions_definition())
            else: raise RuntimeError("In KLASSE sind nur DEFINIERE erlaubt.")
        self.erwarte('KEYWORD', 'KW_ENDE_KLASSE')
        return {'type': 'KLASSEN_DEFINITION', 'name': name, 'elternklasse': elternklasse, 'methoden': methoden}

    def parse_versuche_anweisung(self):
        self.erwarte('KEYWORD', 'KW_VERSUCHE'); self.erwarte('NEUEZEILE'); v = []; f = []
        while not self.ist_kw('KW_FANGE'):
            if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
            v.append(self.parse_anweisung())
        self.erwarte('KEYWORD', 'KW_FANGE'); self.erwarte('NEUEZEILE')
        while not self.ist_kw('KW_ENDE_VERSUCHE'):
             if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
             f.append(self.parse_anweisung())
        self.erwarte('KEYWORD', 'KW_ENDE_VERSUCHE')
        return {'type': 'VERSUCHE_ANWEISUNG', 'versuche_block': v, 'fange_block': f}

    def parse_funktions_definition(self):
        self.erwarte('KEYWORD', 'KW_DEFINIERE'); name = self.erwarte('NAME').get('value'); self.erwarte('KLAMMER_AUF')
        params = []
        if self.aktuelles_token()['type'] != 'KLAMMER_ZU':
            params.append(self.erwarte('NAME').get('value'))
            while self.aktuelles_token()['type'] == 'KOMMA': self.gehe_weiter(); params.append(self.erwarte('NAME').get('value'))
        self.erwarte('KLAMMER_ZU')
        if self.aktuelles_token()['type'] == 'DOPPELPUNKT': self.gehe_weiter()
        self.erwarte('NEUEZEILE'); body = []
        while not self.ist_kw('KW_ENDE_FUNKTION'):
            if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
            body.append(self.parse_anweisung())
        self.erwarte('KEYWORD', 'KW_ENDE_FUNKTION')
        return {'type': 'FUNKTIONS_DEFINITION', 'name': name, 'parameter': params, 'body': body}

    def parse_wenn_anweisung(self):
        self.erwarte('KEYWORD', 'KW_WENN')
        faelle = [] 
        bed = self.parse_ausdruck()
        self.erwarte('KEYWORD', 'KW_DANN'); self.erwarte('NEUEZEILE')
        body = []
        while not (self.ist_kw('KW_SONST') or self.ist_kw('KW_ENDE_WENN')):
            if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
            body.append(self.parse_anweisung())
        faelle.append((bed, body))
        
        sonst_body = None
        while self.ist_kw('KW_SONST'):
            self.gehe_weiter()
            if self.ist_kw('KW_WENN'):
                self.gehe_weiter()
                bed = self.parse_ausdruck()
                self.erwarte('KEYWORD', 'KW_DANN'); self.erwarte('NEUEZEILE')
                body = []
                while not (self.ist_kw('KW_SONST') or self.ist_kw('KW_ENDE_WENN')):
                    if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
                    body.append(self.parse_anweisung())
                faelle.append((bed, body))
            else:
                self.erwarte('NEUEZEILE')
                sonst_body = []
                while not self.ist_kw('KW_ENDE_WENN'):
                    if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
                    sonst_body.append(self.parse_anweisung())
                break

        self.erwarte('KEYWORD', 'KW_ENDE_WENN')
        return {'type': 'WENN_ANWEISUNG', 'faelle': faelle, 'sonst_koerper': sonst_body}

    def parse_schleife_anweisung(self):
        self.erwarte('KEYWORD', 'KW_SCHLEIFE')
        if self.ist_kw('KW_SOLANGE'):
            self.gehe_weiter(); bed = self.parse_ausdruck(); self.erwarte('KEYWORD', 'KW_MACHE'); self.erwarte('NEUEZEILE'); k = []
            while not self.ist_kw('KW_ENDE_SCHLEIFE'):
                if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
                k.append(self.parse_anweisung())
            self.erwarte('KEYWORD', 'KW_ENDE_SCHLEIFE')
            return {'type': 'SCHLEIFE_SOLANGE', 'bedingung': bed, 'koerper': k}
        elif self.ist_kw('KW_FUER'):
            self.gehe_weiter(); var = self.erwarte('NAME').get('value'); self.erwarte('KEYWORD', 'KW_IN'); lst = self.parse_ausdruck(); self.erwarte('KEYWORD', 'KW_MACHE'); self.erwarte('NEUEZEILE'); k = []
            while not self.ist_kw('KW_ENDE_SCHLEIFE'):
                if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
                k.append(self.parse_anweisung())
            self.erwarte('KEYWORD', 'KW_ENDE_SCHLEIFE')
            return {'type': 'SCHLEIFE_FÜR', 'variable': var, 'liste': lst, 'koerper': k}
        raise RuntimeError("Schleifenfehler")

    def parse_global_anweisung(self):
        self.erwarte('KEYWORD', 'KW_GLOBAL'); n = self.erwarte('NAME').get('value')
        return {'type': 'GLOBAL_ANWEISUNG', 'name': n}
    def parse_import_anweisung(self):
        self.erwarte('KEYWORD', 'KW_BENUTZE'); m = self.erwarte('NAME').get('value'); a = None
        if self.ist_kw('KW_ALS'): self.gehe_weiter(); a = self.erwarte('NAME').get('value')
        return {'type': 'IMPORT_ANWEISUNG', 'modul': m, 'alias': a or m}
    def parse_ausgabe_anweisung(self):
        self.erwarte('KEYWORD', 'KW_AUSGABE'); w = self.parse_ausdruck()
        return {'type': 'AUSGABE_ANWEISUNG', 'wert': w}
    def parse_ergebnis_anweisung(self):
        self.erwarte('KEYWORD', 'KW_ERGEBNIS'); w = self.parse_ausdruck()
        return {'type': 'ERGEBNIS_ANWEISUNG', 'wert': w}

    def parse_ausdruck(self): return self.parse_vergleich()
    def parse_vergleich(self):
        links = self.parse_arithmetik()
        while self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] in ['==','!=','<','>','<=','>=']:
            op = self.erwarte('OPERATOR').get('value')
            rechts = self.parse_arithmetik()
            links = {'type': 'BINÄRER_AUSDRUCK', 'links': links, 'operator': op, 'rechts': rechts}
        return links
    def parse_arithmetik(self):
        links = self.parse_term()
        while self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] in ['+', '-']:
            op = self.erwarte('OPERATOR').get('value')
            rechts = self.parse_term()
            links = {'type': 'BINÄRER_AUSDRUCK', 'links': links, 'operator': op, 'rechts': rechts}
        return links
    def parse_term(self):
        links = self.parse_faktor()
        while self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] in ['*', '/', '%']:
            op = self.erwarte('OPERATOR').get('value')
            rechts = self.parse_faktor()
            links = {'type': 'BINÄRER_AUSDRUCK', 'links': links, 'operator': op, 'rechts': rechts}
        return links
    def parse_faktor(self):
        if self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] == '-':
            self.gehe_weiter()
            return {'type': 'UNAER_MINUS', 'wert': self.parse_faktor()}
        links = self.parse_atom()
        if self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] == '^':
            op = self.erwarte('OPERATOR').get('value')
            rechts = self.parse_faktor()
            return {'type': 'BINÄRER_AUSDRUCK', 'links': links, 'operator': op, 'rechts': rechts}
        return links

    def parse_atom(self):
        node = self._parse_basis()
        while True:
            t = self.aktuelles_token()
            if t['type'] == 'PUNKT':
                self.gehe_weiter(); attr = self.erwarte('NAME').get('value')
                if self.aktuelles_token()['type'] == 'KLAMMER_AUF':
                    res = self._parse_argument_liste()
                    node = {'type': 'METHODEN_AUFRUF', 'objekt': node, 'methode': attr, 'args': res['args'], 'kwargs': res['kwargs']}
                else:
                    node = {'type': 'ATTRIBUT_ZUGRIFF', 'objekt': node, 'attribut': attr}
            elif t['type'] == 'KLAMMER_AUF_ECKIG':
                self.gehe_weiter()
                start = None
                if self.aktuelles_token()['type'] != 'DOPPELPUNKT': start = self.parse_ausdruck()
                if self.aktuelles_token()['type'] == 'DOPPELPUNKT':
                    self.gehe_weiter(); ende = None
                    if self.aktuelles_token()['type'] != 'KLAMMER_ZU_ECKIG': ende = self.parse_ausdruck()
                    self.erwarte('KLAMMER_ZU_ECKIG')
                    node = {'type': 'SLICING', 'objekt': node, 'start': start, 'ende': ende}
                else:
                    self.erwarte('KLAMMER_ZU_ECKIG')
                    node = {'type': 'INDEX_ZUGRIFF', 'objekt': node, 'index': start}
            else: break
        return node

    def _parse_basis(self):
        t = self.aktuelles_token()
        if t['type'] == 'KEYWORD':
            val = t['value']
            if val == 'KW_SELBST': self.gehe_weiter(); return {'type': 'VARIABLE', 'name': 'SELBST'}
            if val == 'KW_ELTERN': self.gehe_weiter(); return {'type': 'ELTERN_ZUGRIFF'}
            if val == 'CONST_WAHR': self.gehe_weiter(); return {'type': 'VARIABLE', 'name': 'wahr'}
            if val == 'CONST_FALSCH': self.gehe_weiter(); return {'type': 'VARIABLE', 'name': 'falsch'}
            if val == 'KW_LAMBDA': return self.parse_lambda()
            if val == 'FUNC_EINGABE_TEXT':
                self.gehe_weiter(); prompt = self.parse_ausdruck()
                return {'type': 'EINGABE_AUFRUF', 'modus': 'text', 'prompt': prompt}
            if val == 'FUNC_EINGABE_ZAHL':
                self.gehe_weiter(); prompt = self.parse_ausdruck()
                return {'type': 'EINGABE_AUFRUF', 'modus': 'zahl', 'prompt': prompt}
        if t['type'] == 'ZAHL': self.gehe_weiter(); return {'type': 'ZAHL_LITERAL', 'wert': t['value']}
        if t['type'] == 'STRING': self.gehe_weiter(); return {'type': 'STRING_LITERAL', 'wert': t['value']}
        if t['type'] == 'KLAMMER_AUF': 
            self.gehe_weiter(); node = self.parse_ausdruck(); self.erwarte('KLAMMER_ZU')
            return node
        if t['type'] == 'KLAMMER_AUF_ECKIG': return self.parse_listen_literal()
        if t['type'] == 'GESCHWEIFT_AUF': return self.parse_dict_literal()
        if t['type'] == 'NAME':
            name = t['value']; self.gehe_weiter()
            if self.aktuelles_token()['type'] == 'KLAMMER_AUF':
                res = self._parse_argument_liste()
                return {'type': 'FUNKTIONS_AUFRUF', 'name': name, 'args': res['args'], 'kwargs': res['kwargs']}
            return {'type': 'VARIABLE', 'name': name}
        raise RuntimeError(f"Unerwartetes Token: {t.get('value')} Zeile {t.get('line')}")

    def parse_dict_literal(self):
        self.erwarte('GESCHWEIFT_AUF'); paare = []
        if self.aktuelles_token()['type'] != 'GESCHWEIFT_ZU':
            k = self.parse_ausdruck(); self.erwarte('DOPPELPUNKT'); v = self.parse_ausdruck(); paare.append((k, v))
            while self.aktuelles_token()['type'] == 'KOMMA':
                self.gehe_weiter(); k = self.parse_ausdruck(); self.erwarte('DOPPELPUNKT'); v = self.parse_ausdruck(); paare.append((k, v))
        self.erwarte('GESCHWEIFT_ZU')
        return {'type': 'DICT_LITERAL', 'paare': paare}

    def _parse_argument_liste(self):
        self.erwarte('KLAMMER_AUF')
        args = []
        kwargs = [] # Liste von Tupeln um Reihenfolge zu wahren für AST
        
        if self.aktuelles_token()['type'] != 'KLAMMER_ZU':
            while True:
                # Check ob Keyword Argument: NAME gefolgt von =
                is_kwarg = False
                if self.aktuelles_token()['type'] == 'NAME':
                    nxt = self.peek_token()
                    if nxt['type'] == 'OPERATOR' and nxt['value'] == '=':
                        is_kwarg = True
                
                if is_kwarg:
                    k = self.erwarte('NAME').get('value')
                    self.erwarte('OPERATOR', '=')
                    v = self.parse_ausdruck()
                    kwargs.append((k, v))
                else:
                    args.append(self.parse_ausdruck())
                
                if self.aktuelles_token()['type'] == 'KOMMA':
                    self.gehe_weiter()
                else:
                    break
                    
        self.erwarte('KLAMMER_ZU')
        return {'args': args, 'kwargs': kwargs}

    def parse_listen_literal(self):
        self.erwarte('KLAMMER_AUF_ECKIG'); el = []
        if self.aktuelles_token()['type'] != 'KLAMMER_ZU_ECKIG':
            el.append(self.parse_ausdruck())
            while self.aktuelles_token()['type'] == 'KOMMA': self.gehe_weiter(); el.append(self.parse_ausdruck())
        self.erwarte('KLAMMER_ZU_ECKIG')
        return {'type': 'LISTEN_LITERAL', 'elemente': el}

    def parse_lambda(self):
        self.erwarte('KEYWORD', 'KW_LAMBDA')
        params = []
        if self.aktuelles_token()['type'] == 'KLAMMER_AUF':
            self.gehe_weiter()
            if self.aktuelles_token()['type'] != 'KLAMMER_ZU':
                params.append(self.erwarte('NAME').get('value'))
                while self.aktuelles_token()['type'] == 'KOMMA':
                    self.gehe_weiter(); params.append(self.erwarte('NAME').get('value'))
            self.erwarte('KLAMMER_ZU')
        else:
            params.append(self.erwarte('NAME').get('value'))
        
        self.erwarte('DOPPELPUNKT')
        body = self.parse_ausdruck()
        return {'type': 'LAMBDA_ERSTELLUNG', 'params': params, 'body': body}