"""
🧠 Learning intelligence — recommendation engine, review queue, weak-area detection.

Provides smart guidance: what to work on next, what to review, what's weak.
All logic is transparent and deterministic — no magic.
"""
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Tuple

from engine.models import (
    ChallengeState, ChallengeProgress, SectionInfo, LessonInfo,
    MASTERY_THRESHOLD,
)


# ── Review intervals (simple escalating, not pseudo-SRS) ──

REVIEW_INTERVALS = {
    1: timedelta(days=1),    # first pass: review tomorrow
    2: timedelta(days=3),    # second pass: review in 3 days
    3: timedelta(days=7),    # mastery: review in a week
    6: timedelta(days=14),   # sustained mastery: review in 2 weeks
}


class ActionCategory(Enum):
    """What kind of action is recommended — in priority order."""
    FIX_REGRESSION = "fix_regression"     # was passing, now failing
    REVIEW_DUE = "review_due"             # passing but not practiced recently
    CONTINUE_WORK = "continue_work"       # in progress, never fully passed
    NEW_MATERIAL = "new_material"         # not started, next in sequence
    PRACTICE = "practice"                 # passing, good to reinforce
    CONCEPT_PRACTICE = "concept_practice" # tag-focused practice


@dataclass
class Recommendation:
    """A single recommended action for the learner."""
    category: ActionCategory
    challenge_id: str
    section_num: str
    lesson_num: str
    challenge_index: int
    reason: str                   # human-readable explanation
    priority: int = 0             # lower = higher priority
    lesson_name: str = ""
    section_name: str = ""


@dataclass
class LearningSnapshot:
    """Current state of the learner — used for dashboard and guidance."""
    total_challenges: int = 0
    mastered: int = 0
    currently_passing: int = 0
    in_progress: int = 0
    regressed: int = 0
    not_started: int = 0

    review_due_count: int = 0
    weak_areas: List[str] = field(default_factory=list)  # lesson IDs with issues

    recommendations: List[Recommendation] = field(default_factory=list)
    next_action: Optional[Recommendation] = None

    @property
    def mastery_pct(self) -> float:
        if self.total_challenges == 0:
            return 0.0
        return self.mastered / self.total_challenges

    @property
    def progress_pct(self) -> float:
        if self.total_challenges == 0:
            return 0.0
        return (self.mastered + self.currently_passing) / self.total_challenges


def _parse_iso(ts: str) -> Optional[datetime]:
    """Parse ISO timestamp, return None on failure."""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts)
    except (ValueError, TypeError):
        return None


def _get_review_interval(consecutive_passes: int) -> timedelta:
    """Get review interval based on consecutive pass count."""
    best_match = timedelta(days=1)
    for threshold, interval in sorted(REVIEW_INTERVALS.items()):
        if consecutive_passes >= threshold:
            best_match = interval
    return best_match


def _consecutive_passes(cp: ChallengeProgress) -> int:
    """Count consecutive passes from the end of attempt history."""
    count = 0
    for a in reversed(cp.attempts):
        if a.passed:
            count += 1
        else:
            break
    return count


def _last_pass_time(cp: ChallengeProgress) -> Optional[datetime]:
    """Find the timestamp of the most recent passing attempt."""
    for a in reversed(cp.attempts):
        if a.passed:
            return _parse_iso(a.at)
    return None


def is_review_due(cp: ChallengeProgress, now: Optional[datetime] = None) -> bool:
    """Check if a currently-passing/mastered challenge is due for review."""
    if cp.state not in (ChallengeState.CURRENTLY_PASSING, ChallengeState.MASTERED):
        return False

    now = now or datetime.now()
    last_pass = _last_pass_time(cp)
    if not last_pass:
        return False

    # Normalize timezone awareness: strip tzinfo if they don't match
    if now.tzinfo is not None and last_pass.tzinfo is None:
        last_pass = last_pass.replace(tzinfo=now.tzinfo)
    elif now.tzinfo is None and last_pass.tzinfo is not None:
        now = now.replace(tzinfo=last_pass.tzinfo)

    interval = _get_review_interval(_consecutive_passes(cp))
    return (now - last_pass) >= interval


