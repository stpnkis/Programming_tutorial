#!/usr/bin/env python3
"""🎭 Segmentace — Sémantická, instanční, panoptická."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def typy_segmentace():
    """
    🎯 VÝZVA 1: Typy segmentace.
    Vrať dict:
    {
        "semanticka": {"popis": "každý pixel → třída (silnice, auto, nebe)", "rozlišuje_instance": False},
        "instancni": {"popis": "každý objekt má vlastní masku", "rozlišuje_instance": True},
        "panopticka": {"popis": "sémantická + instanční dohromady", "rozlišuje_instance": True},
        "příklad": "2 auta: sémantická → oba 'auto', instanční → auto_1, auto_2"
    }
    """
    # TODO: ↓
    pass


def watershed_teorie():
    """
    🎯 VÝZVA 2: Watershed a GrabCut.
    Vrať dict:
    {
        "watershed": {
            "princip": "tratí krajinu jako povrch — voda zaplavuje z minim",
            "cv2": "cv2.watershed(img, markers)",
            "použití": "oddělení překrývajících se objektů"
        },
        "grabcut": {
            "princip": "interaktivní segmentace — uživatel označí obdélník",
            "cv2": "mask, bgd, fgd = cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)",
            "použití": "oddělení popředí od pozadí"
        }
    }
    """
    # TODO: ↓
    pass


def unet_architektura():
    """
    🎯 VÝZVA 3: U-Net architektura.
    Vrať dict:
    {
        "encoder": "zmenšuje rozměry, zvyšuje channels (konvoluce + pooling)",
        "bottleneck": "nejmenší rozměry, nejvíce channels",
        "decoder": "zvětšuje rozměry, snižuje channels (upsampling + konvoluce)",
        "skip_connections": "spojení encoder → decoder (zachová detaily)",
        "výstup": "mapa segmentace — stejné rozměry jako vstup",
        "loss": "CrossEntropyLoss nebo DiceLoss",
        "použití": ["medicínské snímky", "satelitní snímky", "robotika"]
    }
    """
    # TODO: ↓
    pass


def segmentacni_metriky():
    """
    🎯 VÝZVA 4: Metriky segmentace.
    Vrať dict:
    {
        "pixel_accuracy": "správně klasifikované pixely / celkový počet",
        "IoU": "intersection over union pro každou třídu",
        "mIoU": "průměr IoU přes všechny třídy",
        "Dice": "2 * |A ∩ B| / (|A| + |B|) — podobné IoU",
        "F1_vs_Dice": "Dice koeficient = F1 score na pixel úrovni"
    }
    """
    # TODO: ↓
    pass


def sam_a_moderni():
    """
    🎯 VÝZVA 5: Moderní segmentační modely.
    Vrať dict:
    {
        "SAM": {"název": "Segment Anything Model (Meta)", "princip": "zero-shot segmentace, prompt-based"},
        "Mask_RCNN": {"princip": "Faster R-CNN + segmentační větvení"},
        "DeepLab": {"princip": "atrous/dilated konvoluce pro větší receptive field"},
        "trendy": ["foundation modely", "zero-shot", "prompt-based", "real-time segmentace"]
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Typy segmentace",
        theory="""SEGMENTACE:
  Klasifikace na pixel úrovni!

  Sémantická: pixel → třída (auto/silnice/nebe)
  Instanční: pixel → objekt_instance (auto_1, auto_2)
  Panoptická: obojí (stuff + things)

  Výstup: maska — obrázek kde každý pixel = ID třídy""",
        task="Popiš 3 typy segmentace.",
        difficulty=1, points=15,
        hints=["sémantická, instanční, panoptická"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "semanticka" in r and "instancni" in r and "panopticka" in r,
                    "3 typy segmentace ✓"
                )
            )(typy_segmentace()),
        ]
    ),
    Challenge(
        title="Watershed & GrabCut",
        task="Popiš tradiční segmentační metody.",
        difficulty=2, points=20,
        hints=["watershed=zaplavování, grabcut=interaktivní fg/bg"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "watershed" in r and "grabcut" in r,
                    "Watershed & GrabCut ✓"
                )
            )(watershed_teorie()),
        ]
    ),
    Challenge(
        title="U-Net",
        theory="""U-NET (2015):
  Encoder (↓) ─── Skip ──→ Decoder (↑)
  Conv+Pool                UpConv+Conv
  64→128→256→             →256→128→64
        512 (bottleneck)

  Skip connections: kopíruje features z encoderu
  do decoderu → zachová prostorové detaily.""",
        task="Popiš U-Net architekturu.",
        difficulty=2, points=25,
        hints=["encoder, bottleneck, decoder, skip connections"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "encoder" in r and "decoder" in r and "skip_connections" in r,
                    "U-Net ✓"
                )
            )(unet_architektura()),
        ]
    ),
    Challenge(
        title="Segmentační metriky",
        task="Popiš pixel accuracy, IoU, mIoU, Dice.",
        difficulty=2, points=20,
        hints=["IoU = intersection/union, Dice = 2*|A∩B|/(|A|+|B|)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "mIoU" in r and "Dice" in r,
                    "Metriky ✓"
                )
            )(segmentacni_metriky()),
        ]
    ),
    Challenge(
        title="Moderní segmentace",
        task="Popiš SAM, Mask R-CNN, DeepLab.",
        difficulty=1, points=15,
        hints=["SAM=zero-shot, Mask R-CNN=detekce+segmentace"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "SAM" in r and "Mask_RCNN" in r,
                    "Moderní modely ✓"
                )
            )(sam_a_moderni()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Segmentace", "09_05")
