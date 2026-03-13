#!/usr/bin/env python3
"""🔧 Refactoring — Zlepšování bez změny chování."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

# 🎯 VÝZVA 1: Extract Function
def spatny_report(data):
    """ŠPATNĚ: jedna velká funkce dělá vše."""
    result = []
    for item in data:
        if item["vek"] >= 18:
            text = f"{item['jmeno']} ({item['vek']})"
            result.append(text)
    total = len(result)
    output = f"Dospělí: {total}\n"
    for r in result:
        output += f"  - {r}\n"
    return output

def filtruj_dospele(data: list) -> list:
    """🎯 Extrahuj: vrať seznam dospělých (věk >= 18)."""
    # TODO: ↓
    pass

def formatuj_osobu(osoba: dict) -> str:
    """🎯 Extrahuj: "Jméno (věk)"."""
    # TODO: ↓
    pass

def generuj_report(data: list) -> str:
    """🎯 Čistý report — použij extrahované funkce."""
    # TODO: ↓
    pass


# 🎯 VÝZVA 2: Replace conditional with polymorphism
def spatna_plocha(tvar: str, **kw) -> float:
    """ŠPATNĚ: if/elif řetěz."""
    if tvar == "kruh":
        return 3.14159 * kw["r"] ** 2
    elif tvar == "ctverec":
        return kw["a"] ** 2
    elif tvar == "obdelnik":
        return kw["a"] * kw["b"]
    raise ValueError(f"Neznámý tvar: {tvar}")

from abc import ABC, abstractmethod

class Tvar(ABC):
    """🎯 Refaktoruj na polymorfismus."""
    @abstractmethod
    def plocha(self) -> float:
        pass

class Kruh(Tvar):
    # TODO: ↓
    pass

class Ctverec(Tvar):
    # TODO: ↓
    pass

class Obdelnik(Tvar):
    # TODO: ↓
    pass


# 🎯 VÝZVA 3: Replace magic numbers
def spatna_kalkulace(cena, mnozstvi):
    """ŠPATNĚ: magic numbers."""
    if mnozstvi > 10:
        return cena * mnozstvi * 0.9   # co je 0.9? 10?
    if cena > 1000:
        return cena * mnozstvi * 0.95  # co je 0.95? 1000?
    return cena * mnozstvi

# 🎯 Refaktoruj:
SLEVA_VELKA_OBJEDNAVKA = 0  # TODO: ↓ 
MIN_MNOZSTVI_PRO_SLEVU = 0  # TODO: ↓
SLEVA_DRAHA_POLOZKA = 0     # TODO: ↓
MIN_CENA_PRO_SLEVU = 0      # TODO: ↓

def cisty_vypocet_ceny(cena: float, mnozstvi: int) -> float:
    """🎯 Použij konstanty místo magic numbers."""
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

test_data = [
    {"jmeno": "Adam", "vek": 25},
    {"jmeno": "Bára", "vek": 15},
    {"jmeno": "Cyril", "vek": 30},
    {"jmeno": "Dana", "vek": 17},
]

challenges = [
    Challenge(
        title="Extract Function",
        theory="""REFAKTORING = zlepšení kódu BEZ změny chování.

EXTRACT FUNCTION: rozděl velkou funkci na menší.
Každá funkce dělá JEDNU věc.

PŘED:    def report(data):
            # 50 řádků mixujících filtrování,
            # formátování a výstup

PO:      def filtruj(data): ...
         def formatuj(osoba): ...
         def report(data):
             osoby = filtruj(data)
             return "\\n".join(formatuj(o) for o in osoby)""",
        task="Rozděl report na filtruj, formatuj, generuj.",
        difficulty=2, points=25,
        hints=[
            "filtruj: [o for o in data if o['vek'] >= 18]",
            "formatuj: f\"{o['jmeno']} ({o['vek']})\""
        ],
        tests=[
            lambda: verify(
                len(filtruj_dospele(test_data)) == 2,
                "Filtrování ✓"
            ),
            lambda: verify(
                formatuj_osobu({"jmeno": "Adam", "vek": 25}) == "Adam (25)",
                "Formátování ✓"
            ),
            lambda: verify(
                "Dospělí: 2" in generuj_report(test_data),
                "Report ✓"
            ),
        ]
    ),
    Challenge(
        title="Polymorfismus místo if/elif",
        theory="""REPLACE CONDITIONAL WITH POLYMORPHISM:

PŘED (smrdí):
  if typ == "a": ...
  elif typ == "b": ...
  elif typ == "c": ...

PO (čisté):
  class A(Base):
      def akce(self): ...
  class B(Base):
      def akce(self): ...

Přidání nového typu = nová třída, NE úprava starého kódu.""",
        task="Refaktoruj tvary na třídy s polymorfismem.",
        difficulty=2, points=25,
        hints=["class Kruh(Tvar): def __init__(self, r): self.r = r"],
        tests=[
            lambda: verify(abs(Kruh(5).plocha() - 78.5398) < 0.1, "Kruh ✓"),
            lambda: verify(Ctverec(4).plocha() == 16, "Čtverec ✓"),
            lambda: verify(Obdelnik(3, 5).plocha() == 15, "Obdélník ✓"),
        ]
    ),
    Challenge(
        title="Magic Numbers → Konstanty",
        theory="""MAGIC NUMBERS = nevysvětlené číselné hodnoty.

ŠPATNĚ: if qty > 10: price *= 0.9
CO JE 10? CO JE 0.9?

SPRÁVNĚ:
  BULK_DISCOUNT = 0.9
  MIN_BULK_QTY = 10
  if qty > MIN_BULK_QTY: price *= BULK_DISCOUNT

Konstanty = dokumentace kódu.""",
        task="Pojmenuj magic numbers a použij v čisté funkci.",
        difficulty=1, points=15,
        hints=["SLEVA_VELKA_OBJEDNAVKA = 0.9; MIN_MNOZSTVI_PRO_SLEVU = 10"],
        tests=[
            lambda: verify(
                cisty_vypocet_ceny(100, 15) == 100 * 15 * 0.9,
                "Velká objednávka ✓"
            ),
            lambda: verify(
                cisty_vypocet_ceny(1500, 1) == 1500 * 1 * 0.95,
                "Drahá položka ✓"
            ),
            lambda: verify(
                cisty_vypocet_ceny(100, 5) == 500,
                "Normální ✓"
            ),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Refactoring", "06_05")
