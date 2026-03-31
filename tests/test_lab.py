"""Tests for engine.lab — PersistentREPL and PTYTerminal."""
import os
import time

import pytest

from engine.lab import PersistentREPL, PTYTerminal


class TestPersistentREPL:
    @pytest.fixture(autouse=True)
    def repl(self):
        r = PersistentREPL()
        yield r
        r.shutdown()

    def test_simple_expression(self, repl):
        result = repl.execute("print(2 + 3)")
        assert "5" in result["stdout"]
        assert result["returncode"] == 0

    def test_variables_persist(self, repl):
        repl.execute("x = 42")
        result = repl.execute("print(x)")
        assert "42" in result["stdout"]

    def test_multiline_code(self, repl):
        # Interactive Python needs a blank line after indented blocks
        code = "for i in range(3):\n    print(i)\n"
        result = repl.execute(code, timeout=5)
        assert "0" in result["stdout"]
        assert "1" in result["stdout"]
        assert "2" in result["stdout"]

    def test_syntax_error_reports_stderr(self, repl):
        result = repl.execute("def bad(:")
        assert result["stderr"] or "SyntaxError" in result["stdout"]

    def test_alive_property(self, repl):
        assert repl.alive is True

    def test_reset_clears_state(self, repl):
        repl.execute("x = 99")
        repl.reset()
        result = repl.execute("print(x)")
        # After reset, x should not exist
        assert "NameError" in result["stderr"] or "NameError" in result["stdout"]

    def test_shutdown(self, repl):
        repl.shutdown()
        assert repl.alive is False


@pytest.mark.skipif(
    os.environ.get("CI") == "true" or os.environ.get("SKIP_PTY") == "1",
    reason="PTY tests require real terminal, skip in CI"
)
class TestPTYTerminal:
    """PTY tests — skipped in CI-like environments where fork+pty is unreliable."""

    @pytest.fixture(autouse=True)
    def terminal(self):
        t = PTYTerminal()
        time.sleep(0.5)  # let shell init
        t.read()  # drain initial output
        yield t
        t.shutdown()

    @pytest.mark.timeout(5)
    def test_alive_property(self, terminal):
        assert terminal.alive is True

    @pytest.mark.timeout(5)
    def test_write_and_read(self, terminal):
        terminal.write("echo hello_pty\n")
        time.sleep(0.5)
        output = terminal.read()
        assert "hello_pty" in output

    @pytest.mark.timeout(5)
    def test_resize(self, terminal):
        terminal.resize(120, 40)

    @pytest.mark.timeout(10)
    def test_reset(self, terminal):
        result = terminal.reset()
        assert result["status"] == "restarted"
        time.sleep(0.5)
        assert terminal.alive is True

    @pytest.mark.timeout(5)
    def test_shutdown(self, terminal):
        terminal.shutdown()
        # After shutdown, alive should be False
        assert terminal.alive is False
