#!/usr/bin/env python3
"""🖼️ CNN — Konvoluční neuronové sítě."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def konvoluce_rucne(obraz, kernel):
    """
    🎯 VÝZVA 1: 2D konvoluce ručně (valid, bez paddingu).
    obraz = [[1,2,3],[4,5,6],[7,8,9]]  (3x3)
    kernel = [[1,0],[-1,0]]  (2x2)

    Výstup je (obraz_h - kern_h + 1) × (obraz_w - kern_w + 1)
    Každý element = sum(obraz_patch * kernel)
    Vrať 2D list.
    """
    # TODO: ↓
    pass


def max_pooling(mat, pool_size=2):
    """
    🎯 VÝZVA 2: Max Pooling ručně.
    mat = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
    pool_size = 2 → 2x2 okno, stride = pool_size
    Vrať zmenšenou matici (bere max z každého okna).
    → [[6,8],[14,16]]
    """
    # TODO: ↓
    pass


def cnn_architektura():
    """
    🎯 VÝZVA 3: Popiš CNN architekturu.
    Vrať dict:
    {
        "vrstvy": [
            {"typ": "Conv2D", "účel": "extrahuje features (hrany, textury, vzory)"},
            {"typ": "ReLU", "účel": "nelinearita"},
            {"typ": "MaxPool", "účel": "zmenšení rozměrů, invariance vůči posunu"},
            {"typ": "Flatten", "účel": "2D → 1D pro FC vrstvy"},
            {"typ": "Linear/FC", "účel": "klasifikace"}
        ],
        "parametry_conv": ["in_channels", "out_channels", "kernel_size", "stride", "padding"],
        "výstupní_rozměr": "(H - K + 2P) / S + 1"
    }
    """
    # TODO: ↓
    pass


def zname_architektury():
    """
    🎯 VÝZVA 4: Známé CNN architektury.
    Vrať list dicts:
    [
        {"název": "LeNet-5", "rok": 1998, "vlastnost": "průkopník CNN, MNIST"},
        {"název": "AlexNet", "rok": 2012, "vlastnost": "ImageNet revoluce, ReLU, Dropout"},
        {"název": "VGG", "rok": 2014, "vlastnost": "hluboká síť, malé 3x3 filtry"},
        {"název": "ResNet", "rok": 2015, "vlastnost": "skip connections, 152 vrstev"},
        {"název": "YOLO", "rok": 2016, "vlastnost": "real-time object detection"}
    ]
    """
    # TODO: ↓
    pass


def pytorch_cnn_teorie():
    """
    🎯 VÝZVA 5: PyTorch CNN kód (jako string).
    Vrať dict:
    {
        "model": '''
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 32 * 7 * 7)
        x = F.relu(self.fc1(x))
        return self.fc2(x)
''',
        "vstup": "1x28x28 (MNIST)",
        "výstup": "10 tříd"
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Konvoluce ručně",
        theory="""KONVOLUCE:
  Kernel (filtr) se posouvá po obrázku:

  Obraz 3×3:     Kernel 2×2:
  [1 2 3]        [1  0]
  [4 5 6]        [-1 0]
  [7 8 9]

  Výstup [0,0] = 1·1 + 2·0 + 4·(-1) + 5·0 = -3
  Výstup [0,1] = 2·1 + 3·0 + 5·(-1) + 6·0 = -3
  ...

  Výstupní rozměr: (H-Kh+1) × (W-Kw+1)""",
        task="Implementuj 2D konvoluci.",
        difficulty=3, points=30,
        hints=["Dva vnořené cykly pro pozici, dva pro kernel"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 2 and len(r[0]) == 2
                    and r[0][0] == -3 and r[0][1] == -3,
                    "Konvoluce 3×3 * 2×2 ✓"
                )
            )(konvoluce_rucne([[1,2,3],[4,5,6],[7,8,9]], [[1,0],[-1,0]])),
        ]
    ),
    Challenge(
        title="Max Pooling",
        theory="""MAX POOLING:
  Zmenšuje rozměry — bere maximum z okna

  [1  2  | 3  4 ]     [6  8 ]
  [5  6  | 7  8 ] →   [14 16]
  [9  10 | 11 12]
  [13 14 | 15 16]

  2×2 pool, stride=2 → rozměry / 2""",
        task="Implementuj max pooling.",
        difficulty=2, points=20,
        hints=["Pro každé okno (i:i+ps, j:j+ps) vezmi max"],
        tests=[
            lambda: verify(
                max_pooling([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]) == [[6,8],[14,16]],
                "MaxPool 4×4→2×2 ✓"
            ),
        ]
    ),
    Challenge(
        title="CNN Architektura",
        task="Popiš vrstvy CNN.",
        difficulty=1, points=15,
        hints=["Conv → ReLU → Pool → Flatten → FC"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("vrstvy", [])) >= 5
                    and r["vrstvy"][0]["typ"] == "Conv2D",
                    "CNN vrstvy ✓"
                )
            )(cnn_architektura()),
        ]
    ),
    Challenge(
        title="Známé CNN architektury",
        theory="""HISTORICKÝ VÝVOJ:
  LeNet-5 (1998) → AlexNet (2012) → VGG (2014)
  → GoogLeNet/Inception (2014) → ResNet (2015)
  → DenseNet (2017) → EfficientNet (2019)

  Klíčový přelom: AlexNet na ImageNet 2012
  ResNet: skip connections umožnily 100+ vrstev""",
        task="Vyjmenuj 5 známých CNN architektur.",
        difficulty=1, points=10,
        hints=["LeNet, AlexNet, VGG, ResNet, YOLO"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) == 5 and r[3]["název"] == "ResNet",
                    "5 architektur ✓"
                )
            )(zname_architektury()),
        ]
    ),
    Challenge(
        title="PyTorch CNN",
        task="Napiš PyTorch CNN model pro MNIST.",
        difficulty=2, points=20,
        hints=["nn.Conv2d, nn.MaxPool2d, nn.Linear"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "Conv2d" in r.get("model", "") and r.get("výstup") == "10 tříd",
                    "PyTorch CNN ✓"
                )
            )(pytorch_cnn_teorie()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "CNN", "08_09")
