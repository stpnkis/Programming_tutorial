#!/usr/bin/env python3
"""🔀 Multiprocessing — Process, Pool, Value/Array, Manager, sdílená paměť."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

import multiprocessing
import time
import math

# ============================================================
# 🔀 MULTIPROCESSING CVIČENÍ
# ============================================================


# VÝZVA 1: Teorie — multiprocessing vs threading
def teorie_multiprocessing():
    """🎯 VÝZVA 1: Vrať slovník s klíčovými fakty o multiprocessing."""
    # TODO: ↓ vyplň správnými hodnotami
    return {
        "vyuziva_vicejadra": None,        # True/False: obchází GIL?
        "vhodne_pro": None,               # "CPU-bound" nebo "IO-bound"
        "overhead_oproti_threading": None, # "vyssi" nebo "nizsi"
        "sdilena_pamet_typ": None,        # třída pro sdílené pole: "Array"
        "pool_metoda_map": None,          # True/False: Pool.map rozdělí iterable mezi procesy?
    }


# VÝZVA 2: Paralelní výpočet — Pool.map
def paralelni_faktorial(cisla: list) -> list:
    """
    🎯 VÝZVA 2: Spočítej faktoriál každého čísla v seznamu pomocí Pool.map.

    Použij multiprocessing.Pool se 2 procesy.
    Vrať seznam faktoriálů ve stejném pořadí.

    Příklad: paralelni_faktorial([3, 4, 5]) → [6, 24, 120]
    """
    def faktorial(n):
        return math.factorial(n)

    # TODO: ↓ použij multiprocessing.Pool(2) a pool.map(faktorial, cisla)
    pass


# VÝZVA 3: Sdílená proměnná — Value
def sdilena_hodnota_demo(pocet_procesu: int) -> int:
    """
    🎯 VÝZVA 3: Spusť `pocet_procesu` procesů, každý inkrementuje sdílenou Value 100×.
    Vrať výslednou hodnotu (musí být pocet_procesu * 100).

    Použij: multiprocessing.Value('i', 0) a Lock pro bezpečný přístup.
    """
    # TODO: ↓ vytvoř Value a Lock
    counter = None   # multiprocessing.Value('i', 0)
    lock = None      # multiprocessing.Lock()

    def inkrementuj(cnt, lck, kolikrat):
        for _ in range(kolikrat):
            # TODO: ↓ with lck: cnt.value += 1
            pass

    procesy = []
    for _ in range(pocet_procesu):
        # TODO: ↓ Process(target=inkrementuj, args=(counter, lock, 100))
        pass

    for p in procesy:
        p.start()
    for p in procesy:
        p.join()

    return counter.value if counter else 0


# VÝZVA 4: Pool.starmap — paralelní výpočet vzdáleností (robotika)
def vzdalenosti_robotu(body: list) -> list:
    """
    🎯 VÝZVA 4: Spočítej euklidovské vzdálenosti od počátku pro seznam bodů (x, y).
    Použij Pool.starmap pro paralelní zpracování.

    body = [(x1,y1), (x2,y2), ...]
    Vrať [sqrt(x1²+y1²), sqrt(x2²+y2²), ...]  zaokrouhleno na 4 des. místa.

    Příklad: vzdalenosti_robotu([(3,4), (0,5)]) → [5.0, 5.0]
    """
    def vzdalenost(x, y):
        # TODO: ↓ math.sqrt(x**2 + y**2) zaokrouhleno na 4 místa
        pass

    # TODO: ↓ použij Pool(2) a pool.starmap(vzdalenost, body)
    pass


# VÝZVA 5: Manager — sdílený slovník mezi procesy
def sdileny_slovnik_demo(pocet_robotu: int) -> dict:
    """
    🎯 VÝZVA 5: Každý z `pocet_robotu` procesů zapíše do sdíleného Manager slovníku
    svůj stav: {robot_id: 'hotovo'}.

    Vrať slovník s pocet_robotu položkami.
    """
    # TODO: ↓ Manager a Manager().dict()
    manager = None  # multiprocessing.Manager()
    stav = None     # manager.dict()

    def robot_prace(robot_id, sdileny_stav):
        # TODO: ↓ sdileny_stav[robot_id] = 'hotovo'
        pass

    procesy = []
    for i in range(pocet_robotu):
        # TODO: ↓ Process(target=robot_prace, args=(i, stav))
        pass

    for p in procesy:
        p.start()
    for p in procesy:
        p.join()

    return dict(stav) if stav else {}


# ============================================================
# ✅ TESTY & CHALLENGES
# ============================================================

def _test_teorie():
    r = teorie_multiprocessing()
    ok = (
        isinstance(r, dict)
        and r.get("vyuziva_vicejadra") is True
        and r.get("vhodne_pro") == "CPU-bound"
        and r.get("overhead_oproti_threading") == "vyssi"
        and r.get("sdilena_pamet_typ") == "Array"
        and r.get("pool_metoda_map") is True
    )
    return verify(ok,
        "✓ Teorie multiprocessing správně!",
        "✗ Zkontroluj: vicejadra=True, CPU-bound, overhead=vyssi, Array, map=True")


def _test_pool_map():
    r = paralelni_faktorial([3, 4, 5, 6])
    ocekavano = [6, 24, 120, 720]
    return verify(r == ocekavano,
        f"✓ Pool.map faktoriál: {r}",
        f"✗ Očekáváno {ocekavano}, dostal {r}")


def _test_sdilena():
    r = sdilena_hodnota_demo(4)
    return verify(r == 400,
        "✓ Sdílená Value: 4 procesy × 100 = 400!",
        f"✗ Dostal {r}, má být 400. Chybí Lock nebo Value?")


def _test_vzdalenosti():
    body = [(3, 4), (0, 5), (1, 1)]
    r = vzdalenosti_robotu(body)
    ocekavano = [5.0, 5.0, round(math.sqrt(2), 4)]
    return verify(r == ocekavano,
        f"✓ Vzdálenosti robotů: {r}",
        f"✗ Očekáváno {ocekavano}, dostal {r}")


def _test_manager():
    r = sdileny_slovnik_demo(5)
    ok = len(r) == 5 and all(r[i] == 'hotovo' for i in range(5))
    return verify(ok,
        "✓ Manager dict: všech 5 robotů reportovalo 'hotovo'!",
        f"✗ Slovník: {r}")


challenges = [
    Challenge(
        title="🔀 Multiprocessing vs Threading — teorie",
        theory=(
            "multiprocessing spouští samostatné procesy s vlastní pamětí → obchází GIL.\n"
            "  • Každý proces má svůj GIL → skutečný paralelismus na vícejádrových CPU\n"
            "  • Vhodné pro: CPU-bound úlohy (výpočty, zpracování obrazu v robotice)\n"
            "  • Vyšší overhead: nový Python interpret, kopírování dat mezi procesy\n"
            "  • Sdílení dat: multiprocessing.Value, Array, Manager (ne běžné proměnné!)\n"
            "  • Pool: fond procesů pro distribuci práce přes map/starmap/apply_async"
        ),
        task="Vyplň slovník v teorie_multiprocessing() správnými hodnotami.",
        difficulty=1, points=15,
        hints=[
            "multiprocessing obchází GIL → vicejadra=True",
            "CPU-bound = výpočetně náročné (FFT, detekce objektů)",
            "Procesy mají vlastní paměť → sdílený Array/Value, ne běžné listy",
        ],
        tests=[_test_teorie],
    ),
    Challenge(
        title="⚡ Pool.map — paralelní faktoriál",
        theory=(
            "multiprocessing.Pool vytvoří fond pracovních procesů:\n"
            "  with multiprocessing.Pool(4) as pool:\n"
            "      vysledky = pool.map(fn, iterovatelny_objekt)\n"
            "Pool.map je blokující — čeká na všechny výsledky.\n"
            "Robotický příklad: zpracuj 100 snímků z kamery paralelně."
        ),
        task=(
            "Implementuj paralelni_faktorial(cisla) pomocí Pool(2).map.\n"
            "Definuj pomocnou funkci faktorial(n) a předej ji do pool.map."
        ),
        difficulty=1, points=15,
        hints=[
            "with multiprocessing.Pool(2) as pool:",
            "    return pool.map(faktorial, cisla)",
            "Funkce předávaná do Pool musí být pickle-able (definuj mimo třídu/lambda)",
        ],
        tests=[_test_pool_map],
    ),
    Challenge(
        title="💾 Sdílená Value — bezpečný čítač mezi procesy",
        theory=(
            "Procesy nesdílí paměť automaticky → musíme použít speciální objekty:\n"
            "  counter = multiprocessing.Value('i', 0)  # 'i' = int\n"
            "  lock = multiprocessing.Lock()\n"
            "  with lock:\n"
            "      counter.value += 1\n"
            "Bez locku může dojít k race condition i u Value!"
        ),
        task=(
            "Implementuj sdilena_hodnota_demo(pocet_procesu).\n"
            "Každý proces inkrementuje Value 100×. Výsledek = pocet_procesu × 100."
        ),
        difficulty=2, points=20,
        hints=[
            "counter = multiprocessing.Value('i', 0)",
            "lock = multiprocessing.Lock()",
            "Předej counter i lock jako argumenty do procesu (args=(counter, lock, 100))",
        ],
        tests=[_test_sdilena],
    ),
    Challenge(
        title="🤖 Pool.starmap — vzdálenosti robotů",
        theory=(
            "Pool.starmap je jako map, ale funkce přijímá více argumentů:\n"
            "  pool.starmap(fn, [(arg1a, arg1b), (arg2a, arg2b), ...])\n"
            "Vhodné pro: výpočet vzdáleností, transformace souřadnic, senzorová data.\n"
            "Robotický příklad: paralelní výpočet vzdáleností obstacle pointů od robota."
        ),
        task=(
            "Implementuj vzdalenosti_robotu(body) pomocí Pool(2).starmap.\n"
            "body = seznam (x, y) n-tic. Vrať sqrt(x²+y²) pro každý bod, 4 des. místa."
        ),
        difficulty=2, points=20,
        hints=[
            "pool.starmap(vzdalenost, body)  — body jsou (x,y) n-tice",
            "round(math.sqrt(x**2 + y**2), 4)",
            "Funkce vzdalenost(x, y) musí být definována mimo Pool volání",
        ],
        tests=[_test_vzdalenosti],
    ),
    Challenge(
        title="📋 Manager — sdílený slovník mezi procesy",
        theory=(
            "multiprocessing.Manager() vytvoří server process spravující sdílené objekty:\n"
            "  with multiprocessing.Manager() as manager:\n"
            "      d = manager.dict()\n"
            "      lst = manager.list()\n"
            "Manager podporuje: dict, list, Value, Queue, Lock, ...\n"
            "Robotický příklad: každý robot (proces) reportuje svůj stav do sdílené mapy."
        ),
        task=(
            "Implementuj sdileny_slovnik_demo(pocet_robotu).\n"
            "Každý proces zapíše sdileny_stav[robot_id] = 'hotovo'.\n"
            "Vrať finální slovník s pocet_robotu záznamy."
        ),
        difficulty=3, points=25,
        hints=[
            "manager = multiprocessing.Manager()",
            "stav = manager.dict()",
            "Předej stav jako argument do procesu — nelze použít globální proměnnou",
        ],
        tests=[_test_manager],
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "🔀 Multiprocessing", "13_02")
