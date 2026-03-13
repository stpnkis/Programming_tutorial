#!/usr/bin/env python3
"""⚡ Asyncio — async/await, event loop, coroutines, gather, Tasks."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

import asyncio
import time

# ============================================================
# ⚡ ASYNCIO CVIČENÍ
# ============================================================


# VÝZVA 1: Teorie — asyncio koncepty
def teorie_asyncio():
    """🎯 VÝZVA 1: Vrať slovník se správnými odpověďmi o asyncio."""
    # TODO: ↓ vyplň správnými hodnotami
    return {
        "event_loop": None,          # "co je event loop" — "smyčka zpracovávající coroutiny"
        "async_vhodne_pro": None,    # "IO-bound" nebo "CPU-bound"
        "gather_ucel": None,         # "spustit více coroutin souběžně"
        "await_blokuje_loop": None,  # True/False: await blokuje celý event loop?
        "task_vs_coroutine": None,   # "Task je naplánovaná coroutina v event loop"
    }


# VÝZVA 2: První coroutina — async def a await
async def pozdrav_async(jmeno: str) -> str:
    """
    🎯 VÝZVA 2: Coroutina vracející pozdrav po 0.1 s prodlevě.
    Vrať string: "Ahoj, {jmeno}!"

    Použij: await asyncio.sleep(0.1)
    """
    # TODO: ↓ await asyncio.sleep(0.1) pak vrať pozdrav
    pass


def spust_pozdrav(jmeno: str) -> str:
    """Spustí pozdrav_async synchronně (pro testování)."""
    return asyncio.run(pozdrav_async(jmeno))


# VÝZVA 3: asyncio.gather — souběžné coroutiny
async def parallel_fetch_simulace(roboti: list) -> list:
    """
    🎯 VÝZVA 3: Simulace paralelního dotazování N robotů na jejich stav.
    Každý robot spí 0.1 s (simulace síťového dotazu) a vrátí "{jmeno}:OK".

    Použij asyncio.gather() pro souběžné spuštění.
    Vrať seznam výsledků ve stejném pořadí jako vstupní seznam.

    Příklad: await parallel_fetch_simulace(["R1","R2"]) → ["R1:OK","R2:OK"]
    """
    async def dotaz_robot(jmeno):
        # TODO: ↓ await asyncio.sleep(0.1) a vrať f"{jmeno}:OK"
        pass

    # TODO: ↓ asyncio.gather(*[dotaz_robot(r) for r in roboti])
    pass


def spust_parallel_fetch(roboti: list) -> list:
    return asyncio.run(parallel_fetch_simulace(roboti))


# VÝZVA 4: asyncio.Task a časování
async def zpracuj_s_timeoutem(coroutina, timeout_s: float):
    """
    🎯 VÝZVA 4: Spusť coroutinu s timeoutem.
    Pokud coroutina skončí včas → vrať výsledek.
    Pokud vyprší timeout → vrať None.

    Použij: asyncio.wait_for(coroutina, timeout=timeout_s)
    Odchyť: asyncio.TimeoutError
    """
    try:
        # TODO: ↓ return await asyncio.wait_for(coroutina, timeout=timeout_s)
        pass
    except asyncio.TimeoutError:
        # TODO: ↓ vrať None
        pass


async def pomala_operace(cekej: float, vysledek):
    await asyncio.sleep(cekej)
    return vysledek


def spust_timeout_test(cekej: float, timeout: float):
    return asyncio.run(zpracuj_s_timeoutem(pomala_operace(cekej, "hotovo"), timeout))


# VÝZVA 5: Producer-consumer s asyncio.Queue (senzorová data)
async def sensor_pipeline(pocet_vzorku: int) -> list:
    """
    🎯 VÝZVA 5: Implementuj async producer-consumer pipeline.

    Producer: generuje `pocet_vzorku` hodnot (0..N-1) do Queue s prodlevou 0.01 s.
    Consumer: čte z Queue, přidá 100 ke každé hodnotě, uloží do výsledků.
    Producer pošle sentinel (None) pro ukončení consumera.

    Vrať setříděný seznam zpracovaných hodnot.
    Příklad: sensor_pipeline(3) → [100, 101, 102]
    """
    fronta = asyncio.Queue()
    vysledky = []

    async def producer():
        for i in range(pocet_vzorku):
            await asyncio.sleep(0.01)
            # TODO: ↓ await fronta.put(i)
            pass
        # TODO: ↓ await fronta.put(None)  # sentinel

    async def consumer():
        while True:
            # TODO: ↓ hodnota = await fronta.get()
            hodnota = None
            if hodnota is None:
                break
            # TODO: ↓ vysledky.append(hodnota + 100)
            pass

    # TODO: ↓ await asyncio.gather(producer(), consumer())
    pass

    return sorted(vysledky)


def spust_pipeline(pocet: int) -> list:
    return asyncio.run(sensor_pipeline(pocet))


# ============================================================
# ✅ TESTY & CHALLENGES
# ============================================================

def _test_teorie():
    r = teorie_asyncio()
    ok = (
        isinstance(r, dict)
        and r.get("event_loop") == "smyčka zpracovávající coroutiny"
        and r.get("async_vhodne_pro") == "IO-bound"
        and r.get("gather_ucel") == "spustit více coroutin souběžně"
        and r.get("await_blokuje_loop") is False
        and r.get("task_vs_coroutine") == "Task je naplánovaná coroutina v event loop"
    )
    return verify(ok,
        "✓ Teorie asyncio správně!",
        "✗ Zkontroluj hodnoty. await neblokuje celý loop — jen aktuální coroutinu")


def _test_pozdrav():
    r = spust_pozdrav("Robot")
    return verify(r == "Ahoj, Robot!",
        "✓ Coroutina vrátila správný pozdrav!",
        f"✗ Očekáváno 'Ahoj, Robot!', dostal '{r}'")


def _test_gather():
    roboti = ["R1", "R2", "R3"]
    start = time.perf_counter()
    r = spust_parallel_fetch(roboti)
    elapsed = time.perf_counter() - start
    # Souběžně → ~0.1 s, ne 0.3 s
    ok = r == ["R1:OK", "R2:OK", "R3:OK"] and elapsed < 0.25
    return verify(ok,
        f"✓ gather: {r} za {elapsed:.2f}s (souběžně!)",
        f"✗ Výsledek: {r}, čas: {elapsed:.2f}s. Použil jsi gather? Pořadí správné?")


def _test_timeout():
    r_ok = spust_timeout_test(cekej=0.05, timeout=0.2)
    r_timeout = spust_timeout_test(cekej=0.5, timeout=0.1)
    return verify(r_ok == "hotovo" and r_timeout is None,
        "✓ wait_for: včasný výsledek 'hotovo', timeout vrátil None!",
        f"✗ Včasný={r_ok} (má být 'hotovo'), timeout={r_timeout} (má být None)")


def _test_pipeline():
    r = spust_pipeline(5)
    ocekavano = [100, 101, 102, 103, 104]
    return verify(r == ocekavano,
        f"✓ Sensor pipeline: {r}",
        f"✗ Očekáváno {ocekavano}, dostal {r}")


challenges = [
    Challenge(
        title="⚡ Asyncio teorie — event loop a coroutiny",
        theory=(
            "asyncio je jednovláknový model souběžnosti pro IO-bound úlohy:\n"
            "  • Event loop: nekonečná smyčka zpracovávající naplánované coroutiny\n"
            "  • coroutina: funkce definovaná s async def, spouštěná přes await\n"
            "  • await: předá řízení zpět event loopu (nablokuje celý loop!)\n"
            "  • Task: coroutina naplánovaná a spravovaná event loopem\n"
            "  • gather: spustí více coroutin souběžně\n"
            "Robotický příklad: async čtení z N senzorů/kamer bez blokování."
        ),
        task="Vyplň slovník v teorie_asyncio() správnými hodnotami.",
        difficulty=1, points=15,
        hints=[
            "event_loop = 'smyčka zpracovávající coroutiny'",
            "await předá řízení loopu — ostatní coroutiny mohou běžet → await_blokuje_loop=False",
            "Task je coroutina naplánovaná schedulerem event loopu",
        ],
        tests=[_test_teorie],
    ),
    Challenge(
        title="🌟 První coroutina — async def & await",
        theory=(
            "Coroutina se definuje pomocí async def a volá pomocí await:\n"
            "  async def moje_fn():\n"
            "      await asyncio.sleep(1)  # nablokující čekání\n"
            "      return 'hotovo'\n"
            "  result = asyncio.run(moje_fn())  # spuštění z sync kódu\n"
            "asyncio.sleep() je async verze time.sleep() — nepřeruší event loop!"
        ),
        task=(
            "Implementuj pozdrav_async(jmeno):\n"
            "  1. await asyncio.sleep(0.1)\n"
            "  2. return f'Ahoj, {jmeno}!'"
        ),
        difficulty=1, points=15,
        hints=[
            "async def pozdrav_async(jmeno: str) -> str:",
            "    await asyncio.sleep(0.1)",
            "    return f'Ahoj, {jmeno}!'",
        ],
        tests=[_test_pozdrav],
    ),
    Challenge(
        title="🚀 asyncio.gather — souběžné dotazy na roboty",
        theory=(
            "asyncio.gather() spustí více coroutin souběžně:\n"
            "  vysledky = await asyncio.gather(co1(), co2(), co3())\n"
            "Výsledky jsou ve stejném pořadí jako coroutiny.\n"
            "3 roboti každý čeká 0.1 s → souběžně 0.1 s celkem (ne 0.3 s!)\n"
            "Robotická aplikace: paralelní health-check N robotů přes TCP."
        ),
        task=(
            "Implementuj parallel_fetch_simulace(roboti).\n"
            "Definuj async dotaz_robot(jmeno) se sleep(0.1) a vrať '{jmeno}:OK'.\n"
            "Použij asyncio.gather pro souběžné spuštění."
        ),
        difficulty=2, points=20,
        hints=[
            "results = await asyncio.gather(*[dotaz_robot(r) for r in roboti])",
            "return list(results)",
            "Pořadí výsledků odpovídá vstupu — gather zachovává pořadí",
        ],
        tests=[_test_gather],
    ),
    Challenge(
        title="⏰ asyncio.wait_for — timeout pro senzorové operace",
        theory=(
            "asyncio.wait_for() přidá timeout k libovolné coroutině:\n"
            "  try:\n"
            "      result = await asyncio.wait_for(coroutina, timeout=1.0)\n"
            "  except asyncio.TimeoutError:\n"
            "      print('Timeout!')\n"
            "Robotická aplikace: senzor neodpovídá do 500 ms → přejdi na zálohu."
        ),
        task=(
            "Implementuj zpracuj_s_timeoutem(coroutina, timeout_s).\n"
            "Pokud coroutina skončí včas → vrať výsledek.\n"
            "Pokud TimeoutError → vrať None."
        ),
        difficulty=2, points=20,
        hints=[
            "return await asyncio.wait_for(coroutina, timeout=timeout_s)",
            "except asyncio.TimeoutError: return None",
            "asyncio.TimeoutError je podtřída TimeoutError i Exception",
        ],
        tests=[_test_timeout],
    ),
    Challenge(
        title="🔄 Async Queue — senzorová pipeline",
        theory=(
            "asyncio.Queue pro komunikaci mezi coroutinami:\n"
            "  fronta = asyncio.Queue()\n"
            "  await fronta.put(data)   # producer\n"
            "  data = await fronta.get() # consumer\n"
            "Sentinel pattern: put(None) signalizuje konec streamu.\n"
            "Robotická aplikace: async čtení z kamery → async zpracování snímků."
        ),
        task=(
            "Implementuj sensor_pipeline(pocet_vzorku):\n"
            "  • producer: vloží 0..N-1 do Queue (sleep 0.01), pak None (sentinel)\n"
            "  • consumer: čte z Queue, přidá 100 ke každé hodnotě\n"
            "  • spusť obě coroutiny přes gather"
        ),
        difficulty=3, points=25,
        hints=[
            "fronta = asyncio.Queue()",
            "await fronta.put(i)  // await fronta.put(None)",
            "hodnota = await fronta.get()  →  if hodnota is None: break",
        ],
        tests=[_test_pipeline],
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "⚡ Asyncio", "13_03")
