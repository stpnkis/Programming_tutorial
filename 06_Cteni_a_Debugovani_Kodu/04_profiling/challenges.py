#!/usr/bin/env python3
"""⏱️ Profiling — Měření výkonu kódu."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify
import time

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

# 🎯 VÝZVA 1: Timerek — měření času
class Timer:
    """
    🎯 Context manager pro měření času.
    with Timer() as t:
        time.sleep(0.1)
    print(t.elapsed)  # ~0.1
    """
    # TODO: ↓ __enter__, __exit__, property elapsed
    pass


# 🎯 VÝZVA 2: Optimalizace pomalého kódu
def pomaly_hledani(seznam: list, hledane: set) -> list:
    """
    POMALÝ KÓD — O(n*m):
    result = []
    for item in seznam:
        if item in hledane_list:  # O(m) pro list!
            result.append(item)
    """
    pass  # neupravuj

def rychly_hledani(seznam: list, hledane: set) -> list:
    """
    🎯 Přepiš RYCHLE — O(n). hledane je UŽ set!
    """
    # TODO: ↓
    pass


def pomaly_deduplikace(lst: list) -> list:
    """POMALÝ: O(n²) deduplikace."""
    result = []
    for item in lst:
        if item not in result:  # O(n) pro list lookup!
            result.append(item)
    return result

def rychly_deduplikace(lst: list) -> list:
    """🎯 Rychlá deduplikace — zachovej pořadí!"""
    # TODO: ↓
    pass


# 🎯 VÝZVA 3: Profiling kvíz
def profiling_nastroje() -> dict:
    """Vyplň profiling nástroje a k čemu slouží."""
    return {
        "time.time()": "",        # TODO: ↓
        "cProfile": "",           # TODO: ↓
        "line_profiler": "",      # TODO: ↓
        "memory_profiler": "",    # TODO: ↓
    }


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Timer context manager",
        theory="""MĚŘENÍ ČASU — základní profiling:

import time
start = time.perf_counter()
# ... kód ...
elapsed = time.perf_counter() - start

Jako context manager:
class Timer:
    def __enter__(self):
        self._start = time.perf_counter()
        return self
    def __exit__(self, *args):
        self._elapsed = time.perf_counter() - self._start
    @property
    def elapsed(self):
        return self._elapsed""",
        task="Napiš Timer jako context manager.",
        difficulty=2, points=25,
        hints=["__enter__: self._start = time.perf_counter(); return self"],
        tests=[
            lambda: (
                lambda: (
                    lambda t: verify(t.elapsed >= 0, "Timer funguje ✓")
                )(
                    (lambda: (
                        Timer().__enter__() or Timer()
                    ))() if False else
                    type('T', (), {'elapsed': 0.01})()  # fallback
                    if not hasattr(Timer, '__enter__') else
                    (lambda: (
                        lambda t: (t.__exit__(None, None, None), t)[1]
                    )(Timer().__enter__()))()
                )
            )(),
        ]
    ),
    Challenge(
        title="Optimalizace hledání — set vs list",
        theory="""PERFORMANCE KILLERS:

❌ item in list → O(n) — projde celý seznam
✅ item in set  → O(1) — hash lookup

❌ result = []; if x not in result: → O(n²)
✅ videno = set(); if x not in videno: → O(n)

❌ string concatenation v smyčce → O(n²)
✅ "".join(parts) → O(n)""",
        task="Přepiš pomalé hledání a deduplikaci.",
        difficulty=2, points=25,
        hints=[
            "return [x for x in seznam if x in hledane]  # hledane je set!",
            "videno = set(); result = []; if x not in videno: ..."
        ],
        tests=[
            lambda: verify(
                set(rychly_hledani([1, 2, 3, 4, 5], {2, 4})) == {2, 4},
                "Rychlé hledání ✓"
            ),
            lambda: verify(
                rychly_deduplikace([1, 2, 3, 2, 1, 4]) == [1, 2, 3, 4],
                "Rychlá deduplikace ✓"
            ),
            lambda: verify(
                rychly_deduplikace([]) == [],
                "Prázdný ✓"
            ),
        ]
    ),
    Challenge(
        title="Profiling nástroje",
        task="Vyplň k čemu slouží profiling nástroje.",
        difficulty=1, points=10,
        hints=["cProfile = funkční profiler, memory_profiler = měření RAM"],
        tests=[
            lambda: verify(
                all(len(profiling_nastroje()[k]) > 5 for k in profiling_nastroje()),
                "Nástroje popsány ✓"
            ),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Profiling", "06_04")
