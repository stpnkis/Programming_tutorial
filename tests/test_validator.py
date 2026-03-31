"""Tests for engine.validator — validation and quality scoring."""
import unittest
import tempfile
import os

from engine.validator import (
    ValidationResult, LessonQuality,
    validate_challenges_file, validate_lesson_yaml,
    validate_all, format_quality_report,
    CHALLENGE_SCHEMA,
)


class TestLessonQuality(unittest.TestCase):
    """Test quality scoring logic."""

    def test_empty_quality_score_zero(self):
        q = LessonQuality(path="test")
        self.assertEqual(q.score, 0.0)
        self.assertEqual(q.grade, "F")

    def test_full_quality(self):
        q = LessonQuality(
            path="test",
            has_challenges=True,
            has_yaml=True,
            has_summary=True,
            has_quality_summary=True,
            has_learning_objectives=True,
            has_tags=True,
            challenge_count=5,
            challenges_with_hints=5,
            challenges_with_quality_hints=5,
            challenges_with_objectives=5,
            challenges_with_misconceptions=5,
            challenges_with_tests=5,
            func_body_quality=5,
            type_diversity=3,
            has_why_it_matters=True,
            has_what_you_will_learn=True,
            has_key_theory=True,
            challenges_with_worked_example=5,
            challenges_with_thinking_notes=5,
            challenges_with_reference_solution=5,
            challenges_with_common_mistakes=5,
            challenges_with_solution_explanation=5,
            has_lesson_summary=True,
            has_recommended_next=True,
            has_before_you_code=True,
            has_reasoning_task=True,
            has_independent_task=True,
        )
        self.assertEqual(q.score, 100.0)
        self.assertEqual(q.grade, "A")

    def test_grade_boundaries(self):
        q = LessonQuality(path="test")
        # Grade D: 20-39
        q.has_challenges = True   # +10
        q.has_yaml = True         # +10
        self.assertIn(q.grade, ("C", "D"))  # 20pts

    def test_partial_hints(self):
        q = LessonQuality(
            path="test",
            has_challenges=True,
            has_yaml=True,
            challenge_count=10,
            challenges_with_quality_hints=5,
        )
        # partial hints should give partial score
        self.assertGreater(q.score, 20)  # has base + partial hints


class TestValidateChallengesFile(unittest.TestCase):

    def _write_temp(self, content):
        fd, path = tempfile.mkstemp(suffix=".py")
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return path

    def test_valid_file(self):
        content = '''\
from engine.models import Challenge

def vyzva_1():
    return 42

challenges = [
    Challenge(
        title="Test",
        tests=[lambda: (True, "ok")]
    ),
]
'''
        path = self._write_temp(content)
        try:
            result = ValidationResult()
            quality = LessonQuality(path="test")
            validate_challenges_file(path, result, quality)
            self.assertEqual(len(result.errors), 0)
            self.assertTrue(quality.has_challenges)
            self.assertEqual(quality.challenge_count, 1)
        finally:
            os.unlink(path)

    def test_missing_file(self):
        result = ValidationResult()
        validate_challenges_file("/nonexistent/file.py", result)
        self.assertEqual(len(result.errors), 1)

    def test_no_challenges(self):
        path = self._write_temp("# empty file\nx = 1\n")
        try:
            result = ValidationResult()
            validate_challenges_file(path, result)
            self.assertEqual(len(result.errors), 1)
        finally:
            os.unlink(path)

    def test_quality_body_detection(self):
        content = '''\
from engine.models import Challenge

def vyzva_1():
    x = 42
    return x * 2

def vyzva_2():
    pass

challenges = [
    Challenge(title="Real"),
    Challenge(title="Skeleton"),
]
'''
        path = self._write_temp(content)
        try:
            result = ValidationResult()
            quality = LessonQuality(path="test")
            validate_challenges_file(path, result, quality)
            # vyzva_1 has real body, vyzva_2 is skeleton
            self.assertEqual(quality.func_body_quality, 1)
        finally:
            os.unlink(path)


