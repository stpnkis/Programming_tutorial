"""
📱 Views — screen functions hub.

Re-exports views from sub-modules and keeps general UI screens
(onboarding, search, progress, roadmap, session summary, goodbye).

Navigation dict format:
    {"action": "challenge", "section": "01", "lesson": "01", "challenge": 1}
    {"action": "lesson", "section": "01", "lesson": "01"}
    None  # go back
"""
from typing import Optional, Dict, List, Tuple

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.align import Align
from rich import box

from engine.models import SectionInfo, LessonInfo, ChallengeState
from engine.content import search_lessons
from engine.recommend import build_snapshot
from engine.presenters import (
    progress_bar, state_icon, format_stats_bar,
    format_state_breakdown, format_session_assessment,
)

# ── Re-exports from split modules ──
from engine.views_practice import (  # noqa: F401
    practice_view, review_view, weak_areas_view, in_progress_view,
)
from engine.views_challenge import (  # noqa: F401
    run_single_view, run_all_view,
)


def _safe_input(console: Console, prompt: str = "[bold]  → [/]") -> str:
    try:
        return console.input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return "q"


# ── Onboarding ──

def onboarding_view(console: Console):
    """First-run welcome screen."""
    console.clear()
    console.print()
    console.print(Align.center(
        Text("⚡ PROGRAMÁTORSKÉ TRÉNINKOVÉ CENTRUM", style="bold cyan")
    ))
    console.print()
    console.print(Panel(
        "[bold]Vítej![/]\n\n"
        "Tohle je tvůj osobní systém pro učení programování.\n"
        "Každá lekce obsahuje sadu výzev — praktických úloh s testy.\n\n"
        "[cyan]Jak to funguje:[/]\n"
        "  1. Vyber si sekci a lekci\n"
        "  2. Otevři soubor [bold]challenges.py[/] a doplň řešení\n"
        "  3. Spusť test a podívej se na výsledek\n"
        "  4. Opakuj, dokud to neprojde 3× po sobě → [bold green]Mastery 💎[/]\n\n"
        "[yellow]Tvůj pokrok se automaticky ukládá.[/]\n"
        "Aplikace ti doporučí, co dělat dál, a upozorní na slabá místa.\n\n"
        "[dim]Začni sekcí 01 — Python Základy.[/]",
        title="[bold]Průvodce začátkem[/]",
        style="cyan", box=box.DOUBLE, padding=(1, 3),
    ))
    console.print()
    _safe_input(console, "  [dim]⏎ Enter pro pokračování...[/]")





# ── Search View ──

def search_view(console: Console, sections: List[SectionInfo], progress
                ) -> Optional[Dict]:
    """Search lessons by name, tag, or topic."""
    console.clear()
    console.print()
    console.print(Rule("[bold]🔍 HLEDAT LEKCE[/]", style="cyan"))
    console.print()
    console.print("  [dim]Hledej podle názvu, tagu nebo tématu.[/]")
    console.print()

    query = _safe_input(console, "  🔍 ")
    if not query or query in ("q", "0"):
        return None

    results = search_lessons(sections, query)

    console.print()
    if not results:
        console.print(f"  [dim]Nic nenalezeno pro '{query}'.[/]")
        console.print()
        _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")
        return None

    console.print(f"  [bold]{len(results)} výsledků:[/]")
    console.print()

    table = Table(
        box=box.SIMPLE, show_header=True,
        header_style="bold cyan", padding=(0, 1),
    )
    table.add_column("#", width=4, justify="right")
    table.add_column("", width=2)
    table.add_column("Lekce", min_width=30)
    table.add_column("Sekce", min_width=20)
    table.add_column("Progres", width=25)

    for i, lesson in enumerate(results, 1):
        completed = progress.get_lesson_completed(
            lesson.section_num, lesson.lesson_num)
        total = lesson.challenge_count
        pct = completed / total if total > 0 else 0
        if total > 0 and completed >= total:
            icon = "[green]✅[/]"
        elif completed > 0:
            icon = "[yellow]🔶[/]"
        else:
            icon = "[dim]⬜[/]"
        sec = _find_section(sections, lesson.section_num)
        sec_name = f"{sec.emoji} {sec.name}" if sec else ""
        table.add_row(
            str(i), icon, lesson.name, sec_name,
            progress_bar(pct) if total > 0 else "[dim]—[/]",
        )

    console.print(table)
    console.print()
    console.print(
        f"  [cyan]\\[1-{len(results)}][/] Otevřít   "
        f"[cyan]\\[0][/] Zpět"
    )
    console.print()

    choice = _safe_input(console)
    try:
        idx = int(choice)
        if 1 <= idx <= len(results):
            lesson = results[idx - 1]
            return {
                "action": "lesson",
                "section": lesson.section_num,
                "lesson": lesson.lesson_num,
            }
    except (ValueError, TypeError):
        pass

    console.print()
    _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")
    return None


# ── Progress Detail ──

