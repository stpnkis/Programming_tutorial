#!/usr/bin/env python3
"""📐 Lineární Algebra — Vektory, matice, transformace."""
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

def skalarni_soucin(a, b) -> float:
    """
    🎯 VÝZVA 1: Skalární součin dvou vektorů.
    a·b = sum(ai * bi)
    BEZ np.dot — implementuj ručně!
    """
    # TODO: ↓
    pass


def nasobeni_matic(A, B):
    """
    🎯 VÝZVA 2: Násobení matic BEZ np.matmul.
    C[i][j] = sum(A[i][k] * B[k][j])
    """
    # TODO: ↓
    pass


def transponuj(mat):
    """
    🎯 VÝZVA 3: Transponuj matici BEZ .T.
    [[1,2],[3,4]] → [[1,3],[2,4]]
    """
    # TODO: ↓
    pass


def numpy_linalg():
    """
    🎯 VÝZVA 4: NumPy lineární algebra.
    A = [[1, 2], [3, 4]]
    Vrať dict:
    - det: determinant
    - inv: inverzní matice
    - vlastni_cisla: eigenvalues (setříděné)
    - hodnost: rank matice
    """
    # TODO: ↓
    pass


def resi_soustavu():
    """
    🎯 VÝZVA 5: Řeš soustavu rovnic:
    2x + y = 5
    x + 3y = 10
    Vrať (x, y) jako tuple.
    Hint: Ax = b → x = A⁻¹b → np.linalg.solve(A, b)
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Skalární součin",
        theory="""SKALÁRNÍ SOUČIN (dot product):
  a·b = a₁b₁ + a₂b₂ + ... + aₙbₙ

  [1,2,3] · [4,5,6] = 1*4 + 2*5 + 3*6 = 32

V NumPy: np.dot(a, b) nebo a @ b

Geometricky: a·b = |a|·|b|·cos(θ)
- a·b > 0 → stejný směr
- a·b = 0 → kolmé
- a·b < 0 → opačný směr""",
        task="Skalární součin ručně (bez np.dot).",
        difficulty=1, points=15,
        hints=["sum(a[i] * b[i] for i in range(len(a)))"],
        tests=[
            lambda: verify(skalarni_soucin([1, 2, 3], [4, 5, 6]) == 32, "Dot product ✓"),
            lambda: verify(skalarni_soucin([1, 0], [0, 1]) == 0, "Kolmé = 0 ✓"),
        ]
    ),
    Challenge(
        title="Násobení matic",
        theory="""MATICOVÉ NÁSOBENÍ:
  C[i][j] = Σ A[i][k] * B[k][j]

  [[1,2],   [[5,6],     [[1*5+2*7, 1*6+2*8],   [[19, 22],
   [3,4]] ×  [7,8]]  =   [3*5+4*7, 3*6+4*8]]  = [43, 50]]

# A je (m×n), B je (n×p) → C je (m×p)
# Počet sloupců A MUSÍ = počet řádků B!""",
        task="Násobení matic ručně (3 vnořené cykly).",
        difficulty=2, points=25,
        hints=["for i... for j... for k... C[i][j] += A[i][k]*B[k][j]"],
        tests=[
            lambda: verify(
                nasobeni_matic([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]],
                "2x2 * 2x2 ✓"
            ),
        ]
    ),
    Challenge(
        title="Transpozice matice",
        task="Prohoď řádky a sloupce.",
        difficulty=1, points=10,
        hints=["[[mat[j][i] for j in range(rows)] for i in range(cols)]"],
        tests=[
            lambda: verify(
                transponuj([[1, 2], [3, 4]]) == [[1, 3], [2, 4]],
                "Transpozice ✓"
            ),
            lambda: verify(
                transponuj([[1, 2, 3]]) == [[1], [2], [3]],
                "1x3 → 3x1 ✓"
            ),
        ]
    ),
    Challenge(
        title="NumPy Lineární Algebra",
        theory="""np.linalg — lineární algebra:
  np.linalg.det(A)       # determinant
  np.linalg.inv(A)       # inverzní matice
  np.linalg.eig(A)       # vlastní čísla + vektory
  np.linalg.matrix_rank(A)  # hodnost
  np.linalg.solve(A, b)  # řeš Ax = b""",
        task="Vypočítej det, inv, eigenvalues, rank.",
        difficulty=2, points=25,
        hints=["np.linalg.det(A), np.linalg.inv(A), np.linalg.eig(A)[0]"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and abs(r["det"] - (-2.0)) < 0.1,
                    "Determinant ✓"
                )
            )(numpy_linalg()) if HAS_NUMPY else verify(True, "Skip"),
        ]
    ),
    Challenge(
        title="Soustava rovnic",
        theory="""Ax = b  →  x = A⁻¹b

  2x +  y = 5     A = [[2,1],    b = [5, 10]
   x + 3y = 10         [1,3]]

  x = np.linalg.solve(A, b)""",
        task="Řeš soustavu dvou rovnic.",
        difficulty=2, points=20,
        hints=["A = np.array([[2,1],[1,3]]); b = np.array([5,10])"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and abs(r[0] - 1.0) < 0.01 and abs(r[1] - 3.0) < 0.01,
                    "x=1, y=3 ✓"
                )
            )(resi_soustavu()) if HAS_NUMPY else verify(True, "Skip"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Lineární Algebra", "07_02")
