"""Tests for the concept mastery model (engine/concepts.py)."""

import pytest
from unittest.mock import MagicMock, patch

from engine.concepts import (
    ConceptMastery,
    ConceptNode,
    ConceptState,
    compute_concept_mastery,
    compute_all_concept_states,
    get_weak_concepts,
    get_ready_concepts,
    get_concept_summary,
    check_prerequisites_met,
    get_all_prerequisites,
    get_dependents,
    invalidate_concept_cache,
)
from engine.models import ChallengeState, ChallengeProgress, AttemptRecord


# ── Helpers ──


def _make_progress(state: ChallengeState) -> ChallengeProgress:
    """Create a ChallengeProgress with the given state."""
    cp = ChallengeProgress(attempts=[])
    cp._state_override = state
    return cp


def _make_mock_graph():
    """Create a small concept graph for testing."""
    return {
        "python.variables": ConceptNode(
            id="python.variables",
            name="Proměnné",
            category="python",
            prerequisites=[],
            difficulty=1,
        ),
        "python.types": ConceptNode(
            id="python.types",
            name="Datové typy",
            category="python",
            prerequisites=["python.variables"],
            difficulty=1,
        ),
        "python.conditions": ConceptNode(
            id="python.conditions",
            name="Podmínky",
            category="python",
            prerequisites=["python.types"],
            difficulty=1,
        ),
        "python.loops": ConceptNode(
            id="python.loops",
            name="Cykly",
            category="python",
            prerequisites=["python.conditions"],
            difficulty=1,
        ),
        "python.functions": ConceptNode(
            id="python.functions",
            name="Funkce",
            category="python",
            prerequisites=["python.variables", "python.types"],
            difficulty=1,
        ),
    }


# ── compute_concept_mastery ──


class TestComputeConceptMastery:
    def test_no_challenges(self):
        """Concept with no associated challenges -> NOT_SEEN."""
        challenge_concepts = {}  # no mapping
        state = compute_concept_mastery(
            "python.variables",
            challenge_concepts,
            lambda x: ChallengeProgress(attempts=[]),
        )
        assert state.mastery == ConceptMastery.NOT_SEEN
        assert state.total_challenges == 0

    def test_all_mastered(self):
        """All challenges mastered -> concept MASTERED."""
        challenge_concepts = {
            "01.01.1": ["python.variables"],
            "01.01.2": ["python.variables"],
            "01.01.3": ["python.variables"],
        }

        def get_prog(cid):
            cp = MagicMock()
            cp.state = ChallengeState.MASTERED
            return cp

        state = compute_concept_mastery(
            "python.variables", challenge_concepts, get_prog
        )
        assert state.mastery == ConceptMastery.MASTERED
        assert state.score == 1.0
        assert state.total_challenges == 3

    def test_partial_passing(self):
        """Some passing, some not -> DEVELOPING or PROFICIENT."""
        challenge_concepts = {
            "01.01.1": ["python.variables"],
            "01.01.2": ["python.variables"],
            "01.01.3": ["python.variables"],
        }

        progress_map = {
            "01.01.1": ChallengeState.MASTERED,
            "01.01.2": ChallengeState.CURRENTLY_PASSING,
            "01.01.3": ChallengeState.IN_PROGRESS,
        }

        def get_prog(cid):
            cp = MagicMock()
            cp.state = progress_map.get(cid, ChallengeState.NOT_STARTED)
            return cp

        state = compute_concept_mastery(
            "python.variables", challenge_concepts, get_prog
        )
        # 2/3 passing ≈ 67% -> DEVELOPING (40–70%)
        assert state.mastery == ConceptMastery.DEVELOPING
        assert state.passing_challenges == 2

    def test_regression_detected(self):
        """Regressed challenges -> concept REGRESSED."""
        challenge_concepts = {
            "01.01.1": ["python.variables"],
            "01.01.2": ["python.variables"],
        }

        def get_prog(cid):
            cp = MagicMock()
            cp.state = (
                ChallengeState.REGRESSED
                if cid == "01.01.1"
                else ChallengeState.MASTERED
            )
            return cp

        state = compute_concept_mastery(
            "python.variables", challenge_concepts, get_prog
        )
        assert state.mastery == ConceptMastery.REGRESSED
        assert state.regressed_challenges == 1


