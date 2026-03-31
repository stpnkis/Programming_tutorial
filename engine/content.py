"""Content discovery: scans filesystem for sections, lessons, challenges.
Also handles metadata loading, challenge type inference, and search index."""
import os
import re
import sys
import importlib.util
from typing import List, Optional, Dict

from engine.models import (
    SectionInfo, LessonInfo, LessonMeta, ChallengeDetail, ChallengeType,
)

# Display metadata for known sections (emoji + human-readable name)
SECTION_META = {
    "01": ("Python Základy", "🐍"),
    "02": ("OOP", "🏗️"),
    "03": ("Datové Struktury & Algoritmy", "🌳"),
    "04": ("Git & Workflow", "📝"),
    "05": ("Testing", "🧪"),
    "06": ("Čtení & Debugování Kódu", "🔍"),
    "07": ("NumPy & Matematika", "📐"),
    "08": ("Machine Learning", "🤖"),
    "09": ("Computer Vision", "👁️"),
    "10": ("ROS2", "🤖"),
    "11": ("Linux & Terminál", "🐧"),
    "12": ("Networking & API", "🌐"),
    "13": ("Paralelismus & Async", "⚡"),
    "14": ("Projekty & Portfolio", "🏆"),
}

# Section-level tags for search and filtering
SECTION_TAGS = {
    "01": ["python", "basics", "fundamentals"],
    "02": ["python", "oop", "classes"],
    "03": ["algorithms", "data-structures"],
    "04": ["git", "workflow", "vcs"],
    "05": ["testing", "pytest", "quality"],
    "06": ["debugging", "reading-code", "profiling"],
    "07": ["numpy", "math", "visualization"],
    "08": ["ml", "machine-learning", "sklearn"],
    "09": ["cv", "computer-vision", "opencv"],
    "10": ["ros2", "robotics"],
    "11": ["linux", "terminal", "bash"],
    "12": ["networking", "api", "http"],
    "13": ["async", "threading", "parallel"],
    "14": ["projects", "portfolio"],
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def discover_sections() -> List[SectionInfo]:
    """Discover all sections from numbered directories in the repo root."""
    sections = []
    for entry in sorted(os.listdir(ROOT)):
        path = os.path.join(ROOT, entry)
        if not os.path.isdir(path):
            continue
        match = re.match(r'^(\d{2})_', entry)
        if not match:
            continue
        num = match.group(1)
        fallback_name = entry.split('_', 1)[1].replace('_', ' ').title() if '_' in entry else entry
        name, emoji = SECTION_META.get(num, (fallback_name, "📦"))
        section = SectionInfo(num=num, name=name, emoji=emoji, dir_name=entry, path=path)
        section.lessons = _discover_lessons(section)
        sections.append(section)
    return sections


def _discover_lessons(section: SectionInfo) -> List[LessonInfo]:
    """Discover lessons (subdirectories with challenges.py) within a section."""
    lessons = []
    for entry in sorted(os.listdir(section.path)):
        subpath = os.path.join(section.path, entry)
        challenge_file = os.path.join(subpath, "challenges.py")
        if not os.path.isdir(subpath) or not os.path.isfile(challenge_file):
            continue
        match = re.match(r'^(\d{2})_(.+)$', entry)
        if not match:
            continue
        lesson_num = match.group(1)
        raw_name = match.group(2).replace('_', ' ').title()
        count = _count_challenges_fast(challenge_file)
        meta = _load_lesson_meta(subpath, section.num)
        lessons.append(LessonInfo(
            section_num=section.num,
            lesson_num=lesson_num,
            name=raw_name,
            dir_name=entry,
            path=subpath,
            challenge_file=challenge_file,
            challenge_count=count,
            meta=meta,
        ))
    return lessons


def _count_challenges_fast(filepath: str) -> int:
    """Fast approximate challenge count by parsing the file for Challenge( patterns."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return len(re.findall(r'^\s+Challenge\(', content, re.MULTILINE))
    except Exception:
        return 0


def _load_lesson_meta(lesson_path: str, section_num: str) -> LessonMeta:
    """Load metadata from lesson.yaml (preferred) or meta.yml, with inference fallback."""
    meta = LessonMeta()

    # Try lesson.yaml first (new canonical format)
    yaml_file = os.path.join(lesson_path, "lesson.yaml")
    if not os.path.isfile(yaml_file):
        # Fallback to old meta.yml
        yaml_file = os.path.join(lesson_path, "meta.yml")

    if os.path.isfile(yaml_file):
        try:
            import yaml
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            meta.summary = data.get("summary", "")
            meta.difficulty = data.get("difficulty", 0)
            meta.estimated_minutes = data.get("estimated_minutes", 0)
            meta.tags = data.get("tags", [])
            meta.prerequisites = data.get("prerequisites", [])
            meta.learning_objectives = data.get("learning_objectives", [])
            # Lesson-level pedagogical content
            meta.why_it_matters = data.get("why_it_matters", "")
            meta.what_you_will_learn = data.get("what_you_will_learn", "")
            meta.key_theory = data.get("key_theory", "")
            if meta.summary or meta.difficulty:
                return meta  # explicit metadata found, use it
        except Exception:
            pass

    # Fallback: infer from content
    meta.tags = SECTION_TAGS.get(section_num, [])
    challenge_file = os.path.join(lesson_path, "challenges.py")
    if os.path.isfile(challenge_file):
        meta.summary = _infer_summary(challenge_file)
        meta.difficulty = _infer_difficulty(challenge_file)
    return meta


def _infer_summary(filepath: str) -> str:
    """Extract summary from the module docstring."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(2000)
        match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if match:
            lines = match.group(1).strip().split('\n')
            # Skip title line (usually has emoji), take the subtitle
            for line in lines:
                line = line.strip()
                if line and not line.startswith('🐍') and not line.startswith('#'):
                    return line
    except Exception:
        pass
    return ""


def _infer_difficulty(filepath: str) -> int:
    """Infer lesson difficulty from challenge difficulties."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        diffs = [int(m) for m in re.findall(r'difficulty=(\d)', content)]
        if diffs:
            avg = sum(diffs) / len(diffs)
            if avg <= 1.3:
                return 1
            elif avg <= 2.0:
                return 2
            return 3
    except Exception:
        pass
    return 0


def load_challenges(filepath: str):
    """Load Challenge objects from a challenge file by importing the module.

    Returns list of Challenge objects, or empty list on error.
    """
    try:
        mod_name = f"_challenge_{id(filepath)}_{os.path.getmtime(filepath)}"
        spec = importlib.util.spec_from_file_location(mod_name, filepath)
        if spec is None or spec.loader is None:
            return []
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, 'challenges', [])
    except Exception:
        return []


def load_challenge_details(section_num: str, lesson_num: str,
                           filepath: str) -> List[ChallengeDetail]:
    """Load challenges and convert to enriched ChallengeDetail objects."""
    raw = load_challenges(filepath)
    details = []

    # Try loading explicit metadata from lesson.yaml
    yaml_meta = _load_yaml_challenge_meta(os.path.dirname(filepath))

    for i, ch in enumerate(raw, 1):
        cid = f"{section_num}.{lesson_num}.{i}"

        # Explicit metadata from YAML takes priority
        yaml_ch = yaml_meta.get(i, {})
        explicit_type = yaml_ch.get("type")
        if explicit_type:
            try:
                ctype = ChallengeType(explicit_type)
            except ValueError:
                ctype = _infer_challenge_type(ch, filepath, i)
        else:
            ctype = _infer_challenge_type(ch, filepath, i)

        explicit_diff = yaml_ch.get("difficulty")
        diff = explicit_diff if explicit_diff else getattr(ch, 'difficulty', 1)

        explicit_pts = yaml_ch.get("points")
        pts = explicit_pts if explicit_pts else getattr(ch, 'points', 10)

        details.append(ChallengeDetail(
            index=i,
            challenge_id=cid,
            title=ch.title,
            description=getattr(ch, 'description', ''),
            task=getattr(ch, 'task', ''),
            theory=getattr(ch, 'theory', '') or '',
            example=getattr(ch, 'example', '') or '',
            example_output=getattr(ch, 'example_output', '') or '',
            hints=getattr(ch, 'hints', []) or [],
            difficulty=diff,
            points=pts,
            challenge_type=ctype,
            tests=getattr(ch, 'tests', []) or [],
            # Challenge-level metadata from YAML
            tags=yaml_ch.get("tags", []),
            estimated_minutes=yaml_ch.get("estimated_minutes", 0),
            learning_objective=yaml_ch.get("learning_objective", ""),
            prerequisites=yaml_ch.get("prerequisites", []),
            hint_strategy=yaml_ch.get("hint_strategy", "progressive"),
            review_priority=yaml_ch.get("review_priority", "normal"),
            expected_misconceptions=yaml_ch.get("expected_misconceptions", []),
            mastery_rule=yaml_ch.get("mastery_rule", "3_consecutive"),
            solution_pattern=yaml_ch.get("solution_pattern", ""),
            # Rich pedagogical content
            why_it_matters=yaml_ch.get("why_it_matters", ""),
            what_you_will_learn=yaml_ch.get("what_you_will_learn", ""),
            key_concept=yaml_ch.get("key_concept", ""),
            worked_example=yaml_ch.get("worked_example", ""),
            common_mistakes=yaml_ch.get("common_mistakes", []),
            thinking_notes=yaml_ch.get("thinking_notes", ""),
            reference_solution=yaml_ch.get("reference_solution", ""),
            solution_explanation=yaml_ch.get("solution_explanation", ""),
            practice_mode=yaml_ch.get("practice_mode", "guided"),
        ))
    return details


def _load_yaml_challenge_meta(lesson_path: str) -> Dict[int, Dict]:
    """Load per-challenge metadata from lesson.yaml if available.

    Returns dict mapping challenge index (1-based) to metadata dict.
    """
    yaml_file = os.path.join(lesson_path, "lesson.yaml")
    if not os.path.isfile(yaml_file):
        return {}

    try:
        import yaml
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        return {}

    challenges = data.get("challenges", [])
    if not isinstance(challenges, list):
        return {}

    result = {}
    for ch in challenges:
        if isinstance(ch, dict) and "id" in ch:
            result[ch["id"]] = ch
    return result


def _infer_challenge_type(ch, filepath: str, index: int) -> ChallengeType:
    """Infer the type of a challenge from its properties and source code."""
    # Explicit type from Challenge object
    explicit = getattr(ch, 'challenge_type', None)
    if explicit:
        try:
            return ChallengeType(explicit)
        except ValueError:
            pass

    # Heuristic: read the source function body
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the corresponding vyzva function
        func_pattern = rf'def vyzva_{index}\b.*?(?=\ndef |\nchallenge|\n#\s*={3,}|\Z)'
        match = re.search(func_pattern, content, re.DOTALL)
        if match:
            func_body = match.group(0)

            # Check for dict/knowledge patterns
            if re.search(r'Vrať dict|Vrať slovník|return\s*\{', func_body):
                return ChallengeType.KNOWLEDGE

            # Check if body is essentially empty (pass, ..., return None)
            lines = [l.strip() for l in func_body.split('\n')
                     if l.strip() and not l.strip().startswith('#')
                     and not l.strip().startswith('"""')
                     and not l.strip().startswith("'''")]
            body_lines = [l for l in lines if not l.startswith('def ')]
            if body_lines and all(
                l in ('pass', '...', 'return ...', 'return None',
                       'return', 'return {}', 'return []')
                or l.startswith('# TODO')
                for l in body_lines
            ):
                return ChallengeType.IMPLEMENTATION

    except Exception:
        pass

    return ChallengeType.IMPLEMENTATION


