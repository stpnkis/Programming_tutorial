#!/usr/bin/env python3
"""📏 Model Evaluation — Validace, metriky, bias/variance."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def bias_variance():
    """
    🎯 VÝZVA 1: Bias-Variance tradeoff.
    Vrať dict:
    {
        "bias": "chyba z příliš jednoduchého modelu (underfitting)",
        "variance": "chyba z přílišné citlivosti na trénovací data (overfitting)",
        "underfitting": {"bias": "vysoký", "variance": "nízký", "příklad": "lineární model na nelineární data"},
        "overfitting": {"bias": "nízký", "variance": "vysoký", "příklad": "strom hloubky 100 na malá data"},
        "optimum": "nízký bias + nízký variance"
    }
    """
    # TODO: ↓
    pass


def validacni_strategie():
    """
    🎯 VÝZVA 2: Validační strategie.
    Vrať dict:
    {
        "holdout": {"popis": "jednorázový split train/test", "nevyhoda": "závisí na splitu"},
        "k_fold": {"popis": "K rotujících foldů", "typicke_k": 5},
        "stratified_k_fold": {"popis": "k-fold zachovávající poměr tříd", "kdy": "nevyvážené třídy"},
        "leave_one_out": {"popis": "K=N, každý vzorek je jednou test", "kdy": "malá data"},
        "time_series_split": {"popis": "chronologické splity", "kdy": "časové řady"}
    }
    """
    # TODO: ↓
    pass


def learning_curves():
    """
    🎯 VÝZVA 3: Co ukazují learning curves?
    Vrať dict:
    {
        "x_osa": "počet trénovacích vzorků",
        "y_osa": "skóre (train a validation)",
        "underfitting": "obě křivky nízko, blízko u sebe",
        "overfitting": "train vysoké, val nízké (velká mezera)",
        "good_fit": "obě křivky vysoko, blízko u sebe",
        "reseni_underfitting": ["složitější model", "více features", "méně regularizace"],
        "reseni_overfitting": ["více dat", "silnější regularizace", "jednodušší model", "dropout"]
    }
    """
    # TODO: ↓
    pass


def roc_auc_teorie():
    """
    🎯 VÝZVA 4: ROC křivka a AUC.
    Vrať dict:
    {
        "roc_x": "False Positive Rate (FPR)",
        "roc_y": "True Positive Rate (TPR/Recall)",
        "auc_1": "perfektní klasifikátor",
        "auc_05": "náhodný klasifikátor",
        "pouziti": "porovnání klasifikátorů při různých thresholdech",
        "threshold": "práh pro rozhodnutí: P(y=1) > threshold → třída 1"
    }
    """
    # TODO: ↓
    pass


def kompletni_evaluace():
    """
    🎯 VÝZVA 5: Checklist pro evaluaci modelu.
    Vrať list kroků:
    [
        "1. Rozděl data (train/val/test)",
        "2. Trénuj na train, ladění na val",
        "3. Cross-validace pro robustní odhad",
        "4. Learning curves pro diagnostiku",
        "5. Metriky vhodné pro problém (accuracy/F1/AUC)",
        "6. Confusion matrix pro detailní analýzu",
        "7. Finální test NA ODLOŽENÉM test setu",
        "8. Statistický test (t-test) pro porovnání modelů"
    ]
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Bias-Variance Tradeoff",
        theory="""BIAS-VARIANCE:
  Total Error = Bias² + Variance + Noise

  Bias: systematická chyba → model moc jednoduchý
  Variance: citlivost na data → model moc složitý

  Model complexity ↑ → Bias ↓, Variance ↑
  Model complexity ↓ → Bias ↑, Variance ↓

  📊 U-křivka:
  underfitting ← optimum → overfitting""",
        task="Popiš bias-variance tradeoff.",
        difficulty=1, points=15,
        hints=["bias=underfitting, variance=overfitting"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "underfitting" in r and "overfitting" in r,
                    "Bias-variance ✓"
                )
            )(bias_variance()),
        ]
    ),
    Challenge(
        title="Validační strategie",
        theory="""CROSS-VALIDATION:
  K-Fold: rozděl na K částí, rotuj
  Stratified: zachovej poměry tříd
  LOOCV: K=N (extrémní, pomalé)

  from sklearn.model_selection import (
      KFold, StratifiedKFold, LeaveOneOut,
      TimeSeriesSplit
  )""",
        task="Popiš 5 validačních strategií.",
        difficulty=2, points=20,
        hints=["holdout, k_fold, stratified, LOOCV, time_series"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and "k_fold" in r and r["k_fold"].get("typicke_k") == 5,
                    "Validace ✓"
                )
            )(validacni_strategie()),
        ]
    ),
    Challenge(
        title="Learning Curves",
        task="Popiš co ukazují learning curves.",
        difficulty=2, points=20,
        hints=["train vs val score s rostoucím počtem dat"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("reseni_overfitting", [])) >= 3,
                    "Learning curves ✓"
                )
            )(learning_curves()),
        ]
    ),
    Challenge(
        title="ROC & AUC",
        theory="""ROC KŘIVKA:
  X-osa: FPR = FP / (FP + TN)
  Y-osa: TPR = TP / (TP + FN) = Recall

  AUC = plocha pod ROC křivkou
  AUC = 1.0 → perfektní
  AUC = 0.5 → náhodný
  AUC < 0.5 → horší než náhoda

  from sklearn.metrics import roc_auc_score
  auc = roc_auc_score(y_true, y_proba)""",
        task="Popiš ROC/AUC.",
        difficulty=2, points=20,
        hints=["FPR vs TPR, AUC=1 perfektní, AUC=0.5 náhodný"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and r.get("auc_1") == "perfektní klasifikátor",
                    "ROC/AUC ✓"
                )
            )(roc_auc_teorie()),
        ]
    ),
    Challenge(
        title="Evaluační checklist",
        task="Sepiš checklist pro evaluaci ML modelu.",
        difficulty=1, points=10,
        hints=["train/val/test, CV, learning curves, metriky, finální test"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r) >= 7,
                    "≥7 kroků ✓"
                )
            )(kompletni_evaluace()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Model Evaluation", "08_06")
