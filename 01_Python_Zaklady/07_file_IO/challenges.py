#!/usr/bin/env python3
"""
🐍 PYTHON ZÁKLADY — Práce se soubory (File I/O)
Čtení a zápis dat — základ pro jakoukoliv reálnou aplikaci.
"""
import sys, os, json, csv, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# Dočasný adresář pro testovací soubory
TEMP = tempfile.mkdtemp()

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def vyzva_1(cesta, obsah):
    """
    🎯 Zapiš text do souboru. Použij 'with' statement.
    Pokud soubor existuje, přepiš ho.
    """
    # TODO: ↓
    pass

def vyzva_2(cesta):
    """
    🎯 Přečti celý obsah souboru a vrať ho jako string.
    Použij 'with' statement.
    """
    # TODO: ↓
    pass

def vyzva_3(cesta):
    """
    🎯 Přečti soubor po řádcích a vrať list řádků (bez \\n na konci).
    """
    # TODO: ↓
    pass

def vyzva_4(cesta, data):
    """
    🎯 Ulož slovník jako JSON soubor (s odsazením 2 mezery, ensure_ascii=False).
    """
    # TODO: ↓
    pass

def vyzva_5(cesta):
    """
    🎯 Načti JSON soubor a vrať obsah jako Python objekt (dict/list).
    """
    # TODO: ↓
    pass

def vyzva_6(cesta, radky):
    """
    🎯 Zapiš CSV soubor. 'radky' je list of lists.
    První řádek je hlavička.
    Příklad: [["jmeno","vek"], ["Jan",25], ["Eva",30]]
    """
    # TODO: Použij csv modul ↓
    pass

def vyzva_7(cesta):
    """
    🎯 Načti CSV soubor a vrať list slovníků.
    Příklad CSV:
      jmeno,vek
      Jan,25
    Výstup: [{"jmeno": "Jan", "vek": "25"}]
    """
    # TODO: Použij csv.DictReader ↓
    pass

# ============================================================
# 🔍 TESTY
# ============================================================

def _setup_test_file(name, content):
    path = os.path.join(TEMP, name)
    with open(path, 'w') as f:
        f.write(content)
    return path

challenges = [
    Challenge(
        title="Zápis do souboru — with open()",
        theory="""'with' automaticky zavře soubor:
  with open("soubor.txt", "w") as f:
      f.write("obsah")

Módy: "r" čtení, "w" zápis, "a" přidání, "r+" čtení+zápis""",
        task="Zapiš text do souboru pomocí with.",
        difficulty=1, points=10,
        hints=["with open(cesta, 'w') as f: f.write(obsah)"],
        tests=[
            lambda: (
                vyzva_1(os.path.join(TEMP, "test1.txt"), "Ahoj!"),
                verify(
                    open(os.path.join(TEMP, "test1.txt")).read() == "Ahoj!",
                    "Zápis do souboru ✓"
                )
            )[1],
        ]
    ),
    Challenge(
        title="Čtení souboru",
        task="Přečti celý soubor jako string.",
        difficulty=1, points=10,
        hints=["with open(cesta, 'r') as f: return f.read()"],
        tests=[
            lambda: verify(
                vyzva_2(_setup_test_file("test2.txt", "Hello World")) == "Hello World",
                "Čtení ✓"
            ),
        ]
    ),
    Challenge(
        title="Řádky souboru",
        theory=""".readlines() vrátí list řádků (s \\n).
.read().splitlines() vrátí list řádků (bez \\n).
Nebo: [line.strip() for line in f]""",
        task="Vrať řádky jako list bez \\n.",
        difficulty=1, points=10,
        hints=["return f.read().splitlines()"],
        tests=[
            lambda: verify(
                vyzva_3(_setup_test_file("test3.txt", "a\nb\nc")) == ["a", "b", "c"],
                "Řádky ✓"
            ),
        ]
    ),
    Challenge(
        title="JSON zápis",
        theory="""JSON je univerzální formát pro data:
  import json
  json.dump(data, f, indent=2)     # do souboru
  json.dumps(data, indent=2)       # do stringu""",
        task="Ulož slovník jako JSON.",
        difficulty=1, points=10,
        hints=["json.dump(data, f, indent=2, ensure_ascii=False)"],
        tests=[
            lambda: (
                vyzva_4(os.path.join(TEMP, "test.json"), {"jmeno": "Jan", "vek": 25}),
                verify(
                    json.load(open(os.path.join(TEMP, "test.json"))) == {"jmeno": "Jan", "vek": 25},
                    "JSON zápis ✓"
                )
            )[1],
        ]
    ),
    Challenge(
        title="JSON čtení",
        task="Načti JSON soubor.",
        difficulty=1, points=10,
        hints=["return json.load(f)"],
        tests=[
            lambda: verify(
                vyzva_5(_setup_test_file("read.json", '{"a": 1, "b": 2}')) == {"a": 1, "b": 2},
                "JSON čtení ✓"
            ),
        ]
    ),
    Challenge(
        title="CSV zápis",
        theory="""CSV (Comma-Separated Values):
  import csv
  writer = csv.writer(f)
  writer.writerow(["jmeno", "vek"])
  writer.writerow(["Jan", 25])""",
        task="Zapiš data jako CSV.",
        difficulty=2, points=15,
        hints=["writer = csv.writer(f); writer.writerows(radky)"],
        tests=[
            lambda: (
                vyzva_6(os.path.join(TEMP, "test.csv"), [["jmeno","vek"],["Jan","25"]]),
                verify(
                    open(os.path.join(TEMP, "test.csv")).read().strip().replace('\r\n','\n') == "jmeno,vek\nJan,25",
                    "CSV zápis ✓"
                )
            )[1],
        ]
    ),
    Challenge(
        title="CSV čtení jako slovníky",
        theory="""csv.DictReader čte CSV s hlavičkou:
  reader = csv.DictReader(f)
  for row in reader:
      print(row["jmeno"])  # přístup přes klíče""",
        task="Načti CSV a vrať list slovníků.",
        difficulty=2, points=15,
        hints=["return list(csv.DictReader(f))"],
        tests=[
            lambda: verify(
                vyzva_7(_setup_test_file("read.csv", "jmeno,vek\nJan,25\nEva,30"))
                == [{"jmeno": "Jan", "vek": "25"}, {"jmeno": "Eva", "vek": "30"}],
                "CSV → dict ✓"
            ),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Python Základy — File I/O", "01_07")
