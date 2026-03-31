"""
🏃 Challenge runner views — run single and run-all screens.

Split from views.py. Handles challenge execution, pedagogical feedback
rendering, and result display with context-aware guidance.
"""
import os
from typing import Optional, List

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from rich import box

from engine.models import (
    SectionInfo, LessonInfo, ChallengeDetail, ChallengeState,
)
from engine.content import load_challenge_details, run_single_challenge
from engine.feedback import classify_error, generate_feedback, format_feedback_panel
from engine.presenters import (
    state_label, type_label, progress_bar, format_lesson_rank,
)
from engine.editor import find_challenge_line


def _safe_input(console: Console, prompt: str = "[bold]  → [/]") -> str:
    try:
        return console.input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return "q"


def run_single_view(
    console: Console, progress, section: SectionInfo, lesson: LessonInfo,
    detail: ChallengeDetail,
    all_details: list = None,
):
    """Run a single challenge with context-aware pedagogical feedback."""
    console.print()
    console.print(f"  [dim]⏳ Spouštím výzvu {detail.index}...[/]")

    state_before = progress.get_challenge(detail.challenge_id).state

    # Reload for fresh code
    fresh_details = load_challenge_details(
        lesson.section_num, lesson.lesson_num, lesson.challenge_file
    )
    if detail.index <= len(fresh_details):
        detail = fresh_details[detail.index - 1]

    passed, messages, error = run_single_challenge(detail)
    points = detail.points if passed else 0

    progress.save_challenge(
        detail.challenge_id, passed, points, detail.points, error=error,
    )

    cp = progress.get_challenge(detail.challenge_id)
    state_after = cp.state

    progress.record_session_attempt(
        detail.challenge_id, passed, points, state_before, state_after,
    )

    console.print()
    if passed:
        msg = messages[0] if messages else "Správně!"
        panel_content = f"[bold green]✅ {msg}[/]\n[yellow]+{points}b[/]"

        if state_after == ChallengeState.MASTERED and state_before != ChallengeState.MASTERED:
            panel_content += "\n\n[bold yellow]💎 Mastery dosaženo! Skvělá práce![/]"
        elif state_after == ChallengeState.CURRENTLY_PASSING:
            consec = sum(1 for a in reversed(cp.attempts) if a.passed)
            remaining = 3 - consec
            if remaining > 0:
                panel_content += f"\n\n[dim]💎 Ještě {remaining}× pro mastery[/]"

        console.print(Panel(panel_content, style="green", box=box.ROUNDED))

        # Suggest next
        if all_details and detail.index < len(all_details):
            next_d = all_details[detail.index]
            next_state = progress.get_challenge(next_d.challenge_id).state
            if next_state != ChallengeState.MASTERED:
                console.print(
                    f"\n  [dim]→ Další: Výzva {next_d.index} — {next_d.title}[/]"
                )
    else:
        # Context-aware pedagogical feedback
        feedback = generate_feedback(
            error or "Test neprošel",
            challenge_type=detail.challenge_type,
            hints=detail.hints,
            attempt_count=cp.attempt_count,
            learning_objective=detail.learning_objective,
            expected_misconceptions=detail.expected_misconceptions,
            hint_strategy=detail.hint_strategy,
            challenge_state=state_after.value if state_after else None,
            solution_pattern=detail.solution_pattern,
        )
        panel_content = format_feedback_panel(feedback, error or "Test neprošel")

        # Regression-specific note
        if state_after == ChallengeState.REGRESSED:
            panel_content += (
                "\n\n[red dim]Dříve to procházelo — zkontroluj, "
                "jestli jsi nezměnil něco v kódu.[/]"
            )

        console.print(Panel(panel_content, style="red", box=box.ROUNDED))

        # File path for quick edit
        rel_path = os.path.relpath(lesson.challenge_file)
        line = find_challenge_line(lesson.challenge_file, detail.index)
        loc = f"{rel_path}:{line}" if line else rel_path
        console.print(f"\n  [dim]📝 Edituj: {loc}[/]")

    console.print()
    _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")


