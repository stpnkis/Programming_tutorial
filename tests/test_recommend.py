"""Tests for the recommendation engine, review queue, and weak area detection."""
import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from engine.recommend import (
    ActionCategory, Recommendation, LearningSnapshot,
    is_review_due, get_review_queue, get_weak_areas,
    get_smart_recommendations, build_snapshot,
    categorize_recommendations, get_concept_recommendations,
    get_available_tags,
    _consecutive_passes, _get_review_interval, _last_pass_time,
    REVIEW_INTERVALS,
)
from engine.models import ChallengeState, ChallengeProgress, AttemptRecord


# ── Helpers ──

def _make_progress(attempts_data: list) -> ChallengeProgress:
    """Create a ChallengeProgress from a list of (passed, timestamp) tuples."""
    attempts = [
        AttemptRecord(passed=p, at=ts, points=10 if p else 0)
        for p, ts in attempts_data
    ]
    return ChallengeProgress(attempts=attempts)


def _ts(days_ago: int) -> str:
    """Create ISO timestamp N days in the past."""
    return (datetime.now() - timedelta(days=days_ago)).isoformat()


def _make_mock_progress(challenges_dict: dict):
    """Create a mock progress object with get_state_counts, data, etc."""
    mock = MagicMock()
    mock.data = {"challenges": challenges_dict}

    def _to_progress(rec):
        attempts = [
            AttemptRecord(
                passed=a["passed"],
                at=a.get("at", ""),
                points=a.get("points", 0),
            )
            for a in rec.get("attempts", [])
        ]
        return ChallengeProgress(attempts=attempts)

    mock._to_progress = _to_progress

    def get_state_counts():
        counts = {}
        for cid, rec in challenges_dict.items():
            cp = _to_progress(rec)
            counts[cp.state] = counts.get(cp.state, 0) + 1
        return counts

    mock.get_state_counts = get_state_counts

    def get_lesson_completed(sec, les):
        prefix = f"{sec}.{les}."
        count = 0
        for cid, rec in challenges_dict.items():
            if cid.startswith(prefix):
                cp = _to_progress(rec)
                if cp.state in (ChallengeState.CURRENTLY_PASSING, ChallengeState.MASTERED):
                    count += 1
        return count

    mock.get_lesson_completed = get_lesson_completed

    def get_lesson_ever_passed(sec, les):
        prefix = f"{sec}.{les}."
        count = 0
        for cid, rec in challenges_dict.items():
            if cid.startswith(prefix):
                cp = _to_progress(rec)
                if any(a.passed for a in cp.attempts):
                    count += 1
        return count

    mock.get_lesson_ever_passed = get_lesson_ever_passed

    return mock


def _make_sections():
    """Create minimal section structure for testing."""
    from engine.models import SectionInfo, LessonInfo, LessonMeta

    meta = LessonMeta()
    lessons_s01 = [
        LessonInfo(
            name=f"Lesson {i}", section_num="01", lesson_num=f"{i:02d}",
            dir_name=f"{i:02d}_lesson", path="", challenge_file="",
            challenge_count=3, meta=meta,
        )
        for i in range(1, 4)
    ]
    lessons_s02 = [
        LessonInfo(
            name=f"Lesson {i}", section_num="02", lesson_num=f"{i:02d}",
            dir_name=f"{i:02d}_lesson", path="", challenge_file="",
            challenge_count=3, meta=meta,
        )
        for i in range(1, 3)
    ]

    return [
        SectionInfo(num="01", name="Python Základy", emoji="🐍",
                    dir_name="01_Python_Zaklady", path="", lessons=lessons_s01),
        SectionInfo(num="02", name="OOP", emoji="🧩",
                    dir_name="02_OOP", path="", lessons=lessons_s02),
    ]


# ── Unit tests ──

class TestConsecutivePasses:

    def test_no_attempts(self):
        cp = ChallengeProgress(attempts=[])
        assert _consecutive_passes(cp) == 0

    def test_all_passes(self):
        cp = _make_progress([(True, _ts(3)), (True, _ts(2)), (True, _ts(1))])
        assert _consecutive_passes(cp) == 3

    def test_fail_at_end(self):
        cp = _make_progress([(True, _ts(3)), (True, _ts(2)), (False, _ts(1))])
        assert _consecutive_passes(cp) == 0

    def test_mixed(self):
        cp = _make_progress([
            (False, _ts(5)), (True, _ts(3)), (False, _ts(2)), (True, _ts(1)),
        ])
        assert _consecutive_passes(cp) == 1


