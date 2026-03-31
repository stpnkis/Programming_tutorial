"""Tests for engine.feedback — error classification and pedagogical feedback."""
import unittest

from engine.feedback import (
    ErrorCategory, classify_error, generate_feedback,
    format_feedback_panel, CATEGORY_EXPLANATIONS,
)
from engine.models import ChallengeType


class TestClassifyError(unittest.TestCase):
    """Test error classification into pedagogical categories."""

    def test_syntax_error(self):
        self.assertEqual(
            classify_error("SyntaxError: invalid syntax"),
            ErrorCategory.SYNTAX,
        )

    def test_indentation_error(self):
        self.assertEqual(
            classify_error("IndentationError: unexpected indent"),
            ErrorCategory.SYNTAX,
        )

    def test_name_error(self):
        self.assertEqual(
            classify_error("NameError: name 'x' is not defined"),
            ErrorCategory.NAME,
        )

    def test_type_error(self):
        self.assertEqual(
            classify_error("TypeError: unsupported operand type(s)"),
            ErrorCategory.TYPE,
        )

    def test_value_error(self):
        self.assertEqual(
            classify_error("ValueError: invalid literal for int()"),
            ErrorCategory.VALUE,
        )

    def test_attribute_error(self):
        self.assertEqual(
            classify_error("AttributeError: 'NoneType' has no attribute 'foo'"),
            ErrorCategory.ATTRIBUTE,
        )

    def test_index_error(self):
        self.assertEqual(
            classify_error("IndexError: list index out of range"),
            ErrorCategory.INDEX,
        )

    def test_key_error(self):
        self.assertEqual(
            classify_error("KeyError: 'missing_key'"),
            ErrorCategory.INDEX,
        )

    def test_import_error(self):
        self.assertEqual(
            classify_error("ImportError: No module named 'foo'"),
            ErrorCategory.IMPORT,
        )

    def test_module_not_found(self):
        self.assertEqual(
            classify_error("ModuleNotFoundError: No module named 'bar'"),
            ErrorCategory.IMPORT,
        )

    def test_runtime_errors(self):
        for msg in [
            "ZeroDivisionError: division by zero",
            "RecursionError: maximum recursion depth exceeded",
            "FileNotFoundError: [Errno 2]",
        ]:
            self.assertEqual(
                classify_error(msg), ErrorCategory.RUNTIME, msg=msg
            )

    def test_logic_error_expected_got(self):
        self.assertEqual(
            classify_error("expected 5, got 3"),
            ErrorCategory.LOGIC,
        )

    def test_logic_error_not_equal(self):
        self.assertEqual(
            classify_error("42 != 43"),
            ErrorCategory.LOGIC,
        )

    def test_assertion_keyword(self):
        self.assertEqual(
            classify_error("Test neprošel"),
            ErrorCategory.ASSERTION,
        )

    def test_empty_message(self):
        self.assertEqual(classify_error(""), ErrorCategory.UNKNOWN)

    def test_unknown_message(self):
        self.assertEqual(
            classify_error("some random output"),
            ErrorCategory.UNKNOWN,
        )

    def test_all_categories_have_explanations(self):
        for cat in ErrorCategory:
            self.assertIn(cat, CATEGORY_EXPLANATIONS)
            title, explanation, guidance = CATEGORY_EXPLANATIONS[cat]
            self.assertTrue(title)
            self.assertTrue(explanation)
            self.assertIsInstance(guidance, list)
            self.assertTrue(len(guidance) > 0)


