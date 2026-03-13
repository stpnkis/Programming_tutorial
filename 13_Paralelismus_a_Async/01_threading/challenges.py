#!/usr/bin/env python3
"""🧵 Threading — Thread, Lock, RLock, Semaphore, Event, Condition, GIL."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

import threading
import time

# ============================================================
# 🧵 THREADING CVIČENÍ
# ============================================================


# VÝZVA 1: Teorie — GIL a thread safety
def teorie_gil_a_threads():
    """🎯 VÝZVA 1: Vrať slovník s klíčovými fakty o GIL a thread safety."""
    # TODO: ↓ vyplň slovník správnými hodnotami
    return {
        "GIL_plny_nazev": None,           # plný název GIL
        "GIL_ovlivnuje": None,            # "CPU-bound" nebo "IO-bound" úlohy
        "thread_safe_operace": None,       # True/False: je list.append() thread-safe v CPython?
        "lock_typ_pro_rekurzi": None,     # název locku vhodného pro rekurzivní volání
        "daemon_thread": None,            # True/False: daemon vlákno brání ukončení programu?
    }


# VÝZVA 2: Vytvoř a spusť vlákna počítající do n
def spust_vlakna(pocet_vlaken: int, pocitej_do: int) -> list:
    """
    🎯 VÝZVA 2: Spusť `pocet_vlaken` vláken, každé počítá 0..pocitej_do-1.
    Vrať setříděný seznam součtů každého vlákna.

    Příklad: spust_vlakna(3, 5) → [10, 10, 10]  (0+1+2+3+4 = 10)
    """
    vysledky = []

    def pocitej(do, vysledky_list):
        # TODO: ↓ spočítej součet range(do) a přidej do vysledky_list
        pass

    vlakna = []
    for _ in range(pocet_vlaken):
        # TODO: ↓ vytvoř a nastartuj Thread(target=pocitej, args=(...))
        pass

    for v in vlakna:
        # TODO: ↓ počkej na dokončení každého vlákna (join)
        pass

    return sorted(vysledky)


# VÝZVA 3: Thread-safe čítač s Lock
class ThreadSafeCounter:
    """
    🎯 VÝZVA 3: Implementuj thread-safe čítač pomocí threading.Lock.

    Metody: increment(), decrement(), value() → int
    """
    def __init__(self):
        # TODO: ↓ inicializuj počítadlo a lock
        self._count = 0
        self._lock = None  # TODO: threading.Lock()

    def increment(self):
        # TODO: ↓ použij lock (with self._lock:) a zvyš _count o 1
        pass

    def decrement(self):
        # TODO: ↓ použij lock a sniž _count o 1
        pass

    def value(self) -> int:
        return self._count


def test_thread_safe_counter():
    """Spustí 10 vláken, každé incrementuje 100×. Výsledek musí být 1000."""
    counter = ThreadSafeCounter()
    vlakna = []
    for _ in range(10):
        t = threading.Thread(target=lambda: [counter.increment() for _ in range(100)])
        vlakna.append(t)
        t.start()
    for t in vlakna:
        t.join()
    return counter.value()


# VÝZVA 4: Semaphore — omezení souběžného přístupu
def simuluj_semaphore(max_soubeznich: int, pocet_uloh: int) -> list:
    """
    🎯 VÝZVA 4: Simulace semaphore — max `max_soubeznich` vláken najednou.

    Každé vlákno:
     - získá semafór
     - spí 0.05 s (simulace práce)
     - zaznamenáme aktuální počet aktivních vláken
     - uvolní semafór

    Vrať seznam zaznamenaných hodnot aktivních vláken.
    Všechny hodnoty musí být <= max_soubeznich.
    """
    semafor = None  # TODO: threading.Semaphore(max_soubeznich)
    aktivni = 0
    lock = threading.Lock()
    zaznamy = []

    def prace():
        nonlocal aktivni
        # TODO: ↓ acquire semaforu, zvyš aktivni, zaznamenej, spi, sniž aktivni, release
        pass

    vlakna = [threading.Thread(target=prace) for _ in range(pocet_uloh)]
    for t in vlakna:
        t.start()
    for t in vlakna:
        t.join()
    return zaznamy


# VÝZVA 5: Event — synchronizace start signálem (robotický příklad)
def robot_cekej_na_signal(pocet_robotu: int) -> list:
    """
    🎯 VÝZVA 5: Spusť `pocet_robotu` vláken (simulace robotů).
    Každý robot čeká na Event 'start_signal'.
    Po nastavení eventu (set()) všichni vykonají práci a vrátí své ID.

    Vrať setříděný seznam ID robotů, kteří dokončili práci.
    """
    start_signal = None  # TODO: threading.Event()
    vysledky = []
    lock = threading.Lock()

    def robot(robot_id):
        # TODO: ↓ počkej na start_signal.wait(), pak přidej robot_id do vysledky (s lockem)
        pass

    vlakna = [threading.Thread(target=robot, args=(i,)) for i in range(pocet_robotu)]
    for t in vlakna:
        t.start()

    time.sleep(0.05)  # dej robotům čas nastartovat
    # TODO: ↓ pošlu start signál (start_signal.set())

    for t in vlakna:
        t.join()
    return sorted(vysledky)


# ============================================================
# ✅ TESTY & CHALLENGES
# ============================================================

def _test_teorie():
    r = teorie_gil_a_threads()
    ok = (
        isinstance(r, dict)
        and r.get("GIL_plny_nazev") == "Global Interpreter Lock"
        and r.get("GIL_ovlivnuje") == "CPU-bound"
        and r.get("thread_safe_operace") is True
        and r.get("lock_typ_pro_rekurzi") == "RLock"
        and r.get("daemon_thread") is False
    )
    return verify(ok,
        "✓ Teorie GIL správně!",
        "✗ Zkontroluj: GIL = 'Global Interpreter Lock', ovlivňuje CPU-bound, "
        "list.append je thread-safe, rekurzivní lock = RLock, daemon=False")


def _test_vlakna():
    r = spust_vlakna(3, 5)
    ocekavano = [10, 10, 10]
    return verify(r == ocekavano,
        "✓ Vlákna běžela správně a vrátila [10, 10, 10]!",
        f"✗ Očekáváno {ocekavano}, dostal {r}")


def _test_counter():
    r = test_thread_safe_counter()
    return verify(r == 1000,
        "✓ Thread-safe counter: 1000 — žádná race condition!",
        f"✗ Čítač vrátil {r}, má být 1000. Chybí Lock?")


def _test_semafor():
    zaznamy = simuluj_semaphore(max_soubeznich=3, pocet_uloh=9)
    ok = len(zaznamy) == 9 and all(1 <= z <= 3 for z in zaznamy)
    return verify(ok,
        "✓ Semaphore funguje — max 3 souběžná vlákna!",
        f"✗ Zaznamy: {zaznamy} — některá překračují limit 3, nebo chybí záznamy")


def _test_event():
    r = robot_cekej_na_signal(5)
    return verify(r == list(range(5)),
        "✓ Všech 5 robotů dokončilo práci po startu!",
        f"✗ Očekáváno [0,1,2,3,4], dostal {r}. Nastavil jsi start_signal.set()?")


challenges = [
    Challenge(
        title="🧵 GIL a Thread Safety — teorie",
        theory=(
            "GIL (Global Interpreter Lock) je mutex v CPython, který zajišťuje, že v daný okamžik "
            "provádí Python bytekód pouze jedno vlákno. To chrání interní struktury interpretu.\n"
            "  • CPU-bound úlohy: GIL brání skutečnému paralelismu → použij multiprocessing\n"
            "  • IO-bound úlohy: vlákno uvolní GIL při čekání na I/O → threading je efektivní\n"
            "  • RLock (Reentrant Lock): stejné vlákno může lock získat vícekrát\n"
            "  • Daemon vlákno: ukončí se automaticky s hlavním vláknem"
        ),
        task="Vyplň slovník v teorie_gil_a_threads() správnými hodnotami.",
        difficulty=1, points=15,
        hints=[
            "GIL plný název: 'Global Interpreter Lock'",
            "CPU-bound: násobení matic. IO-bound: čtení souboru, síť",
            "list.append() je v CPython thread-safe díky GIL",
        ],
        tests=[_test_teorie],
    ),
    Challenge(
        title="🚀 Spuštění vláken — Thread & join",
        theory=(
            "threading.Thread(target=fn, args=(a,b)) vytvoří vlákno.\n"
            "  t.start()  — spustí vlákno\n"
            "  t.join()   — hlavní vlákno čeká na dokončení\n"
            "Sdílená proměnná (list) musí být chráněna při souběžném přístupu!"
        ),
        task=(
            "Implementuj spust_vlakna(pocet_vlaken, pocitej_do).\n"
            "Každé vlákno spočítá sum(range(pocitej_do)) a přidá do sdíleného seznamu."
        ),
        difficulty=1, points=15,
        hints=[
            "t = threading.Thread(target=pocitej, args=(pocitej_do, vysledky))",
            "list.append() je thread-safe v CPython — lock není nutný pro append",
            "Nezapomeň t.start() i t.join() pro každé vlákno",
        ],
        tests=[_test_vlakna],
    ),
    Challenge(
        title="🔒 Thread-safe čítač — Lock",
        theory=(
            "Race condition vzniká, když více vláken mění sdílený stav bez synchronizace.\n"
            "  lock = threading.Lock()\n"
            "  with lock:\n"
            "      # kritická sekce — pouze jedno vlákno najednou\n"
            "      self._count += 1\n"
            "Bez locku: čítač s 10 vlákny × 100 increment může vrátit < 1000!"
        ),
        task=(
            "Implementuj ThreadSafeCounter s metodami increment(), decrement(), value().\n"
            "Použij threading.Lock() pro ochranu _count."
        ),
        difficulty=2, points=20,
        hints=[
            "self._lock = threading.Lock()",
            "with self._lock: self._count += 1",
            "Lock musí být v __init__, ne jako třídní atribut",
        ],
        tests=[_test_counter],
    ),
    Challenge(
        title="🚦 Semaphore — omezení přístupu (robotické zdroje)",
        theory=(
            "Semaphore omezuje počet vláken v kritické sekci:\n"
            "  sem = threading.Semaphore(3)  # max 3 vlákna najednou\n"
            "  sem.acquire()  # získej slot (blokuje, pokud plné)\n"
            "  sem.release()  # uvolni slot\n"
            "Robotický příklad: max 3 roboti přistupují k nabíjecí stanici."
        ),
        task=(
            "Implementuj simuluj_semaphore(max_soubeznich, pocet_uloh).\n"
            "V každém vlákně: acquire → zvyš aktivní → zaznamenej → sleep → sniž → release.\n"
            "Všechny záznamy musí být ≤ max_soubeznich."
        ),
        difficulty=2, points=20,
        hints=[
            "semafor = threading.Semaphore(max_soubeznich)",
            "Použij try/finally: semafor.acquire() → ... → finally: semafor.release()",
            "Nebo: with semafor: ...",
        ],
        tests=[_test_semafor],
    ),
    Challenge(
        title="📡 Event — synchronizace startovního signálu",
        theory=(
            "threading.Event() je vlajka pro synchronizaci vláken:\n"
            "  event = threading.Event()\n"
            "  event.wait()   # blokuje vlákno dokud není flag nastaven\n"
            "  event.set()    # nastaví flag — probudí čekající vlákna\n"
            "  event.clear()  # reset flagu\n"
            "Robotický příklad: roboti čekají na 'start race' signál — pak všichni vyjedou najednou."
        ),
        task=(
            "Implementuj robot_cekej_na_signal(pocet_robotu).\n"
            "Každý robot (vlákno) volá start_signal.wait(), pak přidá své ID do výsledků.\n"
            "Hlavní vlákno po startu všech robotů zavolá start_signal.set()."
        ),
        difficulty=2, points=20,
        hints=[
            "start_signal = threading.Event()",
            "V robot(): start_signal.wait()  pak s lockem přidej robot_id",
            "Po spuštění všech vláken: time.sleep(0.05) pak start_signal.set()",
        ],
        tests=[_test_event],
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "🧵 Threading", "13_01")
