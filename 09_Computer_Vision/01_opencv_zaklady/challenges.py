#!/usr/bin/env python3
"""📷 OpenCV Základy — Načítání, zobrazení, základní operace."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def vytvor_obrazek():
    """
    🎯 VÝZVA 1: Vytvoř obrázek pomocí numpy.
    Vytvoř černý obrázek 200x300 (výška x šířka), 3 kanály (BGR).
    Nakresli bílý obdélník (vyplněný) od pozice (50,50) do (250,150).
    Vrať numpy array.
    """
    # TODO: ↓
    pass


def barevne_prostory():
    """
    🎯 VÝZVA 2: Barevné prostory — teorie.
    Vrať dict:
    {
        "BGR": {"kanály": ["Blue", "Green", "Red"], "použití": "výchozí v OpenCV"},
        "RGB": {"kanály": ["Red", "Green", "Blue"], "použití": "většina frameworků"},
        "HSV": {"kanály": ["Hue", "Saturation", "Value"], "použití": "detekce barev"},
        "GRAY": {"kanály": ["Intensity"], "použití": "edge detection, threshold"},
        "prevod": "cv2.cvtColor(img, cv2.COLOR_BGR2HSV)"
    }
    """
    # TODO: ↓
    pass


def kresli_tvary():
    """
    🎯 VÝZVA 3: Kreslení v OpenCV — teorie.
    Vrať dict s příkazy (string):
    {
        "obdelnik": "cv2.rectangle(img, (x1,y1), (x2,y2), (B,G,R), thickness)",
        "kruh": "cv2.circle(img, (cx,cy), radius, (B,G,R), thickness)",
        "cara": "cv2.line(img, (x1,y1), (x2,y2), (B,G,R), thickness)",
        "text": "cv2.putText(img, 'text', (x,y), cv2.FONT_HERSHEY_SIMPLEX, scale, (B,G,R), thickness)",
        "barvy": {"červená": [0,0,255], "zelená": [0,255,0], "modrá": [255,0,0]}
    }
    """
    # TODO: ↓
    pass


def roi_a_resize():
    """
    🎯 VÝZVA 4: Region of Interest a resize.
    Vrať dict:
    {
        "roi": "roi = img[y1:y2, x1:x2]  # numpy slicing",
        "resize": "cv2.resize(img, (width, height))",
        "resize_factor": "cv2.resize(img, None, fx=0.5, fy=0.5)",
        "interpolace": {
            "INTER_NEAREST": "nejrychlejší, pixelované",
            "INTER_LINEAR": "defaultní, bilineární",
            "INTER_CUBIC": "pomalejší, hladší",
            "INTER_AREA": "nejlepší pro zmenšování"
        }
    }
    """
    # TODO: ↓
    pass


def zakladni_operace():
    """
    🎯 VÝZVA 5: Základní operace s obrázky.
    Vrať dict:
    {
        "načtení": "img = cv2.imread('soubor.jpg')",
        "uložení": "cv2.imwrite('output.jpg', img)",
        "rozměry": "h, w, c = img.shape",
        "kopie": "img_copy = img.copy()",
        "kanály": "b, g, r = cv2.split(img); merged = cv2.merge([b, g, r])",
        "jas": "bright = cv2.convertScaleAbs(img, alpha=1.2, beta=30)"
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Vytvoření obrázku",
        theory="""OPENCV + NUMPY:
  Obrázek = numpy array: shape (H, W, C)
  - H: výška (řádky)
  - W: šířka (sloupce)
  - C: kanály (3 pro BGR)

  img = np.zeros((200, 300, 3), dtype=np.uint8)  # černý
  img[50:150, 50:250] = (255, 255, 255)  # bílý obdélník

  NEBO: cv2.rectangle(img, (50,50), (250,150), (255,255,255), -1)""",
        task="Vytvoř obrázek s bílým obdélníkem.",
        difficulty=1, points=15,
        hints=["np.zeros((200,300,3), dtype=np.uint8); img[50:150, 50:250] = 255"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and r.shape == (200, 300, 3) and r[100, 100, 0] == 255,
                    "Obrázek s obdélníkem ✓"
                )
            )(vytvor_obrazek()) if HAS_NUMPY else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Barevné prostory",
        theory="""BAREVNÉ PROSTORY:
  BGR: Blue-Green-Red (OpenCV default!)
  RGB: Red-Green-Blue (matplotlib, PIL)
  HSV: Hue(0-179)-Saturation(0-255)-Value(0-255)
  GRAY: šedotónový (1 kanál)

  Převod: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  Pozor: OpenCV čte BGR, ne RGB!""",
        task="Popiš barevné prostory.",
        difficulty=1, points=10,
        hints=["BGR, RGB, HSV, GRAY + cv2.cvtColor"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "BGR" in r and "HSV" in r and "GRAY" in r,
                    "Barevné prostory ✓"
                )
            )(barevne_prostory()),
        ]
    ),
    Challenge(
        title="Kreslení tvarů",
        task="Popiš OpenCV kreslicí funkce.",
        difficulty=1, points=10,
        hints=["cv2.rectangle, cv2.circle, cv2.line, cv2.putText"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "obdelnik" in r and "kruh" in r and "text" in r,
                    "Kreslení ✓"
                )
            )(kresli_tvary()),
        ]
    ),
    Challenge(
        title="ROI a Resize",
        task="Popiš ROI výřez a resize.",
        difficulty=1, points=10,
        hints=["img[y1:y2, x1:x2], cv2.resize(img, (w,h))"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "roi" in r and "resize" in r and "interpolace" in r,
                    "ROI & resize ✓"
                )
            )(roi_a_resize()),
        ]
    ),
    Challenge(
        title="Základní operace",
        task="Popiš imread, imwrite, shape, split.",
        difficulty=1, points=10,
        hints=["imread, imwrite, shape, split, merge"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "načtení" in r and "kanály" in r,
                    "Základní operace ✓"
                )
            )(zakladni_operace()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "OpenCV Základy", "09_01")
