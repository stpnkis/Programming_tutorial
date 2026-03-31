"""
🏗️ Project-Based Progression — mini-projects, milestones, rubrics.

Provides:
- Project definitions with milestones and rubrics
- Project ↔ concept mappings
- Milestone tracking and evaluation
- Project reflection prompts
- Project scaffolding
"""

from __future__ import annotations

import os
import yaml
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_FILE = os.path.join(ROOT, "engine", "projects.yaml")


class ProjectDifficulty(Enum):
    MINI = "mini"  # 30-60 min, 1-2 concepts
    STANDARD = "standard"  # 2-4 hours, 3-5 concepts
    CAPSTONE = "capstone"  # 6+ hours, cross-section concepts


class MilestoneState(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REVIEWED = "reviewed"


@dataclass
class Milestone:
    """A single milestone within a project."""

    id: int
    title: str
    description: str = ""
    criteria: List[str] = field(default_factory=list)
    concepts: List[str] = field(default_factory=list)
    hints: List[str] = field(default_factory=list)
    estimated_minutes: int = 15


@dataclass
class ProjectDefinition:
    """Complete project definition."""

    id: str  # e.g. "proj_01_calculator"
    title: str
    summary: str = ""
    difficulty: ProjectDifficulty = ProjectDifficulty.MINI
    section: str = ""  # related section number
    prerequisite_concepts: List[str] = field(default_factory=list)
    concepts_practiced: List[str] = field(default_factory=list)
    milestones: List[Milestone] = field(default_factory=list)
    rubric: List[str] = field(default_factory=list)  # done criteria
    starter_code: str = ""
    reflection_prompts: List[str] = field(default_factory=list)
    estimated_minutes: int = 60
    learning_goals: List[str] = field(default_factory=list)


@dataclass
class ProjectProgress:
    """Tracks a student's progress through a project."""

    project_id: str
    milestone_states: Dict[int, str] = field(default_factory=dict)
    started_at: str = ""
    completed_at: str = ""
    reflections: Dict[str, str] = field(default_factory=dict)  # prompt → answer

    @property
    def is_complete(self) -> bool:
        return all(
            v in ("completed", "reviewed") for v in self.milestone_states.values()
        )

    @property
    def completion_pct(self) -> float:
        if not self.milestone_states:
            return 0.0
        done = sum(
            1 for v in self.milestone_states.values() if v in ("completed", "reviewed")
        )
        return done / len(self.milestone_states)


# ── Project loading ──

_projects_cache: Optional[Dict[str, ProjectDefinition]] = None


def load_projects() -> Dict[str, ProjectDefinition]:
    """Load project definitions from projects.yaml."""
    global _projects_cache
    if _projects_cache is not None:
        return _projects_cache

    if not os.path.isfile(PROJECTS_FILE):
        _projects_cache = {}
        return _projects_cache

    with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    projects: Dict[str, ProjectDefinition] = {}
    for pid, data in raw.get("projects", {}).items():
        milestones = []
        for i, m in enumerate(data.get("milestones", []), 1):
            milestones.append(
                Milestone(
                    id=i,
                    title=m.get("title", f"Milestone {i}"),
                    description=m.get("description", ""),
                    criteria=m.get("criteria", []),
                    concepts=m.get("concepts", []),
                    hints=m.get("hints", []),
                    estimated_minutes=m.get("estimated_minutes", 15),
                )
            )

        diff = data.get("difficulty", "mini")
        try:
            difficulty = ProjectDifficulty(diff)
        except ValueError:
            difficulty = ProjectDifficulty.MINI

        projects[pid] = ProjectDefinition(
            id=pid,
            title=data.get("title", pid),
            summary=data.get("summary", ""),
            difficulty=difficulty,
            section=str(data.get("section", "")),
            prerequisite_concepts=data.get("prerequisite_concepts", []),
            concepts_practiced=data.get("concepts_practiced", []),
            milestones=milestones,
            rubric=data.get("rubric", []),
            starter_code=data.get("starter_code", ""),
            reflection_prompts=data.get("reflection_prompts", []),
            estimated_minutes=data.get("estimated_minutes", 60),
            learning_goals=data.get("learning_goals", []),
        )

    _projects_cache = projects
    return _projects_cache


def get_project(project_id: str) -> Optional[ProjectDefinition]:
    return load_projects().get(project_id)


def get_projects_for_section(section_num: str) -> List[ProjectDefinition]:
    return [p for p in load_projects().values() if p.section == section_num]


def get_available_projects(concept_states: Dict) -> List[ProjectDefinition]:
    """Projects whose prerequisites are met."""
    from engine.concepts import ConceptMastery

    available = []
    for p in load_projects().values():
        prereqs_met = True
        for prereq in p.prerequisite_concepts:
            state = concept_states.get(prereq)
            if not state or state.mastery in (
                ConceptMastery.NOT_SEEN,
                ConceptMastery.WEAK,
            ):
                prereqs_met = False
                break
        if prereqs_met:
            available.append(p)
    return available
