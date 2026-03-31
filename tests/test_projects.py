"""Tests for the project-based progression module (engine/projects.py)."""

import pytest
from unittest.mock import patch

from engine.projects import (
    ProjectDefinition,
    ProjectDifficulty,
    Milestone,
    ProjectProgress,
    load_projects,
    get_project,
    get_projects_for_section,
    get_available_projects,
)
from engine.concepts import ConceptMastery, ConceptState


# ── load_projects ──


class TestLoadProjects:
    def test_loads_from_yaml(self):
        """Should load project definitions from projects.yaml."""
        import engine.projects as proj_mod

        proj_mod._projects_cache = None

        projects = load_projects()
        assert isinstance(projects, dict)
        if projects:
            for pid, proj in projects.items():
                assert isinstance(proj, ProjectDefinition)
                assert proj.id == pid
                assert proj.title

    def test_project_has_milestones(self):
        """Each project should have at least one milestone."""
        projects = load_projects()
        for pid, proj in projects.items():
            assert len(proj.milestones) > 0, f"{pid} has no milestones"
            for m in proj.milestones:
                assert isinstance(m, Milestone)
                assert m.title


# ── get_project ──


class TestGetProject:
    def test_existing_project(self):
        projects = load_projects()
        if projects:
            first_id = next(iter(projects))
            proj = get_project(first_id)
            assert proj is not None
            assert proj.id == first_id

    def test_nonexistent(self):
        assert get_project("nonexistent_project_xyz") is None


# ── ProjectProgress ──


class TestProjectProgress:
    def test_incomplete(self):
        pp = ProjectProgress(
            project_id="test",
            milestone_states={1: "completed", 2: "not_started"},
        )
        assert not pp.is_complete
        assert pp.completion_pct == 0.5

    def test_complete(self):
        pp = ProjectProgress(
            project_id="test",
            milestone_states={1: "completed", 2: "reviewed"},
        )
        assert pp.is_complete
        assert pp.completion_pct == 1.0

    def test_empty(self):
        pp = ProjectProgress(project_id="test")
        assert pp.completion_pct == 0.0


# ── get_available_projects ──


class TestGetAvailableProjects:
    def test_no_prereqs_all_available(self):
        """Projects with no prerequisites are always available."""
        projects = load_projects()
        no_prereq_projects = [
            p for p in projects.values() if not p.prerequisite_concepts
        ]
        # With empty concept states, projects without prereqs should be available
        available = get_available_projects({})
        available_ids = {p.id for p in available}
        for p in no_prereq_projects:
            assert p.id in available_ids

    def test_prereqs_not_met(self):
        """Projects with unmet prereqs should not be available."""
        # Give all concepts NOT_SEEN state
        states = {
            "python.variables": ConceptState(
                "python.variables", mastery=ConceptMastery.NOT_SEEN
            ),
            "python.functions": ConceptState(
                "python.functions", mastery=ConceptMastery.NOT_SEEN
            ),
        }
        available = get_available_projects(states)
        # All projects requiring these concepts should be excluded
        for p in available:
            for prereq in p.prerequisite_concepts:
                if prereq in states:
                    assert states[prereq].mastery not in (
                        ConceptMastery.NOT_SEEN,
                        ConceptMastery.WEAK,
                    )
