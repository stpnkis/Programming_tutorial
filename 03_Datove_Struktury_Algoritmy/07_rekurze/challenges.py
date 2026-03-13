#!/usr/bin/env python3
"""🔄 DSA — Rekurze: Síla volání sebe sama."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def faktorial(n: int) -> int:
    """
    🎯 VÝZVA 1: Faktoriál rekurzivně.
    0! = 1, n! = n * (n-1)!
    """
    # TODO: ↓
    pass


def fibonacci(n: int) -> int:
    """
    🎯 VÝZVA 2: N-tý Fibonacci číslo (rekurzivně).
    fib(0)=0, fib(1)=1, fib(n)=fib(n-1)+fib(n-2)
    """
    # TODO: ↓
    pass


def mocnina(zaklad: float, exp: int) -> float:
    """
    🎯 VÝZVA 3: Rychlá mocnina rekurzivně — O(log n).
    x^0 = 1
    x^n = (x^(n//2))² pokud n sudé
    x^n = x * x^(n-1) pokud n liché
    """
    # TODO: ↓
    pass


def flatten(lst: list) -> list:
    """
    🎯 VÝZVA 4: Zploštění vnořeného seznamu.
    [1, [2, [3, 4], 5], 6] → [1, 2, 3, 4, 5, 6]
    """
    # TODO: ↓
    pass


def hanoi(n: int, zdroj="A", cil="C", pomocny="B") -> list:
    """
    🎯 VÝZVA 5: Hanojské věže — vrať seznam tahů.
    Vrať [(zdroj, cíl), ...] pro přesun n disků.
    hanoi(1) → [("A", "C")]
    hanoi(2) → [("A", "B"), ("A", "C"), ("B", "C")]
    """
    # TODO: ↓
    pass


def permutace(lst: list) -> list:
    """
    🎯 VÝZVA 6: Všechny permutace seznamu.
    [1,2,3] → [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Faktoriál — základ rekurze",
        theory="""REKURZE = funkce volá samu sebe.

Dva klíčové prvky:
1. BASE CASE — kdy přestanu (jinak nekonečná smyčka!)
2. RECURSIVE CASE — zmenšení problému

  def faktorial(n):
      if n <= 1: return 1     # BASE CASE
      return n * faktorial(n-1)  # RECURSIVE CASE

  faktorial(4) = 4 * 3 * 2 * 1 = 24

⚠️ Bez base case → RecursionError (stack overflow)!""",
        task="Klasický faktoriál rekurzivně.",
        difficulty=1, points=10,
        hints=["if n <= 1: return 1; return n * faktorial(n-1)"],
        tests=[
            lambda: verify(faktorial(5) == 120, "5! = 120 ✓"),
            lambda: verify(faktorial(0) == 1, "0! = 1 ✓"),
            lambda: verify(faktorial(1) == 1, "1! = 1 ✓"),
        ]
    ),
    Challenge(
        title="Fibonacci — dvojitá rekurze",
        task="F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).",
        difficulty=1, points=15,
        hints=["if n <= 0: return 0; if n == 1: return 1"],
        tests=[
            lambda: verify(fibonacci(10) == 55, "F(10)=55 ✓"),
            lambda: verify(fibonacci(0) == 0, "F(0)=0 ✓"),
            lambda: verify(fibonacci(1) == 1, "F(1)=1 ✓"),
        ]
    ),
    Challenge(
        title="Rychlá mocnina — O(log n)",
        theory="""2^10 naivně = 2*2*2*...*2 (10 násobení)
2^10 rychle:
  2^10 = (2^5)^2
  2^5 = 2 * (2^2)^2
  → jen 4 násobení!

  def mocnina(x, n):
      if n == 0: return 1
      if n % 2 == 0:
          half = mocnina(x, n // 2)
          return half * half
      return x * mocnina(x, n - 1)""",
        task="Mocnina v O(log n) pomocí dělení exponentu.",
        difficulty=2, points=25,
        hints=["half = mocnina(zaklad, exp // 2); return half * half"],
        tests=[
            lambda: verify(mocnina(2, 10) == 1024, "2^10=1024 ✓"),
            lambda: verify(mocnina(3, 0) == 1, "3^0=1 ✓"),
            lambda: verify(mocnina(5, 3) == 125, "5^3=125 ✓"),
        ]
    ),
    Challenge(
        title="Flatten vnořeného seznamu",
        task="Rekurze pro zploštění libovolně vnořených seznamů.",
        difficulty=2, points=20,
        hints=["for prvek in lst: if isinstance(prvek, list): result.extend(flatten(prvek)); else: result.append(prvek)"],
        tests=[
            lambda: verify(flatten([1, [2, [3, 4], 5], 6]) == [1, 2, 3, 4, 5, 6], "Vnořený ✓"),
            lambda: verify(flatten([]) == [], "Prázdný ✓"),
            lambda: verify(flatten([1, 2, 3]) == [1, 2, 3], "Plochý ✓"),
        ]
    ),
    Challenge(
        title="Hanojské věže",
        theory="""Hanojské věže — klasický rekurzivní problém:
  def hanoi(n, zdroj, cíl, pomocný):
      if n == 1: return [(zdroj, cíl)]
      tahy = hanoi(n-1, zdroj, pomocný, cíl)
      tahy.append((zdroj, cíl))
      tahy += hanoi(n-1, pomocný, cíl, zdroj)
      return tahy

n disků → 2^n - 1 tahů.""",
        task="Vyřeš Hanojské věže rekurzí.",
        difficulty=3, points=30,
        hints=["n==1: [(zdroj,cil)]; jinak: přesuň n-1 + přesuň 1 + přesuň n-1"],
        tests=[
            lambda: verify(hanoi(1) == [("A", "C")], "1 disk ✓"),
            lambda: verify(hanoi(2) == [("A", "B"), ("A", "C"), ("B", "C")], "2 disky ✓"),
            lambda: verify(len(hanoi(3)) == 7, "3 disky = 7 tahů ✓"),
        ]
    ),
    Challenge(
        title="Všechny permutace",
        task="Generuj permutace rekurzivním backtrackingem.",
        difficulty=3, points=30,
        hints=[
            "Base: if len(lst) <= 1: return [lst]",
            "Pro každý prvek: odeber ho, permutuj zbytek, přidej zpět"
        ],
        tests=[
            lambda: verify(len(permutace([1, 2, 3])) == 6, "3! = 6 permutací ✓"),
            lambda: verify(sorted(permutace([1, 2])) == [[1, 2], [2, 1]], "[1,2] perm ✓"),
            lambda: verify(permutace([1]) == [[1]], "Jedna permutace ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "DSA — Rekurze", "03_07")
