"""
💪 Practice & review views — dedicated study mode screens.

Split from views.py for clarity. Handles:
- Categorized practice (regressions, review, continue, new)
- Review sessions
- Weak area analysis
- Concept-focused practice
- In-progress overview
"""
from typing import Optional, Dict, List

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from rich import box

from engine.models import (
    SectionInfo, ChallengeState,
)
from engine.recommend import (
    get_review_queue, get_weak_areas, get_smart_recommendations,
    categorize_recommendations, get_concept_recommendations,
    get_available_tags, Recommendation,
)
from engine.presenters import (
    state_icon, category_label,
)


def _safe_input(console: Console, prompt: str = "[bold]  → [/]") -> str:
    try:
        return console.input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return "q"


def _render_rec_table(console: Console, recs: List[Recommendation],
                      progress, title: str, max_items: int = 10
                      ) -> Optional[Dict]:
    """Shared helper: render a recommendation table and handle selection."""
    if not recs:
        return None

    display_recs = recs[:max_items]
    table = Table(
        box=box.SIMPLE, show_header=True,
        header_style="bold blue", padding=(0, 1),
    )
    table.add_column("#", width=4, justify="right", style="cyan")
    table.add_column("Stav", width=4, justify="center")
    table.add_column("Akce", width=20)
    table.add_column("Lekce", min_width=25)
    table.add_column("Výzva #", width=8, justify="center")
    table.add_column("Důvod", min_width=25)

    for i, rec in enumerate(display_recs, 1):
        cp = progress.get_challenge(rec.challenge_id)
        icon = state_icon(cp.state)
        table.add_row(
            str(i), icon,
            category_label(rec.category),
            f"{rec.section_name} → {rec.lesson_name}",
            str(rec.challenge_index),
            f"[dim]{rec.reason}[/]",
        )

    console.print(table)
    return display_recs


def practice_view(console: Console, progress, sections: List[SectionInfo]
                  ) -> Optional[Dict]:
    """Categorized practice — shows regressions, review, continue, new separately."""
    console.clear()
    console.print()
    console.print(Rule("[bold]💪 CÍLENÝ TRÉNINK[/]", style="blue"))
    console.print()

    cats = categorize_recommendations(progress, sections)

    total_items = sum(len(v) for v in cats.values())
    if total_items == 0:
        console.print(
            "  [green]✅ Nemáš žádné slabé místo — zkus nové učivo![/]")
        console.print()
        _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")
        return None

    # Show categorized summary
    all_recs = []
    idx_offset = 0

    if cats["regressions"]:
        console.print(
            f"  [red bold]🔻 REGRESE ({len(cats['regressions'])})[/]"
            f"  [dim]— Dříve fungovalo, teď ne. Oprav to nejdřív.[/]")
        console.print()
        display = _render_rec_table(
            console, cats["regressions"], progress,
            "Regrese", max_items=5)
        if display:
            all_recs.extend(display)
        console.print()

    if cats["review"]:
        console.print(
            f"  [yellow bold]🔄 K OPAKOVÁNÍ ({len(cats['review'])})[/]"
            f"  [dim]— Projde, ale delší dobu nezkoušené.[/]")
        console.print()
        display = _render_rec_table(
            console, cats["review"], progress,
            "K opakování", max_items=5)
        if display:
            all_recs.extend(display)
        console.print()

    if cats["continue"]:
        console.print(
            f"  [cyan bold]🔶 ROZPRACOVANÉ ({len(cats['continue'])})[/]"
            f"  [dim]— Začaté, ale ještě nedokončené.[/]")
        console.print()
        display = _render_rec_table(
            console, cats["continue"], progress,
            "Rozpracované", max_items=5)
        if display:
            all_recs.extend(display)
        console.print()

    if cats["new"]:
        console.print(
            f"  [green bold]🆕 NOVÉ UČIVO ({len(cats['new'])})[/]"
            f"  [dim]— Další lekce v pořadí.[/]")
        console.print()
        display = _render_rec_table(
            console, cats["new"], progress,
            "Nové učivo", max_items=3)
        if display:
            all_recs.extend(display)
        console.print()

    if not all_recs:
        _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")
        return None

    console.print(Rule(style="dim"))
    console.print()

    # Navigation
    tags = get_available_tags(sections)
    tag_hint = ""
    if tags:
        sample_tags = tags[:5]
        tag_hint = f"   [magenta]\\[k][/] Koncept ({', '.join(sample_tags[:3])}…)"

    console.print(
        f"  [cyan]\\[1-{len(all_recs)}][/] Spustit výzvu"
        f"{tag_hint}"
        f"   [cyan]\\[0][/] Zpět"
    )
    console.print()

    choice = _safe_input(console)
    if choice in ("0", "q", "b", ""):
        return None

    if choice == "k":
        return _concept_practice_view(console, progress, sections, tags)

    try:
        idx = int(choice)
        if 1 <= idx <= len(all_recs):
            rec = all_recs[idx - 1]
            return {
                "action": "challenge",
                "section": rec.section_num,
                "lesson": rec.lesson_num,
                "challenge": rec.challenge_index,
            }
    except (ValueError, TypeError):
        pass
    return None


