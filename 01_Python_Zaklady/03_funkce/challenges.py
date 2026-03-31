#!/usr/bin/env python3
"""
🐍 PYTHON ZÁKLADY — Funkce
Základní stavební blok programů. Rozděl a panuj.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def vyzva_1(a, b):
    """
    🎯 Napiš funkci, která vrátí větší ze dvou čísel.
    Pokud jsou stejná, vrať libovolné z nich.
    """
    return max(a,b)


def vyzva_2(text, n=2):
    """
    🎯 Vrať text opakovaný n-krát s mezerou mezi.
    Default n=2.
    Příklad: ("ha", 3) → "ha ha ha"
    """
    return" ".join([text]*n)


def vyzva_3(*args):
    """
    🎯 Funkce přijímá libovolný počet čísel (*args)
    a vrátí jejich průměr.
    Příklad: (10, 20, 30) → 20.0
    Pokud nejsou žádné argumenty, vrať 0.
    """
    if not args:
        return 0
    return sum(args)/len(args)



def vyzva_4(**kwargs):
    """
    🎯 Funkce přijímá libovolné keyword argumenty (**kwargs)
    a vrátí string ve formátu "klic=hodnota" oddělené čárkou.
    Příklad: (jmeno="Jan", vek=25) → "jmeno=Jan, vek=25"
    Seřaď klíče abecedně.
    """

    return ", ".join(f"{k}={v}" for k in sorted(kwargs) for v in [kwargs[k]])   

def vyzva_5():
    """
    🎯 Vytvoř lambda funkci, která zdvojnásobí číslo.
    Vrať tu lambda funkci.
    Příklad: result(5) → 10
    """
    return lambda x:x*2
    


def vyzva_6(func, seznam):
    """
    🎯 Aplikuj funkci 'func' na každý prvek seznamu a vrať nový seznam.
    Toto je vlastní implementace map().
    Příklad: (lambda x: x*2, [1,2,3]) → [2,4,6]
    """
    # TODO: ↓
    pass


def vyzva_7():
    """
    🎯 Vytvoř funkci make_counter(), která vrátí funkci.
    Každé zavolání vrácené funkce vrátí o 1 vyšší číslo.
    (Toto je closure — funkce "pamatuje" svůj stav.)

    Příklad:
        counter = make_counter()
        counter() → 1
        counter() → 2
        counter() → 3
    """
    # TODO: Doplň make_counter ↓
    def make_counter():
        pass

    return make_counter


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Funkce s return — maximum",
        theory="""Funkce je pojmenovaný blok kódu:
  def nazev(parametry):
      '''Docstring'''
      return vysledek
Klíčové: funkce VRACÍ hodnotu pomocí return.""",
        task="Vrať větší ze dvou čísel.",
        difficulty=1, points=10,
        hints=["if a > b: return a", "Nebo: return max(a, b)"],
        tests=[
            lambda: verify(vyzva_1(3, 7) == 7, "max(3,7) = 7 ✓"),
            lambda: verify(vyzva_1(10, 2) == 10, "max(10,2) = 10 ✓"),
            lambda: verify(vyzva_1(5, 5) == 5, "max(5,5) = 5 ✓"),
        ]
    ),
    Challenge(
        title="Default parametry",
        theory="""Parametry mohou mít výchozí (default) hodnoty:
  def pozdrav(jmeno, pozdrav="Ahoj"):
      return f"{pozdrav}, {jmeno}!"
  pozdrav("Jan")         → "Ahoj, Jan!"
  pozdrav("Jan", "Čau")  → "Čau, Jan!" """,
        task="Opakuj text n-krát (default 2) s mezerami.",
        difficulty=1, points=10,
        hints=["' '.join([text] * n)", "Nebo: return (text + ' ') * n — ale pozor na trailing space"],
        tests=[
            lambda: verify(vyzva_2("ha", 3) == "ha ha ha", "('ha', 3) → 'ha ha ha' ✓"),
            lambda: verify(vyzva_2("ho") == "ho ho", "('ho') → 'ho ho' (default n=2) ✓"),
            lambda: verify(vyzva_2("x", 1) == "x", "('x', 1) → 'x' ✓"),
        ]
    ),
    Challenge(
        title="*args — variabilní argumenty",
        theory="""*args zachytí libovolný počet pozičních argumentů jako tuple:
  def soucet(*args):
      return sum(args)
  soucet(1, 2, 3)  → 6""",
        task="Vrať průměr libovolného počtu čísel.",
        difficulty=2, points=15,
        hints=["Průměr = sum(args) / len(args)", "Nezapomeň ošetřit prázdné args"],
        tests=[
            lambda: verify(vyzva_3(10, 20, 30) == 20.0, "průměr(10,20,30) = 20 ✓"),
            lambda: verify(vyzva_3(5) == 5.0, "průměr(5) = 5 ✓"),
            lambda: verify(vyzva_3() == 0, "průměr() = 0 ✓"),
        ]
    ),
    Challenge(
        title="**kwargs — keyword argumenty",
        theory="""**kwargs zachytí keyword argumenty jako dict:
  def info(**kwargs):
      for k, v in kwargs.items():
          print(f"{k}: {v}")
  info(jmeno="Jan", vek=25)""",
        task="Vrať 'klic=hodnota' string z kwargs, seřazený abecedně.",
        difficulty=2, points=15,
        hints=[
            "sorted(kwargs.items()) seřadí podle klíčů",
            "', '.join(f'{k}={v}' for k, v in sorted(kwargs.items()))"
        ],
        tests=[
            lambda: verify(vyzva_4(jmeno="Jan", vek=25) == "jmeno=Jan, vek=25", "kwargs správně ✓"),
            lambda: verify(vyzva_4(a=1) == "a=1", "jeden kwarg ✓"),
        ]
    ),
    Challenge(
        title="Lambda funkce",
        theory="""Lambda je anonymní jednořádková funkce:
  double = lambda x: x * 2
  double(5)  → 10

