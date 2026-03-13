#!/usr/bin/env python3
"""📊 DSA — Arrays a Linked Lists: Základní datové struktury."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def otoc_seznam(lst: list) -> list:
    """
    🎯 VÝZVA 1: Otoč seznam BEZ reversed() nebo [::-1].
    Použij smyčku nebo swap.
    [1,2,3,4] → [4,3,2,1]
    """
    # TODO: ↓
    pass


def najdi_duplikaty(lst: list) -> list:
    """
    🎯 VÝZVA 2: Najdi všechny prvky, co se opakují.
    [1,2,3,2,4,3] → [2, 3] (seřazené)
    """
    # TODO: ↓
    pass


def merge_sorted(a: list, b: list) -> list:
    """
    🎯 VÝZVA 3: Slouč dva SEŘAZENÉ seznamy do jednoho seřazeného.
    BEZ sorted(). Použij dva ukazatele (pointery).
    merge_sorted([1,3,5], [2,4,6]) → [1,2,3,4,5,6]
    """
    # TODO: ↓
    pass


class Uzel:
    """Uzel linked listu."""
    def __init__(self, hodnota, dalsi=None):
        self.hodnota = hodnota
        self.dalsi = dalsi

    def __repr__(self):
        vals = []
        u = self
        while u:
            vals.append(str(u.hodnota))
            u = u.dalsi
        return " → ".join(vals)


class LinkedList:
    """
    🎯 VÝZVA 4: Jednoduchý linked list.
    - __init__(): self.hlava = None
    - pridej(hodnota) → přidej na KONEC
    - jako_seznam() → [1, 2, 3] (list hodnot)
    - __len__() → počet prvků
    - __repr__() → "1 → 2 → 3"
    """
    # TODO: ↓
    pass


def najdi_prostredni(ll) -> int:
    """
    🎯 VÝZVA 5: Najdi prostřední prvek linked listu.
    Použij techniku dvou ukazatelů (slow/fast pointer).
    [1,2,3,4,5] → 3
    [1,2,3,4] → 3 (druhý z prostředních)
    """
    # TODO: ↓ předpokládej ll je LinkedList s atributem hlava (Uzel)
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Otoč seznam ručně",
        theory="""ARRAY (Python list) = souvislý blok paměti.
✅ Rychlý přístup: O(1) — lst[i]
❌ Pomalé vkládání: O(n) — lst.insert(0, x)

Technika SWAP:
  i, j = 0, len(lst)-1
  while i < j:
      lst[i], lst[j] = lst[j], lst[i]
      i += 1; j -= 1""",
        task="Otoč seznam pomocí swapů (bez [::-1]).",
        difficulty=1, points=15,
        hints=["while i < j: lst[i],lst[j] = lst[j],lst[i]; i+=1; j-=1"],
        tests=[
            lambda: verify(otoc_seznam([1, 2, 3, 4]) == [4, 3, 2, 1], "[1,2,3,4] ✓"),
            lambda: verify(otoc_seznam([]) == [], "Prázdný ✓"),
            lambda: verify(otoc_seznam([42]) == [42], "Jeden prvek ✓"),
        ]
    ),
    Challenge(
        title="Najdi duplikáty v seznamu",
        task="Vrať seřazený seznam prvků, co se opakují.",
        difficulty=1, points=15,
        hints=["Použij Counter nebo set pro počítání výskytů"],
        tests=[
            lambda: verify(najdi_duplikaty([1, 2, 3, 2, 4, 3]) == [2, 3], "Duplikáty ✓"),
            lambda: verify(najdi_duplikaty([1, 2, 3]) == [], "Žádné ✓"),
            lambda: verify(najdi_duplikaty([5, 5, 5]) == [5], "Jeden opakující ✓"),
        ]
    ),
    Challenge(
        title="Merge dvou seřazených seznamů",
        theory="""DVA UKAZATELE (Two Pointers):
  i, j = 0, 0
  while i < len(a) and j < len(b):
      if a[i] <= b[j]:
          result.append(a[i]); i += 1
      else:
          result.append(b[j]); j += 1
  # nezapomeň na zbytek!""",
        task="Slouč dva seřazené seznamy — O(n+m).",
        difficulty=2, points=25,
        hints=["Po while-smyčce přidej result.extend(a[i:]) a result.extend(b[j:])"],
        tests=[
            lambda: verify(merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6], "Merge ✓"),
            lambda: verify(merge_sorted([], [1, 2]) == [1, 2], "Prázdný + plný ✓"),
            lambda: verify(merge_sorted([1], [1]) == [1, 1], "Stejné prvky ✓"),
        ]
    ),
    Challenge(
        title="Linked List od nuly",
        theory="""LINKED LIST = uzly propojené referencemi.
✅ Rychlé vkládání: O(1) na začátek
❌ Pomalý přístup: O(n) — musíš projít

  class Uzel:
      def __init__(self, hodnota, dalsi=None):
          self.hodnota = hodnota
          self.dalsi = dalsi

  class LinkedList:
      def __init__(self):
          self.hlava = None
      def pridej(self, h):
          if not self.hlava:
              self.hlava = Uzel(h)
          else:
              aktualni = self.hlava
              while aktualni.dalsi:
                  aktualni = aktualni.dalsi
              aktualni.dalsi = Uzel(h)""",
        task="Implementuj LinkedList s pridej(), jako_seznam(), __len__.",
        difficulty=2, points=30,
        hints=["Procházej uzly: while aktualni.dalsi: aktualni = aktualni.dalsi"],
        tests=[
            lambda: (
                lambda ll: (ll.pridej(1), ll.pridej(2), ll.pridej(3),
                    verify(ll.jako_seznam() == [1, 2, 3], "jako_seznam ✓"))
            )(LinkedList())[3],
            lambda: (
                lambda ll: (ll.pridej(10), ll.pridej(20),
                    verify(len(ll) == 2, "__len__ ✓"))
            )(LinkedList())[2],
            lambda: verify(len(LinkedList()) == 0, "Prázdný len ✓"),
        ]
    ),
    Challenge(
        title="Prostřední prvek — Slow/Fast pointer",
        theory="""SLOW/FAST POINTER technika:
  slow = fast = hlava
  while fast and fast.dalsi:
      slow = slow.dalsi          # 1 krok
      fast = fast.dalsi.dalsi    # 2 kroky
  # slow je teď uprostřed!

Proč? Fast jde 2x rychleji → když dorazí na konec,
slow je přesně v půlce.""",
        task="Najdi prostřední prvek linked listu.",
        difficulty=3, points=30,
        hints=["slow = fast = ll.hlava; while fast and fast.dalsi: ..."],
        tests=[
            lambda: (
                lambda ll: (ll.pridej(1), ll.pridej(2), ll.pridej(3), ll.pridej(4), ll.pridej(5),
                    verify(najdi_prostredni(ll) == 3, "Lichý [1..5] → 3 ✓"))
            )(LinkedList())[5],
            lambda: (
                lambda ll: (ll.pridej(1), ll.pridej(2), ll.pridej(3), ll.pridej(4),
                    verify(najdi_prostredni(ll) == 3, "Sudý [1..4] → 3 ✓"))
            )(LinkedList())[4],
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "DSA — Arrays a Linked Lists", "03_01")
