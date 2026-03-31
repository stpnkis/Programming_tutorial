"""
📝 Editor integration — open challenge files for editing with minimal friction.

Supports $EDITOR, VS Code, and common fallbacks.
"""
import os
import subprocess
import shutil


def get_editor() -> str:
    """Determine the best available editor."""
    # 1. Explicit env var
    editor = os.environ.get("EDITOR")
    if editor and shutil.which(editor):
        return editor

    # 2. VS Code (most likely for this project)
    for cmd in ("code", "codium"):
        if shutil.which(cmd):
            return cmd

    # 3. Common terminal editors
    for cmd in ("nano", "vim", "vi"):
        if shutil.which(cmd):
            return cmd

    return ""


def open_file(filepath: str, line: int = 0) -> bool:
    """Open a file in the user's editor at the given line.

    Returns True if the editor was launched successfully.
    """
    editor = get_editor()
    if not editor:
        return False

    filepath = os.path.abspath(filepath)
    if not os.path.isfile(filepath):
        return False

    try:
        base = os.path.basename(editor)
        if base in ("code", "codium"):
            # VS Code: --goto file:line
            arg = f"{filepath}:{line}" if line > 0 else filepath
            subprocess.Popen(
                [editor, "--goto", arg],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif base in ("vim", "vi", "nvim"):
            # vim: +line file
            args = [editor]
            if line > 0:
                args.append(f"+{line}")
            args.append(filepath)
            subprocess.call(args)
        elif base == "nano":
            args = [editor]
            if line > 0:
                args.append(f"+{line}")
            args.append(filepath)
            subprocess.call(args)
        else:
            # Generic: just open the file
            subprocess.Popen(
                [editor, filepath],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        return True
    except Exception:
        return False


def find_challenge_line(filepath: str, challenge_index: int) -> int:
    """Find the line number of a vyzva_N function in a challenges.py file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                if line.strip().startswith(f"def vyzva_{challenge_index}"):
                    return i
    except Exception:
        pass
    return 0
