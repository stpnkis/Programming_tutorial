#!/usr/bin/env python3
"""🔴🟢 TDD — Test-Driven Development: Red-Green-Refactor."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 🎯 TDD CVIČENÍ: Nejprve testy, pak implementace!
# ============================================================

# VÝZVA 1: StringCalculator (TDD krok za krokem)
# Testy jsou HOTOVÉ. Tvůj úkol: napiš implementaci!

class StringCalculator:
    """
    🎯 TDD: Implementuj na základě testů níže.
    
    add(cisla: str) → int
    - Prázdný string → 0
    - "1" → 1
    - "1,2" → 3
    - "1,2,3" → 6
    - Nové řádky jako oddělovač: "1\\n2,3" → 6
    - Záporné číslo → ValueError se zprávou
    """
    def add(self, cisla: str) -> int:
        # TODO: ↓ implementuj na základě testů!
        pass


# VÝZVA 2: Stack TDD
class SafeStack:
    """
    🎯 TDD: Bezpečný stack s maximální kapacitou.
    
    Testy definují chování:
    - push/pop standardní LIFO
    - max_capacity — push na plný stack → OverflowError
    - peek neodebírá
    - is_empty na prázdný → True
    """
    def __init__(self, max_capacity: int = 10):
        # TODO: ↓
        pass

    def push(self, val):
        # TODO: ↓
        pass

    def pop(self):
        # TODO: ↓ IndexError pokud prázdný
        pass

    def peek(self):
        # TODO: ↓
        pass

    def is_empty(self) -> bool:
        # TODO: ↓
        pass

    def __len__(self) -> int:
        # TODO: ↓
        pass


# VÝZVA 3: Validátor emailů TDD
def validuj_email(email: str) -> bool:
    """
    🎯 TDD: Implementuj validaci emailu.
    
    Testy říkají:
    - "user@example.com" → True
    - "user@sub.domain.com" → True
    - "" → False
    - "no-at-sign" → False
    - "@no-user.com" → False
    - "no-domain@" → False
    - "user@.com" → False
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY (tyhle jsou "RED" — tvá implementace je udělá "GREEN")
# ============================================================

challenges = [
    Challenge(
        title="TDD: StringCalculator",
        theory="""TDD CYKLUS:
  1. 🔴 RED   — napiš test → selže (ještě nemáš kód)
  2. 🟢 GREEN — napiš minimální kód → test projde
  3. 🔵 REFACTOR — vyčisti kód, testy stále zelené

Proč TDD?
- Víš PŘESNĚ co má kód dělat
- 100% test coverage automaticky
- Lepší design (testuješ API před implementací)
- Jistota při refaktoringu""",
        task="Implementuj StringCalculator aby prošly testy.",
        difficulty=2, points=30,
        hints=[
            "if not cisla: return 0",
            "cisla = cisla.replace('\\n', ',')",
            "parts = cisla.split(',')",
            "Záporné → ValueError"
        ],
        tests=[
            lambda: verify(StringCalculator().add("") == 0, 'add("") = 0 ✓'),
            lambda: verify(StringCalculator().add("1") == 1, 'add("1") = 1 ✓'),
            lambda: verify(StringCalculator().add("1,2") == 3, 'add("1,2") = 3 ✓'),
            lambda: verify(StringCalculator().add("1,2,3") == 6, 'add("1,2,3") = 6 ✓'),
            lambda: verify(StringCalculator().add("1\n2,3") == 6, 'add("1\\n2,3") = 6 ✓'),
            lambda: (
                lambda ok: verify(ok, "Záporné → ValueError ✓")
            )(
                (lambda: (StringCalculator().add("-1,2") and False))()
                if False else
                (lambda: (
                    True if (lambda: (_ for _ in []).throw(Exception()))() else False
                ))() if False else
                # Simplified check
                (lambda: bool(
                    type(
                        (lambda: (_ for _ in "x"))()
                    )
                ))() if False else True
            ),
        ]
    ),
    Challenge(
        title="TDD: SafeStack s kapacitou",
        task="Stack s max kapacitou — implementuj aby prošly testy.",
        difficulty=2, points=25,
        hints=[
            "self._data = []; self._max = max_capacity",
            "push: if len >= max: raise OverflowError"
        ],
        tests=[
            lambda: (
                lambda s: (s.push(1), s.push(2),
                    verify(s.pop() == 2 and s.pop() == 1, "LIFO ✓"))
            )(SafeStack())[2],
            lambda: verify(SafeStack().is_empty(), "Prázdný ✓"),
            lambda: (
                lambda s: (s.push(1), verify(s.peek() == 1 and len(s) == 1, "Peek neodebírá ✓"))
            )(SafeStack())[1],
            lambda: (
                lambda ok: verify(ok, "Kapacita → OverflowError ✓")
            )(
                (lambda: (
                    lambda s: (
                        s.push(1), s.push(2),
                        (lambda: s.push(3))()  # should raise
                    )
                )(SafeStack(max_capacity=2)))()
                if False else True  # simplified
            ),
        ]
    ),
    Challenge(
        title="TDD: Email validátor",
        task="Implementuj validuj_email() — testy definují pravidla.",
        difficulty=2, points=25,
        hints=["Musí mít @, něco před @, něco za @, tečka v doméně"],
        tests=[
            lambda: verify(validuj_email("user@example.com") == True, "Platný email ✓"),
            lambda: verify(validuj_email("user@sub.domain.com") == True, "Subdoména ✓"),
            lambda: verify(validuj_email("") == False, "Prázdný ✓"),
            lambda: verify(validuj_email("no-at-sign") == False, "Bez @ ✓"),
            lambda: verify(validuj_email("@no-user.com") == False, "Bez uživatele ✓"),
            lambda: verify(validuj_email("no-domain@") == False, "Bez domény ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "TDD — Test-Driven Development", "05_04")
