#!/usr/bin/env python3
"""🎨 Image Processing — Filtry, threshold, morfologie."""
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

def prumerovy_filtr(mat, kernel_size=3):
    """
    🎯 VÝZVA 1: Průměrový filtr (blur) ručně.
    Pro každý pixel: průměr okolních pixelů (kernel_size × kernel_size)
    Ignoruj okraje (výstup menší o padding).
    mat = 2D list (šedotónový obrázek)
    Vrať 2D list.
    """
    # TODO: ↓
    pass


def thresholding_teorie():
    """
    🎯 VÝZVA 2: Prahování (thresholding) — teorie.
    Vrať dict:
    {
        "binary": "pixel > T → 255, jinak 0",
        "binary_inv": "pixel > T → 0, jinak 255",
        "otsu": "automaticky najde optimální práh (bimodální histogram)",
        "adaptive": "práh se mění lokálně (pro nerovnoměrné osvětlení)",
        "cv2_binary": "ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)",
        "cv2_otsu": "ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)"
    }
    """
    # TODO: ↓
    pass


def morfologicke_operace():
    """
    🎯 VÝZVA 3: Morfologické operace.
    Vrať dict:
    {
        "eroze": {"efekt": "zmenšuje bílé oblasti", "použití": "odstraní šum",
                  "cv2": "cv2.erode(img, kernel, iterations=1)"},
        "dilatace": {"efekt": "zvětšuje bílé oblasti", "použití": "vyplní díry",
                     "cv2": "cv2.dilate(img, kernel, iterations=1)"},
        "opening": {"efekt": "eroze → dilatace", "použití": "odstraní malý šum",
                    "cv2": "cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)"},
        "closing": {"efekt": "dilatace → eroze", "použití": "vyplní malé díry",
                    "cv2": "cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)"},
        "kernel": "kernel = np.ones((5,5), np.uint8)"
    }
    """
    # TODO: ↓
    pass


def histogram_equalization():
    """
    🎯 VÝZVA 4: Histogram equalization — teorie.
    Vrať dict:
    {
        "princip": "přerozdělit jas rovnoměrně přes celý rozsah 0-255",
        "kdy": "nízký kontrast, tmavé/světlé obrázky",
        "cv2": "equalized = cv2.equalizeHist(gray)",
        "clahe": {
            "popis": "lokální equalizace — lepší výsledky",
            "cv2": "clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)); result = clahe.apply(gray)"
        }
    }
    """
    # TODO: ↓
    pass


def filtry_prehled():
    """
    🎯 VÝZVA 5: Přehled filtrů.
    Vrať list dicts:
    [
        {"filtr": "Blur (průměr)", "cv2": "cv2.blur(img, (5,5))", "efekt": "rozmazání"},
        {"filtr": "Gaussian Blur", "cv2": "cv2.GaussianBlur(img, (5,5), 0)", "efekt": "hladší rozmazání"},
        {"filtr": "Median Blur", "cv2": "cv2.medianBlur(img, 5)", "efekt": "odstraní salt&pepper šum"},
        {"filtr": "Bilateral", "cv2": "cv2.bilateralFilter(img, 9, 75, 75)", "efekt": "rozmaže ale zachová hrany"},
        {"filtr": "Sharpen", "kernel": "[[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]", "efekt": "zostření"}
    ]
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Průměrový filtr",
        theory="""KONVOLUČNÍ FILTRY:
  Filtr (kernel) se posouvá po obrázku.
  Průměrový filtr: průměr okolních pixelů → rozmazání.

  Kernel 3×3:
  [1/9  1/9  1/9]
  [1/9  1/9  1/9]
  [1/9  1/9  1/9]

  Ekvivalent: cv2.blur(img, (3,3))""",
        task="Implementuj průměrový filtr ručně.",
        difficulty=2, points=25,
        hints=["Pro každý vnitřní pixel: průměr okna kernel_size × kernel_size"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 1 and len(r[0]) == 1
                    and r[0][0] == 5,
                    "Blur 3×3 střed=5 ✓"
                )
            )(prumerovy_filtr([[1,2,3],[4,5,6],[7,8,9]], 3)),
        ]
    ),
    Challenge(
        title="Thresholding",
        theory="""PRAHOVÁNÍ:
  Pixely nad práh → bílá (255)
  Pixely pod práh → černá (0)

  Otsu: automaticky najde práh z histogramu
  Adaptive: lokální práh (pro různé osvětlení)""",
        task="Popiš typy thresholdingu.",
        difficulty=1, points=15,
        hints=["binary, binary_inv, otsu, adaptive"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "binary" in r and "otsu" in r and "adaptive" in r,
                    "Thresholding ✓"
                )
            )(thresholding_teorie()),
        ]
    ),
    Challenge(
        title="Morfologické operace",
        task="Popiš erozi, dilataci, opening, closing.",
        difficulty=2, points=20,
        hints=["eroze zmenšuje, dilatace zvětšuje, opening=eroze+dilatace"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "eroze" in r and "dilatace" in r and "opening" in r,
                    "Morfologie ✓"
                )
            )(morfologicke_operace()),
        ]
    ),
    Challenge(
        title="Histogram Equalization",
        task="Popiš histogram equalization a CLAHE.",
        difficulty=1, points=15,
        hints=["equalizeHist pro globální, CLAHE pro lokální"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "clahe" in r and "princip" in r,
                    "Equalization ✓"
                )
            )(histogram_equalization()),
        ]
    ),
    Challenge(
        title="Přehled filtrů",
        task="Vyjmenuj 5 filtrů s cv2 příkazy.",
        difficulty=1, points=10,
        hints=["blur, gaussian, median, bilateral, sharpen"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 5 and r[2]["filtr"] == "Median Blur",
                    "5 filtrů ✓"
                )
            )(filtry_prehled()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Image Processing", "09_02")
