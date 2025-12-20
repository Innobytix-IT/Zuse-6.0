# FILE: language_loader.py
import json
import os
import sys

def get_base_dir():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
LANG_DIR = os.path.join(BASE_DIR, "sprachen")

def lade_sprache(sprach_code):
    pfad_deutsch = os.path.join(LANG_DIR, "deutsch.json")
    # Fallback Pfad Check
    if not os.path.exists(pfad_deutsch):
         pfad_deutsch = os.path.join(os.getcwd(), "sprachen", "deutsch.json")

    if not os.path.exists(pfad_deutsch):
        # Notfall-Config falls Dateien fehlen
        return {}

    with open(pfad_deutsch, "r", encoding="utf-8") as f:
        konfiguration = json.load(f)

    if sprach_code == "deutsch":
        return konfiguration

    pfad_ziel = os.path.join(LANG_DIR, f"{sprach_code}.json")
    if not os.path.exists(pfad_ziel):
        pfad_ziel = os.path.join(os.getcwd(), "sprachen", f"{sprach_code}.json")

    if os.path.exists(pfad_ziel):
        with open(pfad_ziel, "r", encoding="utf-8") as f:
            ziel_config = json.load(f)
            konfiguration.update(ziel_config)
    
    return konfiguration