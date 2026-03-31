"""Tests for editor integration module."""
import os
import pytest
from unittest.mock import patch, MagicMock

from engine.editor import get_editor, open_file, find_challenge_line


class TestGetEditor:

    def test_respects_editor_env(self, monkeypatch):
        monkeypatch.setenv("EDITOR", "nano")
        with patch("shutil.which", return_value="/usr/bin/nano"):
            assert get_editor() == "nano"

    def test_fallback_to_vscode(self, monkeypatch):
        monkeypatch.delenv("EDITOR", raising=False)
        def which_side_effect(cmd):
            if cmd == "code":
                return "/usr/bin/code"
            return None
        with patch("shutil.which", side_effect=which_side_effect):
            assert get_editor() == "code"

    def test_empty_when_nothing(self, monkeypatch):
        monkeypatch.delenv("EDITOR", raising=False)
        with patch("shutil.which", return_value=None):
            assert get_editor() == ""


class TestFindChallengeLine:

    def test_finds_correct_line(self, tmp_path):
        challenge_file = tmp_path / "challenges.py"
        challenge_file.write_text(
            "# header\n"
            "from engine.models import Challenge\n"
            "\n"
            "def vyzva_1():\n"
            "    pass\n"
            "\n"
            "def vyzva_2():\n"
            "    pass\n"
        )
        assert find_challenge_line(str(challenge_file), 1) == 4
        assert find_challenge_line(str(challenge_file), 2) == 7

    def test_returns_zero_if_not_found(self, tmp_path):
        challenge_file = tmp_path / "challenges.py"
        challenge_file.write_text("# empty\n")
        assert find_challenge_line(str(challenge_file), 1) == 0

    def test_nonexistent_file(self):
        assert find_challenge_line("/nonexistent/file.py", 1) == 0


class TestOpenFile:

    def test_returns_false_no_editor(self, monkeypatch):
        monkeypatch.delenv("EDITOR", raising=False)
        with patch("shutil.which", return_value=None):
            assert open_file("/some/file.py") is False

    def test_returns_false_no_file(self, monkeypatch):
        monkeypatch.setenv("EDITOR", "nano")
        with patch("shutil.which", return_value="/usr/bin/nano"):
            assert open_file("/nonexistent/file.py") is False
