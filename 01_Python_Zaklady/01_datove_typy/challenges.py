#!/usr/bin/env python3
"""
🐍 PYTHON ZÁKLADY — Datové typy
Nauč se rozlišovat a pracovat s datovými typy v Pythonu.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ — Edituj kód níže!
# ============================================================

def vyzva_1():
    """
    🎯 Vytvoř proměnné správných typů:
    - cele_cislo: celé číslo 42
    - desetinne: desetinné číslo 3.14
    - text: řetězec "Ahoj"
    - pravda: boolean True
    - nic: hodnota None
    """
    # TODO: Doplň proměnné ↓
    cele_cislo = 42
    desetinne = 3.14
    text = "Ahoj"
    pravda = True
    nic = None

    return cele_cislo, desetinne, text, pravda, nic


def vyzva_2():
    """
    🎯 Převeď mezi typy (type casting):
    - číslo 42 převeď na string
    - string "123" převeď na int
    - string "3.14" převeď na float
    - číslo 0 převeď na bool
    """
    # TODO: Doplň převody ↓
    cislo_jako_text = str(42)     # "42"
    text_jako_cislo = int("123")     # 123
    text_jako_float = float("3.14")       # 3.14
    nula_jako_bool = bool(0)     # False

    return cislo_jako_text, text_jako_cislo, text_jako_float, nula_jako_bool


def vyzva_3():
    """
    🎯 Zjisti typy a pracuj s nimi:
    Vrať seznam typů pro hodnoty: 42, "ahoj", 3.14, True, None, [1,2], (1,2), {1:2}
    Každý typ jako string: "int", "str", "float", "bool", "NoneType", "list", "tuple", "dict"
    """
    hodnoty = [42, "ahoj", 3.14, True, None, [1,2], (1,2), {1:2}]

    # TODO: Pro každou hodnotu zjisti její typ a vrať jako string
    # Hint: type(x).__name__ vrátí název typu jako string
    typy = [type(x).__name__ for x in hodnoty]  # měl by být list stringů

    return typy


def vyzva_4():
    """
    🎯 Aritmetika a operátory:
    Spočítej výsledky pomocí operátorů.
    """
    # TODO: Doplň výsledky ↓
    soucet = 17 + 25           # normální sčítání
    podil = 17 // 5            # 17 děleno 5 (celé číslo, floor division)
    zbytek = 17 % 5            # zbytek po dělení 17 / 5
    mocnina = 2 ** 10          # 2 na 10-tou
    porovnani = 10 >= 10       # je 10 větší nebo rovno 10? (True/False)

    return soucet, podil, zbytek, mocnina, porovnani


def vyzva_5():
    """
    🎯 Bonus: Dynamické typování
    Python je dynamicky typovaný — proměnná může měnit typ.

    Vytvoř proměnnou 'x', která:
    1. Začne jako int 10
    2. Změní se na string "deset"
    3. Změní se na list [10, "deset"]

    Vrať všechny tři verze jako tuple.
    """
    
    x = 10
    verze1 = x

    x = "deset"
    verze2 = x

    x = [10, "deset"]
    verze3 = x

    return verze1, verze2, verze3


# ============================================================
# 🔍 TESTY — Neupravuj kód níže!
# ============================================================

challenges = [
    Challenge(
        title="Vytvoř proměnné správných typů",
        theory="""Python má základní datové typy:
  int    — celá čísla (42, -7, 0)
  float  — desetinná čísla (3.14, -0.5)
  str    — textové řetězce ("ahoj", 'svět')
  bool   — pravdivostní hodnoty (True, False)
  None   — prázdná/žádná hodnota""",
        task="Vytvoř 5 proměnných správných typů (viz docstring funkce).",
        difficulty=1, points=10,
        hints=[
            "Celé číslo je prostě: x = 42",
            "Desetinné číslo má tečku: x = 3.14",
            "None se píše s velkým N: x = None"
        ],
        tests=[
            lambda: verify(
                vyzva_1() == (42, 3.14, "Ahoj", True, None),
                "Všechny typy správně! 🎉",
                f"Očekáváno (42, 3.14, 'Ahoj', True, None), dostal {vyzva_1()}"
            )
        ]
    ),
    Challenge(
        title="Type Casting — převody mezi typy",
        theory="""Typy se dají převádět (castovat):
  str(42)     → "42"
  int("123")  → 123
  float("3.14") → 3.14
  bool(0)     → False, bool(1) → True""",
        task="Převeď hodnoty mezi typy podle zadání.",
        difficulty=1, points=15,
        hints=[
            "str(cislo) převede číslo na text",
            "int(text) převede text na celé číslo",
            "bool(0) je False, bool(cokoliv_jineho) je True"
        ],
        tests=[
            lambda: verify(
                vyzva_2() == ("42", 123, 3.14, False),
                "Převody typů zvládnuty! 🎉",
                f"Očekáváno ('42', 123, 3.14, False), dostal {vyzva_2()}"
            )
        ]
    ),
    Challenge(
        title="Zjisti typy hodnot",
        theory="""Typ zjistíš funkcí type():
  type(42)       → <class 'int'>
  type("ahoj")   → <class 'str'>

Název typu jako string:
  type(42).__name__  → "int" """,
        task="Pro seznam hodnot vrať seznam jejich typů jako stringy.",
        difficulty=2, points=20,
        hints=[
            "Použij list comprehension: [type(x).__name__ for x in hodnoty]",
            "Nebo for cyklus, append do seznamu"
        ],
        tests=[
            lambda: verify(
                vyzva_3() == ["int", "str", "float", "bool", "NoneType", "list", "tuple", "dict"],
                "Všechny typy identifikovány! 🎉",
                f"Očekáváno seznam typů, dostal {vyzva_3()}"
            )
        ]
    ),
    Challenge(
        title="Aritmetika a operátory",
        theory="""Python operátory:
  +  -  *  /     základní aritmetika
  //             celočíselné dělení (floor)
  %              zbytek po dělení (modulo)
  **             mocnina
  ==  !=  <  >  <=  >=   porovnání""",
        task="Doplň výpočty s operátory.",
        difficulty=1, points=15,
        hints=[
            "Floor division: 17 // 5 = 3",
            "Modulo: 17 % 5 = 2",
            "Mocnina: 2 ** 10 = 1024"
        ],
        tests=[
            lambda: verify(
                vyzva_4() == (42, 3, 2, 1024, True),
                "Aritmetika zvládnuta! 🎉",
                f"Očekáváno (42, 3, 2, 1024, True), dostal {vyzva_4()}"
            )
        ]
    ),
    Challenge(
        title="Dynamické typování",
        theory="""Python je dynamicky typovaný jazyk:
  x = 10       # x je int
  x = "deset"  # teď je x str
  x = [1, 2]   # a teď list
Typ proměnné se mění podle přiřazené hodnoty.""",
        task="Proměnná x projde třemi typy — vrať všechny verze.",
        difficulty=1, points=10,
        hints=["Prostě přiřaď x = 10, pak x = 'deset', pak x = [10, 'deset']"],
        tests=[
            lambda: verify(
                vyzva_5() == (10, "deset", [10, "deset"]),
                "Dynamické typování pochopeno! 🎉",
                f"Očekáváno (10, 'deset', [10, 'deset']), dostal {vyzva_5()}"
            )
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, section_name="Python Základy — Datové typy", section_id="01_01")
