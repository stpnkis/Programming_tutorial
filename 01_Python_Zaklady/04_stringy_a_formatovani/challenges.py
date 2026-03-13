#!/usr/bin/env python3
"""
🐍 PYTHON ZÁKLADY — Stringy a formátování
Práce s textem — jeden z nejčastějších úkolů.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def vyzva_1(jmeno, vek):
    """
    🎯 Vrať formátovaný string pomocí f-string:
    "Jmenuju se Jan a je mi 25 let."
    """
    # TODO: Použij f-string ↓
    pass


def vyzva_2(text):
    """
    🎯 Vrať text pozpátku.
    Příklad: "Python" → "nohtyP"
    """
    # TODO: Použij slicing ↓
    pass


def vyzva_3(text):
    """
    🎯 Zjisti jestli je text palindrom (čte se stejně zepředu i zezadu).
    Ignoruj velikost písmen.
    Příklad: "Anna" → True, "Python" → False
    """
    # TODO: ↓
    pass


def vyzva_4(veta):
    """
    🎯 Spočítej počet slov ve větě.
    Příklad: "Ahoj jak se máš" → 4
    """
    # TODO: ↓
    pass


def vyzva_5(text, stary, novy):
    """
    🎯 Nahraď všechny výskyty 'stary' za 'novy' v textu.
    Příklad: ("Hello World", "World", "Python") → "Hello Python"
    """
    # TODO: ↓
    pass


def vyzva_6(data):
    """
    🎯 Zformátuj slovník do tabulkového výstupu.
    data = {"jmeno": "Jan", "vek": 25, "město": "Praha"}
    Výstup:
    jmeno  : Jan
    vek    : 25
    město  : Praha

    Klíče zarovnané doleva na 7 znaků, pak " : " a hodnota.
    Řádky oddělené newline, seřazené abecedně podle klíčů.
    """
    # TODO: ↓
    pass


def vyzva_7(template, **kwargs):
    """
    🎯 Vlastní šablonovací systém:
    Nahraď {klic} v template za hodnotu z kwargs.
    Příklad: ("Ahoj {jmeno}!", jmeno="Jan") → "Ahoj Jan!"
    """
    # TODO: ↓
    pass

# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="F-strings — moderní formátování",
        theory="""F-string je nejčistší způsob formátování v Pythonu:
  name = "Jan"
  age = 25
  f"Jmenuji se {name} a je mi {age} let."

Uvnitř {} může být libovolný výraz:
  f"2 + 2 = {2 + 2}"
  f"Velká: {'ahoj'.upper()}" """,
        task="Vrať formátovaný string s jménem a věkem.",
        difficulty=1, points=10,
        hints=["return f'Jmenuju se {jmeno} a je mi {vek} let.'"],
        tests=[
            lambda: verify(vyzva_1("Jan", 25) == "Jmenuju se Jan a je mi 25 let.", "F-string ✓"),
            lambda: verify(vyzva_1("Eva", 30) == "Jmenuju se Eva a je mi 30 let.", "Další test ✓"),
        ]
    ),
    Challenge(
        title="Slicing — text pozpátku",
        theory="""String slicing: text[start:stop:step]
  "Python"[0:3]   → "Pyt"
  "Python"[::2]   → "Pto" (každý 2. znak)
  "Python"[::-1]  → "nohtyP" (pozpátku!)""",
        task="Otoč text pomocí slicingu.",
        difficulty=1, points=10,
        hints=["return text[::-1]"],
        tests=[
            lambda: verify(vyzva_2("Python") == "nohtyP", "Python → nohtyP ✓"),
            lambda: verify(vyzva_2("abcd") == "dcba", "abcd → dcba ✓"),
        ]
    ),
    Challenge(
        title="Palindrom",
        task="Zjisti jestli je text palindrom (ignoruj velikost písmen).",
        difficulty=2, points=15,
        hints=["lower = text.lower()", "Porovnej s reversed verzí"],
        tests=[
            lambda: verify(vyzva_3("Anna") == True, "'Anna' je palindrom ✓"),
            lambda: verify(vyzva_3("Python") == False, "'Python' není palindrom ✓"),
            lambda: verify(vyzva_3("kayak") == True, "'kayak' je palindrom ✓"),
        ]
    ),
    Challenge(
        title="Počet slov",
        theory=""".split() rozdělí string podle mezer:
  "Ahoj jak se máš".split()  → ["Ahoj", "jak", "se", "máš"]""",
        task="Spočítej slova ve větě.",
        difficulty=1, points=10,
        hints=["return len(veta.split())"],
        tests=[
            lambda: verify(vyzva_4("Ahoj jak se máš") == 4, "4 slova ✓"),
            lambda: verify(vyzva_4("Python") == 1, "1 slovo ✓"),
        ]
    ),
    Challenge(
        title="Nahrazení textu",
        theory=""".replace(old, new) nahradí text:
  "Hello World".replace("World", "Python")  → "Hello Python" """,
        task="Nahraď podřetězec.",
        difficulty=1, points=10,
        hints=["return text.replace(stary, novy)"],
        tests=[
            lambda: verify(vyzva_5("Hello World", "World", "Python") == "Hello Python", "Replace ✓"),
        ]
    ),
    Challenge(
        title="Formátování tabulky",
        theory="""Zarovnání v f-stringu:
  f"{'text':<10}" → "text      " (doleva na 10 znaků)
  f"{'text':>10}" → "      text" (doprava)
  f"{'text':^10}" → "   text   " (na střed)""",
        task="Zformátuj slovník do zarovnané tabulky.",
        difficulty=2, points=20,
        hints=[
            "Pro klíče: f'{klic:<7}'",
            "Seřaď: sorted(data.items())",
            "'\\n'.join(f'{k:<7}: {v}' for k, v in sorted(data.items()))"
        ],
        tests=[
            lambda: verify(
                vyzva_6({"jmeno": "Jan", "vek": 25}) == "jmeno  : Jan\nvek    : 25",
                "Tabulka ✓",
                f"Formát nesedí. Dostal: {repr(vyzva_6({'jmeno': 'Jan', 'vek': 25}))}"
            ),
        ]
    ),
    Challenge(
        title="Vlastní šablonovací systém",
        theory="""V reálném světě často potřebuješ nahrazovat placeholdery.
Django, Jinja, Flask — všechny to dělají.
Teď si to zkusíš sám!""",
        task="Nahraď {klic} v template za hodnoty z kwargs.",
        difficulty=2, points=20,
        hints=[
            "Projdi kwargs a použij replace",
            "for key, val in kwargs.items(): template = template.replace(f'{{{key}}}', str(val))"
        ],
        tests=[
            lambda: verify(
                vyzva_7("Ahoj {jmeno}!", jmeno="Jan") == "Ahoj Jan!",
                "Jednoduché nahrazení ✓"
            ),
            lambda: verify(
                vyzva_7("{a} + {b} = {c}", a=1, b=2, c=3) == "1 + 2 = 3",
                "Více proměnných ✓"
            ),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Python Základy — Stringy a formátování", "01_04")
