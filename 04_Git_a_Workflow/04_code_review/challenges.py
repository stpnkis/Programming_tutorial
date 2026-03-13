#!/usr/bin/env python3
"""👀 Code Review — Umění číst a hodnotit kód."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

# 🎯 VÝZVA 1: Najdi problém v kódu
def review_1_problem() -> str:
    """
    def get_user(id):
        import sqlite3
        conn = sqlite3.connect("db.sqlite")
        result = conn.execute(f"SELECT * FROM users WHERE id = {id}")
        return result.fetchone()
    
    Jaký je HLAVNÍ bezpečnostní problém? (jedno slovo/fráze)
    """
    return ""  # TODO: ↓

def review_1_fix() -> str:
    """Jak bys to opravil? (stručný SQL příkaz)"""
    return ""  # TODO: ↓

# 🎯 VÝZVA 2: Refaktoring
def spatny_kod_oprava(data: list) -> dict:
    """
    ŠPATNÝ KÓD (nereferuj — napiš SPRÁVNOU verzi):
    
    def process(d):
        r = {}
        for i in range(len(d)):
            x = d[i]
            if x > 0:
                if x in r:
                    r[x] = r[x] + 1
                else:
                    r[x] = 1
        return r
    
    🎯 Přepiš čistě: počítej frekvence KLADNÝCH čísel.
    Použij lepší názvy, Pythonic styl.
    """
    # TODO: ↓
    pass

# 🎯 VÝZVA 3: Code review checklist
def review_checklist() -> list:
    """
    Vrať seznam alespoň 5 věcí, na co se dívat při code review.
    Např: ["Čitelnost kódu", "Testy", ...]
    """
    return []  # TODO: ↓

# 🎯 VÝZVA 4: Pojmenování
def lepsi_nazev(spatny: str) -> str:
    """
    Přepiš špatný název na dobrý:
    "d" → "data" nebo "user_data"
    "x" → závisí na kontextu
    "proc" → "process_payment" (spec.)
    "tmp2" → konkrétní účel
    """
    nazvoslovi = {
        "d": "",      # TODO: ↓
        "x": "",      # TODO: ↓  
        "proc": "",   # TODO: ↓
        "calc": "",   # TODO: ↓
        "mgr": "",    # TODO: ↓
    }
    return nazvoslovi.get(spatny, spatny)


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Najdi bezpečnostní problém",
        theory="""CODE REVIEW = systematická kontrola kódu.

Hlavní oblasti:
1. 🔒 BEZPEČNOST — SQL injection, XSS, secrety
2. 📖 ČITELNOST — názvy, struktura, komentáře
3. ⚡ VÝKON — zbytečné operace, N+1, paměť
4. 🧪 TESTY — pokrytí, edge cases
5. 🏗️ ARCHITEKTURA — SRP, coupling, abstractions

SQL INJECTION — NIKDY nepoužívej f-stringy v SQL!
  ŠPATNĚ:  f"SELECT * FROM users WHERE id = {id}"
  SPRÁVNĚ: cursor.execute("SELECT ... WHERE id = ?", (id,))""",
        task="Identifikuj SQL injection a navrhni opravu.",
        difficulty=1, points=15,
        hints=["f-string v SQL = SQL injection", "Použij parametrizovaný dotaz s ?"],
        tests=[
            lambda: verify(
                "injection" in review_1_problem().lower() or "sql" in review_1_problem().lower(),
                "Problém identifikován ✓"
            ),
            lambda: verify("?" in review_1_fix(), "Parametrizovaný dotaz ✓"),
        ]
    ),
    Challenge(
        title="Refaktoruj špatný kód",
        theory="""ČISTÝ KÓD:
1. Pojmenuj věci smysluplně (ne x, d, r)
2. Používej Pythonic idiomy (Counter, comprehensions)
3. Jedna funkce = jedna zodpovědnost
4. DRY — neopakuj se""",
        task="Přepiš frekvenci kladných čísel čistě.",
        difficulty=2, points=25,
        hints=["from collections import Counter; Counter(x for x in data if x > 0)"],
        tests=[
            lambda: verify(
                spatny_kod_oprava([1, -2, 3, 1, 3, 3]) == {1: 2, 3: 3},
                "Frekvence kladných ✓"
            ),
            lambda: verify(spatny_kod_oprava([-1, -2]) == {}, "Žádné kladné ✓"),
            lambda: verify(spatny_kod_oprava([]) == {}, "Prázdný ✓"),
        ]
    ),
    Challenge(
        title="Code Review checklist",
        task="Sepiš minimálně 5 bodů pro code review.",
        difficulty=1, points=10,
        hints=["Čitelnost, testy, bezpečnost, výkon, dokumentace, error handling"],
        tests=[
            lambda: verify(
                len(review_checklist()) >= 5 and all(len(i) > 3 for i in review_checklist()),
                f"Checklist s {len(review_checklist())} body ✓"
            ),
        ]
    ),
    Challenge(
        title="Lepší pojmenování",
        theory="""POJMENOVÁNÍ — nejdůležitější skill!

  ŠPATNĚ:     DOBŘE:
  d           user_data
  x           temperature
  proc        process_payment
  calc        calculate_total
  mgr         connection_manager
  n           item_count
  tmp         intermediate_result""",
        task="Přepiš kryptické názvy na srozumitelné.",
        difficulty=1, points=15,
        hints=["d→data/user_data, proc→process_…, mgr→…_manager"],
        tests=[
            lambda: verify(
                len(lepsi_nazev("d")) >= 4 and
                len(lepsi_nazev("proc")) >= 7 and
                len(lepsi_nazev("mgr")) >= 7,
                "Lepší názvy ✓",
                f"d→{lepsi_nazev('d')}, proc→{lepsi_nazev('proc')}, mgr→{lepsi_nazev('mgr')}"
            ),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Code Review", "04_04")
