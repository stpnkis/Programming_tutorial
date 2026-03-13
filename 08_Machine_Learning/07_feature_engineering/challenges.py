#!/usr/bin/env python3
"""🔧 Feature Engineering — Výběr, transformace, encoding."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def one_hot_rucne(kategorie: list) -> list:
    """
    🎯 VÝZVA 1: One-Hot Encoding ručně.
    kategorie = ["červená", "modrá", "zelená", "červená", "modrá"]
    Unikátní: ["červená", "modrá", "zelená"] (v pořadí výskytu)
    Vrať list of lists:
    [[1,0,0], [0,1,0], [0,0,1], [1,0,0], [0,1,0]]
    """
    # TODO: ↓
    pass


def label_encoding(kategorie: list) -> list:
    """
    🎯 VÝZVA 2: Label Encoding ručně.
    Přiřaď kategoriím čísla (dle abecedního pořadí):
    ["malý", "střední", "velký", "malý"] → [0, 1, 2, 0]
    """
    # TODO: ↓
    pass


def normalizace_minmax(data: list) -> list:
    """
    🎯 VÝZVA 3: Min-Max normalizace ručně.
    x_norm = (x - min) / (max - min) → rozsah [0, 1]
    data = [10, 20, 30, 40, 50]
    → [0.0, 0.25, 0.5, 0.75, 1.0]
    """
    # TODO: ↓
    pass


def feature_selection_teorie():
    """
    🎯 VÝZVA 4: Metody výběru features.
    Vrať dict:
    {
        "filter": {"princip": "statistické testy (korelace, chi2)", "příklad": "odstranit features s nízkou korelací"},
        "wrapper": {"princip": "hledání nejlepší podmnožiny", "příklad": "forward/backward selection"},
        "embedded": {"princip": "výběr během trénování", "příklad": "Lasso (L1), feature_importances_ u stromů"},
        "dimenze": {"PCA": "Principal Component Analysis — projekce do nižší dimenze",
                    "kdy": "příliš mnoho features, korelované features"}
    }
    """
    # TODO: ↓
    pass


def vytvor_features(data: list) -> list:
    """
    🎯 VÝZVA 5: Vytvoř nové features z existujících.
    data = dicts: [{"výška": 180, "váha": 80}, ...]
    Pro každý záznam přidej:
    - bmi: váha / (výška/100)²
    - kategorie_bmi: "podváha" (<18.5), "norma" (18.5-25), "nadváha" (>25)
    Vrať list dicts s přidanými klíči.
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="One-Hot Encoding",
        theory="""ONE-HOT ENCODING:
  Kategorie → binární vektory

  "červená" → [1, 0, 0]
  "modrá"  → [0, 1, 0]
  "zelená" → [0, 0, 1]

  Pandas: pd.get_dummies(df["barva"])
  Sklearn: OneHotEncoder().fit_transform(X)

  Problém: prokletí dimenzionality u mnoha kategorií""",
        task="Implementuj one-hot encoding ručně.",
        difficulty=2, points=20,
        hints=["Najdi unikátní, pro každý prvek vytvoř vektor s 1 na správné pozici"],
        tests=[
            lambda: (
                lambda r: verify(
                    r == [[1,0,0],[0,1,0],[0,0,1],[1,0,0],[0,1,0]],
                    "One-hot ✓"
                )
            )(one_hot_rucne(["červená", "modrá", "zelená", "červená", "modrá"])),
        ]
    ),
    Challenge(
        title="Label Encoding",
        theory="""LABEL ENCODING:
  Kategorie → čísla (abecedně):
  "malý"=0, "střední"=1, "velký"=2

  Sklearn: LabelEncoder().fit_transform(data)

  ⚠️ POZOR: Label encoding implikuje pořadí!
  Červená=0, Modrá=1, Zelená=2 → model si myslí Zelená > Červená
  → Pro nominální data použij One-Hot!""",
        task="Implementuj label encoding dle abecedy.",
        difficulty=1, points=10,
        hints=["sorted(set(data)) pro pořadí, pak index"],
        tests=[
            lambda: verify(
                label_encoding(["malý", "střední", "velký", "malý"]) == [0, 1, 2, 0],
                "Label encoding ✓"
            ),
        ]
    ),
    Challenge(
        title="Min-Max normalizace",
        theory="""MIN-MAX NORMALIZACE:
  x_norm = (x - min) / (max - min)
  → Výstup v rozsahu [0, 1]

  Sklearn: MinMaxScaler().fit_transform(X)

  STANDARDIZACE (z-score):
  z = (x - μ) / σ → mean=0, std=1
  Sklearn: StandardScaler()

  Kdy co:
  - Min-Max: poznáme rozsah, neuronové sítě
  - Z-score: outliers, SVM, lineární modely""",
        task="Min-Max normalizace ručně.",
        difficulty=1, points=10,
        hints=["(x - min(data)) / (max(data) - min(data))"],
        tests=[
            lambda: verify(
                normalizace_minmax([10, 20, 30, 40, 50]) == [0.0, 0.25, 0.5, 0.75, 1.0],
                "Min-Max ✓"
            ),
        ]
    ),
    Challenge(
        title="Feature Selection teorie",
        task="Popiš filter, wrapper, embedded metody.",
        difficulty=2, points=20,
        hints=["filter=statistika, wrapper=podmnožiny, embedded=L1/stromy"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "filter" in r and "wrapper" in r and "embedded" in r,
                    "3 metody výběru ✓"
                )
            )(feature_selection_teorie()),
        ]
    ),
    Challenge(
        title="Feature Engineering — BMI",
        theory="""FEATURE ENGINEERING:
  Vytváření nových features z existujících:
  - Matematické: BMI = weight / height²
  - Binning: věk → kategorie (mladý/střední/starý)
  - Interakce: plocha = šířka * výška
  - Časové: den_v_týdnu, měsíc, is_weekend""",
        task="Spočítej BMI a kategorizuj.",
        difficulty=2, points=25,
        hints=["bmi = váha / (výška/100)**2"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 2
                    and abs(r[0]["bmi"] - 24.69) < 0.1
                    and r[1]["kategorie_bmi"] == "nadváha",
                    "BMI ✓"
                )
            )(vytvor_features([{"výška": 180, "váha": 80}, {"výška": 170, "váha": 90}])),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Feature Engineering", "08_07")
