"""Tests for ChallengeProgress state computation — the core learning model."""
import pytest
from engine.models import (
    ChallengeState, ChallengeProgress, AttemptRecord, MASTERY_THRESHOLD,
)


class TestChallengeProgressState:
    """State is always derived from attempt history — no stored status."""

    def test_empty_is_not_started(self):
        cp = ChallengeProgress()
        assert cp.state == ChallengeState.NOT_STARTED
        assert not cp.ever_passed
        assert cp.attempt_count == 0

    def test_single_fail_is_in_progress(self):
        cp = ChallengeProgress(attempts=[
            AttemptRecord(at="2026-01-01T00:00:00", passed=False),
        ])
        assert cp.state == ChallengeState.IN_PROGRESS
        assert not cp.ever_passed

    def test_multiple_fails_still_in_progress(self):
        cp = ChallengeProgress(attempts=[
            AttemptRecord(at="t1", passed=False),
            AttemptRecord(at="t2", passed=False),
            AttemptRecord(at="t3", passed=False),
        ])
        assert cp.state == ChallengeState.IN_PROGRESS

    def test_first_pass_is_currently_passing(self):
        cp = ChallengeProgress(attempts=[
            AttemptRecord(at="t1", passed=True, points=10),
        ])
        assert cp.state == ChallengeState.CURRENTLY_PASSING
        assert cp.ever_passed

    def test_pass_after_fails_is_currently_passing(self):
        cp = ChallengeProgress(attempts=[
            AttemptRecord(at="t1", passed=False),
            AttemptRecord(at="t2", passed=False),
            AttemptRecord(at="t3", passed=True, points=10),
        ])
        assert cp.state == ChallengeState.CURRENTLY_PASSING

    def test_fail_after_pass_is_regressed(self):
        cp = ChallengeProgress(attempts=[
            AttemptRecord(at="t1", passed=True, points=10),
            AttemptRecord(at="t2", passed=False),
        ])
        assert cp.state == ChallengeState.REGRESSED
        assert cp.ever_passed  # achievement preserved

    def test_three_consecutive_passes_is_mastered(self):
        cp = ChallengeProgress(attempts=[
            AttemptRecord(at="t1", passed=True, points=10),
            AttemptRecord(at="t2", passed=True, points=10),
            AttemptRecord(at="t3", passed=True, points=10),
        ])
        assert cp.state == ChallengeState.MASTERED

    def test_mastery_needs_exact_threshold(self):
        """Two passes is not enough for mastery (threshold=3)."""
        cp = ChallengeProgress(attempts=[
            AttemptRecord(at="t1", passed=True, points=10),
            AttemptRecord(at="t2", passed=True, points=10),
        ])
        assert cp.state == ChallengeState.CURRENTLY_PASSING

    def test_mastery_with_early_failures(self):
        """Mastery only counts consecutive passes from the end."""
        cp = ChallengeProgress(attempts=[
            AttemptRecord(at="t1", passed=False),
            AttemptRecord(at="t2", passed=True, points=10),
            AttemptRecord(at="t3", passed=True, points=10),
            AttemptRecord(at="t4", passed=True, points=10),
        ])
        assert cp.state == ChallengeState.MASTERED

    def test_mastery_broken_by_fail(self):
        """A failure in the middle resets the consecutive count."""
        cp = ChallengeProgress(attempts=[
            AttemptRecord(at="t1", passed=True, points=10),
            AttemptRecord(at="t2", passed=True, points=10),
            AttemptRecord(at="t3", passed=False),
            AttemptRecord(at="t4", passed=True, points=10),
            AttemptRecord(at="t5", passed=True, points=10),
        ])
        assert cp.state == ChallengeState.CURRENTLY_PASSING  # only 2 consecutive

    def test_best_points_tracked(self):
        cp = ChallengeProgress(
            best_points=15, max_points=20,
            attempts=[
                AttemptRecord(at="t1", passed=True, points=10),
                AttemptRecord(at="t2", passed=True, points=15),
            ]
        )
        assert cp.best_points == 15

    def test_last_attempt_at(self):
        cp = ChallengeProgress(attempts=[
            AttemptRecord(at="t1", passed=True),
            AttemptRecord(at="t2", passed=False),
        ])
        assert cp.last_attempt_at == "t2"

    def test_last_attempt_at_none_when_empty(self):
        cp = ChallengeProgress()
        assert cp.last_attempt_at is None


class TestStateTransitions:
    """Verify all valid state transition paths."""

    def _make(self, passes: list) -> ChallengeState:
        attempts = [
            AttemptRecord(at=f"t{i}", passed=p, points=10 if p else 0)
            for i, p in enumerate(passes)
        ]
        return ChallengeProgress(attempts=attempts).state

    def test_not_started_to_in_progress(self):
        assert self._make([False]) == ChallengeState.IN_PROGRESS

    def test_not_started_to_passing(self):
        assert self._make([True]) == ChallengeState.CURRENTLY_PASSING

    def test_in_progress_to_passing(self):
        assert self._make([False, False, True]) == ChallengeState.CURRENTLY_PASSING

    def test_passing_to_mastered(self):
        assert self._make([True, True, True]) == ChallengeState.MASTERED

    def test_passing_to_regressed(self):
        assert self._make([True, False]) == ChallengeState.REGRESSED

    def test_regressed_to_passing(self):
        assert self._make([True, False, True]) == ChallengeState.CURRENTLY_PASSING

    def test_mastered_to_regressed(self):
        assert self._make([True, True, True, False]) == ChallengeState.REGRESSED

    def test_full_cycle(self):
        """not_started → in_progress → passing → mastered → regressed → passing."""
        history = []
        assert ChallengeProgress(attempts=[]).state == ChallengeState.NOT_STARTED

        history.append(False)
        assert self._make(history) == ChallengeState.IN_PROGRESS

        history.append(True)
        assert self._make(history) == ChallengeState.CURRENTLY_PASSING

        history.extend([True, True])
        assert self._make(history) == ChallengeState.MASTERED

        history.append(False)
        assert self._make(history) == ChallengeState.REGRESSED

        history.append(True)
        assert self._make(history) == ChallengeState.CURRENTLY_PASSING
