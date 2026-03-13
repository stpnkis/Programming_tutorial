#!/usr/bin/env python3
"""🐼 Pandas & Data Prep — Načítání, čištění, transformace dat."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def vytvor_dataframe():
    """
    🎯 VÝZVA 1: Vytvoř DataFrame z dict.
    data = {
        "jmeno": ["Alice", "Bob", "Charlie", "Diana"],
        "vek": [25, 30, 35, 28],
        "plat": [50000, 60000, 70000, 55000],
        "mesto": ["Praha", "Brno", "Praha", "Ostrava"]
    }
    Vrať pd.DataFrame(data)
    """
    # TODO: ↓
    pass


def filtrovani(df):
    """
    🎯 VÝZVA 2: Filtrování a výběr.
    Vrať DataFrame obsahující jen řádky kde:
    - vek > 27 AND plat >= 55000
    """
    # TODO: ↓
    pass


def agregace(df):
    """
    🎯 VÝZVA 3: Groupby a agregace.
    Seskup dle 'mesto' a spočítej průměrný plat.
    Vrať dict {mesto: prumerny_plat}
    """
    # TODO: ↓
    pass


def chybejici_data():
    """
    🎯 VÝZVA 4: Práce s chybějícími daty (NaN).
    Vytvoř DataFrame:
    data = {"A": [1, None, 3, None, 5], "B": [10, 20, None, 40, 50]}
    - Vyplň NaN v sloupci A mediánem sloupce A
    - Smaž řádky kde B je NaN
    Vrať výsledný DataFrame.
    """
    # TODO: ↓
    pass


def feature_columns():
    """
    🎯 VÝZVA 5: Nové sloupce a transformace.
    df = vytvor_dataframe()
    - Přidej sloupec 'plat_mesicni' = plat / 12 (zaokrouhli na int)
    - Přidej 'senior' = True pokud vek >= 30, jinak False
    Vrať upravený DataFrame.
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

def _make_df():
    if not HAS_PANDAS:
        return None
    return pd.DataFrame({
        "jmeno": ["Alice", "Bob", "Charlie", "Diana"],
        "vek": [25, 30, 35, 28],
        "plat": [50000, 60000, 70000, 55000],
        "mesto": ["Praha", "Brno", "Praha", "Ostrava"]
    })

challenges = [
    Challenge(
        title="Vytvoření DataFrame",
        theory="""PANDAS DATAFRAME:
  import pandas as pd

  df = pd.DataFrame({"col1": [1,2], "col2": [3,4]})
  df.head()        # prvních 5 řádků
  df.shape          # (počet_řádků, počet_sloupců)
  df.dtypes         # datové typy sloupců
  df.describe()     # statistiky
  df.info()         # info o DataFrame""",
        task="Vytvoř DataFrame z dict.",
        difficulty=1, points=10,
        hints=["pd.DataFrame(data)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and hasattr(r, 'shape') and r.shape == (4, 4),
                    "DataFrame 4x4 ✓"
                )
            )(vytvor_dataframe()) if HAS_PANDAS else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Filtrování dat",
        theory="""FILTROVÁNÍ V PANDAS:
  df[df["vek"] > 25]              # jednoduchá podmínka
  df[(df["vek"] > 25) & (df["plat"] > 50000)]  # AND
  df[(df["vek"] > 25) | (df["plat"] > 50000)]  # OR
  df.query("vek > 25 and plat > 50000")         # alternativa

  df.loc[row_label, col_label]   # výběr dle label
  df.iloc[row_idx, col_idx]      # výběr dle indexu""",
        task="Filtruj: vek > 27 AND plat >= 55000.",
        difficulty=1, points=15,
        hints=["df[(df['vek'] > 27) & (df['plat'] >= 55000)]"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 3,
                    "3 řádky po filtrování ✓"
                )
            )(filtrovani(_make_df())) if HAS_PANDAS else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Groupby a agregace",
        theory="""GROUPBY:
  df.groupby("mesto")["plat"].mean()
  df.groupby("mesto").agg({"plat": "mean", "vek": "max"})

  .sum(), .mean(), .count(), .min(), .max(), .std()""",
        task="Průměrný plat dle města.",
        difficulty=2, points=20,
        hints=["df.groupby('mesto')['plat'].mean().to_dict()"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and r.get("Praha") == 60000 and r.get("Brno") == 60000,
                    "Průměry dle města ✓"
                )
            )(agregace(_make_df())) if HAS_PANDAS else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Chybějící data (NaN)",
        theory="""NaN HANDLING:
  df.isna()           # maska NaN
  df.isna().sum()     # počet NaN v každém sloupci
  df.dropna()         # smaž řádky s NaN
  df.fillna(0)        # nahraď NaN nulou
  df["A"].fillna(df["A"].median())  # mediánem""",
        task="Vyplň NaN mediánem, smaž zbylé NaN řádky.",
        difficulty=2, points=20,
        hints=["fillna(median) pro A, dropna(subset=['B']) pro B"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and r.isna().sum().sum() == 0,
                    "Žádné NaN ✓"
                )
            )(chybejici_data()) if HAS_PANDAS else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Nové sloupce a transformace",
        task="Přidej plat_mesicni a senior sloupce.",
        difficulty=1, points=15,
        hints=["df['plat_mesicni'] = (df['plat'] / 12).astype(int)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "plat_mesicni" in r.columns and "senior" in r.columns,
                    "Nové sloupce ✓"
                )
            )(feature_columns()) if HAS_PANDAS else verify(True, "Skip"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Pandas & Data Prep", "08_01")
