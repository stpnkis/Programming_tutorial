"""
Flask API server — exposes the learning engine as REST endpoints.

Runs in a background thread when launched from the PySide6 desktop shell,
or standalone for development (python3 -m desktop.server).
"""

from __future__ import annotations

import atexit
import os
import threading
from typing import Optional

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import engine.services as svc
from engine.workspace import (
    get_draft,
    save_draft,
    get_starter,
    reset_to_starter,
    get_reference_solution,
    get_workspace_info,
    init_workspace,
)
from engine.lab import (
    get_repl,
    get_terminal,
    reset_repl,
    reset_terminal,
    shutdown_all,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

app = Flask(__name__, static_folder=STATIC, static_url_path="/static")
CORS(app)  # allow QWebEngineView origin

# Clean up lab sessions on exit
atexit.register(shutdown_all)


# ── Static / SPA ─────────────────────────────────────────────


@app.route("/")
def index():
    return send_from_directory(STATIC, "index.html")


# ── Content endpoints ────────────────────────────────────────


@app.route("/api/sections")
def api_sections():
    return jsonify(svc.get_sections())


@app.route("/api/lessons/<section_num>/<lesson_num>")
def api_lesson_detail(section_num: str, lesson_num: str):
    data = svc.get_lesson_detail(section_num, lesson_num)
    if data is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(data)


@app.route("/api/search")
def api_search():
    q = request.args.get("q", "")
    if not q:
        return jsonify([])
    return jsonify(svc.search(q))


# ── Progress endpoints ───────────────────────────────────────


@app.route("/api/progress/snapshot")
def api_snapshot():
    return jsonify(svc.get_progress_snapshot())


@app.route("/api/progress/<challenge_id>")
def api_challenge_progress(challenge_id: str):
    return jsonify(svc.get_challenge_progress(challenge_id))


# ── Recommendation endpoints ────────────────────────────────


@app.route("/api/recommendations")
def api_recommendations():
    limit = request.args.get("limit", 10, type=int)
    return jsonify(svc.get_recommendations(limit=limit))


@app.route("/api/recommendations/categorized")
def api_categorized_recs():
    return jsonify(svc.get_categorized_recs())


# ── Execution endpoints ─────────────────────────────────────


@app.route("/api/challenges/<section_num>/<lesson_num>/<int:idx>/run", methods=["POST"])
def api_run_challenge(section_num: str, lesson_num: str, idx: int):
    result = svc.run_challenge(section_num, lesson_num, idx)
    return jsonify(result)


@app.route("/api/execute", methods=["POST"])
def api_execute_code():
    """REPL endpoint — execute arbitrary code snippet (one-shot, legacy)."""
    data = request.get_json(force=True)
    code = data.get("code", "")
    timeout = min(data.get("timeout", 10), 30)
    return jsonify(svc.execute_code(code, timeout=timeout))


# ── Concept & Adaptive endpoints ─────────────────────────────


@app.route("/api/concepts/mastery")
def api_concept_mastery():
    """Return concept mastery states for all concepts."""
    return jsonify(svc.get_concept_mastery())


@app.route("/api/adaptive/recommendations")
def api_adaptive_recs():
    """Return concept-aware adaptive recommendations."""
    mode = request.args.get("mode", "guided")
    limit = request.args.get("limit", 10, type=int)
    return jsonify(svc.get_adaptive_recs(mode=mode, limit=limit))


@app.route("/api/adaptive/study-plan")
def api_study_plan():
    """Generate a study plan for today."""
    mode = request.args.get("mode", "guided")
    minutes = request.args.get("minutes", 30, type=int)
    return jsonify(svc.get_study_plan(mode=mode, session_minutes=minutes))


@app.route("/api/projects")
def api_projects():
    """Return available projects with progress."""
    return jsonify(svc.get_projects())


@app.route("/api/reflection", methods=["POST"])
def api_reflection():
    """Generate reflection prompts."""
    data = request.get_json(force=True)
    context = data.get("context", "challenge")
    return jsonify(
        svc.get_reflection(
            context=context,
            section_num=data.get("section_num", ""),
            lesson_num=data.get("lesson_num", ""),
            challenge_index=data.get("challenge_index", -1),
            passed=data.get("passed", False),
        )
    )


# ── Workspace endpoints ──────────────────────────────────────


@app.route("/api/workspace/<section_num>/<lesson_num>")
def api_workspace_info(section_num: str, lesson_num: str):
    """Get workspace metadata for a lesson."""
    return jsonify(get_workspace_info(section_num, lesson_num))


@app.route("/api/workspace/<section_num>/<lesson_num>/draft")
def api_get_draft(section_num: str, lesson_num: str):
    """Get the user's current draft code."""
    return jsonify(get_draft(section_num, lesson_num))


@app.route("/api/workspace/<section_num>/<lesson_num>/draft", methods=["PUT"])
def api_save_draft(section_num: str, lesson_num: str):
    """Save (or autosave) the user's draft code."""
    data = request.get_json(force=True)
    content = data.get("content", "")
    return jsonify(save_draft(section_num, lesson_num, content))


@app.route("/api/workspace/<section_num>/<lesson_num>/starter")
def api_get_starter(section_num: str, lesson_num: str):
    """Get the original starter code."""
    return jsonify(get_starter(section_num, lesson_num))


@app.route("/api/workspace/<section_num>/<lesson_num>/reset", methods=["POST"])
def api_reset_to_starter(section_num: str, lesson_num: str):
    """Reset draft to starter code."""
    return jsonify(reset_to_starter(section_num, lesson_num))


@app.route("/api/workspace/<section_num>/<lesson_num>/reference/<int:idx>")
def api_reference_solution(section_num: str, lesson_num: str, idx: int):
    """Get reference solution for a specific challenge."""
    return jsonify(get_reference_solution(section_num, lesson_num, idx))


# ── File endpoints (legacy, kept for backward compat) ────────


@app.route("/api/files/<section_num>/<lesson_num>")
def api_get_file(section_num: str, lesson_num: str):
    return jsonify(get_draft(section_num, lesson_num))


@app.route("/api/files/<section_num>/<lesson_num>", methods=["PUT"])
def api_save_file(section_num: str, lesson_num: str):
    data = request.get_json(force=True)
    content = data.get("content", "")
    return jsonify(save_draft(section_num, lesson_num, content))


# ── Persistent REPL endpoints ────────────────────────────────


@app.route("/api/repl/execute", methods=["POST"])
def api_repl_execute():
    """Execute code in the persistent Python REPL session."""
    data = request.get_json(force=True)
    code = data.get("code", "")
    timeout = min(data.get("timeout", 10), 30)
    repl = get_repl()
    result = repl.execute(code, timeout=timeout)
    return jsonify(result)


@app.route("/api/repl/reset", methods=["POST"])
def api_repl_reset():
    """Restart the Python REPL session."""
    return jsonify(reset_repl())


@app.route("/api/repl/status")
def api_repl_status():
    repl = get_repl()
    return jsonify({"alive": repl.alive})


# ── PTY Terminal endpoints ───────────────────────────────────


@app.route("/api/terminal/write", methods=["POST"])
def api_terminal_write():
    """Send data to the terminal (keystrokes or commands)."""
    data = request.get_json(force=True)
    text = data.get("data", "")
    term = get_terminal()
    ok = term.write(text)
    return jsonify({"success": ok})


@app.route("/api/terminal/read")
def api_terminal_read():
    """Read available output from the terminal."""
    term = get_terminal()
    output = term.read()
    return jsonify({"data": output, "alive": term.alive})


@app.route("/api/terminal/resize", methods=["POST"])
def api_terminal_resize():
    """Resize the terminal."""
    data = request.get_json(force=True)
    cols = data.get("cols", 80)
    rows = data.get("rows", 24)
    term = get_terminal()
    term.resize(cols, rows)
    return jsonify({"success": True})


@app.route("/api/terminal/reset", methods=["POST"])
def api_terminal_reset():
    """Restart the terminal session."""
    return jsonify(reset_terminal())


@app.route("/api/terminal/status")
def api_terminal_status():
    term = get_terminal()
    return jsonify({"alive": term.alive})


# ── Server lifecycle ─────────────────────────────────────────

_server_thread: Optional[threading.Thread] = None


def start_server(port: int = 44556) -> str:
    """Start the Flask API server in a daemon thread."""
    global _server_thread
    url = f"http://127.0.0.1:{port}"
    if _server_thread is not None and _server_thread.is_alive():
        return url

    def _run():
        app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

    _server_thread = threading.Thread(target=_run, daemon=True)
    _server_thread.start()
    return url


# ── Standalone entry point ───────────────────────────────────

if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 44556
    print(f"ProgTrain API server on http://127.0.0.1:{port}")
    print(f"Open http://127.0.0.1:{port} in your browser for the web UI.")
    app.run(host="127.0.0.1", port=port, debug=True)
