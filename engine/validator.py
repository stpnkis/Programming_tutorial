"""
📋 Content validation, lesson.yaml schema, and three-tier quality scoring.

Validates that challenges.py files are well-formed and that
lesson.yaml metadata matches reality. Computes content quality scores
across three tiers: Structure, Metadata, and Pedagogy.

Usage:
    python3 -m engine.validator           # validate all content
    python3 -m engine.validator 01        # validate section 01
    python3 -m engine.validator --fix     # generate missing lesson.yaml stubs
    python3 -m engine.validator --quality # show quality scores per lesson
    python3 -m engine.validator --qa      # quality + improvement suggestions
"""

import os
import re
import sys
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

# Schema definition for lesson.yaml
LESSON_SCHEMA = {
    "required": ["id", "title"],
    "optional": [
        "summary",
        "difficulty",
        "estimated_minutes",
        "tags",
        "prerequisites",
        "learning_objectives",
        "challenges",
        "why_it_matters",
        "what_you_will_learn",
        "key_theory",
        "lesson_summary",
        "recommended_next",
        "before_you_code",
    ],
    "types": {
        "id": str,
        "title": str,
        "summary": str,
        "difficulty": int,
        "estimated_minutes": int,
        "tags": list,
        "prerequisites": list,
        "learning_objectives": list,
        "challenges": list,
        "why_it_matters": str,
        "what_you_will_learn": str,
        "key_theory": str,
        "lesson_summary": str,
        "recommended_next": str,
        "before_you_code": str,
    },
}

