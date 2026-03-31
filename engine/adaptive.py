"""
🎯 Adaptive Learning Engine — concept-aware recommendation, study plans, repair paths.

Builds on recommend.py by adding concept-centric intelligence:
- Weak concept drill: identify and practice weakest concepts
- Repair paths: when a concept regresses, sequence fixing prereqs first
- Study plans: guided, fast-track, reinforcement, project paths
- Session planning: "what to do today" based on concept state
- Transparent reasoning: every recommendation includes WHY
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple

from engine.models import ChallengeState, SectionInfo, LessonInfo
from engine.concepts import (
    ConceptMastery,
    ConceptState,
    ConceptNode,
    load_concept_graph,
    get_all_prerequisites,
    get_ready_concepts,
    get_weak_concepts,
    check_prerequisites_met,
    compute_all_concept_states,
    get_concept_summary,
)
from engine.recommend import (
    ActionCategory,
    Recommendation,
    get_smart_recommendations,
    get_review_queue,
    get_weak_areas,
    _resolve_names,
)


# ── Study plan modes ──


class StudyMode(Enum):
    GUIDED = "guided"  # follow prerequisite order, theory first
    FAST_TRACK = "fast_track"  # skip what you know, jump ahead
    REINFORCEMENT = "reinforcement"  # focus on weak/regressed concepts
    PROJECT = "project"  # project-oriented learning path
    INTERVIEW = "interview"  # algorithm & DS drill focus


STUDY_MODE_INFO = {
    StudyMode.GUIDED: {
        "name": "Vedený postup",
        "emoji": "📚",
        "description": "Systematický postup od základů. Respektuje prerekvizity.",
    },
    StudyMode.FAST_TRACK: {
        "name": "Zrychlený postup",
        "emoji": "⚡",
        "description": "Přeskoč co umíš. Zaměř se na nové koncepty.",
    },
    StudyMode.REINFORCEMENT: {
        "name": "Opakování a posilování",
        "emoji": "🔄",
        "description": "Zaměř se na slabé a regresované koncepty.",
    },
    StudyMode.PROJECT: {
        "name": "Projektový postup",
        "emoji": "🏗️",
        "description": "Uč se skrze projekty a větší celky.",
    },
    StudyMode.INTERVIEW: {
        "name": "Interview drill",
        "emoji": "🎯",
        "description": "Algoritmy, datové struktury, problém-solving.",
    },
}


# ── Adaptive recommendation ──


@dataclass
class AdaptiveRecommendation:
    """Enhanced recommendation with concept-level reasoning."""

    # Core recommendation data
    category: ActionCategory
    challenge_id: str
    section_num: str
    lesson_num: str
    challenge_index: int
    priority: int = 0
    lesson_name: str = ""
    section_name: str = ""
    # Concept-level intelligence
    reason: str = ""  # human-readable explanation
    target_concepts: List[str] = field(default_factory=list)
    improves_weakness: bool = False  # targets a weak concept
    fixes_regression: bool = False  # fixes regressed concept
    prerequisite_gap: bool = False  # fills a prereq gap
    concept_reasoning: str = ""  # detailed concept explanation


@dataclass
class StudyPlan:
    """A structured study plan for a session or longer period."""

    mode: StudyMode
    # Today's plan
    today_recommendations: List[AdaptiveRecommendation] = field(default_factory=list)
    today_focus_concepts: List[str] = field(default_factory=list)
    today_estimated_minutes: int = 0
    # Progress context
    overall_mastery_pct: float = 0.0
    weak_concept_count: int = 0
    regressed_concept_count: int = 0
    ready_to_learn: List[str] = field(default_factory=list)
    # Explanation
    plan_reasoning: str = ""
    focus_area: str = ""


@dataclass
class RepairPath:
    """Sequence of steps to repair a regressed or weak concept."""

    target_concept: str
    target_concept_name: str
    steps: List[AdaptiveRecommendation] = field(default_factory=list)
    missing_prerequisites: List[str] = field(default_factory=list)
    reasoning: str = ""
    estimated_minutes: int = 0


# ── Challenge-to-concept mapping ──


def build_challenge_concept_map(
    sections: List[SectionInfo],
    load_challenge_details_fn,
) -> Dict[str, List[str]]:
    """Build mapping from challenge_id → list of concept_ids.

    Uses lesson.yaml tags + concept_graph to resolve mappings.
    Tags in lessons are matched to concept IDs via a lookup table.
    """
    graph = load_concept_graph()
    tag_to_concepts = _build_tag_concept_lookup(graph)

    mapping: Dict[str, List[str]] = {}

    for section in sections:
        for lesson in section.lessons:
            lesson_tags = [t.lower() for t in lesson.meta.tags]
            lesson_concepts = set()
            for tag in lesson_tags:
                if tag in tag_to_concepts:
                    lesson_concepts.update(tag_to_concepts[tag])

            # Load per-challenge details to get challenge-specific tags
            try:
                details = load_challenge_details_fn(
                    section.num,
                    lesson.lesson_num,
                    lesson.challenge_file,
                )
            except Exception:
                details = []

            for i, detail in enumerate(details, 1):
                cid = f"{lesson.section_num}.{lesson.lesson_num}.{i}"
                ch_tags = [t.lower() for t in getattr(detail, "tags", [])]
                ch_concepts = set(lesson_concepts)
                for tag in ch_tags:
                    if tag in tag_to_concepts:
                        ch_concepts.update(tag_to_concepts[tag])

                # Also check key_concept field
                key_concept = getattr(detail, "key_concept", "") or ""
                if key_concept:
                    for concept_id in graph:
                        if concept_id in key_concept.lower():
                            ch_concepts.add(concept_id)

                mapping[cid] = sorted(ch_concepts)

            # Fallback: if no details loaded, assign lesson concepts
            if not details:
                for i in range(1, lesson.challenge_count + 1):
                    cid = f"{lesson.section_num}.{lesson.lesson_num}.{i}"
                    if cid not in mapping:
                        mapping[cid] = sorted(lesson_concepts)

    return mapping


def _build_tag_concept_lookup(graph: Dict[str, ConceptNode]) -> Dict[str, List[str]]:
    """Build reverse mapping: lesson tag → list of concept IDs."""
    lookup: Dict[str, List[str]] = {}

    # Direct mappings from concept IDs
    for cid, node in graph.items():
        # Map category
        cat = node.category.lower()
        lookup.setdefault(cat, []).append(cid)

        # Map concept ID parts as tags
        parts = cid.split(".")
        for part in parts:
            lookup.setdefault(part.lower(), []).append(cid)

    # Common tag aliases
    _aliases = {
        "basics": ["python.variables", "python.types", "python.operators"],
        "fundamentals": [
            "python.variables",
            "python.types",
            "python.conditions",
            "python.loops",
        ],
        "functions": ["python.functions", "python.function_params"],
        "return": ["python.functions"],
        "parameters": ["python.function_params"],
        "defaults": ["python.function_params"],
        "args": ["python.args_kwargs"],
        "kwargs": ["python.args_kwargs"],
        "variadic": ["python.args_kwargs"],
        "lambda": ["python.lambda"],
        "anonymous": ["python.lambda"],
        "higher-order": ["python.higher_order"],
        "closure": ["python.closures"],
        "strings": ["python.strings", "python.string_methods"],
        "formatting": ["python.fstrings"],
        "lists": ["python.lists", "python.list_indexing", "python.list_methods"],
        "slicing": ["python.list_indexing"],
        "indexing": ["python.list_indexing"],
        "comprehensions": ["python.list_comprehensions"],
        "dictionaries": ["python.dicts", "python.dict_methods"],
        "dict": ["python.dicts"],
        "sets": ["python.sets"],
        "tuples": ["python.tuples"],
        "loops": ["python.loops", "python.loop_control"],
        "conditions": ["python.conditions"],
        "boolean": ["python.boolean_logic"],
        "files": ["python.file_io"],
        "io": ["python.file_io"],
        "exceptions": ["python.exceptions"],
        "errors": ["python.exceptions"],
        "error_handling": ["python.exceptions"],
        "modules": ["python.modules"],
        "imports": ["python.modules"],
        "packages": ["python.packages"],
        "decorators": ["python.decorators"],
        "generators": ["python.generators"],
        "iterators": ["python.generators"],
        "classes": ["oop.classes", "oop.init", "oop.self"],
        "objects": ["oop.classes"],
        "inheritance": ["oop.inheritance"],
        "polymorphism": ["oop.polymorphism"],
        "encapsulation": ["oop.encapsulation"],
        "abstract": ["oop.abstract_classes"],
        "magic_methods": ["oop.magic_methods"],
        "dataclasses": ["oop.dataclasses"],
        "composition": ["oop.composition"],
        "solid": ["oop.solid"],
        "design_patterns": ["oop.design_patterns"],
        "arrays": ["ds.arrays"],
        "linked_lists": ["ds.linked_lists"],
        "stacks": ["ds.stacks"],
        "queues": ["ds.queues"],
        "trees": ["ds.trees"],
        "graphs": ["ds.graphs"],
        "hash": ["ds.hashing"],
        "sorting": ["ds.sorting"],
        "searching": ["ds.searching"],
        "recursion": ["ds.recursion"],
        "dynamic_programming": ["ds.dynamic_programming"],
        "big_o": ["ds.big_o"],
        "complexity": ["ds.big_o"],
        "algorithms": ["ds.sorting", "ds.searching", "ds.recursion"],
        "unittest": ["testing.unittest"],
        "pytest": ["testing.pytest"],
        "mocking": ["testing.mocking"],
        "tdd": ["testing.tdd"],
        "git": ["git.basics"],
        "branching": ["git.branching"],
        "debugging": ["debugging.pdb"],
        "logging": ["debugging.logging"],
    }

    for tag, concepts in _aliases.items():
        lookup.setdefault(tag, []).extend(concepts)

    # Deduplicate
    for tag in lookup:
        lookup[tag] = sorted(set(lookup[tag]))

    return lookup


# ── Adaptive recommendation engine ──


def get_adaptive_recommendations(
    progress,
    sections: List[SectionInfo],
    concept_states: Dict[str, ConceptState],
    challenge_concepts: Dict[str, List[str]],
    mode: StudyMode = StudyMode.GUIDED,
    limit: int = 10,
    now: Optional[datetime] = None,
) -> List[AdaptiveRecommendation]:
    """Build concept-aware adaptive recommendations.

    Combines challenge-level recommendations with concept-level intelligence.
    """
    now = now or datetime.now()
    graph = load_concept_graph()
    recs: List[AdaptiveRecommendation] = []

    if mode == StudyMode.REINFORCEMENT:
        recs = _reinforcement_recommendations(
            progress,
            sections,
            concept_states,
            challenge_concepts,
            graph,
            limit,
            now,
        )
    elif mode == StudyMode.FAST_TRACK:
        recs = _fast_track_recommendations(
            progress,
            sections,
            concept_states,
            challenge_concepts,
            graph,
            limit,
            now,
        )
    elif mode == StudyMode.INTERVIEW:
        recs = _interview_recommendations(
            progress,
            sections,
            concept_states,
            challenge_concepts,
            graph,
            limit,
            now,
        )
    else:
        # GUIDED or PROJECT
        recs = _guided_recommendations(
            progress,
            sections,
            concept_states,
            challenge_concepts,
            graph,
            limit,
            now,
        )

    return recs[:limit]


def _guided_recommendations(
    progress,
    sections,
    concept_states,
    challenge_concepts,
    graph,
    limit,
    now,
) -> List[AdaptiveRecommendation]:
    """Guided mode: respect prerequisites, fix regressions first, then new."""
    recs = []
    priority = 0

    # 1. Fix regressed concepts
    for cs in get_weak_concepts(concept_states):
        if cs.mastery != ConceptMastery.REGRESSED:
            continue
        for cid in cs.weakest_challenge_ids[:2]:
            parts = cid.split(".")
            if len(parts) < 3:
                continue
            sec_name, les_name = _resolve_names(sections, parts[0], parts[1])
            node = graph.get(cs.concept_id)
            recs.append(
                AdaptiveRecommendation(
                    category=ActionCategory.FIX_REGRESSION,
                    challenge_id=cid,
                    section_num=parts[0],
                    lesson_num=parts[1],
                    challenge_index=int(parts[2]),
                    priority=priority,
                    lesson_name=les_name,
                    section_name=sec_name,
                    reason=f"Regrese v konceptu '{node.name if node else cs.concept_id}'",
                    target_concepts=[cs.concept_id],
                    fixes_regression=True,
                    concept_reasoning=f"Koncept '{node.name if node else cs.concept_id}' "
                    f"měl regresi — oprav to, aby se neprohloubila.",
                )
            )
            priority += 1

    # 2. Fill prerequisite gaps for weak concepts
    for cs in get_weak_concepts(concept_states):
        met, missing = check_prerequisites_met(cs.concept_id, concept_states)
        if met:
            continue
        for pid in missing[:2]:
            _add_concept_challenges(
                recs,
                pid,
                progress,
                sections,
                challenge_concepts,
                graph,
                priority=50 + priority,
                reason_prefix="Chybějící prerekvizita",
                is_prereq_gap=True,
            )
            priority += 1

    # 3. Review due (from original engine)
    review = get_review_queue(progress, sections, now)
    for r in review[:3]:
        concepts = challenge_concepts.get(r.challenge_id, [])
        recs.append(
            AdaptiveRecommendation(
                category=ActionCategory.REVIEW_DUE,
                challenge_id=r.challenge_id,
                section_num=r.section_num,
                lesson_num=r.lesson_num,
                challenge_index=r.challenge_index,
                priority=100 + r.priority,
                lesson_name=r.lesson_name,
                section_name=r.section_name,
                reason=r.reason,
                target_concepts=concepts,
                concept_reasoning=(
                    f"Procvič koncepty: {', '.join(concepts[:3])}" if concepts else ""
                ),
            )
        )

    # 4. Ready-to-learn concepts (prereqs met, not started)
    ready = get_ready_concepts(concept_states)
    for concept_id in ready[:3]:
        _add_concept_challenges(
            recs,
            concept_id,
            progress,
            sections,
            challenge_concepts,
            graph,
            priority=200 + priority,
            reason_prefix="Připraveno k učení",
        )
        priority += 1

    # 5. Continue in-progress
    base_recs = get_smart_recommendations(progress, sections, now, limit=5)
    for r in base_recs:
        if r.category == ActionCategory.CONTINUE_WORK:
            concepts = challenge_concepts.get(r.challenge_id, [])
            recs.append(
                AdaptiveRecommendation(
                    category=r.category,
                    challenge_id=r.challenge_id,
                    section_num=r.section_num,
                    lesson_num=r.lesson_num,
                    challenge_index=r.challenge_index,
                    priority=300 + r.priority,
                    lesson_name=r.lesson_name,
                    section_name=r.section_name,
                    reason=r.reason,
                    target_concepts=concepts,
                )
            )

    recs.sort(key=lambda r: r.priority)
    return recs


def _reinforcement_recommendations(
    progress,
    sections,
    concept_states,
    challenge_concepts,
    graph,
    limit,
    now,
) -> List[AdaptiveRecommendation]:
    """Reinforcement mode: focus on weak and regressed concepts."""
    recs = []
    priority = 0

    weak = get_weak_concepts(concept_states)
    for cs in weak:
        _add_concept_challenges(
            recs,
            cs.concept_id,
            progress,
            sections,
            challenge_concepts,
            graph,
            priority=priority,
            reason_prefix=(
                "Posilování slabého konceptu"
                if cs.mastery == ConceptMastery.WEAK
                else "Oprava regrese"
            ),
            is_weakness=cs.mastery == ConceptMastery.WEAK,
            is_regression=cs.mastery == ConceptMastery.REGRESSED,
        )
        priority += 10

    # Add review-due items
    review = get_review_queue(progress, sections, now)
    for r in review[:5]:
        concepts = challenge_concepts.get(r.challenge_id, [])
        recs.append(
            AdaptiveRecommendation(
                category=ActionCategory.REVIEW_DUE,
                challenge_id=r.challenge_id,
                section_num=r.section_num,
                lesson_num=r.lesson_num,
                challenge_index=r.challenge_index,
                priority=100 + r.priority,
                lesson_name=r.lesson_name,
                section_name=r.section_name,
                reason=r.reason,
                target_concepts=concepts,
            )
        )

    recs.sort(key=lambda r: r.priority)
    return recs


def _fast_track_recommendations(
    progress,
    sections,
    concept_states,
    challenge_concepts,
    graph,
    limit,
    now,
) -> List[AdaptiveRecommendation]:
    """Fast-track: skip what's known, advance to highest-level ready concepts."""
    recs = []

    # Fix regressions first (even in fast-track)
    for cs in get_weak_concepts(concept_states):
        if cs.mastery != ConceptMastery.REGRESSED:
            continue
        for cid in cs.weakest_challenge_ids[:1]:
            parts = cid.split(".")
            if len(parts) < 3:
                continue
            sec_name, les_name = _resolve_names(sections, parts[0], parts[1])
            node = graph.get(cs.concept_id)
            recs.append(
                AdaptiveRecommendation(
                    category=ActionCategory.FIX_REGRESSION,
                    challenge_id=cid,
                    section_num=parts[0],
                    lesson_num=parts[1],
                    challenge_index=int(parts[2]),
                    priority=0,
                    lesson_name=les_name,
                    section_name=sec_name,
                    reason=f"Regrese v '{node.name if node else cs.concept_id}'",
                    target_concepts=[cs.concept_id],
                    fixes_regression=True,
                )
            )

    # Ready concepts sorted by difficulty (higher first for fast-track)
    ready = get_ready_concepts(concept_states)
    ready_with_diff = [(cid, graph[cid].difficulty) for cid in ready if cid in graph]
    ready_with_diff.sort(key=lambda x: -x[1])

    priority = 10
    for concept_id, diff in ready_with_diff[:5]:
        _add_concept_challenges(
            recs,
            concept_id,
            progress,
            sections,
            challenge_concepts,
            graph,
            priority=priority,
            reason_prefix="Skok vpřed",
        )
        priority += 10

    recs.sort(key=lambda r: r.priority)
    return recs


