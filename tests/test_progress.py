"""Tests for the Progress module v3 — attempt-based state model."""
import json
import os
import tempfile
from unittest.mock import patch

import pytest

from engine.progress import Progress
from engine.models import ChallengeState, ChallengeProgress, AttemptRecord


@pytest.fixture
def tmp_progress(tmp_path):
    """Fixture that patches PROGRESS_FILE to a temp file."""
    progress_file = str(tmp_path / ".progress.json")
    with patch('engine.progress.PROGRESS_FILE', progress_file):
        yield progress_file


class TestProgressV3:

    def test_fresh_start(self, tmp_progress):
        p = Progress()
        assert p.data["version"] == 3
        assert p.data["challenges"] == {}
        assert p.data["sections"] == {}

    def test_save_challenge_completed(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", True, 15, 15)
        ch = p.data["challenges"]["01.01.1"]
        assert ch["best_points"] == 15
        assert len(ch["attempts"]) == 1
        assert ch["attempts"][0]["passed"] is True

    def test_save_challenge_failed(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.2", False, 0, 10)
        ch = p.data["challenges"]["01.01.2"]
        assert ch["best_points"] == 0
        assert len(ch["attempts"]) == 1
        assert ch["attempts"][0]["passed"] is False

    def test_save_challenge_with_error(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", False, 0, 10, error="Expected 42, got None")
        ch = p.data["challenges"]["01.01.1"]
        assert ch["attempts"][0]["error"] == "Expected 42, got None"

    # ── State computation tests ──

    def test_state_not_started(self, tmp_progress):
        p = Progress()
        cp = p.get_challenge("01.01.1")
        assert cp.state == ChallengeState.NOT_STARTED

    def test_state_in_progress(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", False, 0, 10)
        p.save_challenge("01.01.1", False, 0, 10)
        assert p.get_challenge_state("01.01.1") == ChallengeState.IN_PROGRESS

    def test_state_currently_passing(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", False, 0, 10)
        p.save_challenge("01.01.1", True, 10, 10)
        assert p.get_challenge_state("01.01.1") == ChallengeState.CURRENTLY_PASSING

    def test_state_regressed(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", True, 10, 10)
        p.save_challenge("01.01.1", False, 0, 10)
        assert p.get_challenge_state("01.01.1") == ChallengeState.REGRESSED

    def test_state_mastered(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", True, 10, 10)
        p.save_challenge("01.01.1", True, 10, 10)
        p.save_challenge("01.01.1", True, 10, 10)
        assert p.get_challenge_state("01.01.1") == ChallengeState.MASTERED

    def test_mastery_breaks_on_fail(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", True, 10, 10)
        p.save_challenge("01.01.1", True, 10, 10)
        p.save_challenge("01.01.1", False, 0, 10)
        assert p.get_challenge_state("01.01.1") == ChallengeState.REGRESSED

    def test_mastery_recoverable(self, tmp_progress):
        p = Progress()
        # Pass 3x = mastered
        for _ in range(3):
            p.save_challenge("01.01.1", True, 10, 10)
        assert p.get_challenge_state("01.01.1") == ChallengeState.MASTERED
        # Fail = regressed
        p.save_challenge("01.01.1", False, 0, 10)
        assert p.get_challenge_state("01.01.1") == ChallengeState.REGRESSED
        # Pass again = currently_passing (NOT mastered yet)
        p.save_challenge("01.01.1", True, 10, 10)
        assert p.get_challenge_state("01.01.1") == ChallengeState.CURRENTLY_PASSING

    def test_no_ratcheting_status_reflects_reality(self, tmp_progress):
        """Unlike v2, status should reflect current reality, not historical best."""
        p = Progress()
        p.save_challenge("01.01.1", True, 10, 10)
        assert p.get_challenge("01.01.1").ever_passed is True
        p.save_challenge("01.01.1", False, 0, 10)
        # State is REGRESSED, not still "completed"
        assert p.get_challenge_state("01.01.1") == ChallengeState.REGRESSED
        # But ever_passed is still True (achievement preserved)
        assert p.get_challenge("01.01.1").ever_passed is True
        # Best points preserved
        assert p.get_challenge("01.01.1").best_points == 10

    # ── Bookmark tests ──

    def test_bookmark(self, tmp_progress):
        p = Progress()
        p.set_bookmark("01", "03", "Python Základy", "Funkce", challenge_index=2)
        bm = p.get_bookmark()
        assert bm["section_num"] == "01"
        assert bm["lesson_num"] == "03"
        assert bm["challenge_index"] == 2
        assert bm["section_name"] == "Python Základy"
        assert bm["lesson_name"] == "Funkce"

    def test_bookmark_none_by_default(self, tmp_progress):
        p = Progress()
        assert p.get_bookmark() is None

    # ── Aggregation tests ──

    def test_lesson_completed_count(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", True, 10, 10)
        p.save_challenge("01.01.2", True, 15, 15)
        p.save_challenge("01.01.3", False, 0, 10)
        assert p.get_lesson_completed("01", "01") == 2

    def test_lesson_completed_excludes_regressed(self, tmp_progress):
        """Only currently passing/mastered count as 'completed'."""
        p = Progress()
        p.save_challenge("01.01.1", True, 10, 10)
        p.save_challenge("01.01.1", False, 0, 10)  # regressed
        p.save_challenge("01.01.2", True, 15, 15)   # passing
        assert p.get_lesson_completed("01", "01") == 1

    def test_lesson_ever_passed(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", True, 10, 10)
        p.save_challenge("01.01.1", False, 0, 10)  # regressed but was passed
        p.save_challenge("01.01.2", True, 15, 15)
        assert p.get_lesson_ever_passed("01", "01") == 2

    def test_section_completed_count(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", True, 10, 10)
        p.save_challenge("01.02.1", True, 15, 15)
        p.save_challenge("01.03.1", False, 0, 10)
        assert p.get_section_completed("01") == 2

    def test_get_all_in_progress(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", True, 10, 10)   # passing
        p.save_challenge("01.01.2", False, 0, 10)   # in_progress
        p.save_challenge("01.02.1", True, 10, 10)
        p.save_challenge("01.02.1", False, 0, 10)   # regressed
        results = p.get_all_in_progress()
        ids = [cid for cid, _ in results]
        assert "01.01.2" in ids
        assert "01.02.1" in ids
        assert "01.01.1" not in ids

    def test_state_counts(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", True, 10, 10)
        p.save_challenge("01.01.2", False, 0, 10)
        p.save_challenge("01.01.3", True, 10, 10)
        p.save_challenge("01.01.3", False, 0, 10)
        counts = p.get_state_counts()
        assert counts[ChallengeState.CURRENTLY_PASSING] == 1
        assert counts[ChallengeState.IN_PROGRESS] == 1
        assert counts[ChallengeState.REGRESSED] == 1

    # ── Legacy backward compat tests ──

    def test_legacy_save_section(self, tmp_progress):
        p = Progress()
        p.save_section("01_01", 5, 7, 50)
        sec = p.get_section("01_01")
        assert sec["completed"] == 5
        assert sec["best_points"] == 50

    def test_legacy_ratcheting(self, tmp_progress):
        p = Progress()
        p.save_section("01_01", 5, 7, 50)
        p.save_section("01_01", 3, 7, 30)
        sec = p.get_section("01_01")
        assert sec["completed"] == 5
        assert sec["best_points"] == 50

    # ── Migration tests ──

    def test_v1_migration(self, tmp_progress):
        v1_data = {
            "total_points": 90,
            "total_challenges": 7,
            "sections": {
                "01_01": {
                    "completed": 7, "total": 7,
                    "points": 90, "best_points": 90,
                }
            },
            "streak_days": ["2026-03-14"],
            "started": "2026-03-14T20:44:53",
        }
        with open(tmp_progress, 'w') as f:
            json.dump(v1_data, f)

        p = Progress()
        assert p.data["version"] == 3
        assert "challenges" in p.data
        assert p.data["sections"]["01_01"]["completed"] == 7

    def test_v2_migration(self, tmp_progress):
        """v2 data (status-based) should be migrated to v3 (attempts-based)."""
        v2_data = {
            "version": 2,
            "total_points": 25,
            "total_challenges": 2,
            "sections": {},
            "challenges": {
                "01.01.1": {
                    "status": "completed",
                    "points": 15,
                    "max_points": 15,
                    "attempts": 2,
                    "completed_at": "2026-03-30T10:00:00",
                    "last_attempt_at": "2026-03-30T10:00:00",
                },
                "01.01.2": {
                    "status": "failed",
                    "points": 0,
                    "max_points": 10,
                    "attempts": 1,
                    "last_attempt_at": "2026-03-30T10:00:00",
                },
            },
            "streak_days": ["2026-03-30"],
            "bookmark": None,
            "started": "2026-03-30T10:00:00",
        }
        with open(tmp_progress, 'w') as f:
            json.dump(v2_data, f)

        p = Progress()
        assert p.data["version"] == 3

        # Completed challenge should have passing attempt
        ch1 = p.data["challenges"]["01.01.1"]
        assert isinstance(ch1["attempts"], list)
        assert any(a["passed"] for a in ch1["attempts"])
        cp1 = p.get_challenge("01.01.1")
        assert cp1.state == ChallengeState.CURRENTLY_PASSING
        assert cp1.best_points == 15

        # Failed challenge should have failing attempt
        ch2 = p.data["challenges"]["01.01.2"]
        assert isinstance(ch2["attempts"], list)
        assert not any(a["passed"] for a in ch2["attempts"])
        cp2 = p.get_challenge("01.01.2")
        assert cp2.state == ChallengeState.IN_PROGRESS

    # ── Summary tests ──

    def test_summary_from_v3(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", True, 10, 10)
        p.save_challenge("01.01.2", True, 15, 15)
        s = p.get_summary()
        assert s["total_points"] == 25
        assert s["total_challenges"] == 2

    def test_summary_from_v1(self, tmp_progress):
        p = Progress()
        p.save_section("01_01", 3, 5, 30)
        s = p.get_summary()
        assert s["total_points"] == 30
        assert s["total_challenges"] == 3

    def test_streak(self, tmp_progress):
        p = Progress()
        p.data["streak_days"] = ["2026-03-28", "2026-03-29", "2026-03-30"]
        assert p.get_streak() == 3

    def test_streak_gap(self, tmp_progress):
        p = Progress()
        p.data["streak_days"] = ["2026-03-27", "2026-03-29", "2026-03-30"]
        assert p.get_streak() == 2

    # ── Persistence ──

    def test_persistence(self, tmp_progress):
        p1 = Progress()
        p1.save_challenge("01.01.1", True, 15, 15)

        p2 = Progress()
        cp = p2.get_challenge("01.01.1")
        assert cp.state == ChallengeState.CURRENTLY_PASSING
        assert cp.best_points == 15

    def test_reset(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", True, 15, 15)
        p.reset()
        assert p.data["challenges"] == {}
        assert p.data["sections"] == {}

    def test_activity_recording(self, tmp_progress):
        p = Progress()
        p.save_challenge("01.01.1", True, 15, 15)
        assert len(p.data["streak_days"]) == 1

    # ── Attempt trimming ──

    def test_attempts_trimmed_to_max(self, tmp_progress):
        p = Progress()
        for i in range(15):
            p.save_challenge("01.01.1", i % 2 == 0, 10 if i % 2 == 0 else 0, 10)
        ch = p.data["challenges"]["01.01.1"]
        assert len(ch["attempts"]) == 10  # MAX_ATTEMPTS_STORED
