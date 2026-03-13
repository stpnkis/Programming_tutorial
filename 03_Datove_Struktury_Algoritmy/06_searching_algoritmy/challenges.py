#!/usr/bin/env python3
"""🔍 DSA — Searching Algoritmy: Vyhledávací techniky."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def linearni_hledani(lst: list, cil) -> int:
    """
    🎯 VÝZVA 1: Lineární hledání — O(n).
    Vrať index prvního výskytu nebo -1.
    """
    # TODO: ↓
    pass


def binarni_hledani(lst: list, cil) -> int:
    """
    🎯 VÝZVA 2: Binární hledání (iterativní) — O(log n).
    lst JE SEŘAZENÝ! Vrať index nebo -1.
    """
    # TODO: ↓
    pass


def binarni_rekurze(lst: list, cil, low=0, high=None) -> int:
    """
    🎯 VÝZVA 3: Binární hledání — rekurzivní verze.
    """
    # TODO: ↓
    pass


def najdi_prvni_vetsi(lst: list, cil) -> int:
    """
    🎯 VÝZVA 4: V seřazeném seznamu najdi index prvního prvku > cíl.
    [1, 3, 5, 7, 9], cíl=4 → 2 (index prvku 5)
    Pokud žádný není větší, vrať len(lst).
    Použij modifikované bin. hledání!
    """
    # TODO: ↓
    pass


def hledej_ve_2d(matice: list, cil) -> tuple:
    """
    🎯 VÝZVA 5: Hledání v seřazené 2D matici.
    Každý řádek seřazený, první prvek řádku > poslední předchozího.
    [[1,3,5],[7,9,11],[13,15,17]], cíl=9 → (1, 1)
    Vrať (řádek, sloupec) nebo (-1, -1).
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Lineární hledání — O(n)",
        theory="""LINEÁRNÍ HLEDÁNÍ: projdi vše od začátku.
  for i, prvek in enumerate(lst):
      if prvek == cil:
          return i
  return -1

Jednoduché, ale pomalé pro velké seznamy.""",
        task="Projdi seznam a vrať index.",
        difficulty=1, points=10,
        hints=["enumerate() pro index + hodnotu"],
        tests=[
            lambda: verify(linearni_hledani([10, 20, 30, 40], 30) == 2, "Nalezeno ✓"),
            lambda: verify(linearni_hledani([10, 20, 30], 99) == -1, "Nenalezeno ✓"),
            lambda: verify(linearni_hledani([], 1) == -1, "Prázdný ✓"),
        ]
    ),
    Challenge(
        title="Binární hledání — O(log n)",
        theory="""BINÁRNÍ HLEDÁNÍ: rozděl interval napůl.
PŘEDPOKLAD: seznam je SEŘAZENÝ!

  low, high = 0, len(lst) - 1
  while low <= high:
      mid = (low + high) // 2
      if lst[mid] == cil:    return mid
      elif lst[mid] < cil:   low = mid + 1
      else:                  high = mid - 1
  return -1

1000 prvků → max 10 kroků (log₂ 1000 ≈ 10)
1 000 000 → max 20 kroků!""",
        task="Binární hledání (iterativní).",
        difficulty=2, points=25,
        hints=["mid = (low + high) // 2; porovnej lst[mid] s cílem"],
        tests=[
            lambda: verify(binarni_hledani([1, 3, 5, 7, 9], 5) == 2, "Nalezeno ✓"),
            lambda: verify(binarni_hledani([1, 3, 5, 7, 9], 4) == -1, "Nenalezeno ✓"),
            lambda: verify(binarni_hledani([42], 42) == 0, "Jeden prvek ✓"),
        ]
    ),
    Challenge(
        title="Binární hledání — rekurze",
        task="Rekurzivní verze binárního hledání.",
        difficulty=2, points=25,
        hints=["if high is None: high = len(lst)-1; if low > high: return -1"],
        tests=[
            lambda: verify(binarni_rekurze([1, 3, 5, 7, 9], 7) == 3, "Rekurzivní ✓"),
            lambda: verify(binarni_rekurze([1, 3, 5, 7, 9], 2) == -1, "Nenalezeno ✓"),
            lambda: verify(binarni_rekurze([], 1) == -1, "Prázdný ✓"),
        ]
    ),
    Challenge(
        title="První větší — modifikace bin. hledání",
        theory="""Variace na bin. hledání:
Nehledáš PŘESNÝ zásah, ale HRANICI.

  result = len(lst)
  while low <= high:
      mid = (low + high) // 2
      if lst[mid] > cil:
          result = mid
          high = mid - 1
      else:
          low = mid + 1""",
        task="Najdi index prvního prvku většího než cíl.",
        difficulty=2, points=25,
        hints=["Udržuj result = len(lst); aktualizuj při nálezu většího"],
        tests=[
            lambda: verify(najdi_prvni_vetsi([1, 3, 5, 7, 9], 4) == 2, "5>4 na idx 2 ✓"),
            lambda: verify(najdi_prvni_vetsi([1, 3, 5, 7, 9], 9) == 5, "Nic větší ✓"),
            lambda: verify(najdi_prvni_vetsi([1, 3, 5, 7, 9], 0) == 0, "Vše větší ✓"),
        ]
    ),
    Challenge(
        title="Hledání ve 2D matici",
        theory="""Seřazená 2D matice — dvě bin. hledání:
1. Najdi správný řádek (bin. hledáním)
2. Ve řádku najdi prvek (bin. hledáním)

Nebo: flatten na index → mid//cols, mid%cols""",
        task="Hledej v seřazené matici efektivně.",
        difficulty=3, points=30,
        hints=["Převeď 2D na 1D index: row = mid // cols, col = mid % cols"],
        tests=[
            lambda: verify(
                hledej_ve_2d([[1, 3, 5], [7, 9, 11], [13, 15, 17]], 9) == (1, 1),
                "Nalezeno (1,1) ✓"
            ),
            lambda: verify(
                hledej_ve_2d([[1, 3, 5], [7, 9, 11], [13, 15, 17]], 4) == (-1, -1),
                "Nenalezeno ✓"
            ),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "DSA — Searching Algoritmy", "03_06")