def _interview_recommendations(
    progress,
    sections,
    concept_states,
    challenge_concepts,
    graph,
    limit,
    now,
) -> List[AdaptiveRecommendation]:
    """Interview mode: focus on DS & algorithms."""
    target_categories = {"data_structures", "testing"}
    recs = []
    priority = 0

    # Get DS concepts
    ds_concepts = [
        cid for cid, node in graph.items() if node.category in target_categories
    ]

    for concept_id in ds_concepts:
        cs = concept_states.get(concept_id)
        if cs and cs.mastery in (ConceptMastery.MASTERED, ConceptMastery.PROFICIENT):
            continue  # skip what's already known

        met, missing = check_prerequisites_met(concept_id, concept_states)
        if not met:
            continue  # skip if prereqs not met

        _add_concept_challenges(
            recs,
            concept_id,
            progress,
            sections,
            challenge_concepts,
            graph,
            priority=priority,
            reason_prefix="Interview prep",
        )
        priority += 10

    recs.sort(key=lambda r: r.priority)
    return recs


def _add_concept_challenges(
    recs: List[AdaptiveRecommendation],
    concept_id: str,
    progress,
    sections: List[SectionInfo],
    challenge_concepts: Dict[str, List[str]],
    graph: Dict[str, ConceptNode],
    priority: int = 0,
    reason_prefix: str = "",
    is_weakness: bool = False,
    is_regression: bool = False,
    is_prereq_gap: bool = False,
    max_per_concept: int = 2,
):
    """Add challenge recommendations for a specific concept."""
    node = graph.get(concept_id)
    concept_name = node.name if node else concept_id

    # Find challenges tagged with this concept
    relevant = [
        (cid, concepts)
        for cid, concepts in challenge_concepts.items()
        if concept_id in concepts
    ]

    added = 0
    for cid, concepts in sorted(relevant):
        if added >= max_per_concept:
            break

        cp = progress.get_challenge(cid)
        if cp.state in (ChallengeState.MASTERED,):
            continue  # skip already mastered

        parts = cid.split(".")
        if len(parts) < 3:
            continue

        sec_name, les_name = _resolve_names(sections, parts[0], parts[1])

        reason = f"{reason_prefix}: {concept_name}"
        concept_reasoning = ""
        if is_prereq_gap:
            concept_reasoning = (
                f"Koncept '{concept_name}' je prerekvizita pro slabé koncepty. "
                f"Doplň si základ, aby ses mohl posunout dál."
            )
        elif is_weakness:
            concept_reasoning = (
                f"Koncept '{concept_name}' je slabý ({cp.attempt_count} pokusů). "
                f"Procvič ho pro zlepšení."
            )
        elif is_regression:
            concept_reasoning = (
                f"V konceptu '{concept_name}' máš regresi. "
                f"Nejprve oprav regrese, aby se neprohloubily."
            )

        cat = (
            ActionCategory.FIX_REGRESSION
            if is_regression
            else (
                ActionCategory.CONCEPT_PRACTICE
                if is_weakness
                else (
                    ActionCategory.CONCEPT_PRACTICE
                    if is_prereq_gap
                    else (
                        ActionCategory.NEW_MATERIAL
                        if cp.state == ChallengeState.NOT_STARTED
                        else ActionCategory.CONTINUE_WORK
                    )
                )
            )
        )

        recs.append(
            AdaptiveRecommendation(
                category=cat,
                challenge_id=cid,
                section_num=parts[0],
                lesson_num=parts[1],
                challenge_index=int(parts[2]),
                priority=priority + added,
                lesson_name=les_name,
                section_name=sec_name,
                reason=reason,
                target_concepts=concepts,
                improves_weakness=is_weakness,
                fixes_regression=is_regression,
                prerequisite_gap=is_prereq_gap,
                concept_reasoning=concept_reasoning,
            )
        )
        added += 1


