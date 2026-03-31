# 📝 Autorský průvodce — jak psát obsah

Tento dokument popisuje, jak vytvářet nové lekce a výzvy pro Programátorské Tréninkové Centrum.

## Struktura adresářů

```
XX_Nazev_Sekce/
├── README.md               # Popis sekce
├── YY_nazev_lekce/
│   ├── challenges.py       # Výzvy s testy  ← povinné
│   ├── lesson.yaml         # Metadata       ← povinné
│   └── README.md           # Doplňující materiály (volitelné)
```

## lesson.yaml — metadata lekce

Každá lekce **musí** mít soubor `lesson.yaml`:

```yaml
id: "01.03"                          # sekce.lekce
title: "Funkce"                       # název lekce
summary: "Nauč se definovat a používat funkce v Pythonu."
difficulty: 1                         # 1-3 (1=začátečník)
estimated_minutes: 30
tags: ['python', 'functions']
prerequisites: ['01.02']              # lesson IDs
learning_objectives:
  - "Definovat funkci s parametry"
  - "Používat return hodnoty"

challenges:
  - id: 1
    title: "Základní funkce"
    type: implementation              # viz níže
    difficulty: 1
    points: 10
  - id: 2
    title: "Funkce s parametry"
    type: implementation
    difficulty: 1
    points: 15
```

### Typy výzev

| Typ              | Kdy použít                                       |
|------------------|--------------------------------------------------|
| `implementation` | Student píše kód od nuly (výchozí)               |
| `debugging`      | Student opravuje chybný kód                      |
| `refactoring`    | Student přepíše kód na lepší verzi               |
| `knowledge`      | Teoretická otázka (vrací správnou odpověď)        |

### Obtížnost

| Hodnota | Význam      | Typický čas |
|---------|-------------|-------------|
| 1       | Začátečník  | 5-10 min    |
| 2       | Pokročilý   | 10-20 min   |
| 3       | Expert      | 20+ min     |

### Body

- 10b = jednoduchá výzva
- 15b = středně těžká
- 20b = obtížná
- 25-30b = expertní

## challenges.py — výzvy s testy

```python
from engine.models import Challenge

def vyzva_1():
    \"\"\"
    📝 TEORIE:
    Funkce jsou základním stavebním kamenem programů.
    Definují se klíčovým slovem `def`.

    📌 PŘÍKLAD:
    >>> def pozdrav(jmeno):
    ...     return f"Ahoj, {jmeno}!"

    🎯 ÚKOL:
    Napiš funkci `secti(a, b)`, která vrátí součet dvou čísel.

    💡 HINTY:
    - Použij klíčové slovo `def`
    - Nezapomeň na `return`
    \"\"\"
    def secti(a, b):
        pass  # <- student doplní

    return Challenge(
        title="Základní funkce",
        tasks=[secti],
        tests=[
            lambda: secti(1, 2) == 3,
            lambda: secti(-1, 1) == 0,
            lambda: secti(0, 0) == 0,
        ],
        points=10,
        hints=[
            "Použij def secti(a, b): ...",
            "Nezapomeň na return a + b",
        ],
    )
```

### Konvence pro challenges.py

1. **Název funkce**: `vyzva_N` kde N je pořadové číslo (1, 2, 3...)
2. **Docstring**: Obsahuje teorii (📝), příklad (📌), úkol (🎯) a hinty (💡)
3. **Testy**: Seznam lambda funkcí — vrací `True`/`False`
4. **Hinty**: Od nejobecnějšího po nejkonkrétnější
5. **Return**: Vždy vrací instanci `Challenge()`

### Emoji sekce v docstringu

| Emoji | Sekce      |
|-------|------------|
| 📝    | TEORIE     |
| 📌    | PŘÍKLAD    |
| 🎯    | ÚKOL       |
| 💡    | HINTY      |

## Validace

Po vytvoření obsahu spusťte validátor:

```bash
# Validovat vše
python3 -m engine.validator

# Validovat jednu sekci
python3 -m engine.validator 01

# Generovat lesson.yaml z existujícího obsahu
python3 -m engine.scaffold

# Přegenerovat (přepsat existující)
python3 -m engine.scaffold --overwrite
```

## Checklist pro novou lekci

- [ ] Vytvořen adresář `XY_nazev_lekce/`
- [ ] Vytvořen `challenges.py` s `vyzva_N()` funkcemi
- [ ] Každá výzva má docstring s 📝, 📌, 🎯
- [ ] Testy pokrývají edge-cases
- [ ] Hinty jsou srozumitelné a akční
- [ ] Vytvořen `lesson.yaml` s explicitními typy
- [ ] Body odpovídají obtížnosti
- [ ] `python3 -m engine.validator` hlásí 0 chyb
- [ ] Testy projdou: `python3 -m pytest tests/ -v`