def run_all_view(
    console: Console, progress, section: SectionInfo, lesson: LessonInfo,
    details: List[ChallengeDetail],
):
    """Run all challenges in a lesson with summary and lesson completion feedback."""
    console.clear()
    console.print()
    console.print(Panel(
        f"[bold]{section.emoji} {section.name} → {lesson.name}[/]",
        style="magenta", box=box.DOUBLE,
    ))
    console.print()

    fresh_details = load_challenge_details(
        lesson.section_num, lesson.lesson_num, lesson.challenge_file
    )
    if not fresh_details:
        fresh_details = details

    results_table = Table(
        box=box.SIMPLE, show_header=True, header_style="bold",
        padding=(0, 1), show_edge=False,
    )
    results_table.add_column("", width=3)
    results_table.add_column("#", width=3, justify="right")
    results_table.add_column("Výzva", min_width=30)
    results_table.add_column("Typ", width=10, justify="center")
    results_table.add_column("Body", justify="right", width=8)
    results_table.add_column("Stav", width=16, justify="center")
    results_table.add_column("Detail", max_width=50)

    total_earned = 0
    total_max = 0
    completed_count = 0
    new_masteries = 0

    for d in fresh_details:
        state_before = progress.get_challenge(d.challenge_id).state

        passed, messages, error = run_single_challenge(d)
        points = d.points if passed else 0

        progress.save_challenge(
            d.challenge_id, passed, points, d.points, error=error,
        )
        total_max += d.points

        cp = progress.get_challenge(d.challenge_id)
        state_after = cp.state

        progress.record_session_attempt(
            d.challenge_id, passed, points, state_before, state_after,
        )
        if state_after == ChallengeState.MASTERED and state_before != ChallengeState.MASTERED:
            new_masteries += 1

        if passed:
            total_earned += points
            completed_count += 1
            status = "[green]✅[/]"
            pts_text = f"[green]+{points}b[/]"
            msg = messages[0] if messages else "OK"
            if len(msg) > 50:
                msg = msg[:47] + "..."
            detail_msg = f"[green]{msg}[/]"
        else:
            status = "[red]❌[/]"
            pts_text = f"[dim]{d.points}b[/]"
            cat = classify_error(error or "")
            from engine.feedback import CATEGORY_EXPLANATIONS
            cat_title = CATEGORY_EXPLANATIONS[cat][0]
            detail_msg = f"[red]{cat_title}[/]"

        tl = type_label(d.challenge_type)
        sl = state_label(cp.state)
        results_table.add_row(
            status, str(d.index), d.title, tl, pts_text, sl, detail_msg,
        )

        if not passed and d.hints:
            hint = d.hints[0]
            if len(hint) > 60:
                hint = hint[:57] + "..."
            results_table.add_row(
                "", "", "", "", "", "", f"[yellow]💡 {hint}[/]",
            )

    console.print(results_table)
    console.print()
    console.print(Rule(style="dim"))

    # Summary
    pct = completed_count / len(fresh_details) if fresh_details else 0
    rank = format_lesson_rank(pct)

    console.print(
        f"\n  {rank}   "
        f"{completed_count}/{len(fresh_details)} splněno   "
        f"[yellow]{total_earned}/{total_max}b[/]"
    )
    console.print(f"\n  {progress_bar(pct, 30)}")

    if new_masteries > 0:
        console.print(
            f"\n  [bold yellow]💎 Nové mastery: {new_masteries}[/]"
        )

    if pct >= 1.0:
        console.print("\n  [bold yellow]🎉 Všechny výzvy splněny![/]")
        # Lesson completion message with learning summary
        if lesson.meta.summary:
            console.print(
                f"\n  [dim cyan]📚 {lesson.meta.summary}[/]")
        if lesson.meta.learning_objectives:
            console.print("\n  [dim cyan]Zvládnuté cíle:[/]")
            for obj in lesson.meta.learning_objectives:
                console.print(f"  [dim cyan]  ✓ {obj}[/]")
    elif pct > 0:
        failed = [d for d in fresh_details
                  if progress.get_challenge(d.challenge_id).state
                  not in (ChallengeState.CURRENTLY_PASSING, ChallengeState.MASTERED)]
        if failed:
            console.print(
                f"\n  [dim]📌 Zaměř se na: "
                f"{'  '.join(f'Výzva {d.index}' for d in failed[:3])}[/]"
            )

    rel_path = os.path.relpath(lesson.challenge_file)
    if pct < 1.0:
        console.print(f"\n  [dim]📝 Edituj: [bold]{rel_path}[/bold][/]")

    # Legacy compat
    section_id = f"{section.num}_{lesson.lesson_num}"
    progress.save_section(
        section_id, completed_count, len(fresh_details), total_earned,
    )

    console.print()
    _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")
