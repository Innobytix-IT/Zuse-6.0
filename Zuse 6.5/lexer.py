# FILE: lexer.py (Version ZUSE 6.1 OFFSET FIX)
import re

STATIC_TOKENS = [
    ('STRING',     r'"[^"]*"'),
    ('ZAHL',       r'\d+\.\d+|\.\d+|\d+'), 
    ('NAME',       r'[A-Za-z_äöüÄÖÜß][A-Za-z0-9_äöüÄÖÜß]*'),
    ('OPERATOR',   r'==|!=|<=|>=|[+\-*/=<>\^%]'),
    ('KLAMMER_AUF',r'\('),
    ('KLAMMER_ZU', r'\)'),
    ('KLAMMER_AUF_ECKIG', r'\['),
    ('KLAMMER_ZU_ECKIG',  r'\]'),
    ('GESCHWEIFT_AUF',    r'\{'),
    ('GESCHWEIFT_ZU',     r'\}'),
    ('KOMMA',      r','),
    ('PUNKT',      r'\.'),
    ('DOPPELPUNKT', r':'),
    ('NEUEZEILE',  r'\n'),
    ('LEERZEICHEN',r'[ \t]+'),
    ('KOMMENTAR',  r'#.*'),
    ('UNBEKANNT',  r'.'),
]

class Lexer:
    def __init__(self, sprach_config):
        self.sprach_config = sprach_config
        self.token_regex = self._baue_regex()

    def _baue_regex(self):
        keywords = []
        for key, value in self.sprach_config.items():
            escaped = re.escape(value)
            pattern_str = escaped.replace(r'\ ', r'\s+')
            pattern = rf'\b{pattern_str}\b'
            keywords.append((key, pattern))
        
        keywords.sort(key=lambda x: len(x[1]), reverse=True)
        alle_regeln = keywords + STATIC_TOKENS
        regex_parts = [f'(?P<{name}>{pattern})' for name, pattern in alle_regeln]
        return re.compile('|'.join(regex_parts))

    def tokenize(self, code, start_line=1): # <--- WICHTIG: Hier muss start_line stehen
        tokens = []
        line_num = start_line 
        
        for mo in self.token_regex.finditer(code):
            kind = mo.lastgroup
            value = mo.group()
            start_pos = mo.start()
            end_pos = mo.end()

            if kind == 'NEUEZEILE':
                line_num += 1
                tokens.append({'type': kind, 'value': value, 'line': line_num, 'start': start_pos, 'end': end_pos})
                continue
            elif kind in ['LEERZEICHEN', 'KOMMENTAR']:
                if kind == 'KOMMENTAR':
                     tokens.append({'type': kind, 'value': value, 'line': line_num, 'start': start_pos, 'end': end_pos})
                continue
            elif kind == 'UNBEKANNT':
                raise RuntimeError(f'Lexer Fehler Zeile {line_num}: Unbekanntes Zeichen "{value}"')
            
            if kind.startswith('KW_') or kind.startswith('CONST_') or kind.startswith('FUNC_'):
                tokens.append({
                    'type': 'KEYWORD', 
                    'value': kind,
                    'original': value,
                    'line': line_num,
                    'start': start_pos,
                    'end': end_pos
                })
            else:
                tokens.append({'type': kind, 'value': value, 'line': line_num, 'start': start_pos, 'end': end_pos})
                
        tokens.append({'type': 'EOF', 'line': line_num, 'value': '', 'start': len(code), 'end': len(code)})
        return tokens

# WICHTIG: Auch die Wrapper-Funktion muss das neue Argument annehmen
def tokenize(code, config, start_line=1):
    return Lexer(config).tokenize(code, start_line)