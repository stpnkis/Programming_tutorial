#!/usr/bin/env python3
"""📚 DSA — Stacks a Queues: LIFO a FIFO struktury."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

class Stack:
    """
    🎯 VÝZVA 1: LIFO zásobník.
    - push(hodnota)
    - pop() → vrátí a odebere vrchol (IndexError pokud prázdný)
    - peek() → vrátí vrchol BEZ odebrání
    - is_empty() → bool
    - __len__()
    """
    # TODO: ↓
    pass


def zkontroluj_zavorky(retezec: str) -> bool:
    """
    🎯 VÝZVA 2: Kontrola párových závorek pomocí stacku.
    "({[]})" → True
    "({[}])" → False
    "((" → False
    """
    # TODO: ↓
    pass


class Queue:
    """
    🎯 VÝZVA 3: FIFO fronta.
    - enqueue(hodnota) → přidej na konec
    - dequeue() → odeber z přední strany (IndexError pokud prázdná)
    - peek() → přední prvek BEZ odebrání
    - is_empty() → bool
    - __len__()
    """
    # TODO: ↓
    pass


def hot_potato(jmena: list, pocet: int) -> str:
    """
    🎯 VÝZVA 4: Hra Horký brambor.
    Hráči stojí v kruhu. Brambor se předává.
    Po {pocet} předáních vypadne ten, kdo ho drží.
    Opakuj, dokud nezbude vítěz.
    
    Implementuj pomocí Queue:
    - enqueue/dequeue pro simulaci kruhu
    """
    # TODO: ↓
    pass


class MinStack:
    """
    🎯 VÝZVA 5: Stack, co vrátí minimum v O(1).
    - push(hodnota)
    - pop() → vrátí a odebere vrchní
    - get_min() → vrátí aktuální minimum BEZ odebrání
    Všechny operace O(1)!
    
    Hint: udržuj pomocný stack s minimy.
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Stack — LIFO zásobník",
        theory="""STACK (zásobník) — Last In, First Out.
Představ si hromadu talířů:
  push = položíš talíř navrch
  pop  = vezmeš horní talíř

  stack = []
  stack.append(1)  # push
  stack.append(2)
  stack.pop()      # → 2 (poslední přidaný)

Kde se používá: zpětný krok (Ctrl+Z), volání funkcí,
parsování výrazů.""",
        task="Implementuj Stack s push, pop, peek, is_empty.",
        difficulty=1, points=20,
        hints=["self._data = []; push = append; pop = list.pop()"],
        tests=[
            lambda: (
                lambda s: (s.push(1), s.push(2), s.push(3),
                    verify(s.pop() == 3 and s.peek() == 2, "push/pop/peek ✓"))
            )(Stack())[3],
            lambda: verify(Stack().is_empty(), "Prázdný stack ✓"),
            lambda: (
                lambda s: (s.push("a"), s.push("b"),
                    verify(len(s) == 2, "__len__ ✓"))
            )(Stack())[2],
        ]
    ),
    Challenge(
        title="Kontrola závorek",
        theory="""Klasická Stack úloha:
1. Projdi znak po znaku
2. Je to otvírací ? → push na stack
3. Je to zavírací ? → pop ze stacku a zkontroluj pár
4. Na konci: stack musí být prázdný""",
        task="Použij stack pro párování {}[]().",
        difficulty=2, points=25,
        hints=[
            "Mapa párů: {')':'(', ']':'[', '}':'{'}",
            "if znak in otvírací: push; if znak in zavírací: pop a porovnej"
        ],
        tests=[
            lambda: verify(zkontroluj_zavorky("({[]})") == True, "({[]}) ✓"),
            lambda: verify(zkontroluj_zavorky("({[}])") == False, "({[}]) ✓"),
            lambda: verify(zkontroluj_zavorky("((") == False, "(( ✓"),
            lambda: verify(zkontroluj_zavorky("") == True, "Prázdný ✓"),
            lambda: verify(zkontroluj_zavorky("a + (b * [c])") == True, "S textem ✓"),
        ]
    ),
    Challenge(
        title="Queue — FIFO fronta",
        theory="""QUEUE (fronta) — First In, First Out.
Jako fronta v obchodě:
  enqueue = někdo se přidá na konec
  dequeue = obslouží toho na začátku

  from collections import deque
  q = deque()
  q.append(1)     # enqueue
  q.popleft()     # dequeue → 1""",
        task="Implementuj Queue s enqueue, dequeue, peek.",
        difficulty=1, points=20,
        hints=["from collections import deque; self._data = deque()"],
        tests=[
            lambda: (
                lambda q: (q.enqueue(1), q.enqueue(2), q.enqueue(3),
                    verify(q.dequeue() == 1 and q.peek() == 2, "FIFO ✓"))
            )(Queue())[3],
            lambda: verify(Queue().is_empty(), "Prázdná fronta ✓"),
        ]
    ),
    Challenge(
        title="Horký brambor — simulace",
        task="Kdo přežije hru Horký brambor?",
        difficulty=2, points=25,
        hints=[
            "Pro každé kolečko: pocet-krát dequeue+enqueue (předání)",
            "pak dequeue = vypadl. Opakuj dokud len(q) > 1"
        ],
        tests=[
            lambda: verify(
                hot_potato(["Adam", "Bára", "Cyril", "Dana", "Emil"], 7) is not None,
                "Vrací vítěze ✓"
            ),
            lambda: verify(
                hot_potato(["A", "B"], 1) == "A",
                "Dva hráči, step 1 ✓"
            ),
        ]
    ),
    Challenge(
        title="MinStack — Minimum v O(1)",
        theory="""Trik: udržuj DVA stacky:
  _data = [3, 5, 2, 1]     ← normální stack
  _mins = [3, 3, 2, 1]     ← minimum v každém bodě

push(5):  _data=[3,5], _mins=[3,3]
push(2):  _data=[3,5,2], _mins=[3,3,2]
get_min() → _mins[-1] = 2  → O(1)!""",
        task="Stack s get_min() v konstantním čase.",
        difficulty=3, points=30,
        hints=["push: _mins.append(min(hodnota, _mins[-1]))"],
        tests=[
            lambda: (
                lambda s: (s.push(3), s.push(5), s.push(2), s.push(1),
                    verify(s.get_min() == 1, "Min=1 ✓"))
            )(MinStack())[4],
            lambda: (
                lambda s: (s.push(3), s.push(5), s.push(2), s.pop(),
                    verify(s.get_min() == 3, "Po pop min=3 ✓"))
            )(MinStack())[4],
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "DSA — Stacks a Queues", "03_02")