# ── get_weak_concepts ──


class TestGetWeakConcepts:
    def test_returns_weak_and_regressed(self):
        states = {
            "a": ConceptState("a", mastery=ConceptMastery.WEAK, score=0.2),
            "b": ConceptState("b", mastery=ConceptMastery.MASTERED, score=1.0),
            "c": ConceptState("c", mastery=ConceptMastery.REGRESSED, score=0.5),
        }
        weak = get_weak_concepts(states)
        assert len(weak) == 2
        # REGRESSED should come first
        assert weak[0].concept_id == "c"
        assert weak[1].concept_id == "a"

    def test_empty_states(self):
        assert get_weak_concepts({}) == []


# ── get_ready_concepts ──


class TestGetReadyConcepts:
    @patch("engine.concepts.load_concept_graph")
    def test_ready_with_met_prereqs(self, mock_graph):
        graph = _make_mock_graph()
        mock_graph.return_value = graph

        states = {
            "python.variables": ConceptState(
                "python.variables", mastery=ConceptMastery.MASTERED
            ),
            "python.types": ConceptState(
                "python.types", mastery=ConceptMastery.NOT_SEEN
            ),
            "python.conditions": ConceptState(
                "python.conditions", mastery=ConceptMastery.NOT_SEEN
            ),
            "python.loops": ConceptState(
                "python.loops", mastery=ConceptMastery.NOT_SEEN
            ),
            "python.functions": ConceptState(
                "python.functions", mastery=ConceptMastery.NOT_SEEN
            ),
        }
        ready = get_ready_concepts(states)
        # python.types has prereq python.variables which is MASTERED -> ready
        assert "python.types" in ready
        # python.conditions has prereq python.types which is NOT_SEEN -> NOT ready
        assert "python.conditions" not in ready


# ── check_prerequisites_met ──


class TestCheckPrerequisitesMet:
    @patch("engine.concepts.load_concept_graph")
    def test_all_met(self, mock_graph):
        mock_graph.return_value = _make_mock_graph()
        states = {
            "python.variables": ConceptState(
                "python.variables", mastery=ConceptMastery.PROFICIENT
            ),
            "python.types": ConceptState(
                "python.types", mastery=ConceptMastery.DEVELOPING
            ),
        }
        met, missing = check_prerequisites_met("python.functions", states)
        assert met is True
        assert missing == []

    @patch("engine.concepts.load_concept_graph")
    def test_missing_prereq(self, mock_graph):
        mock_graph.return_value = _make_mock_graph()
        states = {
            "python.variables": ConceptState(
                "python.variables", mastery=ConceptMastery.MASTERED
            ),
            "python.types": ConceptState("python.types", mastery=ConceptMastery.WEAK),
        }
        met, missing = check_prerequisites_met("python.functions", states)
        assert met is False
        assert "python.types" in missing


# ── get_all_prerequisites ──


class TestGetAllPrerequisites:
    @patch("engine.concepts.load_concept_graph")
    def test_transitive(self, mock_graph):
        mock_graph.return_value = _make_mock_graph()
        prereqs = get_all_prerequisites("python.loops")
        # loops -> conditions -> types -> variables
        assert "python.conditions" in prereqs
        assert "python.types" in prereqs
        assert "python.variables" in prereqs


# ── get_dependents ──


class TestGetDependents:
    @patch("engine.concepts.load_concept_graph")
    def test_dependents(self, mock_graph):
        mock_graph.return_value = _make_mock_graph()
        deps = get_dependents("python.variables")
        assert "python.types" in deps
        assert "python.functions" in deps


# ── get_concept_summary ──


class TestGetConceptSummary:
    def test_summary_counts(self):
        states = {
            "a": ConceptState("a", mastery=ConceptMastery.MASTERED),
            "b": ConceptState("b", mastery=ConceptMastery.MASTERED),
            "c": ConceptState("c", mastery=ConceptMastery.WEAK),
            "d": ConceptState("d", mastery=ConceptMastery.NOT_SEEN),
        }
        summary = get_concept_summary(states)
        assert summary["mastered"] == 2
        assert summary["weak"] == 1
        assert summary["not_seen"] == 1
