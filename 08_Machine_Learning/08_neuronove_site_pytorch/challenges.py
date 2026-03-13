#!/usr/bin/env python3
"""🧠 Neuronové sítě — Perceptron, PyTorch základy, backpropagation."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def perceptron(X, y, lr=0.1, epochs=100):
    """
    🎯 VÝZVA 1: Jednoduchý perceptron ručně.
    Binární klasifikátor pro lineárně separabilní data.
    X = [[0,0],[0,1],[1,0],[1,1]]
    y = [0, 0, 0, 1]  (AND gate)

    Algoritmus:
    1. Inicializuj váhy w = [0, 0], bias = 0
    2. Pro každý vzorek: output = 1 if (w·x + bias) > 0 else 0
    3. Aktualizuj: w += lr * (y - output) * x, bias += lr * (y - output)
    4. Opakuj epochs-krát

    Vrať dict: weights (list), bias (float)
    """
    # TODO: ↓
    pass


def aktivacni_funkce():
    """
    🎯 VÝZVA 2: Aktivační funkce.
    Implementuj ručně (bez knihoven):
    - sigmoid(x) = 1 / (1 + e^(-x))
    - relu(x) = max(0, x)
    - tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))
    Vrať dict s klíči "sigmoid", "relu", "tanh" → funkce/callable
    """
    # TODO: ↓
    pass


def forward_pass():
    """
    🎯 VÝZVA 3: Forward pass jednoduché sítě.
    Síť: 2 vstupy → 2 neurony (hidden) → 1 výstup
    Vstupy: x = [1.0, 0.5]
    Váhy hidden: W1 = [[0.1, 0.2], [0.3, 0.4]]  (2x2)
    Bias hidden: b1 = [0.1, 0.1]
    Váhy output: W2 = [[0.5], [0.6]]  (2x1)
    Bias output: b2 = [0.1]
    Aktivace: ReLU pro hidden, Sigmoid pro output

    Spočítej výstup sítě.
    Vrať float.
    """
    # TODO: ↓
    pass


def backprop_teorie():
    """
    🎯 VÝZVA 4: Backpropagation — teorie.
    Vrať dict:
    {
        "princip": "řetězové pravidlo — propagace chyby zpět",
        "kroky": [
            "1. Forward pass — spočítej výstup",
            "2. Spočítej loss (chybu)",
            "3. Backward pass — spočítej gradienty ∂L/∂w",
            "4. Aktualizuj váhy: w -= lr * gradient"
        ],
        "loss_funkce": {
            "MSE": "regrese — (y-ŷ)²",
            "CrossEntropy": "klasifikace — -y·log(ŷ)"
        },
        "optimizery": ["SGD", "Adam", "RMSprop"]
    }
    """
    # TODO: ↓
    pass


def pytorch_model_teorie():
    """
    🎯 VÝZVA 5: PyTorch model — teorie.
    Vrať dict s kódem (jako stringy):
    {
        "import": "import torch; import torch.nn as nn",
        "model": "nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 1), nn.Sigmoid())",
        "loss": "nn.BCELoss()",
        "optimizer": "torch.optim.Adam(model.parameters(), lr=0.01)",
        "train_loop": [
            "optimizer.zero_grad()",
            "output = model(X)",
            "loss = criterion(output, y)",
            "loss.backward()",
            "optimizer.step()"
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
        title="Perceptron",
        theory="""PERCEPTRON (1957, Rosenblatt):
  Nejjednodušší neuron:
  output = 1  if  Σ(wi·xi) + bias > 0
           0  jinak

  Učení:
  error = y - output
  wi += lr * error * xi
  bias += lr * error

  Umí naučit AND, OR — ale NE XOR!""",
        task="Implementuj perceptron pro AND gate.",
        difficulty=2, points=25,
        hints=["w·x + bias > 0 → 1, jinak 0; w += lr*(y-out)*x"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r["weights"]) == 2
                    and all(isinstance(w, (int, float)) for w in r["weights"]),
                    "Perceptron natrénován ✓"
                )
            )(perceptron([[0,0],[0,1],[1,0],[1,1]], [0,0,0,1])),
        ]
    ),
    Challenge(
        title="Aktivační funkce",
        theory="""AKTIVAČNÍ FUNKCE:
  Sigmoid: σ(x) = 1/(1+e⁻ˣ) → (0, 1)  — pro pravděpodobnosti
  ReLU: f(x) = max(0, x)     → [0, ∞)  — nejpoužívanější
  Tanh: f(x) = (eˣ-e⁻ˣ)/(eˣ+e⁻ˣ) → (-1, 1)

  Proč potřebujeme nelinearitu?
  Bez ní by síť = obří lineární model!""",
        task="Implementuj sigmoid, relu, tanh.",
        difficulty=2, points=20,
        hints=["import math; math.exp(-x)"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None
                    and abs(r["sigmoid"](0) - 0.5) < 0.01
                    and r["relu"](-5) == 0
                    and r["relu"](3) == 3,
                    "Aktivace ✓"
                )
            )(aktivacni_funkce()),
        ]
    ),
    Challenge(
        title="Forward Pass",
        theory="""FORWARD PASS:
  h = ReLU(W1 · x + b1)    # hidden layer
  o = Sigmoid(W2 · h + b2)  # output layer

  Krok po kroku:
  z1 = W1 @ x + b1
  h = relu(z1)
  z2 = W2 @ h + b2
  output = sigmoid(z2)""",
        task="Spočítej výstup 2-vrstvé sítě.",
        difficulty=3, points=30,
        hints=["z1 = [sum(W1[i][j]*x[j]) + b1[i] for i ...]; relu; pak output"],
        tests=[
            lambda: verify(
                forward_pass() is not None and isinstance(forward_pass(), float),
                "Forward pass → float ✓"
            ),
        ]
    ),
    Challenge(
        title="Backpropagation teorie",
        task="Popiš backpropagation kroky.",
        difficulty=1, points=10,
        hints=["forward → loss → backward (gradienty) → update"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("kroky", [])) >= 4 and len(r.get("optimizery", [])) >= 2,
                    "Backprop teorie ✓"
                )
            )(backprop_teorie()),
        ]
    ),
    Challenge(
        title="PyTorch Model teorie",
        theory="""PYTORCH BASICS:
  import torch
  import torch.nn as nn

  model = nn.Sequential(
      nn.Linear(in_features, hidden),
      nn.ReLU(),
      nn.Linear(hidden, out_features),
      nn.Sigmoid()
  )

  criterion = nn.BCELoss()
  optimizer = torch.optim.Adam(model.parameters(), lr=0.01)""",
        task="Popiš PyTorch model a train loop.",
        difficulty=1, points=15,
        hints=["zero_grad, forward, loss, backward, step"],
        tests=[
            lambda: (
                lambda r: verify(
                    r is not None and len(r.get("train_loop", [])) == 5
                    and "backward" in r["train_loop"][3],
                    "PyTorch loop ✓"
                )
            )(pytorch_model_teorie()),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Neuronové sítě (PyTorch)", "08_08")
