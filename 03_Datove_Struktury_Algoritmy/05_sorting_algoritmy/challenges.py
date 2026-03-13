#!/usr/bin/env python3
"""📈 DSA — Sorting Algoritmy: Řadící algoritmy od nuly."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def bubble_sort(lst: list) -> list:
    """
    🎯 VÝZVA 1: Bubble Sort — bublinkové řazení.
    Porovnávej sousedy a prohazuj. Opakuj dokud nejsou seřazené.
    Vrať NOVÝ seřazený seznam (neměň originál).
    """
    # TODO: ↓
    pass


def selection_sort(lst: list) -> list:
    """
    🎯 VÝZVA 2: Selection Sort.
    Najdi minimum, dej na začátek. Opakuj pro zbytek.
    Vrať NOVÝ seřazený seznam.
    """
    # TODO: ↓
    pass


def insertion_sort(lst: list) -> list:
    """
    🎯 VÝZVA 3: Insertion Sort.
    Jako řazení karet v ruce — vezmi kartu, vlož na správné místo.
    Vrať NOVÝ seřazený seznam.
    """
    # TODO: ↓
    pass


def merge_sort(lst: list) -> list:
    """
    🎯 VÝZVA 4: Merge Sort — rozděl a panuj.
    1. Rozděl seznam na půl
    2. Rekurzivně seřaď obě půlky
    3. Slouč (merge) seřazené půlky
    O(n log n)!
    """
    # TODO: ↓
    pass


def quick_sort(lst: list) -> list:
    """
    🎯 VÝZVA 5: Quick Sort — rychlé řazení.
    1. Vyber pivot (např. poslední prvek)
    2. Rozděl na menší a větší
    3. Rekurzivně seřaď obě části
    Vrať NOVÝ seřazený seznam.
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

test_data = [
    ([64, 34, 25, 12, 22, 11, 90], [11, 12, 22, 25, 34, 64, 90]),
    ([], []),
    ([1], [1]),
    ([3, 1, 2], [1, 2, 3]),
    ([5, 5, 3, 3], [3, 3, 5, 5]),
]

challenges = [
    Challenge(
        title="Bubble Sort — O(n²)",
        theory="""BUBBLE SORT:
Porovnávej sousedy, větší "bublá" nahoru.

  for i in range(n):
      for j in range(n - 1 - i):
          if lst[j] > lst[j+1]:
              lst[j], lst[j+1] = lst[j+1], lst[j]

Složitost: O(n²) — pomalý, ale snadný na pochopení.
Optimalizace: pokud žádný swap → hotovo.""",
        task="Implementuj bubble sort.",
        difficulty=1, points=15,
        hints=["Dva vnořené cykly, swap sousedních pokud špatné pořadí"],
        tests=[
            lambda: verify(bubble_sort(test_data[0][0]) == test_data[0][1], "Hlavní test ✓"),
            lambda: verify(bubble_sort([]) == [], "Prázdný ✓"),
            lambda: verify(bubble_sort([5, 5, 3, 3]) == [3, 3, 5, 5], "Duplikáty ✓"),
        ]
    ),
    Challenge(
        title="Selection Sort — O(n²)",
        theory="""SELECTION SORT:
V každém kroku najdi minimum ze zbytku.

  for i in range(n):
      min_idx = i
      for j in range(i+1, n):
          if lst[j] < lst[min_idx]:
              min_idx = j
      lst[i], lst[min_idx] = lst[min_idx], lst[i]""",
        task="Najdi minimum, přesuň na začátek.",
        difficulty=1, points=15,
        hints=["min_idx hledej vnořeným cyklem od i+1"],
        tests=[
            lambda: verify(selection_sort(test_data[0][0]) == test_data[0][1], "Selection ✓"),
            lambda: verify(selection_sort([3, 1, 2]) == [1, 2, 3], "[3,1,2] ✓"),
        ]
    ),
    Challenge(
        title="Insertion Sort — O(n²)",
        theory="""INSERTION SORT:
Jak řadíš karty — bere po jedné a vkládáš kam patří.

  for i in range(1, n):
      klic = lst[i]
      j = i - 1
      while j >= 0 and lst[j] > klic:
          lst[j+1] = lst[j]
          j -= 1
      lst[j+1] = klic

Výhoda: rychlý pro skoro seřazené! O(n) best case.""",
        task="Řaď jako karty — vkládej na správné místo.",
        difficulty=2, points=20,
        hints=["while j >= 0 and lst[j] > klic: posouvej doprava"],
        tests=[
            lambda: verify(insertion_sort(test_data[0][0]) == test_data[0][1], "Insertion ✓"),
            lambda: verify(insertion_sort([1]) == [1], "Jeden prvek ✓"),
        ]
    ),
    Challenge(
        title="Merge Sort — O(n log n)",
        theory="""MERGE SORT — Divide & Conquer:
  def merge_sort(lst):
      if len(lst) <= 1: return lst
      mid = len(lst) // 2
      levy = merge_sort(lst[:mid])
      pravy = merge_sort(lst[mid:])
      return merge(levy, pravy)

  merge() sloučí dva seřazené seznamy (viz předchozí lekce!).
Vždy O(n log n) — stabilní, spolehlivý.""",
        task="Rozděl a panuj — rekurzivní merge sort.",
        difficulty=3, points=30,
        hints=["Rozděl: mid = len//2; merge pomocí dvou pointerů"],
        tests=[
            lambda: verify(merge_sort(test_data[0][0]) == test_data[0][1], "Merge Sort ✓"),
            lambda: verify(merge_sort([]) == [], "Prázdný ✓"),
            lambda: verify(merge_sort([9, 1, 8, 2, 7, 3]) == [1, 2, 3, 7, 8, 9], "Mix ✓"),
        ]
    ),
    Challenge(
        title="Quick Sort — O(n log n) průměrně",
        theory="""QUICK SORT:
  def quick_sort(lst):
      if len(lst) <= 1: return lst
      pivot = lst[-1]
      mensi = [x for x in lst[:-1] if x <= pivot]
      vetsi = [x for x in lst[:-1] if x > pivot]
      return quick_sort(mensi) + [pivot] + quick_sort(vetsi)

Průměrně O(n log n), worst case O(n²).
V praxi často nejrychlejší.""",
        task="Quick sort s pivotem.",
        difficulty=3, points=30,
        hints=["pivot = lst[-1]; mensi = [x for x in lst[:-1] if x <= pivot]"],
        tests=[
            lambda: verify(quick_sort(test_data[0][0]) == test_data[0][1], "Quick Sort ✓"),
            lambda: verify(quick_sort([]) == [], "Prázdný ✓"),
            lambda: verify(quick_sort([5, 5, 5]) == [5, 5, 5], "Stejné prvky ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "DSA — Sorting Algoritmy", "03_05")