# ── Study plan generation ──


def generate_study_plan(
    progress,
    sections: List[SectionInfo],
    concept_states: Dict[str, ConceptState],
    challenge_concepts: Dict[str, List[str]],
    mode: StudyMode = StudyMode.GUIDED,
    session_minutes: int = 30,
    now: Optional[datetime] = None,
) -> StudyPlan:
    """Generate a structured study plan for today's session."""
    now = now or datetime.now()

    recs = get_adaptive_recommendations(
        progress,
        sections,
        concept_states,
        challenge_concepts,
        mode=mode,
        limit=15,
        now=now,
    )

    # Estimate time and select recommendations that fit session
    today_recs = []
    minutes_used = 0
    focus_concepts = set()

    for r in recs:
        est_minutes = 5 if r.category in (ActionCategory.REVIEW_DUE,) else 8
        if minutes_used + est_minutes > session_minutes:
            break
        today_recs.append(r)
        minutes_used += est_minutes
        focus_concepts.update(r.target_concepts)

    # Compute summary stats
    summary = get_concept_summary(concept_states)
    total_concepts = sum(summary.values())
    mastered = summary.get("mastered", 0) + summary.get("proficient", 0)
    mastery_pct = mastered / total_concepts if total_concepts > 0 else 0.0

    weak_count = summary.get("weak", 0)
    regressed_count = summary.get("regressed", 0)
    ready = get_ready_concepts(concept_states)

    # Build reasoning
    if mode == StudyMode.REINFORCEMENT:
        reasoning = (
            f"Zaměřeno na opakování a posilování. "
            f"{weak_count} slabých konceptů, {regressed_count} regresí."
        )
        focus = "Slabé a regresované koncepty"
    elif mode == StudyMode.FAST_TRACK:
        reasoning = (
            f"Zrychlený postup — přeskakuji co je zvládnuté. "
            f"{len(ready)} konceptů připraveno k učení."
        )
        focus = "Nové koncepty s nejvyšší obtížností"
    elif mode == StudyMode.INTERVIEW:
        reasoning = "Interview drill — algoritmy a datové struktury."
        focus = "Datové struktury a algoritmy"
    else:
        parts = []
        if regressed_count > 0:
            parts.append(f"oprava {regressed_count} regresí")
        if weak_count > 0:
            parts.append(f"posilování {weak_count} slabých konceptů")
        if ready:
            parts.append(f"{len(ready)} nových konceptů připraveno")
        reasoning = (
            "Vedený postup: " + ", ".join(parts) if parts else "Pokračuj v učení."
        )
        focus = "Prerekvizity → slabiny → nový materiál"

    graph = load_concept_graph()
    return StudyPlan(
        mode=mode,
        today_recommendations=today_recs,
        today_focus_concepts=sorted(focus_concepts)[:5],
        today_estimated_minutes=minutes_used,
        overall_mastery_pct=mastery_pct,
        weak_concept_count=weak_count,
        regressed_concept_count=regressed_count,
        ready_to_learn=[graph[c].name if c in graph else c for c in ready[:5]],
        plan_reasoning=reasoning,
        focus_area=focus,
    )


