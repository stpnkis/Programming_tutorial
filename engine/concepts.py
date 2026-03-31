"""
🧠 Concept Mastery Model — concept-centric knowledge tracking.

Defines the concept taxonomy, concept graph (prerequisites),
and computes concept mastery from per-challenge attempt data.

A *concept* is a reusable unit of knowledge (e.g. "variables",
"boolean_logic", "list_indexing"). Challenges and lessons are tagged
with concepts. The system aggregates challenge-level performance
into concept-level mastery states.

Concept IDs are dot-separated hierarchical strings:
    "python.variables"
    "python.functions.parameters"
    "oop.classes.init"
"""

from __future__ import annotations

import os
import yaml
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from engine.models import ChallengeState, ChallengeProgress


# ── Concept mastery states ──


class ConceptMastery(Enum):
    """Mastery level for a single concept, aggregated from challenges."""

    NOT_SEEN = "not_seen"  # no challenges attempted
    WEAK = "weak"  # < 40% of associated challenges passing
    DEVELOPING = "developing"  # 40-69% passing
    PROFICIENT = "proficient"  # 70-89% passing
    MASTERED = "mastered"  # ≥ 90% passing or mastered
    REGRESSED = "regressed"  # was proficient+, now has regressions


MASTERY_THRESHOLDS = {
    "weak": 0.0,
    "developing": 0.40,
    "proficient": 0.70,
    "mastered": 0.90,
}

MASTERY_DISPLAY = {
    ConceptMastery.NOT_SEEN: ("⬜", "dim", "Neviděno"),
    ConceptMastery.WEAK: ("🔴", "red", "Slabé"),
    ConceptMastery.DEVELOPING: ("🟡", "yellow", "Rozvíjí se"),
    ConceptMastery.PROFICIENT: ("🟢", "green", "Zdatný"),
    ConceptMastery.MASTERED: ("💎", "bold green", "Zvládnuto"),
    ConceptMastery.REGRESSED: ("🔻", "bold red", "Regrese"),
}


# ── Concept definition ──


@dataclass
class ConceptNode:
    """A single concept in the knowledge graph."""

    id: str  # e.g. "python.functions.parameters"
    name: str  # human-readable: "Parametry funkcí"
    description: str = ""  # what this concept includes
    category: str = ""  # top-level grouping: "python", "oop", ...
    prerequisites: List[str] = field(default_factory=list)  # concept IDs
    related: List[str] = field(default_factory=list)  # related concepts
    difficulty: int = 1  # 1-3
    # Teaching pointers
    key_insight: str = ""  # one-sentence core insight
    common_confusion: str = ""  # typical misunderstanding
    transfer_hint: str = ""  # how this appears in other contexts


@dataclass
class ConceptState:
    """Runtime state for a single concept — computed, not stored."""

    concept_id: str
    mastery: ConceptMastery = ConceptMastery.NOT_SEEN
    # Evidence
    total_challenges: int = 0
    passing_challenges: int = 0
    mastered_challenges: int = 0
    regressed_challenges: int = 0
    # Score 0.0-1.0 (passing fraction)
    score: float = 0.0
    # History signal
    had_regression: bool = False
    weakest_challenge_ids: List[str] = field(default_factory=list)


# ── Concept graph (loaded from YAML) ──

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONCEPTS_FILE = os.path.join(ROOT, "engine", "concept_graph.yaml")

_concept_cache: Optional[Dict[str, ConceptNode]] = None


