#!/usr/bin/env python3
"""
🐍 PYTHON ZÁKLADY — Podmínky a cykly
Řízení toku programu — if/else, for, while.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def vyzva_1(cislo):
    """
    🎯 Napiš funkci, která vrátí:
    - "kladné" pokud je číslo > 0
    - "záporné" pokud je číslo < 0
    - "nula" pokud je číslo == 0
    """
    if cislo > 0:
        return "kladné"
    elif cislo == 0:
        return "nula"
    else: 
        return "záporné"


def vyzva_2(cislo):
    """
    🎯 FizzBuzz klasika!
    - Číslo dělitelné 3 → "Fizz"
    - Číslo dělitelné 5 → "Buzz"
    - Číslo dělitelné 3 i 5 → "FizzBuzz"
    - Jinak → číslo jako string
    """
    if cislo%3 == 0 and cislo%5 == 0:
        return "FizzBuzz"
    elif cislo%3 == 0:
        return "Fizz"
    elif cislo%5 == 0:
        return "Buzz"
    else:
        return str(cislo)
    
def vyzva_3(n):
    """
    🎯 Pomocí for cyklu vrať součet čísel od 1 do n (včetně).
    Příklad: n=5 → 1+2+3+4+5 = 15
    """
    for i in range(n):
        if i == 0:
            soucet = 0
        else:
            soucet += i
    return soucet + n


    
    
    


def vyzva_4(seznam):
    """
    🎯 Pomocí for cyklu spočítej, kolik sudých čísel je v seznamu.
    Příklad: [1, 2, 3, 4, 5, 6] → 3
    """
    pocet_sudych = 0

    for i in seznam:
        if i%2==0:
            pocet_sudych +=1

    return pocet_sudych


def vyzva_5(text):
    """
    🎯 Pomocí while cyklu odstraňuj poslední znak textu,
    dokud text nekončí na 'a' nebo není prázdný.
    Vrať výsledný text.
    Příklad: "ahojka" → "ahojka" (už končí na 'a')
    Příklad: "python" → "" (žádné 'a' nenajdeš)
    Příklad: "kobra" → "kobra" (už končí na 'a')
    """
    while text and text[-1] != 'a':
        text = text[:-1]
    return text

def vyzva_6():
    """
    🎯 Vytvoř seznam prvních 10 násobků čísla 7 (7, 14, 21, ..., 70)
    pomocí for cyklu. Vrať ho jako list.
    """
    nasobky = []

    for i in range(1,11):
        nasobky.append(i*7)
    return nasobky


def vyzva_7(matice):
    """
    🎯 Vnořené cykly: Projdi 2D matici (seznam seznamů) a vrať
    součet všech prvků.
    Příklad: [[1, 2], [3, 4], [5, 6]] → 21
    """
    soucet = 0

    for i in matice:
        for m in i:
            soucet+=m

    return soucet




# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="If / Elif / Else — rozhodování",
        theory="""Podmínky řídí tok programu:
  if podminka:
      ...
  elif jina_podminka:
      ...
  else:
      ...""",
        task="Funkce vrátí 'kladné', 'záporné' nebo 'nula' podle čísla.",
        difficulty=1, points=10,
        hints=["if cislo > 0: return 'kladné'", "Nezapomeň na elif a else"],
        tests=[
            lambda: verify(vyzva_1(5) == "kladné", "Kladné ✓", f"vyzva_1(5): očekáváno 'kladné', dostal '{vyzva_1(5)}'"),
            lambda: verify(vyzva_1(-3) == "záporné", "Záporné ✓", f"vyzva_1(-3): očekáváno 'záporné', dostal '{vyzva_1(-3)}'"),
            lambda: verify(vyzva_1(0) == "nula", "Nula ✓", f"vyzva_1(0): očekáváno 'nula', dostal '{vyzva_1(0)}'"),
        ]
    ),
    Challenge(
        title="FizzBuzz — klasický test",
        theory="""FizzBuzz je jeden z nejznámějších programovacích testů.
