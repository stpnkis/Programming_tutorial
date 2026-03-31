"""Tests for engine.workspace — workspace model with drafts, starters, and reset."""
import os
import shutil
import tempfile
from pathlib import Path
from unittest import mock

import pytest

# We test workspace module in isolation, mocking _find_challenge_file
import engine.workspace as ws


@pytest.fixture(autouse=True)
def temp_workspace(tmp_path, monkeypatch):
    """Redirect workspace dir and create a mock challenge file."""
    workspace_dir = tmp_path / "workspace"
    monkeypatch.setattr(ws, "WORKSPACE_DIR", workspace_dir)

    # Create a mock challenge file
    content_dir = tmp_path / "content" / "01" / "01"
    content_dir.mkdir(parents=True)
    challenge_file = content_dir / "challenges.py"
    challenge_file.write_text(
        '# Starter code\ndef vyzva_1():\n    pass\n', encoding="utf-8"
    )

    # Mock _find_challenge_file to return our temp file
    monkeypatch.setattr(ws, "_find_challenge_file",
                        lambda s, l: challenge_file if s == "01" and l == "01" else None)
    monkeypatch.setattr(ws, "ROOT", tmp_path)

    return {"workspace": workspace_dir, "challenge_file": challenge_file}


class TestInitWorkspace:
    def test_creates_workspace_dir(self, temp_workspace):
        result = ws.init_workspace("01", "01")
        assert result["initialized"] is True
        assert result["has_starter"] is True
        assert result["has_draft"] is True

    def test_creates_starter_snapshot(self, temp_workspace):
        ws.init_workspace("01", "01")
        starter = temp_workspace["workspace"] / "01" / "01" / "starter.py"
        assert starter.exists()
        assert "Starter code" in starter.read_text()

    def test_idempotent(self, temp_workspace):
        ws.init_workspace("01", "01")
        # Modify draft
        draft = temp_workspace["workspace"] / "01" / "01" / "draft.py"
        draft.write_text("modified", encoding="utf-8")

        # Re-init should NOT overwrite draft
        ws.init_workspace("01", "01")
        assert draft.read_text() == "modified"

    def test_nonexistent_lesson_returns_error(self, temp_workspace):
        result = ws.init_workspace("99", "99")
        assert result["initialized"] is False
        assert "error" in result


class TestGetDraft:
    def test_returns_draft_content(self, temp_workspace):
        ws.init_workspace("01", "01")
        result = ws.get_draft("01", "01")
        assert "content" in result
        assert "Starter code" in result["content"]
        assert result["source"] == "draft"

    def test_auto_initializes(self, temp_workspace):
        result = ws.get_draft("01", "01")
        assert "content" in result


class TestSaveDraft:
    def test_saves_content(self, temp_workspace):
        ws.init_workspace("01", "01")
        ws.save_draft("01", "01", "new code here")
        result = ws.get_draft("01", "01")
        assert result["content"] == "new code here"

    def test_writes_back_to_original(self, temp_workspace):
        ws.init_workspace("01", "01")
        ws.save_draft("01", "01", "updated code")
        assert temp_workspace["challenge_file"].read_text() == "updated code"

    def test_returns_success(self, temp_workspace):
        ws.init_workspace("01", "01")
        result = ws.save_draft("01", "01", "code")
        assert result["success"] is True
        assert "saved_at" in result


class TestResetToStarter:
    def test_resets_to_original(self, temp_workspace):
        ws.init_workspace("01", "01")
        ws.save_draft("01", "01", "my changes")
        result = ws.reset_to_starter("01", "01")
        assert result["success"] is True
        assert "Starter code" in result["content"]

    def test_draft_matches_starter_after_reset(self, temp_workspace):
        ws.init_workspace("01", "01")
        ws.save_draft("01", "01", "my changes")
        ws.reset_to_starter("01", "01")
        draft = ws.get_draft("01", "01")
        starter = ws.get_starter("01", "01")
        assert draft["content"] == starter["content"]


class TestGetStarter:
    def test_returns_starter_content(self, temp_workspace):
        ws.init_workspace("01", "01")
        result = ws.get_starter("01", "01")
        assert "content" in result
        assert "Starter code" in result["content"]


class TestGetWorkspaceInfo:
    def test_uninitialized(self, temp_workspace):
        info = ws.get_workspace_info("01", "01")
        assert info["initialized"] is False

    def test_initialized(self, temp_workspace):
        ws.init_workspace("01", "01")
        info = ws.get_workspace_info("01", "01")
        assert info["initialized"] is True
        assert info["has_draft"] is True
        assert info["has_starter"] is True
