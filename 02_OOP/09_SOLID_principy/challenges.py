#!/usr/bin/env python3
"""⚖️ OOP — SOLID Principy: Pět pilířů čistého OOP designu."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

# ----- VÝZVA 1: Single Responsibility Principle (SRP) -----
# Špatně: jedna třída dělá vše
class SpatnyReport:
    """Anti-vzor — nedotýkej se."""
    def __init__(self, data):
        self.data = data

    def generuj(self):
        return f"Report: {self.data}"

    def uloz_do_souboru(self, cesta):
        pass  # ukládání — jiná zodpovědnost!

    def posli_emailem(self, adresa):
        pass  # posílání — další zodpovědnost!


class ReportGenerator:
    """
    🎯 Zodpovědnost POUZE: generovat report.
    - __init__(data)
    - generuj() → "Report: {data}"
    """
    # TODO: ↓
    pass


class ReportSaver:
    """
    🎯 Zodpovědnost POUZE: ukládat reporty.
    - uloz(report_text, cesta) → vrátí "Uloženo do {cesta}"
    """
    # TODO: ↓
    pass


# ----- VÝZVA 2: Open/Closed Principle (OCP) -----
from abc import ABC, abstractmethod

class Sleva(ABC):
    """Abstraktní sleva — neupravuj."""
    @abstractmethod
    def vypocti(self, cena: float) -> float:
        """Vrátí cenu PO slevě."""
        pass

class ZadnaSleva(Sleva):
    """
    🎯 Vrátí cenu beze změny.
    """
    # TODO: ↓
    pass


class ProcentniSleva(Sleva):
    """
    🎯 Sleva v procentech.
    - __init__(procenta) např. 20 = 20%
    - vypocti(cena) → cena * (1 - procenta/100)
    """
    # TODO: ↓
    pass


class FixniSleva(Sleva):
    """
    🎯 Fixní sleva v Kč (ale cena neklesne pod 0).
    - __init__(castka)
    - vypocti(cena) → max(0, cena - castka)
    """
    # TODO: ↓
    pass


def aplikuj_slevu(cena: float, sleva: Sleva) -> float:
    """Tato funkce NEMUSÍ znát typy slev — OCP!"""
    return sleva.vypocti(cena)


# ----- VÝZVA 3: Liskov Substitution Principle (LSP) -----

class Ptak:
    """Základní pták."""
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def jez(self):
        return f"{self.jmeno} jí"


class LetajiciPtak(Ptak):
    """
    🎯 Pták, co umí létat.
    - let() → "{jmeno} letí"
    """
    # TODO: ↓
    pass


class Tucnak(Ptak):
    """
    🎯 Tučňák NEUMÍ létat, ale umí plavat.
    - plav() → "{jmeno} plave"
    ⚠️  NEMÁ mít metodu let()!
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="SRP — Každá třída jednu věc",
        theory="""SOLID — 5 principů čistého OOP kódu:

S — Single Responsibility: třída má JEDNU zodpovědnost
O — Open/Closed: otevřený pro rozšíření, zavřený pro modifikaci
L — Liskov Substitution: potomek nahradí rodiče bez problémů
I — Interface Segregation: malé specifické rozhraní
D — Dependency Inversion: závisej na abstrakci

ŠPATNĚ:
  class Report:
      def generuj(): ...
      def uloz(): ...       # jiná zodpovědnost
      def posli(): ...      # další zodpovědnost

SPRÁVNĚ:
  class ReportGenerator:    # JEDNA zodpovědnost
      def generuj(): ...
  class ReportSaver:        # JEDNA zodpovědnost
      def uloz(): ...""",
        task="Rozděl zodpovědnosti do dvou tříd.",
        difficulty=2, points=25,
        hints=["Každá třída dělá PŘESNĚ jednu věc"],
        tests=[
            lambda: verify(
                ReportGenerator([1, 2, 3]).generuj() == "Report: [1, 2, 3]",
                "ReportGenerator ✓"
            ),
            lambda: verify(
                ReportSaver().uloz("text", "/tmp/r.txt") == "Uloženo do /tmp/r.txt",
                "ReportSaver ✓"
            ),
        ]
    ),
    Challenge(
        title="OCP — Rozšiřuj bez modifikace",
        theory="""Open/Closed: přidej nový typ slevy BEZ úpravy
existujícího kódu.

  def aplikuj_slevu(cena, sleva: Sleva):
      return sleva.vypocti(cena)  # funguje s JAKOUKOLI slevou

Přidání nové slevy = nová podtřída, starý kód se NEMĚNÍ.""",
        task="Implementuj 3 typy slev — žádná, procentní, fixní.",
        difficulty=2, points=30,
        hints=[
            "ZadnaSleva().vypocti(cena) → cena",
            "ProcentniSleva(20).vypocti(100) → 80.0"
        ],
        tests=[
            lambda: verify(aplikuj_slevu(100, ZadnaSleva()) == 100, "Žádná sleva ✓"),
            lambda: verify(aplikuj_slevu(100, ProcentniSleva(20)) == 80.0, "20% sleva ✓"),
            lambda: verify(aplikuj_slevu(50, FixniSleva(30)) == 20, "Fixní 30 Kč ✓"),
            lambda: verify(aplikuj_slevu(10, FixniSleva(50)) == 0, "Fixní nepod 0 ✓"),
        ]
    ),
    Challenge(
        title="LSP — Tučňák není LetajícíPták",
        theory="""Liskov: Potomek MUSÍ být schopen nahradit rodiče.

ŠPATNĚ:
  class Ptak:
      def let(): ...
  class Tucnak(Ptak):
      def let(): raise Error  # 💥 porušení LSP!

SPRÁVNĚ:
  class Ptak: ...              # základní chování
  class LetajiciPtak(Ptak): ...  # přidá let()
  class Tucnak(Ptak): ...       # přidá plav()""",
        task="Tučňák plave, ale NELETÍ. LetajícíPták letí.",
        difficulty=2, points=25,
        hints=["LetajiciPtak dědí z Ptak a přidá let()", "Tucnak NEMÁ let()"],
        tests=[
            lambda: verify(LetajiciPtak("Orel").let() == "Orel letí", "Orel letí ✓"),
            lambda: verify(LetajiciPtak("Orel").jez() == "Orel jí", "Orel jí (LSP) ✓"),
            lambda: verify(Tucnak("Tučňák").plav() == "Tučňák plave", "Tučňák plave ✓"),
            lambda: verify(not hasattr(Tucnak("T"), "let"), "Tučňák NEMÁ let() ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "OOP — SOLID Principy", "02_09")
