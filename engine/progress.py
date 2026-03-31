"""
📊 Progress modul v3 — attempt-based learning state tracking.

v3 changes:
- Attempts stored as full history (last 10 per challenge)
- State computed from attempts, not stored as boolean
- ChallengeState: not_started / in_progress / currently_passing / mastered / regressed
- Bookmark extended with challenge_index
- Fully backward compatible with v1/v2
"""
import json
import os
import tempfile
from datetime import datetime
from typing import Optional, List, Dict, Tuple

from engine.models import (
    ChallengeState, ChallengeProgress, AttemptRecord, MASTERY_THRESHOLD
)


PROGRESS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ".progress.json"
)

MAX_ATTEMPTS_STORED = 10  # keep last N attempts per challenge


class Progress:
    """Progress tracker v3 — attempt-based state with full backward compat."""

    def __init__(self):
        self.data = self._load()
        self._ensure_v3()

    # ── Persistence ──

    def _load(self):
        if os.path.exists(PROGRESS_FILE):
            try:
                with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return self._default_data()

    def _default_data(self):
        return {
            "version": 3,
            "total_points": 0,
            "total_challenges": 0,
            "sections": {},
            "challenges": {},
            "streak_days": [],
            "bookmark": None,
            "started": datetime.now().isoformat(),
        }

    def _ensure_v3(self):
        """Migrate v1/v2 data to v3 format."""
        ver = self.data.get("version", 1)
        if ver < 2:
            self.data["version"] = 3
            self.data.setdefault("challenges", {})
            self.data.setdefault("bookmark", None)
        if ver < 3:
            self._migrate_v2_to_v3()
            self.data["version"] = 3
            self._save()

    def _migrate_v2_to_v3(self):
        """Convert v2 challenge records (status+count) to v3 (attempts array)."""
        challenges = self.data.get("challenges", {})
        for cid, rec in list(challenges.items()):
            if isinstance(rec, dict) and "attempts" in rec:
                if isinstance(rec["attempts"], list):
                    continue  # already v3 format
                # v2 format: attempts is an integer count
                v2_status = rec.get("status", "failed")
                v2_attempts_count = rec.get("attempts", 1) if isinstance(rec.get("attempts"), int) else 1
                ts = rec.get("last_attempt_at") or rec.get("completed_at") or datetime.now().isoformat()
                passed = v2_status == "completed"
                points = rec.get("points", 0) if passed else 0
                max_pts = rec.get("max_points", 0)

                attempts = []
                # Create synthetic attempt records
                if v2_attempts_count > 1 and passed:
                    # Had failures before passing
                    for _ in range(v2_attempts_count - 1):
                        attempts.append({"at": ts, "passed": False, "points": 0})
                attempts.append({"at": ts, "passed": passed, "points": points})

                challenges[cid] = {
                    "best_points": rec.get("points", 0) if passed else 0,
                    "max_points": max_pts,
                    "attempts": attempts[-MAX_ATTEMPTS_STORED:],
                }

    def _save(self):
        """Atomic write to disk (write-to-temp + rename)."""
        try:
            dirname = os.path.dirname(PROGRESS_FILE) or '.'
            fd, tmp_path = tempfile.mkstemp(dir=dirname, suffix='.json')
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=2, ensure_ascii=False)
                os.replace(tmp_path, PROGRESS_FILE)
            except Exception:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
                raise
        except IOError as e:
            print(f"  ⚠️  Nepodařilo se uložit progress: {e}")

    # ── V1 backward-compatible methods (used by engine/runner.py) ──

    def save_section(self, section_id, completed, total, points):
        """Save section result. Ratcheting: completed never drops."""
        today = datetime.now().strftime("%Y-%m-%d")
        existing = self.data.get("sections", {}).get(section_id, {})

        self.data["sections"][section_id] = {
            "completed": max(completed, existing.get("completed", 0)),
            "total": max(total, existing.get("total", 0)),
            "points": points,
            "last_attempt": datetime.now().isoformat(),
            "best_points": max(points, existing.get("best_points", 0)),
        }

        self.data["total_points"] = sum(
            s.get("best_points", 0) for s in self.data["sections"].values()
        )
        self.data["total_challenges"] = sum(
            s.get("completed", 0) for s in self.data["sections"].values()
        )

        if today not in self.data.get("streak_days", []):
            self.data.setdefault("streak_days", []).append(today)

        self._save()

    def get_section(self, section_id):
        return self.data.get("sections", {}).get(section_id, {})

    def get_streak(self):
        days = sorted(self.data.get("streak_days", []))
        if not days:
            return 0
        streak = 1
        for i in range(len(days) - 1, 0, -1):
            d1 = datetime.strptime(days[i], "%Y-%m-%d")
            d2 = datetime.strptime(days[i - 1], "%Y-%m-%d")
            if (d1 - d2).days == 1:
                streak += 1
            else:
                break
        return streak

    def get_summary(self):
        """Combined summary from v3 + v1 legacy data."""
        challenges = self.data.get("challenges", {})
        v3_points = 0
        v3_completed = 0
        for c in challenges.values():
            cp = self._to_progress(c)
            if cp.ever_passed:
                v3_completed += 1
                v3_points += cp.best_points

        v1_points = self.data.get("total_points", 0)
        v1_completed = self.data.get("total_challenges", 0)

        return {
            "total_points": max(v3_points, v1_points),
            "total_challenges": max(v3_completed, v1_completed),
            "sections_started": len(self.data.get("sections", {})),
            "streak": self.get_streak(),
            "days_active": len(self.data.get("streak_days", [])),
        }

    def reset(self):
        self.data = self._default_data()
        self._save()

    # ── V3 challenge methods ──

    def save_challenge(self, challenge_id: str, passed: bool, points: int,
                       max_points: int, error: Optional[str] = None):
        """Record a challenge attempt. Appends to attempt history."""
        rec = self.data.get("challenges", {}).get(challenge_id, {
            "best_points": 0,
            "max_points": max_points,
            "attempts": [],
        })

        # Ensure attempts is a list (migrate inline if needed)
        if not isinstance(rec.get("attempts"), list):
            rec["attempts"] = []

        attempt = {
            "at": datetime.now().isoformat(),
            "passed": passed,
            "points": points,
        }
        if error:
            attempt["error"] = error

        rec["attempts"].append(attempt)
        # Trim to last N
        rec["attempts"] = rec["attempts"][-MAX_ATTEMPTS_STORED:]

        if passed:
            rec["best_points"] = max(points, rec.get("best_points", 0))
        rec["max_points"] = max(max_points, rec.get("max_points", 0))

        self.data.setdefault("challenges", {})[challenge_id] = rec
        self._record_activity()
        self._save()

    def get_challenge(self, challenge_id: str) -> ChallengeProgress:
        """Return ChallengeProgress with computed state."""
        rec = self.data.get("challenges", {}).get(challenge_id)
        if not rec:
            return ChallengeProgress()
        return self._to_progress(rec)

    def get_challenge_state(self, challenge_id: str) -> ChallengeState:
        """Shortcut to get just the state."""
        return self.get_challenge(challenge_id).state

    def get_lesson_progress(self, section_num: str, lesson_num: str
                            ) -> List[Tuple[str, ChallengeProgress]]:
        """All challenge progress records for a lesson, ordered by ID."""
        prefix = f"{section_num}.{lesson_num}."
        results = []
        for k, v in sorted(self.data.get("challenges", {}).items()):
            if k.startswith(prefix):
                results.append((k, self._to_progress(v)))
        return results

    def get_lesson_completed(self, section_num, lesson_num):
        """Count of currently-passing+ challenges for a lesson."""
        prefix = f"{section_num}.{lesson_num}."
        count = 0
        for k, v in self.data.get("challenges", {}).items():
            if k.startswith(prefix):
                cp = self._to_progress(v)
                if cp.state in (ChallengeState.CURRENTLY_PASSING, ChallengeState.MASTERED):
                    count += 1
        return count

    def get_lesson_ever_passed(self, section_num, lesson_num):
        """Count of ever-passed challenges (for achievement tracking)."""
        prefix = f"{section_num}.{lesson_num}."
        count = 0
        for k, v in self.data.get("challenges", {}).items():
            if k.startswith(prefix):
                cp = self._to_progress(v)
                if cp.ever_passed:
                    count += 1
        return count

    def get_section_completed(self, section_num):
        prefix = f"{section_num}."
        count = 0
        for k, v in self.data.get("challenges", {}).items():
            if k.startswith(prefix):
                cp = self._to_progress(v)
                if cp.state in (ChallengeState.CURRENTLY_PASSING, ChallengeState.MASTERED):
                    count += 1
        return count

    def get_all_in_progress(self) -> List[Tuple[str, ChallengeProgress]]:
        """All challenges with IN_PROGRESS or REGRESSED state."""
        results = []
        for k, v in sorted(self.data.get("challenges", {}).items()):
            cp = self._to_progress(v)
            if cp.state in (ChallengeState.IN_PROGRESS, ChallengeState.REGRESSED):
                results.append((k, cp))
        return results

    def get_state_counts(self) -> Dict[ChallengeState, int]:
        """Count challenges in each state."""
        counts = {s: 0 for s in ChallengeState}
        for v in self.data.get("challenges", {}).values():
            cp = self._to_progress(v)
            counts[cp.state] += 1
        return counts

    # ── Bookmark ──

    def set_bookmark(self, section_num, lesson_num, section_name="",
                     lesson_name="", challenge_index=0):
        """Save bookmark — where the user left off, down to challenge level."""
        self.data["bookmark"] = {
            "section_num": section_num,
            "lesson_num": lesson_num,
            "challenge_index": challenge_index,
            "section_name": section_name,
            "lesson_name": lesson_name,
            "at": datetime.now().isoformat(),
        }
        self._save()

    def get_bookmark(self):
        return self.data.get("bookmark")

    # ── Internal helpers ──

    def _to_progress(self, rec: dict) -> ChallengeProgress:
        """Convert raw dict to ChallengeProgress."""
        attempts_raw = rec.get("attempts", [])
        attempts = []
        for a in attempts_raw:
            if isinstance(a, dict):
                attempts.append(AttemptRecord(
                    at=a.get("at", ""),
                    passed=a.get("passed", False),
                    points=a.get("points", 0),
                ))
        return ChallengeProgress(
            best_points=rec.get("best_points", 0),
            max_points=rec.get("max_points", 0),
            attempts=attempts,
        )

    def _record_activity(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.data.get("streak_days", []):
            self.data.setdefault("streak_days", []).append(today)

    # ── Session tracking ──

    def start_session(self):
        """Mark the beginning of a study session."""
        self.data["current_session"] = {
            "started_at": datetime.now().isoformat(),
            "challenges_attempted": 0,
            "challenges_passed": 0,
            "points_earned": 0,
            "new_masteries": 0,
            "regressions": 0,
            "challenge_ids": [],
        }

    def record_session_attempt(self, challenge_id: str, passed: bool,
                               points: int, state_before: ChallengeState,
                               state_after: ChallengeState):
        """Record an attempt within the current session."""
        session = self.data.get("current_session")
        if not session:
            self.start_session()
            session = self.data["current_session"]

        session["challenges_attempted"] += 1
        if passed:
            session["challenges_passed"] += 1
            session["points_earned"] += points
        if state_after == ChallengeState.MASTERED and state_before != ChallengeState.MASTERED:
            session["new_masteries"] += 1
        if state_after == ChallengeState.REGRESSED and state_before != ChallengeState.REGRESSED:
            session["regressions"] += 1
        if challenge_id not in session.get("challenge_ids", []):
            session.setdefault("challenge_ids", []).append(challenge_id)

    def get_session_stats(self) -> Optional[Dict]:
        """Return current session stats, or None if no active session."""
        session = self.data.get("current_session")
        if not session:
            return None

        started = session.get("started_at", "")
        duration_min = 0
        if started:
            try:
                start_dt = datetime.fromisoformat(started)
                duration_min = int((datetime.now() - start_dt).total_seconds() / 60)
            except (ValueError, TypeError):
                pass

        return {
            "started_at": started,
            "duration_minutes": duration_min,
            "challenges_attempted": session.get("challenges_attempted", 0),
            "challenges_passed": session.get("challenges_passed", 0),
            "points_earned": session.get("points_earned", 0),
            "new_masteries": session.get("new_masteries", 0),
            "regressions": session.get("regressions", 0),
            "unique_challenges": len(session.get("challenge_ids", [])),
        }

    def end_session(self):
        """Archive current session stats and clear."""
        session = self.data.get("current_session")
        if session:
            session["ended_at"] = datetime.now().isoformat()
            self.data.setdefault("sessions", []).append(session)
            # Keep last 20 sessions
            self.data["sessions"] = self.data["sessions"][-20:]
            del self.data["current_session"]
            self._save()

    def get_session_goal(self) -> Dict:
        """Compute a session goal based on current learning state.

        Returns dict with:
            label: str — one-line Czech description
            target_type: str — "fix_regressions" | "new_challenges" | "practice"
            target_count: int — how many to aim for
            current: int — how many done in this session towards goal
        """
        session = self.data.get("current_session", {})
        regressed = self.get_regressed()
        in_progress = self.get_challenges_by_state(ChallengeState.IN_PROGRESS)

        if regressed:
            count = min(len(regressed), 3)
            done = session.get("regressions_fixed", 0)
            # Track regressions fixed: count new masteries for previously regressed
            return {
                "label": f"Oprav {count} regresi{'e' if count > 1 else ''}",
                "target_type": "fix_regressions",
                "target_count": count,
                "current": session.get("new_masteries", 0),
            }
        elif in_progress:
            count = min(len(in_progress), 3)
            return {
                "label": f"Dokonči {count} rozpracovan{'é' if count > 1 else 'ou'} výzv{'y' if count > 1 else 'u'}",
                "target_type": "practice",
                "target_count": count,
                "current": session.get("challenges_passed", 0),
            }
        else:
            return {
                "label": "Zvládni 3 nové výzvy",
                "target_type": "new_challenges",
                "target_count": 3,
                "current": session.get("challenges_passed", 0),
            }

    # ── Review tracking helpers ──

    def get_challenges_by_state(self, state: ChallengeState
                                ) -> List[Tuple[str, ChallengeProgress]]:
        """Get all challenges in a specific state."""
        results = []
        for k, v in sorted(self.data.get("challenges", {}).items()):
            cp = self._to_progress(v)
            if cp.state == state:
                results.append((k, cp))
        return results

    def get_regressed(self) -> List[Tuple[str, ChallengeProgress]]:
        return self.get_challenges_by_state(ChallengeState.REGRESSED)

    def get_mastered(self) -> List[Tuple[str, ChallengeProgress]]:
        return self.get_challenges_by_state(ChallengeState.MASTERED)