def _concept_practice_view(
    console: Console, progress, sections: List[SectionInfo],
    tags: List[str],
) -> Optional[Dict]:
    """Concept-focused practice — filter by tag."""
    console.clear()
    console.print()
    console.print(Rule("[bold]🎯 KONCEPČNÍ TRÉNINK[/]", style="magenta"))
    console.print()
    console.print("  [dim]Vyber koncept, na který se chceš zaměřit:[/]")
    console.print()

    # Show available tags in columns
    for i, tag in enumerate(tags, 1):
        console.print(f"  [cyan]{i:>2}.[/] {tag}")

    console.print()
    console.print(
        f"  [cyan]\\[1-{len(tags)}][/] Vyber koncept   [cyan]\\[0][/] Zpět")
    console.print()

    choice = _safe_input(console)
    if choice in ("0", "q", "b", ""):
        return None

    try:
        idx = int(choice)
        if 1 <= idx <= len(tags):
            selected_tag = tags[idx - 1]
            return _show_concept_challenges(
                console, progress, sections, selected_tag)
    except (ValueError, TypeError):
        pass
    return None


def _show_concept_challenges(
    console: Console, progress, sections: List[SectionInfo],
    tag: str,
) -> Optional[Dict]:
    """Show challenges for a specific concept/tag."""
    console.clear()
    console.print()
    console.print(Rule(f"[bold]🎯 Koncept: {tag}[/]", style="magenta"))
    console.print()

    recs = get_concept_recommendations(progress, sections, tag, limit=15)
    if not recs:
        console.print(
            f"  [dim]Žádné výzvy pro koncept '{tag}' — "
            f"vše zvládnuto nebo zatím nedostupné.[/]")
        console.print()
        _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")
        return None

    display = _render_rec_table(console, recs, progress, tag, max_items=15)
    if not display:
        _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")
        return None

    console.print()
    console.print(
        f"  [cyan]\\[1-{len(display)}][/] Spustit výzvu   [cyan]\\[0][/] Zpět")
    console.print()

    choice = _safe_input(console)
    if choice in ("0", "q", "b", ""):
        return None

    try:
        idx = int(choice)
        if 1 <= idx <= len(display):
            rec = display[idx - 1]
            return {
                "action": "challenge",
                "section": rec.section_num,
                "lesson": rec.lesson_num,
                "challenge": rec.challenge_index,
            }
    except (ValueError, TypeError):
        pass
    return None


def review_view(console: Console, progress, sections: List[SectionInfo]
                ) -> Optional[Dict]:
    """Dedicated review session with better framing."""
    console.clear()
    console.print()
    console.print(Rule("[bold]🔄 OPAKOVÁNÍ[/]", style="yellow"))
    console.print()
    console.print(
        "  [dim]Výzvy, které jsi zvládl, ale je čas si je připomenout.[/]"
    )
    console.print(
        "  [dim]Pravidelné opakování je klíč k trvalému zapamatování.[/]"
    )
    console.print()

    review = get_review_queue(progress, sections)

    if not review:
        console.print(
            "  [green]✅ Žádné výzvy k opakování! Všechno je čerstvé.[/]"
        )
        console.print()
        _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")
        return None

    table = Table(
        box=box.SIMPLE, show_header=True,
        header_style="bold yellow", padding=(0, 1),
    )
    table.add_column("#", width=4, justify="right", style="cyan")
    table.add_column("Stav", width=4, justify="center")
    table.add_column("Lekce", min_width=25)
    table.add_column("Výzva #", width=8, justify="center")
    table.add_column("Důvod", min_width=25)

    display_items = review[:15]
    for i, rec in enumerate(display_items, 1):
        cp = progress.get_challenge(rec.challenge_id)
        icon = state_icon(cp.state)
        table.add_row(
            str(i), icon,
            f"{rec.section_name} → {rec.lesson_name}",
            str(rec.challenge_index),
            f"[dim]{rec.reason}[/]",
        )

    console.print(table)
    console.print()
    console.print(f"  [bold]{len(review)} výzev k opakování[/]")
    console.print()
    console.print(
        f"  [cyan]\\[1-{min(len(review), 15)}][/] Otevřít výzvu   "
        f"[cyan]\\[0][/] Zpět"
    )
    console.print()

    choice = _safe_input(console)
    if choice in ("0", "q", "b", ""):
        return None

    try:
        idx = int(choice)
        if 1 <= idx <= min(len(review), 15):
            rec = display_items[idx - 1]
            return {
                "action": "challenge",
                "section": rec.section_num,
                "lesson": rec.lesson_num,
                "challenge": rec.challenge_index,
            }
    except (ValueError, TypeError):
        pass
    return None


