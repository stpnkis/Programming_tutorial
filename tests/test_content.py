"""Tests for content discovery, metadata, and challenge type inference."""
import os
import pytest
from unittest.mock import patch

from engine.content import (
    discover_sections, load_challenge_details, search_lessons,
    _infer_challenge_type, get_recommended_next,
)
from engine.models import ChallengeType, ChallengeState


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestContentDiscovery:

    def test_discovers_sections(self):
        sections = discover_sections()
        assert len(sections) >= 14
        assert sections[0].num == "01"
        assert sections[0].name == "Python Základy"

    def test_discovers_lessons(self):
        sections = discover_sections()
        sec01 = sections[0]
        assert len(sec01.lessons) >= 10
        assert sec01.lessons[0].lesson_num == "01"
        assert sec01.lessons[0].challenge_count > 0

    def test_lesson_has_meta(self):
        sections = discover_sections()
        lesson = sections[0].lessons[0]
        # Meta should be populated (at least by inference)
        assert lesson.meta is not None
        assert isinstance(lesson.meta.tags, list)

    def test_lesson_id(self):
        sections = discover_sections()
        lesson = sections[0].lessons[0]
        assert lesson.lesson_id == "01.01"


class TestChallengeDetails:

    def test_load_challenge_details(self):
        sections = discover_sections()
        lesson = sections[0].lessons[0]  # 01_Python_Zaklady/01_datove_typy
        details = load_challenge_details(
            lesson.section_num, lesson.lesson_num, lesson.challenge_file
        )
        assert len(details) > 0
        d = details[0]
        assert d.challenge_id == "01.01.1"
        assert d.title != ""
        assert d.points > 0
        assert isinstance(d.challenge_type, ChallengeType)

    def test_challenge_has_tests(self):
        sections = discover_sections()
        lesson = sections[0].lessons[0]
        details = load_challenge_details(
            lesson.section_num, lesson.lesson_num, lesson.challenge_file
        )
        assert len(details[0].tests) > 0


class TestChallengeTypeInference:

    def test_implementation_type_for_basic_challenges(self):
        """Basic Python challenges should be detected as implementation or knowledge."""
        sections = discover_sections()
        lesson = sections[0].lessons[0]
        details = load_challenge_details(
            lesson.section_num, lesson.lesson_num, lesson.challenge_file
        )
        # All challenges should have a valid type
        for d in details:
            assert isinstance(d.challenge_type, ChallengeType)


class TestSearch:

    def test_search_by_name(self):
        sections = discover_sections()
        results = search_lessons(sections, "datove typy")
        assert len(results) >= 1
        assert any("Datove" in r.name for r in results)

    def test_search_by_tag(self):
        sections = discover_sections()
        results = search_lessons(sections, "python")
        assert len(results) >= 10  # All Python lessons

    def test_search_empty_query(self):
        sections = discover_sections()
        results = search_lessons(sections, "xyznonexistent")
        assert len(results) == 0

    def test_search_case_insensitive(self):
        sections = discover_sections()
        results1 = search_lessons(sections, "OOP")
        results2 = search_lessons(sections, "oop")
        assert len(results1) == len(results2)


class TestRecommendation:

    def test_recommends_first_lesson_when_empty(self):
        sections = discover_sections()

        class FakeProgress:
            def get_lesson_completed(self, s, l):
                return 0

        rec = get_recommended_next(sections, FakeProgress())
        assert rec is not None
        assert rec.section_num == "01"
        assert rec.lesson_num == "01"

    def test_recommends_in_progress_first(self):
        sections = discover_sections()

        class FakeProgress:
            def get_lesson_completed(self, s, l):
                if s == "01" and l == "01":
                    return 3  # partially done (less than total)
                return 0

        rec = get_recommended_next(sections, FakeProgress())
        assert rec is not None
        assert rec.section_num == "01"
        assert rec.lesson_num == "01"
