#!/usr/bin/env python3
"""🏆 DSA — Praktické Úlohy: Kombinace všeho dohromady."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def je_palindrom(s: str) -> bool:
    """
    🎯 VÝZVA 1: Je řetězec palindrom? (ignoruj mezery, velikost)
    "A man a plan a canal Panama" → True
    """
    # TODO: ↓
    pass


def nejdelsi_bez_opakovani(s: str) -> int:
    """
    🎯 VÝZVA 2: Délka nejdelšího podřetězce bez opakujících se znaků.
    "abcabcbb" → 3 ("abc")
    "bbbbb" → 1
    Hint: sliding window + set.
    """
    # TODO: ↓
    pass


def spirala(matice: list) -> list:
    """
    🎯 VÝZVA 3: Projdi matici spirálově.
    [[1,2,3],[4,5,6],[7,8,9]] → [1,2,3,6,9,8,7,4,5]
    """
    # TODO: ↓
    pass


def vyhodnost_akcii(ceny: list) -> int:
    """
    🎯 VÝZVA 4: Max zisk z jednoho nákupu a prodeje.
    [7,1,5,3,6,4] → 5 (kup za 1, prodej za 6)
    [7,6,4,3,1] → 0 (žádný zisk)
    """
    # TODO: ↓
    pass


def platne_ip(s: str) -> list:
    """
    🎯 VÝZVA 5: Generuj všechny platné IP adresy z řetězce číslic.
    "25525511135" → ["255.255.11.135", "255.255.111.35"]
    Každá část 0-255. Žádné vedoucí nuly (kromě "0").
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Palindrom — two pointers",
        theory="""TWO POINTERS pro palindrom:
  s = s.lower().replace(" ", "")
  i, j = 0, len(s) - 1
  while i < j:
      if s[i] != s[j]: return False
      i += 1; j -= 1""",
        task="Zkontroluj palindrom (ignoruj mezery/velikost písmen).",
        difficulty=1, points=15,
        hints=["Normalizuj: s.lower().replace(' ',''); pak two pointers"],
        tests=[
            lambda: verify(je_palindrom("A man a plan a canal Panama"), "Věta ✓"),
            lambda: verify(je_palindrom("racecar"), "racecar ✓"),
            lambda: verify(not je_palindrom("hello"), "hello ✗ ✓"),
        ]
    ),
    Challenge(
        title="Nejdelší podřetězec bez opakování",
        theory="""SLIDING WINDOW:
  start = 0
  videne = set()
  max_delka = 0
  for end in range(len(s)):
      while s[end] in videne:
          videne.remove(s[start])
          start += 1
      videne.add(s[end])
      max_delka = max(max_delka, end - start + 1)""",
        task="Sliding window pro nejdelší unikátní podřetězec.",
        difficulty=3, points=30,
        hints=["Posunuj start doprava dokud se end-ový znak neopakuje"],
        tests=[
            lambda: verify(nejdelsi_bez_opakovani("abcabcbb") == 3, "abc ✓"),
            lambda: verify(nejdelsi_bez_opakovani("bbbbb") == 1, "bbbbb ✓"),
            lambda: verify(nejdelsi_bez_opakovani("pwwkew") == 3, "wke ✓"),
            lambda: verify(nejdelsi_bez_opakovani("") == 0, "Prázdný ✓"),
        ]
    ),
    Challenge(
        title="Spirálový průchod maticí",
        task="Projdi 2D matici spirálově (→↓←↑).",
        difficulty=3, points=30,
        hints=[
            "Udržuj hranice: top, bottom, left, right",
            "4 smyčky: →, ↓, ←, ↑; po každé zúži hranice"
        ],
        tests=[
            lambda: verify(
                spirala([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5],
                "3×3 ✓"
            ),
            lambda: verify(spirala([[1]]) == [1], "1×1 ✓"),
            lambda: verify(spirala([]) == [], "Prázdná ✓"),
        ]
    ),
    Challenge(
        title="Výhodnost akcií — min/max",
        theory="""Sleduj MINIMUM a maximální ZISK:
  min_cena = ceny[0]
  max_zisk = 0
  for cena in ceny[1:]:
      min_cena = min(min_cena, cena)
      max_zisk = max(max_zisk, cena - min_cena)""",
        task="Kdy koupit a prodat pro max zisk?",
        difficulty=2, points=25,
        hints=["Udržuj dosavadní minimum ceny a maximální zisk"],
        tests=[
            lambda: verify(vyhodnost_akcii([7, 1, 5, 3, 6, 4]) == 5, "Zisk 5 ✓"),
            lambda: verify(vyhodnost_akcii([7, 6, 4, 3, 1]) == 0, "Žádný zisk ✓"),
        ]
    ),
    Challenge(
        title="Platné IP adresy — backtracking",
        task="Generuj všechny platné IP z řetězce číslic.",
        difficulty=4, points=40,
        hints=[
            "Backtracking: vyber 1-3 znaky pro každou část (4 části)",
            "Ověř: int(part) <= 255 a žádné vedoucí nuly"
        ],
        tests=[
            lambda: verify(
                sorted(platne_ip("25525511135")) == sorted(["255.255.11.135", "255.255.111.35"]),
                "IP ✓",
                f"Výsledek: {platne_ip('25525511135')}"
            ),
            lambda: verify(platne_ip("0000") == ["0.0.0.0"], "0.0.0.0 ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "DSA — Praktické Úlohy", "03_10")