class TestValidateLessonYaml(unittest.TestCase):

    def _write_yaml(self, content):
        fd, path = tempfile.mkstemp(suffix=".yaml")
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return path

    def test_valid_yaml(self):
        yaml_content = '''\
id: "01.01"
title: "Test Lesson"
summary: "A test"
tags: [python]
learning_objectives: ["Learn basics"]
challenges:
  - id: 1
    title: "Challenge 1"
    type: implementation
'''
        path = self._write_yaml(yaml_content)
        try:
            result = ValidationResult()
            quality = LessonQuality(path="test")
            validate_lesson_yaml(path, "/fake/challenges.py", result, quality)
            self.assertEqual(len(result.errors), 0)
            self.assertTrue(quality.has_yaml)
            self.assertTrue(quality.has_summary)
            self.assertTrue(quality.has_learning_objectives)
            self.assertTrue(quality.has_tags)
        finally:
            os.unlink(path)

    def test_missing_required_field(self):
        yaml_content = 'summary: "no id or title"\n'
        path = self._write_yaml(yaml_content)
        try:
            result = ValidationResult()
            validate_lesson_yaml(path, "/fake", result)
            # Should have errors for missing id and title
            self.assertGreater(len(result.errors), 0)
        finally:
            os.unlink(path)

    def test_invalid_hint_strategy(self):
        yaml_content = '''\
id: "01.01"
title: "Test"
challenges:
  - id: 1
    title: "C1"
    hint_strategy: unknown_strategy
'''
        path = self._write_yaml(yaml_content)
        try:
            result = ValidationResult()
            validate_lesson_yaml(path, "/fake", result)
            warns = [w for w in result.warnings if "hint_strategy" in w]
            self.assertEqual(len(warns), 1)
        finally:
            os.unlink(path)

    def test_invalid_review_priority(self):
        yaml_content = '''\
id: "01.01"
title: "Test"
challenges:
  - id: 1
    title: "C1"
    review_priority: super_high
'''
        path = self._write_yaml(yaml_content)
        try:
            result = ValidationResult()
            validate_lesson_yaml(path, "/fake", result)
            warns = [w for w in result.warnings if "review_priority" in w]
            self.assertEqual(len(warns), 1)
        finally:
            os.unlink(path)

    def test_type_diversity_tracking(self):
        yaml_content = '''\
id: "01.01"
title: "Test"
challenges:
  - id: 1
    title: "C1"
    type: implementation
  - id: 2
    title: "C2"
    type: debugging
  - id: 3
    title: "C3"
    type: knowledge
'''
        path = self._write_yaml(yaml_content)
        try:
            result = ValidationResult()
            quality = LessonQuality(path="test")
            validate_lesson_yaml(path, "/fake", result, quality)
            self.assertEqual(quality.type_diversity, 3)
        finally:
            os.unlink(path)


class TestValidateAll(unittest.TestCase):

    def test_validate_all_returns_result(self):
        result = validate_all()
        self.assertIsInstance(result, ValidationResult)
        self.assertEqual(len(result.errors), 0)
        self.assertGreater(len(result.quality), 0)


class TestFormatQualityReport(unittest.TestCase):

    def test_report_format(self):
        result = ValidationResult()
        result.quality.append(LessonQuality(
            path="01_Test/01_lesson",
            section_num="01",
            lesson_num="01",
            has_challenges=True,
            has_yaml=True,
            challenge_count=3,
        ))
        report = format_quality_report(result)
        self.assertIn("QUALITY REPORT", report)
        self.assertIn("01.01", report)
        self.assertIn("Section Averages", report)
        self.assertIn("Overall", report)


class TestChallengeSchema(unittest.TestCase):

    def test_new_fields_in_schema(self):
        self.assertIn("hint_strategy", CHALLENGE_SCHEMA["optional"])
        self.assertIn("review_priority", CHALLENGE_SCHEMA["optional"])
        self.assertIn("learning_objective", CHALLENGE_SCHEMA["optional"])
        self.assertIn("tags", CHALLENGE_SCHEMA["optional"])
        self.assertIn("estimated_minutes", CHALLENGE_SCHEMA["optional"])

    def test_new_pillar_b_fields(self):
        self.assertIn("expected_misconceptions", CHALLENGE_SCHEMA["optional"])
        self.assertIn("mastery_rule", CHALLENGE_SCHEMA["optional"])
        self.assertIn("solution_pattern", CHALLENGE_SCHEMA["optional"])


class TestQAReport(unittest.TestCase):

    def test_qa_report_runs(self):
        from engine.validator import format_qa_report, ValidationResult
        result = ValidationResult()
        result.quality.append(LessonQuality(
            path="01_Test/01_lesson",
            section_num="01",
            lesson_num="01",
            has_challenges=True,
            has_yaml=True,
            challenge_count=3,
        ))
        report = format_qa_report(result)
        self.assertIsInstance(report, str)
        self.assertIn("01.01", report)

    def test_three_tier_scoring(self):
        q = LessonQuality(
            path="test",
            has_challenges=True,    # +10 structure
            has_yaml=True,          # +10 structure
            challenge_count=5,
            challenges_with_tests=5,  # +10 structure
        )
        self.assertEqual(q.structure_score, 30.0)
        self.assertEqual(q.metadata_score, 0.0)
        self.assertEqual(q.pedagogy_score, 0.0)
        self.assertEqual(q.score, 30.0)


if __name__ == "__main__":
    unittest.main()
