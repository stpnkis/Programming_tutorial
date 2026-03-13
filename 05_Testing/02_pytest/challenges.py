#!/usr/bin/env python3
"""⚡ Testing — pytest: Moderní testování."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# KÓD K TESTOVÁNÍ
# ============================================================

def je_prvocislo(n: int) -> bool:
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

def palindrom(s: str) -> bool:
    s = s.lower().replace(" ", "")
    return s == s[::-1]

class Zasobnik:
    def __init__(self):
        self._data = []
    def push(self, val):
        self._data.append(val)
    def pop(self):
        if not self._data: raise IndexError("Prázdný zásobník")
        return self._data.pop()
    def peek(self):
        if not self._data: raise IndexError("Prázdný zásobník")
        return self._data[-1]
    def __len__(self):
        return len(self._data)

# ============================================================
# 📝 TVOJE ŘEŠENÍ (pytest styl — funkce s assert)
# ============================================================

# 🎯 VÝZVA 1: Základní pytest testy
def test_prvocislo_zakladni():
    """Otestuj: 2, 3, 5 jsou prvočísla. 0, 1, 4 nejsou."""
    # TODO: ↓ (prostě assert!)
    pass


def test_palindrom():
    """Otestuj: 'racecar' True, 'hello' False, 'A Santa at NASA' True."""
    # TODO: ↓
    pass


# 🎯 VÝZVA 2: Fixtures (simulované)
def vytvor_zasobnik_s_daty() -> Zasobnik:
    """Fixture: vrátí zásobník s hodnotami [1, 2, 3]."""
    # TODO: ↓
    pass


def test_zasobnik_pop():
    """Testuj pop na zásobníku z fixture."""
    z = vytvor_zasobnik_s_daty()
    # TODO: ↓ assert pop() == 3, len == 2
    pass


def test_zasobnik_prazdny_pop():
    """Testuj, že pop na prázdný zásobník hodí IndexError."""
    z = Zasobnik()
    # TODO: ↓ zkus z.pop() a chyť IndexError
    pass


# 🎯 VÝZVA 3: Parametrizace
def parametrizovana_prvocisla() -> list:
    """
    Vrať seznam tuplů (vstup, očekávaný_výsledek):
    [(2, True), (3, True), (4, False), (17, True), (20, False), ...]
    Minimum 6 testcasů.
    """
    # TODO: ↓
    return []


def test_parametrizovane_prvocisla():
    """Spusť parametrizované testy z funkce výše."""
    test_data = parametrizovana_prvocisla()
    for vstup, ocekavany in test_data:
        assert je_prvocislo(vstup) == ocekavany, f"je_prvocislo({vstup}) mělo být {ocekavany}"


# ============================================================
# 🔍 TESTY
# ============================================================

def _run_pytest_func(fn):
    """Spusť pytest-styl funkci a vrať úspěch."""
    try:
        fn()
        return True
    except (AssertionError, Exception) as e:
        return False

challenges = [
    Challenge(
        title="pytest styl — assert je vše",
        theory="""PYTEST — jednodušší syntaxe než unittest:

# unittest:                       # pytest:
class Test(TestCase):             def test_plus():
    def test_plus(self):              assert 1 + 1 == 2
        self.assertEqual(1+1, 2)

# pytest automaticky najde funkce začínající "test_"
# Stačí "assert" — žádné self.assertEqual!

Spuštění:
  pytest                    # najde a spustí vše
  pytest -v                 # verbose
  pytest test_file.py -k "test_name"  # specifický test""",
        task="Napiš testy s prostým assert.",
        difficulty=1, points=20,
        hints=["assert je_prvocislo(2) == True; assert palindrom('racecar')"],
        tests=[
            lambda: verify(_run_pytest_func(test_prvocislo_zakladni), "Prvočísla ✓"),
            lambda: verify(_run_pytest_func(test_palindrom), "Palindromy ✓"),
        ]
    ),
    Challenge(
        title="Fixtures — příprava dat",
        theory="""PYTEST FIXTURE = příprava pro testy (DI):

@pytest.fixture
def zasobnik():
    z = Zasobnik()
    z.push(1); z.push(2); z.push(3)
    return z

def test_pop(zasobnik):    # pytest automaticky předá!
    assert zasobnik.pop() == 3

# Výhody: znovupoužitelné, čisté, kompozovatelné""",
        task="Napiš fixture a testy pro zásobník.",
        difficulty=2, points=25,
        hints=[
            "fixture: z = Zasobnik(); z.push(1); z.push(2); z.push(3); return z",
            "try: z.pop() except IndexError: pass else: assert False"
        ],
        tests=[
            lambda: verify(
                vytvor_zasobnik_s_daty() is not None and len(vytvor_zasobnik_s_daty()) == 3,
                "Fixture ✓"
            ),
            lambda: verify(_run_pytest_func(test_zasobnik_pop), "Pop test ✓"),
            lambda: verify(_run_pytest_func(test_zasobnik_prazdny_pop), "Prázdný pop ✓"),
        ]
    ),
    Challenge(
        title="Parametrizace — mnoho vstupů",
        theory="""PARAMETRIZACE v pytest:
@pytest.mark.parametrize("vstup,ocekavane", [
    (2, True),
    (3, True),
    (4, False),
    (17, True),
])
def test_prvocislo(vstup, ocekavane):
    assert je_prvocislo(vstup) == ocekavane

# Každý tuple = samostatný test!""",
        task="Připrav >= 6 testovacích vstupů pro prvočísla.",
        difficulty=1, points=15,
        hints=["[(2,True), (3,True), (4,False), (17,True), (1,False), (0,False)]"],
        tests=[
            lambda: verify(len(parametrizovana_prvocisla()) >= 6, f"Parametry ✓: {len(parametrizovana_prvocisla())} testcasů"),
            lambda: verify(_run_pytest_func(test_parametrizovane_prvocisla), "Všechny param testy ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Testing — pytest", "05_02")
