/**
 * ProgTrain — Keyboard shortcuts and command palette.
 */
const Keyboard = (() => {

  const SHORTCUTS = [
    { keys: 'Ctrl+Enter', action: 'runOrVerify',    desc: 'Spustit / Ověřit' },
    { keys: 'Ctrl+S',     action: 'save',           desc: 'Uložit' },
    { keys: 'Ctrl+Shift+R', action: 'reset',        desc: 'Reset na starter' },
    { keys: 'Alt+Left',   action: 'prevChallenge',  desc: 'Předchozí výzva' },
    { keys: 'Alt+Right',  action: 'nextChallenge',  desc: 'Další výzva' },
    { keys: 'Ctrl+Shift+H', action: 'hint',         desc: 'Další nápověda' },
    { keys: 'Ctrl+Shift+C', action: 'compare',      desc: 'Porovnat s referencí' },
    { keys: 'Ctrl+Shift+E', action: 'reference',    desc: 'Zobrazit referenční řešení' },
    { keys: 'Ctrl+P',     action: 'commandPalette', desc: 'Paleta příkazů' },
    { keys: 'Ctrl+1',     action: 'focusEditor',    desc: 'Fokus: Editor' },
    { keys: 'Ctrl+2',     action: 'focusOutput',    desc: 'Fokus: Výstup' },
    { keys: 'Ctrl+3',     action: 'focusInfo',      desc: 'Fokus: Info panel' },
    { keys: 'Escape',     action: 'escape',         desc: 'Zavřít modal / paletu' },
  ];

  function init() {
    document.addEventListener('keydown', handleKeydown);
  }

  function handleKeydown(e) {
    // Command palette
    if (e.ctrlKey && e.key === 'p') {
      e.preventDefault();
      toggleCommandPalette();
      return;
    }

    // Escape
    if (e.key === 'Escape') {
      if (Store.s.commandPaletteOpen) { closeCommandPalette(); return; }
      Challenge.closeCompareModal();
      return;
    }

    // Don't intercept shortcuts when command palette input is focused
    if (Store.s.commandPaletteOpen) return;

    // Ctrl+Enter — Run (handled by CodeMirror extraKeys too, but also works when editor not focused)
    if (e.ctrlKey && e.key === 'Enter') {
      e.preventDefault();
      if (Store.s.currentView === 'challenge') Challenge.run();
      else if (Store.s.currentView === 'repl') Lab.runRepl();
      return;
    }

    // Ctrl+S — Save
    if (e.ctrlKey && e.key === 's') {
      e.preventDefault();
      if (Store.s.currentView === 'challenge') Workspace.save();
      return;
    }

    // Ctrl+Shift+R — Reset
    if (e.ctrlKey && e.shiftKey && e.key === 'R') {
      e.preventDefault();
      if (Store.s.currentView === 'challenge') Workspace.resetToStarter();
      return;
    }

    // Alt+Left / Alt+Right — Navigate challenges
    if (e.altKey && e.key === 'ArrowLeft') {
      e.preventDefault();
      if (Store.s.currentView === 'challenge') Challenge.navigate(-1);
      return;
    }
    if (e.altKey && e.key === 'ArrowRight') {
      e.preventDefault();
      if (Store.s.currentView === 'challenge') Challenge.navigate(1);
      return;
    }

    // Ctrl+Shift+H — Hint
    if (e.ctrlKey && e.shiftKey && e.key === 'H') {
      e.preventDefault();
      if (Store.s.currentView === 'challenge') Challenge.revealNextHint();
      return;
    }

    // Ctrl+Shift+C — Compare
    if (e.ctrlKey && e.shiftKey && e.key === 'C') {
      e.preventDefault();
      if (Store.s.currentView === 'challenge') Challenge.compareWithReference();
      return;
    }

    // Ctrl+Shift+E — Reference
    if (e.ctrlKey && e.shiftKey && e.key === 'E') {
      e.preventDefault();
      if (Store.s.currentView === 'challenge') Challenge.revealReference();
      return;
    }

    // Ctrl+1/2/3 — Focus zones
    if (e.ctrlKey && !e.shiftKey && !e.altKey) {
      if (e.key === '1') { e.preventDefault(); focusZone('editor'); return; }
      if (e.key === '2') { e.preventDefault(); focusZone('output'); return; }
      if (e.key === '3') { e.preventDefault(); focusZone('info'); return; }
    }
  }

  function focusZone(zone) {
    Store.s.focusZone = zone;
    if (zone === 'editor' && Store.s.editor) {
      Store.s.editor.focus();
    } else if (zone === 'output') {
      const el = document.getElementById('output-content');
      if (el) el.focus();
    } else if (zone === 'info') {
      const el = document.getElementById('challenge-info-panel');
      if (el) el.focus();
    }
  }

  // ── Command Palette ────────────────────────────────────────

  const COMMANDS = [
    { id: 'dashboard',  label: '🏠 Dashboard',                action: () => Dashboard.show() },
    { id: 'repl',       label: '🐍 Python REPL',              action: () => Lab.showRepl() },
    { id: 'terminal',   label: '⬛ Linux Terminal',            action: () => Lab.showTerminal() },
    { id: 'search',     label: '🔍 Hledat...',                action: () => showSearchView() },
    { id: 'run',        label: '▶ Spustit výzvu',             action: () => Challenge.run() },
    { id: 'save',       label: '💾 Uložit',                   action: () => Workspace.save() },
    { id: 'reset',      label: '🔄 Reset na starter',         action: () => Workspace.resetToStarter() },
    { id: 'reference',  label: '📋 Zobrazit referenční řešení', action: () => Challenge.revealReference() },
    { id: 'compare',    label: '⚖️ Porovnat s referencí',     action: () => Challenge.compareWithReference() },
    { id: 'hint',       label: '💡 Další nápověda',            action: () => Challenge.revealNextHint() },
    { id: 'thinking',   label: '🧠 Thinking notes',           action: () => Challenge.showThinkingNotes() },
    { id: 'mistakes',   label: '⚠️ Časté chyby',              action: () => Challenge.showCommonMistakes() },
    { id: 'shortcuts',  label: '⌨️ Zobrazit klávesové zkratky', action: () => showShortcutsModal() },
  ];

  function toggleCommandPalette() {
    if (Store.s.commandPaletteOpen) closeCommandPalette();
    else openCommandPalette();
  }

  function openCommandPalette() {
    Store.s.commandPaletteOpen = true;
    let palette = document.getElementById('command-palette');
    if (!palette) {
      palette = document.createElement('div');
      palette.id = 'command-palette';
      palette.className = 'modal-overlay';
      palette.innerHTML = `
        <div class="palette-container">
          <input type="text" id="palette-input" placeholder="Zadej příkaz..." autocomplete="off">
          <div id="palette-results"></div>
        </div>`;
      palette.addEventListener('click', (e) => {
        if (e.target === palette) closeCommandPalette();
      });
      document.body.appendChild(palette);
    }
    palette.style.display = 'flex';
    const input = document.getElementById('palette-input');
    input.value = '';
    input.focus();
    renderPaletteResults('');
    input.oninput = () => renderPaletteResults(input.value);
    input.onkeydown = handlePaletteKey;
  }

  function closeCommandPalette() {
    Store.s.commandPaletteOpen = false;
    const palette = document.getElementById('command-palette');
    if (palette) palette.style.display = 'none';
  }

  let paletteSelectedIndex = 0;

  function renderPaletteResults(query) {
    const el = document.getElementById('palette-results');
    const q = query.toLowerCase();
    const filtered = COMMANDS.filter(c => c.label.toLowerCase().includes(q));
    paletteSelectedIndex = 0;

    el.innerHTML = filtered.map((c, i) =>
      `<div class="palette-item ${i === 0 ? 'palette-active' : ''}" data-idx="${i}" onclick="Keyboard.executePaletteItem(${i})">${c.label}</div>`
    ).join('');
  }

  function handlePaletteKey(e) {
    const items = document.querySelectorAll('.palette-item');
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      paletteSelectedIndex = Math.min(paletteSelectedIndex + 1, items.length - 1);
      updatePaletteSelection(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      paletteSelectedIndex = Math.max(paletteSelectedIndex - 1, 0);
      updatePaletteSelection(items);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      executePaletteItem(paletteSelectedIndex);
    }
  }

  function updatePaletteSelection(items) {
    items.forEach((item, i) => item.classList.toggle('palette-active', i === paletteSelectedIndex));
    if (items[paletteSelectedIndex]) items[paletteSelectedIndex].scrollIntoView({ block: 'nearest' });
  }

  function executePaletteItem(idx) {
    const q = (document.getElementById('palette-input')?.value || '').toLowerCase();
    const filtered = COMMANDS.filter(c => c.label.toLowerCase().includes(q));
    if (filtered[idx]) {
      closeCommandPalette();
      filtered[idx].action();
    }
  }

  // ── Shortcuts modal ────────────────────────────────────────

  function showShortcutsModal() {
    let modal = document.getElementById('shortcuts-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'shortcuts-modal';
      modal.className = 'modal-overlay';
      modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
      });
      document.body.appendChild(modal);
    }
    let html = '<div class="modal-content"><div class="modal-header"><h3>⌨️ Klávesové zkratky</h3><button onclick="document.getElementById(\'shortcuts-modal\').style.display=\'none\'" class="btn-small">✕</button></div>';
    html += '<table class="shortcuts-table">';
    for (const s of SHORTCUTS) {
      html += `<tr><td><kbd class="kbd-badge">${s.keys}</kbd></td><td>${s.desc}</td></tr>`;
    }
    html += '</table></div>';
    modal.innerHTML = html;
    modal.style.display = 'flex';
  }

  return {
    init, SHORTCUTS, COMMANDS,
    toggleCommandPalette, openCommandPalette, closeCommandPalette,
    executePaletteItem, showShortcutsModal,
  };
})();