CHALLENGE_SCHEMA = {
    "required": ["id", "title"],
    "optional": [
        "type",
        "difficulty",
        "points",
        "tags",
        "estimated_minutes",
        "learning_objective",
        "prerequisites",
        "hint_strategy",
        "review_priority",
        "expected_misconceptions",
        "mastery_rule",
        "solution_pattern",
        # Rich pedagogical fields
        "why_it_matters",
        "what_you_will_learn",
        "key_concept",
        "worked_example",
        "common_mistakes",
        "thinking_notes",
        "reference_solution",
        "solution_explanation",
        "practice_mode",
    ],
    "valid_types": [
        "implementation",
        "knowledge",
        "debugging",
        "refactoring",
        "trace",
        "open",
    ],
    "valid_hint_strategies": ["progressive", "contextual", "conceptual"],
    "valid_review_priorities": ["low", "normal", "high", "critical"],
    "valid_mastery_rules": ["3_consecutive", "2_consecutive", "single_pass"],
    "valid_practice_modes": ["guided", "open", "creative"],
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class LessonQuality:
    """Three-tier quality scoring for a single lesson.

    Tiers:
      - Structure (30pts): files exist, challenges have tests, YAML valid
      - Metadata (30pts): summary, objectives, tags, per-challenge objectives
      - Pedagogy (40pts): hints quality, body quality, type diversity,
                          misconceptions, learning objectives per challenge
    """

    path: str
    section_num: str = ""
    lesson_num: str = ""
    # Structure
    has_challenges: bool = False
    has_yaml: bool = False
    challenge_count: int = 0
    challenges_with_tests: int = 0
    # Metadata
    has_summary: bool = False
    has_quality_summary: bool = False  # summary > 15 chars, not just emoji
    has_learning_objectives: bool = False
    has_tags: bool = False
    challenges_with_objectives: int = 0
    challenges_with_misconceptions: int = 0
    # Pedagogy
    challenges_with_hints: int = 0
    challenges_with_quality_hints: int = 0  # hints with >15 char items
    func_body_quality: int = 0  # challenges with non-skeleton bodies
    type_diversity: int = 0  # number of distinct challenge types used
    # Rich pedagogical content
    has_why_it_matters: bool = False
    has_what_you_will_learn: bool = False
    has_key_theory: bool = False
    has_lesson_summary: bool = False
    has_recommended_next: bool = False
    has_before_you_code: bool = False
    challenges_with_worked_example: int = 0
    challenges_with_thinking_notes: int = 0
    challenges_with_reference_solution: int = 0
    challenges_with_common_mistakes: int = 0
    challenges_with_solution_explanation: int = 0
    # Pedagogical quality flags
    trivial_challenge_count: int = 0  # challenges with difficulty 1 AND points <= 10
    has_independent_task: bool = False  # at least one open/creative practice_mode
    has_reasoning_task: bool = False  # at least one trace/knowledge/debugging type

    @property
    def structure_score(self) -> float:
        """Structure tier: 0-30 points."""
        pts = 0.0
        if self.has_challenges:
            pts += 10
        if self.has_yaml:
            pts += 10
        if self.challenge_count > 0 and self.challenges_with_tests > 0:
            pts += 10 * min(self.challenges_with_tests / self.challenge_count, 1.0)
        return round(pts, 1)

    @property
    def metadata_score(self) -> float:
        """Metadata tier: 0-30 points."""
        pts = 0.0
        if self.has_quality_summary:
            pts += 8
        elif self.has_summary:
            pts += 4
        if self.has_learning_objectives:
            pts += 8
        if self.has_tags:
            pts += 4
        if self.challenge_count > 0:
            pts += 6 * min(self.challenges_with_objectives / self.challenge_count, 1.0)
            pts += 4 * min(
                self.challenges_with_misconceptions / self.challenge_count, 1.0
            )
        return round(pts, 1)

    @property
    def pedagogy_score(self) -> float:
        """Pedagogy tier: 0-40 points."""
        pts = 0.0
        if self.challenge_count > 0:
            # Quality hints (not just existence, but useful content)
            pts += 4 * min(
                self.challenges_with_quality_hints / self.challenge_count, 1.0
            )
            # Non-skeleton challenge bodies
            pts += 4 * min(self.func_body_quality / self.challenge_count, 1.0)
            # Worked examples
            pts += 4 * min(
                self.challenges_with_worked_example / self.challenge_count, 1.0
            )
            # Thinking notes
            pts += 2 * min(
                self.challenges_with_thinking_notes / self.challenge_count, 1.0
            )
            # Reference solutions
            pts += 3 * min(
                self.challenges_with_reference_solution / self.challenge_count, 1.0
            )
            # Solution explanations (new — ensures reference has reasoning)
            pts += 3 * min(
                self.challenges_with_solution_explanation / self.challenge_count, 1.0
            )
            # Common mistakes coverage
            pts += 2 * min(
                self.challenges_with_common_mistakes / self.challenge_count, 1.0
            )
        # Lesson-level pedagogical content
        if self.has_why_it_matters:
            pts += 3
        if self.has_what_you_will_learn:
            pts += 3
        if self.has_key_theory:
            pts += 3
        # New lesson completeness fields
        if self.has_lesson_summary:
            pts += 2
        if self.has_recommended_next:
            pts += 1
        if self.has_before_you_code:
            pts += 1
        # Challenge diversity bonus (caps at 3 pts for 3+ types)
        if self.challenge_count >= 3:
            pts += min(self.type_diversity, 3)
        # Reasoning/independent task bonus
        if self.has_reasoning_task:
            pts += 1
        if self.has_independent_task:
            pts += 1
        return round(min(pts, 40.0), 1)

    @property
    def score(self) -> float:
        """Compute overall quality score (0-100)."""
        return round(
            self.structure_score + self.metadata_score + self.pedagogy_score, 1
        )

    @property
    def grade(self) -> str:
        s = self.score
        if s >= 80:
            return "A"
        elif s >= 60:
            return "B"
        elif s >= 40:
            return "C"
        elif s >= 20:
            return "D"
        return "F"


class ValidationResult:
    """Accumulates validation errors, warnings, and quality data."""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.quality: List[LessonQuality] = []

    def error(self, path: str, msg: str):
        self.errors.append(f"ERROR  {path}: {msg}")

    def warn(self, path: str, msg: str):
        self.warnings.append(f"WARN   {path}: {msg}")

    def ok(self, path: str, msg: str):
        self.info.append(f"OK     {path}: {msg}")

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


def validate_challenges_file(
    filepath: str, result: ValidationResult, quality: Optional[LessonQuality] = None
):
    """Validate a challenges.py file for common issues."""
    rel = os.path.relpath(filepath, ROOT)

    if not os.path.isfile(filepath):
        result.error(rel, "File does not exist")
        return

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        result.error(rel, f"Cannot read file: {e}")
        return

    # Check for Challenge imports
    if "Challenge(" not in content:
        result.error(rel, "No Challenge() instances found")
        return

    # Count challenges
    challenge_count = len(re.findall(r"^\s+Challenge\(", content, re.MULTILINE))
    if challenge_count == 0:
        result.warn(rel, "No Challenge() found at expected indentation")
        return

    if quality:
        quality.has_challenges = True
        quality.challenge_count = challenge_count

    # Check for 'challenges' list
    if "challenges" not in content:
        result.warn(rel, "No 'challenges' variable found (expected list)")

    # Check that challenge functions exist for at least challenge 1
    func_count = len(re.findall(r"^def vyzva_\d+", content, re.MULTILINE))
    if func_count < challenge_count:
        result.warn(
            rel, f"{challenge_count} Challenge() but only {func_count} vyzva_ functions"
        )

    # Check for tests
    test_count = content.count("lambda:")
    if test_count == 0:
        result.warn(rel, "No test lambdas found")

    # Quality: check hints
    if quality:
        quality.challenges_with_tests = min(challenge_count, test_count)
        hint_count = len(re.findall(r"hints\s*=\s*\[", content))
        # Count hints that are non-empty lists
        non_empty_hints = len(re.findall(r'hints\s*=\s*\[\s*["\']', content))
        quality.challenges_with_hints = non_empty_hints
        # Quality hints: find hint strings >15 chars (actually helpful)
        hint_strings = re.findall(r"hints\s*=\s*\[(.*?)\]", content, re.DOTALL)
        quality_hint_count = 0
        for hs_block in hint_strings:
            items = re.findall(r'["\'](.+?)["\']', hs_block)
            if items and any(len(item.strip()) > 15 for item in items):
                quality_hint_count += 1
        quality.challenges_with_quality_hints = quality_hint_count

    # Quality: check function body quality (non-skeleton)
    if quality:
        real_bodies = 0
        for i in range(1, challenge_count + 1):
            func_pattern = (
                rf"def vyzva_{i}\b.*?" rf"(?=\ndef |\nchallenge|\n#\s*={{3,}}|\Z)"
            )
            match = re.search(func_pattern, content, re.DOTALL)
            if match:
                body = match.group(0)
                # Strip the def line, docstrings, comments
                lines = [
                    l.strip()
                    for l in body.split("\n")
                    if l.strip()
                    and not l.strip().startswith("#")
                    and not l.strip().startswith('"""')
                    and not l.strip().startswith("'''")
                    and not l.strip().startswith("def ")
                ]
                skeleton = {
                    "pass",
                    "...",
                    "return ...",
                    "return None",
                    "return",
                    "return {}",
                    "return []",
                }
                if lines and not all(
                    l in skeleton or l.startswith("# TODO") for l in lines
                ):
                    real_bodies += 1
        quality.func_body_quality = real_bodies

    result.ok(rel, f"{challenge_count} challenges, {func_count} functions")


def validate_lesson_yaml(
    yaml_path: str,
    challenges_path: str,
    result: ValidationResult,
    quality: Optional[LessonQuality] = None,
):
    """Validate a lesson.yaml file against its schema and linked challenges."""
    rel = os.path.relpath(yaml_path, ROOT)

    try:
        import yaml
    except ImportError:
        result.warn(rel, "PyYAML not installed — skipping YAML validation")
        return

    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        result.error(rel, f"Cannot parse YAML: {e}")
        return

    if not isinstance(data, dict):
        result.error(rel, "YAML root must be a mapping")
        return

    # Check required fields
    for f_name in LESSON_SCHEMA["required"]:
        if f_name not in data:
            result.error(rel, f"Missing required field: {f_name}")

    # Type checks
    for f_name, expected_type in LESSON_SCHEMA["types"].items():
        if f_name in data and not isinstance(data[f_name], expected_type):
            result.error(
                rel,
                f"Field '{f_name}' must be {expected_type.__name__}, "
                f"got {type(data[f_name]).__name__}",
            )

    # Validate difficulty range
    if "difficulty" in data:
        if not (1 <= data["difficulty"] <= 3):
            result.warn(rel, f"Difficulty {data['difficulty']} outside range 1-3")

    # Quality: lesson-level metadata
    if quality:
        quality.has_yaml = True
        summary_text = data.get("summary", "")
        quality.has_summary = bool(summary_text)
        # Quality summary: >15 chars and not just an emoji prefix
        quality.has_quality_summary = (
            bool(summary_text)
            and len(summary_text) > 15
            and not summary_text.startswith("🐍")
            and not summary_text.startswith("🏗️")
        )
        quality.has_learning_objectives = bool(data.get("learning_objectives"))
        quality.has_tags = bool(data.get("tags"))
        # Lesson-level pedagogical content
        quality.has_why_it_matters = (
            bool(data.get("why_it_matters"))
            and len(str(data.get("why_it_matters", ""))) > 20
        )
        quality.has_what_you_will_learn = (
            bool(data.get("what_you_will_learn"))
            and len(str(data.get("what_you_will_learn", ""))) > 20
        )
        quality.has_key_theory = (
            bool(data.get("key_theory")) and len(str(data.get("key_theory", ""))) > 20
        )
        quality.has_lesson_summary = (
            bool(data.get("lesson_summary"))
            and len(str(data.get("lesson_summary", ""))) > 20
        )
        quality.has_recommended_next = (
            bool(data.get("recommended_next"))
            and len(str(data.get("recommended_next", ""))) > 10
        )
        quality.has_before_you_code = (
            bool(data.get("before_you_code"))
            and len(str(data.get("before_you_code", ""))) > 20
        )

    # Validate challenges list
    if "challenges" in data and isinstance(data["challenges"], list):
        types_seen = set()
        for i, ch in enumerate(data["challenges"]):
            if not isinstance(ch, dict):
                result.error(rel, f"Challenge {i+1} must be a mapping")
                continue
            for f_name in CHALLENGE_SCHEMA["required"]:
                if f_name not in ch:
                    result.error(rel, f"Challenge {i+1} missing required: {f_name}")
            if "type" in ch:
                if ch["type"] not in CHALLENGE_SCHEMA["valid_types"]:
                    result.warn(rel, f"Challenge {i+1} unknown type: {ch['type']}")
                else:
                    types_seen.add(ch["type"])
            if "hint_strategy" in ch:
                if ch["hint_strategy"] not in CHALLENGE_SCHEMA["valid_hint_strategies"]:
                    result.warn(
                        rel,
                        f"Challenge {i+1} unknown hint_strategy: "
                        f"{ch['hint_strategy']}",
                    )
            if "review_priority" in ch:
                if (
                    ch["review_priority"]
                    not in CHALLENGE_SCHEMA["valid_review_priorities"]
                ):
                    result.warn(
                        rel,
                        f"Challenge {i+1} unknown review_priority: "
                        f"{ch['review_priority']}",
                    )
            if "mastery_rule" in ch:
                if ch["mastery_rule"] not in CHALLENGE_SCHEMA["valid_mastery_rules"]:
                    result.warn(
                        rel,
                        f"Challenge {i+1} unknown mastery_rule: "
                        f"{ch['mastery_rule']}",
                    )

            # Quality: per-challenge metadata
            if quality:
                if ch.get("learning_objective"):
                    quality.challenges_with_objectives += 1
                if ch.get("expected_misconceptions"):
                    quality.challenges_with_misconceptions += 1
                if ch.get("worked_example") and len(str(ch["worked_example"])) > 20:
                    quality.challenges_with_worked_example += 1
                if ch.get("thinking_notes") and len(str(ch["thinking_notes"])) > 20:
                    quality.challenges_with_thinking_notes += 1
                if (
                    ch.get("reference_solution")
                    and len(str(ch["reference_solution"])) > 10
                ):
                    quality.challenges_with_reference_solution += 1
                if (
                    ch.get("solution_explanation")
                    and len(str(ch["solution_explanation"])) > 15
                ):
                    quality.challenges_with_solution_explanation += 1
                if ch.get("common_mistakes") and len(ch["common_mistakes"]) > 0:
                    quality.challenges_with_common_mistakes += 1
                # Track trivial challenges (low difficulty + low points)
                diff = ch.get("difficulty", 1)
                pts = ch.get("points", 10)
                if diff <= 1 and pts <= 10:
                    quality.trivial_challenge_count += 1
                # Track reasoning/independent tasks
                ch_type = ch.get("type", "implementation")
                if ch_type in ("trace", "knowledge", "debugging"):
                    quality.has_reasoning_task = True
                pm = ch.get("practice_mode", "guided")
                if pm in ("open", "creative") or ch_type == "open":
                    quality.has_independent_task = True
            if "practice_mode" in ch:
                if ch["practice_mode"] not in CHALLENGE_SCHEMA["valid_practice_modes"]:
                    result.warn(
                        rel,
                        f"Challenge {i+1} unknown practice_mode: "
                        f"{ch['practice_mode']}",
                    )

        if quality:
            quality.type_diversity = len(types_seen)

        # Cross-check count against challenges.py
        if os.path.isfile(challenges_path):
            with open(challenges_path, "r", encoding="utf-8") as f:
                content = f.read()
            actual = len(re.findall(r"^\s+Challenge\(", content, re.MULTILINE))
            declared = len(data["challenges"])
            if actual != declared:
                result.warn(
                    rel,
                    f"YAML declares {declared} challenges but "
                    f"challenges.py has {actual}",
                )

    result.ok(rel, "YAML schema valid")


def validate_section(section_path: str, result: ValidationResult):
    """Validate all lessons within a section directory."""
    rel = os.path.relpath(section_path, ROOT)

    if not os.path.isdir(section_path):
        result.error(rel, "Section directory not found")
        return

    sec_num = os.path.basename(section_path)[:2]
    lesson_dirs = sorted(
        d
        for d in os.listdir(section_path)
        if os.path.isdir(os.path.join(section_path, d)) and re.match(r"^\d{2}_", d)
    )

    if not lesson_dirs:
        result.warn(rel, "No lesson directories found")
        return

    for lesson_dir in lesson_dirs:
        lesson_path = os.path.join(section_path, lesson_dir)
        challenges_file = os.path.join(lesson_path, "challenges.py")
        yaml_file = os.path.join(lesson_path, "lesson.yaml")

        les_num = lesson_dir[:2]
        quality = LessonQuality(
            path=os.path.relpath(lesson_path, ROOT),
            section_num=sec_num,
            lesson_num=les_num,
        )

        if os.path.isfile(challenges_file):
            validate_challenges_file(challenges_file, result, quality)
        else:
            result.warn(os.path.relpath(lesson_path, ROOT), "No challenges.py found")

        if os.path.isfile(yaml_file):
            validate_lesson_yaml(yaml_file, challenges_file, result, quality)

        result.quality.append(quality)


def validate_all(section_filter: Optional[str] = None) -> ValidationResult:
    """Validate the entire content tree (or a specific section)."""
    result = ValidationResult()

    section_dirs = sorted(
        d
        for d in os.listdir(ROOT)
        if os.path.isdir(os.path.join(ROOT, d)) and re.match(r"^\d{2}_", d)
    )

    for section_dir in section_dirs:
        sec_num = section_dir[:2]
        if section_filter and sec_num != section_filter:
            continue
        validate_section(os.path.join(ROOT, section_dir), result)

    return result


def format_quality_report(result: ValidationResult) -> str:
    """Format a quality report from validation results with three-tier scoring."""
    lines = []
    lines.append("")
    lines.append(
        "  ╔══════════════════════════════════════════════════════"
        "══════════════════════════╗"
    )
    lines.append(
        "  ║  QUALITY REPORT — Structure | Metadata | Pedagogy   "
        "                          ║"
    )
    lines.append(
        "  ╠══════╦═══════════════════════════════════╦═══════╦═══"
        "════╦════════╦══════════╣"
    )
    lines.append(
        "  ║ Sec  ║ Lesson                            ║ Str   ║ "
        "Meta  ║ Ped    ║ Total    ║"
    )
    lines.append(
        "  ╠══════╬═══════════════════════════════════╬═══════╬═══"
        "════╬════════╬══════════╣"
    )

    # Group by section
    by_section: Dict[str, List[LessonQuality]] = {}
    for q in result.quality:
        by_section.setdefault(q.section_num, []).append(q)

    section_scores: List[Tuple[str, float]] = []
    for sec_num in sorted(by_section):
        lessons = by_section[sec_num]
        sec_avg = sum(q.score for q in lessons) / len(lessons) if lessons else 0
        section_scores.append((sec_num, sec_avg))
        for q in lessons:
            name = q.path
            if len(name) > 33:
                name = "…" + name[-32:]
            grade = q.grade
            grade_color = {"A": "✅", "B": "🟢", "C": "🟡", "D": "🟠", "F": "🔴"}.get(
                grade, ""
            )
            lines.append(
                f"  ║ {q.section_num}.{q.lesson_num} ║ {name:<33s} ║ "
                f"{q.structure_score:>4.0f}  ║ {q.metadata_score:>4.0f}  ║ "
                f"{q.pedagogy_score:>5.0f}  ║ {q.score:>4.0f} {grade_color:<2s}  ║"
            )

    lines.append(
        "  ╚══════╩═══════════════════════════════════╩═══════╩═══"
        "════╩════════╩══════════╝"
    )

    # Section averages
    lines.append("")
    lines.append("  Section Averages:")
    for sec_num, avg in section_scores:
        bar_len = int(avg / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        g = (
            "A"
            if avg >= 80
            else "B" if avg >= 60 else "C" if avg >= 40 else "D" if avg >= 20 else "F"
        )
        lines.append(f"    {sec_num}: {bar} {avg:>5.1f} ({g})")

    # Overall
    all_scores = [q.score for q in result.quality]
    if all_scores:
        overall = sum(all_scores) / len(all_scores)
        avg_str = sum(q.structure_score for q in result.quality) / len(result.quality)
        avg_met = sum(q.metadata_score for q in result.quality) / len(result.quality)
        avg_ped = sum(q.pedagogy_score for q in result.quality) / len(result.quality)
        lines.append(
            f"\n  Overall: {overall:.1f}/100  "
            f"(Structure: {avg_str:.1f}/30  Metadata: {avg_met:.1f}/30  "
            f"Pedagogy: {avg_ped:.1f}/40)"
        )
        lines.append(f"  Lessons: {len(all_scores)}")
        lines.append(f"  Grade A (≥80): {sum(1 for s in all_scores if s >= 80)}")
        lines.append(f"  Grade F (<20): {sum(1 for s in all_scores if s < 20)}")

    return "\n".join(lines)


def format_qa_report(result: ValidationResult) -> str:
    """Format a QA report showing worst lessons and specific improvement actions."""
    lines = []
    lines.append("")
    lines.append("  ┌────────────────────────────────────────────────────────┐")
    lines.append("  │  🔍 QA IMPROVEMENT REPORT — Prioritized Actions       │")
    lines.append("  └────────────────────────────────────────────────────────┘")
    lines.append("")

    # Sort lessons by score (worst first)
    sorted_q = sorted(result.quality, key=lambda q: q.score)

    # Show worst 15 lessons with specific improvement suggestions
    lines.append("  📋 Worst Lessons (priority improvement targets):")
    lines.append("")

    for q in sorted_q[:15]:
        lines.append(
            f"  ── {q.section_num}.{q.lesson_num} {q.path} "
            f"— Score: {q.score:.0f} ({q.grade})"
        )
        suggestions = _get_improvement_suggestions(q)
        for sug in suggestions:
            lines.append(f"     → {sug}")
        lines.append("")

    # Global improvement summary
    lines.append("  📊 Global Improvement Summary:")
    total = len(result.quality)
    if total > 0:
        no_summary = sum(1 for q in result.quality if not q.has_quality_summary)
        no_objectives = sum(1 for q in result.quality if not q.has_learning_objectives)
        no_hints = sum(
            1
            for q in result.quality
            if q.challenge_count > 0 and q.challenges_with_quality_hints == 0
        )
        no_misconceptions = sum(
            1
            for q in result.quality
            if q.challenge_count > 0 and q.challenges_with_misconceptions == 0
        )
        skeleton_only = sum(
            1
            for q in result.quality
            if q.challenge_count > 0 and q.func_body_quality == 0
        )

        lines.append(f"     Missing quality summaries: {no_summary}/{total}")
        lines.append(f"     Missing learning objectives: {no_objectives}/{total}")
        lines.append(f"     Missing quality hints: {no_hints}/{total}")
        lines.append(f"     Missing misconceptions: {no_misconceptions}/{total}")
        lines.append(f"     Skeleton-only content: {skeleton_only}/{total}")
        lines.append("")

        # Highest impact actions
        lines.append("  🎯 Highest Impact Actions:")
        if skeleton_only > 0:
            lines.append(
                f"     1. Write real challenge bodies for {skeleton_only} skeleton lessons"
            )
        if no_objectives > 0:
            lines.append(f"     2. Add learning objectives to {no_objectives} lessons")
        if no_hints > 0:
            lines.append(f"     3. Add quality hints (>15 chars) to {no_hints} lessons")
        if no_misconceptions > 0:
            lines.append(f"     4. Add expected misconceptions to challenges")

    return "\n".join(lines)


def _get_improvement_suggestions(q: LessonQuality) -> List[str]:
    """Generate specific improvement suggestions for a lesson."""
    suggestions = []
    if not q.has_quality_summary:
        suggestions.append(
            "Add meaningful summary (>15 chars, describe what student learns)"
        )
    if not q.has_learning_objectives:
        suggestions.append("Add learning_objectives list to lesson.yaml")
    if not q.has_why_it_matters:
        suggestions.append("Add why_it_matters — explain practical relevance")
    if not q.has_what_you_will_learn:
        suggestions.append("Add what_you_will_learn — capability framing")
    if not q.has_key_theory:
        suggestions.append("Add key_theory — concise, practical theory before tasks")
    if not q.has_lesson_summary:
        suggestions.append("Add lesson_summary — reinforce key takeaways")
    if not q.has_recommended_next:
        suggestions.append("Add recommended_next — guide to next step")
    if q.challenge_count > 0 and q.func_body_quality == 0:
        suggestions.append("⚠️  All challenge bodies are skeleton — write real content")
    if q.challenge_count > 0 and q.challenges_with_quality_hints == 0:
        suggestions.append("Add quality hints to challenges (specific, >15 chars)")
    if q.challenge_count > 0 and q.challenges_with_objectives == 0:
        suggestions.append("Add learning_objective per challenge in lesson.yaml")
    if q.challenge_count > 0 and q.challenges_with_misconceptions == 0:
        suggestions.append("Add expected_misconceptions per challenge")
    if q.challenge_count > 0 and q.challenges_with_solution_explanation == 0:
        suggestions.append(
            "Add solution_explanation to challenges — explain WHY, not just WHAT"
        )
    if q.challenge_count > 0 and q.challenges_with_reference_solution == 0:
        suggestions.append("Add reference_solution to challenges")
    if q.type_diversity <= 1 and q.challenge_count >= 3:
        suggestions.append(
            "Use diverse challenge types (debugging, knowledge, trace, open)"
        )
    if q.challenge_count >= 4 and q.trivial_challenge_count > q.challenge_count * 0.6:
        suggestions.append(
            "⚠️  Too many trivial challenges — add harder/practical tasks"
        )
    if q.challenge_count >= 3 and not q.has_reasoning_task:
        suggestions.append(
            "Add at least one reasoning task (trace, knowledge, or debugging)"
        )
    return suggestions


def format_concept_coverage_report() -> str:
    """Format a concept coverage report showing which concepts have content."""
    lines = []
    lines.append("")
    lines.append("  ┌────────────────────────────────────────────────────────┐")
    lines.append("  │  🧠 CONCEPT COVERAGE REPORT                           │")
    lines.append("  └────────────────────────────────────────────────────────┘")
    lines.append("")

    try:
        from engine.concepts import load_concept_graph
        from engine.content import discover_sections
        from engine.adaptive import build_challenge_concept_map
        from engine.content import load_challenge_details
    except ImportError as e:
        lines.append(f"  ⚠️  Cannot load concept modules: {e}")
        return "\n".join(lines)

    graph = load_concept_graph()
    if not graph:
        lines.append("  ⚠️  No concept graph found (engine/concept_graph.yaml)")
        return "\n".join(lines)

    sections = discover_sections()
    challenge_concepts = build_challenge_concept_map(sections, load_challenge_details)

    # Count challenges per concept
    concept_coverage: Dict[str, int] = {cid: 0 for cid in graph}
    for cid, concepts in challenge_concepts.items():
        for concept_id in concepts:
            if concept_id in concept_coverage:
                concept_coverage[concept_id] += 1

    # Group by category
    by_category: Dict[str, List[Tuple[str, str, int]]] = {}
    for concept_id, node in graph.items():
        cat = node.category or "other"
        by_category.setdefault(cat, []).append(
            (concept_id, node.name, concept_coverage.get(concept_id, 0))
        )

    total_concepts = len(graph)
    covered = sum(1 for c in concept_coverage.values() if c > 0)
    uncovered = total_concepts - covered
    well_covered = sum(1 for c in concept_coverage.values() if c >= 3)

    lines.append(f"  Total concepts: {total_concepts}")
    lines.append(
        f"  Covered (≥1 challenge): {covered} ({100*covered//total_concepts}%)"
    )
    lines.append(f"  Well-covered (≥3 challenges): {well_covered}")
    lines.append(f"  Uncovered (0 challenges): {uncovered}")
    lines.append("")

    for cat in sorted(by_category):
        items = sorted(by_category[cat], key=lambda x: x[2])
        lines.append(f"  ── {cat.upper()} ──")
        for concept_id, name, count in items:
            icon = "✅" if count >= 3 else "🟡" if count >= 1 else "🔴"
            lines.append(
                f"    {icon} {name:<35s}  {count:>3d} challenges  ({concept_id})"
            )
        lines.append("")

    # Highlight gaps
    if uncovered > 0:
        lines.append("  🔴 UNCOVERED CONCEPTS (need content):")
        for concept_id, count in sorted(concept_coverage.items()):
            if count == 0:
                node = graph[concept_id]
                lines.append(f"     - {node.name} ({concept_id})")
        lines.append("")

    # Weak coverage
    weak_coverage = [(cid, c) for cid, c in concept_coverage.items() if 0 < c < 3]
    if weak_coverage:
        lines.append("  🟡 WEAK COVERAGE (1-2 challenges — need more):")
        for concept_id, count in sorted(weak_coverage, key=lambda x: x[1]):
            node = graph[concept_id]
            lines.append(f"     - {node.name}: {count} challenges ({concept_id})")
        lines.append("")

    # Prerequisite validation
    prereq_issues = []
    for concept_id, node in graph.items():
        for prereq in node.prerequisites:
            if prereq not in graph:
                prereq_issues.append((concept_id, prereq))
    if prereq_issues:
        lines.append("  ⚠️  PREREQUISITE ISSUES:")
        for concept_id, prereq in prereq_issues:
            lines.append(f"     {concept_id} requires unknown concept: {prereq}")
        lines.append("")

    return "\n".join(lines)


def main():
    """CLI entry point."""
    args = sys.argv[1:]
    section_filter = None
    fix_mode = False
    quality_mode = False
    qa_mode = False
    concepts_mode = False

    for arg in args:
        if arg == "--fix":
            fix_mode = True
        elif arg == "--quality":
            quality_mode = True
        elif arg == "--qa":
            qa_mode = True
        elif arg == "--concepts":
            concepts_mode = True
        elif arg == "--help" or arg == "-h":
            print(__doc__.strip())
            print(
                "    python3 -m engine.validator --concepts  # concept coverage report"
            )
            sys.exit(0)
        elif re.match(r"^\d{2}$", arg):
            section_filter = arg
        else:
            print(f"Unknown argument: {arg}")
            sys.exit(1)

    if fix_mode:
        # Generate missing lesson.yaml files
        from engine.scaffold import generate_all_yaml

        count = generate_all_yaml(section_filter=section_filter, overwrite=False)
        print(f"\n✅ Generated {count} lesson.yaml files")
        return

    if concepts_mode:
        print(format_concept_coverage_report())
        return

    result = validate_all(section_filter)

    if qa_mode:
        print(format_quality_report(result))
        print(format_qa_report(result))
        print()
        return

    if quality_mode:
        print(format_quality_report(result))
        print()
        return

    # Print results
    for msg in result.info:
        print(f"  \033[32m{msg}\033[0m")
    for msg in result.warnings:
        print(f"  \033[33m{msg}\033[0m")
    for msg in result.errors:
        print(f"  \033[31m{msg}\033[0m")

    print()
    total = len(result.info) + len(result.warnings) + len(result.errors)
    print(f"  Checked: {total} items")
    print(f"  Errors:  {len(result.errors)}")
    print(f"  Warnings: {len(result.warnings)}")

    if result.is_valid:
        print("\n  \033[32m✅ All content valid\033[0m")
    else:
        print("\n  \033[31m❌ Validation failed\033[0m")
        sys.exit(1)

    # Always show quality summary at end
    if result.quality:
        all_scores = [q.score for q in result.quality]
        overall = sum(all_scores) / len(all_scores)
        grades = {}
        for s in all_scores:
            g = (
                "A"
                if s >= 80
                else "B" if s >= 60 else "C" if s >= 40 else "D" if s >= 20 else "F"
            )
            grades[g] = grades.get(g, 0) + 1
        grade_str = "  ".join(f"{g}:{c}" for g, c in sorted(grades.items()))
        print(f"\n  Quality: {overall:.1f}/100 avg   ({grade_str})")
        print("  Run with --quality for detailed report")
        print("  Run with --concepts for concept coverage report")


if __name__ == "__main__":
    main()
