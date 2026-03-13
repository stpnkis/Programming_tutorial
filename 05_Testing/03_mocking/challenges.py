#!/usr/bin/env python3
"""🎭 Testing — Mocking: Testuj v izolaci."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from engine.runner import Challenge, run_challenges, verify
from unittest.mock import Mock, MagicMock, patch

# ============================================================
# KÓD K TESTOVÁNÍ
# ============================================================

class EmailService:
    def posli(self, adresa, zprava):
        """Reálně posílá email — chceme mockovat!"""
        raise NotImplementedError("V testu neposlíme skutečný email!")

class NotifikacniSystem:
    def __init__(self, email_service):
        self.email = email_service
    
    def upozorni(self, uzivatel, zprava):
        self.email.posli(uzivatel, zprava)
        return f"Notifikace odeslána: {uzivatel}"

class WeatherAPI:
    def get_teplota(self, mesto):
        """Reálně volá API — mockujeme!"""
        raise NotImplementedError("V testu nevoláme API!")

class WeatherApp:
    def __init__(self, api):
        self.api = api
    def doporuceni(self, mesto):
        teplota = self.api.get_teplota(mesto)
        if teplota > 25: return "Vezmi si šortky!"
        elif teplota < 5: return "Obleč se teple!"
        return "Příjemné počasí."

# ============================================================
# 📝 TVOJE ŘEŠENÍ
# ============================================================

def test_notifikace_s_mockem():
    """
    🎯 VÝZVA 1: Mockuj EmailService.
    - Vytvoř Mock() místo skutečného EmailService
    - Zavolej upozorni()
    - Ověř, že email.posli() bylo voláno se správnými argumenty
    Vrať True pokud test projde.
    """
    # TODO: ↓
    pass


def test_weather_horko():
    """
    🎯 VÝZVA 2: Mockuj WeatherAPI — testuj horké počasí.
    - Mock API vrátí 30°C
    - Ověř doporučení = "Vezmi si šortky!"
    Vrať True pokud projde.
    """
    # TODO: ↓
    pass


def test_weather_zima():
    """
    🎯 VÝZVA 2b: Mock API vrátí 0°C → "Obleč se teple!"
    """
    # TODO: ↓
    pass


def test_mock_side_effects():
    """
    🎯 VÝZVA 3: Side effects — mock vrací různé hodnoty.
    - Mock, co pokaždé vrátí jiný výsledek.
    - Použij side_effect=[10, 20, 30]
    Vrať True pokud 3 volání vrátí 10, 20, 30.
    """
    # TODO: ↓
    pass


# ============================================================
# 🔍 TESTY
# ============================================================

challenges = [
    Challenge(
        title="Mock EmailService",
        theory="""MOCKING = nahrada skutečného objektu falešným.

Proč?
- Nechceš v testu posílat skutečné emaily
- Nechceš volat skutečné API
- Nechceš zapisovat do skutečné databáze

from unittest.mock import Mock

mock_email = Mock()
mock_email.posli("a@b.cz", "Ahoj")  # nic se nestane

# Ověření:
mock_email.posli.assert_called_once_with("a@b.cz", "Ahoj")
mock_email.posli.call_count  # → 1""",
        task="Mockuj email service a ověř volání.",
        difficulty=2, points=25,
        hints=[
            "mock_email = Mock()",
            "system = NotifikacniSystem(mock_email)",
            "mock_email.posli.assert_called_once_with(uzivatel, zprava)"
        ],
        tests=[
            lambda: verify(test_notifikace_s_mockem() == True, "Mock email ✓"),
        ]
    ),
    Challenge(
        title="Mock Weather API",
        theory="""NÁVRATOVÁ HODNOTA mocku:
mock = Mock()
mock.get_teplota.return_value = 30  # vždy vrátí 30

app = WeatherApp(mock)
app.doporuceni("Praha")  # interně volá mock.get_teplota("Praha") → 30""",
        task="Mockuj API — testuj horko a zimu.",
        difficulty=2, points=25,
        hints=["mock_api = Mock(); mock_api.get_teplota.return_value = 30"],
        tests=[
            lambda: verify(test_weather_horko() == True, "Horké počasí ✓"),
            lambda: verify(test_weather_zima() == True, "Studené počasí ✓"),
        ]
    ),
    Challenge(
        title="Side Effects — různé odpovědi",
        theory="""SIDE EFFECT — mock vrací pokaždé jiný výsledek:

mock = Mock()
mock.side_effect = [10, 20, 30]
mock()  # → 10
mock()  # → 20
mock()  # → 30

# Nebo funkce:
mock.side_effect = lambda x: x * 2
mock(5)  # → 10""",
        task="Mock s side_effect — 3 různé návratové hodnoty.",
        difficulty=2, points=20,
        hints=["m = Mock(side_effect=[10, 20, 30]); m() → 10; m() → 20; m() → 30"],
        tests=[
            lambda: verify(test_mock_side_effects() == True, "Side effects ✓"),
        ]
    ),
]

if __name__ == "__main__":
    run_challenges(challenges, "Testing — Mocking", "05_03")
