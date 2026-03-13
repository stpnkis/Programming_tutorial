#!/usr/bin/env python3
"""🏗️ OOP — Dědičnost: Znovupoužití kódu pomocí hierarchie tříd."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

class Zvire:
    """Bázová třída — TATO JE HOTOVÁ, neupravuj."""
    def __init__(self, jmeno, vek):
        self.jmeno = jmeno
        self.vek = vek

    def zvuk(self):
        return "..."

    def info(self):
        return f"{self.jmeno}, {self.vek} let"


class Pes(Zvire):
    """
    🎯 VÝZVA 1: Zdědí ze Zvire.
    - Přidej atribut 'rasa' (navíc k jmeno a vek)
    - Přepiš zvuk() → "Haf!"
    - Přidej metodu aport() → "{jmeno} přináší míček!"
    """
    # TODO: ↓
    pass


class Kocka(Zvire):
    """
    🎯 VÝZVA 1b: Další potomek.
    - Přepiš zvuk() → "Mňau!"
    - Přidej metodu pride() → "{jmeno} přišla, když se jí chtělo"
    """
    # TODO: ↓
    pass


class Vozidlo:
    """Bázová třída pro výzvu 2."""
    def __init__(self, znacka, rok):
        self.znacka = znacka
        self.rok = rok
        self.km = 0

    def ujed(self, vzdalenost):
        self.km += vzdalenost

    def __repr__(self):
        return f"{self.znacka} ({self.rok}), {self.km} km"


class Elektromobil(Vozidlo):
    """
    🎯 VÝZVA 2: Elektromobil dědí z Vozidla.
    - Přidej atribut baterie (int, %) — default 100
    - Přepiš ujed(): za každý km se vybije 0.2%.
      Pokud nemá dost baterie, ujede jen co může.
    - Přidej metodu nabij() → nastaví baterii na 100%
    - Přidej metodu stav() → "{znacka}: {baterie}% baterie, {km} km"
    """
    # TODO: ↓
    pass


class Tvar:
    """Bázová třída pro výzvu 3."""
    def __init__(self, barva="černá"):
        self.barva = barva

    def obsah(self):
        raise NotImplementedError("Potomek musí implementovat obsah()")

    def __repr__(self):
        return f"{self.__class__.__name__}(barva={self.barva})"


class Kruh(Tvar):
    """
    🎯 VÝZVA 3: Kruh dědí z Tvar.
    - Atribut: polomer
    - obsah() → π * r²
    """
    # TODO: ↓
    pass


class Obdelnik(Tvar):
    """
    🎯 VÝZVA 3b: Obdélník dědí z Tvar.
    - Atributy: sirka, vyska
    - obsah() → šířka * výška
    """
    # TODO: ↓
    pass

# ============================================================
# 🔍 TESTY
# ============================================================

import math

challenges = [
    Challenge(
        title="Dědičnost — Pes a Kočka ze Zvířete",
        theory="""Dědičnost: potomek přebírá vše od rodiče:
  class Rodic:
      def metoda(self): return "rodič"

  class Potomek(Rodic):      # dědí z Rodic
      def metoda(self):       # přepisuje (override)
          return "potomek"

  super().__init__(...)       # volá rodičovský __init__""",
        task="Pes a Kočka dědí ze Zvíře a přidávají vlastní metody.",
        difficulty=2, points=20,
        hints=[
            "class Pes(Zvire): def __init__(self, jmeno, vek, rasa): super().__init__(jmeno, vek)",
            "self.rasa = rasa"
        ],
        tests=[
            lambda: verify(Pes("Rex", 3, "lab").zvuk() == "Haf!", "Pes štěká ✓"),
            lambda: verify(Pes("Rex", 3, "lab").info() == "Rex, 3 let", "Info ze Zvíře ✓"),
            lambda: verify(Pes("Rex", 3, "lab").aport() == "Rex přináší míček!", "Aport ✓"),
            lambda: verify(Kocka("Micka", 5).zvuk() == "Mňau!", "Kočka mňouká ✓"),
            lambda: verify("přišla" in Kocka("Micka", 5).pride(), "Pride ✓"),
        ]
    ),
    Challenge(
        title="Elektromobil — rozšíření rodiče",
        theory="""Rozšíření rodiče:
  class Potomek(Rodic):
      def __init__(self, x, y, z):
          super().__init__(x, y)  # rodičovský init
          self.z = z              # nový atribut

      def metoda(self):
          super().metoda()        # volej rodičovskou verzi
          # + vlastní logika""",
        task="Elektromobil s baterií, omezeným dojezdem a nabíjením.",
        difficulty=3, points=30,
        hints=[
            "super().__init__(znacka, rok); self.baterie = 100",
            "Max km = self.baterie / 0.2; realne = min(vzdalenost, max_km)",
            "self.km += realne; self.baterie -= realne * 0.2"
        ],
        tests=[
            lambda: verify(
                Elektromobil("Tesla", 2024).stav() == "Tesla: 100% baterie, 0 km",
                "Nové auto ✓"
            ),
            lambda: (
                lambda e: (e.ujed(100), verify(
                    abs(e.baterie - 80) < 0.01 and e.km == 100,
                    "Po 100 km: 80% baterie ✓",
                    f"baterie={e.baterie}, km={e.km}"
                ))
            )(Elektromobil("Tesla", 2024))[1],
            lambda: (
                lambda e: (e.ujed(600), verify(
                    e.km == 500 and abs(e.baterie) < 0.01,
                    "Omezený dojezd — ujel max 500 km ✓",
                    f"km={e.km}, bat={e.baterie}"
                ))
            )(Elektromobil("Tesla", 2024))[1],
        ]
    ),
    Challenge(
        title="Tvary — polymorfismus přes dědičnost",
        theory="""Polymorfismus: různé třídy, stejné rozhraní:
  tvary = [Kruh(5), Obdelnik(3, 4)]
  for t in tvary:
      print(t.obsah())  # každý počítá jinak

NotImplementedError nutí potomky implementovat metodu.""",
        task="Kruh a Obdélník implementují obsah().",
        difficulty=2, points=20,
        hints=[
            "math.pi * self.polomer ** 2",
            "self.sirka * self.vyska"
        ],
        tests=[
            lambda: verify(
                abs(Kruh(5).obsah() - math.pi * 25) < 0.01,
                "Kruh r=5 ✓"
            ),
            lambda: verify(Obdelnik(3, 4).obsah() == 12, "Obdélník 3×4 ✓"),
            lambda: verify(isinstance(Kruh(5), Tvar), "Kruh je Tvar ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "OOP — Dědičnost", "02_02")
