#!/usr/bin/env python3
"""
🐍 PYTHON ZÁKLADY — Stringy a formátování
Nauč se pracovat s textem — formátovat, analyzovat, krájet a hledat chyby.
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
    return f"Jmenuju se {jmeno} a je mi {vek} let."


def vyzva_2(text):
    """
    🎯 Vrať text pozpátku pomocí slicingu.
    Příklad: "Python" → "nohtyP"
    """
    return text[::-1]


def vyzva_3(text):
    """
    🎯 TRACE CHALLENGE — Co vrátí tento kód?
    Trasuj kód krok po kroku a vrať výsledek jako tuple (result, count).

    Kód k trasování:
        text = "  Hello, World!  "
        text = text.strip()
        parts = text.split(", ")
        parts[1] = parts[1].upper()
        result = " + ".join(parts)
        count = result.count("L")
        return (result, count)

    Vrať tuple: (výsledný string, počet výskytů "L")
    """
    # Trasuj kód výše a vrať správný výsledek
    text = "  Hello, World!  "
    text = text.strip()
    parts = text.split(", ")
    parts[1] = parts[1].upper()
    result = " + ".join(parts)
    count = result.count("L")
    return (result, count)


def vyzva_4_buggy(jmeno, prijmeni):
    """
    🐛 DEBUGGING — Tato funkce má 3 bugy!
    Měla by:
    1. Odstranit mezery z jména a příjmení
    2. Kapitalizovat jméno (první velké, zbytek malá)
    3. Příjmení celé velkými písmeny
    4. Vrátit ve formátu "PRIJMENI, Jmeno"

    Příklad: ("  jan ", " novák  ") → "NOVÁK, Jan"

    Najdi a oprav 3 bugy v kódu níže:
    """
    jmeno = jmeno.strip()
    prijmeni = prijmeni.strip()
    jmeno = jmeno.capitalize()
    prijmeni = prijmeni.upper()
    return f"{prijmeni}, {jmeno}"


def vyzva_5(text):
    """
    🎯 Zjisti jestli je text palindrom.
    Ignoruj velikost písmen a okrajové mezery.
    Příklad: "Anna" → True, "Python" → False, "  kayak " → True
    """
    normalized = text.lower().strip()
    return normalized == normalized[::-1]


def vyzva_6(data):
    """
    🎯 Zformátuj slovník do tabulkového výstupu.
    data = {"jmeno": "Jan", "vek": 25, "město": "Praha"}
    Výstup:
    jmeno  : Jan
    město  : Praha
    vek    : 25

    Klíče zarovnané doleva na 7 znaků, pak " : " a hodnota.
    Řádky oddělené newline, seřazené abecedně podle klíčů.
    """
    return "\n".join(f"{k:<7}: {v}" for k, v in sorted(data.items()))


def vyzva_7(template, **kwargs):
    """
    🎯 Vlastní šablonovací systém:
    Nahraď {klic} v template za hodnotu z kwargs.
    Příklad: ("Ahoj {jmeno}!", jmeno="Jan") → "Ahoj Jan!"

    Rozšíření pro kreativní řešení:
    - Zvládni i čísla (ne jen stringy)
    - Co kdyby šablona obsahovala {klíč} který není v kwargs? (ponech ho)
    """
    result = template
    for key, value in kwargs.items():
        result = result.replace(f"{{{key}}}", str(value))
    return result

# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="F-strings — moderní formátování",
        challenge_type="implementation",
        theory="""F-string je nejčistší způsob formátování v Pythonu 3.6+:

  name = "Jan"
  age = 25
  f"Jmenuji se {name} a je mi {age} let."

Uvnitř {} může být libovolný výraz:
  f"2 + 2 = {2 + 2}"
  f"Velká: {'ahoj'.upper()}"

Formátování čísel:
  f"{3.14159:.2f}"     → "3.14"
  f"{1000000:,}"       → "1,000,000"

Zarovnání:
  f"{'text':<10}"      → "text      " (doleva)
  f"{'text':>10}"      → "      text" (doprava)""",
        task="Vrať formátovaný string: 'Jmenuju se {jmeno} a je mi {vek} let.'",
        difficulty=1, points=15,
        hints=[
            "Nezapomeň prefix f před řetězcem: f'...'",
            "Proměnné vlož do složených závorek: {jmeno}",
            "return f'Jmenuju se {jmeno} a je mi {vek} let.'"
        ],
        tests=[
            lambda: verify(vyzva_1("Jan", 25) == "Jmenuju se Jan a je mi 25 let.",
                           "F-string s Janem ✓"),
            lambda: verify(vyzva_1("Eva", 30) == "Jmenuju se Eva a je mi 30 let.",
                           "F-string s Evou ✓"),
            lambda: verify(vyzva_1("R2D2", 0) == "Jmenuju se R2D2 a je mi 0 let.",
                           "F-string s robotem ✓"),
        ]
    ),
    Challenge(
        title="String slicing — výběr a otočení",
        challenge_type="implementation",
        theory="""String slicing: text[start:stop:step]

  s = "Python"
  s[0:3]    → "Pyt"     (znaky 0,1,2 — stop je exkluzivní!)
  s[2:]     → "thon"    (od indexu 2 do konce)
  s[:3]     → "Pyt"     (od začátku do indexu 2)
  s[::2]    → "Pto"     (každý 2. znak)
  s[::-1]   → "nohtyP"  (pozpátku!)

