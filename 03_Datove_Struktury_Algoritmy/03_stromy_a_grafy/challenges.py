#!/usr/bin/env python3
"""🌳 DSA — Stromy a Grafy: Hierarchické a síťové struktury."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

class TreeNode:
    """Uzel binárního stromu (hotový)."""
    def __init__(self, hodnota, levy=None, pravy=None):
        self.hodnota = hodnota
        self.levy = levy
        self.pravy = pravy

    def __repr__(self):
        return f"TreeNode({self.hodnota})"


def inorder(koren: TreeNode) -> list:
    """
    🎯 VÝZVA 1: In-order průchod (levý → kořen → pravý).
    Pro BST vrací seřazené hodnoty!
    """
    # TODO: ↓
    pass


def preorder(koren: TreeNode) -> list:
    """
    🎯 VÝZVA 1b: Pre-order průchod (kořen → levý → pravý).
    """
    # TODO: ↓
    pass


def vyska_stromu(koren: TreeNode) -> int:
    """
    🎯 VÝZVA 2: Výška stromu.
    Prázdný strom → 0, jeden uzel → 1.
    """
    # TODO: ↓
    pass


def vloz_do_bst(koren: TreeNode, hodnota) -> TreeNode:
    """
    🎯 VÝZVA 3: Vlož hodnotu do BST (Binary Search Tree).
    Menší → doleva, větší → doprava.
    Vrať kořen (nový pokud strom prázdný).
    """
    # TODO: ↓
    pass


class Graf:
    """
    🎯 VÝZVA 4: Neorientovaný graf (adjacency list).
    - pridej_vrchol(v) → přidá vrchol
    - pridej_hranu(v1, v2) → přidá hranu mezi v1 a v2
    - sousedi(v) → vrátí seznam sousedů
    - bfs(start) → BFS průchod, vrátí seznam vrcholů v pořadí navštívení
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

# Testovací strom:
#       4
#      / \
#     2   6
#    / \ / \
#   1  3 5  7
test_strom = TreeNode(4,
    TreeNode(2, TreeNode(1), TreeNode(3)),
    TreeNode(6, TreeNode(5), TreeNode(7))
)

challenges = [
    Challenge(
        title="Průchody binárním stromem",
        theory="""BINÁRNÍ STROM: každý uzel má max 2 potomky.

Průchody (rekurzivní):
  def inorder(node):        # L → Root → R
      if not node: return []
      return inorder(node.levy) + [node.hodnota] + inorder(node.pravy)

  def preorder(node):       # Root → L → R
      if not node: return []
      return [node.hodnota] + preorder(node.levy) + preorder(node.pravy)

BST (Binary Search Tree): levý < kořen < pravý
→ inorder průchod BST = SEŘAZENÝ seznam!""",
        task="Implementuj inorder a preorder průchod.",
        difficulty=2, points=25,
        hints=["Rekurze! if not koren: return []", "inorder: levy + [koren] + pravy"],
        tests=[
            lambda: verify(inorder(test_strom) == [1, 2, 3, 4, 5, 6, 7], "Inorder ✓"),
            lambda: verify(preorder(test_strom) == [4, 2, 1, 3, 6, 5, 7], "Preorder ✓"),
            lambda: verify(inorder(None) == [], "Prázdný strom ✓"),
        ]
    ),
    Challenge(
        title="Výška stromu",
        theory="""VÝŠKA = nejdelší cesta od kořene k listu.
  def vyska(node):
      if not node: return 0
      return 1 + max(vyska(node.levy), vyska(node.pravy))""",
        task="Spočítej výšku stromu rekurzivně.",
        difficulty=1, points=15,
        hints=["1 + max(vyska(levy), vyska(pravy))"],
        tests=[
            lambda: verify(vyska_stromu(test_strom) == 3, "Výška 3 ✓"),
            lambda: verify(vyska_stromu(None) == 0, "Prázdný → 0 ✓"),
            lambda: verify(vyska_stromu(TreeNode(1)) == 1, "List → 1 ✓"),
        ]
    ),
    Challenge(
        title="Vložení do BST",
        theory="""BST pravidlo: levý < kořen < pravý
  def vloz(koren, val):
      if not koren: return TreeNode(val)
      if val < koren.hodnota:
          koren.levy = vloz(koren.levy, val)
      else:
          koren.pravy = vloz(koren.pravy, val)
      return koren""",
        task="Vlož hodnotu do BST na správné místo.",
        difficulty=2, points=25,
        hints=["Rekurze: if not koren: return TreeNode(hodnota)"],
        tests=[
            lambda: (
                lambda r: verify(
                    inorder(r) == [1, 2, 3, 4, 5, 6, 7, 8],
                    "Vložení 8 ✓"
                )
            )(vloz_do_bst(test_strom, 8)),
            lambda: (
                lambda r: verify(
                    isinstance(r, TreeNode) and r.hodnota == 42,
                    "Vložení do prázdného ✓"
                )
            )(vloz_do_bst(None, 42)),
        ]
    ),
    Challenge(
        title="Graf s BFS průchodem",
        theory="""GRAF = vrcholy + hrany.
Adjacency list: {A: [B, C], B: [A], C: [A]}

BFS (Breadth-First Search) — procházej po vrstvách:
  def bfs(start):
      visited = set()
      queue = [start]
      result = []
      while queue:
          v = queue.pop(0)
          if v in visited: continue
          visited.add(v)
          result.append(v)
          queue.extend(sousedi(v))
      return result""",
        task="Implementuj Graf s BFS průchodem.",
        difficulty=3, points=35,
        hints=[
            "self._adj = {}; pridej_vrchol: self._adj[v] = []",
            "pridej_hranu: self._adj[v1].append(v2) a naopak",
            "BFS: fronta + visited set"
        ],
        tests=[
            lambda: (
                lambda g: (
                    g.pridej_vrchol("A"), g.pridej_vrchol("B"), g.pridej_vrchol("C"),
                    g.pridej_hranu("A", "B"), g.pridej_hranu("A", "C"),
                    verify(sorted(g.sousedi("A")) == ["B", "C"], "Sousedi ✓")
                )
            )(Graf())[4],
            lambda: (
                lambda g: (
                    g.pridej_vrchol("A"), g.pridej_vrchol("B"),
                    g.pridej_vrchol("C"), g.pridej_vrchol("D"),
                    g.pridej_hranu("A", "B"), g.pridej_hranu("A", "C"),
                    g.pridej_hranu("B", "D"),
                    verify(
                        g.bfs("A") == ["A", "B", "C", "D"],
                        "BFS průchod ✓",
                        f"BFS: {g.bfs('A')}"
                    )
                )
            )(Graf())[7],
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "DSA — Stromy a Grafy", "03_03")
