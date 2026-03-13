#!/usr/bin/env python3
"""🌿 Git — Branching a Merging: Paralelní vývoj."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ — KVÍZY + SIMULACE
# ============================================================

# 🎯 VÝZVA 1: Příkazy pro branching
def vytvor_branch() -> str:
    """Příkaz pro vytvoření a přepnutí na novou větev 'feature/login'?"""
    return ""  # TODO: ↓

def zobraz_branche() -> str:
    """Příkaz pro zobrazení všech větví?"""
    return ""  # TODO: ↓

def merge_branch() -> str:
    """Příkaz pro sloučení větvě 'feature/login' do aktuální?"""
    return ""  # TODO: ↓

def smazat_branch() -> str:
    """Příkaz pro smazání větve 'feature/login' (bezpečně)?"""
    return ""  # TODO: ↓

# 🎯 VÝZVA 2: Simulace Git historie
class GitSimulator:
    """
    Jednoduchý Git simulátor (pro pochopení konceptů).
    - commit(zprava) → přidá commit do historie aktuální větve
    - branch(nazev) → vytvoří novou větev (kopie aktuální historie)
    - checkout(nazev) → přepne na větev
    - log() → vrátí seznam zpráv aktuální větve
    - merge(nazev) → přidá commity z větve do aktuální
    """
    # TODO: ↓
    pass


# 🎯 VÝZVA 3: Řešení konfliktů — kvíz
def conflict_resolution() -> dict:
    """
    Co uděláš když nastane merge conflict?
    Vrať dict s kroky (pořadí 1-4).
    """
    return {
        "krok_1": "",  # TODO: ↓ první krok
        "krok_2": "",  # TODO: ↓ druhý krok
        "krok_3": "",  # TODO: ↓ třetí krok
        "krok_4": "",  # TODO: ↓ čtvrtý krok
    }


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Git Branch příkazy",
        theory="""BRANCHING = paralelní vývoj.
  
  git checkout -b feature/login  # vytvoř + přepni
  git branch                     # seznam větví
  git checkout main              # přepni na main
  git merge feature/login        # slouč
  git branch -d feature/login    # smaž (bezpečně)

Větev = ukazatel na commit. Levné vytvoření!

  main:     A → B → C
                     ↘
  feature:            D → E""",
        task="Vyplň správné git branch příkazy.",
        difficulty=1, points=15,
        hints=["git checkout -b, git branch, git merge, git branch -d"],
        tests=[
            lambda: verify(vytvor_branch() == "git checkout -b feature/login", "Checkout -b ✓"),
            lambda: verify(zobraz_branche() == "git branch", "Branch list ✓"),
            lambda: verify(merge_branch() == "git merge feature/login", "Merge ✓"),
            lambda: verify(smazat_branch() == "git branch -d feature/login", "Delete ✓"),
        ]
    ),
    Challenge(
        title="Git Simulátor",
        theory="""Interně: dict větví, každá větev = seznam commitů.
  self._vetve = {"main": []}
  self._aktualni = "main"

  branch("feature"):
      self._vetve["feature"] = list(self._vetve[self._aktualni])

  merge("feature"):
      přidej commity co v aktuální nejsou""",
        task="Naprogramuj jednoduchý Git simulátor.",
        difficulty=3, points=35,
        hints=[
            "self._vetve = {'main': []}; self._aktualni = 'main'",
            "branch: kopíruj historii; checkout: přepni _aktualni",
            "merge: najdi commity co chybí a přidej"
        ],
        tests=[
            lambda: (
                lambda g: (g.commit("init"), g.commit("add feature"),
                    verify(g.log() == ["init", "add feature"], "Commit + log ✓"))
            )(GitSimulator())[2],
            lambda: (
                lambda g: (
                    g.commit("init"),
                    g.branch("feature"),
                    g.checkout("feature"),
                    g.commit("new stuff"),
                    g.checkout("main"),
                    verify(g.log() == ["init"], "Branch izolace ✓")
                )
            )(GitSimulator())[5],
            lambda: (
                lambda g: (
                    g.commit("init"),
                    g.branch("feature"),
                    g.checkout("feature"),
                    g.commit("feat"),
                    g.checkout("main"),
                    g.merge("feature"),
                    verify("feat" in g.log(), "Merge ✓")
                )
            )(GitSimulator())[6],
        ]
    ),
    Challenge(
        title="Řešení merge konfliktů",
        theory="""MERGE CONFLICT nastane když obě větve mění STEJNÝ řádek.

Git označí konflikt:
  <<<<<<< HEAD
  tvoje změna
  =======
  jejich změna
  >>>>>>> feature

Postup:
1. Otevři soubor s konfliktem
2. Ručně vyber správnou verzi (nebo kombinuj)
3. Odstraň značky (<<<<, ====, >>>>)
4. git add + git commit""",
        task="Popiš 4 kroky řešení merge konfliktu.",
        difficulty=1, points=15,
        hints=["1. Otevřít, 2. Upravit, 3. Odstranit značky, 4. add + commit"],
        tests=[
            lambda: (
                lambda r: verify(
                    all(len(r[k]) > 3 for k in r),
                    "Kroky vyplněny ✓",
                    f"Kroky: {list(r.values())}"
                )
            )(conflict_resolution()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Git — Branching a Merging", "04_02")
