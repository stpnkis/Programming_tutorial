#!/usr/bin/env python3
"""🔄 Transfer Learning — Předtrénované modely, fine-tuning."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def transfer_learning_princip():
    """
    🎯 VÝZVA 1: Co je Transfer Learning?
    Vrať dict:
    {
        "definice": "využití modelu natrénovaného na velkém datasetu pro jiný úkol",
        "proč": "málo dat pro trénování od nuly",
        "zdroj": "ImageNet (1.2M obrázků, 1000 tříd)",
        "kroky": [
            "1. Vezmi předtrénovaný model (ResNet, VGG...)",
            "2. Odstraň poslední vrstvy (klasifikátor)",
            "3. Přidej nové vrstvy pro tvůj úkol",
            "4. Trénuj nové vrstvy (zmraz zbytek)"
        ]
    }
    """
    # TODO: ↓
    pass


def feature_extraction_vs_finetuning():
    """
    🎯 VÝZVA 2: Feature extraction vs Fine-tuning.
    Vrať dict:
    {
        "feature_extraction": {
            "zmrazeno": "všechny vrstvy kromě nových",
            "trénuje_se": "jen nový klasifikátor",
            "kdy": "málo dat, podobný domén",
            "rychlost": "rychlý"
        },
        "fine_tuning": {
            "zmrazeno": "první vrstvy (nízkoúrovňové features)",
            "trénuje_se": "pozdější vrstvy + nový klasifikátor",
            "kdy": "více dat, odlišnější doména",
            "rychlost": "pomalší"
        }
    }
    """
    # TODO: ↓
    pass


def pytorch_transfer_code():
    """
    🎯 VÝZVA 3: PyTorch transfer learning kód (jako stringy).
    Vrať dict:
    {
        "load_model": "model = torchvision.models.resnet18(pretrained=True)",
        "freeze": "for param in model.parameters(): param.requires_grad = False",
        "replace_head": "model.fc = nn.Linear(512, num_classes)",
        "optimizer": "optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)"
    }
    """
    # TODO: ↓
    pass


def data_augmentation():
    """
    🎯 VÝZVA 4: Data augmentace — techniky.
    Vrať dict:
    {
        "geometrické": ["horizontální flip", "rotace", "crop", "resize"],
        "barevné": ["brightness", "contrast", "saturation", "hue"],
        "pokročilé": ["mixup", "cutout", "cutmix"],
        "pytorch": {
            "train": "transforms.Compose([RandomResizedCrop(224), RandomHorizontalFlip(), ToTensor(), Normalize()])",
            "val": "transforms.Compose([Resize(256), CenterCrop(224), ToTensor(), Normalize()])"
        },
        "proč": "zvětšuje efektivně dataset, redukuje overfitting"
    }
    """
    # TODO: ↓
    pass


def kdyz_transfer_learning():
    """
    🎯 VÝZVA 5: Kdy použít transfer learning?
    Vrať dict:
    {
        "velke_data_podobna_domena": "fine-tune celý model",
        "velke_data_jina_domena": "fine-tune od pozdějších vrstev",
        "male_data_podobna_domena": "feature extraction (zmrazit, jen nová hlava)",
        "male_data_jina_domena": "feature extraction z dřívějších vrstev",
        "modely": ["ResNet", "VGG", "EfficientNet", "ViT", "BERT"]
    }
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Transfer Learning princip",
        theory="""TRANSFER LEARNING:
  Předtrénovaný model na ImageNet umí:
  - Nízké vrstvy: hrany, textury
  - Střední vrstvy: tvary, části objektů
  - Vysoké vrstvy: celé objekty

  Tyto features jsou OBECNÉ → přenositelné!

  Místo trénování od nuly:
  ResNet18 (11M params) + nová hlava (512→N)""",
        task="Popiš princip transfer learningu.",
        difficulty=1, points=15,
        hints=["Předtrénovaný model + nové vrstvy"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("kroky", [])) >= 4,
                    "TL princip ✓"
                )
            )(transfer_learning_princip()),
        ]
    ),
    Challenge(
        title="Feature Extraction vs Fine-tuning",
        theory="""DVA PŘÍSTUPY:
  1. Feature Extraction:
     Zmraž celou síť → trénuj jen novou hlavu
     Rychlé, málo dat stačí

  2. Fine-tuning:
     Zmraž první vrstvy → trénuj pozdější + hlavu
     Pomalejší, potřebuješ více dat
     Nižší learning rate!""",
        task="Porovnej feature extraction vs fine-tuning.",
        difficulty=2, points=20,
        hints=["feature_extraction: zmrazit vše, fine_tuning: zmrazit jen začátek"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "feature_extraction" in r and "fine_tuning" in r,
                    "FE vs FT ✓"
                )
            )(feature_extraction_vs_finetuning()),
        ]
    ),
    Challenge(
        title="PyTorch Transfer Learning",
        task="Napiš PyTorch kód pro transfer learning.",
        difficulty=2, points=25,
        hints=["resnet18(pretrained=True), zmraž, nahraď model.fc"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "resnet18" in r.get("load_model", "")
                    and "requires_grad" in r.get("freeze", ""),
                    "PyTorch TL kód ✓"
                )
            )(pytorch_transfer_code()),
        ]
    ),
    Challenge(
        title="Data Augmentace",
        task="Popiš augmentační techniky.",
        difficulty=1, points=15,
        hints=["flip, rotace, crop, color jitter, mixup"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("geometrické", [])) >= 3
                    and "pytorch" in r,
                    "Augmentace ✓"
                )
            )(data_augmentation()),
        ]
    ),
    Challenge(
        title="Kdy TL použít?",
        task="Popiš strategie podle velikosti dat a domény.",
        difficulty=1, points=15,
        hints=["velká/malá data × podobná/jiná doména → 4 scénáře"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and "male_data_podobna_domena" in r
                    and len(r.get("modely", [])) >= 4,
                    "TL strategie ✓"
                )
            )(kdyz_transfer_learning()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Transfer Learning", "08_10")
