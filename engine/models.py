"""Domain models for the training center."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


# ── Enums ──

class ChallengeState(Enum):
    """Learning state for a single challenge, derived from attempt history."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"            # attempted, never passed
    CURRENTLY_PASSING = "currently_passing"  # last run passed
    MASTERED = "mastered"                   # 3+ consecutive passes
    REGRESSED = "regressed"                 # passed before, last run failed


class ChallengeType(Enum):
    """Type of challenge — affects UI rendering, feedback, and mastery logic."""
    IMPLEMENTATION = "implementation"  # write code from scratch (body is pass/...)
    KNOWLEDGE = "knowledge"            # return correct data structure
    DEBUGGING = "debugging"            # fix broken code
    REFACTORING = "refactoring"        # improve existing code
    TRACE = "trace"                    # trace execution and predict output
    OPEN = "open"                      # open-ended / creative task


MASTERY_THRESHOLD = 3  # consecutive passes needed for mastery

# State display config
STATE_DISPLAY = {
    ChallengeState.NOT_STARTED: ("⬜", "dim", "Nezahájeno"),
    ChallengeState.IN_PROGRESS: ("🔶", "yellow", "Rozpracováno"),
    ChallengeState.CURRENTLY_PASSING: ("✅", "green", "Projde"),
    ChallengeState.MASTERED: ("💎", "bold green", "Zvládnuto"),
    ChallengeState.REGRESSED: ("🔻", "red", "Regrese"),
}

TYPE_DISPLAY = {
    ChallengeType.IMPLEMENTATION: ("impl", "cyan"),
    ChallengeType.KNOWLEDGE: ("knowledge", "magenta"),
    ChallengeType.DEBUGGING: ("debug", "yellow"),
    ChallengeType.REFACTORING: ("refactor", "blue"),
    ChallengeType.TRACE: ("trace", "green"),
    ChallengeType.OPEN: ("open", "bright_cyan"),
}


# ── Attempt / Progress records ──

@dataclass
class AttemptRecord:
    """Single attempt at a challenge."""
    at: str       # ISO timestamp
    passed: bool
    points: int = 0


@dataclass
class ChallengeProgress:
    """Per-challenge progress with full attempt history."""
    best_points: int = 0
    max_points: int = 0
    attempts: List[AttemptRecord] = field(default_factory=list)

    @property
    def state(self) -> ChallengeState:
        """Compute state from attempt history — this is the source of truth."""
        if not self.attempts:
            return ChallengeState.NOT_STARTED

        any_pass = any(a.passed for a in self.attempts)
        last = self.attempts[-1]

        if not any_pass:
            return ChallengeState.IN_PROGRESS

        if not last.passed:
            return ChallengeState.REGRESSED

        # Last attempt passed — check for mastery
        consecutive = 0
        for a in reversed(self.attempts):
            if a.passed:
                consecutive += 1
            else:
                break

        if consecutive >= MASTERY_THRESHOLD:
            return ChallengeState.MASTERED

        return ChallengeState.CURRENTLY_PASSING

    @property
    def ever_passed(self) -> bool:
        return any(a.passed for a in self.attempts)

    @property
    def attempt_count(self) -> int:
        return len(self.attempts)

    @property
    def last_attempt_at(self) -> Optional[str]:
        return self.attempts[-1].at if self.attempts else None

    @property
    def last_error(self) -> Optional[str]:
        """Return the error message from the most recent failed attempt, if any."""
        for a in reversed(self.attempts):
            if not a.passed and hasattr(a, 'error') and a.error:
                return a.error
        return None


# ── Content structures ──

@dataclass
class SectionInfo:
    """Discovered section from filesystem."""
    num: str              # "01"
    name: str             # "Python Základy"
    emoji: str            # "🐍"
    dir_name: str         # "01_Python_Zaklady"
    path: str             # absolute path
    lessons: List['LessonInfo'] = field(default_factory=list)


@dataclass
class LessonMeta:
    """Optional metadata for a lesson (from meta.yml or inferred)."""
    summary: str = ""
    difficulty: int = 0          # 0=unknown, 1-3
    estimated_minutes: int = 0
    tags: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)
    # Lesson-level pedagogical content
    why_it_matters: str = ""          # why this topic is important
    what_you_will_learn: str = ""     # capabilities after completion
    key_theory: str = ""              # concise essential theory


@dataclass
class LessonInfo:
    """Discovered lesson from filesystem."""
    section_num: str      # "01"
    lesson_num: str       # "01"
    name: str             # "Datové Typy"
    dir_name: str         # "01_datove_typy"
    path: str             # absolute path
    challenge_file: str   # absolute path to challenges.py
    challenge_count: int = 0
    meta: LessonMeta = field(default_factory=LessonMeta)

    @property
    def lesson_id(self) -> str:
        return f"{self.section_num}.{self.lesson_num}"


@dataclass
class ChallengeDetail:
    """Runtime detail of a loaded challenge, enriched with metadata."""
    index: int                # 1-based index within lesson
    challenge_id: str         # "01.01.1"
    title: str
    description: str = ""
    task: str = ""
    theory: str = ""
    example: str = ""
    example_output: str = ""
    hints: List[str] = field(default_factory=list)
    difficulty: int = 1
    points: int = 10
    challenge_type: ChallengeType = ChallengeType.IMPLEMENTATION
    tests: list = field(default_factory=list, repr=False)
    # Challenge-level metadata (from lesson.yaml)
    tags: List[str] = field(default_factory=list)
    estimated_minutes: int = 0
    learning_objective: str = ""
    prerequisites: List[str] = field(default_factory=list)
    hint_strategy: str = "progressive"     # progressive | contextual | conceptual
    review_priority: str = "normal"        # low | normal | high | critical
    expected_misconceptions: List[str] = field(default_factory=list)
    mastery_rule: str = "3_consecutive"    # 3_consecutive | 2_consecutive | single_pass
    solution_pattern: str = ""             # expected output shape for feedback
    # Rich pedagogical content (from lesson.yaml challenge-level or inferred)
    why_it_matters: str = ""               # why this challenge matters
    what_you_will_learn: str = ""          # what skill this builds
    key_concept: str = ""                  # core concept in brief
    worked_example: str = ""               # step-by-step worked example
    common_mistakes: List[str] = field(default_factory=list)  # frequent errors
    thinking_notes: str = ""               # how to reason about this
    reference_solution: str = ""           # ideal solution code
    solution_explanation: str = ""         # why the solution works
    practice_mode: str = "guided"          # guided | open | creative


@dataclass
class RunResult:
    """Result of running a single challenge."""
    challenge_id: str
    passed: bool
    points_earned: int
    max_points: int
    messages: List[str] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class TestResult:
    """Result of running a single test within a challenge."""
    passed: bool
    message: str
    error: Optional[str] = None
