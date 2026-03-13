#!/usr/bin/env python3
"""🏷️ Klasifikace — KNN, SVM, Decision Tree, Random Forest."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import sklearn
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def knn_klasifikator():
    """
    🎯 VÝZVA 1: K-Nearest Neighbors.
    Vytvoř jednoduché 2D data:
    X = [[1,1],[1,2],[2,1],[5,5],[5,6],[6,5]]
    y = [0, 0, 0, 1, 1, 1]
    Nafituj KNeighborsClassifier(n_neighbors=3)
    Predikuj třídu bodu [3,3].
    Vrať int (0 nebo 1).
    """
    # TODO: ↓
    pass


def rozhodovaci_strom():
    """
    🎯 VÝZVA 2: Decision Tree Classifier.
    Stejná data jako výzva 1.
    Nafituj DecisionTreeClassifier(random_state=42)
    Vrať dict:
    - prediction: predikce pro [3,3]
    - hloubka: model.get_depth()
    """
    # TODO: ↓
    pass


def random_forest():
    """
    🎯 VÝZVA 3: Random Forest.
    Vrať dict popisující Random Forest:
    {
        "princip": "ansámbl rozhodovacích stromů",
        "agregace": "většinové hlasování (klasifikace)",
        "vyhody": ["odolnost proti overfitting", "není třeba feature scaling"],
        "parametry": ["n_estimators", "max_depth", "min_samples_split"]
    }
    """
    # TODO: ↓
    pass


def confusion_matrix_rucne(y_true, y_pred):
    """
    🎯 VÝZVA 4: Confusion matrix ručně.
    Pro binární klasifikaci (0/1):
    Vrať dict: TP, TN, FP, FN
    - TP = true=1, pred=1
    - TN = true=0, pred=0
    - FP = true=0, pred=1
    - FN = true=1, pred=0
    """
    # TODO: ↓
    pass


def metriky_klasifikace(y_true, y_pred):
    """
    🎯 VÝZVA 5: Klasifikační metriky.
    Na základě y_true a y_pred spočítej:
    - accuracy: (TP+TN) / (TP+TN+FP+FN)
    - precision: TP / (TP+FP)
    - recall: TP / (TP+FN)
    - f1: 2 * precision * recall / (precision + recall)
    Vrať dict.
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="K-Nearest Neighbors",
        theory="""KNN ALGORITMUS:
  1. Spočítej vzdálenost od nového bodu ke všem
  2. Vyber K nejbližších sousedů
  3. Hlasuj — většinová třída vyhrává

  from sklearn.neighbors import KNeighborsClassifier
  model = KNeighborsClassifier(n_neighbors=3)
  model.fit(X, y)
  model.predict([[3, 3]])

Výhody: jednoduchý, žádný trénink
Nevýhody: pomalý na velkých datech""",
        task="Nafituj KNN(k=3) a predikuj [3,3].",
        difficulty=1, points=15,
        hints=["KNeighborsClassifier(n_neighbors=3).fit(X, y).predict([[3,3]])"],
        tests=[
            lambda: verify(
                knn_klasifikator() in [0, 1],
                "KNN predikce ✓"
            ) if HAS_SKLEARN else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Rozhodovací strom",
        theory="""DECISION TREE:
  Dělí prostor příznaků pomocí podmínek:
  if x₁ < 3.5:
    if x₂ < 1.5: třída 0
    else: třída 0
  else: třída 1

  from sklearn.tree import DecisionTreeClassifier
  model = DecisionTreeClassifier(random_state=42)
  model.get_depth()  # hloubka stromu""",
        task="Nafituj Decision Tree.",
        difficulty=1, points=15,
        hints=["DecisionTreeClassifier(random_state=42).fit(X, y)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "prediction" in r and "hloubka" in r,
                    "Strom s prediction a depth ✓"
                )
            )(rozhodovaci_strom()) if HAS_SKLEARN else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Random Forest teorie",
        theory="""RANDOM FOREST:
  = Ansámbl rozhodovacích stromů

  Každý strom:
  - trénuje na náhodném podvzorku (bagging)
  - každý split vybírá z náhodných features

  Predikce = většinové hlasování stromů

  Příklad: 100 stromů, 60 říká "kočka", 40 "pes" → kočka""",
        task="Popiš Random Forest jako dict.",
        difficulty=1, points=10,
        hints=["ansámbl, většinové hlasování, n_estimators"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "ansámbl" in r.get("princip", "") and len(r.get("vyhody", [])) >= 2,
                    "RF teorie ✓"
                )
            )(random_forest()),
        ]
    ),
    Challenge(
        title="Confusion Matrix",
        theory="""CONFUSION MATRIX:
                 Predicted
                 0    1
  Actual  0   [ TN | FP ]
          1   [ FN | TP ]

  TP = Správně pozitivní (true=1, pred=1)
  TN = Správně negativní (true=0, pred=0)
  FP = Falešně pozitivní (true=0, pred=1)
  FN = Falešně negativní (true=1, pred=0)""",
        task="Spočítej TP, TN, FP, FN.",
        difficulty=2, points=20,
        hints=["Projdi zip(y_true, y_pred) a počítej"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and r["TP"] == 2 and r["TN"] == 2 and r["FP"] == 1 and r["FN"] == 1,
                    "Confusion matrix ✓"
                )
            )(confusion_matrix_rucne([0, 0, 0, 1, 1, 1], [0, 0, 1, 0, 1, 1])),
        ]
    ),
    Challenge(
        title="Klasifikační metriky",
        theory="""METRIKY:
  Accuracy = (TP+TN) / (TP+TN+FP+FN)
  Precision = TP / (TP+FP) — "z pred. pozitivních, kolik správně?"
  Recall = TP / (TP+FN)    — "z reálných pozitivních, kolik nalezeno?"
  F1 = 2·P·R / (P+R)       — harmonický průměr P a R

  Accuracy je misleading u nevyvážených datasetů!""",
        task="Spočítej accuracy, precision, recall, F1.",
        difficulty=2, points=25,
        hints=["Nejdřív spočítej TP/TN/FP/FN, pak metriky"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and abs(r.get("accuracy", 0) - 4/6) < 0.01,
                    "Accuracy ✓"
                )
            )(metriky_klasifikace([0, 0, 0, 1, 1, 1], [0, 0, 1, 0, 1, 1])),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Klasifikace", "08_04")