def progress_view(console: Console, progress, sections: List[SectionInfo]):
    """Detailed progress overview."""
    console.clear()
    console.print()
    console.print(Rule("[bold]📊 TVŮJ PROGRESS[/]", style="cyan"))
    console.print()

    summary = progress.get_summary()
    snap = build_snapshot(progress, sections)

    # Stats table
    stats_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    stats_table.add_column("Stat", style="bold")
    stats_table.add_column("Value", style="yellow")
    stats_table.add_row("🏆 Celkové body", str(summary["total_points"]))
    stats_table.add_row("✅ Splněno výzev", str(summary["total_challenges"]))
    stats_table.add_row("📂 Zahájeno sekcí", str(summary["sections_started"]))
    stats_table.add_row("🔥 Streak", f"{summary['streak']} dní")
    stats_table.add_row("📅 Aktivních dní", str(summary["days_active"]))
    console.print(stats_table)

    # State breakdown
    console.print()
    console.print("  [bold]Stavy výzev:[/]")
    console.print(
        f"    💎 [bold green]Mastered: {snap.mastered}[/]"
        f"  [dim]— stabilně zvládnuté (3+ úspěchů v řadě)[/]"
    )
    console.print(
        f"    ✅ [green]Projde: {snap.currently_passing}[/]"
        f"  [dim]— naposledy úspěšné, ale ještě ne mastered[/]"
    )
    console.print(
        f"    🔶 [yellow]Rozpracované: {snap.in_progress}[/]"
        f"  [dim]— začaté, zatím neprošlo[/]"
    )
    console.print(
        f"    🔻 [red]Regrese: {snap.regressed}[/]"
        f"  [dim]— dříve procházelo, teď ne[/]"
    )
    if snap.review_due_count > 0:
        console.print(
            f"    🔄 [yellow]K opakování: {snap.review_due_count}[/]"
            f"  [dim]— projde, ale delší dobu nezkoušené[/]"
        )
    console.print(
        f"    ⬜ [dim]Nezahájené: {snap.not_started}[/]"
    )
    console.print()

    # Mastery lines
    if snap.total_challenges > 0:
        console.print(
            f"  [bold]Mastery:[/] {progress_bar(snap.mastery_pct, 30)}"
        )
        console.print(
            f"  [bold]Celkový progress:[/] {progress_bar(snap.progress_pct, 30)}"
        )
        console.print()

    # Per-section table
    section_table = Table(
        title="Detail po sekcích", box=box.ROUNDED,
        show_header=True, header_style="bold cyan",
    )
    section_table.add_column("Sekce", min_width=30)
    section_table.add_column("Progres", width=30)
    section_table.add_column("Hotovo", justify="center", width=12)
    section_table.add_column("Body", justify="right", width=8)

    for section in sections:
        completed, total = _get_section_stats(progress, section)
        pct = completed / total if total > 0 else 0
        v3_prefix = f"{section.num}."
        sec_points = sum(
            progress.get_challenge(k).best_points
            for k in progress.data.get("challenges", {})
            if k.startswith(v3_prefix)
        )
        if sec_points == 0:
            for k, v in progress.data.get("sections", {}).items():
                if k.startswith(section.num + "_"):
                    sec_points += v.get("best_points", 0)

        section_table.add_row(
            f"{section.emoji} {section.name}",
            progress_bar(pct) if total > 0 else "[dim]Nezahájeno[/]",
            f"{completed}/{total}" if total > 0 else "[dim]—[/]",
            f"[yellow]{sec_points}b[/]" if sec_points > 0 else "[dim]—[/]",
        )

    console.print(section_table)
    console.print()
    _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")


# ── Roadmap ──

def roadmap_view(console: Console):
    """Learning roadmap with phases."""
    console.clear()
    console.print()
    console.print(Rule("[bold]🗺️  MAPA UČENÍ[/]", style="cyan"))
    console.print()

    phases = [
        ("FÁZE 1: ZÁKLADY", "2-4 týdny", "green",
         "01 Python Základy → 02 OOP → 03 Datové struktury",
         "Bez tohohle se nedá stavět nic dalšího."),
        ("FÁZE 2: PROFESNÍ NÁVYKY", "1-2 týdny", "yellow",
         "04 Git → 05 Testing → 06 Čtení a debugování kódu",
         "To co odděluje amatéra od profíka."),
        ("FÁZE 3: DATA A ML", "2-4 týdny", "cyan",
         "07 NumPy & Matematika → 08 Machine Learning",
         "Od čísel k inteligentním modelům."),
        ("FÁZE 4: ROBOTIKA", "2-4 týdny", "magenta",
         "09 Computer Vision → 10 ROS2",
         "Tvůj hlavní obor — vidění a ovládání robotů."),
        ("FÁZE 5: INFRASTRUKTURA", "1-2 týdny", "blue",
         "11 Linux → 12 Networking → 13 Paralelismus",
         "To co drží vše pohromadě v reálném světě."),
        ("FÁZE 6: PROJEKTY 🏆", "", "yellow",
         "14 Reálné projekty do portfolia",
         "Spojení všeho do funkčních aplikací."),
    ]

    for i, (title, duration, color, content, note) in enumerate(phases):
        panel_title = title
        if duration:
            panel_title += f" ({duration})"
        console.print(Panel(
            f"[bold]{content}[/]\n[dim]{note}[/]",
            title=panel_title, style=color,
            box=box.ROUNDED, padding=(0, 2),
        ))
        if i < len(phases) - 1:
            console.print(Align.center("[dim]│[/]"))

    console.print()
    console.print(
        "  [bold]💡 Pravidlo:[/] Nepřecházej na další fázi, "
        "dokud neumíš aktuální napsat bez nápovědy."
    )
    console.print()
    _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")