Testuje schopnost kombinovat podmínky.
Klíč: Kontroluj dělitelnost 3 i 5 PRVNÍ (jinak se ti to rozpadne).""",
        task="Implementuj FizzBuzz.",
        difficulty=2, points=20,
        hints=[
            "Dělitelnost: cislo % 3 == 0",
            "Kontroluj nejdřív cislo % 15 == 0 (nebo % 3 == 0 and % 5 == 0)",
            "Jinak: return str(cislo)"
        ],
        tests=[
            lambda: verify(vyzva_2(15) == "FizzBuzz", "FizzBuzz(15) ✓"),
            lambda: verify(vyzva_2(9) == "Fizz", "Fizz(9) ✓"),
            lambda: verify(vyzva_2(10) == "Buzz", "Buzz(10) ✓"),
            lambda: verify(vyzva_2(7) == "7", "Číslo(7) ✓"),
        ]
    ),
    Challenge(
        title="For cyklus — součet čísel",
        theory="""For cyklus prochází přes sekvenci:
  for i in range(1, n+1):   # čísla 1, 2, ..., n
      ...
range(start, stop) — stop NENÍ zahrnutý!""",
        task="Vrať součet 1 + 2 + ... + n.",
        difficulty=1, points=10,
        hints=["soucet = 0; for i in range(1, n+1): soucet += i"],
        tests=[
            lambda: verify(vyzva_3(5) == 15, "n=5 → 15 ✓"),
            lambda: verify(vyzva_3(100) == 5050, "n=100 → 5050 ✓"),
            lambda: verify(vyzva_3(1) == 1, "n=1 → 1 ✓"),
        ]
    ),
    Challenge(
        title="Počítání sudých čísel",
        task="Spočítej kolik sudých čísel je v seznamu.",
        difficulty=1, points=10,
        hints=["Sudé číslo: x % 2 == 0", "Zaveď počítadlo a v cyklu ho zvyšuj"],
        tests=[
            lambda: verify(vyzva_4([1,2,3,4,5,6]) == 3, "[1-6] → 3 sudá ✓"),
            lambda: verify(vyzva_4([1,3,5]) == 0, "[1,3,5] → 0 sudých ✓"),
            lambda: verify(vyzva_4([2,4,6,8]) == 4, "[2,4,6,8] → 4 sudá ✓"),
        ]
    ),
    Challenge(
        title="While cyklus — ořezávání textu",
        theory="""While cyklus běží dokud je podmínka True:
  while podminka:
      ...
Pozor na nekonečné cykly! Vždy měj podmínku ukončení.""",
        task="Ořezávej text odzadu, dokud nekončí na 'a' nebo není prázdný.",
        difficulty=2, points=15,
        hints=[
            "while text and text[-1] != 'a':",
            "text = text[:-1] — odstraní poslední znak"
        ],
        tests=[
            lambda: verify(vyzva_5("ahojka") == "ahojka", "'ahojka' → 'ahojka' ✓"),
            lambda: verify(vyzva_5("python") == "", "'python' → '' ✓"),
            lambda: verify(vyzva_5("kobra") == "kobra", "'kobra' → 'kobra' ✓"),
        ]
    ),
    Challenge(
        title="Násobky sedmičky",
        task="Vytvoř list [7, 14, 21, ..., 70] pomocí for cyklu.",
        difficulty=1, points=10,
        hints=["for i in range(1, 11): vysledek.append(i * 7)"],
        tests=[
            lambda: verify(
                vyzva_6() == [7, 14, 21, 28, 35, 42, 49, 56, 63, 70],
                "Násobky 7 správně! ✓"
            ),
        ]
    ),
    Challenge(
        title="Vnořené cykly — součet matice",
        theory="""Vnořené cykly procházejí 2D struktury:
  for radek in matice:
      for prvek in radek:
          ...""",
        task="Spočítej součet všech prvků v 2D matici.",
        difficulty=2, points=15,
        hints=["Dva vnořené for cykly", "Nebo: sum(sum(radek) for radek in matice)"],
        tests=[
            lambda: verify(vyzva_7([[1,2],[3,4],[5,6]]) == 21, "[[1,2],[3,4],[5,6]] → 21 ✓"),
            lambda: verify(vyzva_7([[10]]) == 10, "[[10]] → 10 ✓"),
            lambda: verify(vyzva_7([[0,0],[0,0]]) == 0, "Samé nuly → 0 ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Python Základy — Podmínky a cykly", "01_02")
