"""
🎓 Pedagogical feedback — error classification and learning-oriented guidance.

Classifies runtime errors into categories and generates feedback that:
- Explains what happened (not just "failed")
- Guides toward the fix without giving it away
- Addresses common misconceptions
- Adapts to challenge type
"""
from enum import Enum
from typing import Optional, List, Tuple
import re

from engine.models import ChallengeType


class ErrorCategory(Enum):
    """Classification of errors for pedagogical feedback."""
    SYNTAX = "syntax"
    NAME = "name"               # NameError — undefined variable/function
    TYPE = "type"               # TypeError — wrong type in operation
    VALUE = "value"             # ValueError — right type, wrong value
    ATTRIBUTE = "attribute"     # AttributeError — missing method/property
    INDEX = "index"             # IndexError/KeyError — wrong access
    ASSERTION = "assertion"     # AssertionError or test comparison failure
    LOGIC = "logic"             # Correct types, wrong result
    IMPORT = "import"           # ImportError
    RUNTIME = "runtime"         # Other runtime errors
    UNKNOWN = "unknown"


# Czech-language explanations per category
CATEGORY_EXPLANATIONS = {
    ErrorCategory.SYNTAX: (
        "Syntaktická chyba",
        "Python nedokáže přečíst tvůj kód — je tam chyba ve struktuře.",
        [
            "Zkontroluj párové závorky (), [], {}",
            "Ověř odsazení (indentaci) — Python je na to citlivý",
            "Zkontroluj dvojtečky na konci if/for/def/class",
            "Hledej chybějící nebo přebytečné uvozovky",
        ],
    ),
    ErrorCategory.NAME: (
        "Neznámé jméno",
        "Python narazil na proměnnou nebo funkci, kterou nezná.",
        [
            "Zkontroluj překlepy v názvech proměnných",
            "Ověř, že proměnná existuje PŘED místem, kde ji používáš",
            "Zkontroluj, jestli jsi ji nedefinoval v jiném scope (bloku)",
            "U importů — importoval jsi správný modul?",
        ],
    ),
    ErrorCategory.TYPE: (
        "Špatný datový typ",
        "Operace nebo funkce dostala datový typ, který neumí zpracovat.",
        [
            "Zkontroluj, co přesně funkce očekává — int, str, list?",
            "Pozor na None — může se vrátit místo očekávané hodnoty",
            "Zkus si vypsat type(proměnná) pro ladění",
            "Při spojování stringů: nemůžeš sčítat str + int",
        ],
    ),
    ErrorCategory.VALUE: (
        "Špatná hodnota",
        "Správný typ, ale neplatná hodnota pro danou operaci.",
        [
            "Ověř rozsah vstupních hodnot",
            "Pozor na prázdné stringy, nuly, nebo neočekávané formáty",
            "Zkontroluj, jestli převádíš správný formát (např. int('3.14') nefunguje)",
        ],
    ),
    ErrorCategory.ATTRIBUTE: (
        "Neexistující atribut/metoda",
        "Objekt nemá metodu nebo vlastnost, kterou se snažíš použít.",
        [
            "Zkontroluj typ objektu — je to opravdu to, co si myslíš?",
            "Ověř název metody — překlep?",
            "Možná pracuješ s None místo skutečného objektu",
            "U stringu: .split(), u listu: .append() — nepleteš si je?",
        ],
    ),
    ErrorCategory.INDEX: (
        "Chybný přístup k prvku",
        "Snažíš se přistoupit k prvku, který neexistuje.",
        [
            "Indexy v Pythonu začínají od 0, ne od 1",
            "Ověř délku seznamu/slovníku PŘED přístupem",
            "U slovníků: existuje klíč? Zkus .get() pro bezpečný přístup",
            "Prázdný seznam nemá žádné prvky — ověř, jestli se naplnil",
        ],
    ),
    ErrorCategory.ASSERTION: (
        "Test neprošel",
        "Výsledek je jiný, než test očekává.",
        [
            "Porovnej svůj výstup s očekávaným — i drobné rozdíly (mezery, typy) se počítají",
            "Zkontroluj návratovou hodnotu funkce — vrací přesně to, co má?",
            "Pozor na return vs print — test kontroluje RETURN, ne výpis",
            "Zkus si výsledek vypisovat a porovnat ručně",
        ],
    ),
    ErrorCategory.LOGIC: (
        "Logická chyba",
        "Kód běží bez chyb, ale výsledek nesedí.",
        [
            "Projdi si algoritmus krok po kroku na papíře",
            "Zkontroluj okrajové případy (prázdný vstup, 0, 1 prvek)",
            "Ověř správnost podmínek (< vs <=, and vs or)",
            "Zkus si přidat debug výpisy ke klíčovým proměnným",
        ],
    ),
    ErrorCategory.IMPORT: (
        "Chyba importu",
        "Modul nebo balíček se nepodařilo najít.",
        [
            "Je modul nainstalovaný? Zkus: pip install název_modulu",
            "Zkontroluj název — je přesně správně?",
            "Pokud importuješ vlastní soubor, ověř cestu a strukturu",
        ],
    ),
    ErrorCategory.RUNTIME: (
        "Běhová chyba",
        "Kód se rozběhl, ale narazil na problém za běhu.",
        [
            "Přečti si celou chybovou hlášku — typ chyby je v prvním řádku",
            "Traceback ukazuje řádek, kde to spadlo — začni tam",
            "Zkontroluj vstupní data — jsou taková, jaká očekáváš?",
        ],
    ),
    ErrorCategory.UNKNOWN: (
        "Neznámá chyba",
        "Něco se pokazilo, ale automatická klasifikace nepomohla.",
        [
            "Přečti si celou chybovou hlášku pozorně",
            "Zkopíruj klíčovou část chyby a vyhledej ji online",
            "Zkus kód zjednodušit — odstraň části a testuj postupně",
        ],
    ),
}

