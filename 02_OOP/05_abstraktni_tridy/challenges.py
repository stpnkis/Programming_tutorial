#!/usr/bin/env python3
"""🏗️ OOP — Abstraktní třídy: Definuj kontrakt, potomci implementují."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify
from abc import ABC, abstractmethod
import math

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

class Senzor(ABC):
    """
    🎯 VÝZVA 1: Abstraktní senzor (je hotový — neupravuj!)
    Potomci MUSÍ implementovat: read() a unit()
    """
    def __init__(self, nazev):
        self.nazev = nazev

    @abstractmethod
    def read(self):
        """Přečti hodnotu ze senzoru."""
        pass

    @abstractmethod
    def unit(self):
        """Vrať jednotku měření."""
        pass

    def report(self):
        return f"{self.nazev}: {self.read()} {self.unit()}"


class TeplotniSenzor(Senzor):
    """🎯 Implementuj read() → 22.5, unit() → "°C" """
    # TODO: ↓
    pass


class VlhkostniSenzor(Senzor):
    """🎯 Implementuj read() → 65, unit() → "%" """
    # TODO: ↓
    pass


class Tvar(ABC):
    """
    🎯 VÝZVA 2: Abstraktní třída pro geometrické tvary.
    Doplň abstraktní metody: obsah() a obvod()
    Konkrétní metoda popis() je hotová.
    """
    # TODO: Definuj abstraktní metody obsah() a obvod() ↓

    def popis(self):
        return f"{self.__class__.__name__}: obsah={self.obsah():.2f}, obvod={self.obvod():.2f}"


class Kruh(Tvar):
    """🎯 Kruh s polomerem. obsah = π*r², obvod = 2*π*r"""
    # TODO: ↓
    pass


class Ctverec(Tvar):
    """🎯 Čtverec se stranou. obsah = a², obvod = 4*a"""
    # TODO: ↓
    pass


class Trojuhelnik(Tvar):
    """🎯 Trojúhelník se 3 stranami. obsah = Heronův vzorec, obvod = a+b+c"""
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Abstraktní senzor — kontrakt",
        theory="""Abstraktní třída (ABC) definuje rozhraní:
  from abc import ABC, abstractmethod

  class Senzor(ABC):
      @abstractmethod
      def read(self):  # MUSÍ být implementováno
          pass

  s = Senzor()  # TypeError! Nelze vytvořit instanci ABC.

Abstraktní třída = smlouva: "každý senzor MUSÍ umět read()".""",
        task="Implementuj TeplotniSenzor a VlhkostniSenzor.",
        difficulty=2, points=20,
        hints=[
            "class TeplotniSenzor(Senzor): def __init__(self): super().__init__('Teplota')",
            "def read(self): return 22.5; def unit(self): return '°C'"
        ],
        tests=[
            lambda: verify(TeplotniSenzor().read() == 22.5, "Teplota read ✓"),
            lambda: verify(TeplotniSenzor().unit() == "°C", "Teplota unit ✓"),
            lambda: verify("22.5 °C" in TeplotniSenzor().report(), "Report ✓"),
            lambda: verify(VlhkostniSenzor().read() == 65, "Vlhkost read ✓"),
            lambda: verify(
                _raises(lambda: Senzor("test"), TypeError),
                "Senzor() nelze vytvořit přímo ✓"
            ),
        ]
    ),
    Challenge(
        title="Geometrické tvary — abstraktní hierarchie",
        theory="""Heronův vzorec pro obsah trojúhelníku:
  s = (a + b + c) / 2
  obsah = sqrt(s * (s-a) * (s-b) * (s-c))

Abstrakce vynucuje: KAŽDÝ tvar MUSÍ umět obsah() a obvod().""",
        task="Kruh, Čtverec a Trojúhelník — implementuj obsah() a obvod().",
        difficulty=2, points=30,
        hints=[
            "Kruh: math.pi * self.r ** 2, 2 * math.pi * self.r",
            "Čtverec: self.a ** 2, 4 * self.a",
            "Heron: s = (a+b+c)/2; sqrt(s*(s-a)*(s-b)*(s-c))"
        ],
        tests=[
            lambda: verify(abs(Kruh(5).obsah() - 78.54) < 0.1, "Kruh obsah ✓"),
            lambda: verify(abs(Kruh(5).obvod() - 31.42) < 0.1, "Kruh obvod ✓"),
            lambda: verify(Ctverec(4).obsah() == 16, "Čtverec obsah ✓"),
            lambda: verify(Ctverec(4).obvod() == 16, "Čtverec obvod ✓"),
            lambda: verify(abs(Trojuhelnik(3,4,5).obsah() - 6.0) < 0.01, "Trojúhelník 3-4-5 ✓"),
            lambda: verify("popis" in dir(Kruh(1)), "popis() zděděn z Tvar ✓"),
        ]
    ),
]

def _raises(func, exc_type):
    try: func(); return False
    except exc_type: return True
    except: return False

if __name__ == "__main__":
    run_challenges(challenges, "OOP — Abstraktní třídy", "02_05")