Negativní indexy:
  s[-1]     → "n"       (poslední znak)
  s[-3:]    → "hon"     (poslední 3 znaky)""",
        task="Otoč text pozpátku pomocí slicingu.",
        difficulty=1, points=15,
        hints=[
            "Slicing s negativním krokem: text[::krok]",
            "Krok -1 projde string pozpátku",
            "return text[::-1]"
        ],
        tests=[
            lambda: verify(vyzva_2("Python") == "nohtyP", "Python → nohtyP ✓"),
            lambda: verify(vyzva_2("abcd") == "dcba", "abcd → dcba ✓"),
            lambda: verify(vyzva_2("") == "", "Prázdný string ✓"),
            lambda: verify(vyzva_2("a") == "a", "Jeden znak ✓"),
        ]
    ),
    Challenge(
        title="Co vypíše tento kód?",
        challenge_type="trace",
        theory="""Trasování kódu = mentální simulace, řádek po řádku.

Pro string operace si pamatuj:
  .strip()       — odstraní whitespace z okrajů
  .split(sep)    — rozdělí string podle sep
  .upper()       — vrátí NOVÝ string velkými písmeny
  .join(list)    — spojí prvky listu
  .count(sub)    — spočítá výskyty (case-sensitive!)

KLÍČOVÉ: Stringy jsou immutable — metody vrací NOVÝ string!
  text.upper()     — text se NEZMĚNÍ (výsledek je zahozený)
  text = text.upper()  — teď se text změní""",
        task="""Trasuj tento kód a vrať (result, count):

    text = "  Hello, World!  "
    text = text.strip()
    parts = text.split(", ")
    parts[1] = parts[1].upper()
    result = " + ".join(parts)
    count = result.count("L")

Tip: trasuj krok po kroku, zapiš si stav proměnných po každém řádku.""",
        difficulty=2, points=20,
        hints=[
            "Po strip(): text = 'Hello, World!'",
            "Po split(', '): parts = ['Hello', 'World!']",
            "Po upper(): parts = ['Hello', 'WORLD!']",
            "Po join: result = 'Hello + WORLD!'",
            ".count('L') počítá jen VELKÉ L — 'Hello' má jen malé 'l'!",
            "return ('Hello + WORLD!', 1)"
        ],
        tests=[
            lambda: verify(vyzva_3() == ("Hello + WORLD!", 1),
                           "Trasování správné! ✓",
                           f"Očekáváno ('Hello + WORLD!', 1), dostal {repr(vyzva_3())}"),
        ]
    ),
    Challenge(
        title="Najdi bug ve formátovači",
        challenge_type="debugging",
        theory="""Stringy jsou IMMUTABLE — metody nikdy nemění originál!

❌ Typický bug:
  text = "ahoj"
  text.upper()       # Vrátí "AHOJ", ale text je stále "ahoj"!

✅ Správně:
  text = text.upper()  # Pouze s přiřazením se hodnota změní

Tohle platí pro VŠECHNY string metody:
  .strip(), .replace(), .lower(), .upper(), .capitalize()...""",
        task="""Funkce vyzva_4_buggy měla formátovat jméno a příjmení:
  ("  jan ", " novák  ") → "NOVÁK, Jan"

Ale má 3 bugy! Oprav je ve funkci vyzva_4_buggy.
(Tři řádky volají string metodu, ale neuloží výsledek zpět.)""",
        difficulty=2, points=20,
        hints=[
            "Podívej se na řádky s .strip(), .capitalize() a .upper()",
            "Bugy: výsledek metody se nikam nepřiřazuje",
            "Oprava: jmeno = jmeno.strip() místo jmeno.strip()",
            "Oprav všechny tři: strip, capitalize, upper — přiřazuj výsledek zpět"
        ],
        tests=[
            lambda: verify(vyzva_4_buggy("  jan ", " novák  ") == "NOVÁK, Jan",
                           "Formátování jména ✓",
                           f"Očekáváno 'NOVÁK, Jan', dostal {repr(vyzva_4_buggy('  jan ', ' novák  '))}"),
            lambda: verify(vyzva_4_buggy("karel", "dvořák") == "DVOŘÁK, Karel",
                           "Další test ✓"),
            lambda: verify(vyzva_4_buggy("  ANNA  ", "  Smith  ") == "SMITH, Anna",
                           "Edge case ✓"),
        ]
    ),
    Challenge(
        title="Palindrom s normalizací",
        challenge_type="implementation",
        theory="""Palindrom = text, který se čte stejně zepředu i zezadu.