def load_concept_graph() -> Dict[str, ConceptNode]:
    """Load the concept taxonomy from concept_graph.yaml.

    Returns dict mapping concept_id → ConceptNode.
    """
    global _concept_cache
    if _concept_cache is not None:
        return _concept_cache

    if not os.path.isfile(CONCEPTS_FILE):
        _concept_cache = {}
        return _concept_cache

    with open(CONCEPTS_FILE, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    nodes: Dict[str, ConceptNode] = {}
    for cid, data in raw.get("concepts", {}).items():
        nodes[cid] = ConceptNode(
            id=cid,
            name=data.get("name", cid),
            description=data.get("description", ""),
            category=data.get("category", cid.split(".")[0] if "." in cid else ""),
            prerequisites=data.get("prerequisites", []),
            related=data.get("related", []),
            difficulty=data.get("difficulty", 1),
            key_insight=data.get("key_insight", ""),
            common_confusion=data.get("common_confusion", ""),
            transfer_hint=data.get("transfer_hint", ""),
        )

    _concept_cache = nodes
    return _concept_cache


def invalidate_concept_cache():
    """Force reload on next access."""
    global _concept_cache
    _concept_cache = None


def get_concept(concept_id: str) -> Optional[ConceptNode]:
    """Get a single concept node by ID."""
    return load_concept_graph().get(concept_id)


def get_all_concepts() -> List[ConceptNode]:
    """All concepts sorted by category then ID."""
    return sorted(load_concept_graph().values(), key=lambda c: (c.category, c.id))


def get_concept_categories() -> List[str]:
    """Unique top-level categories."""
    return sorted(set(c.category for c in load_concept_graph().values()))


# ── Prerequisite graph queries ──


def get_prerequisites(concept_id: str) -> List[str]:
    """Direct prerequisites for a concept."""
    node = get_concept(concept_id)
    return node.prerequisites if node else []


def get_all_prerequisites(concept_id: str) -> Set[str]:
    """Transitive closure of prerequisites (all ancestor concepts)."""
    graph = load_concept_graph()
    visited: Set[str] = set()
    stack = [concept_id]
    while stack:
        cid = stack.pop()
        node = graph.get(cid)
        if not node:
            continue
        for prereq in node.prerequisites:
            if prereq not in visited:
                visited.add(prereq)
                stack.append(prereq)
    return visited


def get_dependents(concept_id: str) -> List[str]:
    """Concepts that directly depend on this concept."""
    graph = load_concept_graph()
    return [cid for cid, node in graph.items() if concept_id in node.prerequisites]


def check_prerequisites_met(
    concept_id: str, concept_states: Dict[str, ConceptState]
) -> Tuple[bool, List[str]]:
    """Check if all prerequisites are at least DEVELOPING.

    Returns (all_met, list_of_missing_concept_ids).
    """
    prereqs = get_prerequisites(concept_id)
    missing = []
    for pid in prereqs:
        state = concept_states.get(pid)
        if state is None or state.mastery in (
            ConceptMastery.NOT_SEEN,
            ConceptMastery.WEAK,
        ):
            missing.append(pid)
    return len(missing) == 0, missing


# ── Concept mastery computation ──


def compute_concept_mastery(
    concept_id: str, challenge_concepts: Dict[str, List[str]], get_challenge_progress
) -> ConceptState:
    """Compute mastery state for a single concept.

    Args:
        concept_id: The concept to evaluate.
        challenge_concepts: Mapping of challenge_id → list of concept_ids.
        get_challenge_progress: Callable(challenge_id) → ChallengeProgress.
    """
    # Find all challenges tagged with this concept
    relevant = [
        cid for cid, concepts in challenge_concepts.items() if concept_id in concepts
    ]

    state = ConceptState(concept_id=concept_id)
    state.total_challenges = len(relevant)

    if not relevant:
        return state

    passing = 0
    mastered = 0
    regressed = 0
    weakest = []

    for cid in relevant:
        cp = get_challenge_progress(cid)
        cs = cp.state
        if cs in (ChallengeState.CURRENTLY_PASSING, ChallengeState.MASTERED):
            passing += 1
        if cs == ChallengeState.MASTERED:
            mastered += 1
        if cs == ChallengeState.REGRESSED:
            regressed += 1
            weakest.append(cid)
        elif cs == ChallengeState.IN_PROGRESS:
            weakest.append(cid)

    state.passing_challenges = passing
    state.mastered_challenges = mastered
    state.regressed_challenges = regressed
    state.weakest_challenge_ids = weakest[:5]  # top 5
    state.score = passing / len(relevant) if relevant else 0.0

    # Determine mastery level
    if regressed > 0:
        state.mastery = ConceptMastery.REGRESSED
        state.had_regression = True
    elif state.score >= MASTERY_THRESHOLDS["mastered"]:
        state.mastery = ConceptMastery.MASTERED
    elif state.score >= MASTERY_THRESHOLDS["proficient"]:
        state.mastery = ConceptMastery.PROFICIENT
    elif state.score >= MASTERY_THRESHOLDS["developing"]:
        state.mastery = ConceptMastery.DEVELOPING
    elif passing > 0 or any(
        get_challenge_progress(c).attempt_count > 0 for c in relevant
    ):
        state.mastery = ConceptMastery.WEAK
    else:
        state.mastery = ConceptMastery.NOT_SEEN

    return state


def compute_all_concept_states(
    challenge_concepts: Dict[str, List[str]],
    get_challenge_progress,
) -> Dict[str, ConceptState]:
    """Compute mastery for all known concepts.

    Args:
        challenge_concepts: Mapping challenge_id → [concept_ids].
        get_challenge_progress: Callable(cid) → ChallengeProgress.

    Returns:
        Dict mapping concept_id → ConceptState.
    """
    graph = load_concept_graph()
    states = {}
    for concept_id in graph:
        states[concept_id] = compute_concept_mastery(
            concept_id,
            challenge_concepts,
            get_challenge_progress,
        )
    return states


def get_weak_concepts(concept_states: Dict[str, ConceptState]) -> List[ConceptState]:
    """Concepts that are WEAK or REGRESSED — ordered by severity."""
    weak = [
        s
        for s in concept_states.values()
        if s.mastery in (ConceptMastery.REGRESSED, ConceptMastery.WEAK)
    ]
    # Regressed first, then by score ascending
    weak.sort(
        key=lambda s: (0 if s.mastery == ConceptMastery.REGRESSED else 1, s.score)
    )
    return weak


def get_ready_concepts(concept_states: Dict[str, ConceptState]) -> List[str]:
    """Concepts whose prerequisites are met but are NOT_SEEN — good to learn next."""
    ready = []
    for cid, state in concept_states.items():
        if state.mastery != ConceptMastery.NOT_SEEN:
            continue
        met, _ = check_prerequisites_met(cid, concept_states)
        if met:
            ready.append(cid)
    return ready


def get_concept_summary(concept_states: Dict[str, ConceptState]) -> Dict[str, int]:
    """Count concepts per mastery level."""
    summary: Dict[str, int] = {m.value: 0 for m in ConceptMastery}
    for state in concept_states.values():
        summary[state.mastery.value] += 1
    return summary
