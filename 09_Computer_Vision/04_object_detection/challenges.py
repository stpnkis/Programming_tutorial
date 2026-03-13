#!/usr/bin/env python3
"""🎯 Object Detection — YOLO, SSD, Haar, HOG."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def iou_rucne(box1, box2):
    """
    🎯 VÝZVA 1: Intersection over Union (IoU) ručně.
    box = [x1, y1, x2, y2] (levý-horní, pravý-dolní)
    IoU = area(intersection) / area(union)
    Vrať float.
    """
    # TODO: ↓
    pass


def nms_teorie():
    """
    🎯 VÝZVA 2: Non-Maximum Suppression.
    Vrať dict:
    {
        "princip": "odstraní duplicitní detekce téhož objektu",
        "algoritmus": [
            "1. Seřaď boxy dle confidence (desc)",
            "2. Vyber box s nejvyšší confidence",
            "3. Smaž boxy s IoU > threshold vůči vybranému",
            "4. Opakuj dokud jsou boxy"
        ],
        "threshold": "typicky 0.5 — 0.7",
        "cv2": "indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)"
    }
    """
    # TODO: ↓
    pass


def detektory_prehled():
    """
    🎯 VÝZVA 3: Přehled detektorů.
    Vrať list dicts:
    [
        {"název": "Haar Cascades", "typ": "tradiční", "rychlost": "rychlý", "přesnost": "nízká", "příklad": "obličeje"},
        {"název": "HOG + SVM", "typ": "tradiční", "rychlost": "střední", "přesnost": "střední", "příklad": "chodci"},
        {"název": "R-CNN / Faster R-CNN", "typ": "two-stage", "rychlost": "pomalý", "přesnost": "vysoká", "příklad": "COCO"},
        {"název": "SSD", "typ": "one-stage", "rychlost": "rychlý", "přesnost": "střední", "příklad": "real-time"},
        {"název": "YOLO", "typ": "one-stage", "rychlost": "velmi rychlý", "přesnost": "vysoká", "příklad": "robotika, auto"}
    ]
    """
    # TODO: ↓
    pass


def yolo_teorie():
    """
    🎯 VÝZVA 4: YOLO — You Only Look Once.
    Vrať dict:
    {
        "princip": "celý obrázek najednou → grid → bbox + class",
        "verze": {"YOLOv5": "PyTorch, Ultralytics", "YOLOv8": "nejnovější, Ultralytics"},
        "výstup_na_bunku": ["x, y, w, h", "confidence", "class_probabilities"],
        "inference": [
            "from ultralytics import YOLO",
            "model = YOLO('yolov8n.pt')",
            "results = model('image.jpg')",
            "boxes = results[0].boxes"
        ],
        "metriky": {"mAP": "mean Average Precision", "FPS": "frames per second"}
    }
    """
    # TODO: ↓
    pass


def anotace_a_dataset():
    """
    🎯 VÝZVA 5: Anotace a dataset pro detekci.
    Vrať dict:
    {
        "formaty": {
            "COCO": "JSON — {images, annotations: [{bbox, category_id}]}",
            "YOLO": "TXT — class_id center_x center_y width height (normalizováno)",
            "Pascal_VOC": "XML — <object><bndbox><xmin>..."
        },
        "nastroje": ["CVAT", "LabelImg", "Roboflow", "Label Studio"],
        "tipy": [
            "konzistentní anotace",
            "dostatek vzorků na třídu (min ~100)",
            "různé podmínky (osvětlení, úhly)",
            "augmentace zvyšuje efektivní počet"
        ]
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="IoU (Intersection over Union)",
        theory="""IoU = plocha průniku / plocha sjednocení

  box1    box2
  ┌───┐
  │ ┌─┼──┐
  └─┼─┘  │    IoU = intersection / union
    └────┘

  intersection = max(0, min(x2) - max(x1)) * max(0, min(y2) - max(y1))
  union = area1 + area2 - intersection

  IoU > 0.5 → "dobrá" detekce (COCO standard)""",
        task="Spočítej IoU dvou bounding boxů.",
        difficulty=2, points=25,
        hints=["Průnik: max(x1), max(y1), min(x2), min(y2); clamp na 0"],
        tests=[
            lambda: verify(
                abs((iou_rucne([0,0,2,2], [1,1,3,3]) or 0) - 1/7) < 0.02,
                "IoU ≈ 1/7 ✓"
            ),
            lambda: verify(
                (iou_rucne([0,0,1,1], [2,2,3,3]) or -1) == 0.0,
                "Žádný průnik → IoU=0 ✓"
            ),
        ]
    ),
    Challenge(
        title="Non-Maximum Suppression",
        task="Popiš NMS algoritmus.",
        difficulty=2, points=20,
        hints=["Seřaď dle confidence, vyber top, smaž překrývající se"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("algoritmus", [])) >= 4,
                    "NMS ✓"
                )
            )(nms_teorie()),
        ]
    ),
    Challenge(
        title="Přehled detektorů",
        task="Porovnej 5 detekčních metod.",
        difficulty=1, points=15,
        hints=["Haar, HOG, R-CNN, SSD, YOLO"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 5 and r[4]["název"] == "YOLO",
                    "5 detektorů ✓"
                )
            )(detektory_prehled()),
        ]
    ),
    Challenge(
        title="YOLO",
        theory="""YOLO (You Only Look Once):
  - Rozdělí obrázek na S×S grid
  - Každá buňka predikuje B bounding boxů
  - Každý box: (x, y, w, h, confidence)
  - + class probabilities

  One-stage: celý obrázek najednou
  → Velmi rychlý (real-time: 30+ FPS)""",
        task="Popiš YOLO princip a inference kód.",
        difficulty=2, points=20,
        hints=["grid → bbox + conf + class, Ultralytics"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "verze" in r and len(r.get("inference", [])) >= 3,
                    "YOLO ✓"
                )
            )(yolo_teorie()),
        ]
    ),
    Challenge(
        title="Anotace a datasety",
        task="Popiš formáty anotací a nástroje.",
        difficulty=1, points=10,
        hints=["COCO JSON, YOLO TXT, VOC XML, CVAT/Roboflow"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "COCO" in r.get("formaty", {})
                    and len(r.get("nastroje", [])) >= 3,
                    "Anotace ✓"
                )
            )(anotace_a_dataset()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Object Detection", "09_04")