# Patterns for error classification
_ERROR_PATTERNS = [
    (r"SyntaxError|IndentationError|TabError", ErrorCategory.SYNTAX),
    (r"NameError", ErrorCategory.NAME),
    (r"TypeError", ErrorCategory.TYPE),
    (r"ValueError", ErrorCategory.VALUE),
    (r"AttributeError", ErrorCategory.ATTRIBUTE),
    (r"IndexError|KeyError", ErrorCategory.INDEX),
    (r"AssertionError|AssertError", ErrorCategory.ASSERTION),
    (r"ImportError|ModuleNotFoundError", ErrorCategory.IMPORT),
    (r"ZeroDivisionError|RecursionError|OverflowError|MemoryError|"
     r"RuntimeError|StopIteration|FileNotFoundError|PermissionError|"
     r"OSError|IOError|TimeoutError", ErrorCategory.RUNTIME),
]

# Patterns that suggest logic errors (test passed type checks but wrong result)
_LOGIC_PATTERNS = [
    r"očekáváno\s+.+,\s+dostal",
    r"expected\s+.+,\s+got",
    r"Expected\s+.+\s+but\s+got",
    r"!=",
    r"does not equal",
    r"is not equal",
]


def classify_error(error_msg: str) -> ErrorCategory:
    """Classify an error message into a pedagogical category."""
    if not error_msg:
        return ErrorCategory.UNKNOWN

    # Check explicit error type patterns first
    for pattern, category in _ERROR_PATTERNS:
        if re.search(pattern, error_msg, re.IGNORECASE):
            return category

    # Check for logic error patterns (test comparison failures)
    for pattern in _LOGIC_PATTERNS:
        if re.search(pattern, error_msg, re.IGNORECASE):
            return ErrorCategory.LOGIC

    # Check for assertion-like test failures (common in our test framework)
    if any(kw in error_msg.lower() for kw in ("špatně", "failed", "neprošel", "chyba")):
        return ErrorCategory.ASSERTION

    return ErrorCategory.UNKNOWN


