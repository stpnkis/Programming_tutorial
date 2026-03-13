#!/usr/bin/env python3
"""🏗️ OOP — Kompozice vs Dědičnost: "Has-a" vs "Is-a"."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

class Motor:
    """Hotová třída — neupravuj."""
    def __init__(self, vykon_kw):
        self.vykon_kw = vykon_kw
        self._nastartovany = False

    def nastartuj(self):
        self._nastartovany = True
        return f"Motor {self.vykon_kw}kW nastartován"

    def vypni(self):
        self._nastartovany = False
        return "Motor vypnut"

    @property
    def bezi(self):
        return self._nastartovany


class GPS:
    """Hotová třída — neupravuj."""
    def __init__(self):
        self._pozice = (0.0, 0.0)

    def nastav_pozici(self, lat, lon):
        self._pozice = (lat, lon)

    @property
    def pozice(self):
        return self._pozice


class Auto:
    """
    🎯 VÝZVA 1: Auto HAS-A Motor a HAS-A GPS (kompozice).
    - __init__(znacka, vykon_kw): vytvoří motor a GPS
    - nastartuj() → deleguje na motor
    - pozice → deleguje na GPS
    - info() → "{znacka}, motor {'běží' / 'stojí'}, pozice: {lat}, {lon}"
    """
    # TODO: ↓
    pass


class Inventory:
    """Hotová třída — neupravuj."""
    def __init__(self):
        self._polozky = {}

    def pridej(self, nazev, pocet=1):
        self._polozky[nazev] = self._polozky.get(nazev, 0) + pocet

    def odeber(self, nazev, pocet=1):
        if nazev in self._polozky:
            self._polozky[nazev] = max(0, self._polozky[nazev] - pocet)
            if self._polozky[nazev] == 0:
                del self._polozky[nazev]

    def pocet(self, nazev):
        return self._polozky.get(nazev, 0)

    @property
    def vsechny(self):
        return dict(self._polozky)


class Postava:
    """
    🎯 VÝZVA 2: RPG postava HAS-A Inventory.
    - jmeno, hp (default 100)
    - inventar: Inventory instance
    - seber(predmet, pocet=1) → přidá do inventáře
    - zahod(predmet, pocet=1) → odebere z inventáře
    - stav() → "{jmeno} (HP: {hp}) — inventář: {dict}"
    """
    # TODO: ↓
    pass


class Logger:
    """Hotová třída."""
    def __init__(self):
        self._zaznamy = []

    def log(self, zprava):
        self._zaznamy.append(zprava)

    @property
    def zaznamy(self):
        return list(self._zaznamy)


class Databaze:
    """
    🎯 VÝZVA 3: Databáze HAS-A Logger.
    - __init__(): prázdný dict _data a Logger
    - uloz(klic, hodnota) → uloží + loguje "ULOŽENO: {klic}"
    - nacti(klic) → vrátí hodnotu + loguje "NAČTENO: {klic}"
    - smaz(klic) → smaže + loguje "SMAZÁNO: {klic}"
    - logy → vrátí záznamy z loggeru
    """
    # TODO: ↓
    pass

# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Auto = Motor + GPS (kompozice)",
        theory="""DĚDIČNOST (Is-A):    Auto IS-A Vozidlo
KOMPOZICE  (Has-A):  Auto HAS-A Motor, Auto HAS-A GPS

Kompozice je flexibilnější:
  class Auto:
      def __init__(self):
          self.motor = Motor(100)    # HAS-A
          self.gps = GPS()           # HAS-A

      def nastartuj(self):
          return self.motor.nastartuj()  # delegace

Pravidlo: PREFERUJ kompozici před dědičností.""",
        task="Auto s motorem a GPS — deleguj na komponenty.",
        difficulty=2, points=25,
        hints=[
            "self.motor = Motor(vykon_kw); self.gps = GPS()",
            "def nastartuj(self): return self.motor.nastartuj()"
        ],
        tests=[
            lambda: verify("nastartován" in Auto("Tesla", 200).nastartuj(), "Nastartování ✓"),
            lambda: verify(Auto("Tesla", 200).pozice == (0.0, 0.0), "GPS pozice ✓"),
            lambda: (
                lambda a: (a.nastartuj(), verify("běží" in a.info(), "Info s běžícím motorem ✓"))
            )(Auto("Tesla", 200))[1],
        ]
    ),
    Challenge(
        title="RPG Postava s inventářem",
        task="Postava která sbírá a zahazuje předměty.",
        difficulty=2, points=25,
        hints=[
            "self.inventar = Inventory()",
            "def seber(self, p, n=1): self.inventar.pridej(p, n)"
        ],
        tests=[
            lambda: (
                lambda p: (p.seber("meč"), p.seber("lektvar", 3),
                    verify(p.inventar.pocet("meč") == 1 and p.inventar.pocet("lektvar") == 3,
                           "Sbírání ✓"))
            )(Postava("Hrdina"))[2],
            lambda: (
                lambda p: (p.seber("šípy", 5), p.zahod("šípy", 2),
                    verify(p.inventar.pocet("šípy") == 3, "Zahazování ✓"))
            )(Postava("Lučištník"))[2],
        ]
    ),
    Challenge(
        title="Databáze s logováním",
        theory="""Kompozice odděluje zodpovědnosti:
  - Databáze → ukládání dat
  - Logger → logování

Každá třída dělá JEDNU věc dobře (Single Responsibility).""",
        task="Databáze která loguje vše co dělá.",
        difficulty=2, points=25,
        hints=["self.logger = Logger(); self.logger.log(f'ULOŽENO: {klic}')"],
        tests=[
            lambda: (
                lambda db: (db.uloz("a", 1), db.nacti("a"), db.smaz("a"),
                    verify(
                        db.logy == ["ULOŽENO: a", "NAČTENO: a", "SMAZÁNO: a"],
                        "Logování operací ✓",
                        f"Logy: {db.logy}"
                    ))
            )(Databaze())[3],
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "OOP — Kompozice vs Dědičnost", "02_08")
