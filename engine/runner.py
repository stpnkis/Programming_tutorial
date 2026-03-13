"""
🏃 Runner modul — spouštění a ověřování výzev.
Srdce tréninkového centra.
"""
import traceback
import time
import sys
import os

# Přidej root do path pro importy
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from engine.ui import UI, Colors as C
from engine.progress import Progress


class Challenge:
    """
    Jedna výzva/úkol k vyřešení.

    Parametry:
        title: Název výzvy
        description: Popis co má uživatel udělat
        task: Konkrétní zadání
        hints: Seznam nápověd (postupně se odhalují)
        tests: Seznam testovacích funkcí - každá vrací (bool, message)
        difficulty: 1-3 (⭐ až ⭐⭐⭐)
        points: Počet bodů za splnění
        theory: Vysvětlení teorie (volitelné)
        example: Příklad kódu (volitelné)
    """

    def __init__(self, title, description="", task="", hints=None,
                 tests=None, difficulty=1, points=10, theory=None,
                 example=None, example_output=None):
        self.title = title
        self.description = description
        self.task = task
        self.hints = hints or []
        self.tests = tests or []
        self.difficulty = min(max(difficulty, 1), 3)
        self.points = points
        self.theory = theory
        self.example = example
        self.example_output = example_output
        self.solved = False


def run_challenges(challenges, section_name="", section_id=""):
    """
    Spustí sadu výzev interaktivně.

    challenges: seznam Challenge objektů
    section_name: jméno sekce pro zobrazení
    section_id: ID pro ukládání progressu (např. "01_01")
    """
    progress = Progress()

    UI.clear()
    UI.banner(f"🏋️ {section_name}" if section_name else "🏋️ TRÉNINK")

    total_points = sum(ch.points for ch in challenges)
    earned_points = 0
    completed = 0

    for i, ch in enumerate(challenges, 1):
        # Hlavička výzvy
        UI.challenge_header(i, ch.title, ch.difficulty, ch.points)

        # Teorie
        if ch.theory:
            UI.theory(ch.theory)

        # Příklad
        if ch.example:
            UI.example(ch.example, ch.example_output)

        # Popis
        if ch.description:
            print(f"  {C.WHITE}{ch.description}{C.RESET}\n")

        # Zadání
        if ch.task:
            UI.task(ch.task)

        # Spuštění testů
        all_passed = True
        hint_index = 0

        for j, test_fn in enumerate(ch.tests):
            try:
                result, message = test_fn()
                if result:
                    UI.success(message)
                else:
                    UI.fail(message)
                    all_passed = False

                    # Nabídni hint
                    if ch.hints and hint_index < len(ch.hints):
                        if UI.ask_hint():
                            UI.hint(ch.hints[hint_index])
                            hint_index += 1
                    break

            except Exception as e:
                UI.fail(f"Chyba při testu: {e}")
                # Zobraz traceback pro debugging
                print(f"  {C.DIM}")
                traceback.print_exc()
                print(f"  {C.RESET}")
                all_passed = False

                if ch.hints and hint_index < len(ch.hints):
                    if UI.ask_hint():
                        UI.hint(ch.hints[hint_index])
                        hint_index += 1
                break

        if all_passed and ch.tests:
            ch.solved = True
            earned_points += ch.points
            completed += 1
            print(f"\n  {C.GREEN}{C.BOLD}  +{ch.points} bodů! 💰{C.RESET}")
        elif not ch.tests:
            # Výzva bez automatických testů (manuální review)
            UI.info("Tato výzva nemá automatické testy. Zkontroluj výstup sám.")
            ch.solved = True
            earned_points += ch.points
            completed += 1

        # Progress bar
        print()
        UI.progress_bar(completed, len(challenges))

        if i < len(challenges):
            UI.wait()
            print()

    # Závěrečné shrnutí
    print()
    UI.double_line()
    print(f"\n  {C.BOLD}📊 VÝSLEDKY:{C.RESET}")
    UI.score_display(earned_points, total_points)
    UI.progress_bar(completed, len(challenges))

    if completed == len(challenges):
        UI.celebration()

    # Ulož progress
    if section_id:
        progress.save_section(section_id, completed, len(challenges), earned_points)

    return earned_points, total_points


def verify(condition, success_msg="Správně!", fail_msg="Špatně."):
    """
    Jednoduchá verifikační funkce pro testy.
    Vrací tuple (bool, message) pro použití v Challenge.tests.
    """
    if condition:
        return (True, success_msg)
    return (False, fail_msg)


def make_test(func, expected, description="Test", compare=None):
    """
    Vytvoří testovací funkci z funkce a očekávaného výsledku.

    func: funkce k otestování (callable bez argumentů)
    expected: očekávaný výsledek
    description: popis testu
    compare: volitelná porovnávací funkce
    """
    def test():
        try:
            result = func()
            if compare:
                passed = compare(result, expected)
            else:
                passed = result == expected
            if passed:
                return (True, f"{description}: ✓")
            else:
                return (False, f"{description}: očekáváno {expected}, dostal {result}")
        except Exception as e:
            return (False, f"{description}: chyba - {e}")
    return test


def make_tests(test_cases, func_to_test):
    """
    Vytvoří seznam testů z test cases.

    test_cases: seznam (args, expected_result, description)
    func_to_test: funkce k otestování
    """
    tests = []
    for args, expected, desc in test_cases:
        if not isinstance(args, tuple):
            args = (args,)
        def _test(a=args, e=expected, d=desc):
            try:
                result = func_to_test(*a)
                if result == e:
                    return (True, f"{d}: ✓")
                else:
                    return (False, f"{d}: očekáváno {e!r}, dostal {result!r}")
            except Exception as ex:
                return (False, f"{d}: chyba - {ex}")
        tests.append(_test)
    return tests


class Timer:
    """Kontextový manažer pro měření času."""
    def __init__(self, label=""):
        self.label = label

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start
        if self.label:
            print(f"  {C.DIM}⏱️  {self.label}: {self.elapsed:.4f}s{C.RESET}")