# ── Repair paths ──


def build_repair_path(
    concept_id: str,
    progress,
    sections: List[SectionInfo],
    concept_states: Dict[str, ConceptState],
    challenge_concepts: Dict[str, List[str]],
) -> RepairPath:
    """Build a repair path for a weak or regressed concept.

    The path sequences: missing prereqs first → then concept challenges.
    """
    graph = load_concept_graph()
    node = graph.get(concept_id)
    concept_name = node.name if node else concept_id

    path = RepairPath(
        target_concept=concept_id,
        target_concept_name=concept_name,
    )

    # Check prerequisites
    met, missing = check_prerequisites_met(concept_id, concept_states)
    path.missing_prerequisites = missing

    steps = []
    minutes = 0

    # Step 1: Fix missing prerequisites
    for pid in missing:
        _add_concept_challenges(
            steps,
            pid,
            progress,
            sections,
            challenge_concepts,
            graph,
            priority=len(steps),
            reason_prefix="Doplň prerekvizitu",
            is_prereq_gap=True,
        )
        minutes += 10

    # Step 2: Practice the target concept
    _add_concept_challenges(
        steps,
        concept_id,
        progress,
        sections,
        challenge_concepts,
        graph,
        priority=100 + len(steps),
        reason_prefix="Procvič cílový koncept",
        is_weakness=True,
        max_per_concept=5,
    )
    minutes += 15

    path.steps = steps
    path.estimated_minutes = minutes

    if missing:
        prereq_names = [graph[p].name if p in graph else p for p in missing]
        path.reasoning = (
            f"Konzept '{concept_name}' je slabý a chybí prerekvizity: "
            f"{', '.join(prereq_names)}. Nejprve doplň základy, pak procvič koncept."
        )
    else:
        path.reasoning = (
            f"Koncept '{concept_name}' je slabý. "
            f"Procvič relevantní výzvy pro zlepšení."
        )

    return path
