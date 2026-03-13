#!/usr/bin/env python3
"""📜 Bash Scripting — proměnné, podmínky, cykly, funkce, argumenty."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def promenne_a_zaklady():
    """
    🎯 VÝZVA 1: Proměnné a základy Bash skriptů.
    Vrať dict:
    {
        "shebang": "#!/usr/bin/env bash  # nebo #!/bin/bash",
        "spuštění": ["chmod +x skript.sh", "./skript.sh", "bash skript.sh"],
        "proměnné": {
            "přiřazení": "JMENO='Karel'  # bez mezer kolem =",
            "použití": "echo $JMENO nebo echo ${JMENO}",
            "readonly": "readonly PI=3.14159",
            "export": "export PATH=$PATH:/nová/cesta  # viditelná pro podprocesy"
        },
        "uvozovky": {
            "dvojité": "\"text $PROMĚNNÁ\"  # expanduje proměnné",
            "jednoduché": "'text $PROMĚNNÁ'  # bere doslova",
            "backtick": "výsledek=$(příkaz)  # zachytí výstup příkazu"
        },
        "speciální_proměnné": {
            "$0": "název skriptu",
            "$1 .. $9": "poziční argumenty",
            "$#": "počet argumentů",
            "$@": "všechny argumenty jako seznam",
            "$?": "exit kód posledního příkazu",
            "$$": "PID aktuálního shellu",
            "$!": "PID posledního procesu na pozadí"
        }
    }
    """
    # TODO: ↓
    pass


def podminky_if():
    """
    🎯 VÝZVA 2: Podmínky a testování v Bash.
    Vrať dict:
    {
        "if_syntaxe": [
            "if [ podmínka ]; then",
            "    příkazy",
            "elif [ jiná_podmínka ]; then",
            "    příkazy",
            "else",
            "    příkazy",
            "fi"
        ],
        "číselné_porovnání": {
            "-eq": "rovná se (equal)",
            "-ne": "nerovná se (not equal)",
            "-lt": "menší než (less than)",
            "-le": "menší nebo rovno",
            "-gt": "větší než (greater than)",
            "-ge": "větší nebo rovno"
        },
        "řetězcové_porovnání": {
            "==": "rovnají se",
            "!=": "nerovnají se",
            "-z": "prázdný řetězec",
            "-n": "neprázdný řetězec"
        },
        "souborové_testy": {
            "-f": "existuje a je soubor",
            "-d": "existuje a je adresář",
            "-e": "existuje (cokoliv)",
            "-r": "čitelný",
            "-w": "zapisovatelný",
            "-x": "spustitelný"
        },
        "logické_operátory": {
            "&&": "a zároveň (AND)",
            "||": "nebo (OR)",
            "!": "negace (NOT)"
        },
        "příklad": "if [ -f \"$SOUBOR\" ] && [ -r \"$SOUBOR\" ]; then cat \"$SOUBOR\"; fi"
    }
    """
    # TODO: ↓
    pass


def cykly():
    """
    🎯 VÝZVA 3: Cykly v Bash (for, while, until).
    Vrať dict:
    {
        "for_seznam": [
            "for POLOZKA in jablko hruška švestka; do",
            "    echo \"Ovoce: $POLOZKA\"",
            "done"
        ],
        "for_rozsah": [
            "for I in {1..10}; do",
            "    echo \"Číslo: $I\"",
            "done"
        ],
        "for_c_styl": [
            "for ((I=0; I<10; I++)); do",
            "    echo \"Iterace $I\"",
            "done"
        ],
        "for_soubory": [
            "for SOUBOR in *.txt; do",
            "    echo \"Zpracovávám: $SOUBOR\"",
            "done"
        ],
        "while": [
            "COUNTER=0",
            "while [ $COUNTER -lt 5 ]; do",
            "    echo \"Counter: $COUNTER\"",
            "    ((COUNTER++))",
            "done"
        ],
        "while_read": [
            "while IFS= read -r RADEK; do",
            "    echo \"Řádek: $RADEK\"",
            "done < soubor.txt"
        ],
        "break_continue": {
            "break": "ukončí cyklus",
            "continue": "přeskočí na další iteraci"
        }
    }
    """
    # TODO: ↓
    pass


def funkce_a_argumenty():
    """
    🎯 VÝZVA 4: Funkce a zpracování argumentů.
    Vrať dict:
    {
        "definice_funkce": [
            "#!/usr/bin/env bash",
            "",
            "pozdrav() {",
            "    local JMENO=$1  # lokální proměnná!",
            "    echo \"Ahoj, $JMENO!\"",
            "    return 0  # exit kód funkce",
            "}",
            "",
            "pozdrav 'Karel'  # volání"
        ],
        "local": "local zabraňuje znečištění globálního namespace",
        "return": "return vrací exit kód (0-255), ne hodnotu!",
        "výstupní_hodnota": "výstup funkce = co vypíše na stdout; zachytíš přes VÝSLEDEK=$(funkce)",
        "argumenty_skriptu": {
            "základní": "$1, $2, ... poziční parametry",
            "getopt": "getopt/getopts pro přepínače jako -f soubor --verbose",
            "příklad_getopts": [
                "while getopts 'f:v' OPT; do",
                "    case $OPT in",
                "        f) SOUBOR=$OPTARG ;;",
                "        v) VERBOSE=1 ;;",
                "        ?) echo 'Neznámý přepínač'; exit 1 ;;",
                "    esac",
                "done"
            ]
        }
    }
    """
    # TODO: ↓
    pass


def exit_kody_a_debug():
    """
    🎯 VÝZVA 5: Exit kódy, ošetření chyb a ladění skriptů.
    Vrať dict:
    {
        "exit_kody": {
            "0": "úspěch",
            "1": "obecná chyba",
            "2": "chybné použití příkazu",
            "126": "příkaz nalezen, ale nelze spustit",
            "127": "příkaz nenalezen",
            "128+N": "ukončen signálem N (např. 130 = Ctrl+C = SIGINT)"
        },
        "ošetření_chyb": {
            "set -e": "ukonči skript při jakékoliv chybě",
            "set -u": "chyba při použití nedefinované proměnné",
            "set -o pipefail": "chyba pokud selže část roury",
            "doporučené": "set -euo pipefail  # na začátek každého skriptu",
            "trap": "trap 'cleanup' EXIT ERR  # spusť při ukončení/chybě"
        },
        "ladění": {
            "bash -x skript.sh": "zobrazí každý příkaz před spuštěním (trace)",
            "bash -n skript.sh": "zkontroluje syntaxi bez spuštění",
            "set -x / set +x": "toggle trace uvnitř skriptu",
            "shellcheck": "shellcheck skript.sh  # statická analýza"
        },
        "vzor_robustního_skriptu": [
            "#!/usr/bin/env bash",
            "set -euo pipefail",
            "",
            "readonly SKRIPT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)\"",
            "",
            "cleanup() { echo 'Čistím...'; }",
            "trap cleanup EXIT",
            "",
            "main() {",
            "    echo 'Hotovo'",
            "}",
            "",
            "main \"$@\""
        ]
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Proměnné a základy skriptů",
        theory="""Bash skript = soubor s příkazy:
  Shebang: #!/usr/bin/env bash
  Spuštění: chmod +x skript.sh && ./skript.sh

  Proměnné: JMENO='Karel' (bez mezer!)
  Použití: $JMENO nebo ${JMENO}
  Speciální: $0=název, $1..$9=argumenty,
             $#=počet, $?=exit kód, $$=PID""",
        task="Popiš základy Bash skriptování — shebang, proměnné, speciální proměnné.",
        difficulty=1, points=15,
        hints=["shebang, readonly, export, $0/$#/$?, dvojité vs jednoduché uvozovky"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "shebang" in r
                    and "proměnné" in r
                    and "speciální_proměnné" in r
                    and "$?" in r.get("speciální_proměnné", {}),
                    "Proměnné a základy ✓"
                )
            )(promenne_a_zaklady()),
        ]
    ),
    Challenge(
        title="Podmínky a testování",
        theory="""if/elif/else/fi — podmíněné větvení

  Testovací operátory:
  Číselné: -eq -ne -lt -le -gt -ge
  Řetězce: == != -z (prázdný) -n (neprázdný)
  Soubory: -f (soubor) -d (adresář) -e (existuje) -x (spustitelný)
  Logické: && || !

  [ podmínka ] — starý test (POSIX)
  [[ podmínka ]] — moderní (Bash, doporučeno)""",
        task="Popiš syntaxi if/elif/else a testovací operátory v Bash.",
        difficulty=2, points=20,
        hints=["if [ ] then elif else fi, -eq/-lt/-gt, -f/-d/-e, && || !"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "if_syntaxe" in r
                    and "číselné_porovnání" in r
                    and "souborové_testy" in r
                    and "-f" in r.get("souborové_testy", {}),
                    "Podmínky ✓"
                )
            )(podminky_if()),
        ]
    ),
    Challenge(
        title="Cykly",
        theory="""Cykly v Bash:

  for ITEM in seznam; do ... done
  for I in {1..10}; do ... done
  for ((I=0; I<N; I++)); do ... done
  for SOUBOR in *.txt; do ... done

  while [ podmínka ]; do ... done
  while read -r RADEK; do ... done < soubor.txt

  break — ukonči, continue — přeskoč iteraci""",
        task="Popiš různé varianty cyklů for a while v Bash, včetně čtení ze souboru.",
        difficulty=2, points=20,
        hints=["for in, {1..10}, C-styl for, while read, break, continue"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "for_rozsah" in r
                    and "while_read" in r
                    and "break_continue" in r
                    and isinstance(r.get("for_soubory"), list),
                    "Cykly ✓"
                )
            )(cykly()),
        ]
    ),
    Challenge(
        title="Funkce a argumenty",
        theory="""Funkce v Bash:
  nazev_funkce() { příkazy; }
  Voláme: nazev_funkce arg1 arg2

  DŮLEŽITÉ:
  - local proměnná — vyhni se globálnímu znečištění
  - return N — jen exit kód (0-255)
  - Výstup = stdout → zachyť přes $(funkce)

  Argumenty skriptu:
  getopts 'f:v' pro přepínače -f hodnota -v""",
        task="Popiš definici funkcí, local, return a zpracování přepínačů přes getopts.",
        difficulty=3, points=25,
        hints=["function() {}, local, return, $(funkce), getopts, $OPTARG"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "definice_funkce" in r
                    and "local" in r
                    and "argumenty_skriptu" in r
                    and "getopts" in str(r.get("argumenty_skriptu", {})),
                    "Funkce a argumenty ✓"
                )
            )(funkce_a_argumenty()),
        ]
    ),
    Challenge(
        title="Exit kódy a ladění",
        theory="""Robustní Bash skripty:
  set -e   — ukonči při chybě
  set -u   — chyba při nedefinované proměnné
  set -o pipefail — chyba v rouru

  Ladění:
  bash -x skript.sh  — trace každého příkazu
  bash -n skript.sh  — jen syntaktická kontrola
  shellcheck         — statická analýza

  Exit kódy: 0=OK, 1=chyba, 127=nenalezen, 128+N=signál""",
        task="Popiš exit kódy, ošetření chyb (set -euo pipefail, trap) a ladění Bash skriptů.",
        difficulty=3, points=25,
        hints=["set -euo pipefail, trap, exit 0/1, bash -x, bash -n, shellcheck"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "exit_kody" in r
                    and "0" in r.get("exit_kody", {})
                    and "ošetření_chyb" in r
                    and "set -e" in r.get("ošetření_chyb", {})
                    and "ladění" in r,
                    "Exit kódy a ladění ✓"
                )
            )(exit_kody_a_debug()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Bash Scripting", "11_02")