def weak_areas_view(console: Console, progress, sections: List[SectionInfo]
                    ) -> Optional[Dict]:
    """Show lessons with regressions and struggling challenges."""
    console.clear()
    console.print()
    console.print(Rule("[bold]⚠️  SLABÁ MÍSTA[/]", style="red"))
    console.print()
    console.print(
        "  [dim]Lekce, kde máš regresi nebo se dlouho trápíš s výzvami.[/]"
    )
    console.print()

    weak = get_weak_areas(progress, sections)

    if not weak:
        console.print(
            "  [green]✅ Žádná slabá místa! Pokračuj v dobré práci.[/]"
        )
        console.print()
        _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")
        return None

    table = Table(
        box=box.SIMPLE, show_header=True,
        header_style="bold red", padding=(0, 1),
    )
    table.add_column("#", width=4, justify="right", style="cyan")
    table.add_column("Lekce", min_width=30)
    table.add_column("🔻 Regrese", width=12, justify="center")
    table.add_column("😓 Trápí se", width=12, justify="center")
    table.add_column("Celkem", width=10, justify="center")

    for i, w in enumerate(weak, 1):
        table.add_row(
            str(i),
            f"{w['section_name']} → {w['lesson_name']}",
            f"[red]{w['regressed']}[/]" if w["regressed"] else "[dim]0[/]",
            f"[yellow]{w['struggling']}[/]" if w["struggling"] else "[dim]0[/]",
            str(w["total"]),
        )

    console.print(table)
    console.print()
    console.print(
        f"  [cyan]\\[1-{len(weak)}][/] Otevřít lekci   "
        f"[cyan]\\[0][/] Zpět"
    )
    console.print()

    choice = _safe_input(console)
    if choice in ("0", "q", "b", ""):
        return None

    try:
        idx = int(choice)
        if 1 <= idx <= len(weak):
            w = weak[idx - 1]
            return {
                "action": "lesson",
                "section": w["section_num"],
                "lesson": w["lesson_num"],
            }
    except (ValueError, TypeError):
        pass
    return None


def in_progress_view(console: Console, progress, sections: List[SectionInfo]
                     ) -> Optional[Dict]:
    """Show all in-progress and regressed challenges."""
    console.clear()
    console.print()
    console.print(Rule("[bold]🔶 ROZPRACOVANÉ VÝZVY[/]", style="yellow"))
    console.print()

    in_prog = progress.get_all_in_progress()

    if not in_prog:
        console.print("  [dim]Žádné rozpracované výzvy. Začni pracovat![/]")
        console.print()
        _safe_input(console, "  [dim]⏎ Enter pro návrat...[/]")
        return None

    by_lesson: Dict[str, list] = {}
    for cid, cp in in_prog:
        parts = cid.split('.')
        if len(parts) >= 2:
            lesson_key = f"{parts[0]}.{parts[1]}"
            by_lesson.setdefault(lesson_key, []).append((cid, cp))

    table = Table(
        box=box.SIMPLE, show_header=True,
        header_style="bold yellow", padding=(0, 1),
    )
    table.add_column("#", width=4, justify="right", style="cyan")
    table.add_column("Stav", width=4, justify="center")
    table.add_column("Lekce", min_width=25)
    table.add_column("Výzva", width=8, justify="center")
    table.add_column("Pokusů", width=8, justify="center")
    table.add_column("Naposledy", width=18)

    items = []
    for lesson_key, challenges in sorted(by_lesson.items()):
        parts = lesson_key.split('.')
        lesson_name = _resolve_lesson_name(sections, parts[0], parts[1])
        for cid, cp in challenges:
            ch_num = cid.split('.')[-1] if '.' in cid else "?"
            icon = state_icon(cp.state)
            ts = cp.last_attempt_at[:16] if cp.last_attempt_at else "—"
            items.append((cid, parts[0], parts[1], ch_num))
            table.add_row(
                str(len(items)), icon, lesson_name, ch_num,
                str(cp.attempt_count), f"[dim]{ts}[/]",
            )

    console.print(table)
    console.print()
    console.print(f"  [dim]Celkem {len(items)} výzev čeká na dokončení.[/]")
    console.print()
    console.print(
        f"  [cyan]\\[1-{len(items)}][/] Otevřít výzvu   "
        f"[cyan]\\[0][/] Zpět"
    )
    console.print()

    choice = _safe_input(console)
    if choice in ("0", "q", "b", ""):
        return None

    try:
        idx = int(choice)
        if 1 <= idx <= len(items):
            cid, sec_num, les_num, ch_num = items[idx - 1]
            return {
                "action": "challenge",
                "section": sec_num,
                "lesson": les_num,
                "challenge": int(ch_num),
            }
    except (ValueError, TypeError):
        pass
    return None


# ── Helpers ──

def _find_section(sections: List[SectionInfo], num: str):
    for s in sections:
        if s.num == num:
            return s
    return None


def _find_lesson(section, num: str):
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
