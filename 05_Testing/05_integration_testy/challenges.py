#!/usr/bin/env python3
"""🔗 Testing — Integrační testy: Jak spolupracují komponenty."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify

# ============================================================
# SYSTÉM K TESTOVÁNÍ
# ============================================================

class Databaze:
    def __init__(self):
        self._data = {}
    def uloz(self, klic, hodnota):
        self._data[klic] = hodnota
    def nacti(self, klic):
        return self._data.get(klic)
    def smaz(self, klic):
        self._data.pop(klic, None)
    def existuje(self, klic):
        return klic in self._data

class UserService:
    def __init__(self, db):
        self.db = db
    def registruj(self, username, heslo):
        if self.db.existuje(f"user:{username}"):
            raise ValueError(f"Uživatel {username} existuje")
        if len(heslo) < 6:
            raise ValueError("Heslo příliš krátké")
        self.db.uloz(f"user:{username}", {"heslo": heslo, "aktivni": True})
        return True
    def prihlasit(self, username, heslo):
        data = self.db.nacti(f"user:{username}")
        if not data or data["heslo"] != heslo:
            return False
        return True
    def deaktivuj(self, username):
        data = self.db.nacti(f"user:{username}")
        if data:
            data["aktivni"] = False
            self.db.uloz(f"user:{username}", data)

class OrderService:
    def __init__(self, db, user_service):
        self.db = db
        self.users = user_service
        self._order_counter = 0
    def vytvor_objednavku(self, username, polozky):
        data = self.db.nacti(f"user:{username}")
        if not data or not data.get("aktivni"):
            raise ValueError("Neplatný uživatel")
        self._order_counter += 1
        order_id = f"order:{self._order_counter}"
        self.db.uloz(order_id, {"user": username, "polozky": polozky, "stav": "nová"})
        return order_id

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def test_registrace_a_prihlaseni() -> bool:
    """
    🎯 VÝZVA 1: Integrační test — registrace + přihlášení.
    1. Vytvoř DB a UserService
    2. Registruj uživatele "jan", heslo "tajne123"
    3. Ověř přihlášení se správným heslem → True
    4. Ověř přihlášení se špatným heslem → False
    Vrať True pokud vše OK.
    """
    # TODO: ↓
    pass


def test_duplikat_registrace() -> bool:
    """
    🎯 VÝZVA 2: Test duplikátní registrace.
    1. Registruj "jan"
    2. Zkus registrovat "jan" znovu → ValueError
    Vrať True pokud chytíš ValueError.
    """
    # TODO: ↓
    pass


def test_objednavka_workflow() -> bool:
    """
    🎯 VÝZVA 3: Celý workflow — registrace → objednávka.
    1. Vytvoř DB, UserService, OrderService
    2. Registruj uživatele
    3. Vytvoř objednávku
    4. Ověř, že objednávka existuje v DB
    Vrať True pokud OK.
    """
    # TODO: ↓
    pass


def test_deaktivovany_neobjedna() -> bool:
    """
    🎯 VÝZVA 4: Deaktivovaný uživatel nemůže objednávat.
    1. Registruj a pak deaktivuj uživatele
    2. Zkus vytvořit objednávku → ValueError
    Vrať True pokud správně selže.
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Registrace + Přihlášení flow",
        theory="""INTEGRAČNÍ TESTY testují spolupráci komponent.

Unit test: testuje JEDNU funkci izolovaně
Integrační test: testuje CELÝ WORKFLOW

  DB ←→ UserService ←→ OrderService

Postup:
1. Připrav skutečné (ne mock) objekty
2. Proveď celý workflow
3. Ověř výsledek

Integrační testy jsou POMALEJŠÍ, ale odhalí problémy
na rozhraních mezi komponentami.""",
        task="Otestuj registrace → přihlášení workflow.",
        difficulty=2, points=25,
        hints=["db = Databaze(); us = UserService(db); us.registruj(...); us.prihlasit(...)"],
        tests=[
            lambda: verify(test_registrace_a_prihlaseni() == True, "Registrace+login ✓"),
        ]
    ),
    Challenge(
        title="Duplikátní registrace",
        task="Ověř, že duplicitní registrace vyhodí chybu.",
        difficulty=1, points=15,
        hints=["try: us.registruj('jan',...) znovu; except ValueError: return True"],
        tests=[
            lambda: verify(test_duplikat_registrace() == True, "Duplikát → error ✓"),
        ]
    ),
    Challenge(
        title="Celý objednávkový flow",
        task="Registrace → objednávka → ověření v DB.",
        difficulty=2, points=25,
        hints=["os = OrderService(db, us); oid = os.vytvor_objednavku(...)"],
        tests=[
            lambda: verify(test_objednavka_workflow() == True, "Objednávka flow ✓"),
        ]
    ),
    Challenge(
        title="Deaktivovaný uživatel",
        task="Neaktivní uživatel = žádná objednávka.",
        difficulty=2, points=20,
        hints=["us.deaktivuj('jan'); try: os.vytvor_objednavku(...) except ValueError: True"],
        tests=[
            lambda: verify(test_deaktivovany_neobjedna() == True, "Deaktivace blokuje ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Integrační Testy", "05_05")
