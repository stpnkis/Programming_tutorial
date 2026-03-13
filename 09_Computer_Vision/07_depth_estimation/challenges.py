#!/usr/bin/env python3
"""🌊 Depth Estimation — Hloubkové mapy, mono/stereo depth."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def depth_metody():
    """
    🎯 VÝZVA 1: Metody odhadu hloubky.
    Vrať dict:
    {
        "stereo": {"vstup": "2 kamery", "princip": "triangulace z disparity"},
        "structured_light": {"vstup": "projektor + kamera", "princip": "promítnutý vzor → deformace = hloubka"},
        "ToF": {"vstup": "Time-of-Flight senzor", "princip": "čas letu světla → vzdálenost"},
        "monocular_dl": {"vstup": "1 kamera + DL model", "princip": "naučený odhad z jednoho snímku"},
        "LiDAR": {"vstup": "laserový scanner", "princip": "čas odrazu laseru → point cloud"}
    }
    """
    # TODO: ↓
    pass


def depth_senzory():
    """
    🎯 VÝZVA 2: Hloubkové senzory pro robotiku.
    Vrať list dicts:
    [
        {"senzor": "Intel RealSense D435", "typ": "stereo + IR", "rozsah": "0.3-3m", "použití": "indoor robotika"},
        {"senzor": "Intel RealSense L515", "typ": "LiDAR", "rozsah": "0.25-9m", "použití": "skenování"},
        {"senzor": "Azure Kinect", "typ": "ToF", "rozsah": "0.5-5.5m", "použití": "body tracking"},
        {"senzor": "ZED 2", "typ": "stereo", "rozsah": "0.3-20m", "použití": "outdoor, SLAM"},
        {"senzor": "Velodyne Puck", "typ": "LiDAR", "rozsah": "100m", "použití": "autonomní vozidla"}
    ]
    """
    # TODO: ↓
    pass


def mono_depth_teorie():
    """
    🎯 VÝZVA 3: Monokulární depth estimation.
    Vrať dict:
    {
        "princip": "DL model predikuje hloubku z jednoho obrázku",
        "cues": ["velikost objektu", "textura/gradient", "pozice v obraze", "zakrývání", "perspektiva"],
        "modely": ["MiDaS", "DPT (Dense Prediction Transformer)", "Depth Anything"],
        "omezení": ["relativní hloubka (ne metrická)", "selhává na neznámých scénách"],
        "použití": "MiDaS: model = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')"
    }
    """
    # TODO: ↓
    pass


def depth_map_operace():
    """
    🎯 VÝZVA 4: Operace s depth mapou.
    Vrať dict:
    {
        "vizualizace": "cv2.applyColorMap(depth_norm, cv2.COLORMAP_JET)",
        "normalizace": "depth_norm = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)",
        "filtrovani": "cv2.bilateralFilter(depth, 5, 75, 75)  # zachová hrany",
        "body_do_3D": "Z = depth[v, u]; X = (u - cx) * Z / fx; Y = (v - cy) * Z / fy",
        "point_cloud": "Open3D: pcd = o3d.geometry.PointCloud(); pcd.points = o3d.utility.Vector3dVector(points)"
    }
    """
    # TODO: ↓
    pass


def depth_aplikace():
    """
    🎯 VÝZVA 5: Aplikace hloubkových dat.
    Vrať dict:
    {
        "obstacle_avoidance": "robot se vyhýbá překážkám dle depth mapy",
        "grasping": "poloha objektu v 3D pro uchopení",
        "SLAM": "Simultaneous Localization and Mapping",
        "3D_reconstruction": "depth frames → 3D model scény",
        "AR": "umístění virtuálních objektů do reálného světa"
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Metody odhadu hloubky",
        theory="""DEPTH ESTIMATION:
  Cíl: pro každý pixel zjistit vzdálenost od kamery.

  Pasivní: stereo (2 kamery), monocular DL
  Aktivní: structured light, ToF, LiDAR

  Výstup: depth mapa — obrázek kde hodnota = vzdálenost""",
        task="Popiš 5 metod odhadu hloubky.",
        difficulty=1, points=15,
        hints=["stereo, structured light, ToF, mono DL, LiDAR"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "stereo" in r and "LiDAR" in r and "monocular_dl" in r,
                    "Depth metody ✓"
                )
            )(depth_metody()),
        ]
    ),
    Challenge(
        title="Depth senzory",
        task="Vyjmenuj 5 depth senzorů pro robotiku.",
        difficulty=1, points=15,
        hints=["RealSense, Kinect, ZED, Velodyne"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 5 and r[0]["senzor"] == "Intel RealSense D435",
                    "5 senzorů ✓"
                )
            )(depth_senzory()),
        ]
    ),
    Challenge(
        title="Monokulární depth",
        task="Popiš DL monokulární depth estimation.",
        difficulty=2, points=25,
        hints=["MiDaS, DPT, visual cues, relativní hloubka"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("cues", [])) >= 4 and len(r.get("modely", [])) >= 2,
                    "Mono depth ✓"
                )
            )(mono_depth_teorie()),
        ]
    ),
    Challenge(
        title="Depth mapa — operace",
        task="Popiš vizualizaci, filtraci a 3D projekci.",
        difficulty=2, points=25,
        hints=["applyColorMap, normalizace, pixel→3D: X=(u-cx)*Z/fx"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "body_do_3D" in r and "point_cloud" in r,
                    "Depth operace ✓"
                )
            )(depth_map_operace()),
        ]
    ),
    Challenge(
        title="Aplikace hloubky",
        task="Popiš 5 aplikací depth dat.",
        difficulty=1, points=10,
        hints=["obstacle avoidance, grasping, SLAM, 3D reconstruction, AR"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "SLAM" in r and "grasping" in r,
                    "Depth aplikace ✓"
                )
            )(depth_aplikace()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Depth Estimation", "09_07")