def run_single_challenge(detail: ChallengeDetail):
    """Run a single challenge's tests and return (passed, messages, error)."""
    if not detail.tests:
        return True, ["Bez automatických testů"], None

    messages = []
    for test_fn in detail.tests:
        try:
            passed, msg = test_fn()
            messages.append(msg)
            if not passed:
                return False, messages, msg
        except Exception as e:
            error_msg = str(e)
            messages.append(f"Chyba: {error_msg}")
            return False, messages, error_msg

    return True, messages, None


def search_lessons(sections: List[SectionInfo], query: str) -> List[LessonInfo]:
    """Search lessons by name, tags, or summary. Case-insensitive."""
    query_lower = query.lower()
    results = []
    for section in sections:
        # Check section name too
        section_match = query_lower in section.name.lower()
        for lesson in section.lessons:
            if (section_match
                    or query_lower in lesson.name.lower()
                    or query_lower in lesson.meta.summary.lower()
                    or any(query_lower in t for t in lesson.meta.tags)):
                results.append(lesson)
    return results


def get_recommended_next(sections: List[SectionInfo],
                         progress) -> Optional[LessonInfo]:
    """Find the best next lesson to work on.

    Priority:
    1. In-progress lessons (partially done)
    2. First not-started lesson in the earliest incomplete section
    """
    # First: find in-progress lessons
    for section in sections:
        for lesson in section.lessons:
            if lesson.challenge_count == 0:
                continue
            completed = progress.get_lesson_completed(
                lesson.section_num, lesson.lesson_num)
            if 0 < completed < lesson.challenge_count:
                return lesson

    # Then: first not-started lesson
    for section in sections:
        for lesson in section.lessons:
            if lesson.challenge_count == 0:
                continue
            completed = progress.get_lesson_completed(
                lesson.section_num, lesson.lesson_num)
            if completed == 0:
                return lesson

    return None