# ── Session Summary ──

def session_summary_view(console: Console, progress):
    """Show what the user accomplished during this session."""
    stats = progress.get_session_stats()
    if not stats or stats["challenges_attempted"] == 0:
        progress.end_session()
        return

    console.clear()
    console.print()
    console.print(Rule("[bold]📋 SHRNUTÍ SEZENÍ[/]", style="cyan"))
    console.print()

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column("", style="bold")
    table.add_column("", style="yellow")

    table.add_row("⏱️  Doba studia", f"{stats['duration_minutes']} minut")
    table.add_row("🎯 Výzvy řešené", str(stats["challenges_attempted"]))
    table.add_row("✅ Úspěšné", str(stats["challenges_passed"]))
    table.add_row("🏆 Body získané", str(stats["points_earned"]))
    if stats["new_masteries"] > 0:
        table.add_row("💎 Nové mastery", str(stats["new_masteries"]))
    if stats["regressions"] > 0:
        table.add_row("🔻 Regrese", str(stats["regressions"]))
    table.add_row("📝 Unique výzvy", str(stats["unique_challenges"]))

    console.print(table)

    # Success rate bar
    attempted = stats["challenges_attempted"]
    passed = stats["challenges_passed"]
    if attempted > 0:
        rate = passed / attempted
        console.print(
            f"\n  [bold]Úspěšnost:[/] {progress_bar(rate, 20)}"
            f"  ({passed}/{attempted})"
        )

    # Session goal completion
    goal = progress.get_session_goal()
    done = min(goal["current"], goal["target_count"])
    if done >= goal["target_count"]:
        console.print(
            f"\n  [bold green]🎯 Cíl sezení splněn: {goal['label']} ✅[/]"
        )
    else:
        console.print(
            f"\n  [dim]🎯 Cíl sezení: {goal['label']} "
            f"({done}/{goal['target_count']})[/]"
        )

    # Next session recommendation — more specific
    console.print()
    if stats["regressions"] > 0:
        console.print(
            f"  [yellow]📌 Příště:[/] Oprav {stats['regressions']} regres"
            f"{'i' if stats['regressions'] == 1 else 'í'} — "
            f"stiskni [bold]t[/bold] (trénink) hned na začátku."
        )
    elif passed == 0 and attempted > 0:
        console.print(
            "  [cyan]📌 Příště:[/] Zkus menší kroky — otevři detail výzvy "
            "a přečti si hinty a teorii dřív, než začneš řešit."
        )
    elif stats.get("new_masteries", 0) > 0:
        console.print(
            f"  [green]📌 Příště:[/] Výborně ({stats['new_masteries']} "
            f"nových mastery)! Pokračuj novým učivem."
        )
    else:
        console.print(
            "  [cyan]📌 Příště:[/] Dokončuj rozpracované výzvy a "
            "opakuj starší — klíč k trvalému zapamatování."
        )

    # Assessment
    console.print()
    assessment = format_session_assessment(
        stats["challenges_attempted"], stats["challenges_passed"])
    if assessment:
        console.print(f"  {assessment}")

    console.print()
    progress.end_session()
    _safe_input(console, "  [dim]⏎ Enter...[/]")





# ── Goodbye ──

def goodbye_view(console: Console):
    """Exit screen."""
    console.clear()
    console.print()
    console.print(Align.center("[cyan]Hodně štěstí na tréninku! 💪[/]"))
    console.print()





# ── Helpers ──

def _find_section(sections: List[SectionInfo], num: str):
    for s in sections:
        if s.num == num:
            return s
    return None


def _find_lesson(section: SectionInfo, num: str):
    for l in section.lessons:
        if l.lesson_num == num:
            return l
    return None


def _resolve_lesson_name(sections: List[SectionInfo], sec_num: str,
                         les_num: str) -> str:
    section = _find_section(sections, sec_num)
    if section:
        lesson = _find_lesson(section, les_num)
        if lesson:
            return f"{section.emoji} {lesson.name}"
    return f"Sekce {sec_num} Lekce {les_num}"


def _get_section_stats(progress, section: SectionInfo) -> Tuple[int, int]:
    total_completed = 0
    total_challenges = 0
    for lesson in section.lessons:
        completed = progress.get_lesson_completed(
            lesson.section_num, lesson.lesson_num)
        total = lesson.challenge_count
        if completed == 0:
            # Legacy fallback
            section_id = f"{lesson.section_num}_{lesson.lesson_num}"
            legacy = progress.get_section(section_id)
            if legacy:
                completed = legacy.get("completed", 0)
        total_completed += completed
        total_challenges += total
    return total_completed, total_challenges
