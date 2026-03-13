#!/usr/bin/env python3
"""📐 Camera Calibration — Kalibrace kamery, distortion, homografie."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def kamerovy_model():
    """
    🎯 VÝZVA 1: Pinhole kamerový model.
    Vrať dict:
    {
        "princip": "3D bod → 2D projekce přes ohnisko",
        "intrinsic_matice": {
            "popis": "vnitřní parametry kamery (3×3)",
            "parametry": ["fx (ohnisková vzdálenost x)", "fy (ohnisková vzdálenost y)",
                         "cx (principal point x)", "cy (principal point y)"],
            "matice": "[[fx, 0, cx], [0, fy, cy], [0, 0, 1]]"
        },
        "extrinsic": {
            "popis": "pozice a orientace kamery v prostoru",
            "parametry": ["R (rotační matice 3×3)", "t (translační vektor 3×1)"]
        },
        "projekce": "p = K · [R|t] · P  (3D → 2D)"
    }
    """
    # TODO: ↓
    pass


def kalibrace_postup():
    """
    🎯 VÝZVA 2: Postup kalibrace kamery.
    Vrať dict:
    {
        "kroky": [
            "1. Vytiskni šachovnicový vzor (checkerboard)",
            "2. Vyfoť z různých úhlů (min 10-20 snímků)",
            "3. Najdi rohy: cv2.findChessboardCorners(gray, (cols, rows))",
            "4. Upřesni rohy: cv2.cornerSubPix(gray, corners, ...)",
            "5. Kalibruj: cv2.calibrateCamera(obj_pts, img_pts, img_size)",
            "6. Odstraň distortion: cv2.undistort(img, mtx, dist)"
        ],
        "výstup": ["camera_matrix (K)", "dist_coeffs", "rvecs", "tvecs"],
        "uložení": "np.savez('calibration.npz', mtx=mtx, dist=dist)"
    }
    """
    # TODO: ↓
    pass


def distortion_typy():
    """
    🎯 VÝZVA 3: Typy distortion (zkreslení).
    Vrať dict:
    {
        "radialni": {
            "popis": "čáry se ohýbají od/k středu",
            "barrel": "ven od středu (wide-angle)",
            "pincushion": "dovnitř ke středu (telephoto)",
            "koeficienty": ["k1", "k2", "k3"]
        },
        "tangencialni": {
            "popis": "čočka není perfektně rovnoběžná se senzorem",
            "koeficienty": ["p1", "p2"]
        },
        "dist_coeffs": "[k1, k2, p1, p2, k3]",
        "oprava": "cv2.undistort(img, mtx, dist)"
    }
    """
    # TODO: ↓
    pass


def homografie():
    """
    🎯 VÝZVA 4: Homografie — perspektivní transformace.
    Vrať dict:
    {
        "popis": "mapování bodů z jedné roviny do druhé (3×3 matice)",
        "použití": ["panorama stitching", "AR overlay", "bird's eye view", "document scanning"],
        "cv2_najdi": "H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)",
        "cv2_aplikuj": "result = cv2.warpPerspective(img, H, (width, height))",
        "body": "potřeba min 4 korespondencí"
    }
    """
    # TODO: ↓
    pass


def stereo_vision():
    """
    🎯 VÝZVA 5: Stereo vize — základy.
    Vrať dict:
    {
        "princip": "dvě kamery → disparita → hloubka",
        "disparita": "d = x_left - x_right (posunutí bodu mezi obrazy)",
        "hloubka": "Z = f * B / d  (f=ohnisko, B=baseline, d=disparita)",
        "cv2": "stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15); disparity = stereo.compute(left, right)",
        "alternativy": ["StereoBM (rychlý)", "StereoSGBM (přesnější)", "deep learning (RAFT-Stereo)"]
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Kamerový model",
        theory="""PINHOLE CAMERA MODEL:
  3D svět → 2D obrázek

  p = K · [R|t] · P

  K = intrinsická matice (ohnisko, principal point)
  [R|t] = extrinsické parametry (pozice kamery)
  P = 3D bod, p = 2D pixel""",
        task="Popiš pinhole model a parametry.",
        difficulty=2, points=20,
        hints=["K matice: fx, fy, cx, cy; extrinsic: R, t"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "intrinsic_matice" in r and "extrinsic" in r,
                    "Kamerový model ✓"
                )
            )(kamerovy_model()),
        ]
    ),
    Challenge(
        title="Kalibrace kamery",
        task="Popiš postup kalibrace.",
        difficulty=2, points=25,
        hints=["Šachovnice, findChessboardCorners, calibrateCamera, undistort"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("kroky", [])) >= 5,
                    "Kalibrace ✓"
                )
            )(kalibrace_postup()),
        ]
    ),
    Challenge(
        title="Distortion",
        task="Popiš typy distortion.",
        difficulty=1, points=15,
        hints=["radiální (barrel/pincushion), tangenciální"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "radialni" in r and "tangencialni" in r,
                    "Distortion ✓"
                )
            )(distortion_typy()),
        ]
    ),
    Challenge(
        title="Homografie",
        task="Popiš homografii a perspektivní transformaci.",
        difficulty=2, points=20,
        hints=["findHomography, warpPerspective, min 4 body"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and r.get("body") == "potřeba min 4 korespondencí",
                    "Homografie ✓"
                )
            )(homografie()),
        ]
    ),
    Challenge(
        title="Stereo vize",
        task="Popiš stereo vizi a výpočet hloubky.",
        difficulty=2, points=25,
        hints=["Z = f*B/d, StereoBM"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "disparita" in r and "hloubka" in r,
                    "Stereo ✓"
                )
            )(stereo_vision()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Camera Calibration", "09_06")
