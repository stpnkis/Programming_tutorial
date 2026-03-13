#!/usr/bin/env python3
"""
🐍 PYTHON ZÁKLADY — List & Dict Comprehensions
Elegantní a pythonovský způsob tvorby kolekcí.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def vyzva_1():
    """🎯 Vytvoř list druhých mocnin čísel 1-10: [1, 4, 9, 16, ..., 100]"""
    # TODO: Použij list comprehension ↓
    return ...

def vyzva_2():
    """🎯 Vytvoř list sudých čísel od 2 do 20: [2, 4, 6, ..., 20]"""
    # TODO: List comprehension s podmínkou ↓
    return ...

def vyzva_3(slova):
    """
    🎯 Převeď seznam slov na velká písmena, ale jen ta delší než 3 znaky.
    Příklad: ["ah", "python", "je", "super"] → ["PYTHON", "SUPER"]
    """
    # TODO: ↓
    return ...

def vyzva_4(matice):
    """
    🎯 Zploštění matice (flatten): [[1,2],[3,4],[5,6]] → [1,2,3,4,5,6]
    Použij vnořenou comprehension.
    """
    # TODO: ↓
    return ...

def vyzva_5(studenti):
    """
    🎯 Dict comprehension: Ze seznamu tuplů vytvoř slovník.
    Vstup: [("Jan", 90), ("Eva", 85), ("Petr", 70)]
    Výstup: {"Jan": 90, "Eva": 85, "Petr": 70}
    """
    # TODO: ↓
    return ...

def vyzva_6(text):
    """
    🎯 Spočítej frekvenci písmen v textu (ignoruj mezery, malá písmena).
    Příklad: "Ahoj Aho" → {"a": 2, "h": 2, "o": 2, "j": 1}
    Vrať dict seřazený abecedně (dict comprehension + sorted).
    """
    # TODO: ↓
    return ...

def vyzva_7():
    """
    🎯 Generator expression: Vytvoř generátor, který produkuje
    Fibonacciho čísla menší než 100.
    HINT: Nemusíš použít comprehension — stačí generátorová funkce (yield).
    Vrať seznam těch čísel.
    """
    # TODO: ↓
    return ...

# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="List comprehension — druhé mocniny",
        theory="""List comprehension je zkrácený zápis:
  [výraz for proměnná in sekvence]

Příklad:
  [x**2 for x in range(5)]  → [0, 1, 4, 9, 16]

Nahrazuje:
  result = []
  for x in range(5):
      result.append(x**2)""",
        task="Vytvoř list [1, 4, 9, ..., 100].",
        difficulty=1, points=10,
        hints=["[x**2 for x in range(1, 11)]"],
        tests=[lambda: verify(vyzva_1() == [i**2 for i in range(1,11)], "Druhé mocniny ✓")]
    ),
    Challenge(
        title="Comprehension s podmínkou",
        theory="""Podmínka v comprehension:
  [výraz for x in sekvence if podmínka]

  [x for x in range(20) if x % 2 == 0]  → sudá čísla""",
        task="List sudých čísel od 2 do 20.",
        difficulty=1, points=10,
        hints=["[x for x in range(2, 21) if x % 2 == 0]", "Nebo: list(range(2, 21, 2))"],
        tests=[lambda: verify(vyzva_2() == list(range(2, 21, 2)), "Sudá čísla ✓")]
    ),
    Challenge(
        title="Filtrování a transformace",
        task="Velká písmena jen pro slova delší než 3 znaky.",
        difficulty=2, points=15,
        hints=["[s.upper() for s in slova if len(s) > 3]"],
        tests=[
            lambda: verify(vyzva_3(["ah","python","je","super"]) == ["PYTHON","SUPER"], "Filtrace ✓"),
            lambda: verify(vyzva_3(["a","bb","ccc","dddd"]) == ["DDDD"], "Délka > 3 ✓"),
        ]
    ),
    Challenge(
        title="Vnořená comprehension — flatten",
        theory="""Vnořená comprehension:
  [prvek for radek in matice for prvek in radek]
Pořadí: vnější cyklus PRVNÍ, vnitřní DRUHÝ.""",
        task="Zploštění 2D listu na 1D.",
        difficulty=2, points=15,
        hints=["[x for row in matice for x in row]"],
        tests=[
            lambda: verify(vyzva_4([[1,2],[3,4],[5,6]]) == [1,2,3,4,5,6], "Flatten ✓"),
            lambda: verify(vyzva_4([[1],[2],[3]]) == [1,2,3], "Jednoduché ✓"),
        ]
    ),
    Challenge(
        title="Dict comprehension",
        theory="""Dict comprehension:
  {klic: hodnota for prvek in sekvence}

  {x: x**2 for x in range(5)}  → {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}""",
        task="Ze seznamu tuplů vytvoř slovník.",
        difficulty=1, points=10,
        hints=["{jmeno: znamka for jmeno, znamka in studenti}"],
        tests=[
            lambda: verify(
                vyzva_5([("Jan",90),("Eva",85)]) == {"Jan": 90, "Eva": 85}, "Dict ✓"
            )
        ]
    ),
    Challenge(
        title="Frekvence písmen",
        task="Spočítej kolikrát se které písmeno vyskytuje.",
        difficulty=2, points=20,
        hints=[
            "Nejdřív text.lower().replace(' ', '')",
            "Použij Counter z collections nebo dict comprehension",
        ],
        tests=[
            lambda: verify(
                vyzva_6("Ahoj Aho") == {"a": 2, "h": 2, "j": 1, "o": 2},
                "Frekvence ✓",
                f"Dostal {vyzva_6('Ahoj Aho')}"
            )
        ]
    ),
    Challenge(
        title="Generátory — Fibonacci",
        theory="""Generátor produkuje hodnoty líně (lazy):
  def gen():
      yield 1
      yield 2

Nebo generator expression:
  (x**2 for x in range(10))

Generátory šetří paměť — negenerují vše najednou.""",
        task="Vrať seznam Fibonacciho čísel menších než 100.",
        difficulty=3, points=25,
        hints=[
            "Fibonacci: a, b = 0, 1; poté a, b = b, a+b",
            "Použij while a yield, pak list(generator())"
        ],
        tests=[
            lambda: verify(
                vyzva_7() == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89],
                "Fibonacci ✓",
                f"Dostal {vyzva_7()}"
            )
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Python Základy — Comprehensions & Generátory", "01_05")
