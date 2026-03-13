#!/usr/bin/env python3
"""🏗️ OOP — Dataclasses: Méně boilerplate, víc práce."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify
from dataclasses import dataclass, field

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

# 🎯 VÝZVA 1: Vytvoř dataclass Bod3D s atributy x, y, z (float)
# Automaticky dostaneš __init__, __repr__, __eq__

# TODO: ↓ (použij @dataclass)


# 🎯 VÝZVA 2: Dataclass Student s:
# - jmeno: str
# - rocnik: int
# - znamky: list[float] = prázdný list (pozor na mutable default!)
# - metoda prumer() → průměr známek

# TODO: ↓


# 🎯 VÝZVA 3: Frozen (immutable) dataclass Barva
# - r, g, b: int (0-255)
# - metoda hex() → "#RRGGBB" formát

# TODO: ↓ (použij @dataclass(frozen=True))


# 🎯 VÝZVA 4: Dataclass Konfigurace s __post_init__ validací
# - host: str
# - port: int (default 8080)
# - debug: bool (default False)
# __post_init__ musí validovat: port 1-65535, host neprázdný

# TODO: ↓


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Dataclass — rychlé třídy",
        theory="""@dataclass automaticky vytvoří __init__, __repr__, __eq__:
  from dataclasses import dataclass

  @dataclass
  class Bod:
      x: float
      y: float

  b = Bod(1.0, 2.0)    # __init__ automaticky
  print(b)              # Bod(x=1.0, y=2.0)
  b == Bod(1.0, 2.0)    # True — __eq__ automaticky

Ušetří spoustu boilerplate kódu.""",
        task="Vytvoř dataclass Bod3D.",
        difficulty=1, points=15,
        hints=["@dataclass\nclass Bod3D:\n    x: float\n    y: float\n    z: float"],
        tests=[
            lambda: verify(Bod3D(1, 2, 3).x == 1, "Atributy ✓"),
            lambda: verify(Bod3D(1, 2, 3) == Bod3D(1, 2, 3), "__eq__ ✓"),
            lambda: verify("Bod3D" in repr(Bod3D(1, 2, 3)), "__repr__ ✓"),
        ]
    ),
    Challenge(
        title="Dataclass s mutable default",
        theory="""POZOR: Mutable default hodnoty (list, dict) musíš obalit:
  from dataclasses import field

  @dataclass
  class Student:
      jmeno: str
      znamky: list = field(default_factory=list)  # ✓

  # ŠPATNĚ: znamky: list = []  ← sdílený list!""",
        task="Student se známkami a průměrem.",
        difficulty=2, points=20,
        hints=[
            "znamky: list = field(default_factory=list)",
            "def prumer(self): return sum(self.znamky) / len(self.znamky) if self.znamky else 0"
        ],
        tests=[
            lambda: verify(Student("Jan", 2, [1,2,3]).prumer() == 2.0, "Průměr ✓"),
            lambda: verify(Student("Eva", 1).znamky == [], "Prázdné známky ✓"),
            lambda: verify(
                Student("A", 1).znamky is not Student("B", 1).znamky,
                "Nezávislé seznamy ✓"
            ),
        ]
    ),
    Challenge(
        title="Frozen dataclass — immutable",
        theory="""frozen=True činí objekt neměnným:
  @dataclass(frozen=True)
  class Bod:
      x: float
      y: float

  b = Bod(1, 2)
  b.x = 3  # FrozenInstanceError!

Proč? Bezpečnost — jistota že se data nezmění.""",
        task="Frozen dataclass Barva s hex() metodou.",
        difficulty=2, points=20,
        hints=[
            "@dataclass(frozen=True)\nclass Barva:\n    r: int\n    g: int\n    b: int",
            "def hex(self): return f'#{self.r:02x}{self.g:02x}{self.b:02x}'"
        ],
        tests=[
            lambda: verify(Barva(255, 128, 0).hex() == "#ff8000", "hex() ✓"),
            lambda: verify(
                _raises(lambda: setattr(Barva(0,0,0), 'r', 1), Exception),
                "Frozen — nelze změnit ✓"
            ),
        ]
    ),
    Challenge(
        title="__post_init__ validace",
        theory="""__post_init__ se volá po __init__:
  @dataclass
  class Config:
      port: int = 8080

      def __post_init__(self):
          if not (1 <= self.port <= 65535):
              raise ValueError("Neplatný port")

Ideální místo pro validaci.""",
        task="Konfigurace s validací portu a hostu.",
        difficulty=2, points=20,
        hints=["def __post_init__(self): if not self.host: raise ValueError(...)"],
        tests=[
            lambda: verify(Konfigurace("localhost").port == 8080, "Default port ✓"),
            lambda: verify(
                _raises(lambda: Konfigurace("", 8080), ValueError),
                "Prázdný host → ValueError ✓"
            ),
            lambda: verify(
                _raises(lambda: Konfigurace("localhost", 99999), ValueError),
                "Neplatný port → ValueError ✓"
            ),
        ]
    ),
]

def _raises(func, exc_type):
    try: func(); return False
    except exc_type: return True
    except: return False

if __name__ == "__main__":
    run_challenges(challenges, "OOP — Dataclasses", "02_07")
