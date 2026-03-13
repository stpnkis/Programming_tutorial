#!/usr/bin/env python3
"""🏗️ CV Pipeline Projekt — Kompletní pipeline pro počítačové vidění."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def pipeline_architektura():
    """
    🎯 VÝZVA 1: CV Pipeline — architektura.
    Vrať dict:
    {
        "kroky": [
            "1. Capture (získání snímku z kamery)",
            "2. Preprocessing (resize, normalize, undistort)",
            "3. Detection / Segmentation (najdi objekty)",
            "4. Post-processing (NMS, filtrování, tracking)",
            "5. 3D projection (pixel → 3D souřadnice)",
            "6. Action (rozhodnutí / řízení robota)"
        ],
        "real_time": "každý krok musí stihnout < frame_time (33ms pro 30 FPS)",
        "optimalizace": ["GPU inference", "model quantization", "threading", "resize vstupu"]
    }
    """
    # TODO: ↓
    pass


def objektovy_detekcni_pipeline():
    """
    🎯 VÝZVA 2: Detekční pipeline krok po kroku.
    Vrať dict:
    {
        "vstup": "RGB frame z kamery",
        "preprocessing": ["resize na model input", "BGR → RGB", "normalize [0,1]", "to tensor"],
        "model": "YOLOv8 / Faster R-CNN",
        "výstup_modelu": "list of [x1,y1,x2,y2, confidence, class_id]",
        "postprocessing": ["NMS", "confidence filter > 0.5", "class filter"],
        "vizualizace": "cv2.rectangle + cv2.putText na originální frame"
    }
    """
    # TODO: ↓
    pass


def tracking_zaklady():
    """
    🎯 VÝZVA 3: Object Tracking.
    Vrať dict:
    {
        "proč": "sledovat objekt přes snímky (ne jen detekovat)",
        "metody": {
            "SORT": "Simple Online Realtime Tracking — Kalman filter + Hungarian algorithm",
            "DeepSORT": "SORT + appearance embedding (Re-ID)",
            "ByteTrack": "využívá i nízko-confidence detekce"
        },
        "metriky": {
            "MOTA": "Multi-Object Tracking Accuracy",
            "IDF1": "identitu zachovávající F1",
            "ID_switches": "kolikrát se přehodila ID"
        }
    }
    """
    # TODO: ↓
    pass


def edge_deployment():
    """
    🎯 VÝZVA 4: Nasazení na edge zařízení.
    Vrať dict:
    {
        "zarizeni": ["NVIDIA Jetson", "Raspberry Pi", "Intel NCS2", "Google Coral"],
        "optimalizace_modelu": {
            "quantization": "FP32 → FP16 / INT8 (menší, rychlejší)",
            "pruning": "odstraní nepotřebné váhy",
            "TensorRT": "NVIDIA optimalizace pro Jetson",
            "ONNX": "univerzální formát pro export modelů"
        },
        "framework": ["ONNX Runtime", "TensorRT", "OpenVINO", "TFLite"]
    }
    """
    # TODO: ↓
    pass


def projekt_navrh():
    """
    🎯 VÝZVA 5: Navrhni robotický CV projekt.
    Vrať dict s návrhem:
    {
        "název": <libovolný název projektu>,
        "cíl": <co robot dělá>,
        "senzory": <list senzorů>,
        "cv_kroky": <list CV kroků>,
        "model": <jaký ML model>,
        "výstup": <co systém produkuje>,
        "technologie": <list knihoven/frameworků>
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="CV Pipeline architektura",
        theory="""CV PIPELINE:
  Camera → Preprocess → Model → Postprocess → Action

  Klíčové:
  - Real-time: musí zvládnout 30+ FPS
  - Latence: co nejnižší (robotika!)
  - Robustnost: různé podmínky osvětlení

  Optimalizace:
  - Menší model (YOLOv8n vs YOLOv8x)
  - Menší vstupní rozlišení
  - GPU inference (TensorRT)""",
        task="Navrhni architekturu CV pipeline.",
        difficulty=2, points=20,
        hints=["6 kroků: capture → preprocess → detect → postprocess → 3D → action"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("kroky", [])) >= 5
                    and len(r.get("optimalizace", [])) >= 3,
                    "Pipeline ✓"
                )
            )(pipeline_architektura()),
        ]
    ),
    Challenge(
        title="Detekční pipeline",
        task="Popiš detekční pipeline od vstupu po vizualizaci.",
        difficulty=2, points=20,
        hints=["input → preprocess → model → NMS → vizualizace"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "preprocessing" in r and "postprocessing" in r
                    and len(r["preprocessing"]) >= 3,
                    "Detekční pipeline ✓"
                )
            )(objektovy_detekcni_pipeline()),
        ]
    ),
    Challenge(
        title="Object Tracking",
        task="Popiš SORT, DeepSORT, metriky trackingu.",
        difficulty=2, points=25,
        hints=["SORT=Kalman+Hungarian, DeepSORT=+ReID, ByteTrack"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "SORT" in r.get("metody", {}) and "MOTA" in r.get("metriky", {}),
                    "Tracking ✓"
                )
            )(tracking_zaklady()),
        ]
    ),
    Challenge(
        title="Edge Deployment",
        task="Popiš nasazení modelů na edge zařízeních.",
        difficulty=2, points=20,
        hints=["Jetson, quantization, TensorRT, ONNX"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("zarizeni", [])) >= 3
                    and "quantization" in r.get("optimalizace_modelu", {}),
                    "Edge ✓"
                )
            )(edge_deployment()),
        ]
    ),
    Challenge(
        title="Návrh CV projektu",
        task="Navrhni kompletní robotický CV projekt.",
        difficulty=3, points=30,
        hints=["Název, cíl, senzory, CV kroky, model, výstup, technologie"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and all(k in r for k in ["název", "cíl", "senzory", "cv_kroky", "model"]),
                    "Projekt navržen ✓"
                )
            )(projekt_navrh()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "CV Pipeline Projekt", "09_09")
