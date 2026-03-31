"""
Lab sessions — persistent Python REPL and PTY-backed terminal.

Provides:
- PersistentREPL: Python subprocess that stays alive between code submissions
- PTYTerminal: Linux PTY-backed bash session for shell integration
"""
from __future__ import annotations

import fcntl
import os
import pty
import select
import signal
import struct
import subprocess
import sys
import termios
import threading
import time
from typing import Any, Dict, Optional


class PersistentREPL:
    """Persistent Python REPL session.

    Maintains a Python subprocess with stdin/stdout/stderr pipes.
    Variables and state persist between execute() calls.
    """

    def __init__(self, cwd: Optional[str] = None):
        self._proc: Optional[subprocess.Popen] = None
        self._cwd = cwd or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._lock = threading.Lock()
        self._start()

    def _start(self) -> None:
        """Start the Python subprocess."""
        # Clean env: suppress VS Code shell integration, PYTHONSTARTUP, etc.
        env = os.environ.copy()
        env.pop("PYTHONSTARTUP", None)
        env.pop("VSCODE_SHELL_INTEGRATION", None)
        self._proc = subprocess.Popen(
            [sys.executable, "-u", "-i"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self._cwd,
            env=env,
            text=True,
            bufsize=0,
        )
        # Consume initial Python header
        self._read_available(self._proc.stderr, timeout=0.5)

    def _read_available(self, stream, timeout: float = 0.5) -> str:
        """Non-blocking read of available data from a stream using select."""
        fd = stream.fileno()
        output = []
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            ready, _, _ = select.select([fd], [], [], min(remaining, 0.05))
            if ready:
                chunk = os.read(fd, 4096)
                if not chunk:
                    break
                output.append(chunk.decode("utf-8", errors="replace"))
                deadline = time.monotonic() + 0.1  # extend slightly when data arrives
        return "".join(output)

    def execute(self, code: str, timeout: float = 10.0) -> Dict[str, Any]:
        """Send code to the persistent session and collect output."""
        with self._lock:
            if self._proc is None or self._proc.poll() is not None:
                self._start()

            # Use a sentinel to detect end of execution
            sentinel = f"__PROGTRAIN_DONE_{id(code)}__"
            # Wrap in exec() so multiline blocks work reliably in -i mode
            escaped = code.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
            full_code = f'exec("""{escaped}"""\n)\nprint({sentinel!r})\n'

            try:
                self._proc.stdin.write(full_code)
                self._proc.stdin.flush()
            except (BrokenPipeError, OSError):
                self._start()
                return {"stdout": "", "stderr": "Session reset (broken pipe)", "returncode": -1}

            stdout_parts = []
            stderr_parts = []
            start = time.monotonic()

            while time.monotonic() - start < timeout:
                stdout_chunk = self._read_available(self._proc.stdout, timeout=0.2)
                stderr_chunk = self._read_available(self._proc.stderr, timeout=0.1)

                if stdout_chunk:
                    stdout_parts.append(stdout_chunk)
                if stderr_chunk:
                    stderr_parts.append(stderr_chunk)

                combined = "".join(stdout_parts)
                if sentinel in combined:
                    # Remove sentinel from output
                    combined = combined.replace(sentinel + "\n", "").replace(sentinel, "")
                    return {
                        "stdout": combined,
                        "stderr": "".join(stderr_parts),
                        "returncode": 0,
                    }

            return {
                "stdout": "".join(stdout_parts).replace(sentinel + "\n", "").replace(sentinel, ""),
                "stderr": "".join(stderr_parts) + f"\n⏱ Timeout ({timeout}s)",
                "returncode": -1,
            }

    @property
    def alive(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    def reset(self) -> Dict[str, Any]:
        """Restart the Python session."""
        self.shutdown()
        self._start()
        return {"status": "restarted"}

    def shutdown(self) -> None:
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._proc.kill()
        self._proc = None


class PTYTerminal:
    """PTY-backed terminal session for Linux shell integration.

    Uses pty module to create a pseudo-terminal, providing a real shell
    experience with job control, colors, and interactive commands.
    """

    def __init__(self, shell: str = "/bin/bash", cwd: Optional[str] = None):
        self._master_fd: Optional[int] = None
        self._pid: Optional[int] = None
        self._shell = shell
        self._cwd = cwd or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._lock = threading.Lock()
        self._output_buffer: list = []
        self._reader_thread: Optional[threading.Thread] = None
        self._running = False
        self._start()

    def _start(self) -> None:
        """Fork a PTY and start the shell."""
        env = os.environ.copy()
        env.pop("VSCODE_SHELL_INTEGRATION", None)
        env["TERM"] = "xterm-256color"

        pid, fd = pty.fork()

        if pid == 0:
            # Child process
            os.chdir(self._cwd)
            os.execvpe(self._shell, [self._shell], env)
        else:
            # Parent process
            self._master_fd = fd
            self._pid = pid
            self._running = True

            # Set initial size
            self.resize(80, 24)

            # Start reader thread
            self._reader_thread = threading.Thread(target=self._read_loop, daemon=True)
            self._reader_thread.start()

    def _read_loop(self) -> None:
        """Continuously read output from the PTY."""
        while self._running and self._master_fd is not None:
            try:
                ready, _, _ = select.select([self._master_fd], [], [], 0.1)
                if ready:
                    data = os.read(self._master_fd, 4096)
                    if data:
                        with self._lock:
                            self._output_buffer.append(data.decode("utf-8", errors="replace"))
                    else:
                        break
            except (OSError, ValueError):
                break

    def write(self, data: str) -> bool:
        """Send data (keystrokes/commands) to the terminal."""
        if self._master_fd is None:
            return False
        try:
            os.write(self._master_fd, data.encode("utf-8"))
            return True
        except OSError:
            return False

    def read(self) -> str:
        """Read and drain the output buffer."""
        with self._lock:
            if not self._output_buffer:
                return ""
            result = "".join(self._output_buffer)
            self._output_buffer.clear()
            return result

    def resize(self, cols: int, rows: int) -> None:
        """Resize the PTY."""
        if self._master_fd is not None:
            winsize = struct.pack("HHHH", rows, cols, 0, 0)
            try:
                fcntl.ioctl(self._master_fd, termios.TIOCSWINSZ, winsize)
            except OSError:
                pass

    @property
    def alive(self) -> bool:
        if self._pid is None:
            return False
        try:
            pid, _ = os.waitpid(self._pid, os.WNOHANG)
            return pid == 0
        except ChildProcessError:
            return False

    def reset(self) -> Dict[str, Any]:
        """Kill current shell and start fresh."""
        self.shutdown()
        self._output_buffer.clear()
        self._start()
        return {"status": "restarted"}

    def shutdown(self) -> None:
        """Clean up the PTY session."""
        self._running = False
        if self._pid is not None:
            try:
                os.kill(self._pid, signal.SIGTERM)
                os.waitpid(self._pid, 0)
            except (ProcessLookupError, ChildProcessError):
                pass
            self._pid = None
        if self._master_fd is not None:
            try:
                os.close(self._master_fd)
            except OSError:
                pass
            self._master_fd = None


# ── Singleton instances ──

_repl: Optional[PersistentREPL] = None
_terminal: Optional[PTYTerminal] = None


def get_repl() -> PersistentREPL:
    global _repl
    if _repl is None or not _repl.alive:
        _repl = PersistentREPL()
    return _repl


def get_terminal() -> PTYTerminal:
    global _terminal
    if _terminal is None or not _terminal.alive:
        _terminal = PTYTerminal()
    return _terminal


def reset_repl() -> Dict[str, Any]:
    global _repl
    if _repl:
        _repl.shutdown()
    _repl = PersistentREPL()
    return {"status": "restarted"}


def reset_terminal() -> Dict[str, Any]:
    global _terminal
    if _terminal:
        _terminal.shutdown()
    _terminal = PTYTerminal()
    return {"status": "restarted"}


def shutdown_all() -> None:
    """Clean shutdown of all lab sessions."""
    global _repl, _terminal
    if _repl:
        _repl.shutdown()
        _repl = None
    if _terminal:
        _terminal.shutdown()
        _terminal = None
