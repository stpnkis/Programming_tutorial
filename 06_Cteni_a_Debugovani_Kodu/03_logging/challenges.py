#!/usr/bin/env python3
"""📝 Logging — Profesionální logování."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify
import logging

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

# 🎯 VÝZVA 1: Logging úrovně
def logging_urovne() -> list:
    """
    Vrať logging úrovně od nejnižší po nejvyšší:
    ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    """
    return []  # TODO: ↓

def kdy_pouzit() -> dict:
    """Kdy použít kterou úroveň?"""
    return {
        "DEBUG": "",     # TODO: ↓
        "INFO": "",      # TODO: ↓
        "WARNING": "",   # TODO: ↓
        "ERROR": "",     # TODO: ↓
        "CRITICAL": "",  # TODO: ↓
    }

# 🎯 VÝZVA 2: Logger třída
class SimpleLogger:
    """
    🎯 Vlastní logger (simulace).
    - __init__(nazev, uroven="INFO")
    - log(uroven, zprava) → přidá do záznamy pokud uroven >= nastavené
    - debug/info/warning/error(zprava) — zkratky
    - zaznamy → list zpráv (formát: "[UROVEN] zprava")
    
    Pořadí: DEBUG < INFO < WARNING < ERROR < CRITICAL
    """
    UROVNE = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
    
    # TODO: ↓
    pass


# 🎯 VÝZVA 3: Strukturované logování
def log_format_zprava(uzivatel: str, akce: str, stav: str, **extra) -> str:
    """
    Formátuj log zprávu jako strukturovanou:
    "[2024-01-01] user=jan action=login status=ok ip=1.2.3.4"
    
    Formát: "[DATE] user={uzivatel} action={akce} status={stav} {extra}"
    Pro DATE použij "LOG" (zjednodušení).
    """
    # TODO: ↓
    pass

# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Logging úrovně",
        theory="""LOGGING > print()

print() = debug, smažeš pak
logging = profesi, zůstane, konfigurovatelné

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Detailní info pro vývojáře")
logger.info("Normální provoz")
logger.warning("Pozor, něco podezřelého")
logger.error("Chyba! Ale program běží dál")
logger.critical("Fatální chyba!")

V produkci: level=WARNING (debug/info se nezobrazí)""",
        task="Seřaď logging úrovně a popiš kdy je použít.",
        difficulty=1, points=15,
        hints=["DEBUG < INFO < WARNING < ERROR < CRITICAL"],
        tests=[
            lambda: verify(
                logging_urovne() == ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                "Úrovně ✓"
            ),
            lambda: verify(
                all(len(kdy_pouzit()[k]) > 5 for k in kdy_pouzit()),
                "Popisy ✓"
            ),
        ]
    ),
    Challenge(
        title="SimpleLogger třída",
        task="Logger s filtrováním podle úrovně.",
        difficulty=2, points=25,
        hints=[
            "self._uroven = uroven; self._zaznamy = []",
            "if UROVNE[uroven] >= UROVNE[self._uroven]: append"
        ],
        tests=[
            lambda: (
                lambda l: (l.info("start"), l.debug("detail"),
                    verify(len(l.zaznamy) == 1 and "[INFO]" in l.zaznamy[0],
                           "INFO logger filtruje DEBUG ✓"))
            )(SimpleLogger("test", "INFO"))[2],
            lambda: (
                lambda l: (l.warning("pozor"), l.error("chyba"),
                    verify(len(l.zaznamy) == 2, "WARNING+ERROR ✓"))
            )(SimpleLogger("test", "WARNING"))[2],
        ]
    ),
    Challenge(
        title="Strukturované logování",
        theory="""STRUKTUROVANÉ LOGY = strojově čitelné:
  [LOG] user=jan action=login status=ok ip=1.2.3.4

Proč? Snadné parsování, filtrování, hledání v logách.
V produkci: JSON formát pro ELK/Grafana.""",
        task="Formátuj strukturovanou log zprávu.",
        difficulty=1, points=15,
        hints=["f'[LOG] user={uzivatel} action={akce} status={stav}'"],
        tests=[
            lambda: (
                lambda z: verify(
                    "user=jan" in z and "action=login" in z and "status=ok" in z,
                    "Struktura ✓"
                )
            )(log_format_zprava("jan", "login", "ok", ip="1.2.3.4")),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Logging", "06_03")
