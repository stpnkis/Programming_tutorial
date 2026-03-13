#!/usr/bin/env python3
"""🏗️ OOP — Zapouzdření: Skrývání implementace, kontrola přístupu."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

class Teplomer:
    """
    🎯 VÝZVA 1: Teplomer s property
    - Privátní atribut _teplota (v Celsiech)
    - Property 'teplota' s getterem a setterem
    - Setter validuje: teplota musí být mezi -273.15 a 1000
      pokud ne → raise ValueError
    - Property 'fahrenheit' (jen getter): F = C * 9/5 + 32
    """
    def __init__(self, teplota=20.0):
        # TODO: ↓
        pass

    # TODO: @property teplota, teplota.setter, fahrenheit


class Heslo:
    """
    🎯 VÝZVA 2: Správce hesel
    - Privátní atribut __heslo (name mangling s __)
    - Metoda nastav(nove_heslo): heslo musí mít 8+ znaků a číslo
      pokud ne → raise ValueError s popisem
    - Metoda over(pokus): vrátí True/False
    - Heslo NELZE přečíst přímo! (žádný getter pro raw heslo)
    """
    def __init__(self, heslo):
        # TODO: ↓
        pass

    # TODO: nastav(), over()


class Robot:
    """
    🎯 VÝZVA 3: Robot s read-only properties
    - jmeno (read-only property)
    - _energie (privátní, 0-100)
    - energie (property s getter i setter, validace 0-100)
    - status (read-only): "aktivní" pokud energie > 0, jinak "vypnutý"
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Property — kontrolovaný přístup",
        theory="""Property = getter/setter elegantně:
  class Kruh:
      def __init__(self, r):
          self._r = r        # konvence: _ = privátní

      @property
      def polomer(self):     # getter
          return self._r

      @polomer.setter
      def polomer(self, val):# setter s validací
          if val < 0:
              raise ValueError
          self._r = val

Přístup jako k atributu: k.polomer = 5 (ne k.set_polomer(5))""",
        task="Teploměr s validací a převodem na Fahrenheit.",
        difficulty=2, points=25,
        hints=[
            "@property\ndef teplota(self): return self._teplota",
            "@teplota.setter\ndef teplota(self, val): if -273.15 <= val <= 1000: self._teplota = val else: raise ValueError"
        ],
        tests=[
            lambda: verify(Teplomer(20).teplota == 20, "Getter ✓"),
            lambda: verify(Teplomer(100).fahrenheit == 212.0, "100°C = 212°F ✓"),
            lambda: verify(
                _raises(lambda: Teplomer(-300), ValueError),
                "Validace: -300°C → ValueError ✓"
            ),
            lambda: (
                lambda t: (setattr(t, 'teplota', 50), verify(t.teplota == 50, "Setter ✓"))
            )(Teplomer(20))[1],
        ]
    ),
    Challenge(
        title="Name Mangling — skutečně privátní",
        theory="""Python konvence přístupu:
  self.verejny      # veřejný
  self._chraneny    # chráněný (konvence, ne vynucené)
  self.__privatni   # name mangling → _Trida__privatni

__ (dvojité podtržítko) ztíží přímý přístup.""",
        task="Bezpečný správce hesel s validací.",
        difficulty=3, points=30,
        hints=[
            "Validace: len(heslo) >= 8 and any(c.isdigit() for c in heslo)",
            "self.__heslo = heslo; def over(self, pokus): return pokus == self.__heslo"
        ],
        tests=[
            lambda: verify(Heslo("Secret123").over("Secret123") == True, "Správné heslo ✓"),
            lambda: verify(Heslo("Secret123").over("wrong") == False, "Špatné heslo ✓"),
            lambda: verify(
                _raises(lambda: Heslo("short"), ValueError),
                "Krátké heslo → ValueError ✓"
            ),
            lambda: verify(
                _raises(lambda: Heslo("NoNumbers"), ValueError),
                "Bez čísla → ValueError ✓"
            ),
        ]
    ),
    Challenge(
        title="Read-only a validované properties",
        task="Robot s read-only jménem, validovanou energií a dynamic statusem.",
        difficulty=2, points=20,
        hints=[
            "@property\ndef jmeno(self): return self._jmeno  # bez setteru = read-only",
            "@property\ndef status(self): return 'aktivní' if self._energie > 0 else 'vypnutý'"
        ],
        tests=[
            lambda: verify(Robot("R2D2", 100).jmeno == "R2D2", "Jméno ✓"),
            lambda: verify(Robot("R2D2", 100).status == "aktivní", "Aktivní ✓"),
            lambda: verify(Robot("R2D2", 0).status == "vypnutý", "Vypnutý ✓"),
            lambda: (
                lambda r: (setattr(r, 'energie', 50), verify(r.energie == 50, "Setter energie ✓"))
            )(Robot("R2D2", 100))[1],
        ]
    ),
]

def _raises(func, exc_type):
    try: func(); return False
    except exc_type: return True
    except: return False

if __name__ == "__main__":
    run_challenges(challenges, "OOP — Zapouzdření", "02_04")
