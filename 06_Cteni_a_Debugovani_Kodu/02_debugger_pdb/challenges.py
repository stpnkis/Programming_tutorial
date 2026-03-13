#!/usr/bin/env python3
"""🔬 Debugger — pdb a breakpoints."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

# 🎯 VÝZVA 1: Debugovací příkazy
def pdb_prikazy() -> dict:
    """Vyplň co dělá každý pdb příkaz."""
    return {
        "n": "",     # TODO: ↓ next
        "s": "",     # TODO: ↓ step
        "c": "",     # TODO: ↓ continue
        "p": "",     # TODO: ↓ print
        "l": "",     # TODO: ↓ list
        "q": "",     # TODO: ↓ quit
        "b": "",     # TODO: ↓ breakpoint
        "w": "",     # TODO: ↓ where
    }

# 🎯 VÝZVA 2: Oprav buggy kód pomocí "mentálního debuggeru"
def buggy_flatten(lst):
    """BUGGY verze — nečti, rovnou píš svou opravu níže."""
    result = []
    for item in lst:
        if type(item) == list:
            result.append(buggy_flatten(item))  # bug: append vs extend
    else:
        result.append(item)  # bug: indentace
    return result

def opraveny_flatten(lst: list) -> list:
    """
    🎯 Napiš SPRÁVNÝ flatten.
    [1, [2, [3]], 4] → [1, 2, 3, 4]
    """
    # TODO: ↓
    pass

# 🎯 VÝZVA 3: Kde je chyba?
def buggy_binary_search(lst, target):
    """BUGGY bin. search — najdi 2 bugy."""
    low = 0
    high = len(lst)  # Bug 1: mělo být len(lst) - 1
    while low < high:  # Bug 2: mělo být low <= high
        mid = (low + high) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def opraveny_binary_search(lst: list, target) -> int:
    """
    🎯 Oprav binární hledání (2 bugy).
    """
    # TODO: ↓
    pass

# 🎯 VÝZVA 4: Breakpoint strategie
def kde_dat_breakpoint() -> dict:
    """
    Pro každý typ bugu, kde umístíš breakpoint?
    """
    return {
        "nesprávný_výstup": "",    # TODO: ↓ kam dám breakpoint?
        "nekonečná_smyčka": "",    # TODO: ↓
        "indexerror": "",          # TODO: ↓
        "wrong_logic": "",        # TODO: ↓
    }


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="PDB příkazy",
        theory="""PDB — Python debugger. Spustíš:
  python3 -m pdb skript.py
  # nebo v kódu:
  breakpoint()  # od Python 3.7

PŘÍKAZY:
  n (next)      — další řádek (NEjdi do funkce)
  s (step)      — další krok (VEJDI do funkce)
  c (continue)  — pokračuj do dalšího breakpointu
  p expr        — vytiskni výraz
  pp expr       — pretty-print
  l (list)      — ukaž kód kolem
  b N           — nastav breakpoint na řádek N
  w (where)     — ukaž call stack
  q (quit)      — ukonči debugger

TIP: breakpoint() přímo v kódu je nejrychlejší!""",
        task="Popiš co dělá každý pdb příkaz.",
        difficulty=1, points=15,
        hints=["n=next line, s=step into, c=continue, p=print"],
        tests=[
            lambda: (
                lambda p: verify(
                    all(len(p[k]) > 2 for k in p),
                    f"Příkazy popsány ✓ ({len(p)} příkazů)"
                )
            )(pdb_prikazy()),
        ]
    ),
    Challenge(
        title="Oprav flatten (append vs extend)",
        theory="""ČASTÝ BUG: append vs extend
  lst.append([1,2])  → [... , [1,2]]  # vnořený list!
  lst.extend([1,2])  → [... , 1, 2]   # zploštěný

A pozor na INDENTACI — Python for...else je záludný:
  for x in lst:
      ...
  else:        # toto se spustí po NORMÁLNÍM konci cyklu!
      ...""",
        task="Oprav flatten — extend místo append + správná indentace.",
        difficulty=2, points=25,
        hints=["isinstance(item, list): result.extend(opraveny_flatten(item)); else: result.append(item)"],
        tests=[
            lambda: verify(opraveny_flatten([1, [2, [3]], 4]) == [1, 2, 3, 4], "Vnořený ✓"),
            lambda: verify(opraveny_flatten([]) == [], "Prázdný ✓"),
            lambda: verify(opraveny_flatten([1, 2, 3]) == [1, 2, 3], "Plochý ✓"),
        ]
    ),
    Challenge(
        title="Oprav binární hledání (2 bugy)",
        theory="""MENTÁLNÍ DEBUGGER — projdi kód jako počítač:
Bug 1: high = len(lst) → IndexError! Mělo být len(lst)-1
Bug 2: while low < high → nezkontroluje mid==target
        u low == high. Mělo být low <= high.""",
        task="Najdi a oprav oba bugy v binárním hledání.",
        difficulty=2, points=25,
        hints=["high = len(lst) - 1; while low <= high"],
        tests=[
            lambda: verify(opraveny_binary_search([1, 3, 5, 7, 9], 7) == 3, "Nalezeno ✓"),
            lambda: verify(opraveny_binary_search([1, 3, 5, 7, 9], 1) == 0, "První ✓"),
            lambda: verify(opraveny_binary_search([1, 3, 5, 7, 9], 9) == 4, "Poslední ✓"),
            lambda: verify(opraveny_binary_search([1, 3, 5, 7, 9], 4) == -1, "Nenalezeno ✓"),
        ]
    ),
    Challenge(
        title="Kde umístit breakpoint?",
        task="Strategie pro umístění breakpointů.",
        difficulty=1, points=10,
        hints=["Nesprávný výstup: těsně před return; Smyčka: uvnitř smyčky"],
        tests=[
            lambda: (
                lambda d: verify(
                    all(len(d[k]) > 5 for k in d),
                    "Strategie vyplněny ✓"
                )
            )(kde_dat_breakpoint()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Debugger — pdb", "06_02")
