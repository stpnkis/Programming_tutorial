#!/usr/bin/env python3
"""⏱️ Real-time systémy — priority, scheduling, timing, latency, watchdog, robotika."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

import threading
import time
import heapq

# ============================================================
# ⏱️ REAL-TIME SYSTÉMY CVIČENÍ
# ============================================================


# VÝZVA 1: Teorie — real-time systémy
def teorie_realtime():
    """🎯 VÝZVA 1: Vrať slovník se správnými odpověďmi o real-time systémech."""
    # TODO: ↓ vyplň správnými hodnotami
    return {
        "hard_vs_soft_rt": None,
            # "hard: nedodržení deadline = selhání systému; soft: degradace výkonu"
        "jitter": None,
            # "variabilita v časování — odchylka od očekávaného okamžiku"
        "watchdog_ucel": None,
            # "detekce zamrzlého procesu/vlákna a jeho reset"
        "ROS2_executor_typ": None,
            # "MultiThreadedExecutor" nebo "SingleThreadedExecutor" pro paralelismus
        "periodicka_uloha_ms": None,
            # int: typická perioda řídicí smyčky robotického ramena v ms (1-10)
    }


# VÝZVA 2: Přesné periodické spuštění (real-time smyčka)
def periodic_loop(perioda_s: float, pocet_iteraci: int) -> list:
    """
    🎯 VÝZVA 2: Implementuj přesnou periodickou smyčku.

    Každou iteraci zaznamenej aktuální čas (time.perf_counter()).
    Použij drift-compensated timing: next_time += perioda (ne sleep(perioda)).

    Vrať seznam N zaznamenaných časových razítek.
    Jitter (max - min výpočet rozestupů) musí být < 0.02 s.

    Hint: next_time = time.perf_counter() + perioda_s
          while ...: time.sleep(max(0, next_time - time.perf_counter()))
                     zaznamenej; next_time += perioda_s
    """
    zaznamy = []
    # TODO: ↓ implementuj drift-compensated periodic loop
    pass
    return zaznamy


def _zkontroluj_jitter(zaznamy, perioda_s):
    """Spočítá max jitter ze seznamu časových razítek."""
    if len(zaznamy) < 2:
        return float('inf')
    rozestupy = [zaznamy[i+1] - zaznamy[i] for i in range(len(zaznamy)-1)]
    odchylky = [abs(r - perioda_s) for r in rozestupy]
    return max(odchylky)


# VÝZVA 3: Watchdog timer
class Watchdog:
    """
    🎯 VÝZVA 3: Implementuj Watchdog timer.

    Watchdog spustí callback pokud není reset() zavolán do `timeout_s` sekund.
    Reset prodlouží timeout.
    Stop() zastaví watchdoga.

    Robotická aplikace: pokud řídicí smyčka přestane resetovat watchdog
    → watchdog zavolá nouzové zastavení.
    """
    def __init__(self, timeout_s: float, callback):
        self.timeout_s = timeout_s
        self.callback = callback
        self._timer = None
        self._stopped = False
        # TODO: ↓ spusť watchdog timer (self._restart())

    def _restart(self):
        """Zruší starý timer a naplánuje nový."""
        if self._timer:
            self._timer.cancel()
        if not self._stopped:
            # TODO: ↓ self._timer = threading.Timer(self.timeout_s, self._on_timeout)
            # TODO: ↓ self._timer.daemon = True
            # TODO: ↓ self._timer.start()
            pass

    def _on_timeout(self):
        """Zavolá callback při vypršení."""
        # TODO: ↓ self.callback()
        pass

    def reset(self):
        """Resetuje watchdog — prodlouží timeout."""
        # TODO: ↓ self._restart()
        pass

    def stop(self):
        """Zastaví watchdog."""
        self._stopped = True
        if self._timer:
            # TODO: ↓ self._timer.cancel()
            pass


# VÝZVA 4: Prioritní scheduler úloh (EDF — Earliest Deadline First)
class EDFScheduler:
    """
    🎯 VÝZVA 4: Jednoduchý EDF (Earliest Deadline First) scheduler.

    add_task(deadline, task_fn): přidá úlohu s daným deadline (float, abs. čas)
    run_all(): spustí úlohy v pořadí dle deadline (nejbližší první)
    Vrátí seznam výsledků funkcí v pořadí spuštění.

    Robotika: řídicí smyčka musí splnit kritické deadlines před méně důležitými úlohami.
    """
    def __init__(self):
        # TODO: ↓ self._heap = [] (min-heap: (deadline, task_fn))
        pass

    def add_task(self, deadline: float, task_fn):
        # TODO: ↓ heapq.heappush(self._heap, (deadline, task_fn))
        pass

    def run_all(self) -> list:
        vysledky = []
        # TODO: ↓ while self._heap: deadline, fn = heapq.heappop(self._heap); vysledky.append(fn())
        pass
        return vysledky


# VÝZVA 5: Měření latence — timing analýza
def analyzuj_latenci(mereni_us: list) -> dict:
    """
    🎯 VÝZVA 5: Analyzuj seznam naměřených latencí v mikrosekundách.

    Vrať slovník:
      min_us: minimální latence
      max_us: maximální latence
      avg_us: průměrná latence (zaokrouhleno na 2 des. místa)
      jitter_us: max_us - min_us
      nad_1ms: počet měření > 1000 µs (latence přes 1 ms)
      percentil_99_us: 99. percentil (seřaď, ber index int(0.99 * N))

    Robotika: analýza latence CAN sběrnice, síťové komunikace, reakce servomotoru.
    """
    if not mereni_us:
        return {}

    # TODO: ↓ implementuj všechny statistiky
    return {
        "min_us": None,
        "max_us": None,
        "avg_us": None,
        "jitter_us": None,
        "nad_1ms": None,
        "percentil_99_us": None,
    }


# ============================================================
# ✅ TESTY & CHALLENGES
# ============================================================

def _test_teorie():
    r = teorie_realtime()
    ok = (
        isinstance(r, dict)
        and r.get("hard_vs_soft_rt") == "hard: nedodržení deadline = selhání systému; soft: degradace výkonu"
        and r.get("jitter") == "variabilita v časování — odchylka od očekávaného okamžiku"
        and r.get("watchdog_ucel") == "detekce zamrzlého procesu/vlákna a jeho reset"
        and r.get("ROS2_executor_typ") == "MultiThreadedExecutor"
        and isinstance(r.get("periodicka_uloha_ms"), int)
        and 1 <= r.get("periodicka_uloha_ms") <= 10
    )
    return verify(ok,
        "✓ Teorie real-time systémů správně!",
        "✗ Zkontroluj: hard RT = selhání při miss, jitter = variabilita, "
        "watchdog = detekce zamrznutí, ROS2 = MultiThreadedExecutor")


def _test_periodic():
    zaznamy = periodic_loop(perioda_s=0.05, pocet_iteraci=6)
    ok_pocet = len(zaznamy) == 6
    jitter = _zkontroluj_jitter(zaznamy, 0.05)
    ok_jitter = jitter < 0.02
    return verify(ok_pocet and ok_jitter,
        f"✓ Periodic loop: {len(zaznamy)} iterací, jitter={jitter*1000:.1f} ms",
        f"✗ Počet={len(zaznamy)} (má být 6), jitter={jitter*1000:.1f} ms (má být <20 ms). "
        f"Použij drift compensation: next_time += perioda")


def _test_watchdog():
    spusteno = []

    def alarm():
        spusteno.append(True)

    wd = Watchdog(timeout_s=0.1, callback=alarm)

    # Reset watchdoga — neměl by spustit alarm
    time.sleep(0.06)
    wd.reset()
    time.sleep(0.06)
    wd.reset()
    time.sleep(0.06)
    wd.stop()

    # Kontrola: s resetem neměl alarm spustit
    ok_no_alarm = len(spusteno) == 0

    # Nový watchdog BEZ resetování — MAL BY spustit alarm
    spusteno2 = []
    wd2 = Watchdog(timeout_s=0.1, callback=lambda: spusteno2.append(True))
    time.sleep(0.2)

    ok_alarm = len(spusteno2) >= 1

    return verify(ok_no_alarm and ok_alarm,
        "✓ Watchdog: reset prodlužuje timeout, bez resetu spustí alarm!",
        f"✗ S resety: {len(spusteno)} alarmů (má být 0); "
        f"bez resetu: {len(spusteno2)} alarmů (má být ≥1)")


def _test_edf():
    now = time.perf_counter()
    scheduler = EDFScheduler()
    vysledky_poradi = []

    scheduler.add_task(now + 0.3, lambda: vysledky_poradi.append("C") or "C")
    scheduler.add_task(now + 0.1, lambda: vysledky_poradi.append("A") or "A")
    scheduler.add_task(now + 0.2, lambda: vysledky_poradi.append("B") or "B")

    r = scheduler.run_all()
    ok = vysledky_poradi == ["A", "B", "C"]
    return verify(ok,
        f"✓ EDF scheduler: pořadí {vysledky_poradi} — nejbližší deadline první!",
        f"✗ Pořadí {vysledky_poradi}, má být ['A','B','C']. Použij heapq?")


def _test_latence():
    mereni = [100, 200, 1500, 300, 500, 800, 1200, 50, 900, 400]
    r = analyzuj_latenci(mereni)
    ok = (
        isinstance(r, dict)
        and r.get("min_us") == 50
        and r.get("max_us") == 1500
        and r.get("avg_us") == round(sum(mereni) / len(mereni), 2)
        and r.get("jitter_us") == 1450
        and r.get("nad_1ms") == 2
        and r.get("percentil_99_us") == sorted(mereni)[int(0.99 * len(mereni))]
    )
    return verify(ok,
        f"✓ Analýza latence: min={r.get('min_us')}, max={r.get('max_us')}, "
        f"jitter={r.get('jitter_us')}, nad 1ms={r.get('nad_1ms')}",
        f"✗ Zkontroluj výpočty. Dostal: {r}")


challenges = [
    Challenge(
        title="⏱️ Real-time teorie — hard RT vs soft RT",
        theory=(
            "Real-time systémy musí reagovat v definovaných časových mezích:\n"
            "  Hard RT: překročení deadline = selhání systému (airbag, robotická chirurgie)\n"
            "  Soft RT: překročení deadline = degradace (video streaming, web server)\n"
            "  Jitter: variabilita v časování — nízký jitter = předvídatelné chování\n"
            "  Watchdog: hardware/software timer, který resetuje systém při zamrznutí\n"
            "  ROS2 MultiThreadedExecutor: souběžné zpracování callbacků v ROS2\n"
            "  Řídicí smyčka robota: typicky 1-10 ms perioda (100-1000 Hz)"
        ),
        task="Vyplň slovník v teorie_realtime() správnými hodnotami.",
        difficulty=1, points=15,
        hints=[
            "Hard RT: nedodržení deadline = selhání systému; soft RT: degradace výkonu",
            "Jitter = variabilita v časování — odchylka od očekávaného okamžiku",
            "ROS2 MultiThreadedExecutor umožňuje paralelní callbacks",
        ],
        tests=[_test_teorie],
    ),
    Challenge(
        title="🔄 Periodická smyčka — drift compensation",
        theory=(
            "Naivní implementace: while True: work(); sleep(T)\n"
            "  → drift: každá iterace je T + čas_práce → smyčka se zpomaluje!\n"
            "Správná implementace (drift-compensated):\n"
            "  next_time = perf_counter() + T\n"
            "  while True:\n"
            "      work()\n"
            "      sleep(max(0, next_time - perf_counter()))\n"
            "      next_time += T  # absolutní čas, ne relativní!\n"
            "Robotika: řídicí smyčka servomotorů musí mít stabilní periodu."
        ),
        task=(
            "Implementuj periodic_loop(perioda_s, pocet_iteraci).\n"
            "Používej drift-compensated timing (next_time += perioda_s).\n"
            "Zaznamenej čas každé iterace přes time.perf_counter()."
        ),
        difficulty=2, points=20,
        hints=[
            "next_time = time.perf_counter() + perioda_s",
            "time.sleep(max(0, next_time - time.perf_counter()))",
            "zaznamy.append(time.perf_counter())  pak  next_time += perioda_s",
        ],
        tests=[_test_periodic],
    ),
    Challenge(
        title="🐕 Watchdog timer — detekce zamrznutí",
        theory=(
            "Watchdog timer restartuje systém pokud nedostane heartbeat signal:\n"
            "  threading.Timer(T, callback) — jednorázový timer v novém vlákně\n"
            "  timer.cancel()  — zruší naplánovaný callback\n"
            "Pattern:\n"
            "  def reset(): timer.cancel(); timer = Timer(T, alarm); timer.start()\n"
            "Robotická aplikace: pokud navigační node přestane publikovat po dobu T,\n"
            "watchdog zavolá nouzové zastavení robota."
        ),
        task=(
            "Implementuj třídu Watchdog(timeout_s, callback).\n"
            "  __init__: spusť timer\n"
            "  reset(): zruš starý timer, naplánuj nový\n"
            "  stop(): zruš timer bez spuštění callbacku"
        ),
        difficulty=2, points=20,
        hints=[
            "self._timer = threading.Timer(self.timeout_s, self._on_timeout)",
            "self._timer.daemon = True  # nezasekne ukončení programu",
            "V reset(): cancel starý timer → new Timer → start",
        ],
        tests=[_test_watchdog],
    ),
    Challenge(
        title="📋 EDF Scheduler — Earliest Deadline First",
        theory=(
            "EDF je optimální scheduling algoritmus pro real-time systémy:\n"
            "  Vždy zpracuj úlohu s nejbližším deadlinem jako první.\n"
            "  Implementace: min-heap dle deadline\n"
            "    import heapq\n"
            "    heapq.heappush(heap, (deadline, fn))\n"
            "    deadline, fn = heapq.heappop(heap)\n"
            "Robotická aplikace: senzorová data s timestampem → zpracuj nejstarší první."
        ),
        task=(
            "Implementuj EDFScheduler:\n"
            "  __init__: self._heap = []\n"
            "  add_task(deadline, fn): heappush\n"
            "  run_all(): spusť v pořadí deadline, vrať výsledky"
        ),
        difficulty=2, points=20,
        hints=[
            "import heapq",
            "heapq.heappush(self._heap, (deadline, task_fn))",
            "deadline, fn = heapq.heappop(self._heap)  →  vysledky.append(fn())",
        ],
        tests=[_test_edf],
    ),
    Challenge(
        title="📊 Analýza latence — timing statistiky",
        theory=(
            "Analýza latence je klíčová pro real-time ladění:\n"
            "  min/max: rozsah měření\n"
            "  avg: průměr\n"
            "  jitter: max - min (šíře variability)\n"
            "  percentil 99: 99 % měření je pod touto hodnotou\n"
            "    idx = int(0.99 * N)  →  sorted_data[idx]\n"
            "Robotická aplikace: analýza latence CAN sběrnice, etherCAT, ROS2 topic."
        ),
        task=(
            "Implementuj analyzuj_latenci(mereni_us).\n"
            "Vrať dict: min_us, max_us, avg_us (2 des. místa), jitter_us,\n"
            "           nad_1ms (počet > 1000), percentil_99_us."
        ),
        difficulty=3, points=25,
        hints=[
            "min_us = min(mereni_us)  //  max_us = max(mereni_us)",
            "avg_us = round(sum(mereni_us) / len(mereni_us), 2)",
            "percentil: serazeno = sorted(mereni_us); serazeno[int(0.99 * len(mereni_us))]",
        ],
        tests=[_test_latence],
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "⏱️ Real-time systémy", "13_05")
