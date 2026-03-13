#!/usr/bin/env python3
"""📈 Regrese — Lineární, polynomiální, regularizace."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    from sklearn.linear_model import LinearRegression
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def linearni_regrese_rucne(X, y):
    """
    🎯 VÝZVA 1: Lineární regrese ručně (nejmenší čtverce).
    y = a*x + b
    a = (N*Σxy - Σx*Σy) / (N*Σx² - (Σx)²)
    b = (Σy - a*Σx) / N
    Vrať (a, b) jako tuple.
    """
    # TODO: ↓
    pass


def sklearn_regrese():
    """
    🎯 VÝZVA 2: Lineární regrese se sklearn.
    X = [[1],[2],[3],[4],[5]]
    y = [2.1, 3.9, 6.1, 8.0, 9.9]

    Nafituj LinearRegression, vrať dict:
    - coef: koeficient (float)
    - intercept: intercept (float)
    - prediction: predikce pro x=6 (float)
    """
    # TODO: ↓
    pass


def polynomialni_regrese():
    """
    🎯 VÝZVA 3: Polynomiální regrese.
    X = np.array([1,2,3,4,5]).reshape(-1,1)
    y = np.array([1,4,9,16,25])  # x²

    Použij PolynomialFeatures(degree=2) + LinearRegression
    Vrať predikci pro x=6 (float, ≈36).
    """
    # TODO: ↓
    pass


def regularizace():
    """
    🎯 VÝZVA 4: Ridge vs Lasso.
    Vrať dict popisující rozdíly:
    {
        "ridge": {"penalizace": "L2", "vzorec": "||w||²", "efekt": "zmenšuje váhy"},
        "lasso": {"penalizace": "L1", "vzorec": "|w|", "efekt": "vynuluje váhy (výběr features)"},
        "kdy_ridge": "mnoho korelovaných features",
        "kdy_lasso": "potřeba výběru features"
    }
    """
    # TODO: ↓
    pass


def metriky_regrese(y_true, y_pred):
    """
    🎯 VÝZVA 5: Regresní metriky ručně.
    Vrať dict:
    - mae: Mean Absolute Error = (1/N) Σ|yi - ŷi|
    - mse: Mean Squared Error = (1/N) Σ(yi - ŷi)²
    - rmse: Root MSE = √MSE
    - r2: R² = 1 - Σ(yi-ŷi)² / Σ(yi-ȳ)²
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Lineární regrese ručně",
        theory="""NEJMENŠÍ ČTVERCE (OLS):
  Minimalizujeme Σ(yi - (a·xi + b))²

  a = (N·Σxy - Σx·Σy) / (N·Σx² - (Σx)²)
  b = (Σy - a·Σx) / N

  Příklad: x=[1,2,3], y=[2,4,6] → a=2, b=0""",
        task="Implementuj OLS ručně.",
        difficulty=2, points=25,
        hints=["Spočítej Σx, Σy, Σxy, Σx² pak do vzorce"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and abs(r[0] - 2.0) < 0.01 and abs(r[1]) < 0.01,
                    "a=2, b≈0 ✓"
                )
            )(linearni_regrese_rucne([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])),
        ]
    ),
    Challenge(
        title="Sklearn LinearRegression",
        theory="""SKLEARN REGRESE:
  from sklearn.linear_model import LinearRegression

  model = LinearRegression()
  model.fit(X, y)        # X musí být 2D!
  model.coef_            # koeficienty
  model.intercept_       # intercept
  model.predict([[6]])   # predikce""",
        task="Nafituj model a predikuj x=6.",
        difficulty=1, points=15,
        hints=["model.fit(X, y); model.predict([[6]])[0]"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and abs(r["coef"] - 2.0) < 0.1 and abs(r["prediction"] - 12.0) < 0.5,
                    "Coef≈2, pred(6)≈12 ✓"
                )
            )(sklearn_regrese()) if HAS_SKLEARN else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Polynomiální regrese",
        theory="""POLYNOMIÁLNÍ REGRESE:
  from sklearn.preprocessing import PolynomialFeatures

  poly = PolynomialFeatures(degree=2)
  X_poly = poly.fit_transform(X)  # [x] → [1, x, x²]

  model = LinearRegression()
  model.fit(X_poly, y)

  # Pipeline:
  from sklearn.pipeline import Pipeline
  pipe = Pipeline([
      ('poly', PolynomialFeatures(degree=2)),
      ('lr', LinearRegression())
  ])""",
        task="Nafituj polynomiální model na x² data.",
        difficulty=2, points=25,
        hints=["PolynomialFeatures(degree=2) + LinearRegression v Pipeline"],
        tests=[
            lambda: verify(
                abs((polynomialni_regrese() or 0) - 36.0) < 1.0,
                "pred(6) ≈ 36 ✓"
            ) if (HAS_SKLEARN and HAS_NUMPY) else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Ridge vs Lasso",
        theory="""REGULARIZACE:
  Ridge (L2): loss + α·Σwi²    → zmenšuje váhy
  Lasso (L1): loss + α·Σ|wi|   → vynuluje váhy

  from sklearn.linear_model import Ridge, Lasso

  Ridge(alpha=1.0).fit(X, y)
  Lasso(alpha=0.1).fit(X, y)

  α (alpha) = síla regularizace""",
        task="Popiš rozdíly Ridge vs Lasso.",
        difficulty=1, points=10,
        hints=["Dict s ridge/lasso klíči a penalizace/efekt"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and r["ridge"]["penalizace"] == "L2" and r["lasso"]["penalizace"] == "L1",
                    "L2 vs L1 ✓"
                )
            )(regularizace()),
        ]
    ),
    Challenge(
        title="Regresní metriky",
        theory="""METRIKY:
  MAE = (1/N) Σ|yi - ŷi|
  MSE = (1/N) Σ(yi - ŷi)²
  RMSE = √MSE
  R² = 1 - SS_res / SS_tot
     = 1 - Σ(yi-ŷi)² / Σ(yi-ȳ)²

  R²=1 → perfektní, R²=0 → jako průměr""",
        task="Spočítej MAE, MSE, RMSE, R².",
        difficulty=2, points=20,
        hints=["import math; math.sqrt(mse); mean_y = sum(y)/len(y)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and abs(r["mae"] - 1.0) < 0.01 and abs(r["mse"] - 1.0) < 0.01,
                    "MAE=1, MSE=1 ✓"
                )
            )(metriky_regrese([3, 5, 7], [2, 6, 8])),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Regrese", "08_03")