def generate_feedback(
    error_msg: str,
    challenge_type: ChallengeType = ChallengeType.IMPLEMENTATION,
    hints: Optional[List[str]] = None,
    attempt_count: int = 0,
    *,
    learning_objective: str = "",
    expected_misconceptions: Optional[List[str]] = None,
    hint_strategy: str = "progressive",
    challenge_state: Optional[str] = None,
    solution_pattern: str = "",
) -> dict:
    """Generate structured pedagogical feedback for a failed challenge.

    Context-aware: uses challenge metadata (learning objective, misconceptions,
    hint strategy, state) to produce feedback that's specific to THIS challenge,
    not just the error category.

    Returns dict with keys:
        category: ErrorCategory
        title: str - short Czech title
        explanation: str - what happened
        guidance: List[str] - actionable tips
        hint: Optional[str] - hint based on strategy + attempt count
        encouragement: str - motivational note based on context
        misconception_match: Optional[str] - matched misconception if any
        learning_frame: str - learning objective framing
    """
    category = classify_error(error_msg)
    title, explanation, guidance = CATEGORY_EXPLANATIONS[category]
    guidance = list(guidance)  # copy

    # ── Misconception matching ──
    misconception_match = _match_misconception(
        error_msg, category, expected_misconceptions or [])
    if misconception_match:
        # Insert misconception-specific guidance at the top
        guidance.insert(0, f"⚡ {misconception_match}")

    # ── Challenge-type-specific guidance ──
    type_tips = _get_type_specific_tips(category, challenge_type)
    if type_tips:
        guidance.extend(type_tips)

    # ── Solution pattern hint ──
    if solution_pattern and category in (ErrorCategory.ASSERTION, ErrorCategory.LOGIC):
        guidance.append(f"Očekávaný formát výstupu: {solution_pattern}")

    # ── Hint selection based on strategy ──
    hint = _select_hint(hints, attempt_count, hint_strategy, category)

    # ── Context-aware encouragement ──
    encouragement = _build_encouragement(
        attempt_count, challenge_state, category)

    # ── Learning objective framing ──
    learning_frame = ""
    if learning_objective:
        learning_frame = f"Cíl výzvy: {learning_objective}"
        if category in (ErrorCategory.LOGIC, ErrorCategory.ASSERTION):
            learning_frame += " — zaměř se na to, jestli tvůj kód splňuje tento cíl."

    return {
        "category": category,
        "title": title,
        "explanation": explanation,
        "guidance": guidance[:5],  # max 5 tips
        "hint": hint,
        "encouragement": encouragement,
        "misconception_match": misconception_match,
        "learning_frame": learning_frame,
    }


def _match_misconception(
    error_msg: str,
    category: ErrorCategory,
    misconceptions: List[str],
) -> Optional[str]:
    """Try to match the error against known misconceptions for this challenge."""
    if not misconceptions:
        return None

    error_lower = error_msg.lower()

    # Each misconception is a short description; try keyword matching
    for misconception in misconceptions:
        mc_lower = misconception.lower()
        # Extract key terms from the misconception
        keywords = [w for w in re.findall(r'\w{3,}', mc_lower)
                    if w not in ('pro', 'při', 'ale', 'jako', 'nebo',
                                 'místo', 'které', 'který', 'která',
                                 'the', 'and', 'for', 'with')]
        if keywords and any(kw in error_lower for kw in keywords):
            return misconception

    # Category-based matching — if misconception mentions the error type
    category_keywords = {
        ErrorCategory.TYPE: ["typ", "type", "int", "str", "float", "none"],
        ErrorCategory.NAME: ["jméno", "proměnná", "undefined", "name"],
        ErrorCategory.INDEX: ["index", "klíč", "key", "prvek"],
        ErrorCategory.VALUE: ["hodnota", "value", "formát", "range"],
    }
    cat_kws = category_keywords.get(category, [])
    for misconception in misconceptions:
        mc_lower = misconception.lower()
        if any(kw in mc_lower for kw in cat_kws):
            return misconception

    return None


