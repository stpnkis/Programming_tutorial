#!/usr/bin/env python3
"""🚀 CI/CD — Automatizace testů a nasazení."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

# 🎯 VÝZVA 1: Co je CI/CD?
def ci_cd_definice() -> dict:
    """Vyplň co znamenají zkratky."""
    return {
        "CI": "",  # TODO: ↓ Continuous ...?
        "CD": "",  # TODO: ↓ Continuous ...?
    }

def ci_kroky() -> list:
    """
    Vrať typické kroky CI pipeline v pořadí.
    Minimum 4 kroky.
    """
    return []  # TODO: ↓ ["checkout kódu", "instalace závislostí", ...]

# 🎯 VÝZVA 2: GitHub Actions YAML
def github_actions_yaml() -> str:
    """
    Napiš minimální GitHub Actions workflow (jako string).
    Musí obsahovat: name, on (push), jobs, steps.
    """
    yaml = ""  # TODO: ↓
    return yaml

# 🎯 VÝZVA 3: Pipeline simulátor
class Pipeline:
    """
    CI/CD Pipeline simulátor.
    - add_step(nazev, funkce) → přidá krok
    - run() → spustí všechny kroky, vrátí dict {"passed": bool, "results": [...]}
    - Pokud krok selže (vyhodí výjimkou), pipeline se ZASTAVÍ.
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="CI/CD — definice a kroky",
        theory="""CI = Continuous Integration
  → automatické testování při každém PUSH/PR
  → "Funguje můj kód s ostatními?"

CD = Continuous Deployment/Delivery
  → automatické nasazení po úspěšných testech
  → "Dostaň kód k uživatelům automaticky"

Typická CI pipeline:
  1. Checkout kódu
  2. Instalace závislostí
  3. Spuštění testů
  4. Linting & formátování
  5. Build
  6. Deploy (CD)""",
        task="Vyplň CI/CD definice a kroky pipeline.",
        difficulty=1, points=15,
        hints=["CI = Continuous Integration, CD = Continuous Deployment"],
        tests=[
            lambda: verify(
                "integration" in ci_cd_definice()["CI"].lower(),
                "CI ✓"
            ),
            lambda: verify(
                "deploy" in ci_cd_definice()["CD"].lower() or "delivery" in ci_cd_definice()["CD"].lower(),
                "CD ✓"
            ),
            lambda: verify(len(ci_kroky()) >= 4, f"Pipeline: {len(ci_kroky())} kroků ✓"),
        ]
    ),
    Challenge(
        title="GitHub Actions YAML",
        theory="""GITHUB ACTIONS — CI/CD přímo v GitHubu:

name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest""",
        task="Napiš GitHub Actions YAML workflow (jako string).",
        difficulty=2, points=20,
        hints=["name:, on:, jobs:, steps: — klíčové sekce YAML"],
        tests=[
            lambda: (
                lambda y: verify(
                    "name" in y and "on" in y and "jobs" in y and "steps" in y,
                    "YAML struktura ✓",
                    f"Délka: {len(y)} znaků"
                )
            )(github_actions_yaml()),
        ]
    ),
    Challenge(
        title="Pipeline simulátor",
        task="Simuluj CI pipeline — spouštěj kroky v pořadí.",
        difficulty=2, points=25,
        hints=[
            "self._steps = []; add_step appends (name, fn)",
            "run: iteruj, volej fn(), chyť výjimku = fail"
        ],
        tests=[
            lambda: (
                lambda p: (
                    p.add_step("lint", lambda: True),
                    p.add_step("test", lambda: True),
                    (lambda r: verify(r["passed"] and len(r["results"]) == 2,
                                       "Pipeline pass ✓"))(p.run())
                )
            )(Pipeline())[2],
            lambda: (
                lambda p: (
                    p.add_step("lint", lambda: True),
                    p.add_step("fail", lambda: (_ for _ in "").throw(Exception("bug"))),
                    p.add_step("test", lambda: True),
                    (lambda r: verify(not r["passed"], "Pipeline fail → stop ✓"))(p.run())
                )
            )(Pipeline())[3],
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "CI/CD Základy", "04_05")
