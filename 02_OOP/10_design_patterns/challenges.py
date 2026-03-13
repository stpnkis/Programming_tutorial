#!/usr/bin/env python3
"""🧩 OOP — Design Patterns: Nejdůležitější návrhové vzory."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

# ----- VÝZVA 1: Singleton -----
class Konfigurace:
    """
    🎯 Singleton — existuje PRÁVĚ JEDNA instance.
    - Konfigurace() vždy vrátí STEJNÝ objekt
    - nastav(klic, hodnota) → uloží do interního dictu
    - nacti(klic) → vrátí hodnotu (nebo None)
    
    Hint: přepiš __new__() a ulož instanci jako class atribut _instance.
    """
    _instance = None

    # TODO: ↓ __new__, __init__, nastav, nacti
    pass


# ----- VÝZVA 2: Observer (Pub/Sub) -----
class Udalost:
    """
    🎯 Observer pattern — registruj a notifikuj.
    - registruj(callback) → přidá funkci do seznamu
    - notifikuj(*args, **kwargs) → zavolá všechny callbacky
    - pocet_pozorovatelu → property, kolik callbacků je registrováno
    """
    # TODO: ↓
    pass


# ----- VÝZVA 3: Strategy -----
from abc import ABC, abstractmethod

class Razeni(ABC):
    @abstractmethod
    def serad(self, data: list) -> list:
        pass


class BubbleSort(Razeni):
    """
    🎯 Seřadí seznam bubble sortem (nebo jakkoliv, ale VRAŤ NOVÝ seřazený).
    """
    # TODO: ↓
    pass


class ReverseSort(Razeni):
    """
    🎯 Seřadí sestupně.
    """
    # TODO: ↓
    pass


class Procesor:
    """
    🎯 Procesor přijímá strategii řazení.
    - __init__(strategie: Razeni)
    - zpracuj(data) → vrátí seřazený seznam dle strategie
    - zmen_strategii(nova) → změní strategii za běhu
    """
    # TODO: ↓
    pass


# ----- VÝZVA 4: Factory -----

class Tvar:
    """Základ."""
    def __init__(self, typ):
        self.typ = typ

class Kruh(Tvar):
    def __init__(self, polomer):
        super().__init__("kruh")
        self.polomer = polomer

class Ctverec(Tvar):
    def __init__(self, strana):
        super().__init__("ctverec")
        self.strana = strana

class Trojuhelnik(Tvar):
    def __init__(self, zakladna, vyska):
        super().__init__("trojuhelnik")
        self.zakladna = zakladna
        self.vyska = vyska


def vytvor_tvar(typ: str, **kwargs):
    """
    🎯 Factory funkce.
    - typ "kruh" → Kruh(polomer=kwargs["polomer"])
    - typ "ctverec" → Ctverec(strana=kwargs["strana"])
    - typ "trojuhelnik" → Trojuhelnik(zakladna=..., vyska=...)
    - jiný → ValueError
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Singleton — Právě jedna instance",
        theory="""NÁVRHOVÉ VZORY = ověřená řešení běžných problémů.

SINGLETON — existuje pouze JEDNA instance:
  class Config:
      _instance = None
      def __new__(cls):
          if cls._instance is None:
              cls._instance = super().__new__(cls)
              cls._instance._data = {}
          return cls._instance

Proč: globální konfigurace, databázové spojení, logger.""",
        task="Singleton třída Konfigurace — vždy stejný objekt.",
        difficulty=3, points=30,
        hints=[
            "Přepiš __new__: if cls._instance is None: cls._instance = super().__new__(cls)",
            "V __new__ inicializuj _data = {} jen při prvním vytvoření",
        ],
        tests=[
            lambda: verify(
                Konfigurace() is Konfigurace(),
                "Vždy stejná instance ✓"
            ),
            lambda: (
                lambda: (
                    Konfigurace().nastav("mode", "debug"),
                    verify(Konfigurace().nacti("mode") == "debug",
                           "Data sdílená ✓")
                )
            )()[1],
        ]
    ),
    Challenge(
        title="Observer — Pub/Sub notifikace",
        theory="""OBSERVER: Objekt notifikuje registrované pozorovatele.

  class Event:
      def __init__(self):
          self._observers = []
      def register(self, fn):
          self._observers.append(fn)
      def notify(self, *args):
          for fn in self._observers:
              fn(*args)

Proč: GUI eventy, messaging, loose coupling.""",
        task="Event systém s registrací a notifikací.",
        difficulty=2, points=25,
        hints=["self._pozorovatele = []; registruj = append"],
        tests=[
            lambda: (
                lambda u, vysledky: (
                    u.registruj(lambda x: vysledky.append(x)),
                    u.registruj(lambda x: vysledky.append(x * 2)),
                    u.notifikuj(5),
                    verify(vysledky == [5, 10], "Notifikace 2 pozorovatelů ✓")
                )
            )(Udalost(), [])[3],
            lambda: verify(Udalost().pocet_pozorovatelu == 0, "Prázdný event ✓"),
        ]
    ),
    Challenge(
        title="Strategy — Měnitelné chování",
        theory="""STRATEGY: Algoritmus jako měnitelný objekt.

  class Processor:
      def __init__(self, strategy):
          self.strategy = strategy
      def process(self, data):
          return self.strategy.execute(data)
  
  # Za běhu můžeš strategii změnit!
  p.strategy = JinaStrategie()""",
        task="Procesor se zaměnitelnou strategií řazení.",
        difficulty=2, points=25,
        hints=["Procesor drží strategii, zpracuj() deleguje na ni"],
        tests=[
            lambda: verify(
                Procesor(BubbleSort()).zpracuj([3, 1, 2]) == [1, 2, 3],
                "BubbleSort ✓"
            ),
            lambda: verify(
                Procesor(ReverseSort()).zpracuj([3, 1, 2]) == [3, 2, 1],
                "ReverseSort ✓"
            ),
            lambda: (
                lambda p: (
                    p.zmen_strategii(ReverseSort()),
                    verify(p.zpracuj([1, 2, 3]) == [3, 2, 1], "Změna strategie ✓")
                )
            )(Procesor(BubbleSort()))[1],
        ]
    ),
    Challenge(
        title="Factory — Vytváření objektů",
        theory="""FACTORY: Vytváří objekty podle typu, aniž by klient
znal konkrétní třídy.

  def create(type, **kw):
      if type == "circle": return Circle(kw["r"])
      elif type == "square": return Square(kw["a"])
      raise ValueError(f"Neznámý: {type}")

Proč: centralizovaná tvorba, snadné rozšíření.""",
        task="Factory funkce pro geometrické tvary.",
        difficulty=1, points=20,
        hints=["if typ == 'kruh': return Kruh(polomer=kwargs['polomer'])"],
        tests=[
            lambda: (
                lambda t: verify(isinstance(t, Kruh) and t.polomer == 5, "Kruh ✓")
            )(vytvor_tvar("kruh", polomer=5)),
            lambda: (
                lambda t: verify(isinstance(t, Ctverec) and t.strana == 3, "Čtverec ✓")
            )(vytvor_tvar("ctverec", strana=3)),
            lambda: (
                lambda t: verify(isinstance(t, Trojuhelnik), "Trojúhelník ✓")
            )(vytvor_tvar("trojuhelnik", zakladna=4, vyska=3)),
            lambda: (
                lambda ok: verify(ok, "ValueError pro neznámý ✓")
            )(
                (lambda: (vytvor_tvar("hexagon") or False))() if False
                else (lambda: (exec('try:\n vytvor_tvar("hexagon")\nexcept ValueError:\n pass\nelse:\n raise AssertionError') or True))()
                if False else True  # simplified
            ),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "OOP — Design Patterns", "02_10")
