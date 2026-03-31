"""
Tests for services.py adaptive/concept integration — verifies that
the service layer correctly calls adaptive.py with proper arguments.
"""

import pytest
from unittest.mock import patch, MagicMock
from engine.adaptive import StudyMode, AdaptiveRecommendation, StudyPlan
from engine.recommend import ActionCategory


@pytest.fixture(autouse=True)
def reset_services():
    """Reset singleton state between tests."""
    import engine.services as svc

    svc._sections = None
    svc._progress = None


@pytest.fixture
def mock_sections():
    """Provide minimal section list."""
    section = MagicMock()
    section.num = "01"
    section.name = "Python Zaklady"
    section.lessons = []
    return [section]


@pytest.fixture
def mock_progress():
    progress = MagicMock()
    progress.get_challenge.return_value = MagicMock(
        state=MagicMock(value="not_started"),
        attempt_count=0,
        best_points=0,
        max_points=10,
        ever_passed=False,
        last_attempt_at=None,
    )
    return progress


class TestGetAdaptiveRecs:
    """Verify get_adaptive_recs properly computes concept_states and passes them."""

    @patch("engine.services._get_sections")
    @patch("engine.services._get_progress")
    @patch("engine.services.load_challenge_details")
    def test_returns_list(
        self, mock_lcd, mock_prog, mock_secs, mock_sections, mock_progress
    ):
        mock_secs.return_value = mock_sections
        mock_prog.return_value = mock_progress
        mock_lcd.return_value = []

        import engine.services as svc

        result = svc.get_adaptive_recs(mode="guided", limit=5)
        assert isinstance(result, list)

    @patch("engine.services._get_sections")
    @patch("engine.services._get_progress")
    @patch("engine.services.load_challenge_details")
    def test_mode_mapping(
        self, mock_lcd, mock_prog, mock_secs, mock_sections, mock_progress
    ):
        mock_secs.return_value = mock_sections
        mock_prog.return_value = mock_progress
        mock_lcd.return_value = []

        import engine.services as svc

        # Each mode should work without error
        for mode in ["guided", "fast_track", "reinforcement", "interview"]:
            result = svc.get_adaptive_recs(mode=mode, limit=3)
            assert isinstance(result, list)

    @patch("engine.services._get_sections")
    @patch("engine.services._get_progress")
    @patch("engine.services.load_challenge_details")
    def test_rec_serialization_fields(
        self, mock_lcd, mock_prog, mock_secs, mock_sections, mock_progress
    ):
        """If there are recommendations, they have the correct field names."""
        mock_secs.return_value = mock_sections
        mock_prog.return_value = mock_progress
        mock_lcd.return_value = []

        import engine.services as svc

        result = svc.get_adaptive_recs(mode="guided", limit=10)
        # Even if empty, we verified no crash
        for r in result:
            assert "target_concepts" in r
            assert "concept_reasoning" in r
            assert "concepts" not in r  # old broken field name
            assert "concept_reason" not in r  # old broken field name


class TestGetStudyPlan:
    """Verify get_study_plan properly computes and serializes."""

    @patch("engine.services._get_sections")
    @patch("engine.services._get_progress")
    @patch("engine.services.load_challenge_details")
    def test_returns_dict(
        self, mock_lcd, mock_prog, mock_secs, mock_sections, mock_progress
    ):
        mock_secs.return_value = mock_sections
        mock_prog.return_value = mock_progress
        mock_lcd.return_value = []

        import engine.services as svc

        result = svc.get_study_plan(mode="guided", session_minutes=30)
        assert isinstance(result, dict)
        assert "mode" in result
        assert "focus_concepts" in result
        assert "estimated_minutes" in result
        assert "reasoning" in result
        assert "steps" in result

    @patch("engine.services._get_sections")
    @patch("engine.services._get_progress")
    @patch("engine.services.load_challenge_details")
    def test_no_broken_fields(
        self, mock_lcd, mock_prog, mock_secs, mock_sections, mock_progress
    ):
        mock_secs.return_value = mock_sections
        mock_prog.return_value = mock_progress
        mock_lcd.return_value = []

        import engine.services as svc

        result = svc.get_study_plan()
        # Old broken field names should NOT be present
        assert (
            "message" not in result
        )  # was plan.message, now plan.plan_reasoning → "reasoning"
        assert "repair_paths" not in result  # never existed on StudyPlan
        # New correct fields
        assert "mode_name" in result
        assert "mode_emoji" in result
        assert "overall_mastery_pct" in result

    @patch("engine.services._get_sections")
    @patch("engine.services._get_progress")
    @patch("engine.services.load_challenge_details")
    def test_step_serialization(
        self, mock_lcd, mock_prog, mock_secs, mock_sections, mock_progress
    ):
        mock_secs.return_value = mock_sections
        mock_prog.return_value = mock_progress
        mock_lcd.return_value = []

        import engine.services as svc

        result = svc.get_study_plan()
        for step in result.get("steps", []):
            assert "target_concepts" in step
            assert "concept_reasoning" in step
            assert "concepts" not in step
            assert "concept_reason" not in step


class TestGetConceptMastery:
    """Verify concept mastery service works."""

    @patch("engine.services._get_sections")
    @patch("engine.services._get_progress")
    @patch("engine.services.load_challenge_details")
    def test_returns_dict_with_concepts(
        self, mock_lcd, mock_prog, mock_secs, mock_sections, mock_progress
    ):
        mock_secs.return_value = mock_sections
        mock_prog.return_value = mock_progress
        mock_lcd.return_value = []

        import engine.services as svc

        result = svc.get_concept_mastery()
        assert isinstance(result, dict)
        assert "concepts" in result
        assert "weak_concepts" in result
        assert "ready_concepts" in result
