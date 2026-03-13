#!/usr/bin/env python3
"""#️⃣ DSA — Hashování: Slovníky, sety a hash funkce."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def dva_soucty(cisla: list, cil: int) -> tuple:
    """
    🎯 VÝZVA 1: Two Sum — najdi dva indexy, jejichž součet = cíl.
    Použij hash mapu (dict) pro O(n) řešení!
    dva_soucty([2, 7, 11, 15], 9) → (0, 1)
    """
    # TODO: ↓
    pass


def prvni_unikatni(retezec: str) -> str:
    """
    🎯 VÝZVA 2: Najdi první neopakující se znak.
    "aabcbd" → "c"
    "aabb" → ""
    Hint: Counter nebo dict na frekvence.
    """
    # TODO: ↓
    pass


def seskup_anagramy(slova: list) -> list:
    """
    🎯 VÝZVA 3: Seskup slova, co jsou navzájem anagramy.
    ["eat","tea","tan","ate","nat","bat"] → [["eat","tea","ate"],["tan","nat"],["bat"]]
    Vrať skupiny seřazené podle prvního výskytu. Slova ve skupině v původním pořadí.
    Hint: seřazená písmena jako hash klíč!
    """
    # TODO: ↓
    pass


class HashTabulka:
    """
    🎯 VÝZVA 4: Vlastní hash tabulka s řetězením (chaining).
    - __init__(velikost=10)
    - _hash(klic) → index (hash(klic) % velikost)
    - vloz(klic, hodnota) → uloží/přepíše
    - najdi(klic) → hodnota (nebo None)
    - smaz(klic) → True pokud smazáno, False pokud neexistuje
    
    Kolize řeší řetězením: self._buckety[i] = [(k1,v1), (k2,v2)]
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Two Sum — O(n) s hash mapou",
        theory="""HASH MAPA = dict v Pythonu.
O(1) přístup, vkládání i mazání (průměrně).

Two Sum trik:
  videne = {}  # hodnota → index
  for i, num in enumerate(cisla):
      hledane = cil - num
      if hledane in videne:
          return (videne[hledane], i)
      videne[num] = i

BEZ hash mapy: O(n²) — dva vnořené cykly
S hash mapou: O(n) — jeden průchod!""",
        task="Najdi dva čísly co dají součet. Vrať indexy.",
        difficulty=2, points=25,
        hints=["hledane = cil - cisla[i]; if hledane in videne: ..."],
        tests=[
            lambda: verify(dva_soucty([2, 7, 11, 15], 9) == (0, 1), "Two Sum ✓"),
            lambda: verify(dva_soucty([3, 2, 4], 6) == (1, 2), "Druhý test ✓"),
        ]
    ),
    Challenge(
        title="První unikátní znak",
        task="Najdi první znak, co se v řetězci neopakuje.",
        difficulty=1, points=15,
        hints=["from collections import Counter; cnt = Counter(retezec)"],
        tests=[
            lambda: verify(prvni_unikatni("aabcbd") == "c", "'c' ✓"),
            lambda: verify(prvni_unikatni("aabb") == "", "Žádný ✓"),
            lambda: verify(prvni_unikatni("xy") == "x", "'x' ✓"),
        ]
    ),
    Challenge(
        title="Seskupení anagramů",
        theory="""Anagram: stejná písmena, jiné pořadí.
Klíč: seřaď písmena → "eat" → "aet", "tea" → "aet" → STEJNÝ klíč!

  from collections import defaultdict
  groups = defaultdict(list)
  for slovo in slova:
      klic = tuple(sorted(slovo))
      groups[klic].append(slovo)""",
        task="Seskup anagramy pomocí hash mapy.",
        difficulty=2, points=30,
        hints=["klic = ''.join(sorted(slovo)); groups[klic].append(slovo)"],
        tests=[
            lambda: (
                lambda result: verify(
                    [sorted(g) for g in sorted(result, key=lambda x: x[0])] ==
                    [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]],
                    "Anagramy ✓",
                    f"Výsledek: {result}"
                )
            )(seskup_anagramy(["eat", "tea", "tan", "ate", "nat", "bat"])),
        ]
    ),
    Challenge(
        title="Hash tabulka s řetězením",
        theory="""Interně: pole bucketů, každý bucket = seznam párů.
  _buckety = [[], [], [], ...]   # velikost = 10

  def _hash(self, klic):
      return hash(klic) % self._velikost

Kolize: více klíčů mapuje na stejný index
→ řetězení: uložíme oba do seznamu na tom indexu.""",
        task="Vlastní hash tabulka — vlož, najdi, smaž.",
        difficulty=3, points=35,
        hints=[
            "self._buckety = [[] for _ in range(velikost)]",
            "vloz: projdi bucket, přepiš pokud klíč existuje, jinak append"
        ],
        tests=[
            lambda: (
                lambda h: (h.vloz("a", 1), h.vloz("b", 2),
                    verify(h.najdi("a") == 1 and h.najdi("b") == 2, "Vložení + hledání ✓"))
            )(HashTabulka())[2],
            lambda: (
                lambda h: (h.vloz("x", 10), h.vloz("x", 20),
                    verify(h.najdi("x") == 20, "Přepsání ✓"))
            )(HashTabulka())[2],
            lambda: (
                lambda h: (h.vloz("k", 1), 
                    verify(h.smaz("k") == True and h.najdi("k") is None, "Smazání ✓"))
            )(HashTabulka())[1],
            lambda: verify(HashTabulka().najdi("neexistuje") is None, "None pro neexistující ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "DSA — Hashování", "03_04")
