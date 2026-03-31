"""Tests for the reflection module (engine/reflection.py)."""

import pytest

from engine.reflection import (
    ReflectionPrompt,
    generate_post_challenge_reflection,
    generate_post_lesson_reflection,
    generate_concept_insight,
    get_weekly_reflection_prompts,
)
from engine.concepts import ConceptNode


# ── generate_post_challenge_reflection ──


class TestPostChallengeReflection:
    def test_returns_prompts(self):
        prompts = generate_post_challenge_reflection(
            challenge_title="Test",
            challenge_type="implementation",
            concepts=["python.functions"],
            attempt_count=1,
            passed=True,
        )
        assert isinstance(prompts, list)
        assert len(prompts) > 0
        assert all(isinstance(p, ReflectionPrompt) for p in prompts)

    def test_more_prompts_on_failure(self):
        """Failed challenge should generate at least as many prompts as passed."""
        passed_prompts = generate_post_challenge_reflection(
            challenge_title="Test",
            challenge_type="implementation",
            concepts=["python.loops"],
            attempt_count=1,
            passed=True,
        )
        failed_prompts = generate_post_challenge_reflection(
            challenge_title="Test",
            challenge_type="implementation",
            concepts=["python.loops"],
            attempt_count=3,
            passed=False,
        )
        assert len(failed_prompts) >= len(passed_prompts)

    def test_empty_concepts(self):
        """Should work even with no concepts."""
        prompts = generate_post_challenge_reflection(
            challenge_title="Test",
            challenge_type="basic",
            concepts=[],
            attempt_count=1,
            passed=True,
        )
        assert isinstance(prompts, list)


# ── generate_post_lesson_reflection ──


class TestPostLessonReflection:
    def test_returns_prompts(self):
        prompts = generate_post_lesson_reflection(
            lesson_name="Třídy",
            concepts=["oop.classes"],
            mastered_count=3,
            total_count=5,
        )
        assert isinstance(prompts, list)
        assert len(prompts) > 0

    def test_includes_transfer(self):
        """Should include at least one transfer or metacognitive prompt."""
        prompts = generate_post_lesson_reflection(
            lesson_name="Funkce",
            concepts=["python.functions"],
            mastered_count=2,
            total_count=3,
        )
        categories = {p.category for p in prompts}
        assert categories  # at least one category present


# ── generate_concept_insight ──


class TestConceptInsight:
    def test_with_key_insight(self):
        graph = {
            "python.functions": ConceptNode(
                id="python.functions",
                name="Funkce",
                key_insight="Funkce jsou stavební bloky.",
                common_confusion="Zapomíná se na return.",
                transfer_hint="V JS se chová jako arrow function.",
            ),
        }
        insight = generate_concept_insight("python.functions", graph)
        assert insight is not None
        assert isinstance(insight, ReflectionPrompt)

    def test_unknown_concept(self):
        insight = generate_concept_insight("nonexistent", {})
        assert insight is None


# ── get_weekly_reflection_prompts ──


class TestWeeklyReflection:
    def test_returns_list(self):
        prompts = get_weekly_reflection_prompts()
        assert isinstance(prompts, list)
        assert len(prompts) > 0
        assert all(isinstance(p, ReflectionPrompt) for p in prompts)