def get_review_queue(progress, sections: List[SectionInfo],
                     now: Optional[datetime] = None) -> List[Recommendation]:
    """Build ordered list of challenges due for review."""
    now = now or datetime.now()
    queue = []

    for cid, rec in sorted(progress.data.get("challenges", {}).items()):
        cp = progress._to_progress(rec)
        if not is_review_due(cp, now):
            continue

        parts = cid.split(".")
        if len(parts) < 3:
            continue
        sec_num, les_num, ch_idx = parts[0], parts[1], parts[2]

        # Resolve names
        sec_name, les_name = _resolve_names(sections, sec_num, les_num)

        last_pass = _last_pass_time(cp)
        days_ago = (now - last_pass).days if last_pass else 0

        queue.append(Recommendation(
            category=ActionCategory.REVIEW_DUE,
            challenge_id=cid,
            section_num=sec_num,
            lesson_num=les_num,
            challenge_index=int(ch_idx),
            reason=f"Naposledy úspěšně před {days_ago} dny",
            priority=10 + days_ago,  # older = slightly lower priority
            lesson_name=les_name,
            section_name=sec_name,
        ))

    queue.sort(key=lambda r: r.priority)
    return queue


def get_weak_areas(progress, sections: List[SectionInfo]) -> List[Dict]:
    """Identify lessons where the learner struggles.

    A lesson is 'weak' if it has:
    - Any regressed challenges, OR
    - Challenges with 3+ failed attempts and no passes
    """
    weak = []

    for section in sections:
        for lesson in section.lessons:
            regressed = 0
            struggling = 0  # many fails, no pass
            total = 0

            prefix = f"{lesson.section_num}.{lesson.lesson_num}."
            for cid, rec in progress.data.get("challenges", {}).items():
                if not cid.startswith(prefix):
                    continue
                total += 1
                cp = progress._to_progress(rec)
                if cp.state == ChallengeState.REGRESSED:
                    regressed += 1
                elif cp.state == ChallengeState.IN_PROGRESS and cp.attempt_count >= 3:
                    struggling += 1

            if regressed > 0 or struggling > 0:
                weak.append({
                    "lesson_id": lesson.lesson_id,
                    "lesson_name": lesson.name,
                    "section_name": section.name,
                    "section_num": lesson.section_num,
                    "lesson_num": lesson.lesson_num,
                    "regressed": regressed,
                    "struggling": struggling,
                    "total": total,
                })

    # Sort by severity: regressed first, then struggling
    weak.sort(key=lambda w: (-w["regressed"], -w["struggling"]))
    return weak


def get_smart_recommendations(progress, sections: List[SectionInfo],
                              now: Optional[datetime] = None,
                              limit: int = 5) -> List[Recommendation]:
    """Build a prioritized list of recommendations across all categories.

    Priority order:
    1. Fix regressions (was passing, now failing)
    2. Review due (passing but not practiced recently)
    3. Continue work (in-progress, partially done)
    4. New material (first not-started lesson in sequence)
    """
    now = now or datetime.now()
    recs = []
    priority = 0

    # 1. Regressions — highest priority
    for cid, rec in sorted(progress.data.get("challenges", {}).items()):
        cp = progress._to_progress(rec)
        if cp.state != ChallengeState.REGRESSED:
            continue

        parts = cid.split(".")
        if len(parts) < 3:
            continue
        sec_num, les_num, ch_idx = parts[0], parts[1], parts[2]
        sec_name, les_name = _resolve_names(sections, sec_num, les_num)

        recs.append(Recommendation(
            category=ActionCategory.FIX_REGRESSION,
            challenge_id=cid,
            section_num=sec_num,
            lesson_num=les_num,
            challenge_index=int(ch_idx),
            reason="Dříve procházelo, teď ne — oprav to",
            priority=priority,
            lesson_name=les_name,
            section_name=sec_name,
        ))
        priority += 1

    # 2. Review due
    for r in get_review_queue(progress, sections, now):
        r.priority = 100 + r.priority
        recs.append(r)

    # 3. Continue work — in-progress challenges
    for cid, rec in sorted(progress.data.get("challenges", {}).items()):
        cp = progress._to_progress(rec)
        if cp.state != ChallengeState.IN_PROGRESS:
            continue

        parts = cid.split(".")
        if len(parts) < 3:
            continue
        sec_num, les_num, ch_idx = parts[0], parts[1], parts[2]
        sec_name, les_name = _resolve_names(sections, sec_num, les_num)

        recs.append(Recommendation(
            category=ActionCategory.CONTINUE_WORK,
            challenge_id=cid,
            section_num=sec_num,
            lesson_num=les_num,
            challenge_index=int(ch_idx),
            reason=f"Rozpracováno ({cp.attempt_count} pokusů)",
            priority=200 + cp.attempt_count,
            lesson_name=les_name,
            section_name=sec_name,
        ))
        priority += 1

    # 4. New material — first not-started lesson
    for section in sections:
        for lesson in section.lessons:
            if lesson.challenge_count == 0:
                continue
            completed = progress.get_lesson_completed(
                lesson.section_num, lesson.lesson_num)
            ever = progress.get_lesson_ever_passed(
                lesson.section_num, lesson.lesson_num)
            if completed == 0 and ever == 0:
                recs.append(Recommendation(
                    category=ActionCategory.NEW_MATERIAL,
                    challenge_id=f"{lesson.section_num}.{lesson.lesson_num}.1",
                    section_num=lesson.section_num,
                    lesson_num=lesson.lesson_num,
                    challenge_index=1,
                    reason="Další nová lekce v pořadí",
                    priority=300,
                    lesson_name=lesson.name,
                    section_name=section.name,
                ))
                break  # Only first not-started per section
        else:
            continue

    recs.sort(key=lambda r: r.priority)
    return recs[:limit]


