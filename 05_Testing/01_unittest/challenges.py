#!/usr/bin/env python3
"""🧪 Testing — unittest: Standardní testovací knihovna."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify
import unittest

# ============================================================
# KÓD K TESTOVÁNÍ (neupravuj)
# ============================================================

class Calculator:
    def secti(self, a, b): return a + b
    def odecti(self, a, b): return a - b
    def nasob(self, a, b): return a * b
    def del_(self, a, b):
        if b == 0: raise ZeroDivisionError("Dělení nulou!")
        return a / b

class Kosik:
    def __init__(self):
        self._polozky = []
    def pridej(self, nazev, cena):
        self._polozky.append({"nazev": nazev, "cena": cena})
    def celkova_cena(self):
        return sum(p["cena"] for p in self._polozky)
    def pocet(self):
        return len(self._polozky)
    def vyprazdni(self):
        self._polozky.clear()

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

class TestCalculator(unittest.TestCase):
    """
    🎯 VÝZVA 1: Napiš testy pro Calculator.
    - test_secti: 2+3=5
    - test_odecti: 10-4=6
    - test_nasob: 3*7=21
    - test_deleni: 10/2=5.0
    - test_deleni_nulou: raise ZeroDivisionError
    """
    def setUp(self):
        """Příprava — spustí se PŘED každým testem."""
        # TODO: ↓ vytvoř self.calc
        pass

    # TODO: ↓ napiš test metody (test_secti, test_odecti, ...)
    pass


class TestKosik(unittest.TestCase):
    """
    🎯 VÝZVA 2: Napiš testy pro Košík.
    - test_prazdny: nový košík má 0 položek, cena 0
    - test_pridej: po přidání je pocet 1
    - test_celkova_cena: 2 položky → součet cen
    - test_vyprazdni: po vyprázdnění 0 položek
    """
    def setUp(self):
        # TODO: ↓
        pass

    # TODO: ↓ napiš testy
    pass


# 🎯 VÝZVA 3: Parametrizované testy
class TestSectiParametrizovane(unittest.TestCase):
    """
    Otestuj sčítání s více vstupy.
    Napiš metodu test_vice_vstupu, která testuje:
    (1,1,2), (0,0,0), (-1,1,0), (100,200,300)
    Hint: subTest context manager.
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

def _run_test_class(cls):
    """Helper: spustí test třídu a vrátí výsledek."""
    suite = unittest.TestLoader().loadTestsFromTestCase(cls)
    runner = unittest.TextTestRunner(stream=open(os.devnull, 'w'), verbosity=0)
    result = runner.run(suite)
    return result

challenges = [
    Challenge(
        title="unittest — Calculator testy",
        theory="""UNITTEST — standardní Python testovací framework.

import unittest

class TestMyClass(unittest.TestCase):
    def setUp(self):                     # příprava
        self.obj = MyClass()
    
    def test_neco(self):                 # test začíná "test_"
        self.assertEqual(result, expected)
    
    def test_vyjimka(self):
        with self.assertRaises(ValueError):
            risky_function()

# assertEqual, assertTrue, assertFalse, assertIn
# assertRaises, assertAlmostEqual, assertIsNone""",
        task="Otestuj Calculator — assertEqual + assertRaises.",
        difficulty=2, points=25,
        hints=[
            "self.calc = Calculator() v setUp",
            "self.assertEqual(self.calc.secti(2,3), 5)",
            "with self.assertRaises(ZeroDivisionError): self.calc.del_(1,0)"
        ],
        tests=[
            lambda: (
                lambda r: verify(
                    r.testsRun >= 4 and len(r.failures) == 0 and len(r.errors) == 0,
                    f"Calculator: {r.testsRun} testů, 0 selhání ✓",
                    f"{r.testsRun} testů, {len(r.failures)} failures, {len(r.errors)} errors"
                )
            )(_run_test_class(TestCalculator)),
        ]
    ),
    Challenge(
        title="unittest — Košík testy",
        task="Otestuj nákupní košík — setUp + tearDown pattern.",
        difficulty=2, points=25,
        hints=["self.kosik = Kosik() v setUp; assertEqual pro počty a ceny"],
        tests=[
            lambda: (
                lambda r: verify(
                    r.testsRun >= 3 and len(r.failures) == 0,
                    f"Košík: {r.testsRun} testů OK ✓"
                )
            )(_run_test_class(TestKosik)),
        ]
    ),
    Challenge(
        title="Parametrizované testy — subTest",
        theory="""PARAMETRIZOVANÉ TESTY:
class TestCalc(unittest.TestCase):
    def test_secti_params(self):
        data = [(1,1,2), (0,0,0), (-1,1,0)]
        for a, b, expected in data:
            with self.subTest(a=a, b=b):
                self.assertEqual(calc.secti(a,b), expected)

subTest = pokud jeden selže, ostatní se STÁLE spustí.""",
        task="Testuj sčítání s více vstupy (subTest).",
        difficulty=2, points=20,
        hints=["for a,b,exp in test_data: with self.subTest(): assertEqual"],
        tests=[
            lambda: (
                lambda r: verify(
                    r.testsRun >= 1 and len(r.failures) == 0,
                    "Parametrizované testy ✓"
                )
            )(_run_test_class(TestSectiParametrizovane)),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Testing — unittest", "05_01")
