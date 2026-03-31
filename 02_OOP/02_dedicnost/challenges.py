#!/usr/bin/env python3
"""🏗️ OOP — Dědičnost: Znovupoužití kódu pomocí hierarchie tříd."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify
import math

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
    def __init__(self, jmeno, vek, rasa):
        super().__init__(jmeno, vek)
        self.rasa = rasa

    def zvuk(self):
        return "Haf!"

    def aport(self):
        return f"{self.jmeno} přináší míček!"


class Kocka(Zvire):
    """
    🎯 VÝZVA 1b: Další potomek.
    - Přepiš zvuk() → "Mňau!"
    - Přidej metodu pride() → "{jmeno} přišla, když se jí chtělo"
    """
    def __init__(self, jmeno, vek):
        super().__init__(jmeno, vek)

    def zvuk(self):
        return "Mňau!"

    def pride(self):
        return f"{self.jmeno} přišla, když se jí chtělo"


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
    def __init__(self, znacka, rok):
        super().__init__(znacka, rok)
        self.baterie = 100

    def ujed(self, vzdalenost):
        max_km = self.baterie / 0.2
        realne = min(vzdalenost, max_km)
        self.km += realne
        self.baterie -= realne * 0.2

    def nabij(self):
        self.baterie = 100

    def stav(self):
        return f"{self.znacka}: {self.baterie:.0f}% baterie, {self.km:.0f} km"


# ── VÝZVA 3: Trasování dědičnosti ─────────────────────────

class Osoba:
    """Bázová třída pro výzvy 3 a 4."""
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def predstav_se(self):
        return f"Jsem {self.jmeno}"


class Ucitel(Osoba):
    """Pro trasovací výzvu."""
    def __init__(self, jmeno, roky_praxe):
        super().__init__(jmeno)
        self.roky_praxe = roky_praxe

    def predstav_se(self):
        return f"Učitel {self.jmeno} ({self.roky_praxe} let praxe)"


def vyzva_3():
    """
    🎯 TRACE CHALLENGE — Kdo se zavolá?
    Trasuj tento kód krok po kroku:

        u = Ucitel("Jan", 10)
        vysledek = u.predstav_se()
        jmeno = u.jmeno

    Vrať tuple: (vysledek, jmeno)
    """
    u = Ucitel("Jan", 10)
    vysledek = u.predstav_se()
    jmeno = u.jmeno
    return (vysledek, jmeno)


# ── VÝZVA 4: Debugging dědičnosti ─────────────────────────

class Zamestnanec(Osoba):
    """
    🐛 DEBUGGING — Tato třída měla chybu (chybějící super().__init__).
    Oprav ji, aby info() fungovalo správně.
    """
    def __init__(self, jmeno, pozice, plat):
        super().__init__(jmeno)
        self.pozice = pozice
        self.plat = plat

    def info(self):
        return f"{self.jmeno} - {self.pozice} ({self.plat} Kč)"


# ── VÝZVA 5: Tvary — polymorfismus ────────────────────────

class Tvar:
    """Bázová třída pro výzvu 5."""
    def __init__(self, barva="černá"):
        self.barva = barva

    def obsah(self):
        raise NotImplementedError("Potomek musí implementovat obsah()")

    def __repr__(self):
        return f"{self.__class__.__name__}(barva={self.barva})"


class Kruh(Tvar):
    """
    🎯 VÝZVA 5: Kruh dědí z Tvar.
    - Atribut: polomer
    - obsah() → π * r²
    """
    def __init__(self, polomer, barva="černá"):
        super().__init__(barva)
        self.polomer = polomer

    def obsah(self):
        return math.pi * self.polomer ** 2


class Obdelnik(Tvar):
    """
    🎯 VÝZVA 5b: Obdélník dědí z Tvar.
    - Atributy: sirka, vyska
    - obsah() → šířka * výška
    """
    def __init__(self, sirka, vyska, barva="černá"):
        super().__init__(barva)
        self.sirka = sirka
        self.vyska = vyska

    def obsah(self):
        return self.sirka * self.vyska

# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Pes a Kočka — základní dědičnost",
        challenge_type="implementation",
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
            "class Pes(Zvire): definuj __init__ s parametry jmeno, vek, rasa",
            "Zavolej super().__init__(jmeno, vek) pro inicializaci rodiče",
            "self.rasa = rasa pro nový atribut",
            "def zvuk(self): return 'Haf!' pro override"
        ],
        tests=[
            lambda: verify(Pes("Rex", 3, "lab").zvuk() == "Haf!", "Pes štěká ✓"),
            lambda: verify(Pes("Rex", 3, "lab").info() == "Rex, 3 let", "Info ze Zvíře ✓"),
            lambda: verify(Pes("Rex", 3, "lab").aport() == "Rex přináší míček!", "Aport ✓"),
            lambda: verify(isinstance(Pes("Rex", 3, "lab"), Zvire), "Pes je Zvíře ✓"),
            lambda: verify(Kocka("Micka", 5).zvuk() == "Mňau!", "Kočka mňouká ✓"),
            lambda: verify("přišla" in Kocka("Micka", 5).pride(), "Pride ✓"),
        ]
    ),
    Challenge(
        title="Elektromobil — rozšíření rodiče",
        challenge_type="implementation",
        theory="""Rozšíření rodiče:
  class Potomek(Rodic):
      def __init__(self, x, y, z):
          super().__init__(x, y)  # rodičovský init
          self.z = z              # nový atribut

      def metoda(self):
          super().metoda()        # volej rodičovskou verzi
          # + vlastní logika""",
        task="Elektromobil s baterií, omezeným dojezdem a nabíjením.",
        difficulty=3, points=25,
        hints=[
            "super().__init__(znacka, rok); self.baterie = 100",
            "Max km = self.baterie / 0.2; realne = min(vzdalenost, max_km)",
            "self.km += realne; self.baterie -= realne * 0.2",
            "stav() vrátí f'{self.znacka}: {self.baterie:.0f}% baterie, {self.km:.0f} km'"
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
            lambda: (
                lambda e: (e.ujed(500), e.nabij(), verify(
                    e.baterie == 100,
                    "Nabíjení na 100% ✓"
                ))
            )(Elektromobil("Tesla", 2024))[2],
        ]
    ),
    Challenge(
        title="Kdo se zavolá? — trasování dědičnosti",
        challenge_type="trace",
        theory="""Trasování dědičnosti:
  1. Potomek.__init__() se zavolá při vytvoření
  2. super().__init__() zavolá rodičovský init
  3. Metoda se hledá nejdřív v potomku, pak v rodiči (MRO)

  class A:
      def __init__(self): self.x = 1
      def greet(self): return f"A: {self.x}"

  class B(A):
      def __init__(self):
          super().__init__()  # A.__init__() → self.x = 1
          self.y = 2
      def greet(self):
          return f"B: {self.x}, {self.y}"  # override

  b = B()
  b.greet()  # → "B: 1, 2" (B.greet, ne A.greet)""",
        task="""Trasuj kód a vrať tuple (vysledek, jmeno):

    u = Ucitel("Jan", 10)
    vysledek = u.predstav_se()
    jmeno = u.jmeno""",
        difficulty=2, points=20,
        hints=[
            "Ucitel.__init__ volá super().__init__('Jan') → self.jmeno = 'Jan'",
            "Pak self.roky_praxe = 10",
            "u.predstav_se() → override v Ucitel → 'Učitel Jan (10 let praxe)'",
            "u.jmeno → zděděný atribut → 'Jan'",
            "return ('Učitel Jan (10 let praxe)', 'Jan')"
        ],
        tests=[
            lambda: verify(
                vyzva_3() == ("Učitel Jan (10 let praxe)", "Jan"),
                "Trasování správné! ✓",
                f"Očekáváno ('Učitel Jan (10 let praxe)', 'Jan'), dostal {repr(vyzva_3())}"
            ),
        ]
    ),
    Challenge(
        title="Najdi bug v hierarchii",
        challenge_type="debugging",
        theory="""Nejčastější OOP bug: chybějící super().__init__()

❌ BUG:
  class Student(Osoba):
      def __init__(self, jmeno, uni):
          self.uni = uni           # Chybí super().__init__(jmeno)!

  s = Student("Jan", "ČVUT")
  s.uni       # "ČVUT" ✓
  s.jmeno     # AttributeError! ← Bug

✅ OPRAVA:
  class Student(Osoba):
      def __init__(self, jmeno, uni):
          super().__init__(jmeno)  # ← Toto chybělo!
          self.uni = uni""",
        task="""Třída Zamestnanec(Osoba) má bug — chybí super().__init__().
Oprav ji, aby info() vracelo: "Jan - programátor (50000 Kč)".""",
        difficulty=2, points=20,
        hints=[
            "Podívej se na Zamestnanec.__init__ — volá super().__init__()?",
            "Bez super().__init__(jmeno) neexistuje self.jmeno",
            "Přidej super().__init__(jmeno) jako první řádek v __init__",
            "Pak self.pozice a self.plat normálně"
        ],
        tests=[
            lambda: verify(
                Zamestnanec("Jan", "programátor", 50000).info() == "Jan - programátor (50000 Kč)",
                "Zaměstnanec funguje ✓",
                f"Dostal: {repr(Zamestnanec('Jan', 'programátor', 50000).info())}"
            ),
            lambda: verify(
                Zamestnanec("Eva", "designér", 45000).jmeno == "Eva",
                "Zděděný atribut jmeno ✓"
            ),
            lambda: verify(
                isinstance(Zamestnanec("Jan", "prog", 1), Osoba),
                "Zamestnanec je Osoba ✓"
            ),
        ]
    ),
    Challenge(
        title="Tvary — polymorfismus přes dědičnost",
        challenge_type="implementation",
        theory="""Polymorfismus: různé třídy, stejné rozhraní:
  tvary = [Kruh(5), Obdelnik(3, 4)]
  for t in tvary:
      print(t.obsah())  # každý počítá jinak

NotImplementedError nutí potomky implementovat metodu.""",
        task="Kruh a Obdélník implementují obsah().",
        difficulty=2, points=15,
        hints=[
            "Kruh: super().__init__(barva), self.polomer = polomer",
            "Kruh.obsah(): math.pi * self.polomer ** 2",
            "Obdelnik: self.sirka, self.vyska",
            "Obdelnik.obsah(): self.sirka * self.vyska"
        ],
        tests=[
            lambda: verify(
                abs(Kruh(5).obsah() - math.pi * 25) < 0.01,
                "Kruh r=5 ✓"
            ),
            lambda: verify(Obdelnik(3, 4).obsah() == 12, "Obdélník 3×4 ✓"),
            lambda: verify(isinstance(Kruh(5), Tvar), "Kruh je Tvar ✓"),
            lambda: verify(isinstance(Obdelnik(3, 4), Tvar), "Obdélník je Tvar ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "OOP — Dědičnost", "02_02")