def build_snapshot(progress, sections: List[SectionInfo],
                   now: Optional[datetime] = None) -> LearningSnapshot:
    """Build a complete picture of the learner's current state."""
    now = now or datetime.now()

    state_counts = progress.get_state_counts()
    total = sum(lesson.challenge_count for s in sections for lesson in s.lessons)

    recs = get_smart_recommendations(progress, sections, now, limit=5)
    weak = get_weak_areas(progress, sections)
    review = get_review_queue(progress, sections, now)

    snap = LearningSnapshot(
        total_challenges=total,
        mastered=state_counts.get(ChallengeState.MASTERED, 0),
        currently_passing=state_counts.get(ChallengeState.CURRENTLY_PASSING, 0),
        in_progress=state_counts.get(ChallengeState.IN_PROGRESS, 0),
        regressed=state_counts.get(ChallengeState.REGRESSED, 0),
        not_started=total - sum(state_counts.values()),
        review_due_count=len(review),
        weak_areas=[w["lesson_id"] for w in weak],
        recommendations=recs,
        next_action=recs[0] if recs else None,
    )
    return snap


def _resolve_names(sections: List[SectionInfo],
                   sec_num: str, les_num: str) -> Tuple[str, str]:
    """Resolve section/lesson display names from their numbers."""
    for s in sections:
        if s.num == sec_num:
            for l in s.lessons:
                if l.lesson_num == les_num:
                    return s.name, l.name
            return s.name, f"Lekce {les_num}"
    return f"Sekce {sec_num}", f"Lekce {les_num}"


def get_concept_recommendations(
    progress, sections: List[SectionInfo],
    tag: str, limit: int = 10,
) -> List[Recommendation]:
    """Get recommendations filtered by concept tag.

    Returns challenges matching the tag, prioritized:
    regressed > in_progress > not_started > passing (for review).
    """
    tag_lower = tag.lower()
    recs = []

    for section in sections:
        if not any(tag_lower in t.lower()
                   for t in section.lessons[0].meta.tags if section.lessons):
            # Quick check: skip sections with no matching tags
            sec_tags = []
            for lesson in section.lessons:
                sec_tags.extend(lesson.meta.tags)
            if not any(tag_lower in t.lower() for t in sec_tags):
                continue

        for lesson in section.lessons:
            lesson_tags = [t.lower() for t in lesson.meta.tags]
            if tag_lower not in lesson_tags:
                continue

            for i in range(1, lesson.challenge_count + 1):
                cid = f"{lesson.section_num}.{lesson.lesson_num}.{i}"
                cp = progress.get_challenge(cid)
                state = cp.state

                if state == ChallengeState.REGRESSED:
                    cat = ActionCategory.FIX_REGRESSION
                    reason = "Regrese v tomto konceptu"
                    priority = 0
                elif state == ChallengeState.IN_PROGRESS:
                    cat = ActionCategory.CONTINUE_WORK
                    reason = f"Rozpracováno ({cp.attempt_count} pokusů)"
                    priority = 100
                elif state == ChallengeState.NOT_STARTED:
                    cat = ActionCategory.CONCEPT_PRACTICE
                    reason = f"Nová výzva — koncept: {tag}"
                    priority = 200
                elif is_review_due(cp):
                    cat = ActionCategory.REVIEW_DUE
                    reason = "K opakování"
                    priority = 50
                else:
                    continue  # mastered and not due

                recs.append(Recommendation(
                    category=cat,
                    challenge_id=cid,
                    section_num=lesson.section_num,
                    lesson_num=lesson.lesson_num,
                    challenge_index=i,
                    reason=reason,
                    priority=priority,
                    lesson_name=lesson.name,
                    section_name=section.name,
                ))

    recs.sort(key=lambda r: r.priority)
    return recs[:limit]


