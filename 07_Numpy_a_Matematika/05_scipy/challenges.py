#!/usr/bin/env python3
"""🔬 SciPy — Optimalizace, interpolace, signály, integrace."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import scipy
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def najdi_minimum():
    """
    🎯 VÝZVA 1: Najdi minimum funkce f(x) = (x-3)² + 2
    Použij scipy.optimize.minimize_scalar
    Vrať dict: x_min (kde je minimum), f_min (hodnota v minimu)
    """
    # TODO: ↓
    pass


def interpoluj_data():
    """
    🎯 VÝZVA 2: Interpolace
    x_znamy = [0, 1, 2, 3, 4, 5]
    y_znamy = [0, 1, 4, 9, 16, 25]  (x²)

    Použij scipy.interpolate.interp1d s kind='quadratic'
    Vrať hodnotu interpolace v bodě x=2.5
    (očekávaný výsledek ≈ 6.25)
    """
    # TODO: ↓
    pass


def numericka_integrace():
    """
    🎯 VÝZVA 3: Numerická integrace.
    Spočítej ∫₀¹ x² dx = 1/3 ≈ 0.3333
    Použij scipy.integrate.quad
    Vrať (vysledek, chyba) — tuple z quad.
    """
    # TODO: ↓
    pass


def fit_krivky():
    """
    🎯 VÝZVA 4: Fitování křivky (curve fitting).
    Data: x = [0, 1, 2, 3, 4, 5]
          y = [0.1, 2.1, 3.9, 6.2, 7.8, 10.1]
    Model: y = a*x + b  (lineární)

    Použij scipy.optimize.curve_fit
    Vrať dict: a (sklon), b (intercept)
    (a ≈ 2.0, b ≈ 0.0)
    """
    # TODO: ↓
    pass


def reseni_ode():
    """
    🎯 VÝZVA 5: Řešení ODE (obyčejná diferenciální rovnice).
    dy/dt = -2*y, y(0) = 1
    Analytické řešení: y(t) = e^(-2t)

    Použij scipy.integrate.solve_ivp
    t_span = (0, 3), t_eval = [0, 1, 2, 3]
    Vrať list hodnot y v bodech t_eval (zaokrouhleno na 2 des. místa)
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Optimalizace — minimum funkce",
        theory="""SCIPY.OPTIMIZE:
  from scipy.optimize import minimize_scalar, minimize

  # Najdi minimum skalární funkce f(x):
  result = minimize_scalar(f)
  result.x   # kde je minimum
  result.fun  # hodnota v minimu

  # Vícerozměrná optimalizace:
  result = minimize(f, x0=[1,1])

f(x) = (x-3)² + 2 → minimum v x=3, f(3)=2""",
        task="Najdi minimum pomocí SciPy.",
        difficulty=1, points=15,
        hints=["from scipy.optimize import minimize_scalar; minimize_scalar(f)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and abs(r["x_min"] - 3.0) < 0.01 and abs(r["f_min"] - 2.0) < 0.01,
                    "Minimum v x=3, f=2 ✓"
                )
            )(najdi_minimum()) if HAS_SCIPY else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Interpolace dat",
        theory="""SCIPY.INTERPOLATE:
  from scipy.interpolate import interp1d

  f = interp1d(x, y, kind='linear')    # lineární
  f = interp1d(x, y, kind='quadratic') # kvadratická
  f = interp1d(x, y, kind='cubic')     # kubická

  f(2.5)  # vrátí interpolovanou hodnotu

kind: 'linear', 'quadratic', 'cubic', 'nearest'""",
        task="Interpoluj parabolická data v bodě x=2.5.",
        difficulty=2, points=20,
        hints=["interp1d(x, y, kind='quadratic'); pak funkce(2.5)"],
        tests=[
            lambda: verify(
                abs((interpoluj_data() or 0) - 6.25) < 0.1,
                "Interpolace(2.5) ≈ 6.25 ✓"
            ) if HAS_SCIPY else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Numerická integrace",
        theory="""SCIPY.INTEGRATE:
  from scipy.integrate import quad

  result, error = quad(f, a, b)
  # f = funkce, a = dolní mez, b = horní mez

  # Příklad: ∫₀¹ x² dx = 1/3
  result, err = quad(lambda x: x**2, 0, 1)
  # result ≈ 0.3333""",
        task="Spočítej ∫₀¹ x² dx.",
        difficulty=1, points=15,
        hints=["from scipy.integrate import quad; quad(lambda x: x**2, 0, 1)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and abs(r[0] - 1/3) < 0.001,
                    "∫x²dx = 1/3 ✓"
                )
            )(numericka_integrace()) if HAS_SCIPY else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Fitování křivky",
        theory="""CURVE FITTING:
  from scipy.optimize import curve_fit

  def model(x, a, b):
      return a * x + b

  popt, pcov = curve_fit(model, x_data, y_data)
  # popt = optimální parametry [a, b]
  # pcov = kovarianční matice

  a, b = popt""",
        task="Nafituj lineární model y = a*x + b.",
        difficulty=2, points=25,
        hints=["def lin(x, a, b): return a*x+b; curve_fit(lin, x, y)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and abs(r["a"] - 2.0) < 0.2 and abs(r["b"]) < 0.5,
                    "a≈2, b≈0 ✓"
                )
            )(fit_krivky()) if (HAS_SCIPY and HAS_NUMPY) else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="ODE — diferenciální rovnice",
        theory="""SCIPY.INTEGRATE.SOLVE_IVP:
  from scipy.integrate import solve_ivp

  def ode(t, y):
      return -2 * y  # dy/dt = -2y

  sol = solve_ivp(ode, t_span=(0, 3), y0=[1],
                  t_eval=[0, 1, 2, 3])
  sol.y[0]  # hodnoty y v bodech t_eval

  Analyticky: y(t) = e^(-2t)
  y(0) = 1, y(1) ≈ 0.135, y(2) ≈ 0.018""",
        task="Řeš dy/dt = -2y pomocí solve_ivp.",
        difficulty=3, points=30,
        hints=["solve_ivp(lambda t, y: -2*y, (0,3), [1], t_eval=[0,1,2,3])"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 4 and abs(r[0] - 1.0) < 0.01,
                    "y(0) = 1 ✓"
                )
            )(reseni_ode()) if HAS_SCIPY else verify(True, "Skip"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "SciPy", "07_05")
