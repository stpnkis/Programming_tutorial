#!/usr/bin/env python3
"""
🏗️ OOP — Třídy a objekty
Základní stavební jednotka OOP — třída jako šablona, objekt jako instance.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

class Pes:
    """
    🎯 VÝZVA 1: Vytvoř třídu Pes
    Atributy: jmeno (str), vek (int), rasa (str)
    Metoda: stekej() → vrátí "Haf! Jsem {jmeno}!"
    Metoda: info() → vrátí "{jmeno}, {rasa}, {vek} let"
    """
    # TODO: Doplň __init__, stekej() a info() ↓
    pass


class Bankomat:
    """
    🎯 VÝZVA 2: Bankovní účet
    Atributy: majitel (str), zustatek (float, default 0)
    Metoda: vloz(castka) → přidá na účet, vrátí nový zůstatek
    Metoda: vyber(castka) → odebere z účtu, vrátí nový zůstatek
       - Pokud není dost peněz, vrátí "Nedostatek prostředků"
    Metoda: stav() → vrátí "Účet {majitel}: {zustatek} Kč"
    """
    # TODO: Doplň celou třídu ↓
    pass


class Pocitadlo:
    """
    🎯 VÝZVA 3: Třídní (class) vs instanční proměnné
    Třídní proměnná: celkem_kliknuti (sdílená všemi instancemi)
    Instanční proměnná: moje_kliknuti (jen pro tuto instanci)

    Metoda: klikni() → zvýší obě počítadla o 1
    Class method: celkem() → vrátí celkem_kliknuti
    """
    celkem_kliknuti = 0

    # TODO: Doplň __init__, klikni() a celkem() ↓
    pass


class Bod:
    """
    🎯 VÝZVA 4: Třída pro 2D bod
    Atributy: x, y (float)
    Metoda: vzdalenost(other) → euklidovská vzdálenost k jinému bodu
    Metoda: __repr__() → "Bod(x, y)"
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Třída Pes — první OOP",
        theory="""Třída je šablona (blueprint) pro objekty:
  class Pes:
      def __init__(self, jmeno, vek):
          self.jmeno = jmeno   # instanční atribut
          self.vek = vek

      def stekej(self):        # metoda
          return f"Haf! Jsem {self.jmeno}!"

  rex = Pes("Rex", 3)         # vytvoření instance
  rex.stekej()                 # volání metody

self = odkaz na konkrétní instanci.""",
        task="Doplň třídu Pes s __init__, stekej() a info().",
        difficulty=1, points=15,
        hints=[
            "def __init__(self, jmeno, vek, rasa): self.jmeno = jmeno ...",
            "def stekej(self): return f'Haf! Jsem {self.jmeno}!'"
        ],
        tests=[
            lambda: verify(
                Pes("Rex", 3, "labrador").stekej() == "Haf! Jsem Rex!",
                "stekej() ✓"
            ),
            lambda: verify(
                Pes("Rex", 3, "labrador").info() == "Rex, labrador, 3 let",
                "info() ✓"
            ),
        ]
    ),
    Challenge(
        title="Bankomat — stav a metody",
        theory="""Atributy uchovávají stav, metody ho mění:
  class Ucet:
      def __init__(self, zustatek=0):
          self.zustatek = zustatek

      def vloz(self, castka):
          self.zustatek += castka
          return self.zustatek

Metody mohou měnit stav objektu (self.atribut).""",
        task="Bankovní účet s vkládáním a výběrem.",
        difficulty=2, points=20,
        hints=[
            "self.zustatek += castka",
            "if castka > self.zustatek: return 'Nedostatek prostředků'"
        ],
        tests=[
            lambda: verify(
                (lambda b: (b.vloz(1000), b.stav()))(Bankomat("Jan")) == (1000, "Účet Jan: 1000 Kč"),
                "Vklad ✓"
            ),
            lambda: verify(
                (lambda b: (b.vloz(1000), b.vyber(300)))(Bankomat("Jan")) == (1000, 700),
                "Výběr ✓"
            ),
            lambda: verify(
                (lambda b: (b.vloz(100), b.vyber(200)))(Bankomat("Jan")) == (100, "Nedostatek prostředků"),
                "Nedostatek ✓"
            ),
        ]
    ),
    Challenge(
        title="Třídní vs instanční proměnné",
        theory="""Třídní proměnné jsou sdílené:
  class Kocka:
      pocet_kocek = 0           # třídní — stejná pro všechny

      def __init__(self, jmeno):
          self.jmeno = jmeno    # instanční — unikátní
          Kocka.pocet_kocek += 1

  k1 = Kocka("Micka")
  k2 = Kocka("Mourek")
  Kocka.pocet_kocek → 2""",
        task="Počítadlo s třídní a instanční proměnnou.",
        difficulty=2, points=20,
        hints=[
            "def __init__(self): self.moje_kliknuti = 0",
            "@classmethod\ndef celkem(cls): return cls.celkem_kliknuti"
        ],
        tests=[
            lambda: (
                setattr(Pocitadlo, 'celkem_kliknuti', 0),
                (lambda p1, p2: (
                    p1.klikni(), p1.klikni(), p2.klikni(),
                    verify(
                        p1.moje_kliknuti == 2 and p2.moje_kliknuti == 1 and Pocitadlo.celkem() == 3,
                        "Třídní vs instanční ✓",
                        f"p1={p1.moje_kliknuti}, p2={p2.moje_kliknuti}, celkem={Pocitadlo.celkem()}"
                    )
                ))(Pocitadlo(), Pocitadlo())
            )[-1][-1],
        ]
    ),
    Challenge(
        title="Třída Bod — __repr__ a metody",
        theory="""__repr__ definuje jak se objekt zobrazí:
  class Bod:
      def __repr__(self):
          return f"Bod({self.x}, {self.y})"

  print(Bod(1, 2))  → Bod(1, 2)

Vzdálenost: sqrt((x2-x1)² + (y2-y1)²)""",
        task="2D bod s vzdáleností a repr.",
        difficulty=2, points=20,
        hints=[
            "import math; math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)",
            "def __repr__(self): return f'Bod({self.x}, {self.y})'"
        ],
        tests=[
            lambda: verify(repr(Bod(1, 2)) == "Bod(1, 2)", "__repr__ ✓"),
            lambda: verify(
                abs(Bod(0, 0).vzdalenost(Bod(3, 4)) - 5.0) < 0.01,
                "Vzdálenost (0,0)→(3,4) = 5.0 ✓"
            ),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "OOP — Třídy a objekty", "02_01")
