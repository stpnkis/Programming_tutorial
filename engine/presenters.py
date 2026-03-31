"""
🎨 Presenters — pure formatting functions for the TUI.

These functions take data and return Rich-formatted strings.
No Console dependency, no IO, no state — fully testable.
"""
from typing import Dict, List, Optional, Tuple

from engine.models import (
    ChallengeState, ChallengeType, STATE_DISPLAY, TYPE_DISPLAY,
)
from engine.recommend import ActionCategory


def progress_bar(pct: float, width: int = 20) -> str:
    """Rich-formatted progress bar."""
    filled = int(width * pct)
    bar = '█' * filled + '░' * (width - filled)
    color = "green" if pct >= 0.8 else ("yellow" if pct > 0 else "bright_black")
    return f"[{color}]{bar}[/] {pct:>4.0%}"


def state_icon(state: ChallengeState) -> str:
    """Emoji icon for a challenge state."""
    icon, style, _ = STATE_DISPLAY[state]
    return f"[{style}]{icon}[/]"


def state_label(state: ChallengeState) -> str:
    """Styled label for a challenge state."""
    _, style, label = STATE_DISPLAY[state]
    return f"[{style}]{label}[/]"


def type_label(ctype: ChallengeType) -> str:
    """Styled label for a challenge type."""
    label, style = TYPE_DISPLAY[ctype]
    return f"[{style}]{label}[/]"


def category_label(cat: ActionCategory) -> str:
    """Styled label for a recommendation category."""
    labels = {
        ActionCategory.FIX_REGRESSION: "[red]🔻 Oprav regresi[/]",
        ActionCategory.REVIEW_DUE: "[yellow]🔄 K opakování[/]",
        ActionCategory.CONTINUE_WORK: "[cyan]🔶 Pokračuj[/]",
        ActionCategory.NEW_MATERIAL: "[green]🆕 Nové učivo[/]",
        ActionCategory.PRACTICE: "[blue]💪 Procvičuj[/]",
        ActionCategory.CONCEPT_PRACTICE: "[magenta]🎯 Koncept[/]",
    }
    return labels.get(cat, str(cat.value))


def difficulty_stars(difficulty: int) -> str:
    """Star display for difficulty (1-3)."""
    return "⭐" * difficulty + "☆" * max(0, 3 - difficulty)


def format_stats_bar(summary: dict, snap) -> str:
    """Format the dashboard stats line."""
    return (
        f"🏆 [yellow]{summary['total_points']}[/] bodů   "
        f"✅ [green]{summary['total_challenges']}[/] výzev   "
        f"🔥 [red]{summary['streak']}[/] dní streak   "
        f"📅 {summary['days_active']} aktivních dní"
    )


def format_state_breakdown(snap) -> str:
    """Compact state breakdown for the dashboard."""
    parts = []
    if snap.mastered > 0:
        parts.append(f"💎 {snap.mastered} mastered")
    if snap.currently_passing > 0:
        parts.append(f"✅ {snap.currently_passing} projde")
    if snap.in_progress > 0:
        parts.append(f"🔶 {snap.in_progress} rozpracovaných")
    if snap.regressed > 0:
        parts.append(f"🔻 {snap.regressed} regresí")
    if snap.review_due_count > 0:
        parts.append(f"🔄 {snap.review_due_count} k opakování")
    return "   ".join(parts)


def format_mastery_indicator(state: ChallengeState, attempts: list) -> str:
    """Mastery progress indicator for challenge detail."""
    if state == ChallengeState.CURRENTLY_PASSING:
        consec = sum(1 for a in reversed(attempts) if a.passed)
        return f"[dim]💎 {consec}/3 k mastery[/]"
    elif state == ChallengeState.MASTERED:
        return "[bold green]💎 Zvládnuto![/]"
    return ""


def format_session_assessment(attempted: int, passed: int) -> str:
    """Session end assessment message."""
    if attempted == 0:
        return ""
    pct = passed / attempted
    if pct >= 0.8:
        return "[bold green]🌟 Výborné sezení![/]"
    elif pct >= 0.5:
        return "[bold cyan]👍 Dobrá práce![/]"
    else:
        return "[bold yellow]💪 Nevzdávej se — chyby jsou součást učení.[/]"


def format_lesson_rank(pct: float) -> str:
    """Rank label for lesson completion percentage."""
    if pct >= 1.0:
        return "[bold yellow]🏆 PERFEKTNÍ![/]"
    elif pct >= 0.7:
        return "[bold cyan]🥈 Skvělé![/]"
    elif pct >= 0.4:
        return "[bold green]🥉 Dobrý začátek[/]"
    return "[bold]🌱 Pokračuj[/]"
