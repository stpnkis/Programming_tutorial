"""Tests for desktop.server — Flask API endpoints."""
import json
from unittest import mock

import pytest

# We need to patch lab functions in the desktop.server namespace,
# because server.py uses `from engine.lab import get_repl, ...`
# which binds names at import time.

_mock_repl = mock.MagicMock()
_mock_repl.alive = True
_mock_repl.execute.return_value = {"stdout": "42\n", "stderr": "", "returncode": 0}
_mock_repl.reset.return_value = {"status": "restarted"}

_mock_terminal = mock.MagicMock()
_mock_terminal.alive = True
_mock_terminal.write.return_value = True
_mock_terminal.read.return_value = "$ "
_mock_terminal.reset.return_value = {"status": "restarted"}

# Patch engine.lab BEFORE server imports them
import engine.lab as lab_module
lab_module.get_repl = lambda: _mock_repl
lab_module.get_terminal = lambda: _mock_terminal
lab_module.reset_repl = lambda: {"status": "restarted"}
lab_module.reset_terminal = lambda: {"status": "restarted"}
lab_module.shutdown_all = lambda: None

import desktop.server as server_module
from desktop.server import app

# Also patch the already-bound names in server's namespace
server_module.get_repl = lambda: _mock_repl
server_module.get_terminal = lambda: _mock_terminal
server_module.reset_repl = lambda: {"status": "restarted"}
server_module.reset_terminal = lambda: {"status": "restarted"}
server_module.shutdown_all = lambda: None

# Patch workspace functions to prevent writing to real challenge files
_orig_save_draft = server_module.save_draft
_orig_reset_to_starter = server_module.reset_to_starter

_fake_workspace = {}

def _fake_save(s, l, content):
    _fake_workspace[(s, l)] = content
    return {"success": True, "saved_at": 0}

def _fake_reset(s, l):
    return {"success": True, "content": "# starter"}

server_module.save_draft = _fake_save
server_module.reset_to_starter = _fake_reset


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestContentEndpoints:
    def test_sections(self, client):
        resp = client.get("/api/sections")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, list)
        assert len(data) >= 10  # we have 14 sections

    def test_lesson_detail(self, client):
        resp = client.get("/api/lessons/01/01")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "name" in data
        assert "challenges" in data

    def test_lesson_not_found(self, client):
        resp = client.get("/api/lessons/99/99")
        assert resp.status_code == 404

    def test_search(self, client):
        resp = client.get("/api/search?q=python")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, list)

    def test_search_empty(self, client):
        resp = client.get("/api/search?q=")
        assert resp.status_code == 200
        assert resp.get_json() == []


class TestProgressEndpoints:
    def test_snapshot(self, client):
        resp = client.get("/api/progress/snapshot")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, dict)


class TestRecommendationEndpoints:
    def test_recommendations(self, client):
        resp = client.get("/api/recommendations")
        assert resp.status_code == 200

    def test_categorized(self, client):
        resp = client.get("/api/recommendations/categorized")
        assert resp.status_code == 200


class TestExecutionEndpoints:
    def test_run_challenge(self, client):
        resp = client.post("/api/challenges/01/01/1/run")
        assert resp.status_code == 200

    def test_execute_legacy(self, client):
        resp = client.post("/api/execute",
                           data=json.dumps({"code": "print(1)"}),
                           content_type="application/json")
        assert resp.status_code == 200


class TestWorkspaceEndpoints:
    def test_workspace_info(self, client):
        resp = client.get("/api/workspace/01/01")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "initialized" in data or "has_draft" in data

    def test_get_draft(self, client):
        resp = client.get("/api/workspace/01/01/draft")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, dict)

    def test_save_draft(self, client):
        resp = client.put("/api/workspace/01/01/draft",
                          data=json.dumps({"content": "# test"}),
                          content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data.get("success") is True
        # Verify it went to fake workspace, not real file
        assert _fake_workspace.get(("01", "01")) == "# test"

    def test_get_starter(self, client):
        resp = client.get("/api/workspace/01/01/starter")
        assert resp.status_code == 200

    def test_reset_to_starter(self, client):
        resp = client.post("/api/workspace/01/01/reset")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data.get("success") is True

    def test_reference_solution(self, client):
        resp = client.get("/api/workspace/01/01/reference/1")
        assert resp.status_code == 200


class TestREPLEndpoints:
    def test_repl_execute(self, client):
        resp = client.post("/api/repl/execute",
                           data=json.dumps({"code": "print(42)"}),
                           content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "stdout" in data

    def test_repl_reset(self, client):
        resp = client.post("/api/repl/reset")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "restarted"

    def test_repl_status(self, client):
        resp = client.get("/api/repl/status")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "alive" in data


class TestTerminalEndpoints:
    def test_terminal_write(self, client):
        resp = client.post("/api/terminal/write",
                           data=json.dumps({"data": "ls\n"}),
                           content_type="application/json")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True

    def test_terminal_read(self, client):
        resp = client.get("/api/terminal/read")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "data" in data
        assert "alive" in data

    def test_terminal_resize(self, client):
        resp = client.post("/api/terminal/resize",
                           data=json.dumps({"cols": 120, "rows": 40}),
                           content_type="application/json")
        assert resp.status_code == 200

    def test_terminal_reset(self, client):
        resp = client.post("/api/terminal/reset")
        assert resp.status_code == 200

    def test_terminal_status(self, client):
        resp = client.get("/api/terminal/status")
        assert resp.status_code == 200


class TestLegacyFileEndpoints:
    def test_get_file(self, client):
        resp = client.get("/api/files/01/01")
        assert resp.status_code == 200

    def test_save_file(self, client):
        resp = client.put("/api/files/01/01",
                          data=json.dumps({"content": "# legacy save"}),
                          content_type="application/json")
        assert resp.status_code == 200
        # Verify it went through fake save, not real file
        assert _fake_workspace.get(("01", "01")) == "# legacy save"


class TestStaticServing:
    def test_index(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"html" in resp.data.lower()