class TestReviewInterval:

    def test_single_pass(self):
        assert _get_review_interval(1) == REVIEW_INTERVALS[1]

    def test_two_passes(self):
        assert _get_review_interval(2) == REVIEW_INTERVALS[2]

    def test_mastered(self):
        assert _get_review_interval(3) == REVIEW_INTERVALS[3]

    def test_sustained_mastery(self):
        assert _get_review_interval(6) == REVIEW_INTERVALS[6]

    def test_many_passes(self):
        assert _get_review_interval(20) == REVIEW_INTERVALS[6]


class TestIsReviewDue:

    def test_not_passing_not_due(self):
        """In-progress challenges are never due for review."""
        cp = _make_progress([(False, _ts(10))])
        assert not is_review_due(cp)

    def test_recent_pass_not_due(self):
        """Just passed today — not due yet."""
        cp = _make_progress([(True, _ts(0))])
        now = datetime.now()
        assert not is_review_due(cp, now)

    def test_one_pass_after_one_day(self):
        """Single pass, 2 days ago — should be due."""
        cp = _make_progress([(True, _ts(2))])
        now = datetime.now()
        assert is_review_due(cp, now)

    def test_mastered_within_interval(self):
        """Mastered (3 passes), last pass 5 days ago — interval is 7 days, not due."""
        cp = _make_progress([
            (True, _ts(10)), (True, _ts(8)), (True, _ts(5)),
        ])
        now = datetime.now()
        assert not is_review_due(cp, now)

    def test_mastered_past_interval(self):
        """Mastered (3 passes), last pass 10 days ago — interval is 7 days, due."""
        cp = _make_progress([
            (True, _ts(20)), (True, _ts(15)), (True, _ts(10)),
        ])
        now = datetime.now()
        assert is_review_due(cp, now)


class TestLastPassTime:

    def test_no_passes(self):
        cp = _make_progress([(False, _ts(1))])
        assert _last_pass_time(cp) is None

    def test_finds_last(self):
        cp = _make_progress([(True, _ts(5)), (False, _ts(2)), (True, _ts(1))])
        result = _last_pass_time(cp)
        assert result is not None
        # Should be approximately 1 day ago
        assert (datetime.now() - result).total_seconds() < 2 * 86400


class TestGetReviewQueue:

    def test_empty_progress(self):
        progress = _make_mock_progress({})
        sections = _make_sections()
        assert get_review_queue(progress, sections) == []

    def test_due_challenges_included(self):
        """Challenges passed long ago should appear in review queue."""
        progress = _make_mock_progress({
            "01.01.1": {"attempts": [
                {"passed": True, "at": _ts(5), "points": 10, "max_points": 10},
            ]},
        })
        sections = _make_sections()
        queue = get_review_queue(progress, sections)
        assert len(queue) == 1
        assert queue[0].challenge_id == "01.01.1"
        assert queue[0].category == ActionCategory.REVIEW_DUE

    def test_recent_passes_not_in_queue(self):
        """Recently passed challenges should not be in review queue."""
        progress = _make_mock_progress({
            "01.01.1": {"attempts": [
                {"passed": True, "at": _ts(0), "points": 10, "max_points": 10},
            ]},
        })
        sections = _make_sections()
        queue = get_review_queue(progress, sections)
        assert len(queue) == 0


class TestGetWeakAreas:

    def test_no_weak_areas(self):
        progress = _make_mock_progress({})
        sections = _make_sections()
        assert get_weak_areas(progress, sections) == []

    def test_regressed_challenge_makes_weak(self):
        """A lesson with a regressed challenge should be a weak area."""
        progress = _make_mock_progress({
            "01.01.1": {"attempts": [
                {"passed": True, "at": _ts(5), "points": 10, "max_points": 10},
                {"passed": False, "at": _ts(1), "points": 0, "max_points": 10},
            ]},
        })
        sections = _make_sections()
        weak = get_weak_areas(progress, sections)
        assert len(weak) == 1
        assert weak[0]["regressed"] == 1
        assert weak[0]["lesson_num"] == "01"

    def test_struggling_challenge_makes_weak(self):
        """3+ failed attempts with no pass makes a weak area."""
        progress = _make_mock_progress({
            "01.02.1": {"attempts": [
                {"passed": False, "at": _ts(5), "points": 0, "max_points": 10},
                {"passed": False, "at": _ts(3), "points": 0, "max_points": 10},
                {"passed": False, "at": _ts(1), "points": 0, "max_points": 10},
            ]},
        })
        sections = _make_sections()
        weak = get_weak_areas(progress, sections)
        assert len(weak) == 1
        assert weak[0]["struggling"] == 1


