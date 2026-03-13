#!/usr/bin/env python3
"""
🐍 PYTHON ZÁKLADY — Error Handling
Správné zachycení a řízení chyb — robustní kód.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def vyzva_1(a, b):
    """
    🎯 Bezpečné dělení: Vrať a / b.
    Pokud b == 0, vrať string "Dělení nulou!".
    Použij try/except.
    """
    # TODO: ↓
    pass

def vyzva_2(seznam, index):
    """
    🎯 Bezpečný přístup k prvku seznamu.
    Vrať prvek na daném indexu.
    Pokud index neexistuje, vrať None.
    Použij try/except IndexError.
    """
    # TODO: ↓
    pass

def vyzva_3(text):
    """
    🎯 Převeď text na int.
    Pokud se nepovede: zkus float.
    Pokud ani to: vrať None.
    """
    # TODO: Vnořený try/except ↓
    pass

def vyzva_4(vek):
    """
    🎯 Validuj věk: musí být int a v rozsahu 0-150.
    Pokud ne, vyhoď ValueError s popisnou zprávou:
    - "Věk musí být celé číslo" (pokud není int)
    - "Věk musí být mezi 0 a 150" (pokud je mimo rozsah)
    Pokud je OK, vrať True.
    """
    # TODO: raise ValueError(...) ↓
    pass


class NeplatnyEmailError(Exception):
    """Vlastní výjimka pro neplatný email."""
    # TODO (vyzva_5): Vytvořenou třídu nech — je hotová.
    pass


def vyzva_5(email):
    """
    🎯 Validuj email: musí obsahovat '@' a '.'.
    Pokud ne, vyhoď NeplatnyEmailError s textem "Neplatný email: {email}".
    Pokud je OK, vrať True.
    """
    # TODO: ↓
    pass

def vyzva_6(cisla):
    """
    🎯 Projdi seznam a vrať součet. Pokud nějaký prvek
    není číslo (int/float), přeskoč ho (zachyť TypeError/ValueError).
    Příklad: [1, "dva", 3, None, 5] → 9
    """
    # TODO: ↓
    pass

# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Try/Except — bezpečné dělení",
        theory="""try/except zachytí chyby:
  try:
      result = 10 / 0
  except ZeroDivisionError:
      result = "Chyba!"

Bez try/except by program spadl. S ním běží dál.""",
        task="Bezpečně děl čísla, ošetři dělení nulou.",
        difficulty=1, points=10,
        hints=["try: return a / b\nexcept ZeroDivisionError: return 'Dělení nulou!'"],
        tests=[
            lambda: verify(vyzva_1(10, 2) == 5.0, "10/2 = 5.0 ✓"),
            lambda: verify(vyzva_1(10, 0) == "Dělení nulou!", "Dělení nulou ošetřeno ✓"),
        ]
    ),
    Challenge(
        title="IndexError — bezpečný přístup",
        task="Bezpečně přistup k prvku seznamu.",
        difficulty=1, points=10,
        hints=["try: return seznam[index]\nexcept IndexError: return None"],
        tests=[
            lambda: verify(vyzva_2([1,2,3], 1) == 2, "Index 1 ✓"),
            lambda: verify(vyzva_2([1,2,3], 10) is None, "Out of range → None ✓"),
        ]
    ),
    Challenge(
        title="Vnořený try/except — postupný parsing",
        theory="""Vnořáním try/except můžeš zkoušet více parsovacích strategií:
  try:
      return int(text)
  except ValueError:
      try:
          return float(text)
      except ValueError:
          return None""",
        task="Zkus int, pak float, pak None.",
        difficulty=2, points=15,
        hints=["Vnořený try/except — viz teorie"],
        tests=[
            lambda: verify(vyzva_3("42") == 42, "'42' → 42 ✓"),
            lambda: verify(vyzva_3("3.14") == 3.14, "'3.14' → 3.14 ✓"),
            lambda: verify(vyzva_3("ahoj") is None, "'ahoj' → None ✓"),
        ]
    ),
    Challenge(
        title="Raise — vyhazování výjimek",
        theory="""raise vyhodí výjimku:
  raise ValueError("Špatná hodnota!")
  raise TypeError("Špatný typ!")

Používej raise když vstup nesplňuje podmínky.""",
        task="Validuj věk — raise ValueError pro špatné vstupy.",
        difficulty=2, points=15,
        hints=["if not isinstance(vek, int): raise ValueError(...)"],
        tests=[
            lambda: verify(vyzva_4(25) == True, "Platný věk ✓"),
            lambda: (
                lambda: (vyzva_4("dvacet"), False)[1]  # mělo by vyhodit chybu
            )() if False else
            verify(
                (lambda: (True, None) if _raises(lambda: vyzva_4("dvacet"), ValueError) else (False, None))()[0],
                "String vyhodí ValueError ✓",
                "Měl vyhodit ValueError pro string"
            ),
            lambda: verify(
                _raises(lambda: vyzva_4(-5), ValueError),
                "Záporný věk vyhodí ValueError ✓",
                "Měl vyhodit ValueError pro záporné číslo"
            ),
        ]
    ),
    Challenge(
        title="Vlastní výjimka — Custom Exception",
        theory="""Vlastní výjimky dědí z Exception:
  class MojeChyba(Exception):
      pass

  raise MojeChyba("Něco se pokazilo")

Proč? Lepší popis chyby, snazší zachytávání.""",
        task="Validuj email s vlastní výjimkou NeplatnyEmailError.",
        difficulty=2, points=20,
        hints=["if '@' not in email or '.' not in email: raise NeplatnyEmailError(...)"],
        tests=[
            lambda: verify(vyzva_5("jan@email.cz") == True, "Platný email ✓"),
            lambda: verify(
                _raises(lambda: vyzva_5("spatnyemail"), NeplatnyEmailError),
                "Neplatný email vyhodí chybu ✓"
            ),
        ]
    ),
    Challenge(
        title="Graceful handling — přeskakování chyb",
        theory="""Někdy chceš zpracovat co se dá a chyby přeskočit:
  for item in data:
      try:
          result += item
      except TypeError:
          continue  # přeskoč, pokračuj dál""",
        task="Sečti jen čísla v seznamu, nečíselné prvky přeskoč.",
        difficulty=2, points=15,
        hints=["try: soucet += cislo\nexcept (TypeError, ValueError): continue"],
        tests=[
            lambda: verify(vyzva_6([1, "dva", 3, None, 5]) == 9, "Součet s přeskočením ✓"),
            lambda: verify(vyzva_6([1, 2, 3]) == 6, "Čistý seznam ✓"),
            lambda: verify(vyzva_6(["a", "b"]) == 0, "Samé nečísla → 0 ✓"),
        ]
    ),
]

def _raises(func, exc_type):
    """Pomocná funkce — ověří že funkce vyhodí výjimku."""
    try:
        func()
        return False
    except exc_type:
        return True
    except Exception:
        return False

if __name__ == "__main__":
    run_challenges(challenges, "Python Základy — Error Handling", "01_08")