Příklady: "anna", "kayak", "racecar"
Ne-palindromy: "ahoj", "python"

Pro kontrolu potřebuješ:
1. Normalizovat (malá písmena, bez mezer na krajích)
2. Porovnat s obrácenou verzí

  text = "Anna"
  n = text.lower()    # "anna"
  n == n[::-1]        # "anna" == "anna" → True""",
        task="Zjisti jestli je text palindrom (ignoruj velikost písmen a okrajové mezery).",
        difficulty=2, points=15,
        hints=[
            "Nejdřív normalizuj: text.lower().strip()",
            "Pak porovnej s obrácenou verzí: normalized == normalized[::-1]",
            "normalized = text.lower().strip(); return normalized == normalized[::-1]"
        ],
        tests=[
            lambda: verify(vyzva_5("Anna") is True, "'Anna' je palindrom ✓"),
            lambda: verify(vyzva_5("Python") is False, "'Python' není palindrom ✓"),
            lambda: verify(vyzva_5("kayak") is True, "'kayak' je palindrom ✓"),
            lambda: verify(vyzva_5("  Kayak  ") is True, "'  Kayak  ' s mezerami ✓"),
            lambda: verify(vyzva_5("") is True, "Prázdný string je palindrom ✓"),
        ]
    ),
    Challenge(
        title="Formátování tabulky",
        challenge_type="implementation",
        theory="""Zarovnání v f-stringu:
  f"{'text':<10}"  → "text      " (doleva na 10 znaků)
  f"{'text':>10}"  → "      text" (doprava)
  f"{'text':^10}"  → "   text   " (na střed)

Iterace přes slovník:
  for k, v in data.items():
      print(f"{k}: {v}")

Řazení:
  sorted(data.items())  → seřazené páry (klíč, hodnota)

Spojení řádků:
  '\\n'.join(list_of_strings)""",
        task="Zformátuj slovník do zarovnané tabulky (klíče na 7 znaků, seřadit abecedně).",
        difficulty=2, points=20,
        hints=[
            "Pro klíče: f'{klic:<7}'",
            "Seřaď: sorted(data.items())",
            "Spoj: '\\n'.join(f'{k:<7}: {v}' for k, v in sorted(data.items()))"
        ],
        tests=[
            lambda: verify(
                vyzva_6({"jmeno": "Jan", "vek": 25}) == "jmeno  : Jan\nvek    : 25",
                "Dva řádky ✓",
                f"Formát nesedí. Dostal: {repr(vyzva_6({'jmeno': 'Jan', 'vek': 25}))}"
            ),
            lambda: verify(
                vyzva_6({"b": 2, "a": 1, "c": 3}) == "a      : 1\nb      : 2\nc      : 3",
                "Řazení ✓"
            ),
        ]
    ),
    Challenge(
        title="Vlastní šablonovací systém",
        challenge_type="implementation",
        theory="""V reálném světě často potřebuješ nahrazovat placeholdery v textu.
Django, Jinja, Flask — všechny používají šablonovací systémy.

Základní princip:
  template = "Ahoj {jmeno}!"
  # Nahraď {jmeno} za skutečnou hodnotu
  # → "Ahoj Jan!"

**kwargs zachytí pojmenované argumenty jako slovník:
  def f(**kwargs):  # kwargs = {"jmeno": "Jan", "vek": 25}
      ...
  f(jmeno="Jan", vek=25)""",
        task="""Nahraď {klic} v template za hodnoty z kwargs.
Příklad: ("Ahoj {jmeno}!", jmeno="Jan") → "Ahoj Jan!"
Zvládni i čísla — převeď je na text.""",
        difficulty=3, points=25,
        hints=[
            "Projdi kwargs: for key, value in kwargs.items()",
            "Pro každý klíč nahraď: template.replace(f'{{{key}}}', str(value))",
            "Pozor: f'{{{key}}}' vytvoří string '{klíč}' — {{ je escape pro { v f-stringu",
            """result = template
for key, value in kwargs.items():
    result = result.replace(f'{{{key}}}', str(value))
return result"""
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
            lambda: verify(
                vyzva_7("Beze změny") == "Beze změny",
                "Bez placeholderů ✓"
            ),
            lambda: verify(
                vyzva_7("{x}{x}", x="ha") == "haha",
                "Duplicitní placeholder ✓"
            ),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, section_name="Python Základy — Stringy a formátování", section_id="01_04")

if __name__ == "__main__":
    run_challenges(challenges, "Python Základy — Stringy a formátování", "01_04")
