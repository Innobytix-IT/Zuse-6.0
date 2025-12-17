# FILE: translate.py
from lexer import tokenize
from language_loader import lade_sprache

def uebersetze_code(code, von_sprache, zu_sprache):
    if not code.strip(): return ""
    src_config = lade_sprache(von_sprache)
    target_config = lade_sprache(zu_sprache)

    mapping = {}
    for key, val in target_config.items():
        mapping[key] = val

    try:
        tokens = tokenize(code, src_config)
    except:
        return code

    tokens_to_translate = [t for t in tokens if t['type'] == 'KEYWORD']
    tokens_to_translate.sort(key=lambda x: x['start'], reverse=True)
    
    result_code = code
    for t in tokens_to_translate:
        canonical_key = t['value']
        if canonical_key in mapping:
            neues_wort = mapping[canonical_key]
            result_code = result_code[:t['start']] + neues_wort + result_code[t['end']:]
            
    return result_code