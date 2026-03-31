"""
Workspace model — per-lesson draft management with autosave, reset, and compare.

Manages a user workspace directory (~/.progtrain/workspace/) that stores:
- Draft copies of challenge files (user's working code)
- Starter snapshots (original code at first open)
- Reference solutions (extracted from lesson.yaml)

Separation: starter code (immutable) / user draft (mutable) / reference (from content).
"""
from __future__ import annotations

import os
import shutil
import time
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORKSPACE_DIR = Path.home() / ".progtrain" / "workspace"


def _lesson_workspace(section_num: str, lesson_num: str) -> Path:
    return WORKSPACE_DIR / section_num / lesson_num


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _find_challenge_file(section_num: str, lesson_num: str) -> Optional[Path]:
    """Find the original challenges.py for a lesson by scanning content dirs."""
    from engine.content import discover_sections
    for s in discover_sections():
        if s.num != section_num:
            continue
        for l in s.lessons:
            if l.lesson_num != lesson_num:
                continue
            return Path(l.challenge_file)
    return None


def init_workspace(section_num: str, lesson_num: str) -> Dict[str, Any]:
    """Initialize workspace for a lesson if not already done.

    On first open:
    1. Copy challenges.py → workspace/starter.py (immutable snapshot)
    2. Copy challenges.py → workspace/draft.py (user's working copy)

    Returns workspace state info.
    """
    ws = _lesson_workspace(section_num, lesson_num)
    _ensure_dir(ws)

    challenge_file = _find_challenge_file(section_num, lesson_num)
    if challenge_file is None or not challenge_file.exists():
        return {"error": "Challenge file not found", "initialized": False}

    starter = ws / "starter.py"
    draft = ws / "draft.py"

    # First init: snapshot starter code
    if not starter.exists():
        shutil.copy2(challenge_file, starter)

    # If no draft yet, copy from original
    if not draft.exists():
        shutil.copy2(challenge_file, draft)
    
    return {
        "initialized": True,
        "workspace_path": str(ws),
        "has_draft": draft.exists(),
        "has_starter": starter.exists(),
    }


def get_draft(section_num: str, lesson_num: str) -> Dict[str, Any]:
    """Get the user's draft code. Auto-initializes workspace."""
    init_workspace(section_num, lesson_num)
    draft = _lesson_workspace(section_num, lesson_num) / "draft.py"
    
    if not draft.exists():
        # Fallback to original file
        challenge_file = _find_challenge_file(section_num, lesson_num)
        if challenge_file and challenge_file.exists():
            content = challenge_file.read_text(encoding="utf-8")
            rel = str(challenge_file.relative_to(ROOT))
            return {"content": content, "path": rel, "source": "original"}
        return {"error": "No draft or original file found"}

    content = draft.read_text(encoding="utf-8")
    challenge_file = _find_challenge_file(section_num, lesson_num)
    rel = str(challenge_file.relative_to(ROOT)) if challenge_file else ""
    return {
        "content": content,
        "path": rel,
        "source": "draft",
        "last_modified": draft.stat().st_mtime,
    }


def save_draft(section_num: str, lesson_num: str, content: str) -> Dict[str, Any]:
    """Save the user's draft code. Also writes back to original file for TUI compat."""
    init_workspace(section_num, lesson_num)
    ws = _lesson_workspace(section_num, lesson_num)
    draft = ws / "draft.py"

    # Save draft
    draft.write_text(content, encoding="utf-8")

    # Also write to the original challenge file (TUI compatibility)
    challenge_file = _find_challenge_file(section_num, lesson_num)
    if challenge_file and challenge_file.exists():
        challenge_file.write_text(content, encoding="utf-8")

    return {
        "success": True,
        "saved_at": time.time(),
    }


def get_starter(section_num: str, lesson_num: str) -> Dict[str, Any]:
    """Get the starter code (original snapshot)."""
    init_workspace(section_num, lesson_num)
    starter = _lesson_workspace(section_num, lesson_num) / "starter.py"
    if not starter.exists():
        return {"error": "No starter code snapshot"}
    return {"content": starter.read_text(encoding="utf-8")}


def reset_to_starter(section_num: str, lesson_num: str) -> Dict[str, Any]:
    """Reset draft back to starter code."""
    ws = _lesson_workspace(section_num, lesson_num)
    starter = ws / "starter.py"
    draft = ws / "draft.py"

    if not starter.exists():
        return {"error": "No starter code to reset to"}

    content = starter.read_text(encoding="utf-8")
    draft.write_text(content, encoding="utf-8")

    # Also write to original file
    challenge_file = _find_challenge_file(section_num, lesson_num)
    if challenge_file and challenge_file.exists():
        challenge_file.write_text(content, encoding="utf-8")

    return {"success": True, "content": content}


def get_reference_solution(section_num: str, lesson_num: str,
                           challenge_index: int) -> Dict[str, Any]:
    """Get reference solution for a specific challenge from lesson.yaml."""
    from engine.content import load_challenge_details, discover_sections

    for s in discover_sections():
        if s.num != section_num:
            continue
        for l in s.lessons:
            if l.lesson_num != lesson_num:
                continue
            details = load_challenge_details(s.num, l.lesson_num, l.challenge_file)
            for d in details:
                if d.index == challenge_index:
                    ref = getattr(d, "reference_solution", "")
                    expl = getattr(d, "solution_explanation", "")
                    if ref:
                        return {
                            "reference_solution": ref,
                            "solution_explanation": expl,
                            "title": d.title,
                        }
                    return {"error": "No reference solution available for this challenge"}
    return {"error": "Challenge not found"}


def get_workspace_info(section_num: str, lesson_num: str) -> Dict[str, Any]:
    """Get workspace metadata for a lesson."""
    ws = _lesson_workspace(section_num, lesson_num)
    draft = ws / "draft.py"
    starter = ws / "starter.py"

    return {
        "initialized": ws.exists(),
        "has_draft": draft.exists(),
        "has_starter": starter.exists(),
        "draft_modified": draft.stat().st_mtime if draft.exists() else None,
        "workspace_path": str(ws),
    }
