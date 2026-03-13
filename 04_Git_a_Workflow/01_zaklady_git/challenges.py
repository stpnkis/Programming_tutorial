#!/usr/bin/env python3
"""📦 Git — Základy: Verzování kódu od nuly."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ — KVÍZOVÉ VÝZVY
# ============================================================

# 🎯 VÝZVA 1: Git příkazy
def git_init_prikaz() -> str:
    """Jaký příkaz inicializuje nový Git repozitář?"""
    return ""  # TODO: ↓

def git_status_prikaz() -> str:
    """Jaký příkaz zobrazí stav repozitáře?"""
    return ""  # TODO: ↓

def git_add_vse() -> str:
    """Jaký příkaz přidá VŠECHNY změny do staging area?"""
    return ""  # TODO: ↓

def git_commit_msg() -> str:
    """Příkaz pro commit se zprávou 'Initial commit'?"""
    return ""  # TODO: ↓

# 🎯 VÝZVA 2: Oblast Git
def git_oblasti() -> dict:
    """
    Vyplň 3 oblasti Gitu v pořadí:
    working_directory → staging → repository
    """
    return {
        "oblast_1": "",  # TODO: ↓ kde edituješ soubory?
        "oblast_2": "",  # TODO: ↓ kam jdou po git add?
        "oblast_3": "",  # TODO: ↓ kam jdou po git commit?
    }

# 🎯 VÝZVA 3: Gitignore
def gitignore_vzory() -> list:
    """
    Vrať seznam vzorů pro .gitignore:
    - Python cache složky
    - virtual environment
    - .env soubor
    - __pycache__
    """
    return []  # TODO: ↓ ["__pycache__/", ...]

# 🎯 VÝZVA 4: Git log a diff
def git_log_oneline() -> str:
    """Příkaz pro kompaktní historii (jeden řádek na commit)?"""
    return ""  # TODO: ↓

def git_diff_staged() -> str:
    """Příkaz pro zobrazení staged změn?"""
    return ""  # TODO: ↓

# 🎯 VÝZVA 5: Dobrá commit zpráva
def dobra_zprava(spatna: str) -> str:
    """
    Přepiš špatnou commit zprávu na dobrou.
    Pravidla: imperativ, max 50 znaků, popis co a proč.
    
    Špatná: "fixed stuff"
    Dobrá: "Fix login validation for empty passwords"
    
    Špatná: spatna (argument)
    """
    return ""  # TODO: ↓ přepiš na lepší zprávu


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Základní Git příkazy",
        theory="""GIT = distribuovaný verzovací systém.

Základní workflow:
  git init                  # vytvoř repo
  git status                # co se změnilo?
  git add .                 # přidej do staging
  git commit -m "zpráva"    # ulož snapshot
  git log                   # historie
  git diff                  # co se liší?

Staging area = "přípravná zóna" před commitem.
Můžeš vybrat JEN některé soubory k commitnutí.""",
        task="Vyplň správné Git příkazy.",
        difficulty=1, points=15,
        hints=["git init, git status, git add ., git commit -m 'zpráva'"],
        tests=[
            lambda: verify(git_init_prikaz() == "git init", "git init ✓"),
            lambda: verify(git_status_prikaz() == "git status", "git status ✓"),
            lambda: verify(git_add_vse() == "git add .", "git add . ✓"),
            lambda: verify(git_commit_msg() == "git commit -m 'Initial commit'", "git commit ✓"),
        ]
    ),
    Challenge(
        title="Tři oblasti Gitu",
        theory="""GIT MÁ 3 OBLASTI:
  ┌─────────────────┐
  │ Working Dir      │ ← edituješ soubory
  └───────┬─────────┘
          │ git add
  ┌───────▼─────────┐
  │ Staging Area     │ ← připraveno k commitu
  └───────┬─────────┘
          │ git commit
  ┌───────▼─────────┐
  │ Repository       │ ← uložená historie
  └─────────────────┘""",
        task="Pojmenuj 3 oblasti Gitu.",
        difficulty=1, points=10,
        hints=["working directory → staging area → repository"],
        tests=[
            lambda: (
                lambda o: verify(
                    "working" in o["oblast_1"].lower() and
                    "staging" in o["oblast_2"].lower() and
                    "repository" in o["oblast_3"].lower(),
                    "3 oblasti ✓"
                )
            )(git_oblasti()),
        ]
    ),
    Challenge(
        title=".gitignore vzory",
        theory=""".gitignore — soubory, co Git IGNORUJE:
  __pycache__/      # Python cache
  *.pyc             # kompilované Python soubory
  venv/             # virtual environment
  .env              # secrety a konfigurace
  *.log             # log soubory
  .idea/            # IDE konfigurace

NIKDY necommituj: hesla, API klíče, velké datové soubory!""",
        task="Napiš typické .gitignore vzory pro Python projekt.",
        difficulty=1, points=10,
        hints=["__pycache__/, venv/, .env"],
        tests=[
            lambda: (
                lambda vzory: verify(
                    any("pycache" in v for v in vzory) and
                    any("venv" in v for v in vzory) and
                    any(".env" in v for v in vzory),
                    ".gitignore ✓",
                    f"Vzory: {vzory}"
                )
            )(gitignore_vzory()),
        ]
    ),
    Challenge(
        title="Git log a diff",
        task="Příkazy pro historii a porovnání změn.",
        difficulty=1, points=10,
        hints=["git log --oneline, git diff --staged"],
        tests=[
            lambda: verify(git_log_oneline() == "git log --oneline", "Log ✓"),
            lambda: verify(git_diff_staged() == "git diff --staged", "Diff ✓"),
        ]
    ),
    Challenge(
        title="Dobrá commit zpráva",
        theory="""PRAVIDLA pro commit zprávy:
1. Imperativ: "Add feature" ne "Added feature"
2. Max 50 znaků pro subject
3. Popis CO a PROČ (ne jak)
4. Velké první písmeno

ŠPATNĚ:              DOBŘE:
"update"              "Add user authentication"
"fix bug"             "Fix null pointer in login"
"asdf"                "Refactor database queries" """,
        task="Přepiš 'changed some things' na dobrou zprávu.",
        difficulty=1, points=15,
        hints=["Imperativ, specificky, max 50 znaků"],
        tests=[
            lambda: (
                lambda z: verify(
                    len(z) > 5 and len(z) <= 50 and z[0].isupper(),
                    "Dobrá zpráva ✓",
                    f"Zpráva: '{z}'"
                )
            )(dobra_zprava("changed some things")),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Git — Základy", "04_01")
