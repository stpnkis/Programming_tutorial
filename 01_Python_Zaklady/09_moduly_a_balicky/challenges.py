#!/usr/bin/env python3
"""
🐍 PYTHON ZÁKLADY — Moduly a balíčky
Organizace kódu do modulů — profesionální struktura projektu.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def vyzva_1():
    """
    🎯 Importuj modul 'math' a vrať:
    - pi (math.pi)
    - odmocninu ze 144 (math.sqrt)
    - logaritmus 100 o základu 10 (math.log10)
    Vrať jako tuple (pi, sqrt, log).
    """
    # TODO: import a použití ↓
    pass

def vyzva_2():
    """
    🎯 Z modulu 'collections' importuj POUZE Counter.
    Spočítej písmena v "abrakadabra" a vrať 3 nejčastější
    jako list tuplů: [("a", 5), ("b", 2), ("r", 2)]
    """
    # TODO: from ... import ... ↓
    pass

def vyzva_3():
    """
    🎯 Importuj modul 'datetime' a vrať:
    - dnešní datum jako string ve formátu "YYYY-MM-DD"
    """
    # TODO: ↓
    pass

def vyzva_4():
    """
    🎯 Importuj modul 'os' a 'os.path'. Vrať:
    - aktuální pracovní adresář (os.getcwd())
    - Existuje soubor '/etc/hostname'? (True/False)
    - Absolutní cesta k tomuto souboru (__file__)
    Vrať jako tuple.
    """
    # TODO: ↓
    pass

def vyzva_5():
    """
    🎯 Importuj 'random' s aliasem 'rnd'.
    Nastav seed na 42 (rnd.seed(42)).
    Vygeneruj 5 náhodných celých čísel 1-100 (rnd.randint).
    Vrať je jako list.
    """
    # TODO: import ... as ... ↓
    pass

def vyzva_6():
    """
    🎯 Zjisti jaké atributy/funkce má modul 'string'.
    Vrať seznam názvů, které začínají velkým písmenem.
    Hint: dir(modul) vrátí seznam atributů.
    """
    # TODO: ↓
    pass

# ============================================================
# 🔍 TESTY
# ============================================================
import math
from datetime import date

challenges = [
    Challenge(
        title="Import celého modulu",
        theory="""Import modulu:
  import math           # celý modul
  math.sqrt(16)         # přes tečkovou notaci

  from math import sqrt # jen konkrétní věc
  sqrt(16)              # přímo

  import numpy as np    # s aliasem
  np.array([1,2])""",
        task="Importuj math a vrať pi, sqrt(144), log10(100).",
        difficulty=1, points=10,
        hints=["import math; return (math.pi, math.sqrt(144), math.log10(100))"],
        tests=[
            lambda: verify(
                vyzva_1() == (math.pi, 12.0, 2.0),
                "Math import ✓"
            ),
        ]
    ),
    Challenge(
        title="From ... import — Counter",
        theory="""Counter je speciální slovník pro počítání:
  from collections import Counter
  c = Counter("abracadabra")
  c.most_common(3)  → [('a', 5), ('b', 2), ('r', 2)]""",
        task="Spočítej 3 nejčastější písmena v 'abrakadabra'.",
        difficulty=2, points=15,
        hints=["from collections import Counter", "Counter('abrakadabra').most_common(3)"],
        tests=[
            lambda: verify(
                vyzva_2() == [("a", 5), ("b", 2), ("r", 2)],
                "Counter ✓",
                f"Dostal: {vyzva_2()}"
            ),
        ]
    ),
    Challenge(
        title="Datum — datetime modul",
        task="Vrať dnešní datum ve formátu YYYY-MM-DD.",
        difficulty=1, points=10,
        hints=["from datetime import date; return date.today().isoformat()"],
        tests=[
            lambda: verify(
                vyzva_3() == date.today().isoformat(),
                "Datum ✓"
            ),
        ]
    ),
    Challenge(
        title="OS modul — systémové operace",
        theory="""os modul pro práci se systémem:
  os.getcwd()                # aktuální adresář
  os.path.exists(cesta)      # existuje soubor?
  os.path.abspath(__file__)  # absolutní cesta""",
        task="Vrať info o systému pomocí os modulu.",
        difficulty=2, points=15,
        hints=["os.getcwd(), os.path.exists('/etc/hostname'), os.path.abspath(__file__)"],
        tests=[
            lambda: verify(
                isinstance(vyzva_4(), tuple) and len(vyzva_4()) == 3,
                "OS info ✓",
                "Vrať tuple se 3 prvky"
            ),
        ]
    ),
    Challenge(
        title="Import s aliasem — random",
        theory="""Alias zkracuje název:
  import numpy as np
  import pandas as pd
  import matplotlib.pyplot as plt

Seed zajistí reprodukovatelnost náhodných čísel.""",
        task="Generuj 5 náhodných čísel 1-100 se seedem 42.",
        difficulty=1, points=10,
        hints=["import random as rnd; rnd.seed(42); return [rnd.randint(1,100) for _ in range(5)]"],
        tests=[
            lambda: (
                lambda: verify(vyzva_5() == vyzva_5(), "Se seedem jsou výsledky reprodukovatelné ✓")
            )(),
            lambda: verify(
                len(vyzva_5()) == 5 and all(1 <= x <= 100 for x in vyzva_5()),
                "5 čísel v rozsahu 1-100 ✓"
            ),
        ]
    ),
    Challenge(
        title="Introspekce — dir()",
        theory="""dir(objekt) ukáže vše co objekt nabízí:
  dir(str)    → všechny metody stringu
  dir(math)   → všechny funkce math modulu

Mocný nástroj pro prozkoumání neznámých modulů!""",
        task="Najdi atributy modulu 'string' začínající velkým písmenem.",
        difficulty=2, points=15,
        hints=["import string; [x for x in dir(string) if x[0].isupper()]"],
        tests=[
            lambda: verify(
                isinstance(vyzva_6(), list) and len(vyzva_6()) > 0,
                f"Nalezeno {len(vyzva_6())} atributů ✓"
            ),
            lambda: verify(
                "Formatter" in vyzva_6(),
                "Obsahuje 'Formatter' ✓",
                f"Dostal: {vyzva_6()}"
            ),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Python Základy — Moduly a balíčky", "01_09")
