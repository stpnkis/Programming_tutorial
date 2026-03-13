#!/usr/bin/env python3
"""⏱️ DSA — Big O Analýza: Složitost algoritmů."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ — KVÍZ + ANALÝZA
# ============================================================

def slozitost_1(lst: list) -> int:
    """Jaká je složitost? Vrať odpověď v otazka_1."""
    total = 0
    for x in lst:
        total += x
    return total


def slozitost_2(lst: list) -> list:
    """Jaká je složitost? Vrať odpověď v otazka_2."""
    result = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            result.append(lst[i] + lst[j])
    return result


def slozitost_3(lst: list, cil: int) -> int:
    """Jaká je složitost? Vrať odpověď v otazka_3."""
    low, high = 0, len(lst) - 1
    while low <= high:
        mid = (low + high) // 2
        if lst[mid] == cil:
            return mid
        elif lst[mid] < cil:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# 🎯 VÝZVA 1: Urči složitost těchto funkcí
# Možnosti: "O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)", "O(2^n)"

otazka_1 = ""  # TODO: ↓ složitost slozitost_1
otazka_2 = ""  # TODO: ↓ složitost slozitost_2
otazka_3 = ""  # TODO: ↓ složitost slozitost_3


# 🎯 VÝZVA 2: Seřaď od nejrychlejší po nejpomalejší
# Správné pořadí = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)", "O(2^n)"]

poradi_slozitosti = []  # TODO: ↓ seřaď!


# 🎯 VÝZVA 3: Praktická analýza
def otazka_sort():
    """Jakou složitost má Python sort (Timsort)?"""
    return ""  # TODO: ↓ "O(n log n)" nebo jiná?


def otazka_dict_lookup():
    """Jakou složitost má dict lookup (průměrně)?"""
    return ""  # TODO: ↓


def otazka_list_append():
    """Jakou složitost má list.append() (amortizovaně)?"""
    return ""  # TODO: ↓


# 🎯 VÝZVA 4: Napiš funkci s danou složitostí

def funkce_o_1(lst: list) -> int:
    """
    Napiš funkci se složitostí O(1).
    Vrať první prvek (nebo 0 pro prázdný).
    """
    # TODO: ↓
    pass


def funkce_o_n(lst: list) -> int:
    """
    Napiš funkci se složitostí O(n).
    Vrať součet všech prvků.
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Urči Big O složitost",
        theory="""BIG O — jak roste čas s velikostí vstupu?

O(1)       — konstantní (dict lookup, array index)
O(log n)   — logaritmická (binární hledání)
O(n)       — lineární (procházení seznamu)
O(n log n) — kvazi-lineární (merge sort, Tim sort)
O(n²)      — kvadratická (vnořené cykly, bubble sort)
O(2^n)     — exponenciální (všechny podmnožiny)

PRAVIDLA:
1. Počítej vnořené smyčky → O(n) * O(n) = O(n²)
2. Ignoruj konstanty → O(3n) = O(n)
3. Bere se dominantní člen → O(n² + n) = O(n²)""",
        task='Urči složitost tří funkcí: otazka_1, otazka_2, otazka_3.',
        difficulty=1, points=20,
        hints=["slozitost_1: jeden cyklus = ?", "slozitost_2: dva vnořené = ?", "slozitost_3: půlení = ?"],
        tests=[
            lambda: verify(otazka_1 == "O(n)", f"slozitost_1 = {otazka_1} ✓"),
            lambda: verify(otazka_2 == "O(n^2)", f"slozitost_2 = {otazka_2} ✓"),
            lambda: verify(otazka_3 == "O(log n)", f"slozitost_3 = {otazka_3} ✓"),
        ]
    ),
    Challenge(
        title="Seřaď složitosti",
        task="Od nejrychlejší po nejpomalejší.",
        difficulty=1, points=15,
        hints=["O(1) < O(log n) < O(n) < ..."],
        tests=[
            lambda: verify(
                poradi_slozitosti == ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)", "O(2^n)"],
                "Pořadí ✓"
            ),
        ]
    ),
    Challenge(
        title="Python operace — jaká složitost?",
        theory="""Python interně:
  sorted() → Timsort → O(n log n)
  dict[key] → hash lookup → O(1) průměrně
  list.append() → amortizované O(1)
  list.insert(0, x) → O(n) — posouvá vše
  x in list → O(n) — lineární hledání
  x in set → O(1) — hash lookup""",
        task="Jaká je složitost sort, dict lookup, list append?",
        difficulty=1, points=15,
        hints=["sort = O(n log n), dict = O(1), append = O(1)"],
        tests=[
            lambda: verify(otazka_sort() == "O(n log n)", f"Sort: {otazka_sort()} ✓"),
            lambda: verify(otazka_dict_lookup() == "O(1)", f"Dict: {otazka_dict_lookup()} ✓"),
            lambda: verify(otazka_list_append() == "O(1)", f"Append: {otazka_list_append()} ✓"),
        ]
    ),
    Challenge(
        title="Napiš funkci s danou složitostí",
        task="O(1) a O(n) funkce.",
        difficulty=1, points=15,
        hints=["O(1): return lst[0]; O(n): sum(lst)"],
        tests=[
            lambda: verify(funkce_o_1([1, 2, 3]) == 1, "O(1) ✓"),
            lambda: verify(funkce_o_1([]) == 0, "O(1) prázdný ✓"),
            lambda: verify(funkce_o_n([1, 2, 3, 4]) == 10, "O(n) ✓"),
            lambda: verify(funkce_o_n([]) == 0, "O(n) prázdný ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "DSA — Big O Analýza", "03_09")
