#!/usr/bin/env python3
"""
🐍 PYTHON ZÁKLADY — Slovníky a množiny
Nejdůležitější datové struktury po listu.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def vyzva_1():
    """
    🎯 Vytvoř slovník 'osoba' s klíči: jmeno, vek, mesto
    Hodnoty: "Jan", 25, "Praha"
    Pak přidej klíč 'email' s hodnotou "jan@email.cz"
    Vrať celý slovník.
    """
    # TODO: ↓
    osoba = ...
    # Přidej email
    return osoba

def vyzva_2(slovnik, klic, default=None):
    """
    🎯 Bezpečně získej hodnotu ze slovníku.
    Pokud klíč neexistuje, vrať default.
    Nepoužívej try/except — existuje lepší metoda.
    """
    # TODO: ↓
    pass

def vyzva_3(seznam):
    """
    🎯 Ze seznamu slov vrať slovník {slovo: délka_slova}.
    Příklad: ["ahoj", "svět"] → {"ahoj": 4, "svět": 4}
    """
    # TODO: ↓
    return ...

def vyzva_4(text):
    """
    🎯 Spočítej frekvenci slov v textu. Ignoruj velikost písmen.
    Příklad: "to je to co je" → {"to": 2, "je": 2, "co": 1}
    Vrať slovník seřazený abecedně.
    """
    # TODO: ↓
    return ...

def vyzva_5(dict1, dict2):
    """
    🎯 Sloučení dvou slovníků: Pokud klíč existuje v obou,
    sečti hodnoty. Vrať nový slovník.
    Příklad: {"a": 1, "b": 2}, {"b": 3, "c": 4} → {"a": 1, "b": 5, "c": 4}
    """
    # TODO: ↓
    return ...

def vyzva_6(seznam1, seznam2):
    """
    🎯 Množinové operace: Vrať tuple (průnik, sjednocení, rozdíl).
    - průnik: prvky v obou
    - sjednocení: všechny unikátní prvky
    - rozdíl: prvky v seznam1, ale ne v seznam2
    Vše vrať jako seřazené seznamy.
    """
    # TODO: Použij set operace ↓
    return ..., ..., ...

def vyzva_7(data):
    """
    🎯 Invertuj slovník: klíče se stanou hodnotami a naopak.
    Příklad: {"a": 1, "b": 2} → {1: "a", 2: "b"}
    """
    # TODO: ↓
    return ...

# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Slovník — vytvoření a přidání",
        theory="""Slovník (dict) mapuje klíče na hodnoty:
  d = {"klic": "hodnota", "vek": 25}
  d["novy_klic"] = "nova_hodnota"   # přidání
  d["vek"]                          # přístup → 25""",
        task="Vytvoř slovník osoby a přidej email.",
        difficulty=1, points=10,
        hints=["osoba = {'jmeno': 'Jan', 'vek': 25, 'mesto': 'Praha'}"],
        tests=[
            lambda: verify(
                vyzva_1() == {"jmeno": "Jan", "vek": 25, "mesto": "Praha", "email": "jan@email.cz"},
                "Slovník ✓"
            ),
        ]
    ),
    Challenge(
        title="Bezpečný přístup — .get()",
        theory="""dict[klic] vyhodí KeyError pokud klíč neexistuje.
dict.get(klic, default) vrátí default místo chyby:
  d = {"a": 1}
  d.get("b", 0)  → 0 (místo KeyError)""",
        task="Použij .get() pro bezpečný přístup.",
        difficulty=1, points=10,
        hints=["return slovnik.get(klic, default)"],
        tests=[
            lambda: verify(vyzva_2({"a": 1}, "a") == 1, "Existující klíč ✓"),
            lambda: verify(vyzva_2({"a": 1}, "b", 0) == 0, "Neexistující s default ✓"),
            lambda: verify(vyzva_2({"a": 1}, "b") is None, "Neexistující bez default ✓"),
        ]
    ),
    Challenge(
        title="Seznam na slovník",
        task="Mapuj slova na jejich délky.",
        difficulty=1, points=10,
        hints=["{slovo: len(slovo) for slovo in seznam}"],
        tests=[
            lambda: verify(
                vyzva_3(["ahoj", "svět"]) == {"ahoj": 4, "svět": 4},
                "Mapování ✓"
            ),
        ]
    ),
    Challenge(
        title="Frekvence slov",
        task="Spočítej výskyty slov v textu.",
        difficulty=2, points=20,
        hints=[
            "slova = text.lower().split()",
            "Použij dict.get(slovo, 0) + 1 nebo Counter"
        ],
        tests=[
            lambda: verify(
                vyzva_4("to je to co je") == {"co": 1, "je": 2, "to": 2},
                "Frekvence ✓",
                f"Dostal: {vyzva_4('to je to co je')}"
            ),
        ]
    ),
    Challenge(
        title="Sloučení slovníků se sčítáním",
        theory="""Sloučení slovníků v Python 3.9+:
  d1 | d2  — nový slovník (d2 přepíše d1)
Ale my chceme SEČÍST hodnoty — to musíš ručně.""",
        task="Slouč dva slovníky, při kolizi sečti hodnoty.",
        difficulty=2, points=20,
        hints=[
            "Zkopíruj dict1, pak projdi dict2",
            "result[k] = result.get(k, 0) + v"
        ],
        tests=[
            lambda: verify(
                vyzva_5({"a": 1, "b": 2}, {"b": 3, "c": 4}) == {"a": 1, "b": 5, "c": 4},
                "Sloučení ✓"
            ),
        ]
    ),
    Challenge(
        title="Množinové operace",
        theory="""Množina (set) nemá duplikáty:
  s1 = {1, 2, 3}
  s2 = {2, 3, 4}
  s1 & s2   → {2, 3}      průnik
  s1 | s2   → {1, 2, 3, 4} sjednocení
  s1 - s2   → {1}          rozdíl""",
        task="Vrať průnik, sjednocení a rozdíl dvou seznamů.",
        difficulty=2, points=15,
        hints=["Převeď na set(), pak & | - , pak sorted() zpět na list"],
        tests=[
            lambda: verify(
                vyzva_6([1,2,3,4], [3,4,5,6]) == ([3,4], [1,2,3,4,5,6], [1,2]),
                "Množinové operace ✓"
            ),
        ]
    ),
    Challenge(
        title="Invertování slovníku",
        task="Prohoď klíče a hodnoty.",
        difficulty=1, points=10,
        hints=["{v: k for k, v in data.items()}"],
        tests=[
            lambda: verify(
                vyzva_7({"a": 1, "b": 2}) == {1: "a", 2: "b"},
                "Inverze ✓"
            ),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Python Základy — Slovníky a množiny", "01_06")
