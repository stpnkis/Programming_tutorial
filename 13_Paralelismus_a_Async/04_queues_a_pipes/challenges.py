#!/usr/bin/env python3
"""📦 Queues & Pipes — Queue, Pipe, producer-consumer, thread/process-safe fronty."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

import queue
import threading
import multiprocessing
import time

# ============================================================
# 📦 QUEUES & PIPES CVIČENÍ
# ============================================================


# VÝZVA 1: Teorie — fronty a roury
def teorie_queues_a_pipes():
    """🎯 VÝZVA 1: Vrať slovník s fakty o frontách a rourách."""
    # TODO: ↓ vyplň správnými hodnotami
    return {
        "queue_FIFO_poradi": None,         # True/False: queue.Queue je FIFO?
        "queue_LifoQueue_je": None,        # "zásobník" nebo "fronta"
        "Pipe_pocet_koncu": None,          # int: kolik konců má multiprocessing.Pipe?
        "thread_safe_queue": None,         # název thread-safe fronty z modulu queue
        "producer_consumer_vzor": None,    # "návrhový vzor pro oddělení produkce a konzumace"
    }


# VÝZVA 2: threading.Queue — thread-safe fronta
def threading_queue_demo(polozky: list) -> list:
    """
    🎯 VÝZVA 2: Producer-Consumer s queue.Queue.

    Producer vlákno vloží všechny `polozky` do fronty.
    Consumer vlákno čte z fronty a přidá 10 ke každé položce.
    Sentinel None ukončí consumera.

    Vrať zpracovaný seznam ve správném pořadí.
    Příklad: threading_queue_demo([1,2,3]) → [11, 12, 13]
    """
    fronta = queue.Queue()
    vysledky = []

    def producer():
        for p in polozky:
            # TODO: ↓ fronta.put(p)
            pass
        # TODO: ↓ fronta.put(None)  # sentinel

    def consumer():
        while True:
            # TODO: ↓ item = fronta.get()
            item = None
            if item is None:
                break
            # TODO: ↓ vysledky.append(item + 10)

    t_prod = threading.Thread(target=producer)
    t_cons = threading.Thread(target=consumer)
    # TODO: ↓ nastartuj a joinuj obě vlákna
    pass

    return vysledky


# VÝZVA 3: PriorityQueue — prioritní fronta (robotické úkoly)
def prioritni_fronta_demo(ukoly: list) -> list:
    """
    🎯 VÝZVA 3: Zpracuj robotické úkoly podle priority (nižší číslo = vyšší priorita).

    ukoly = [(priorita, nazev), ...]
    Vlož všechny do queue.PriorityQueue a vyber je v pořadí priority.

    Vrať seznam názvů úkolů v pořadí zpracování.
    Příklad: [(3,"C"),(1,"A"),(2,"B")] → ["A","B","C"]
    """
    pq = queue.PriorityQueue()

    for priorita, nazev in ukoly:
        # TODO: ↓ pq.put((priorita, nazev))
        pass

    vysledky = []
    while not pq.empty():
        # TODO: ↓ _, nazev = pq.get() a přidej do vysledky
        pass

    return vysledky


# VÝZVA 4: multiprocessing.Pipe — komunikace mezi procesy
def pipe_echo_demo(zpravy: list) -> list:
    """
    🎯 VÝZVA 4: Pošli zprávy přes multiprocessing.Pipe a přijmi je zpět.

    Vytoř Pipe (parent_conn, child_conn).
    Child process: čte ze child_conn, pošle "<zprava>_echo" zpět přes child_conn.
    Parent: pošle zprávy, přijme odpovědi.
    Sentinel "STOP" ukončí child process.

    Vrať seznam odpovědí.
    Příklad: pipe_echo_demo(["ahoj","ros2"]) → ["ahoj_echo","ros2_echo"]
    """
    parent_conn, child_conn = multiprocessing.Pipe()

    def child_worker(conn):
        while True:
            # TODO: ↓ zprava = conn.recv()
            zprava = None
            if zprava == "STOP":
                break
            # TODO: ↓ conn.send(f"{zprava}_echo")

    p = multiprocessing.Process(target=child_worker, args=(child_conn,))
    p.start()

    vysledky = []
    for z in zpravy:
        # TODO: ↓ parent_conn.send(z) a parent_conn.recv() → přidej do vysledky
        pass

    # TODO: ↓ parent_conn.send("STOP")
    p.join()
    return vysledky


# VÝZVA 5: multiprocessing.Queue — sdílená fronta mezi procesy
def mp_queue_senzory(senzory: list) -> dict:
    """
    🎯 VÝZVA 5: Každý senzor (process) čte svá data a vloží do sdílené fronty.
    Hlavní proces přečte výsledky.

    senzory = [("lidar", [1,2,3]), ("kamera", [4,5]), ("imu", [6])]
    Každý worker process: vloží (jmeno, sum(data)) do fronty.

    Vrať slovník {jmeno: sum(data)}.
    Příklad: [("s1",[1,2])] → {"s1": 3}
    """
    fronta = multiprocessing.Queue()

    def sensor_worker(jmeno, data, q):
        # TODO: ↓ q.put((jmeno, sum(data)))
        pass

    procesy = []
    for jmeno, data in senzory:
        p = multiprocessing.Process(target=sensor_worker, args=(jmeno, data, fronta))
        procesy.append(p)
        # TODO: ↓ p.start()

    for p in procesy:
        p.join()

    vysledek = {}
    while not fronta.empty():
        # TODO: ↓ jmeno, hodnota = fronta.get() a přidej do vysledek
        pass

    return vysledek


# ============================================================
# ✅ TESTY & CHALLENGES
# ============================================================

def _test_teorie():
    r = teorie_queues_a_pipes()
    ok = (
        isinstance(r, dict)
        and r.get("queue_FIFO_poradi") is True
        and r.get("queue_LifoQueue_je") == "zásobník"
        and r.get("Pipe_pocet_koncu") == 2
        and r.get("thread_safe_queue") == "Queue"
        and r.get("producer_consumer_vzor") == "návrhový vzor pro oddělení produkce a konzumace"
    )
    return verify(ok,
        "✓ Teorie front a rour správně!",
        "✗ FIFO=True, LifoQueue=zásobník, Pipe=2 konce, thread-safe='Queue'")


def _test_threading_queue():
    r = threading_queue_demo([1, 2, 3, 4, 5])
    ocekavano = [11, 12, 13, 14, 15]
    return verify(r == ocekavano,
        f"✓ Threading Queue: {r}",
        f"✗ Očekáváno {ocekavano}, dostal {r}")


def _test_prioritni():
    ukoly = [(3, "C"), (1, "A"), (2, "B"), (1, "AA")]
    r = prioritni_fronta_demo(ukoly)
    # priorita 1 = A a AA (pořadí mezi stejnou prioritou: dle názvu)
    ok = r[0] in ("A", "AA") and r[-1] == "C"
    return verify(ok,
        f"✓ PriorityQueue: {r} — nejdřív priorita 1, naposledy 3!",
        f"✗ Dostal {r}, první má být priorita 1 (A/AA), poslední C")


def _test_pipe():
    r = pipe_echo_demo(["ahoj", "ros2", "robot"])
    ocekavano = ["ahoj_echo", "ros2_echo", "robot_echo"]
    return verify(r == ocekavano,
        f"✓ Pipe echo: {r}",
        f"✗ Očekáváno {ocekavano}, dostal {r}")


def _test_mp_queue():
    senzory = [("lidar", [1, 2, 3]), ("kamera", [4, 5]), ("imu", [6])]
    r = mp_queue_senzory(senzory)
    ok = r == {"lidar": 6, "kamera": 9, "imu": 6}
    return verify(ok,
        f"✓ Multiprocessing Queue: {r}",
        f"✗ Očekáváno {{'lidar':6,'kamera':9,'imu':6}}, dostal {r}")


challenges = [
    Challenge(
        title="📦 Teorie front a rour",
        theory=(
            "Fronty a roury jsou hlavní způsob, jak bezpečně předávat data mezi vlákny/procesy:\n"
            "  queue.Queue        — thread-safe FIFO, pro threading\n"
            "  queue.LifoQueue    — thread-safe zásobník (LIFO)\n"
            "  queue.PriorityQueue — prvky dle priority (min-heap)\n"
            "  multiprocessing.Queue — process-safe fronta\n"
            "  multiprocessing.Pipe  — obousměrná roura (2 konce: parent, child)\n"
            "Producer-Consumer: producer generuje data, consumer zpracovává — oddělení zodpovědností."
        ),
        task="Vyplň slovník v teorie_queues_a_pipes() správnými hodnotami.",
        difficulty=1, points=15,
        hints=[
            "Queue = First In First Out → FIFO_poradi=True",
            "LifoQueue = Last In First Out = zásobník (stack)",
            "Pipe vrací (conn1, conn2) — 2 konce",
        ],
        tests=[_test_teorie],
    ),
    Challenge(
        title="🚦 Producer-Consumer s queue.Queue",
        theory=(
            "queue.Queue je thread-safe — žádný Lock není potřeba:\n"
            "  q = queue.Queue()\n"
            "  q.put(item)    # blokuje pokud maxsize dosažen\n"
            "  q.get()        # blokuje pokud prázdná\n"
            "Sentinel pattern: producent pošle None → consumer se ukončí.\n"
            "Robotika: fronta příkazů pro rameno — producer (planner) → consumer (executor)."
        ),
        task=(
            "Implementuj threading_queue_demo(polozky).\n"
            "Producer: vloží každou položku + None (sentinel).\n"
            "Consumer: čte, přičte 10, ukládá výsledky."
        ),
        difficulty=1, points=15,
        hints=[
            "fronta.put(p)  a na konci fronta.put(None)",
            "item = fronta.get()  →  if item is None: break",
            "t.start() pro obě vlákna, pak t.join() pro obě",
        ],
        tests=[_test_threading_queue],
    ),
    Challenge(
        title="⭐ PriorityQueue — plánování robotických úkolů",
        theory=(
            "queue.PriorityQueue zpracovává prvky dle priority (min-heap):\n"
            "  pq = queue.PriorityQueue()\n"
            "  pq.put((priorita, data))  # tuple — nižší číslo = vyšší priorita\n"
            "  priorita, data = pq.get()\n"
            "Robotická aplikace: nouzové zastavení (priorita 0) před rutinními úkoly (priorita 5)."
        ),
        task=(
            "Implementuj prioritni_fronta_demo(ukoly).\n"
            "Vlož (priorita, nazev) do PriorityQueue, pak vyzvedni v pořadí priority.\n"
            "Vrať seznam názvů."
        ),
        difficulty=2, points=20,
        hints=[
            "pq.put((priorita, nazev))",
            "while not pq.empty(): priorita, nazev = pq.get()",
            "Tuple porovnávání: (1,'A') < (2,'B') — nejprve priorita, pak název",
        ],
        tests=[_test_prioritni],
    ),
    Challenge(
        title="🔧 multiprocessing.Pipe — IPC komunikace",
        theory=(
            "Pipe je nejrychlejší IPC mechanismus pro 2 procesy:\n"
            "  parent_conn, child_conn = multiprocessing.Pipe()\n"
            "  conn.send(obj)   # pošle Python objekt (serialize přes pickle)\n"
            "  conn.recv()      # blokuje do příjmu\n"
            "Pokud duplexní=False → jednosměrná roura.\n"
            "Robotika: master proces posílá příkazy → worker proces plní úkoly."
        ),
        task=(
            "Implementuj pipe_echo_demo(zpravy).\n"
            "Child process: přijmi zprávu, odpověz '{zprava}_echo', zastav na 'STOP'.\n"
            "Parent: pošli zprávy, přijmi odpovědi."
        ),
        difficulty=2, points=20,
        hints=[
            "conn.recv() blokuje — čeká na zprávu",
            "conn.send(f'{zprava}_echo') v child workeru",
            "parent_conn.send(z) pak parent_conn.recv() → přidej do vysledky",
        ],
        tests=[_test_pipe],
    ),
    Challenge(
        title="🤖 multiprocessing.Queue — senzorová fúze",
        theory=(
            "multiprocessing.Queue je process-safe (ne jen thread-safe):\n"
            "  q = multiprocessing.Queue()\n"
            "  q.put(data)   # z libovolného procesu\n"
            "  q.get()       # blokuje\n"
            "  q.empty()     # True/False\n"
            "Robotická aplikace: LiDAR, kamera, IMU jsou samostatné procesy → výsledky\n"
            "posílají do hlavní fronty → sensor fusion modul zpracovává."
        ),
        task=(
            "Implementuj mp_queue_senzory(senzory).\n"
            "Každý worker process spočítá sum(data) a vloží (jmeno, sum) do fronty.\n"
            "Hlavní proces přečte výsledky a vrátí slovník."
        ),
        difficulty=3, points=25,
        hints=[
            "q.put((jmeno, sum(data))) v sensor_worker",
            "Nezapomeň p.start() pro každý proces",
            "while not fronta.empty(): jmeno, val = fronta.get()",
        ],
        tests=[_test_mp_queue],
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "📦 Queues & Pipes", "13_04")
