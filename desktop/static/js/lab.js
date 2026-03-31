/**
 * ProgTrain — Lab module: Persistent REPL + PTY Terminal.
 */
const Lab = (() => {

  // ── REPL ───────────────────────────────────────────────────

  function showRepl() {
    UI.showView('repl');
    UI.setBreadcrumb('Python REPL');
    const st = Store.s;

    if (!st.replEditor) {
      const container = document.getElementById('repl-editor-container');
      container.innerHTML = '';
      st.replEditor = CodeMirror(container, {
        value: '# Persistentní Python session\n# Proměnné zůstávají mezi spuštěními\nprint("Ahoj, světe!")\n',
        mode: 'python',
        theme: 'dracula',
        lineNumbers: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        extraKeys: {
          'Ctrl-Enter': () => runRepl(),
        },
      });
    }
  }

  async function runRepl() {
    const st = Store.s;
    if (!st.replEditor) return;
    const code = st.replEditor.getValue();
    const outEl = document.getElementById('repl-output');

    const firstLine = code.split('\n')[0];
    const more = code.split('\n').length > 1 ? ' ...' : '';
    outEl.textContent += `>>> ${firstLine}${more}\n`;

    const result = await Api.replExecute(code, 10);
    if (result.stdout) outEl.textContent += result.stdout;
    if (result.stderr) outEl.textContent += result.stderr;
    if (result.returncode !== 0 && !result.stderr && result.returncode !== undefined) {
      outEl.textContent += `(exit code: ${result.returncode})\n`;
    }
    outEl.textContent += '\n';
    outEl.scrollTop = outEl.scrollHeight;
  }

  async function resetRepl() {
    await Api.replReset();
    document.getElementById('repl-output').textContent = '🔄 Python session restarted.\n\n';
  }

  function clearReplOutput() {
    document.getElementById('repl-output').textContent = '';
  }

  // ── Terminal ───────────────────────────────────────────────

  function showTerminal() {
    UI.showView('terminal');
    UI.setBreadcrumb('Linux Terminal');
    if (!Store.s.terminal) initTerminal();
    startTerminalPolling();
  }

  function initTerminal() {
    const container = document.getElementById('xterm-container');
    container.innerHTML = '';
    if (typeof Terminal === 'undefined') {
      container.innerHTML = '<p class="muted" style="padding:16px">Terminal library not loaded.</p>';
      return;
    }

    const st = Store.s;
    st.terminal = new Terminal({
      cursorBlink: true,
      fontSize: 14,
      fontFamily: "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
      theme: {
        background: '#1e1e2e', foreground: '#cdd6f4', cursor: '#89b4fa',
        cursorAccent: '#1e1e2e',
        black: '#45475a', red: '#f38ba8', green: '#a6e3a1', yellow: '#f9e2af',
        blue: '#89b4fa', magenta: '#cba6f7', cyan: '#94e2d5', white: '#bac2de',
        brightBlack: '#585b70', brightRed: '#f38ba8', brightGreen: '#a6e3a1',
        brightYellow: '#f9e2af', brightBlue: '#89b4fa', brightMagenta: '#cba6f7',
        brightCyan: '#94e2d5', brightWhite: '#a6adc8',
      },
    });
    st.terminal.open(container);

    if (typeof FitAddon !== 'undefined') {
      st.terminalFitAddon = new FitAddon.FitAddon();
      st.terminal.loadAddon(st.terminalFitAddon);
      setTimeout(() => {
        st.terminalFitAddon.fit();
        Api.termResize(st.terminal.cols, st.terminal.rows);
      }, 100);
      window.addEventListener('resize', () => {
        if (st.terminalFitAddon && st.currentView === 'terminal') {
          st.terminalFitAddon.fit();
          Api.termResize(st.terminal.cols, st.terminal.rows);
        }
      });
    }

    st.terminal.onData(data => Api.termWrite(data));
    updateTerminalStatus(true);
  }

  function startTerminalPolling() {
    stopTerminalPolling();
    Store.s.terminalPollTimer = setInterval(pollTerminal, 100);
  }

  function stopTerminalPolling() {
    if (Store.s.terminalPollTimer) {
      clearInterval(Store.s.terminalPollTimer);
      Store.s.terminalPollTimer = null;
    }
  }

  async function pollTerminal() {
    if (!Store.s.terminal) return;
    const result = await Api.termRead();
    if (result.data) Store.s.terminal.write(result.data);
    updateTerminalStatus(result.alive !== false);
  }

  function updateTerminalStatus(alive) {
    const el = document.getElementById('terminal-status');
    if (el) {
      el.style.color = alive ? 'var(--green)' : 'var(--red)';
      el.title = alive ? 'Terminal running' : 'Terminal stopped';
    }
  }

  async function resetTerminalSession() {
    await Api.termReset();
    if (Store.s.terminal) Store.s.terminal.clear();
    updateTerminalStatus(true);
  }

  return {
    showRepl, runRepl, resetRepl, clearReplOutput,
    showTerminal, startTerminalPolling, stopTerminalPolling, resetTerminalSession,
  };
})();