def _select_hint(
    hints: Optional[List[str]],
    attempt_count: int,
    hint_strategy: str,
    category: ErrorCategory,
) -> Optional[str]:
    """Select the right hint based on hint strategy."""
    if not hints:
        return None

    if hint_strategy == "conceptual":
        # Always show first hint (conceptual explanation) until it's read
        return hints[0]

    elif hint_strategy == "contextual":
        # Pick hint based on error category, not attempt sequence
        if category in (ErrorCategory.SYNTAX, ErrorCategory.NAME):
            return hints[0] if hints else None
        elif category in (ErrorCategory.LOGIC, ErrorCategory.ASSERTION):
            return hints[-1] if hints else None
        else:
            idx = min(attempt_count // 2, len(hints) - 1)
            return hints[idx] if idx >= 0 else None

    else:
        # progressive (default): reveal hints one per attempt
        hint_idx = min(attempt_count, len(hints) - 1)
        return hints[hint_idx] if hint_idx >= 0 else None


def _build_encouragement(
    attempt_count: int,
    challenge_state: Optional[str],
    category: ErrorCategory,
) -> str:
    """Build context-aware encouragement message."""
    # Regression-specific
    if challenge_state == "regressed":
        if attempt_count <= 1:
            return "Dříve to fungovalo — zkontroluj, co se změnilo od posledně."
        return "Regrese se stává. Projdi svůj kód a porovnej s předchozí verzí."

    # Syntax errors — quick fix expected
    if category == ErrorCategory.SYNTAX:
        return "Syntaktická chyba se dá většinou opravit rychle — podívej se na vyznačený řádek."

    # Import errors
    if category == ErrorCategory.IMPORT:
        return "Importy jsou časté z počátku — ověř, že máš správné prostředí."

    # Standard progression
    if attempt_count <= 1:
        return "První pokus málokdy sedí — to je normální."
    elif attempt_count <= 3:
        return "Chyby jsou součást učení. Zkus to znovu."
    elif attempt_count <= 5:
        return "Nevzdávej to — podívej se na hinty a guidance výše."
    else:
        return "Zkus problém rozložit na menší části a testovat postupně."


def _get_type_specific_tips(
    category: ErrorCategory,
    challenge_type: ChallengeType,
) -> List[str]:
    """Additional tips specific to the challenge type."""
    tips = []

    if challenge_type == ChallengeType.DEBUGGING:
        if category == ErrorCategory.SYNTAX:
            tips.append("U debugging výzvy: chyba už je v kódu — najdi ji a oprav")
        elif category in (ErrorCategory.LOGIC, ErrorCategory.ASSERTION):
            tips.append("Porovnej aktuální chování s očekávaným — co přesně je jinak?")

    elif challenge_type == ChallengeType.KNOWLEDGE:
        if category == ErrorCategory.ASSERTION:
            tips.append("Vrať přesně požadovanou datovou strukturu ve správném formátu")

    elif challenge_type == ChallengeType.REFACTORING:
        if category == ErrorCategory.ASSERTION:
            tips.append("Refactoring nesmí změnit chování — testy ověřují původní výstup")

    return tips


def format_feedback_panel(feedback: dict, error_msg: str) -> str:
    """Format feedback dict into Rich markup for display in a Panel.

    Returns Rich-formatted string ready for Panel content.
    """
    lines = []
    lines.append(f"[bold red]❌ {feedback['title']}[/]")
    lines.append("")

    # Learning objective frame (if available)
    if feedback.get("learning_frame"):
        lines.append(f"[dim cyan]{feedback['learning_frame']}[/]")
        lines.append("")

    # Show the actual error (truncated)
    err_display = error_msg.strip()
    if len(err_display) > 200:
        err_display = err_display[:197] + "..."
    lines.append(f"[red]{err_display}[/]")
    lines.append("")

    # Misconception match (if found)
    if feedback.get("misconception_match"):
        lines.append(
            f"[yellow bold]⚡ Častá chyba: {feedback['misconception_match']}[/]")
        lines.append("")

    # Explanation
    lines.append(f"[yellow]{feedback['explanation']}[/]")
    lines.append("")

    # Guidance (numbered)
    lines.append("[cyan]Co zkusit:[/]")
    for i, tip in enumerate(feedback["guidance"], 1):
        lines.append(f"  [cyan]{i}.[/] {tip}")

    # Hint
    if feedback.get("hint"):
        lines.append("")
        lines.append(f"[yellow]💡 Nápověda: {feedback['hint']}[/]")

    # Encouragement
    lines.append("")
    lines.append(f"[dim]{feedback['encouragement']}[/]")

    return "\n".join(lines)
