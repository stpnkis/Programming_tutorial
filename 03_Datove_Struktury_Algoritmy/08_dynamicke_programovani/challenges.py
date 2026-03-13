#!/usr/bin/env python3
"""💎 DSA — Dynamické Programování: Optimální podstruktury."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def fib_memo(n: int, cache=None) -> int:
    """
    🎯 VÝZVA 1: Fibonacci s memoizací (top-down DP).
    Použij dict jako cache!
    """
    # TODO: ↓
    pass


def fib_tab(n: int) -> int:
    """
    🎯 VÝZVA 2: Fibonacci tabulací (bottom-up DP).
    Vytvoř tabulku od 0 do n, vyplňuj odspodu.
    """
    # TODO: ↓
    pass


def schody(n: int) -> int:
    """
    🎯 VÝZVA 3: Kolik způsobů vyjít n schodů?
    V každém kroku uděláš 1 nebo 2 schody.
    schody(1)=1, schody(2)=2, schody(3)=3, schody(4)=5
    """
    # TODO: ↓
    pass


def max_podposloupnost(cisla: list) -> int:
    """
    🎯 VÝZVA 4: Maximální součet souvislé podposloupnosti (Kadane's).
    [-2, 1, -3, 4, -1, 2, 1, -5, 4] → 6 (podsekvence [4,-1,2,1])
    """
    # TODO: ↓
    pass


def batoh(predmety: list, kapacita: int) -> int:
    """
    🎯 VÝZVA 5: 0/1 Knapsack (batoh).
    predmety = [(vaha, cena), ...]
    kapacita = max váha
    Vrať maximální cenu, co se vejde.
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Fibonacci — Memoizace (Top-Down)",
        theory="""DYNAMICKÉ PROGRAMOVÁNÍ: řeš podproblémy jen jednou!

Naivní fib(40) → miliardy volání → pomalé!
S memoizací: uložíš výsledky → O(n)

TOP-DOWN (memoizace):
  def fib(n, cache={}):
      if n in cache: return cache[n]
      if n <= 1: return n
      cache[n] = fib(n-1, cache) + fib(n-2, cache)
      return cache[n]

⚠️ Pozor na mutable default argument — pro test OK.""",
        task="Fibonacci s cache (top-down).",
        difficulty=2, points=20,
        hints=["if cache is None: cache = {}; if n in cache: return cache[n]"],
        tests=[
            lambda: verify(fib_memo(50) == 12586269025, "F(50) rychle ✓"),
            lambda: verify(fib_memo(0) == 0, "F(0) ✓"),
        ]
    ),
    Challenge(
        title="Fibonacci — Tabulace (Bottom-Up)",
        theory="""BOTTOM-UP (tabulace):
  def fib(n):
      if n <= 1: return n
      dp = [0] * (n + 1)
      dp[1] = 1
      for i in range(2, n + 1):
          dp[i] = dp[i-1] + dp[i-2]
      return dp[n]

Výhody: žádná rekurze, žádný stack overflow.""",
        task="Tabulka od 0 do n — vyplňuj odspodu.",
        difficulty=2, points=20,
        hints=["dp = [0]*(n+1); dp[1] = 1; for i in range(2,n+1): dp[i] = dp[i-1]+dp[i-2]"],
        tests=[
            lambda: verify(fib_tab(50) == 12586269025, "F(50) tab ✓"),
            lambda: verify(fib_tab(1) == 1, "F(1) ✓"),
        ]
    ),
    Challenge(
        title="Počet cest po schodech",
        theory="""Schody — jako Fibonacci, ale s příběhem!
  schody(n) = schody(n-1) + schody(n-2)
  (jeden krok + dva kroky)""",
        task="Kolik způsobů vyjít n schodů (1 nebo 2 kroky)?",
        difficulty=2, points=20,
        hints=["Stejná struktura jako Fibonacci!"],
        tests=[
            lambda: verify(schody(1) == 1, "1 schod ✓"),
            lambda: verify(schody(3) == 3, "3 schody ✓"),
            lambda: verify(schody(5) == 8, "5 schodů ✓"),
        ]
    ),
    Challenge(
        title="Kadane's Algorithm — Max podsekvence",
        theory="""Kadane's: udržuj aktuální maximum a globální maximum.
  max_aktualni = max_globalni = cisla[0]
  for x in cisla[1:]:
      max_aktualni = max(x, max_aktualni + x)
      max_globalni = max(max_globalni, max_aktualni)
Pokud přidání je horší než začít znovu → začni znovu.""",
        task="Maximální součet souvislé podsekvence.",
        difficulty=2, points=25,
        hints=["max_aktualni = max(x, max_aktualni + x)"],
        tests=[
            lambda: verify(max_podposloupnost([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6,
                           "Kadane ✓"),
            lambda: verify(max_podposloupnost([-1, -2, -3]) == -1, "Vše záporné ✓"),
            lambda: verify(max_podposloupnost([5]) == 5, "Jeden prvek ✓"),
        ]
    ),
    Challenge(
        title="0/1 Knapsack (Batoh)",
        theory="""Klasický DP problém:
  dp[i][w] = max cena s prvními i předměty a kapacitou w

  for i in range(1, n+1):
      for w in range(kapacita+1):
          if vaha[i] <= w:
              dp[i][w] = max(dp[i-1][w],
                             dp[i-1][w-vaha[i]] + cena[i])
          else:
              dp[i][w] = dp[i-1][w]""",
        task="Optimální výběr předmětů do batohu.",
        difficulty=3, points=35,
        hints=["2D tabulka dp[n+1][kapacita+1]; vyplňuj řádek po řádku"],
        tests=[
            lambda: verify(
                batoh([(2, 3), (3, 4), (4, 5), (5, 6)], 5) == 7,
                "Batoh ✓ (váha 2+3=5, cena 3+4=7)"
            ),
            lambda: verify(batoh([], 10) == 0, "Prázdný ✓"),
            lambda: verify(batoh([(10, 100)], 5) == 0, "Nic se nevejde ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "DSA — Dynamické Programování", "03_08")
