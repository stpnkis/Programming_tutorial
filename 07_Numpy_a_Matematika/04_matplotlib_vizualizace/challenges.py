#!/usr/bin/env python3
"""📈 Matplotlib Vizualizace — Grafy, styly, subplots."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.figure
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def vytvor_line_plot():
    """
    🎯 VÝZVA 1: Základní čárový graf.
    x = [0, 1, 2, 3, 4]
    y = [0, 1, 4, 9, 16]  (x²)
    - Vytvoř fig, ax = plt.subplots()
    - ax.plot(x, y)
    - ax.set_title("Kvadratická funkce")
    - ax.set_xlabel("x"), ax.set_ylabel("y")
    - Vrať (fig, ax)
    """
    # TODO: ↓
    pass


def vytvor_bar_chart():
    """
    🎯 VÝZVA 2: Sloupcový graf.
    kategorie = ["Python", "Java", "C++", "Rust", "Go"]
    popularita = [35, 25, 15, 15, 10]
    - Vytvoř sloupcový graf (ax.bar)
    - Nastav title "Populární jazyky"
    - Vrať (fig, ax)
    """
    # TODO: ↓
    pass


def vytvor_scatter():
    """
    🎯 VÝZVA 3: Bodový graf.
    Vygeneruj 50 náhodných bodů:
      np.random.seed(42)
      x = np.random.randn(50)
      y = 2*x + np.random.randn(50)*0.5
    - ax.scatter(x, y)
    - Přidej title "Korelace"
    - Vrať (fig, ax)
    """
    # TODO: ↓
    pass


def vytvor_subplots():
    """
    🎯 VÝZVA 4: Více grafů (subplots).
    Vytvoř fig s 2x2 mřížkou (fig, axes = plt.subplots(2, 2))
    x = np.linspace(0, 2*np.pi, 100)
    - axes[0,0]: sin(x) — title "sin"
    - axes[0,1]: cos(x) — title "cos"
    - axes[1,0]: tan(x) (ořízni na [-5,5]) — title "tan"
    - axes[1,1]: x² — title "x²"
    - fig.tight_layout()
    - Vrať (fig, axes)
    """
    # TODO: ↓
    pass


def vytvor_histogram_plot():
    """
    🎯 VÝZVA 5: Histogram + normální rozložení.
    np.random.seed(42)
    data = np.random.randn(1000)
    - fig, ax = plt.subplots()
    - ax.hist(data, bins=30, density=True, alpha=0.7)
    - Přidej title "Normální rozložení"
    - Vrať (fig, ax)
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Čárový graf (line plot)",
        theory="""MATPLOTLIB BASICS:
  import matplotlib.pyplot as plt

  fig, ax = plt.subplots()     # vytvoř figure + axes
  ax.plot(x, y)                # čárový graf
  ax.set_title("Title")        # titulek
  ax.set_xlabel("X")           # popis osy
  ax.set_ylabel("Y")
  plt.savefig("graf.png")      # uložení
  plt.show()                   # zobrazení

fig – celý obrázek, ax – jeden graf v obrázku.""",
        task="Vytvoř line plot x vs x².",
        difficulty=1, points=15,
        hints=["fig, ax = plt.subplots(); ax.plot(x, y)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and isinstance(r, tuple) and len(r) == 2,
                    "Vrací (fig, ax) ✓"
                )
            )(vytvor_line_plot()) if HAS_MPL else verify(True, "Skip"),
            lambda: (
                lambda r: verify(
                    r is not None and hasattr(r[0], 'savefig'),
                    "fig je Figure ✓"
                )
            )(vytvor_line_plot()) if HAS_MPL else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Sloupcový graf (bar chart)",
        theory="""SLOUPCOVÝ GRAF:
  ax.bar(categories, values)
  ax.barh(categories, values)  # horizontální

Vlastnosti:
  ax.bar(x, y, color='skyblue', edgecolor='black')
  ax.bar(x, y, width=0.5)""",
        task="Vytvoř sloupcový graf popularit jazyků.",
        difficulty=1, points=15,
        hints=["ax.bar(kategorie, popularita)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and isinstance(r, tuple) and r[1].get_title() == "Populární jazyky",
                    "Bar chart s titulem ✓"
                )
            )(vytvor_bar_chart()) if HAS_MPL else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Bodový graf (scatter)",
        theory="""SCATTER PLOT:
  ax.scatter(x, y)
  ax.scatter(x, y, c=colors, s=sizes, alpha=0.5)

  c = barva bodů (pole nebo jedna barva)
  s = velikost bodů
  alpha = průhlednost (0-1)""",
        task="Vytvoř scatter plot s korelovanými body.",
        difficulty=1, points=15,
        hints=["np.random.seed(42), ax.scatter(x, y)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and isinstance(r, tuple) and len(r) == 2,
                    "Scatter vrací (fig, ax) ✓"
                )
            )(vytvor_scatter()) if (HAS_MPL and HAS_NUMPY) else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Subplots (mřížka grafů)",
        theory="""SUBPLOTS:
  fig, axes = plt.subplots(rows, cols)
  fig, axes = plt.subplots(2, 2, figsize=(10, 8))

  axes[0, 0].plot(x, y)    # levý horní
  axes[0, 1].plot(x, y)    # pravý horní
  axes[1, 0].plot(x, y)    # levý dolní
  axes[1, 1].plot(x, y)    # pravý dolní

  fig.tight_layout()  # automatické odsazení""",
        task="Vytvoř 2x2 mřížku s sin, cos, tan, x².",
        difficulty=2, points=25,
        hints=["fig, axes = plt.subplots(2, 2); np.linspace(0, 2*np.pi, 100)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and isinstance(r, tuple) and r[1].shape == (2, 2),
                    "2x2 subplot grid ✓"
                )
            )(vytvor_subplots()) if (HAS_MPL and HAS_NUMPY) else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Histogram",
        theory="""HISTOGRAM:
  ax.hist(data, bins=30)
  ax.hist(data, bins=30, density=True, alpha=0.7,
          color='steelblue', edgecolor='black')

  bins = počet sloupců
  density = True → normalizuje na hustotu pravděpodobnosti
  alpha = průhlednost""",
        task="Histogram normálního rozložení.",
        difficulty=1, points=15,
        hints=["ax.hist(data, bins=30, density=True, alpha=0.7)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and isinstance(r, tuple) and r[1].get_title() == "Normální rozložení",
                    "Histogram s titulem ✓"
                )
            )(vytvor_histogram_plot()) if (HAS_MPL and HAS_NUMPY) else verify(True, "Skip"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Matplotlib Vizualizace", "07_04")
