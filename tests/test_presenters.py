"""Tests for engine.presenters — pure formatting functions."""
import unittest

from engine.models import ChallengeState, ChallengeType, AttemptRecord
from engine.presenters import (
    progress_bar, state_icon, state_label, type_label,
    category_label, difficulty_stars,
    format_stats_bar, format_state_breakdown,
    format_mastery_indicator, format_session_assessment,
    format_lesson_rank,
)
from engine.recommend import ActionCategory


class TestProgressBar(unittest.TestCase):

    def test_zero_pct(self):
        result = progress_bar(0.0, 10)
        self.assertIn("░" * 10, result)
        self.assertIn("0%", result)

    def test_full_pct(self):
        result = progress_bar(1.0, 10)
        self.assertIn("█" * 10, result)
        self.assertIn("100%", result)

    def test_half_pct(self):
        result = progress_bar(0.5, 10)
        self.assertIn("█" * 5, result)

    def test_color_green_high(self):
        result = progress_bar(0.9)
        self.assertIn("green", result)

    def test_color_yellow_mid(self):
        result = progress_bar(0.5)
        self.assertIn("yellow", result)


class TestStateFormatters(unittest.TestCase):

    def test_state_icon_all_states(self):
        for state in ChallengeState:
            icon = state_icon(state)
            self.assertIsInstance(icon, str)
            self.assertTrue(len(icon) > 0)

    def test_state_label_all_states(self):
        for state in ChallengeState:
            label = state_label(state)
            self.assertIsInstance(label, str)
            self.assertTrue(len(label) > 0)

    def test_type_label_all_types(self):
        for ctype in ChallengeType:
            label = type_label(ctype)
            self.assertIsInstance(label, str)
            self.assertTrue(len(label) > 0)


class TestCategoryLabel(unittest.TestCase):

    def test_all_categories(self):
        for cat in ActionCategory:
            label = category_label(cat)
            self.assertIsInstance(label, str)
            self.assertTrue(len(label) > 0)


class TestDifficultyStars(unittest.TestCase):

    def test_difficulty_1(self):
        self.assertEqual(difficulty_stars(1), "⭐☆☆")

    def test_difficulty_3(self):
        self.assertEqual(difficulty_stars(3), "⭐⭐⭐")


class TestFormatMasteryIndicator(unittest.TestCase):

    def test_mastered_state(self):
        result = format_mastery_indicator(
            ChallengeState.MASTERED,
            [AttemptRecord(at="2024-01-01", passed=True)] * 3,
        )
        self.assertIn("Zvládnuto", result)

    def test_currently_passing_shows_progress(self):
        attempts = [
            AttemptRecord(at="2024-01-01", passed=True),
            AttemptRecord(at="2024-01-02", passed=True),
        ]
        result = format_mastery_indicator(
            ChallengeState.CURRENTLY_PASSING, attempts)
        self.assertIn("2/3", result)

    def test_not_started_empty(self):
        result = format_mastery_indicator(ChallengeState.NOT_STARTED, [])
        self.assertEqual(result, "")


class TestSessionAssessment(unittest.TestCase):

    def test_high_score(self):
        result = format_session_assessment(10, 9)
        self.assertIn("Výborné", result)

    def test_medium_score(self):
        result = format_session_assessment(10, 6)
        self.assertIn("Dobrá", result)

    def test_low_score(self):
        result = format_session_assessment(10, 2)
        self.assertIn("Nevzdávej", result)

    def test_zero_attempts(self):
        self.assertEqual(format_session_assessment(0, 0), "")


class TestLessonRank(unittest.TestCase):

    def test_perfect(self):
        result = format_lesson_rank(1.0)
        self.assertIn("PERFEKTNÍ", result)

    def test_good(self):
        result = format_lesson_rank(0.7)
        self.assertIn("Skvělé", result)

    def test_start(self):
        result = format_lesson_rank(0.4)
        self.assertIn("Dobrý", result)

    def test_new(self):
        result = format_lesson_rank(0.1)
        self.assertIn("Pokračuj", result)


if __name__ == "__main__":
    unittest.main()
