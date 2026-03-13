#!/usr/bin/env python3
"""☁️ Point Clouds — Mračna bodů, Open3D, registrace."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def point_cloud_zaklady():
    """
    🎯 VÝZVA 1: Co je point cloud?
    Vrať dict:
    {
        "definice": "kolekce 3D bodů (x, y, z) + volitelné atributy",
        "atributy": ["barva (RGB)", "normála", "intenzita", "label"],
        "zdroje": ["LiDAR", "stereo kamera", "depth kamera", "3D scanner"],
        "formaty": ["PCD", "PLY", "LAS/LAZ", "XYZ"],
        "knihovny": ["Open3D", "PCL (Point Cloud Library)", "PyVista"]
    }
    """
    # TODO: ↓
    pass


def open3d_operace():
    """
    🎯 VÝZVA 2: Open3D základní operace (jako kód/stringy).
    Vrať dict:
    {
        "načtení": "pcd = o3d.io.read_point_cloud('cloud.pcd')",
        "vizualizace": "o3d.visualization.draw_geometries([pcd])",
        "voxel_downsample": "pcd_down = pcd.voxel_down_sample(voxel_size=0.05)",
        "statistický_filtr": "pcd_clean, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)",
        "normály": "pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))",
        "uložení": "o3d.io.write_point_cloud('output.pcd', pcd)"
    }
    """
    # TODO: ↓
    pass


def icp_registrace():
    """
    🎯 VÝZVA 3: ICP (Iterative Closest Point) registrace.
    Vrať dict:
    {
        "princip": "najdi transformaci (R, t) zarovnávající dva point cloudy",
        "algoritmus": [
            "1. Pro každý bod najdi nejbližší bod v cíli",
            "2. Spočítej optimální R, t minimalizující vzdálenosti",
            "3. Aplikuj transformaci",
            "4. Opakuj do konvergence"
        ],
        "varianty": {
            "point_to_point": "minimalizuje vzdálenost bod-bod",
            "point_to_plane": "minimalizuje vzdálenost bod-rovina (rychlejší konvergence)"
        },
        "open3d": "result = o3d.pipelines.registration.registration_icp(source, target, threshold, init_transform)"
    }
    """
    # TODO: ↓
    pass


def segmentace_pc():
    """
    🎯 VÝZVA 4: Segmentace point cloudu.
    Vrať dict:
    {
        "RANSAC_rovina": {
            "popis": "najdi rovinu (podlaha) v point cloudu",
            "open3d": "plane, inliers = pcd.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)",
            "výstup": "ax + by + cz + d = 0"
        },
        "clustering": {
            "popis": "seskup body do objektů",
            "open3d": "labels = np.array(pcd.cluster_dbscan(eps=0.02, min_points=10))",
            "metoda": "DBSCAN"
        },
        "deep_learning": ["PointNet", "PointNet++", "RandLA-Net"]
    }
    """
    # TODO: ↓
    pass


def pc_aplikace_robotika():
    """
    🎯 VÝZVA 5: Point clouds v robotice.
    Vrať dict:
    {
        "SLAM": "budování mapy + lokalizace z point cloudů",
        "grasping": "najdi uchopitelné body na objektu",
        "navigation": "plánování cesty bez překážek",
        "inspection": "kontrola kvality povrchu",
        "3D_mapping": "vytvoření 3D modelu prostředí (RTAB-Map, ORB-SLAM)"
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Point Cloud základy",
        theory="""POINT CLOUD:
  Kolekce bodů v 3D prostoru:
  [[x1,y1,z1], [x2,y2,z2], ...]

  + barva, normála, intenzita...

  LiDAR: 100k-1M bodů/frame
  Depth kamera: ~300k bodů (640×480)

  Formáty: PCD (PCL), PLY (obecný), LAS (GIS)""",
        task="Popiš point cloud, atributy, zdroje.",
        difficulty=1, points=15,
        hints=["Kolekce 3D bodů + atributy, LiDAR/stereo/depth"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("zdroje", [])) >= 3 and len(r.get("formaty", [])) >= 3,
                    "Point cloud RPC ✓"
                )
            )(point_cloud_zaklady()),
        ]
    ),
    Challenge(
        title="Open3D operace",
        task="Popiš Open3D: načtení, downsample, filtr, normály.",
        difficulty=2, points=20,
        hints=["read_point_cloud, voxel_down_sample, remove_statistical_outlier"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "voxel_downsample" in r and "normály" in r,
                    "Open3D ✓"
                )
            )(open3d_operace()),
        ]
    ),
    Challenge(
        title="ICP Registrace",
        theory="""ICP (Iterative Closest Point):
  Cíl: zarovnat dva point cloudy

  Source → Transformace → Target
  Minimalizuje: Σ ||T(si) - ti||²

  Potřebuje dobrý počáteční odhad!
  Varianta point-to-plane je rychlejší.""",
        task="Popiš ICP algoritmus.",
        difficulty=2, points=25,
        hints=["Nejbližší bod, R+t, iteruj do konvergence"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("algoritmus", [])) >= 4 and "varianty" in r,
                    "ICP ✓"
                )
            )(icp_registrace()),
        ]
    ),
    Challenge(
        title="Segmentace Point Cloudu",
        task="Popiš RANSAC rovinu, clustering, DL modely.",
        difficulty=2, points=25,
        hints=["RANSAC pro rovinu, DBSCAN pro clustering, PointNet"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "RANSAC_rovina" in r and "clustering" in r and "deep_learning" in r,
                    "PC segmentace ✓"
                )
            )(segmentace_pc()),
        ]
    ),
    Challenge(
        title="Point Clouds v robotice",
        task="Popiš aplikace v robotice.",
        difficulty=1, points=10,
        hints=["SLAM, grasping, navigation, inspection"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "SLAM" in r and "grasping" in r and "navigation" in r,
                    "PC robotika ✓"
                )
            )(pc_aplikace_robotika()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Point Clouds", "09_08")
