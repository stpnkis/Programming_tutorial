"""
Service facade — clean interface between the learning engine and any UI layer.

This module provides UI-agnostic services that both the TUI (Rich) and
the desktop GUI (Flask API) can consume.  Every public function returns
plain Python dicts / lists suitable for JSON serialisation.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import textwrap
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from engine.models import (
    ChallengeDetail,
    ChallengeState,
    ChallengeType,
    SectionInfo,
)
from engine.content import (
    discover_sections,
    load_challenge_details,
    run_single_challenge,
    search_lessons,
)
from engine.progress import Progress
from engine.recommend import (
    build_snapshot,
    categorize_recommendations,
    get_review_queue,
    get_smart_recommendations,
    get_weak_areas,
)
from engine.feedback import classify_error, generate_feedback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Singleton state ──────────────────────────────────────────

_sections: Optional[List[SectionInfo]] = None
_progress: Optional[Progress] = None


def _get_sections() -> List[SectionInfo]:
    global _sections
    if _sections is None:
        _sections = discover_sections()
    return _sections


def _get_progress() -> Progress:
    global _progress
    if _progress is None:
        _progress = Progress()
    return _progress


def refresh_sections() -> None:
    """Force re-discovery (e.g. after adding new content)."""
    global _sections
    _sections = None


def refresh_progress() -> None:
    """Reload progress from disk."""
    global _progress
    _progress = Progress()


# ── Content services ─────────────────────────────────────────


def get_sections() -> List[Dict[str, Any]]:
    """Return all curriculum sections with their lessons."""
    result = []
    for s in _get_sections():
        lessons = []
        for l in s.lessons:
            prog = _get_progress()
            completed = prog.get_lesson_completed(l.section_num, l.lesson_num)
            lessons.append(
                {
                    "id": l.lesson_id,
                    "section_num": l.section_num,
                    "lesson_num": l.lesson_num,
                    "name": l.name,
                    "dir_name": l.dir_name,
                    "challenge_count": l.challenge_count,
                    "completed": completed,
                    "meta": {
                        "summary": l.meta.summary,
                        "difficulty": l.meta.difficulty,
                        "estimated_minutes": l.meta.estimated_minutes,
                        "tags": l.meta.tags,
                        "prerequisites": l.meta.prerequisites,
                        "learning_objectives": l.meta.learning_objectives,
                    },
                }
            )
        result.append(
            {
                "num": s.num,
                "name": s.name,
                "emoji": s.emoji,
                "lessons": lessons,
            }
        )
    return result


def get_lesson_detail(section_num: str, lesson_num: str) -> Optional[Dict[str, Any]]:
    """Return lesson detail including all challenge metadata."""
    for s in _get_sections():
        if s.num != section_num:
            continue
        for l in s.lessons:
            if l.lesson_num != lesson_num:
                continue

            # Load enriched challenge details
            details = load_challenge_details(s.num, l.lesson_num, l.challenge_file)
            prog = _get_progress()

            challenges = []
            for d in details:
                cp = prog.get_challenge(d.challenge_id)
                challenges.append(
                    {
                        "index": d.index,
                        "id": d.challenge_id,
                        "title": d.title,
                        "description": d.description,
                        "task": d.task,
                        "theory": d.theory,
                        "example": d.example,
                        "example_output": d.example_output,
                        "hints": d.hints,
                        "difficulty": d.difficulty,
                        "points": d.points,
                        "type": d.challenge_type.value,
                        "tags": d.tags,
                        "learning_objective": d.learning_objective,
                        "expected_misconceptions": d.expected_misconceptions,
                        "hint_strategy": d.hint_strategy,
                        # Pedagogical content (new rich fields)
                        "why_it_matters": getattr(d, "why_it_matters", ""),
                        "what_you_will_learn": getattr(d, "what_you_will_learn", ""),
                        "key_concept": getattr(d, "key_concept", ""),
                        "worked_example": getattr(d, "worked_example", ""),
                        "common_mistakes": getattr(d, "common_mistakes", []),
                        "thinking_notes": getattr(d, "thinking_notes", ""),
                        "reference_solution": getattr(d, "reference_solution", ""),
                        "solution_explanation": getattr(d, "solution_explanation", ""),
                        "practice_mode": getattr(d, "practice_mode", "guided"),
                        # Progress
                        "state": cp.state.value,
                        "attempt_count": cp.attempt_count,
                        "best_points": cp.best_points,
                    }
                )

            # Load lesson-level pedagogical content from YAML
            yaml_data = _load_lesson_yaml(l.path)

            return {
                "id": l.lesson_id,
                "name": l.name,
                "section_num": section_num,
                "lesson_num": lesson_num,
                "dir_name": l.dir_name,
                "challenge_file": l.challenge_file,
                "meta": {
                    "summary": l.meta.summary,
                    "difficulty": l.meta.difficulty,
                    "estimated_minutes": l.meta.estimated_minutes,
                    "tags": l.meta.tags,
                    "prerequisites": l.meta.prerequisites,
                    "learning_objectives": l.meta.learning_objectives,
                },
                # Lesson-level pedagogical content (from model + yaml)
                "why_it_matters": l.meta.why_it_matters
                or yaml_data.get("why_it_matters", ""),
                "what_you_will_learn": l.meta.what_you_will_learn
                or yaml_data.get("what_you_will_learn", ""),
                "key_theory": l.meta.key_theory or yaml_data.get("key_theory", ""),
                "lesson_summary": yaml_data.get("lesson_summary", ""),
                "recommended_next": yaml_data.get("recommended_next", ""),
                "before_you_code": yaml_data.get("before_you_code", ""),
                "challenges": challenges,
            }
    return None


def _load_lesson_yaml(lesson_path: str) -> Dict[str, Any]:
    """Load raw lesson.yaml data."""
    yaml_file = os.path.join(lesson_path, "lesson.yaml")
    if not os.path.isfile(yaml_file):
        return {}
    try:
        import yaml

        with open(yaml_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


# ── Progress services ────────────────────────────────────────


def get_progress_snapshot() -> Dict[str, Any]:
    """Return global learning snapshot."""
    snap = build_snapshot(_get_progress(), _get_sections())
    return {
        "total_challenges": snap.total_challenges,
        "mastered": snap.mastered,
        "currently_passing": snap.currently_passing,
        "in_progress": snap.in_progress,
        "regressed": snap.regressed,
        "not_started": snap.not_started,
        "review_due_count": snap.review_due_count,
        "mastery_pct": snap.mastery_pct,
        "progress_pct": snap.progress_pct,
    }


def get_challenge_progress(challenge_id: str) -> Dict[str, Any]:
    """Return progress for a single challenge."""
    cp = _get_progress().get_challenge(challenge_id)
    return {
        "state": cp.state.value,
        "attempt_count": cp.attempt_count,
        "best_points": cp.best_points,
        "max_points": cp.max_points,
        "ever_passed": cp.ever_passed,
        "last_attempt_at": cp.last_attempt_at,
    }


# ── Recommendation services ─────────────────────────────────


def get_recommendations(limit: int = 10) -> List[Dict[str, Any]]:
    """Return smart recommendations."""
    now = datetime.now(timezone.utc)
    recs = get_smart_recommendations(
        _get_progress(),
        _get_sections(),
        now,
        limit=limit,
    )
    return [
        {
            "section_num": r.section_num,
            "lesson_num": r.lesson_num,
            "lesson_name": r.lesson_name,
            "challenge_index": r.challenge_index,
            "category": r.category.value,
            "reason": r.reason,
        }
        for r in recs
    ]


def get_categorized_recs() -> Dict[str, List[Dict[str, Any]]]:
    """Return recommendations grouped by category."""
    now = datetime.now(timezone.utc)
    cats = categorize_recommendations(_get_progress(), _get_sections(), now)
    result = {}
    for key, recs in cats.items():
        result[key] = [
            {
                "section_num": r.section_num,
                "lesson_num": r.lesson_num,
                "lesson_name": r.lesson_name,
                "challenge_index": r.challenge_index,
                "category": r.category.value,
                "reason": r.reason,
            }
            for r in recs
        ]
    return result


# ── Execution services ───────────────────────────────────────


def run_challenge(
    section_num: str, lesson_num: str, challenge_index: int
) -> Dict[str, Any]:
    """Run a single challenge and record the result.

    Returns execution result with feedback.
    """
    sections = _get_sections()
    detail = _find_challenge_detail(section_num, lesson_num, challenge_index)
    if detail is None:
        return {"error": "Challenge not found"}

    passed, messages, error = run_single_challenge(detail)

    # Record in progress
    prog = _get_progress()
    state_before = prog.get_challenge_state(detail.challenge_id)
    prog.save_challenge(
        detail.challenge_id,
        passed,
        detail.points if passed else 0,
        detail.points,
        error,
    )
    state_after = prog.get_challenge_state(detail.challenge_id)

    # Generate feedback if failed
    feedback_data = None
    if not passed and error:
        feedback_data = generate_feedback(
            error,
            detail.challenge_type,
            detail.hints,
            prog.get_challenge(detail.challenge_id).attempt_count,
            learning_objective=detail.learning_objective,
            expected_misconceptions=detail.expected_misconceptions,
            hint_strategy=detail.hint_strategy,
            challenge_state=state_after,
            solution_pattern=detail.solution_pattern,
        )
        # Serialise enum
        feedback_data["category"] = feedback_data["category"].value

    return {
        "passed": passed,
        "messages": messages,
        "error": error,
        "points": detail.points if passed else 0,
        "max_points": detail.points,
        "state_before": state_before.value,
        "state_after": state_after.value,
        "feedback": feedback_data,
    }


def execute_code(code: str, timeout: int = 10) -> Dict[str, Any]:
    """Execute arbitrary Python code in a subprocess (REPL mode).

    Returns stdout, stderr, and return code.
    """
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        delete=False,
        dir=ROOT,
    ) as f:
        f.write(code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=ROOT,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": f"Časový limit {timeout}s překročen.",
            "returncode": -1,
        }
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


# ── File services ────────────────────────────────────────────


def get_challenge_file_content(section_num: str, lesson_num: str) -> Dict[str, Any]:
    """Return the challenge file content for editing."""
    lesson = _find_lesson(section_num, lesson_num)
    if lesson is None:
        return {"error": "Lesson not found"}

    try:
        with open(lesson.challenge_file, "r", encoding="utf-8") as f:
            content = f.read()
        rel_path = os.path.relpath(lesson.challenge_file, ROOT)
        return {
            "path": rel_path,
            "content": content,
            "absolute_path": lesson.challenge_file,
        }
    except Exception as e:
        return {"error": str(e)}


def save_challenge_file(
    section_num: str, lesson_num: str, content: str
) -> Dict[str, Any]:
    """Save edited challenge file content."""
    lesson = _find_lesson(section_num, lesson_num)
    if lesson is None:
        return {"error": "Lesson not found"}

    try:
        with open(lesson.challenge_file, "w", encoding="utf-8") as f:
            f.write(content)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}


def search(query: str) -> List[Dict[str, Any]]:
    """Search lessons by name/tags/summary."""
    results = search_lessons(_get_sections(), query)
    return [
        {
            "id": l.lesson_id,
            "name": l.name,
            "section_num": l.section_num,
            "lesson_num": l.lesson_num,
            "summary": l.meta.summary,
            "tags": l.meta.tags,
        }
        for l in results
    ]


# ── Concept mastery services ─────────────────────────────────


def get_concept_mastery() -> Dict[str, Any]:
    """Return concept mastery states for all concepts."""
    from engine.concepts import (
        load_concept_graph,
        compute_all_concept_states,
        get_weak_concepts,
        get_ready_concepts,
    )
    from engine.adaptive import build_challenge_concept_map

    graph = load_concept_graph()
    sections = _get_sections()
    progress = _get_progress()
    challenge_map = build_challenge_concept_map(sections, load_challenge_details)
    states = compute_all_concept_states(challenge_map, progress.get_challenge)

    concepts = {}
    for cid, state in states.items():
        node = graph.get(cid)
        concepts[cid] = {
            "name": node.name if node else cid,
            "category": node.category if node else "",
            "mastery": state.mastery.value,
            "score": state.score,
            "total_challenges": state.total_challenges,
            "passing_challenges": state.passing_challenges,
            "prerequisites": node.prerequisites if node else [],
            "key_insight": node.key_insight if node else "",
            "common_confusion": node.common_confusion if node else "",
        }

    weak = get_weak_concepts(states)
    ready = get_ready_concepts(states)

    return {
        "concepts": concepts,
        "weak_concepts": [c.concept_id for c in weak],
        "ready_concepts": ready,
    }


def get_adaptive_recs(mode: str = "guided", limit: int = 10) -> List[Dict[str, Any]]:
    """Return concept-aware adaptive recommendations."""
    from engine.adaptive import (
        get_adaptive_recommendations,
        build_challenge_concept_map,
        StudyMode,
    )
    from engine.concepts import compute_all_concept_states

    mode_map = {
        "guided": StudyMode.GUIDED,
        "fast_track": StudyMode.FAST_TRACK,
        "reinforcement": StudyMode.REINFORCEMENT,
        "interview": StudyMode.INTERVIEW,
    }
    study_mode = mode_map.get(mode, StudyMode.GUIDED)

    sections = _get_sections()
    progress = _get_progress()
    challenge_map = build_challenge_concept_map(sections, load_challenge_details)
    concept_states = compute_all_concept_states(challenge_map, progress.get_challenge)

    recs = get_adaptive_recommendations(
        progress,
        sections,
        concept_states,
        challenge_map,
        mode=study_mode,
        limit=limit,
    )
    return [
        {
            "section_num": r.section_num,
            "lesson_num": r.lesson_num,
            "lesson_name": r.lesson_name,
            "challenge_index": r.challenge_index,
            "category": r.category.value,
            "reason": r.reason,
            "target_concepts": r.target_concepts,
            "concept_reasoning": r.concept_reasoning,
        }
        for r in recs
    ]


def get_study_plan(mode: str = "guided", session_minutes: int = 30) -> Dict[str, Any]:
    """Generate a study plan for today."""
    from engine.adaptive import (
        generate_study_plan,
        build_challenge_concept_map,
        StudyMode,
        STUDY_MODE_INFO,
    )
    from engine.concepts import compute_all_concept_states

    mode_map = {
        "guided": StudyMode.GUIDED,
        "fast_track": StudyMode.FAST_TRACK,
        "reinforcement": StudyMode.REINFORCEMENT,
        "interview": StudyMode.INTERVIEW,
    }
    study_mode = mode_map.get(mode, StudyMode.GUIDED)

    sections = _get_sections()
    progress = _get_progress()
    challenge_map = build_challenge_concept_map(sections, load_challenge_details)
    concept_states = compute_all_concept_states(challenge_map, progress.get_challenge)

    plan = generate_study_plan(
        progress,
        sections,
        concept_states,
        challenge_map,
        mode=study_mode,
        session_minutes=session_minutes,
    )

    mode_info = STUDY_MODE_INFO.get(plan.mode, {})

    return {
        "mode": plan.mode.value,
        "mode_name": mode_info.get("name", ""),
        "mode_emoji": mode_info.get("emoji", ""),
        "mode_description": mode_info.get("description", ""),
        "focus_concepts": plan.today_focus_concepts,
        "focus_area": plan.focus_area,
        "estimated_minutes": plan.today_estimated_minutes,
        "reasoning": plan.plan_reasoning,
        "overall_mastery_pct": round(plan.overall_mastery_pct * 100, 1),
        "weak_concept_count": plan.weak_concept_count,
        "regressed_concept_count": plan.regressed_concept_count,
        "ready_to_learn": plan.ready_to_learn,
        "steps": [
            {
                "section_num": r.section_num,
                "lesson_num": r.lesson_num,
                "lesson_name": r.lesson_name,
                "challenge_index": r.challenge_index,
                "category": r.category.value,
                "reason": r.reason,
                "target_concepts": r.target_concepts,
                "concept_reasoning": r.concept_reasoning,
            }
            for r in plan.today_recommendations
        ],
    }


def get_projects() -> List[Dict[str, Any]]:
    """Return available projects with progress."""
    from engine.projects import load_projects, get_available_projects
    from engine.concepts import load_concept_graph, compute_all_concept_states
    from engine.adaptive import build_challenge_concept_map

    graph = load_concept_graph()
    challenge_map = build_challenge_concept_map(
        _get_sections(),
        load_challenge_details,
    )
    states = compute_all_concept_states(challenge_map, _get_progress().get_challenge)

    available = get_available_projects(states)
    all_projects = load_projects()

    result = []
    for pid, proj in all_projects.items():
        is_available = pid in [p.id for p in available]
        result.append(
            {
                "id": pid,
                "name": proj.title,
                "description": proj.summary,
                "difficulty": proj.difficulty.value,
                "section": proj.section,
                "required_concepts": proj.prerequisite_concepts,
                "available": is_available,
                "milestones": [
                    {
                        "id": m.id,
                        "name": m.name,
                        "description": m.description,
                        "concepts": m.concepts,
                        "hints": m.hints,
                        "estimated_minutes": m.estimated_minutes,
                    }
                    for m in proj.milestones
                ],
            }
        )
    return result


def get_reflection(
    context: str,
    section_num: str = "",
    lesson_num: str = "",
    challenge_index: int = -1,
    passed: bool = False,
) -> Dict[str, Any]:
    """Generate reflection prompts based on context."""
    from engine.reflection import (
        generate_post_challenge_reflection,
        generate_post_lesson_reflection,
        generate_concept_insight,
    )

    if context == "challenge" and challenge_index >= 0:
        detail = _find_challenge_detail(section_num, lesson_num, challenge_index)
        if detail is None:
            return {"prompts": []}
        cp = _get_progress().get_challenge(detail.challenge_id)
        prompts = generate_post_challenge_reflection(
            challenge_title=detail.title,
            challenge_type=detail.challenge_type.value,
            concepts=detail.tags,
            attempt_count=cp.attempt_count,
            passed=passed,
        )
        return {"prompts": [p.__dict__ for p in prompts]}

    if context == "lesson":
        lesson = _find_lesson(section_num, lesson_num)
        if lesson is None:
            return {"prompts": []}
        prompts = generate_post_lesson_reflection(
            lesson_name=lesson.name,
            concepts=lesson.meta.tags,
            mastered_count=0,
            total_count=lesson.challenge_count,
        )
        return {"prompts": [p.__dict__ for p in prompts]}

    if context == "concept":
        from engine.concepts import load_concept_graph

        graph = load_concept_graph()
        # Return insights for weak concepts
        from engine.concepts import compute_all_concept_states, get_weak_concepts
        from engine.adaptive import build_challenge_concept_map

        challenge_map = build_challenge_concept_map(
            _get_sections(),
            load_challenge_details,
        )
        states = compute_all_concept_states(
            challenge_map, _get_progress().get_challenge
        )
        weak = get_weak_concepts(states)
        insights = []
        for ws in weak[:5]:
            insight = generate_concept_insight(ws.concept_id, graph)
            if insight:
                insights.append(insight.__dict__)
        return {"insights": insights}

    return {"prompts": []}


# ── Helpers ──────────────────────────────────────────────────


def _find_lesson(section_num: str, lesson_num: str):
    for s in _get_sections():
        if s.num != section_num:
            continue
        for l in s.lessons:
            if l.lesson_num == lesson_num:
                return l
    return None


def _find_challenge_detail(
    section_num: str, lesson_num: str, index: int
) -> Optional[ChallengeDetail]:
    lesson = _find_lesson(section_num, lesson_num)
    if lesson is None:
        return None
    details = load_challenge_details(section_num, lesson_num, lesson.challenge_file)
    for d in details:
        if d.index == index:
            return d
    return None
