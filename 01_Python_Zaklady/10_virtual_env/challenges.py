#!/usr/bin/env python3
"""
🐍 PYTHON ZÁKLADY — Virtual Environment
Izolace projektu — každý projekt své závislosti.
Tento soubor je víc přehled + kvíz (ne kód k doplnění).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 KVÍZOVÉ OTÁZKY — vrať správnou odpověď
# ============================================================

def vyzva_1():
    """
    🎯 Jaký příkaz vytvoří nový virtual environment v složce 'venv'?
    Vrať správný příkaz jako string.
    a) "pip install venv"
    b) "python3 -m venv venv"
    c) "virtualenv create venv"
    d) "conda create venv"
    """
    # TODO: Vrať string s příkazem ↓
    return ...

def vyzva_2():
    """
    🎯 Jak aktivuješ virtual environment na Linuxu?
    Vrať správný příkaz jako string.
    a) "venv/activate"
    b) "source venv/bin/activate"
    c) "activate venv"
    d) "python activate venv"
    """
    # TODO: ↓
    return ...

def vyzva_3():
    """
    🎯 Jak uložíš závislosti projektu do souboru?
    Vrať správný příkaz jako string.
    """
    # TODO: ↓
    return ...

def vyzva_4():
    """
    🎯 Jak nainstaluješ závislosti ze souboru requirements.txt?
    Vrať správný příkaz jako string.
    """
    # TODO: ↓
    return ...

def vyzva_5():
    """
    🎯 Vrať True/False:
    Měl bys commitovat složku venv/ do Gitu?
    """
    # TODO: ↓
    return ...

# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Vytvoření virtual environment",
        theory="""Virtual environment izoluje závislosti projektu:
  - Projekt A potřebuje numpy 1.24
  - Projekt B potřebuje numpy 1.21
  - Bez venv by se praly → s venv má každý svoje.

Vytvoření: python3 -m venv nazev_slozky""",
        task="Jaký příkaz vytvoří venv?",
        difficulty=1, points=10,
        hints=["python3 -m venv ..."],
        tests=[
            lambda: verify(vyzva_1() == "python3 -m venv venv", "Správně! ✓"),
        ]
    ),
    Challenge(
        title="Aktivace venv",
        theory="""Aktivace na různých OS:
  Linux/Mac:   source venv/bin/activate
  Windows:     venv\\Scripts\\activate

Po aktivaci uvidíš (venv) v promptu.""",
        task="Jak aktivuješ venv na Linuxu?",
        difficulty=1, points=10,
        hints=["source ..."],
        tests=[
            lambda: verify(vyzva_2() == "source venv/bin/activate", "Správně! ✓"),
        ]
    ),
    Challenge(
        title="Uložení závislostí",
        theory="""pip freeze vypíše nainstalované balíčky:
  pip freeze > requirements.txt

Tento soubor pak můžeš sdílet s ostatními.""",
        task="Jak uložíš závislosti?",
        difficulty=1, points=10,
        hints=["pip freeze > ..."],
        tests=[
            lambda: verify(vyzva_3() == "pip freeze > requirements.txt", "Správně! ✓"),
        ]
    ),
    Challenge(
        title="Instalace ze souboru",
        theory="""pip install -r načte závislosti ze souboru:
  pip install -r requirements.txt""",
        task="Jak instaluješ z requirements.txt?",
        difficulty=1, points=10,
        hints=["pip install -r ..."],
        tests=[
            lambda: verify(vyzva_4() == "pip install -r requirements.txt", "Správně! ✓"),
        ]
    ),
    Challenge(
        title="Git a venv",
        theory="""venv/ složka obsahuje tisíce souborů a závisí na OS.
NIKDY ji necommituj do Gitu!
Místo toho commituj requirements.txt.

V .gitignore přidej:
  venv/
  __pycache__/""",
        task="Commitovat venv/ do Gitu?",
        difficulty=1, points=10,
        hints=["Ne! Commituj jen requirements.txt"],
        tests=[
            lambda: verify(vyzva_5() == False, "Správně — venv se necommituje! ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Python Základy — Virtual Environment", "01_10")
