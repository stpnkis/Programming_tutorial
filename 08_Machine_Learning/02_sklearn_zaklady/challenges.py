#!/usr/bin/env python3
"""🤖 Sklearn Základy — Pipeline, train/test, transformery."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def rozdeleni_dat():
    """
    🎯 VÝZVA 1: Train/test split.
    X = [[i] for i in range(100)]  # 100 vzorků, 1 feature
    y = [i * 2 for i in range(100)]
    Rozděl 80/20, random_state=42
    Vrať (X_train, X_test, y_train, y_test)
    """
    # TODO: ↓
    pass


def standardni_skaler():
    """
    🎯 VÝZVA 2: StandardScaler — standardizace.
    data = [[1], [2], [3], [4], [5]]
    Nafituj scaler na data a transformuj.
    Vrať transformovaná data jako list of lists.
    Hint: scaler.fit_transform(data)
    """
    # TODO: ↓
    pass


def sklearn_pipeline():
    """
    🎯 VÝZVA 3: Vytvoř Pipeline.
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LinearRegression

    Vytvoř pipeline: StandardScaler → LinearRegression
    Vrať Pipeline objekt.
    """
    # TODO: ↓
    pass


def cross_validace():
    """
    🎯 VÝZVA 4: Cross-validation.
    X = np.array([[i] for i in range(50)])
    y = np.array([2*i + 1 for i in range(50)])

    Použij cross_val_score s LinearRegression, cv=5
    Vrať průměrné skóre (float).
    """
    # TODO: ↓
    pass


def grid_search_demo():
    """
    🎯 VÝZVA 5: Hyperparameter tuning koncept.
    Vrať dict popisující grid search:
    {
        "model": "KNeighborsClassifier",
        "params": {"n_neighbors": [3, 5, 7, 9]},
        "cv": 5,
        "scoring": "accuracy"
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Train/Test Split",
        theory="""TRAIN/TEST SPLIT:
  from sklearn.model_selection import train_test_split

  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.2, random_state=42
  )

  # test_size=0.2 → 80% train, 20% test
  # random_state → reprodukovatelnost""",
        task="Rozděl 100 vzorků na 80/20.",
        difficulty=1, points=15,
        hints=["train_test_split(X, y, test_size=0.2, random_state=42)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r[0]) == 80 and len(r[1]) == 20,
                    "80/20 split ✓"
                )
            )(rozdeleni_dat()) if HAS_SKLEARN else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="StandardScaler",
        theory="""STANDARDIZACE:
  Převede data na z-skóre: z = (x - μ) / σ
  → mean=0, std=1

  scaler = StandardScaler()
  X_scaled = scaler.fit_transform(X)

  # DŮLEŽITÉ:
  scaler.fit(X_train)       # fituj jen na train!
  X_train_s = scaler.transform(X_train)
  X_test_s = scaler.transform(X_test)  # ne fit_transform!""",
        task="Standardizuj data pomocí StandardScaler.",
        difficulty=1, points=15,
        hints=["StandardScaler().fit_transform(data).tolist()"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 5 and abs(sum(v[0] for v in r)) < 0.01,
                    "Mean ≈ 0 ✓"
                )
            )(standardni_skaler()) if HAS_SKLEARN else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Sklearn Pipeline",
        theory="""PIPELINE:
  from sklearn.pipeline import Pipeline

  pipe = Pipeline([
      ('scaler', StandardScaler()),
      ('model', LinearRegression())
  ])

  pipe.fit(X_train, y_train)
  pipe.predict(X_test)

Pipeline zajistí správné pořadí transformací.""",
        task="Vytvoř Pipeline: Scaler → LinearRegression.",
        difficulty=2, points=20,
        hints=["Pipeline([('scaler', StandardScaler()), ('model', LinearRegression())])"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and hasattr(r, 'fit') and hasattr(r, 'predict'),
                    "Pipeline s fit/predict ✓"
                )
            )(sklearn_pipeline()) if HAS_SKLEARN else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Cross-Validation",
        theory="""CROSS-VALIDATION:
  from sklearn.model_selection import cross_val_score

  scores = cross_val_score(model, X, y, cv=5)
  print(f"Mean: {scores.mean():.3f} ± {scores.std():.3f}")

  cv=5 → 5 foldů: 4 train, 1 test (rotuje)
  Robustnější odhad výkonu modelu.""",
        task="Cross-validace s LinearRegression, cv=5.",
        difficulty=2, points=25,
        hints=["cross_val_score(LinearRegression(), X, y, cv=5).mean()"],
        tests=[
            lambda: verify(
                (cross_validace() or 0) > 0.9,
                "R² > 0.9 ✓"
            ) if (HAS_SKLEARN and HAS_NUMPY) else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Grid Search Koncept",
        theory="""HYPERPARAMETER TUNING:
  from sklearn.model_selection import GridSearchCV

  param_grid = {"n_neighbors": [3, 5, 7, 9]}
  grid = GridSearchCV(KNeighborsClassifier(), param_grid,
                      cv=5, scoring='accuracy')
  grid.fit(X, y)
  grid.best_params_   # nejlepší parametry
  grid.best_score_    # nejlepší skóre""",
        task="Popiš grid search konfiguraci jako dict.",
        difficulty=1, points=10,
        hints=["dict s 'model', 'params', 'cv', 'scoring'"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and r.get("cv") == 5 and "n_neighbors" in r.get("params", {}),
                    "Grid search config ✓"
                )
            )(grid_search_demo()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Sklearn Základy", "08_02")