def get_available_tags(sections: List[SectionInfo]) -> List[str]:
    """Collect all unique tags across all lessons."""
    tags = set()
    for section in sections:
        for lesson in section.lessons:
            tags.update(lesson.meta.tags)
    return sorted(tags)


def categorize_recommendations(
    progress, sections: List[SectionInfo],
    now: Optional[datetime] = None,
    limit: int = 20,
) -> Dict[str, List[Recommendation]]:
    """Get recommendations categorized by action type.

    Returns dict with keys: 'regressions', 'review', 'continue', 'new'.
    """
    now = now or datetime.now()
    result: Dict[str, List[Recommendation]] = {
        "regressions": [],
        "review": [],
        "continue": [],
        "new": [],
    }

    # Regressions
    for cid, rec in sorted(progress.data.get("challenges", {}).items()):
        cp = progress._to_progress(rec)
        if cp.state != ChallengeState.REGRESSED:
            continue
        parts = cid.split(".")
        if len(parts) < 3:
            continue
        sec_num, les_num, ch_idx = parts[0], parts[1], parts[2]
        sec_name, les_name = _resolve_names(sections, sec_num, les_num)
        result["regressions"].append(Recommendation(
            category=ActionCategory.FIX_REGRESSION,
            challenge_id=cid,
            section_num=sec_num, lesson_num=les_num,
            challenge_index=int(ch_idx),
            reason="Dříve procházelo, teď ne",
            lesson_name=les_name, section_name=sec_name,
        ))

    # Review due
    result["review"] = get_review_queue(progress, sections, now)[:limit]

    # Continue work
    for cid, rec in sorted(progress.data.get("challenges", {}).items()):
        cp = progress._to_progress(rec)
        if cp.state != ChallengeState.IN_PROGRESS:
            continue
        parts = cid.split(".")
        if len(parts) < 3:
            continue
        sec_num, les_num, ch_idx = parts[0], parts[1], parts[2]
        sec_name, les_name = _resolve_names(sections, sec_num, les_num)
        result["continue"].append(Recommendation(
            category=ActionCategory.CONTINUE_WORK,
            challenge_id=cid,
            section_num=sec_num, lesson_num=les_num,
            challenge_index=int(ch_idx),
            reason=f"Rozpracováno ({cp.attempt_count} pokusů)",
            lesson_name=les_name, section_name=sec_name,
        ))

    # New material
    for section in sections:
        for lesson in section.lessons:
            if lesson.challenge_count == 0:
                continue
            completed = progress.get_lesson_completed(
                lesson.section_num, lesson.lesson_num)
            ever = progress.get_lesson_ever_passed(
                lesson.section_num, lesson.lesson_num)
            if completed == 0 and ever == 0:
                result["new"].append(Recommendation(
                    category=ActionCategory.NEW_MATERIAL,
                    challenge_id=f"{lesson.section_num}.{lesson.lesson_num}.1",
                    section_num=lesson.section_num,
                    lesson_num=lesson.lesson_num,
                    challenge_index=1,
                    reason="Další nová lekce v pořadí",
                    lesson_name=lesson.name,
                    section_name=section.name,
                ))
                break

    return result
