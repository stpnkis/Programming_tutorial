"""
⚡ App controller — navigation + core screens.

v5: Decomposed architecture. This file is the CONTROLLER only.
Views, presenters, feedback, and actions live in their own modules.
"""
import os
from typing import Optional, List

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.align import Align
from rich import box

from engine.models import (
    SectionInfo, LessonInfo, ChallengeDetail, ChallengeState,
    ChallengeType, ChallengeProgress,
)
from engine.content import (
    discover_sections, load_challenge_details, search_lessons,
)
from engine.recommend import (
    build_snapshot, get_smart_recommendations,
    ActionCategory, LearningSnapshot,
)
from engine.editor import open_file, find_challenge_line, get_editor
from engine.progress import Progress
from engine.presenters import (
    progress_bar, state_icon, state_label, type_label,
    category_label, difficulty_stars,
    format_state_breakdown, format_stats_bar,
)
from engine.views import (
    onboarding_view, review_view, weak_areas_view,
    in_progress_view, search_view, progress_view,
    roadmap_view, session_summary_view, practice_view,
    goodbye_view, run_single_view, run_all_view,
    _safe_input as safe_input,
)


class App:
    """Main application controller — routes between screens."""

    def __init__(self):
        self.console = Console()
        self.progress = Progress()
        self.sections = discover_sections()
        self.progress.start_session()
        self._first_run = not self.progress.data.get("challenges")

    def run(self):
        """Main application loop."""
        try:
            if self._first_run:
                onboarding_view(self.console)

            while True:
                action = self._dashboard()
                if action == "quit":
                    session_summary_view(self.console, self.progress)
                    goodbye_view(self.console)
                    break
                elif action == "progress":
                    progress_view(self.console, self.progress, self.sections)
                elif action == "map":
                    roadmap_view(self.console)
                elif action == "continue":
                    self._resume()
                elif action == "in_progress":
                    nav = in_progress_view(
                        self.console, self.progress, self.sections)
                    self._handle_navigation(nav)
                elif action == "search":
                    nav = search_view(
                        self.console, self.sections, self.progress)
                    self._handle_navigation(nav)
                elif action == "review":
                    nav = review_view(
                        self.console, self.progress, self.sections)
                    self._handle_navigation(nav)
                elif action == "weak":
                    nav = weak_areas_view(
                        self.console, self.progress, self.sections)
                    self._handle_navigation(nav)
                elif action == "practice":
                    nav = practice_view(
                        self.console, self.progress, self.sections)
                    self._handle_navigation(nav)
                elif action.startswith("s:"):
                    num = action[2:]
                    section = self._find_section(num)
                    if section:
                        self._section_screen(section)
        except KeyboardInterrupt:
            session_summary_view(self.console, self.progress)
            goodbye_view(self.console)

    # ── Navigation ──

    def _handle_navigation(self, nav: Optional[dict]):
        """Handle navigation dict returned from views."""
        if not nav:
            return
        action = nav.get("action")
        if action == "challenge":
            section = self._find_section(nav["section"])
            if section:
                lesson = self._find_lesson(section, nav["lesson"])
                if lesson:
                    details = load_challenge_details(
                        lesson.section_num, lesson.lesson_num,
                        lesson.challenge_file,
                    )
                    ch_idx = nav.get("challenge", 1) - 1
                    if details and 0 <= ch_idx < len(details):
                        self._challenge_detail(section, lesson, details, ch_idx)
        elif action == "lesson":
            section = self._find_section(nav["section"])
            if section:
                lesson = self._find_lesson(section, nav["lesson"])
                if lesson:
                    self._lesson_detail(section, lesson)

    # ── Helpers ──

    def _find_section(self, num: str) -> Optional[SectionInfo]:
        for s in self.sections:
            if s.num == num:
                return s
        return None

    def _find_lesson(self, section: SectionInfo,
                     num: str) -> Optional[LessonInfo]:
        for l in section.lessons:
            if l.lesson_num == num:
                return l
        return None

    def _refresh(self):
        self.progress = Progress()

    def _safe_input(self, prompt: str = "[bold]  → [/]") -> str:
        return safe_input(self.console, prompt)

    def _get_lesson_stats(self, lesson: LessonInfo):
        total = lesson.challenge_count
        if total == 0:
            return 0, 0
        completed = self.progress.get_lesson_completed(
            lesson.section_num, lesson.lesson_num)
        if completed > 0:
            return completed, total
        section_id = f"{lesson.section_num}_{lesson.lesson_num}"
        legacy = self.progress.get_section(section_id)
        if legacy:
            return legacy.get("completed", 0), legacy.get("total", total)
        return 0, total

    def _get_section_stats(self, section: SectionInfo):
        total_completed = 0
        total_challenges = 0
        for lesson in section.lessons:
            c, t = self._get_lesson_stats(lesson)
            total_completed += c
            total_challenges += t
        return total_completed, total_challenges

    # ── Dashboard ──

    def _dashboard(self) -> str:
        self.console.clear()
        self._refresh()

        self.console.print()
        self.console.print(Align.center(
            Text("⚡ PROGRAMÁTORSKÉ TRÉNINKOVÉ CENTRUM", style="bold cyan")
        ))
        self.console.print(Align.center(
            Text("Buduj programátorskou intuici krok za krokem", style="dim")
        ))
        self.console.print()

        snap = build_snapshot(self.progress, self.sections)

        # Stats bar
        summary = self.progress.get_summary()
        if summary["total_points"] > 0 or summary["total_challenges"] > 0:
            self.console.print(Align.center(
                format_stats_bar(summary, snap)))

            breakdown = format_state_breakdown(snap)
            if breakdown:
                self.console.print(Align.center(f"[dim]{breakdown}[/]"))
            self.console.print()

        # Bookmark
        bookmark = self.progress.get_bookmark()
        has_bookmark = bookmark is not None
        if has_bookmark:
            sec_name = bookmark.get('section_name', '')
            les_name = bookmark.get('lesson_name', '')
            ch_idx = bookmark.get('challenge_index', 0)
            ch_info = f" — Výzva {ch_idx}" if ch_idx else ""
            self.console.print(Panel(
                f"[bold]▶ Pokračovat:[/] {sec_name} → {les_name}{ch_info}"
                f"  [dim](stiskni [bold]c[/bold])[/]",
                style="green", box=box.ROUNDED, padding=(0, 2),
            ))
            self.console.print()

        # Smart recommendation
        if snap.next_action:
            rec = snap.next_action
            cat = category_label(rec.category)
            self.console.print(
                f"  💡 {cat}: "
                f"[cyan]{rec.section_num}.{rec.lesson_num}[/] "
                f"{rec.lesson_name}"
                f"  [dim]{rec.reason}[/]"
            )
            self.console.print()

        # Session goal
        goal = self.progress.get_session_goal()
        done = min(goal["current"], goal["target_count"])
        goal_pbar = progress_bar(
            done / goal["target_count"] if goal["target_count"] > 0 else 0,
            width=10,
        )
        goal_status = "[green]✅[/]" if done >= goal["target_count"] else "🎯"
        self.console.print(
            f"  {goal_status} [bold]Cíl sezení:[/] {goal['label']}   "
            f"{goal_pbar}  ({done}/{goal['target_count']})"
        )
        self.console.print()

        # Regression alert
        if snap.regressed > 0:
            self.console.print(
                f"  [red bold]⚠️  {snap.regressed} výzev má regresi — "
                f"dříve procházelo, teď ne. Stiskni [bold]w[/bold] pro detail.[/]"
            )
            self.console.print()

        # Section table
        table = Table(
            box=box.SIMPLE_HEAVY, show_header=True,
            header_style="bold cyan", padding=(0, 1),
        )
        table.add_column("#", style="cyan", width=4, justify="right")
        table.add_column("", width=2)
        table.add_column("Sekce", min_width=30)
        table.add_column("Progres", width=30)
        table.add_column("Hotovo", justify="right", width=10)

        for section in self.sections:
            completed, total = self._get_section_stats(section)
            pct = completed / total if total > 0 else 0
            if total > 0 and completed >= total:
                status_icon = "[green]✅[/]"
            elif completed > 0:
                status_icon = "[yellow]🔶[/]"
            else:
                status_icon = "[dim]⬜[/]"
            table.add_row(
                section.num, status_icon,
                f"{section.emoji} {section.name}",
                progress_bar(pct) if total > 0 else "[dim]—[/]",
                f"{completed}/{total}" if total > 0 else "[dim]—[/]",
            )

        self.console.print(table)
        self.console.print()

        # Menu
        menu_parts = []
        if has_bookmark:
            menu_parts.append("[cyan]\\[c][/] Pokračovat")
        menu_parts.append("[cyan]\\[01-14][/] Sekce")
        menu_parts.append("[cyan]\\[i][/] Rozpracované")
        if snap.review_due_count > 0:
            menu_parts.append(
                f"[yellow]\\[v][/] Opakování ({snap.review_due_count})")
        if snap.regressed > 0 or snap.weak_areas:
            menu_parts.append("[red]\\[w][/] Slabá místa")
        menu_parts.extend([
            "[blue]\\[t][/] Trénink",
            "[cyan]\\[s][/] Hledat",
            "[cyan]\\[p][/] Progress",
            "[cyan]\\[m][/] Mapa",
            "[cyan]\\[q][/] Konec",
        ])
        self.console.print("  " + "   ".join(menu_parts))
        self.console.print()

        choice = self._safe_input()

        if choice in ("q", "quit", "exit"):
            return "quit"
        elif choice == "p":
            return "progress"
        elif choice == "m":
            return "map"
        elif choice == "c" and has_bookmark:
            return "continue"
        elif choice == "i":
            return "in_progress"
        elif choice == "s":
            return "search"
        elif choice == "v":
            return "review"
        elif choice == "w":
            return "weak"
        elif choice == "t":
            return "practice"
        else:
            for section in self.sections:
                if choice == section.num or choice == section.num.lstrip("0"):
                    return f"s:{section.num}"
            return "invalid"

    # ── Section Screen ──

    def _section_screen(self, section: SectionInfo):
        while True:
            self.console.clear()
            self._refresh()

            self.console.print()
            self.console.print(
                Rule(f"{section.emoji} {section.num}. {section.name}",
                     style="blue")
            )
            self.console.print()

            if not section.lessons:
                self.console.print(
                    "  [yellow]⚠️  Zatím žádné lekce.[/]")
                self._safe_input("\n  [dim]⏎ Enter pro návrat...[/]")
                return

            table = Table(
                box=box.SIMPLE, show_header=True,
                header_style="bold blue", padding=(0, 1),
            )
            table.add_column("#", style="cyan", width=4, justify="right")
            table.add_column("", width=2)
            table.add_column("Lekce", min_width=30)
            table.add_column("Obtížnost", width=10, justify="center")
            table.add_column("Progres", width=30)
            table.add_column("Hotovo", justify="right", width=10)

            for lesson in section.lessons:
                completed, total = self._get_lesson_stats(lesson)
                pct = completed / total if total > 0 else 0
                if total > 0 and completed >= total:
                    s_icon = "[green]✅[/]"
                elif completed > 0:
                    s_icon = "[yellow]🔶[/]"
                else:
                    s_icon = "[dim]⬜[/]"
                diff = lesson.meta.difficulty
                diff_str = "⭐" * diff if diff > 0 else "[dim]—[/]"
                table.add_row(
                    lesson.lesson_num, s_icon, lesson.name,
                    diff_str,
                    progress_bar(pct) if total > 0 else "[dim]—[/]",
                    f"{completed}/{total}" if total > 0 else "[dim]—[/]",
                )

            self.console.print(table)

            has_summaries = any(l.meta.summary for l in section.lessons)
            if has_summaries:
                self.console.print()
                for lesson in section.lessons:
                    if lesson.meta.summary:
                        self.console.print(
                            f"  [dim]{lesson.lesson_num}. "
                            f"{lesson.meta.summary}[/]"
                        )

            self.console.print()
            max_num = max(
                int(l.lesson_num) for l in section.lessons
            ) if section.lessons else 0
            self.console.print(
                f"  [cyan]\\[01-{max_num:02d}][/] Otevři lekci   "
                f"[cyan]\\[0][/] Zpět"
            )
            self.console.print()

            choice = self._safe_input()
            if choice in ("0", "", "q", "b"):
                return

            try:
                lesson_num = f"{int(choice):02d}"
                lesson = self._find_lesson(section, lesson_num)
                if lesson:
                    self._lesson_detail(section, lesson)
            except (ValueError, TypeError):
                pass

    # ── Lesson Detail ──

    def _lesson_detail(self, section: SectionInfo, lesson: LessonInfo):
        while True:
            self.console.clear()
            self._refresh()

            self.console.print()
            self.console.print(Panel(
                f"[bold]{section.emoji} {section.name} → {lesson.name}[/]",
                style="magenta", box=box.DOUBLE,
            ))

            details = load_challenge_details(
                lesson.section_num, lesson.lesson_num, lesson.challenge_file
            )

            if not details:
                self.console.print(
                    "  [yellow]⚠️  Žádné výzvy nebo chyba při načítání.[/]"
                )
                self.console.print(f"  [dim]{lesson.challenge_file}[/]")
                self._safe_input("\n  [dim]⏎ Enter pro návrat...[/]")
                return

            # Stats
            passing = mastered_count = regressed_count = 0
            total_pts = max_pts = 0
            for d in details:
                cp = self.progress.get_challenge(d.challenge_id)
                if cp.state in (ChallengeState.CURRENTLY_PASSING,
                                ChallengeState.MASTERED):
                    passing += 1
                if cp.state == ChallengeState.MASTERED:
                    mastered_count += 1
                if cp.state == ChallengeState.REGRESSED:
                    regressed_count += 1
                total_pts += cp.best_points
                max_pts += d.points

            pct = passing / len(details) if details else 0
            stats_line = (
                f"  {progress_bar(pct, 25)}   "
                f"[yellow]{total_pts}/{max_pts}b[/]"
            )
            if mastered_count > 0:
                stats_line += f"   💎 {mastered_count} mastered"
            if regressed_count > 0:
                stats_line += f"   [red]🔻 {regressed_count} regresí[/]"
            self.console.print(stats_line)

            if lesson.meta.summary:
                self.console.print(
                    f"  [dim]{lesson.meta.summary}[/]")
            if lesson.meta.learning_objectives:
                self.console.print(
                    f"  [dim]Cíle: "
                    f"{', '.join(lesson.meta.learning_objectives)}[/]"
                )
            self.console.print()

            # Challenge table
            table = Table(
                box=box.SIMPLE, show_header=True,
                header_style="bold magenta", padding=(0, 1),
            )
            table.add_column("#", width=3, justify="right", style="cyan")
            table.add_column("Stav", width=4, justify="center")
            table.add_column("Výzva", min_width=35)
            table.add_column("Typ", width=12, justify="center")
            table.add_column("Body", width=8, justify="right")
            table.add_column("Pokusy", width=8, justify="center")

            for d in details:
                cp = self.progress.get_challenge(d.challenge_id)
                state = cp.state
                icon = state_icon(state)
                tl = type_label(d.challenge_type)
                stars = difficulty_stars(d.difficulty)
                pts = f"[yellow]{d.points}b[/]"
                attempts_str = (str(cp.attempt_count)
                                if cp.attempt_count > 0 else "[dim]—[/]")
                title = d.title
                if state == ChallengeState.REGRESSED:
                    title += " [red]![/]"
                table.add_row(
                    str(d.index), icon, f"{title} {stars}", tl,
                    pts, attempts_str,
                )

            self.console.print(table)
            self.console.print()

            # File path
            rel_path = os.path.relpath(lesson.challenge_file)
            editor_name = get_editor()
            if editor_name:
                self.console.print(
                    f"  [dim]📝 [bold]{rel_path}[/bold]   "
                    f"\\[e] Otevřít v editoru[/]"
                )
            else:
                self.console.print(
                    f"  [dim]📝 Edituj: [bold]{rel_path}[/bold][/]")
            self.console.print()

            # Menu
            parts = [
                f"[cyan]\\[1-{len(details)}][/] Detail výzvy",
                "[cyan]\\[r][/] Run all",
            ]
            if editor_name:
                parts.append("[cyan]\\[e][/] Editor")
            parts.append("[cyan]\\[0][/] Zpět")
            self.console.print("  " + "   ".join(parts))
            self.console.print()

            self.progress.set_bookmark(
                section.num, lesson.lesson_num,
                section_name=section.name, lesson_name=lesson.name,
            )

            choice = self._safe_input()
            if choice in ("0", "q", "b", ""):
                return
            elif choice == "r":
                run_all_view(
                    self.console, self.progress, section, lesson, details)
            elif choice == "e" and editor_name:
                open_file(lesson.challenge_file)
            else:
                try:
                    idx = int(choice)
                    if 1 <= idx <= len(details):
                        self._challenge_detail(
                            section, lesson, details, idx - 1)
                except (ValueError, TypeError):
                    pass

    # ── Challenge Detail ──

    def _challenge_detail(self, section: SectionInfo, lesson: LessonInfo,
                          details: List[ChallengeDetail], detail_idx: int):
        while True:
            self.console.clear()
            self._refresh()

            d = details[detail_idx]
            cp = self.progress.get_challenge(d.challenge_id)
            state = cp.state

            # Header
            self.console.print()
            stars = difficulty_stars(d.difficulty)
            self.console.print(Panel(
                f"[bold]🏆 VÝZVA {d.index}/{len(details)}: {d.title}[/]\n"
                f"{stars}  |  [yellow]{d.points}b[/]  |  "
                f"Typ: {type_label(d.challenge_type)}",
                style="magenta", box=box.DOUBLE,
            ))

            # Status
            state_info = f"  📊 Stav: {state_label(state)}"
            state_info += f"   |   Pokusů: {cp.attempt_count}"
            if cp.last_attempt_at:
                state_info += (
                    f"   |   Naposledy: [dim]{cp.last_attempt_at[:16]}[/]")
            if cp.best_points > 0:
                state_info += (
                    f"   |   Nejlepší: [yellow]{cp.best_points}b[/]")

            from engine.presenters import format_mastery_indicator
            mastery = format_mastery_indicator(state, cp.attempts)
            if mastery:
                state_info += f"   |   {mastery}"

            self.console.print(state_info)

            # Learning objective (if available)
            if d.learning_objective:
                self.console.print(
                    f"  [dim]🎯 Cíl: {d.learning_objective}[/]")
            self.console.print()

            # Theory
            if d.theory:
                self.console.print("  [cyan bold]📚 TEORIE:[/]")
                for line in d.theory.strip().split('\n'):
                    self.console.print(f"  [cyan]  {line.rstrip()}[/]")
                self.console.print()

            # Example
            if d.example:
                self.console.print("  [dim]Příklad:[/]")
                for line in d.example.strip().split('\n'):
                    self.console.print(f"  [green]  >>> {line.strip()}[/]")
                if d.example_output:
                    self.console.print(
                        f"  [white]  {d.example_output}[/]")
                self.console.print()

            # Description
            if d.description:
                self.console.print(f"  {d.description}")
                self.console.print()

            # Task
            if d.task:
                self.console.print("  [yellow bold]📝 ÚKOL:[/]")
                for line in d.task.strip().split('\n'):
                    self.console.print(f"  [yellow]  {line.rstrip()}[/]")
                self.console.print()

            # Last error with pedagogical feedback
            if state in (ChallengeState.REGRESSED, ChallengeState.IN_PROGRESS):
                last_err = self._get_last_error(d.challenge_id)
                if last_err:
                    from engine.feedback import generate_feedback
                    fb = generate_feedback(
                        last_err,
                        challenge_type=d.challenge_type,
                        hints=d.hints,
                        attempt_count=cp.attempt_count,
                        learning_objective=d.learning_objective,
                        expected_misconceptions=d.expected_misconceptions,
                        hint_strategy=d.hint_strategy,
                        challenge_state=state.value,
                        solution_pattern=d.solution_pattern,
                    )
                    self.console.print(
                        f"  [red bold]❌ {fb['title']}:[/]")
                    err_lines = last_err.split('\n')
                    for line in err_lines[:4]:
                        self.console.print(f"  [red]  {line}[/]")
                    self.console.print()
                    # Show top guidance
                    for tip in fb["guidance"][:2]:
                        self.console.print(f"  [yellow]💡 {tip}[/]")
                    if state == ChallengeState.REGRESSED:
                        self.console.print(
                            "  [dim]Dříve to procházelo — zkontroluj, "
                            "jestli jsi nezměnil něco v kódu.[/]"
                        )
                    self.console.print()

            # Hints count
            if d.hints:
                self.console.print(
                    f"  [dim]💡 Dostupné hinty: {len(d.hints)}[/]")

            # File path
            rel_path = os.path.relpath(lesson.challenge_file)
            line_num = find_challenge_line(
                lesson.challenge_file, d.index)
            if line_num:
                self.console.print(
                    f"  [dim]📝 {rel_path}:{line_num}[/]")
            else:
                self.console.print(f"  [dim]📝 {rel_path}[/]")
            self.console.print()

            # Navigation
            nav_parts = ["[cyan]\\[r][/] Spustit"]
            editor_name = get_editor()
            if editor_name:
                nav_parts.append("[cyan]\\[e][/] Editor")
            if d.hints:
                nav_parts.append("[cyan]\\[h][/] Hinty")
            if detail_idx > 0:
                nav_parts.append("[cyan]\\[p][/] Předchozí")
            if detail_idx < len(details) - 1:
                nav_parts.append("[cyan]\\[n][/] Další")
            nav_parts.append("[cyan]\\[0][/] Zpět")
            self.console.print("  " + "   ".join(nav_parts))
            self.console.print()

            self.progress.set_bookmark(
                section.num, lesson.lesson_num,
                section_name=section.name, lesson_name=lesson.name,
                challenge_index=d.index,
            )

            choice = self._safe_input()
            if choice in ("0", "q", "b", ""):
                return
            elif choice == "r":
                run_single_view(
                    self.console, self.progress, section, lesson,
                    d, details,
                )
            elif choice == "e" and editor_name:
                line = find_challenge_line(
                    lesson.challenge_file, d.index)
                open_file(lesson.challenge_file, line)
            elif choice == "h" and d.hints:
                self._show_hints(d)
            elif choice == "p" and detail_idx > 0:
                detail_idx -= 1
            elif choice == "n" and detail_idx < len(details) - 1:
                detail_idx += 1

    def _get_last_error(self, challenge_id: str) -> Optional[str]:
        raw = self.progress.data.get("challenges", {}).get(
            challenge_id, {})
        for a in reversed(raw.get("attempts", [])):
            if isinstance(a, dict) and not a.get("passed") and a.get("error"):
                return a["error"]
        return None

    def _show_hints(self, detail: ChallengeDetail):
        self.console.print()
        for i, hint in enumerate(detail.hints, 1):
            self.console.print(f"  [yellow]💡 Hint {i}: {hint}[/]")
        self.console.print()
        self._safe_input("  [dim]⏎ Enter...[/]")

    # ── Resume ──

    def _resume(self):
        bookmark = self.progress.get_bookmark()
        if not bookmark:
            return
        section = self._find_section(bookmark["section_num"])
        if not section:
            return
        lesson = self._find_lesson(section, bookmark["lesson_num"])
        if not lesson:
            return

        ch_idx = bookmark.get("challenge_index", 0)
        if ch_idx > 0:
            details = load_challenge_details(
                lesson.section_num, lesson.lesson_num,
                lesson.challenge_file,
            )
            if details and ch_idx <= len(details):
                self._challenge_detail(
                    section, lesson, details, ch_idx - 1)
                return

        self._lesson_detail(section, lesson)
