#!/usr/bin/env python3
"""🔮 Clustering — K-means, DBSCAN, hierarchické shlukování."""
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

def kmeans_rucne(body, k, max_iter=10):
    """
    🎯 VÝZVA 1: K-means ručně (zjednodušený).
    body = [[1,1],[1,2],[2,1],[8,8],[8,9],[9,8]]
    k = 2
    1. Vyber prvních k bodů jako centra
    2. Přiřaď každý bod k nejbližšímu centru (Euklidovská vzdálenost)
    3. Přepočítej centra jako průměr přiřazených bodů
    4. Opakuj (max_iter)
    Vrať list přiřazení (labels) — list int délky len(body)
    """
    # TODO: ↓
    pass


def sklearn_kmeans():
    """
    🎯 VÝZVA 2: Sklearn K-Means.
    X = np.array([[1,1],[1,2],[2,1],[8,8],[8,9],[9,8]])
    Nafituj KMeans(n_clusters=2, random_state=42, n_init=10)
    Vrať dict:
    - labels: list přiřazení
    - centers: centra clusterů (list of lists)
    - inertia: inertia (float)
    """
    # TODO: ↓
    pass


def elbow_metoda():
    """
    🎯 VÝZVA 3: Elbow metoda — teorie.
    Vrať dict:
    {
        "princip": "testuj různé K, sleduj inerci",
        "inertia": "součet čtvercových vzdáleností od center",
        "optimalni_k": "ohyb (elbow) v grafu inertia vs K",
        "postup": ["spočítej inertia pro K=1..10", "vykresli graf", "najdi ohyb"]
    }
    """
    # TODO: ↓
    pass


def dbscan_teorie():
    """
    🎯 VÝZVA 4: DBSCAN teorie a parametry.
    Vrať dict:
    {
        "princip": "hustotní shlukování — body v hustých regionech",
        "parametry": {"eps": "maximální vzdálenost sousedů", "min_samples": "min. bodů pro core point"},
        "typy_bodu": {"core": "≥min_samples v eps", "border": "v eps od core", "noise": "ani jedno"},
        "vyhody": ["nemusí zadat K", "najde nepravidelné tvary", "detekuje outliers"],
        "nevyhody": ["citlivý na eps/min_samples", "špatný na různé hustoty"]
    }
    """
    # TODO: ↓
    pass


def porovnani_clusteru():
    """
    🎯 VÝZVA 5: Porovnání clusterovacích metod.
    Vrať list dicts:
    [
        {"metoda": "K-Means", "tvar": "kulovité", "K": "nutné zadat", "rychlost": "rychlý"},
        {"metoda": "DBSCAN", "tvar": "libovolné", "K": "automaticky", "rychlost": "střední"},
        {"metoda": "Hierarchické", "tvar": "libovolné", "K": "z dendrogramu", "rychlost": "pomalý"}
    ]
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="K-Means ručně",
        theory="""K-MEANS ALGORITMUS:
  1. Zvol K center (náhodně nebo heuristicky)
  2. Přiřaď každý bod k nejbližšímu centru
  3. Přepočítej centra = průměr přiřazených bodů
  4. Opakuj 2-3 do konvergence

  Vzdálenost: √((x1-x2)² + (y1-y2)²)

  K-Means vždy konverguje, ale možná k lokálnímu minimu.""",
        task="Implementuj K-means ručně.",
        difficulty=3, points=30,
        hints=["Euklidovská dist, přiřaď, přepočítej centra, opakuj"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 6 and len(set(r)) == 2
                    and r[0] == r[1] == r[2] and r[3] == r[4] == r[5],
                    "2 clustery ✓"
                )
            )(kmeans_rucne([[1,1],[1,2],[2,1],[8,8],[8,9],[9,8]], 2)),
        ]
    ),
    Challenge(
        title="Sklearn K-Means",
        theory="""SKLEARN K-MEANS:
  from sklearn.cluster import KMeans

  km = KMeans(n_clusters=3, random_state=42, n_init=10)
  km.fit(X)
  km.labels_          # přiřazení k clusterům
  km.cluster_centers_ # centra
  km.inertia_         # součet vzdáleností""",
        task="Nafituj KMeans(n_clusters=2).",
        difficulty=1, points=15,
        hints=["KMeans(n_clusters=2, random_state=42).fit(X)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r["labels"]) == 6 and len(r["centers"]) == 2,
                    "2 clustery, 2 centra ✓"
                )
            )(sklearn_kmeans()) if (HAS_SKLEARN and HAS_NUMPY) else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Elbow metoda",
        task="Popiš elbow metodu pro výběr K.",
        difficulty=1, points=10,
        hints=["Sleduj inerci pro různé K, najdi ohyb"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "ohyb" in r.get("optimalni_k", "").lower()
                    or r is not None and "elbow" in r.get("optimalni_k", "").lower(),
                    "Elbow princip ✓"
                )
            )(elbow_metoda()),
        ]
    ),
    Challenge(
        title="DBSCAN",
        theory="""DBSCAN:
  Density-Based Spatial Clustering of Applications with Noise

  Core point: ≥ min_samples bodů v okruhu eps
  Border point: v eps od core, ale sám < min_samples
  Noise: nikam nepatří → label = -1

  from sklearn.cluster import DBSCAN
  db = DBSCAN(eps=0.5, min_samples=5).fit(X)""",
        task="Popiš DBSCAN algoritmus.",
        difficulty=2, points=20,
        hints=["eps, min_samples, core/border/noise"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "core" in r.get("typy_bodu", {}) and "noise" in r.get("typy_bodu", {}),
                    "DBSCAN body ✓"
                )
            )(dbscan_teorie()),
        ]
    ),
    Challenge(
        title="Porovnání metod",
        task="Porovnej K-Means, DBSCAN, Hierarchické.",
        difficulty=1, points=10,
        hints=["List dicts s metoda/tvar/K/rychlost"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 3 and r[0]["metoda"] == "K-Means",
                    "3 metody ✓"
                )
            )(porovnani_clusteru()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Clustering", "08_05")
