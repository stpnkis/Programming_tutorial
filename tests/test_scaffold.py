"""Tests for engine.scaffold_concepts — concept auto-tagging tool."""

import os
import tempfile
import pytest
import yaml

from engine.scaffold_concepts import (
    suggest_concepts_for_lesson,
    scaffold,
    _build_tag_to_concepts,
)
from engine.concepts import load_concept_graph


class TestSuggestConcepts:
    """Verify concept suggestion logic."""

    def test_suggest_from_tags(self, tmp_path):
        """Tags like 'strings' should suggest python.strings."""
        yaml_path = tmp_path / "lesson.yaml"
        yaml_path.write_text(
            yaml.dump({"name": "Test", "tags": ["strings", "formatting"]}),
            encoding="utf-8",
        )
        graph = load_concept_graph()
        lookup = _build_tag_to_concepts(graph)
        existing, suggested = suggest_concepts_for_lesson(str(yaml_path), graph, lookup)
        assert len(existing) == 0
        assert "python.strings" in suggested or "python.string_methods" in suggested

    def test_existing_concepts_not_re_suggested(self, tmp_path):
        """Concepts already listed should not appear in suggested."""
        yaml_path = tmp_path / "lesson.yaml"
        yaml_path.write_text(
            yaml.dump(
                {
                    "name": "Test",
                    "tags": ["strings"],
                    "concepts": ["python.strings"],
                }
            ),
            encoding="utf-8",
        )
        graph = load_concept_graph()
        lookup = _build_tag_to_concepts(graph)
        existing, suggested = suggest_concepts_for_lesson(str(yaml_path), graph, lookup)
        assert "python.strings" in existing
        assert "python.strings" not in suggested

    def test_empty_tags(self, tmp_path):
        """Lesson with no tags should still work."""
        yaml_path = tmp_path / "lesson.yaml"
        yaml_path.write_text(yaml.dump({"name": "Test"}), encoding="utf-8")
        graph = load_concept_graph()
        lookup = _build_tag_to_concepts(graph)
        existing, suggested = suggest_concepts_for_lesson(str(yaml_path), graph, lookup)
        assert isinstance(existing, list)
        assert isinstance(suggested, list)


class TestScaffoldIntegration:
    """Integration test — scaffold reads real lesson.yaml files."""

    def test_scaffold_runs_without_crash(self):
        """Scaffold should run across the whole repo without errors."""
        report = scaffold(section_filter="", apply=False)
        assert isinstance(report, dict)
        assert len(report) > 0

    def test_scaffold_section_filter(self):
        """Section filter should limit results."""
        full = scaffold(section_filter="", apply=False)
        s01 = scaffold(section_filter="01", apply=False)
        assert len(s01) <= len(full)
        for path in s01:
            assert path.startswith("01_")
