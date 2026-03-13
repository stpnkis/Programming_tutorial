#!/usr/bin/env python3
"""📖 Čtení kódu — Rozumění cizím projektům."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 PŘEČTI KÓD A ODPOVĚZ
# ============================================================

# 🎯 VÝZVA 1: Co dělá tato funkce?
def mystery_1(data):
    result = {}
    for item in data:
        key = item[0]
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result

def co_dela_mystery_1() -> str:
    """Popiš jednou větou co dělá mystery_1."""
    return ""  # TODO: ↓

def mystery_1_result():
    """Co vrátí mystery_1(["ahoj", "auto", "bok", "brno", "ahoj"])?"""
    return {}  # TODO: ↓ vrať očekávaný výsledek

# 🎯 VÝZVA 2: Najdi bug
def buggy_average(cisla):
    """Tato funkce MÁ BUG. Najdi ho."""
    total = 0
    for c in cisla:
        total += c
    return total / len(cisla)  # Bug: co když cisla je prázdný?

def opraveny_average(cisla: list) -> float:
    """
    🎯 Oprav bug — prázdný seznam by měl vrátit 0.0.
    """
    # TODO: ↓
    pass

# 🎯 VÝZVA 3: Trasování kódu — projdi ručně
def trace_me(n):
    result = 1
    for i in range(1, n + 1):
        if i % 2 == 0:
            result *= i
        else:
            result += i
    return result

def trace_vysledek() -> int:
    """Co vrátí trace_me(5)? Projdi ručně krok po kroku."""
    return 0  # TODO: ↓

# 🎯 VÝZVA 4: Porozumění třídě
class Node:
    def __init__(self, v, l=None, r=None):
        self.v = v; self.l = l; self.r = r

def mystery_tree(n):
    if not n: return 0
    return max(mystery_tree(n.l), mystery_tree(n.r)) + 1

def co_pocita_mystery_tree() -> str:
    """Co počítá mystery_tree?"""
    return ""  # TODO: ↓

def mystery_tree_result():
    """Co vrátí mystery_tree(Node(1, Node(2, Node(4)), Node(3)))?"""
    return 0  # TODO: ↓


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Co dělá tato funkce?",
        theory="""ČTENÍ KÓDU — nejdůležitější skill!

Postup:
1. Přečti názvy (funkce, proměnné)
2. Identifikuj INPUT a OUTPUT
3. Projdi logiku krok po kroku
4. Zakresli si příklad
5. Shrň jednou větou

Čteš MNOHEM více kódu než píšeš.
Schopnost rychle pochopit cizí kód = superschopnost.""",
        task="Popiš mystery_1 a predikuj výstup.",
        difficulty=1, points=20,
        hints=["Seskupuje prvky podle prvního znaku", "result je dict se skupinami"],
        tests=[
            lambda: verify(
                "skupin" in co_dela_mystery_1().lower() or "group" in co_dela_mystery_1().lower()
                or "seskup" in co_dela_mystery_1().lower() or "prvn" in co_dela_mystery_1().lower(),
                "Popis ✓"
            ),
            lambda: verify(
                mystery_1_result() == mystery_1(["ahoj", "auto", "bok", "brno", "ahoj"]),
                "Predikce výstupu ✓"
            ),
        ]
    ),
    Challenge(
        title="Najdi a oprav bug",
        task="buggy_average padá na prázdném seznamu!",
        difficulty=1, points=15,
        hints=["if not cisla: return 0.0"],
        tests=[
            lambda: verify(opraveny_average([1, 2, 3]) == 2.0, "Normální ✓"),
            lambda: verify(opraveny_average([]) == 0.0, "Prázdný ✓"),
            lambda: verify(opraveny_average([10]) == 10.0, "Jeden prvek ✓"),
        ]
    ),
    Challenge(
        title="Trasování kódu ručně",
        theory="""TRASOVÁNÍ = projdi kód jako počítač:

trace_me(5):
  result = 1
  i=1 (lichý): result = 1 + 1 = 2
  i=2 (sudý):  result = 2 * 2 = 4
  i=3 (lichý): result = 4 + 3 = 7
  i=4 (sudý):  result = 7 * 4 = 28
  i=5 (lichý): result = 28 + 5 = 33

Piš si na papír! Nejlepší debugovací technika.""",
        task="Projdi trace_me(5) krok po kroku.",
        difficulty=2, points=20,
        hints=["i=1:+1, i=2:*2, i=3:+3, i=4:*4, i=5:+5"],
        tests=[
            lambda: verify(trace_vysledek() == trace_me(5), f"Trace = {trace_me(5)} ✓"),
        ]
    ),
    Challenge(
        title="Porozumění rekurzivní funkci",
        task="Co počítá mystery_tree? Jaký výsledek?",
        difficulty=2, points=20,
        hints=["Node se dvěma potomky, rekurze max + 1...", "Výška stromu!"],
        tests=[
            lambda: verify(
                "výšk" in co_pocita_mystery_tree().lower() or
                "hloub" in co_pocita_mystery_tree().lower() or
                "depth" in co_pocita_mystery_tree().lower() or
                "height" in co_pocita_mystery_tree().lower(),
                "Funkce popsána ✓"
            ),
            lambda: verify(
                mystery_tree_result() == mystery_tree(Node(1, Node(2, Node(4)), Node(3))),
                f"Výsledek = {mystery_tree(Node(1, Node(2, Node(4)), Node(3)))} ✓"
            ),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Čtení Cizích Projektů", "06_01")