Je to zkratka za:
  def double(x):
      return x * 2""",
        task="Vrať lambda funkci, která zdvojnásobí číslo.",
        difficulty=1, points=10,
        hints=["return lambda x: x * 2"],
        tests=[
            lambda: verify(callable(vyzva_5()), "Je to funkce ✓"),
            lambda: verify(vyzva_5()(5) == 10, "double(5) = 10 ✓"),
            lambda: verify(vyzva_5()(0) == 0, "double(0) = 0 ✓"),
        ]
    ),
    Challenge(
        title="Funkce jako argument (Higher-Order)",
        theory="""V Pythonu jsou funkce first-class objekty:
  - Můžeš je přiřadit do proměnné
  - Předat jako argument jiné funkci
  - Vrátit z funkce
To je základ funkcionálního programování.""",
        task="Implementuj vlastní map() — aplikuj funkci na každý prvek.",
        difficulty=2, points=15,
        hints=["return [func(x) for x in seznam]"],
        tests=[
            lambda: verify(vyzva_6(lambda x: x*2, [1,2,3]) == [2,4,6], "double [1,2,3] ✓"),
            lambda: verify(vyzva_6(str, [1,2,3]) == ["1","2","3"], "str [1,2,3] ✓"),
            lambda: verify(vyzva_6(lambda x: x**2, [3,4]) == [9,16], "square [3,4] ✓"),
        ]
    ),
    Challenge(
        title="Closure — funkce s pamětí",
        theory="""Closure je funkce, která si pamatuje proměnné z vnějšího scope:
  def make_multiplier(n):
      def multiply(x):
          return x * n   # 'n' je z vnějšího scope
      return multiply

  double = make_multiplier(2)
  double(5)  → 10

Proč je to užitečné? Můžeš vytvářet specializované funkce.""",
        task="Vytvoř make_counter() — closure, která počítá volání.",
        difficulty=3, points=25,
        hints=[
            "Potřebuješ proměnnou count a vnitřní funkci",
            "V Pythonu 3: použij nonlocal count uvnitř vnitřní funkce",
            "def make_counter():\n    count = [0]\n    def counter():\n        count[0] += 1\n        return count[0]\n    return counter"
        ],
        tests=[
            lambda: (
                verify(True, "make_counter existuje ✓")
                if callable(vyzva_7())
                else verify(False, "make_counter musí vracet funkci")
            ),
            lambda: (
                lambda mk: (
                    lambda c: verify(
                        c() == 1 and c() == 2 and c() == 3,
                        "Counter počítá 1, 2, 3 ✓",
                        "Counter musí počítat nahoru od 1"
                    )
                )(mk())
            )(vyzva_7()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Python Základy — Funkce", "01_03")