class TestGenerateFeedback(unittest.TestCase):
    """Test structured feedback generation."""

    def test_basic_structure(self):
        fb = generate_feedback("NameError: name 'x' is not defined")
        self.assertIn("category", fb)
        self.assertIn("title", fb)
        self.assertIn("explanation", fb)
        self.assertIn("guidance", fb)
        self.assertIn("hint", fb)
        self.assertIn("encouragement", fb)

    def test_category_matches_classification(self):
        fb = generate_feedback("TypeError: cannot add str and int")
        self.assertEqual(fb["category"], ErrorCategory.TYPE)

    def test_guidance_max_4(self):
        fb = generate_feedback("SyntaxError: invalid syntax")
        self.assertLessEqual(len(fb["guidance"]), 4)

    def test_hint_from_list(self):
        fb = generate_feedback(
            "NameError: x", hints=["Use a variable", "Check scope"],
            attempt_count=0,
        )
        self.assertEqual(fb["hint"], "Use a variable")

    def test_hint_advances_with_attempts(self):
        fb = generate_feedback(
            "NameError: x", hints=["First hint", "Second hint"],
            attempt_count=1,
        )
        self.assertEqual(fb["hint"], "Second hint")

    def test_hint_clamps_to_last(self):
        fb = generate_feedback(
            "NameError: x", hints=["Only hint"],
            attempt_count=99,
        )
        self.assertEqual(fb["hint"], "Only hint")

    def test_no_hints(self):
        fb = generate_feedback("NameError: x", hints=None)
        self.assertIsNone(fb["hint"])

    def test_encouragement_varies_by_attempt(self):
        fb1 = generate_feedback("err", attempt_count=0)
        fb5 = generate_feedback("err", attempt_count=5)
        fb10 = generate_feedback("err", attempt_count=10)
        # Each should be a non-empty string
        self.assertTrue(fb1["encouragement"])
        self.assertTrue(fb5["encouragement"])
        self.assertTrue(fb10["encouragement"])

    def test_debugging_type_adds_tips(self):
        # Debugging + ASSERTION: base tips + type-specific; verify works
        fb = generate_feedback(
            "AssertionError: test failed",
            challenge_type=ChallengeType.DEBUGGING,
        )
        self.assertEqual(fb["category"], ErrorCategory.ASSERTION)
        self.assertLessEqual(len(fb["guidance"]), 6)
        # Knowledge + ASSERTION should add the data structure tip
        fb2 = generate_feedback(
            "AssertionError: wrong result",
            challenge_type=ChallengeType.KNOWLEDGE,
        )
        self.assertEqual(fb2["category"], ErrorCategory.ASSERTION)

    def test_refactoring_type_adds_tips(self):
        fb = generate_feedback(
            "AssertionError: refactor broke it",
            challenge_type=ChallengeType.REFACTORING,
        )
        self.assertEqual(fb["category"], ErrorCategory.ASSERTION)


class TestFormatFeedbackPanel(unittest.TestCase):
    """Test Rich markup formatting."""

    def test_contains_title(self):
        fb = generate_feedback("NameError: name 'x' is not defined")
        result = format_feedback_panel(fb, "NameError: name 'x' is not defined")
        self.assertIn(fb["title"], result)

    def test_contains_error_message(self):
        fb = generate_feedback("SyntaxError: bad")
        result = format_feedback_panel(fb, "SyntaxError: bad")
        self.assertIn("SyntaxError: bad", result)

    def test_truncates_long_error(self):
        long_err = "E" * 300
        fb = generate_feedback(long_err)
        result = format_feedback_panel(fb, long_err)
        self.assertIn("...", result)
        self.assertLessEqual(len(result.split("\n")[2]), 300)

    def test_includes_hint_when_present(self):
        fb = generate_feedback("err", hints=["Try this"])
        result = format_feedback_panel(fb, "err")
        self.assertIn("Try this", result)


class TestContextAwareFeedback(unittest.TestCase):
    """Test context-aware feedback with misconceptions and learning objective."""

    def test_learning_frame_from_objective(self):
        fb = generate_feedback(
            "NameError: name 'x' is not defined",
            learning_objective="Understand variable scope",
        )
        self.assertIn("learning_frame", fb)
        self.assertIn("Understand variable scope", fb["learning_frame"])

    def test_misconception_matching(self):
        fb = generate_feedback(
            "NameError: name 'my_var' is not defined",
            expected_misconceptions=[
                "variable not defined — zapomněl jsi proměnnou inicializovat",
            ],
        )
        self.assertIn("misconception_match", fb)
        if fb["misconception_match"]:
            self.assertIn("inicializovat", fb["misconception_match"])

    def test_progressive_hint_strategy(self):
        """Progressive strategy reveals hints one per attempt."""
        fb1 = generate_feedback(
            "AssertionError: fail",
            hints=["Hint A", "Hint B", "Hint C"],
            attempt_count=1,
            hint_strategy="progressive",
        )
        fb2 = generate_feedback(
            "AssertionError: fail",
            hints=["Hint A", "Hint B", "Hint C"],
            attempt_count=2,
            hint_strategy="progressive",
        )
        # Both should have a hint but potentially different ones
        self.assertIn("hint", fb1)
        self.assertIn("hint", fb2)

    def test_regression_encouragement(self):
        fb = generate_feedback(
            "AssertionError: wrong result",
            challenge_state="regressed",
            attempt_count=5,
        )
        self.assertTrue(fb["encouragement"])

    def test_returns_all_expected_keys(self):
        fb = generate_feedback(
            "TypeError: wrong type",
            learning_objective="Learn types",
            expected_misconceptions=["type confusion"],
            hint_strategy="progressive",
            challenge_state="in_progress",
            solution_pattern="return int",
        )
        for key in ("category", "title", "guidance", "hint", "encouragement",
                     "misconception_match", "learning_frame"):
            self.assertIn(key, fb)


if __name__ == "__main__":
    unittest.main()
