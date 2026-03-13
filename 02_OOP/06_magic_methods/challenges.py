#!/usr/bin/env python3
"""🏗️ OOP — Magic Methods: Přizpůsob chování tříd operátorům a built-in funkcím."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

class Vektor:
    """
    🎯 2D vektor s magic methods.
    - __init__(x, y)
    - __repr__   → "Vektor(x, y)"
    - __add__    → sčítání vektorů: Vektor(1,2) + Vektor(3,4) = Vektor(4,6)
    - __sub__    → odčítání
    - __mul__    → násobení skalárem: Vektor(1,2) * 3 = Vektor(3,6)
    - __eq__     → porovnání: Vektor(1,2) == Vektor(1,2) → True
    - __abs__    → velikost (délka): abs(Vektor(3,4)) = 5.0
    - __len__    → vrátí 2 (2D vektor má 2 složky)
    """
    # TODO: Doplň kompletní třídu ↓
    pass


class Penize:
    """
    🎯 Peněžní částka s měnou.
    - __init__(castka, mena="CZK")
    - __repr__   → "100 CZK"
    - __add__    → sčítání (jen stejná měna! Jinak raise ValueError)
    - __sub__    → odčítání
    - __lt__     → porovnání <
    - __le__     → porovnání <=
    - __bool__   → True pokud castka > 0
    """
    # TODO: ↓
    pass


class FrontaTiskovych:
    """
    🎯 Fronta (FIFO) s magic methods:
    - __init__(): prázdná fronta
    - __len__    → počet úloh
    - __bool__   → True pokud neprázdná
    - __contains__(item) → je item ve frontě?
    - __iter__   → iterace přes položky
    - __repr__   → "Fronta[položka1, položka2, ...]"
    - pridej(item) → přidá na konec
    - dalsi() → odebere z fronty (FIFO) a vrátí, raise IndexError pokud prázdná
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================
import math

challenges = [
    Challenge(
        title="Vektor — aritmetické magic methods",
        theory="""Magic methods přizpůsobují chování:
  __add__(self, other)   → self + other
  __sub__(self, other)   → self - other
  __mul__(self, other)   → self * other
  __eq__(self, other)    → self == other
  __repr__(self)         → repr(self), print(self)
  __abs__(self)          → abs(self)
  __len__(self)          → len(self)

Příklad:
  class Bod:
      def __add__(self, other):
          return Bod(self.x + other.x, self.y + other.y)""",
        task="Implementuj 2D vektor se všemi operátory.",
        difficulty=3, points=30,
        hints=[
            "def __add__(self, other): return Vektor(self.x + other.x, self.y + other.y)",
            "def __abs__(self): return math.sqrt(self.x**2 + self.y**2)"
        ],
        tests=[
            lambda: verify(repr(Vektor(1,2)) == "Vektor(1, 2)", "__repr__ ✓"),
            lambda: verify(Vektor(1,2) + Vektor(3,4) == Vektor(4,6), "__add__ ✓"),
            lambda: verify(Vektor(5,5) - Vektor(2,3) == Vektor(3,2), "__sub__ ✓"),
            lambda: verify(Vektor(1,2) * 3 == Vektor(3,6), "__mul__ ✓"),
            lambda: verify(abs(abs(Vektor(3,4)) - 5.0) < 0.01, "__abs__ ✓"),
            lambda: verify(len(Vektor(1,2)) == 2, "__len__ ✓"),
        ]
    ),
    Challenge(
        title="Peníze — validace a porovnání",
        theory="""__lt__ a __le__ pro porovnávání:
  def __lt__(self, other):   # self < other
      return self.x < other.x

  def __bool__(self):         # bool(self), if self:
      return self.hodnota > 0

Proč? Logický objekt: if penize: "máš peníze" """,
        task="Peněžní třída s kontrolou měny.",
        difficulty=2, points=25,
        hints=[
            "def __add__(self, other): if self.mena != other.mena: raise ValueError",
            "def __bool__(self): return self.castka > 0"
        ],
        tests=[
            lambda: verify(repr(Penize(100)) == "100 CZK", "__repr__ ✓"),
            lambda: verify(repr(Penize(100, "CZK") + Penize(50, "CZK")) == "150 CZK", "__add__ ✓"),
            lambda: verify(
                _raises(lambda: Penize(100, "CZK") + Penize(50, "EUR"), ValueError),
                "Různé měny → ValueError ✓"
            ),
            lambda: verify(Penize(50) < Penize(100), "__lt__ ✓"),
            lambda: verify(bool(Penize(100)) == True, "bool(100) = True ✓"),
            lambda: verify(bool(Penize(0)) == False, "bool(0) = False ✓"),
        ]
    ),
    Challenge(
        title="Fronta — kontejnerová magic methods",
        theory="""Kontejnerové magic methods:
  __len__       → len(obj)
  __contains__  → item in obj
  __iter__      → for item in obj:
  __getitem__   → obj[index]

S těmito se tvá třída chová jako built-in kolekce.""",
        task="Fronta s FIFO chováním a magic methods.",
        difficulty=3, points=30,
        hints=[
            "self._items = []; self._items.append(item); self._items.pop(0)",
            "def __contains__(self, item): return item in self._items"
        ],
        tests=[
            lambda: (
                lambda f: (f.pridej("A"), f.pridej("B"), verify(len(f) == 2, "__len__ ✓"))
            )(FrontaTiskovych())[2],
            lambda: (
                lambda f: (f.pridej("A"), f.pridej("B"), verify(f.dalsi() == "A", "FIFO ✓"))
            )(FrontaTiskovych())[2],
            lambda: (
                lambda f: (f.pridej("X"), verify("X" in f, "__contains__ ✓"))
            )(FrontaTiskovych())[2],
            lambda: (
                lambda f: (f.pridej("A"), f.pridej("B"),
                    verify(list(f) == ["A", "B"], "__iter__ ✓"))
            )(FrontaTiskovych())[2],
        ]
    ),
]

def _raises(func, exc_type):
    try: func(); return False
    except exc_type: return True
    except: return False

if __name__ == "__main__":
    run_challenges(challenges, "OOP — Magic Methods", "02_06")
