"""Tests for session tracking in Progress."""
import os
import json
import pytest
import tempfile
from datetime import datetime

from engine.progress import Progress
from engine.models import ChallengeState


@pytest.fixture
def tmp_progress(tmp_path, monkeypatch):
    """Create a Progress instance with a temp file."""
    progress_file = tmp_path / ".progress.json"
    monkeypatch.setattr("engine.progress.PROGRESS_FILE", str(progress_file))
    return Progress()


class TestSessionTracking:

    def test_start_session(self, tmp_progress):
        tmp_progress.start_session()
        session = tmp_progress.data.get("current_session")
        assert session is not None
        assert session["challenges_attempted"] == 0
        assert session["challenges_passed"] == 0
        assert "started_at" in session

    def test_record_attempt_pass(self, tmp_progress):
        tmp_progress.start_session()
        tmp_progress.record_session_attempt(
            "01.01.1", True, 10,
            ChallengeState.NOT_STARTED, ChallengeState.CURRENTLY_PASSING,
        )

        session = tmp_progress.data["current_session"]
        assert session["challenges_attempted"] == 1
        assert session["challenges_passed"] == 1
        assert session["points_earned"] == 10
        assert "01.01.1" in session["challenge_ids"]

    def test_record_attempt_fail(self, tmp_progress):
        tmp_progress.start_session()
        tmp_progress.record_session_attempt(
            "01.01.1", False, 0,
            ChallengeState.NOT_STARTED, ChallengeState.IN_PROGRESS,
        )

        session = tmp_progress.data["current_session"]
        assert session["challenges_attempted"] == 1
        assert session["challenges_passed"] == 0
        assert session["points_earned"] == 0

    def test_record_mastery(self, tmp_progress):
        tmp_progress.start_session()
        tmp_progress.record_session_attempt(
            "01.01.1", True, 10,
            ChallengeState.CURRENTLY_PASSING, ChallengeState.MASTERED,
        )
        session = tmp_progress.data["current_session"]
        assert session["new_masteries"] == 1

    def test_record_regression(self, tmp_progress):
        tmp_progress.start_session()
        tmp_progress.record_session_attempt(
            "01.01.1", False, 0,
            ChallengeState.CURRENTLY_PASSING, ChallengeState.REGRESSED,
        )
        session = tmp_progress.data["current_session"]
        assert session["regressions"] == 1

    def test_unique_challenges_counted(self, tmp_progress):
        tmp_progress.start_session()
        for _ in range(3):
            tmp_progress.record_session_attempt(
                "01.01.1", False, 0,
                ChallengeState.IN_PROGRESS, ChallengeState.IN_PROGRESS,
            )
        session = tmp_progress.data["current_session"]
        assert session["challenges_attempted"] == 3
        assert len(session["challenge_ids"]) == 1

    def test_get_session_stats(self, tmp_progress):
        tmp_progress.start_session()
        tmp_progress.record_session_attempt(
            "01.01.1", True, 10,
            ChallengeState.NOT_STARTED, ChallengeState.CURRENTLY_PASSING,
        )
        stats = tmp_progress.get_session_stats()
        assert stats is not None
        assert stats["challenges_attempted"] == 1
        assert stats["challenges_passed"] == 1
        assert stats["points_earned"] == 10
        assert stats["unique_challenges"] == 1
        assert stats["duration_minutes"] >= 0

    def test_no_session_returns_none(self, tmp_progress):
        assert tmp_progress.get_session_stats() is None

    def test_end_session_archives(self, tmp_progress):
        tmp_progress.start_session()
        tmp_progress.record_session_attempt(
            "01.01.1", True, 10,
            ChallengeState.NOT_STARTED, ChallengeState.CURRENTLY_PASSING,
        )
        tmp_progress.end_session()

        assert "current_session" not in tmp_progress.data
        sessions = tmp_progress.data.get("sessions", [])
        assert len(sessions) == 1
        assert sessions[0]["challenges_attempted"] == 1
        assert "ended_at" in sessions[0]

    def test_end_session_keeps_max_20(self, tmp_progress):
        for i in range(25):
            tmp_progress.start_session()
            tmp_progress.end_session()
        assert len(tmp_progress.data["sessions"]) == 20

    def test_auto_start_on_record(self, tmp_progress):
        """Recording without starting should auto-start."""
        tmp_progress.record_session_attempt(
            "01.01.1", True, 10,
            ChallengeState.NOT_STARTED, ChallengeState.CURRENTLY_PASSING,
        )
        assert "current_session" in tmp_progress.data


class TestChallengesByState:

    def test_get_challenges_by_state(self, tmp_progress):
        tmp_progress.save_challenge("01.01.1", False, 0, 10)
        result = tmp_progress.get_challenges_by_state(ChallengeState.IN_PROGRESS)
        assert len(result) == 1
        assert result[0][0] == "01.01.1"

    def test_get_regressed(self, tmp_progress):
        tmp_progress.save_challenge("01.01.1", True, 10, 10)
        tmp_progress.save_challenge("01.01.1", False, 0, 10)
        regressed = tmp_progress.get_regressed()
        assert len(regressed) == 1

    def test_get_mastered(self, tmp_progress):
        for _ in range(3):
            tmp_progress.save_challenge("01.01.1", True, 10, 10)
        mastered = tmp_progress.get_mastered()
        assert len(mastered) == 1
