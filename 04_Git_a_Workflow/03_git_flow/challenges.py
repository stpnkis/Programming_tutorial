#!/usr/bin/env python3
"""🔄 Git Flow — Profesionální workflow."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

# 🎯 VÝZVA 1: Typy větví v Git Flow
def git_flow_vetve() -> dict:
    """
    Vyplň účel každé větve v Git Flow:
    """
    return {
        "main": "",       # TODO: ↓ co je na main?
        "develop": "",    # TODO: ↓ co je na develop?
        "feature": "",    # TODO: ↓ k čemu feature větve?
        "release": "",    # TODO: ↓ k čemu release větve?
        "hotfix": "",     # TODO: ↓ k čemu hotfix větve?
    }

# 🎯 VÝZVA 2: Pojmenování větví
def spravny_nazev(popis: str) -> str:
    """
    Přepiš popis na správný název větve.
    "přidání login stránky" → "feature/login-page"
    "oprava kritického bugu v platbách" → "hotfix/payment-fix"
    "příprava verze 2.0" → "release/2.0"
    """
    # TODO: ↓ vrať správný název
    if "login" in popis:
        return ""  # TODO
    elif "bugu" in popis or "kritick" in popis:
        return ""  # TODO
    elif "verze" in popis:
        return ""  # TODO
    return ""

# 🎯 VÝZVA 3: PR/MR šablona
def pull_request_sablona(typ: str, popis: str, testy: bool) -> dict:
    """
    Vytvoř strukturu Pull Request / Merge Request.
    Vrať dict s klíči: title, description, checklist
    """
    return {
        "title": "",           # TODO: ↓ stručný titul
        "description": "",     # TODO: ↓ co se změnilo a proč
        "checklist": [],       # TODO: ↓ seznam kontrolních bodů (min 3)
    }

# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Git Flow větve",
        theory="""GIT FLOW — profesionální branching model:

  main     ──●────────────●── (produkce, stabilní)
              ↑             ↑
  hotfix    ──●             │
              ↑             │
  release   ──────────●─────│
                      ↑     │
  develop  ──●──●──●──●──●──● (integrace)
              ↑  ↑  ↑
  feature   ──●  ●  ●  (nové funkce)

main = stabilní produkční kód
develop = integrace nových věcí
feature/* = nová funkce
release/* = příprava vydání
hotfix/* = urgentní oprava v produkci""",
        task="Vyplň účel každé Git Flow větve.",
        difficulty=1, points=15,
        hints=["main=produkce, develop=integrace, feature=nová funkce"],
        tests=[
            lambda: (
                lambda v: verify(
                    all(len(v[k]) > 3 for k in v),
                    "Větve popsány ✓"
                )
            )(git_flow_vetve()),
        ]
    ),
    Challenge(
        title="Pojmenování větví",
        theory="""Konvence pojmenování:
  feature/nazev-funkce
  bugfix/popis-bugu
  hotfix/urgentni-oprava
  release/verze

Pravidla:
- Malá písmena, pomlčky místo mezer
- Prefix určuje typ (feature/, hotfix/, ...)
- Stručný, popisný název""",
        task="Přepiš popis na správný název větve.",
        difficulty=1, points=15,
        hints=["feature/login-page, hotfix/payment-fix, release/2.0"],
        tests=[
            lambda: verify(
                spravny_nazev("přidání login stránky") == "feature/login-page",
                "Feature ✓"
            ),
            lambda: verify(
                spravny_nazev("oprava kritického bugu v platbách") == "hotfix/payment-fix",
                "Hotfix ✓"
            ),
            lambda: verify(
                spravny_nazev("příprava verze 2.0") == "release/2.0",
                "Release ✓"
            ),
        ]
    ),
    Challenge(
        title="Pull Request šablona",
        theory="""PULL REQUEST (PR) = žádost o sloučení kódu.

Dobrý PR obsahuje:
  Title:       Stručný popis (co se mění)
  Description: Detaily — co, proč, jak
  Checklist:
    ☐ Testy projdou
    ☐ Kód je přehlédnutý
    ☐ Dokumentace aktualizována
    ☐ Bez breaking changes

Tip: Menší PR = rychlejší review = méně bugů""",
        task="Vytvoř strukturu Pull Requestu.",
        difficulty=1, points=15,
        hints=["title: krátký popis; checklist: ['Testy OK', 'Code review', 'Docs']"],
        tests=[
            lambda: (
                lambda pr: verify(
                    len(pr["title"]) > 3 and
                    len(pr["description"]) > 10 and
                    len(pr["checklist"]) >= 3,
                    "PR šablona ✓",
                    f"Title: {pr['title']}, Checklist: {len(pr['checklist'])} bodů"
                )
            )(pull_request_sablona("feature", "Přidána autentizace", True)),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Git Flow", "04_03")
