#!/usr/bin/env python3
"""🏗️ OOP — Polymorfismus: Stejné rozhraní, různé chování."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

class Platba:
    """Bázová třída — neupravuj."""
    def zpracuj(self, castka):
        raise NotImplementedError

class Karta(Platba):
    """🎯 zpracuj() → "Platba kartou: {castka} Kč" """
    # TODO: ↓
    pass

class Hotovost(Platba):
    """🎯 zpracuj() → "Platba hotově: {castka} Kč" """
    # TODO: ↓
    pass

class Prevod(Platba):
    """🎯 zpracuj() → "Bankovní převod: {castka} Kč" """
    # TODO: ↓
    pass


def zpracuj_platby(platby, castka):
    """
    🎯 VÝZVA 2: Projdi seznam platebních metod a zavolej zpracuj() na každé.
    Vrať list výsledků. Tohle je polymorfismus v akci!
    """
    # TODO: ↓
    return ...


class Notifikator:
    """Bázová třída — neupravuj."""
    def posli(self, zprava):
        raise NotImplementedError

class EmailNotifikator(Notifikator):
    """🎯 posli() → "EMAIL: {zprava}" """
    # TODO: ↓
    pass

class SMSNotifikator(Notifikator):
    """🎯 posli() → "SMS: {zprava}" """
    # TODO: ↓
    pass

class SlackNotifikator(Notifikator):
    """🎯 posli() → "SLACK: {zprava}" """
    # TODO: ↓
    pass


def upozorni_vsechny(notifikatory, zprava):
    """
    🎯 VÝZVA 4: Pošli zprávu přes všechny notifikátory.
    Vrať list výsledků.
    """
    # TODO: ↓
    return ...


# Duck typing výzva
def vyzva_5_delka(objekt):
    """
    🎯 VÝZVA 5: Duck typing — "Pokud to chodí jako kachna..."
    Vrať délku objektu. Funguje pro string, list, dict, tuple...
    Pokud objekt nemá délku, vrať -1.
    Nepoužívej isinstance! Použij try/except nebo hasattr.
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Platební metody — polymorfní třídy",
        theory="""Polymorfismus = mnoho forem, jedno rozhraní.
Každá třída implementuje stejnou metodu po svém:
  class Pes:   def zvuk(self): return "Haf"
  class Kocka: def zvuk(self): return "Mňau"

Klienta nezajímá JAKÝ objekt, jen že má metodu zvuk().""",
        task="Implementuj 3 platební metody.",
        difficulty=1, points=15,
        hints=["def zpracuj(self, castka): return f'Platba kartou: {castka} Kč'"],
        tests=[
            lambda: verify(Karta().zpracuj(100) == "Platba kartou: 100 Kč", "Karta ✓"),
            lambda: verify(Hotovost().zpracuj(50) == "Platba hotově: 50 Kč", "Hotovost ✓"),
            lambda: verify(Prevod().zpracuj(200) == "Bankovní převod: 200 Kč", "Převod ✓"),
        ]
    ),
    Challenge(
        title="Polymorfismus v akci",
        theory="""Síla polymorfismu: Nový typ = 0 změn ve zbytku kódu.
  platby = [Karta(), Hotovost(), Bitcoin()]  # přidání nového typu
  for p in platby:
      p.zpracuj(100)  # funguje bez úprav!

Toto je Open/Closed princip (SOLID).""",
        task="Zpracuj seznam plateb polymorfně.",
        difficulty=1, points=15,
        hints=["[p.zpracuj(castka) for p in platby]"],
        tests=[
            lambda: verify(
                zpracuj_platby([Karta(), Hotovost(), Prevod()], 100) ==
                ["Platba kartou: 100 Kč", "Platba hotově: 100 Kč", "Bankovní převod: 100 Kč"],
                "Polymorfní zpracování ✓"
            ),
        ]
    ),
    Challenge(
        title="Notifikační systém",
        task="Email, SMS a Slack notifikátory.",
        difficulty=1, points=15,
        hints=["Stejný pattern jako platby"],
        tests=[
            lambda: verify(EmailNotifikator().posli("Test") == "EMAIL: Test", "Email ✓"),
            lambda: verify(SMSNotifikator().posli("Test") == "SMS: Test", "SMS ✓"),
            lambda: verify(
                upozorni_vsechny([EmailNotifikator(), SlackNotifikator()], "Alert") ==
                ["EMAIL: Alert", "SLACK: Alert"],
                "Hromadné upozornění ✓"
            ),
        ]
    ),
    Challenge(
        title="Duck Typing — Pythonický polymorfismus",
        theory="""Python nepoužívá formální interfaces.
Místo toho: Duck Typing.
  "Pokud to chodí jako kachna a kváká jako kachna, je to kachna."
  
  len("ahoj")     # string má __len__
  len([1, 2, 3])  # list má __len__
  len({"a": 1})   # dict má __len__

Nezajímá nás TYP, zajímá nás CO UMÍŠ (jaké metody máš).""",
        task="Vrať délku čehokoliv co má len(), jinak -1.",
        difficulty=2, points=20,
        hints=["try: return len(objekt)\nexcept TypeError: return -1"],
        tests=[
            lambda: verify(vyzva_5_delka("ahoj") == 4, "String ✓"),
            lambda: verify(vyzva_5_delka([1,2,3]) == 3, "List ✓"),
            lambda: verify(vyzva_5_delka(42) == -1, "Int → -1 ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "OOP — Polymorfismus", "02_03")