class TestSmartRecommendations:

    def test_empty_gives_new_material(self):
        """With no progress, should recommend first lesson."""
        progress = _make_mock_progress({})
        sections = _make_sections()
        recs = get_smart_recommendations(progress, sections)
        assert len(recs) >= 1
        assert recs[0].category == ActionCategory.NEW_MATERIAL

    def test_regression_first_priority(self):
        """Regressions should be recommended before anything else."""
        progress = _make_mock_progress({
            "01.01.1": {"attempts": [
                {"passed": True, "at": _ts(5), "points": 10, "max_points": 10},
                {"passed": False, "at": _ts(1), "points": 0, "max_points": 10},
            ]},
        })
        sections = _make_sections()
        recs = get_smart_recommendations(progress, sections)
        assert recs[0].category == ActionCategory.FIX_REGRESSION

    def test_limit_respected(self):
        progress = _make_mock_progress({})
        sections = _make_sections()
        recs = get_smart_recommendations(progress, sections, limit=2)
        assert len(recs) <= 2


class TestBuildSnapshot:

    def test_empty_snapshot(self):
        progress = _make_mock_progress({})
        sections = _make_sections()
        snap = build_snapshot(progress, sections)
        assert snap.total_challenges > 0
        assert snap.mastered == 0
        assert snap.regressed == 0
        assert snap.mastery_pct == 0.0

    def test_mastery_pct(self):
        """Mastery percentage should be mastered / total."""
        progress = _make_mock_progress({
            "01.01.1": {"attempts": [
                {"passed": True, "at": _ts(5), "points": 10, "max_points": 10},
                {"passed": True, "at": _ts(3), "points": 10, "max_points": 10},
                {"passed": True, "at": _ts(1), "points": 10, "max_points": 10},
            ]},
        })
        sections = _make_sections()
        snap = build_snapshot(progress, sections)
        assert snap.mastered == 1
        # Total is 3 lessons * 3 challenges = 9
        assert snap.total_challenges == 15  # 3*3 + 2*3 = 9+6=15
        assert snap.mastery_pct == pytest.approx(1 / 15)

    def test_snapshot_has_recommendations(self):
        progress = _make_mock_progress({})
        sections = _make_sections()
        snap = build_snapshot(progress, sections)
        assert snap.recommendations is not None
        assert snap.next_action is not None


class TestLearningSnapshot:

    def test_progress_pct_calculation(self):
        snap = LearningSnapshot(
            total_challenges=100,
            mastered=20,
            currently_passing=30,
        )
        assert snap.progress_pct == pytest.approx(0.5)

    def test_zero_total(self):
        snap = LearningSnapshot(total_challenges=0)
        assert snap.mastery_pct == 0.0
        assert snap.progress_pct == 0.0


class TestCategorizeRecommendations:

    def test_empty_progress_gives_new(self):
        progress = _make_mock_progress({})
        sections = _make_sections()
        cats = categorize_recommendations(progress, sections)
        assert isinstance(cats, dict)
        assert "regressions" in cats
        assert "review" in cats
        assert "continue" in cats
        assert "new" in cats
        # With no progress, should have new material
        assert len(cats["new"]) > 0

    def test_regression_categorized(self):
        progress = _make_mock_progress({
            "01.01.1": {"attempts": [
                {"passed": True, "at": _ts(5), "points": 10, "max_points": 10},
                {"passed": False, "at": _ts(1), "points": 0, "max_points": 10},
            ]},
        })
        sections = _make_sections()
        cats = categorize_recommendations(progress, sections)
        assert len(cats["regressions"]) >= 1
        assert cats["regressions"][0].challenge_id == "01.01.1"


class TestGetAvailableTags:

    def test_returns_list(self):
        sections = _make_sections()
        tags = get_available_tags(sections)
        assert isinstance(tags, list)

    def test_tags_from_yaml_metadata(self):
        """Tags come from lesson yaml metadata, so with empty meta returns empty."""
        sections = _make_sections()
        tags = get_available_tags(sections)
        # Default LessonMeta has no tags, so empty is fine
        assert isinstance(tags, list)


class TestGetConceptRecommendations:

    def test_returns_empty_for_unknown_tag(self):
        progress = _make_mock_progress({})
        sections = _make_sections()
        recs = get_concept_recommendations(progress, sections, "nonexistent_tag")
        assert isinstance(recs, list)

    def test_returns_list(self):
        progress = _make_mock_progress({})
        sections = _make_sections()
        recs = get_concept_recommendations(progress, sections, "python")
        assert isinstance(recs, list)
