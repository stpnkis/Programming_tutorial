#!/usr/bin/env python3
"""🔍 Detekce hran a features — Canny, Sobel, Harris, ORB."""
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

def sobel_rucne(mat):
    """
    🎯 VÝZVA 1: Sobelův operátor ručně (horizontální).
    Sobel kernel Gx: [[-1,0,1],[-2,0,2],[-1,0,1]]
    Aplikuj na mat (2D list), vrať absolutní hodnoty.
    Vrať 2D list (menší o okraje).
    """
    # TODO: ↓
    pass


def detekce_hran_teorie():
    """
    🎯 VÝZVA 2: Metody detekce hran.
    Vrať dict:
    {
        "Sobel": {"typ": "gradientní", "cv2": "cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)", "detekuje": "hrany v jednom směru"},
        "Laplacian": {"typ": "druhá derivace", "cv2": "cv2.Laplacian(gray, cv2.CV_64F)", "detekuje": "hrany ve všech směrech"},
        "Canny": {"typ": "multi-stage", "cv2": "cv2.Canny(gray, 100, 200)", "detekuje": "tenké hrany, nejpoužívanější"},
        "Canny_kroky": [
            "1. Gaussian blur (redukce šumu)",
            "2. Gradient (Sobel)",
            "3. Non-maximum suppression (ztenčení)",
            "4. Hystereze (dva prahy: strong/weak edge)"
        ]
    }
    """
    # TODO: ↓
    pass


def harris_corners_teorie():
    """
    🎯 VÝZVA 3: Harris Corner Detection.
    Vrať dict:
    {
        "princip": "detekce rohů — bodů kde gradient se mění ve dvou směrech",
        "klasifikace": {
            "rovná_plocha": "malé lambda1, lambda2 → žádná změna",
            "hrana": "jedno lambda velké → změna v jednom směru",
            "roh": "obě lambda velké → změna ve dvou směrech"
        },
        "cv2": "dst = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)",
        "alternativa": "cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)"
    }
    """
    # TODO: ↓
    pass


def feature_matching_teorie():
    """
    🎯 VÝZVA 4: Feature Descriptors a Matching.
    Vrať dict:
    {
        "ORB": {"typ": "binární deskriptor", "cv2": "orb = cv2.ORB_create()", "rychlost": "rychlý", "free": True},
        "SIFT": {"typ": "float deskriptor", "cv2": "sift = cv2.SIFT_create()", "rychlost": "pomalý", "free": True},
        "matching": {
            "BFMatcher": "bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True); matches = bf.match(des1, des2)",
            "FLANN": "rychlejší pro velké datasety",
            "ratio_test": "ponech jen matches kde best < 0.75 * second_best"
        }
    }
    """
    # TODO: ↓
    pass


def kontury():
    """
    🎯 VÝZVA 5: Kontury (contours) v OpenCV.
    Vrať dict:
    {
        "najdi": "contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)",
        "kresli": "cv2.drawContours(img, contours, -1, (0,255,0), 2)",
        "vlastnosti": {
            "plocha": "cv2.contourArea(cnt)",
            "obvod": "cv2.arcLength(cnt, closed=True)",
            "bounding_box": "x,y,w,h = cv2.boundingRect(cnt)",
            "min_kruh": "center, radius = cv2.minEnclosingCircle(cnt)",
            "momenty": "M = cv2.moments(cnt); cx = M['m10']/M['m00']"
        },
        "aproximace": "approx = cv2.approxPolyDP(cnt, epsilon, True)"
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Sobelův operátor ručně",
        theory="""SOBEL:
  Detekuje hrany — approximace gradientu:

  Gx = [[-1,0,1],   Gy = [[-1,-2,-1],
        [-2,0,2],          [ 0, 0, 0],
        [-1,0,1]]          [ 1, 2, 1]]

  Gradient magnitude: G = √(Gx² + Gy²)
  Gradient direction: θ = atan2(Gy, Gx)""",
        task="Aplikuj Sobelův Gx kernel.",
        difficulty=3, points=30,
        hints=["Konvoluce mat s Sobel kernelem, absolutní hodnoty"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 1 and len(r[0]) == 1,
                    "Sobel výstup ✓"
                )
            )(sobel_rucne([[1,2,3],[4,5,6],[7,8,9]])),
        ]
    ),
    Challenge(
        title="Metody detekce hran",
        task="Popiš Sobel, Laplacian, Canny.",
        difficulty=1, points=15,
        hints=["Sobel=gradient, Laplacian=2.derivace, Canny=multi-stage"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "Canny" in r and len(r.get("Canny_kroky", [])) >= 4,
                    "Edge detection ✓"
                )
            )(detekce_hran_teorie()),
        ]
    ),
    Challenge(
        title="Harris Corner Detection",
        task="Popiš Harris corner detection.",
        difficulty=2, points=20,
        hints=["Dva eigenvalues matice gradientů → roh/hrana/plocha"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "roh" in r.get("klasifikace", {}),
                    "Harris ✓"
                )
            )(harris_corners_teorie()),
        ]
    ),
    Challenge(
        title="Feature Matching",
        task="Popiš ORB, SIFT, matching.",
        difficulty=2, points=20,
        hints=["ORB=rychlý binární, SIFT=float, BFMatcher"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "ORB" in r and "SIFT" in r and "matching" in r,
                    "Feature matching ✓"
                )
            )(feature_matching_teorie()),
        ]
    ),
    Challenge(
        title="Kontury",
        task="Popiš práci s konturami.",
        difficulty=1, points=15,
        hints=["findContours, drawContours, contourArea, boundingRect"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "najdi" in r and "vlastnosti" in r
                    and "plocha" in r["vlastnosti"],
                    "Kontury ✓"
                )
            )(kontury()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Detekce hran & Features", "09_03")
