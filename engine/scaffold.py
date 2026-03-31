"""
🏗️ Scaffold tool — generates lesson.yaml files from existing challenges.py.

Reads each challenges.py, loads challenges, and writes a lesson.yaml
with all metadata fields populated from inference. Authors can then
review and refine the generated metadata.

Usage:
    python3 -m engine.scaffold              # generate for all lessons
    python3 -m engine.scaffold 01           # generate for section 01
    python3 -m engine.scaffold --overwrite  # overwrite existing files
"""
import os
import re
import sys
from typing import Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _build_yaml_content(lesson_path: str, section_num: str,
                        lesson_num: str) -> Optional[str]:
    """Build lesson.yaml content from challenges.py analysis."""
    challenges_file = os.path.join(lesson_path, "challenges.py")
    if not os.path.isfile(challenges_file):
        return None

    # Extract info from directory name
    dir_name = os.path.basename(lesson_path)
    match = re.match(r"^\d{2}_(.+)$", dir_name)
    title = match.group(1).replace("_", " ").title() if match else dir_name

    # Read challenges.py
    try:
        with open(challenges_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return None

    # Extract module docstring for summary
    summary = ""
    doc_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
    if doc_match:
        lines = doc_match.group(1).strip().split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("🐍") and not line.startswith("#"):
                summary = line
                break

    # Count and analyze challenges
    challenge_blocks = re.findall(
        r'Challenge\(\s*(.*?)\s*\)', content, re.DOTALL
    )

    challenges_yaml = []
    difficulties = []
    for i, block in enumerate(challenge_blocks, 1):
        # Extract title
        title_match = re.search(r'title\s*=\s*["\'](.+?)["\']', block)
        ch_title = title_match.group(1) if title_match else f"Challenge {i}"

        # Extract difficulty
        diff_match = re.search(r'difficulty\s*=\s*(\d)', block)
        diff = int(diff_match.group(1)) if diff_match else 1
        difficulties.append(diff)

        # Extract points
        pts_match = re.search(r'points\s*=\s*(\d+)', block)
        pts = int(pts_match.group(1)) if pts_match else 10

        # Extract challenge_type
        type_match = re.search(r'challenge_type\s*=\s*["\'](\w+)["\']', block)
        ch_type = type_match.group(1) if type_match else _infer_type_from_context(
            content, i
        )

        challenges_yaml.append({
            "id": i,
            "title": ch_title,
            "type": ch_type,
            "difficulty": diff,
            "points": pts,
        })

    if not challenges_yaml:
        return None

    # Calculate lesson difficulty
    avg_diff = sum(difficulties) / len(difficulties) if difficulties else 1
    lesson_diff = 1 if avg_diff <= 1.3 else (2 if avg_diff <= 2.0 else 3)

    # Estimate minutes
    est_minutes = len(challenges_yaml) * 5 + lesson_diff * 5

    # Section tags
    from engine.content import SECTION_TAGS
    tags = SECTION_TAGS.get(section_num, [])

    # Build YAML string manually (no PyYAML dependency for generation)
    lines = [
        f'id: "{section_num}.{lesson_num}"',
        f'title: "{title}"',
        f'summary: "{_escape_yaml(summary)}"',
        f"difficulty: {lesson_diff}",
        f"estimated_minutes: {est_minutes}",
        f"tags: [{', '.join(repr(t) for t in tags)}]",
        "prerequisites: []",
        "learning_objectives: []",
        "",
        "# Lesson-level pedagogical content",
        'why_it_matters: ""',
        'what_you_will_learn: ""',
        'key_theory: ""',
        "",
        "challenges:",
    ]

    for ch in challenges_yaml:
        lines.append(f'  - id: {ch["id"]}')
        lines.append(f'    title: "{_escape_yaml(ch["title"])}"')
        lines.append(f'    type: {ch["type"]}')
        lines.append(f'    difficulty: {ch["difficulty"]}')
        lines.append(f'    points: {ch["points"]}')
        lines.append(f'    learning_objective: ""')
        lines.append(f'    tags: []')
        lines.append(f'    estimated_minutes: {ch["difficulty"] * 3 + 2}')
        lines.append(f'    hint_strategy: progressive')
        lines.append(f'    review_priority: normal')
        lines.append(f'    expected_misconceptions: []')
        lines.append(f'    mastery_rule: 3_consecutive')
        lines.append(f'    solution_pattern: ""')
        lines.append(f'    # Rich pedagogical content')
        lines.append(f'    why_it_matters: ""')
        lines.append(f'    what_you_will_learn: ""')
        lines.append(f'    key_concept: ""')
        lines.append(f'    worked_example: ""')
        lines.append(f'    common_mistakes: []')
        lines.append(f'    thinking_notes: ""')
        lines.append(f'    reference_solution: ""')
        lines.append(f'    solution_explanation: ""')
        lines.append(f'    practice_mode: guided')

    return "\n".join(lines) + "\n"


def _escape_yaml(s: str) -> str:
    """Escape special characters for YAML string values."""
    return s.replace('"', '\\"').replace("\n", " ")


def _infer_type_from_context(content: str, index: int) -> str:
    """Infer challenge type from the source code context."""
    # Find the corresponding vyzva function
    func_pattern = rf'def vyzva_{index}\b.*?(?=\ndef |\nchallenge|\n#\s*={3,}|\Z)'
    match = re.search(func_pattern, content, re.DOTALL)
    if match:
        func_body = match.group(0)
        if re.search(r'Vrať dict|Vrať slovník|return\s*\{', func_body):
            return "knowledge"
        body_lines = [
            l.strip() for l in func_body.split("\n")
            if l.strip() and not l.strip().startswith("#")
            and not l.strip().startswith('"""')
            and not l.strip().startswith("def ")
        ]
        if body_lines and all(
            l in ("pass", "...", "return ...", "return None", "return",
                  "return {}", "return []")
            or l.startswith("# TODO")
            for l in body_lines
        ):
            return "implementation"
    return "implementation"


def generate_lesson_yaml(lesson_path: str, section_num: str,
                         lesson_num: str, overwrite: bool = False) -> bool:
    """Generate lesson.yaml for a single lesson directory. Returns True if created."""
    yaml_path = os.path.join(lesson_path, "lesson.yaml")
    if os.path.exists(yaml_path) and not overwrite:
        return False

    content = _build_yaml_content(lesson_path, section_num, lesson_num)
    if not content:
        return False

    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def generate_all_yaml(section_filter: Optional[str] = None,
                      overwrite: bool = False) -> int:
    """Generate lesson.yaml for all lessons. Returns count of files created."""
    count = 0
    for section_dir in sorted(os.listdir(ROOT)):
        section_path = os.path.join(ROOT, section_dir)
        if not os.path.isdir(section_path) or not re.match(r"^\d{2}_", section_dir):
            continue

        sec_num = section_dir[:2]
        if section_filter and sec_num != section_filter:
            continue

        for lesson_dir in sorted(os.listdir(section_path)):
            lesson_path = os.path.join(section_path, lesson_dir)
            if not os.path.isdir(lesson_path):
                continue
            match = re.match(r"^(\d{2})_", lesson_dir)
            if not match:
                continue

            les_num = match.group(1)
            if generate_lesson_yaml(lesson_path, sec_num, les_num, overwrite):
                rel = os.path.relpath(lesson_path, ROOT)
                print(f"  ✅ {rel}/lesson.yaml")
                count += 1
    return count


def main():
    args = sys.argv[1:]
    section_filter = None
    overwrite = False

    for arg in args:
        if arg == "--overwrite":
            overwrite = True
        elif arg == "--help" or arg == "-h":
            print(__doc__.strip())
            sys.exit(0)
        elif re.match(r"^\d{2}$", arg):
            section_filter = arg
        else:
            print(f"Unknown argument: {arg}")
            sys.exit(1)

    count = generate_all_yaml(section_filter=section_filter, overwrite=overwrite)
    print(f"\n{'✅' if count > 0 else '⚠️'} Generated {count} lesson.yaml files")


if __name__ == "__main__":
    main()
