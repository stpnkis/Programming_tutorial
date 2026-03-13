#!/usr/bin/env python3
"""📊 Statistika — Střední hodnota, odchylky, distribuce, korelace."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def zakladni_statistiky(data: list) -> dict:
    """
    🎯 VÝZVA 1: Základní statistiky BEZ NumPy.
    Vrať dict: mean, median, mode, rozsah (max-min)
    - mean = průměr
    - median = prostřední hodnota (setříď, pak střed)
    - mode = nejčastější prvek
    - rozsah = max - min
    """
    # TODO: ↓
    pass


def rozptyl_smerodatna(data: list) -> dict:
    """
    🎯 VÝZVA 2: Rozptyl + směrodatná odchylka ručně.
    variance = (1/N) * Σ(xi - mean)²
    std = sqrt(variance)
    Vrať dict: variance, std
    """
    # TODO: ↓
    pass


def numpy_statistiky(data):
    """
    🎯 VÝZVA 3: NumPy statistické funkce.
    data = np.array(data)
    Vrať dict:
    - mean, median, std
    - percentil_25, percentil_75
    - var
    """
    # TODO: ↓
    pass


def korelace(x, y):
    """
    🎯 VÝZVA 4: Pearsonův korelační koeficient.
    r = Σ(xi-mx)(yi-my) / sqrt(Σ(xi-mx)² * Σ(yi-my)²)
    Vrať float.
    Bonus: np.corrcoef(x, y)[0, 1]
    """
    # TODO: ↓
    pass


def histogram_bins(data, n_bins: int) -> list:
    """
    🎯 VÝZVA 5: Ručně spočítej frekvence pro histogram.
    - Rozděl rozsah [min, max] na n_bins intervalů
    - Spočítej kolik hodnot spadá do každého binu
    - Vrať list frekvencí délky n_bins
    - Poslední bin je inkluzivní zprava: [low, high]
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Základní statistiky",
        theory="""STŘEDNÍ HODNOTA (mean):
  mean = Σxi / N = (1+2+3+4+5) / 5 = 3.0

MEDIÁN:
  Setřiď → prostřední prvek
  [1,2,3,4,5] → 3  (lichý počet)
  [1,2,3,4] → (2+3)/2 = 2.5  (sudý počet)

MODUS:
  Nejčastější prvek: [1,2,2,3] → 2

ROZSAH:
  max - min: [1,5] → 4""",
        task="Spočítej mean, median, mode, rozsah.",
        difficulty=1, points=20,
        hints=["sorted(data), collections.Counter pro mode"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and r["mean"] == 3.0 and r["median"] == 3 and r["rozsah"] == 4,
                    "Základní statistiky ✓"
                )
            )(zakladni_statistiky([1, 2, 3, 4, 5])),
            lambda: (
                lambda r: verify(
                    r is not None and r["mode"] == 2,
                    "Mode ✓"
                )
            )(zakladni_statistiky([1, 2, 2, 3, 4])),
        ]
    ),
    Challenge(
        title="Rozptyl a směrodatná odchylka",
        theory="""ROZPTYL (variance):
  σ² = (1/N) * Σ(xi - μ)²

  data = [2, 4, 4, 4, 5, 5, 7, 9]
  μ = 5
  σ² = ((2-5)² + (4-5)² + ... + (9-5)²) / 8 = 4.0

SMĚRODATNÁ ODCHYLKA (std):
  σ = √σ² = √4 = 2.0""",
        task="Rozptyl a std ručně.",
        difficulty=2, points=20,
        hints=["sum((x - mean)**2 for x in data) / len(data)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and abs(r["variance"] - 4.0) < 0.01 and abs(r["std"] - 2.0) < 0.01,
                    "Variance=4, Std=2 ✓"
                )
            )(rozptyl_smerodatna([2, 4, 4, 4, 5, 5, 7, 9])),
        ]
    ),
    Challenge(
        title="NumPy statistiky",
        theory="""NumPy statistické funkce:
  np.mean(a), np.median(a), np.std(a)
  np.var(a)
  np.percentile(a, 25)
  np.percentile(a, 75)
  np.corrcoef(x, y)""",
        task="Použij NumPy pro mean, median, std, percentily.",
        difficulty=1, points=15,
        hints=["np.percentile(data, 25)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and abs(r["mean"] - 5.5) < 0.01,
                    "NumPy mean ✓"
                )
            )(numpy_statistiky(list(range(1, 11)))) if HAS_NUMPY else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Korelační koeficient",
        theory="""PEARSONOVA KORELACE:
  r = Σ(xi-mx)(yi-my) / √(Σ(xi-mx)² · Σ(yi-my)²)

  r = 1.0 → perfektní pozitivní korelace
  r = 0.0 → žádná lineární korelace
  r = -1.0 → perfektní negativní korelace

  x = [1,2,3,4,5], y = [2,4,6,8,10] → r = 1.0""",
        task="Korelace ručně nebo np.corrcoef.",
        difficulty=2, points=25,
        hints=["np.corrcoef(x, y)[0, 1] nebo ruční vzorec"],
        tests=[
            lambda: verify(
                abs((korelace([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]) or 0) - 1.0) < 0.01,
                "Perfektní korelace ✓"
            ),
            lambda: verify(
                abs((korelace([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) or 0) - (-1.0)) < 0.01,
                "Negativní korelace ✓"
            ),
        ]
    ),
    Challenge(
        title="Histogram (bins)",
        theory="""HISTOGRAM:
  Rozděl rozsah dat na biny a spočítej frekvence.

  data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  3 biny: [1-4): 3, [4-7): 3, [7-10]: 4

  bin_width = (max - min) / n_bins""",
        task="Spočítej frekvence pro histogram ručně.",
        difficulty=2, points=20,
        hints=["bin_width = (max-min)/n_bins, pak int((x-min)/bin_width)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 3 and sum(r) == 10,
                    "Histogram 3 biny ✓"
                )
            )(histogram_bins([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Statistika", "07_03")
