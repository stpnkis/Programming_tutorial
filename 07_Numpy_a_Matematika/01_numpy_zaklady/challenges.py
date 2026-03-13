#!/usr/bin/env python3
"""🔢 NumPy — Základy: Vektorové operace."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("⚠️  NumPy není nainstalován! Spusť: pip install numpy")

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def vytvor_pole():
    """
    🎯 VÝZVA 1: Vytvoř NumPy pole.
    a) [1, 2, 3, 4, 5] → np.array
    b) matice 3x3 samé nuly
    c) vektor 10 jedniček
    d) range 0-9
    Vrať tuple (a, b, c, d).
    """
    # TODO: ↓
    pass


def operace_s_poli():
    """
    🎯 VÝZVA 2: Vektorové operace.
    a = [1, 2, 3, 4, 5]
    b = [10, 20, 30, 40, 50]
    Vrať tuple:
    - soucet: a + b elementwise
    - nasobek: a * 3
    - soucin: a * b elementwise
    - mocnina: a ** 2
    """
    # TODO: ↓
    pass


def indexovani_a_slicing():
    """
    🎯 VÝZVA 3: Indexování a slicing.
    mat = np.arange(1, 10).reshape(3, 3)
    → [[1,2,3],[4,5,6],[7,8,9]]
    Vrať tuple:
    - prvek [1,2] (= 6)
    - druhy_radek (= [4,5,6])
    - treti_sloupec (= [3,6,9])
    - podmatice 2x2 vlevo nahoře (= [[1,2],[4,5]])
    """
    # TODO: ↓
    pass


def boolean_indexing():
    """
    🎯 VÝZVA 4: Boolean indexing (filtrování).
    arr = np.array([3, 7, 2, 8, 1, 9, 4, 6])
    Vrať tuple:
    - vetsi_nez_5: prvky > 5
    - sude: sudé prvky
    - mezi_3_a_7: prvky >= 3 a <= 7
    """
    # TODO: ↓
    pass


def agregace():
    """
    🎯 VÝZVA 5: Agregační funkce.
    arr = np.array([4, 7, 2, 9, 1, 5, 8, 3, 6])
    Vrať dict:
    - sum, mean, std, min, max, argmin, argmax
    """
    # TODO: ↓
    pass

# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Vytváření NumPy polí",
        theory="""NUMPY = základ vědeckého Pythonu.

import numpy as np

np.array([1, 2, 3])        # z listu
np.zeros((3, 3))            # matice nul
np.ones(10)                 # vektor jedniček
np.arange(10)               # 0..9
np.linspace(0, 1, 5)        # 5 bodů mezi 0 a 1
np.random.randn(3, 3)       # náhodná 3x3

Proč NumPy?
- 100x rychlejší než Python listy
- Vektorové operace (bez for smyček!)
- Základ pro pandas, sklearn, pytorch""",
        task="Vytvoř 4 různá NumPy pole.",
        difficulty=1, points=15,
        hints=["np.array([1,2,3,4,5]), np.zeros((3,3)), np.ones(10), np.arange(10)"],
        tests=[
            lambda: verify(HAS_NUMPY, "NumPy nainstalován ✓") if not HAS_NUMPY else verify(True, "NumPy ✓"),
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 4,
                    "4 pole vytvořena ✓"
                )
            )(vytvor_pole()) if HAS_NUMPY else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Vektorové operace — BEZ for smyčky",
        theory="""VECTORIZED OPERATIONS — klíč k NumPy:

a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

a + b    → [11, 22, 33]    # elementwise
a * 3    → [3, 6, 9]       # broadcast
a * b    → [10, 40, 90]    # elementwise
a ** 2   → [1, 4, 9]       # elementwise

ŽÁDNÉ for smyčky! NumPy to dělá v C → 100x rychlejší.""",
        task="Sčítání, násobení, mocniny — vše vektorově.",
        difficulty=1, points=15,
        hints=["np.array + np.array, np.array * 3, np.array ** 2"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and np.array_equal(r[0], np.array([11, 22, 33, 44, 55])),
                    "Součet ✓"
                )
            )(operace_s_poli()) if HAS_NUMPY else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Indexování a Slicing",
        theory="""2D INDEXOVÁNÍ:
mat = np.array([[1,2,3],[4,5,6],[7,8,9]])

mat[1, 2]       → 6        # řádek 1, sloupec 2
mat[1]           → [4,5,6]  # celý řádek
mat[:, 2]        → [3,6,9]  # celý sloupec
mat[:2, :2]      → [[1,2],[4,5]]  # podmatice""",
        task="Indexuj matici — prvky, řádky, sloupce, podmatice.",
        difficulty=2, points=20,
        hints=["mat[1,2], mat[1], mat[:,2], mat[:2,:2]"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and r[0] == 6,
                    "Indexování ✓"
                )
            )(indexovani_a_slicing()) if HAS_NUMPY else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Boolean Indexing — filtrování",
        theory="""BOOLEAN INDEXING — mocný filtr:
arr = np.array([3, 7, 2, 8])

arr > 5         → [False, True, False, True]
arr[arr > 5]    → [7, 8]  # jen prvky kde True!

# Kombinace:
arr[(arr > 2) & (arr < 8)]  → [3, 7]""",
        task="Filtruj pole pomocí podmínek.",
        difficulty=2, points=20,
        hints=["arr[arr > 5], arr[arr % 2 == 0], arr[(arr >= 3) & (arr <= 7)]"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and np.array_equal(r[0], np.array([7, 8, 9, 6])),
                    "Boolean filter ✓"
                )
            )(boolean_indexing()) if HAS_NUMPY else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Agregační funkce",
        task="sum, mean, std, min, max, argmin, argmax.",
        difficulty=1, points=15,
        hints=["{'sum': arr.sum(), 'mean': arr.mean(), 'argmax': arr.argmax(), ...}"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and r.get("sum") == 45 and r.get("mean") == 5.0,
                    "Agregace ✓"
                )
            )(agregace()) if HAS_NUMPY else verify(True, "Skip"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "NumPy Základy", "07_01")
