#!/usr/bin/env python3
"""🐚 Bash Základy — cd, ls, cat, grep, pipe, redirect, chmod, man."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def navigace_a_soubory():
    """
    🎯 VÝZVA 1: Navigace a práce se soubory.
    Vrať dict s nejdůležitějšími příkazy:
    {
        "pwd": "vypíše aktuální adresář",
        "cd": {
            "domů": "cd ~ nebo cd",
            "nadřazený": "cd ..",
            "absolutní": "cd /etc/apt",
            "relativní": "cd ./podsložka",
            "předchozí": "cd -"
        },
        "ls": {
            "základní": "ls",
            "detailní": "ls -l",
            "skryté": "ls -a",
            "vše": "ls -la",
            "lidsky čitelné": "ls -lh"
        },
        "soubory": {
            "vytvoř": "touch soubor.txt",
            "smaž": "rm soubor.txt",
            "smaž_rekurzivně": "rm -rf složka/",
            "kopíruj": "cp zdroj.txt cíl.txt",
            "přesuň": "mv zdroj.txt cíl.txt",
            "vytvoř_složku": "mkdir -p cesta/ke/složce"
        }
    }
    """
    # TODO: ↓
    pass


def cteni_souboru():
    """
    🎯 VÝZVA 2: Čtení a zobrazování souborů.
    Vrať dict:
    {
        "cat": {
            "příkaz": "cat soubor.txt",
            "použití": "zobrazí celý soubor najednou",
            "více_souborů": "cat soubor1.txt soubor2.txt"
        },
        "less": {
            "příkaz": "less soubor.txt",
            "použití": "stránkování, q=quit, /=hledej, n=další nález",
            "výhoda": "nenahraje celý soubor do paměti"
        },
        "head": {
            "příkaz": "head -n 20 soubor.txt",
            "výchozí": "prvních 10 řádků"
        },
        "tail": {
            "příkaz": "tail -n 20 soubor.txt",
            "sledování_logu": "tail -f /var/log/syslog",
            "výchozí": "posledních 10 řádků"
        },
        "wc": {
            "řádky": "wc -l soubor.txt",
            "slova": "wc -w soubor.txt",
            "znaky": "wc -c soubor.txt"
        }
    }
    """
    # TODO: ↓
    pass


def grep_a_hledani():
    """
    🎯 VÝZVA 3: Hledání textu s grep.
    Vrať dict:
    {
        "základní": "grep 'vzor' soubor.txt",
        "ignoruj_velikost": "grep -i 'vzor' soubor.txt",
        "rekurzivní": "grep -r 'vzor' ./složka/",
        "čísla_řádků": "grep -n 'vzor' soubor.txt",
        "invertovaný": "grep -v 'vzor' soubor.txt  # řádky BEZ vzoru",
        "regex": "grep -E 'vzor[0-9]+' soubor.txt",
        "počet_nálezů": "grep -c 'vzor' soubor.txt",
        "jen_název_souboru": "grep -l 'vzor' *.txt",
        "příklady": [
            "grep -n 'ERROR' /var/log/syslog",
            "grep -r 'import os' ~/projekty/",
            "grep -v '^#' /etc/fstab  # bez komentářů"
        ],
        "alternativy": {
            "ripgrep": "rg 'vzor'  # rychlejší alternativa",
            "ack": "ack 'vzor'  # developer-friendly"
        }
    }
    """
    # TODO: ↓
    pass


def pipe_a_redirect():
    """
    🎯 VÝZVA 4: Roury (pipe) a přesměrování výstupu.
    Vrať dict:
    {
        "pipe": {
            "symbol": "|",
            "princip": "stdout jednoho příkazu → stdin druhého",
            "příklady": [
                "ls -la | grep '.py'",
                "cat soubor.txt | sort | uniq",
                "ps aux | grep python | head -5",
                "cat /var/log/syslog | grep ERROR | wc -l"
            ]
        },
        "redirect": {
            "přepis": "příkaz > soubor.txt  # přepíše obsah",
            "přidání": "příkaz >> soubor.txt  # přidá na konec",
            "stdin": "příkaz < soubor.txt  # čte ze souboru",
            "stderr_do_stdout": "příkaz 2>&1",
            "vše_do_souboru": "příkaz > soubor.txt 2>&1",
            "zahodit_výstup": "příkaz > /dev/null 2>&1"
        },
        "užitečné_filtry": {
            "sort": "sort soubor.txt  # seřadí řádky",
            "uniq": "sort | uniq  # odstraní duplicity",
            "cut": "cut -d':' -f1 /etc/passwd  # vyřízne sloupec",
            "awk": "awk '{print $1}' soubor.txt  # vypíše 1. sloupec",
            "sed": "sed 's/staré/nové/g' soubor.txt  # nahradí text",
            "tr": "echo 'VELKÁ' | tr 'A-Z' 'a-z'  # převede na malá"
        }
    }
    """
    # TODO: ↓
    pass


def opravneni_a_man():
    """
    🎯 VÝZVA 5: Oprávnění souborů a manuálové stránky.
    Vrať dict:
    {
        "chmod": {
            "symbolický": {
                "přidej_exec": "chmod +x skript.sh",
                "odeber_write": "chmod go-w soubor.txt",
                "nastav_read_only": "chmod a=r soubor.txt"
            },
            "numerický": {
                "rwxr-xr-x": "chmod 755 soubor  # vlastník vše, ostatní čtení+spuštění",
                "rw-r--r--": "chmod 644 soubor  # vlastník čtení+zápis, ostatní čtení",
                "rwx------": "chmod 700 soubor  # jen vlastník, vše",
                "výpočet": "r=4, w=2, x=1 → sečti pro každou skupinu"
            }
        },
        "chown": {
            "změň_vlastníka": "chown uživatel soubor.txt",
            "změň_skupinu": "chown uživatel:skupina soubor.txt",
            "rekurzivní": "chown -R uživatel:skupina složka/"
        },
        "ls_oprávnění": {
            "formát": "-rwxr-xr-x  1 uživatel skupina  1234 Jan  1 12:00 soubor",
            "pořadí": "typ | vlastník | skupina | ostatní"
        },
        "man": {
            "zobrazit": "man příkaz  # manuálová stránka",
            "hledat": "man -k klíčové_slovo",
            "sekce": "man 5 fstab  # sekce 5 = formáty souborů",
            "rychlá_nápověda": "příkaz --help"
        }
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Navigace a soubory",
        theory="""Základní navigace v Bash:
  pwd   — kde jsem?
  cd    — přejdi do adresáře (cd ~, cd .., cd -, cd /cesta)
  ls    — seznam souborů (-l detailní, -a skryté, -h čitelné velikosti)
  touch — vytvoř prázdný soubor
  mkdir -p — vytvoř celou cestu adresářů
  rm -rf — smaž rekurzivně (POZOR: nevratné!)
  cp / mv — kopíruj / přesuň""",
        task="Popiš příkazy pro navigaci v souborovém systému a práci se soubory.",
        difficulty=1, points=15,
        hints=["pwd, cd ~, cd .., ls -la, touch, mkdir -p, rm, cp, mv"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "cd" in r
                    and isinstance(r.get("cd"), dict)
                    and "ls" in r
                    and "soubory" in r,
                    "Navigace a soubory ✓"
                )
            )(navigace_a_soubory()),
        ]
    ),
    Challenge(
        title="Čtení souborů",
        theory="""Prohlížení obsahu souborů:
  cat  — celý soubor najednou (vhodné pro krátké soubory)
  less — stránkování (q=konec, /=hledej, n=další)
  head — prvních N řádků (výchozí 10)
  tail — posledních N řádků; -f sleduje přibývající obsah (logy!)
  wc   — počítej řádky (-l), slova (-w), znaky (-c)""",
        task="Popiš příkazy pro čtení a zobrazování obsahu souborů.",
        difficulty=1, points=15,
        hints=["cat, less, head -n, tail -f, wc -l"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "tail" in r
                    and "sledování_logu" in r.get("tail", {})
                    and "less" in r
                    and "wc" in r,
                    "Čtení souborů ✓"
                )
            )(cteni_souboru()),
        ]
    ),
    Challenge(
        title="grep a hledání",
        theory="""grep — hledání vzorů v textu:
  grep 'vzor' soubor   — základní vyhledávání
  -i   ignoruj velikost písmen
  -r   rekurzivní prohledávání složky
  -n   zobraz čísla řádků
  -v   invertuj (řádky BEZ vzoru)
  -c   počet nálezů
  -E   rozšířené regulární výrazy (ERE)
  -l   jen názvy souborů s nálezem""",
        task="Popiš parametry a použití příkazu grep, včetně příkladů.",
        difficulty=2, points=20,
        hints=["-i, -r, -n, -v, -c, -E, příklady s logy a kódem"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "rekurzivní" in r
                    and "invertovaný" in r
                    and isinstance(r.get("příklady"), list)
                    and len(r["příklady"]) >= 2,
                    "grep ✓"
                )
            )(grep_a_hledani()),
        ]
    ),
    Challenge(
        title="Pipe a přesměrování",
        theory="""Skládání příkazů — síla Unixové filozofie:
  |   (pipe) — stdout → stdin dalšího příkazu
  >   přepiš soubor
  >>  přidej na konec souboru
  <   čti ze souboru
  2>&1  přesměruj stderr na stdout
  /dev/null  černá díra (zahodí výstup)

  Filtry: sort, uniq, cut, awk, sed, tr""",
        task="Popiš roury (pipe) a přesměrování vstupů/výstupů v Bash.",
        difficulty=2, points=20,
        hints=["| pipe, > přepis, >> přidání, 2>&1, /dev/null, sort, awk, sed"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "pipe" in r
                    and isinstance(r["pipe"].get("příklady"), list)
                    and len(r["pipe"]["příklady"]) >= 3
                    and "redirect" in r
                    and "užitečné_filtry" in r,
                    "Pipe a redirect ✓"
                )
            )(pipe_a_redirect()),
        ]
    ),
    Challenge(
        title="Oprávnění a man",
        theory="""Oprávnění souborů (Unix permission model):
  ls -l zobrazí: -rwxr-xr-x (typ | owner | group | others)
  r=4, w=2, x=1 → chmod 755 = rwxr-xr-x

  chmod — změna oprávnění
  chown — změna vlastníka/skupiny

  Manuálové stránky:
  man příkaz   — plná dokumentace
  příkaz --help — stručná nápověda
  man -k klíč  — hledání v popisech""",
        task="Popiš systém oprávnění Unix (chmod, chown) a způsoby získání nápovědy (man).",
        difficulty=2, points=20,
        hints=["chmod 755, chmod +x, chown user:group, man, --help"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "chmod" in r
                    and "numerický" in r.get("chmod", {})
                    and "chown" in r
                    and "man" in r,
                    "Oprávnění a man ✓"
                )
            )(opravneni_a_man()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Bash Základy", "11_01")
