/**
 * ProgTrain — Workspace module: autosave, draft management.
 */
const Workspace = (() => {

  function startAutosave() {
    stopAutosave();
    const st = Store.s;
    if (st.editor) st.editor.on('change', markDirty);
    st.autosaveTimer = setInterval(doAutosave, 15000);
  }

  function stopAutosave() {
    const st = Store.s;
    if (st.autosaveTimer) { clearInterval(st.autosaveTimer); st.autosaveTimer = null; }
    if (st.editor) st.editor.off('change', markDirty);
    if (st.autosaveDirty) doAutosave();
  }

  function markDirty() {
    Store.s.autosaveDirty = true;
    const ind = document.getElementById('autosave-indicator');
    if (ind) ind.textContent = '● neuloženo';
  }

  async function doAutosave() {
    const st = Store.s;
    if (!st.autosaveDirty || !st.currentChallenge || !st.editor) return;
    st.autosaveDirty = false;
    const { section_num, lesson_num } = st.currentChallenge;
    await Api.saveDraft(section_num, lesson_num, st.editor.getValue());
    const ind = document.getElementById('autosave-indicator');
    if (ind) {
      ind.textContent = '✓ uloženo';
      setTimeout(() => { if (ind.textContent === '✓ uloženo') ind.textContent = ''; }, 2000);
    }
  }

  async function save() {
    const st = Store.s;
    if (!st.currentChallenge || !st.editor) return;
    const { section_num, lesson_num } = st.currentChallenge;
    st.autosaveDirty = false;
    const result = await Api.saveDraft(section_num, lesson_num, st.editor.getValue());
    if (result.success) {
      UI.toast('Soubor uložen', 'pass');
      const ind = document.getElementById('autosave-indicator');
      if (ind) ind.textContent = '✓ uloženo';
    } else {
      UI.toast(`Chyba při ukládání: ${result.error}`, 'fail');
    }
  }

  async function resetToStarter() {
    const st = Store.s;
    if (!st.currentChallenge) return;
    if (!confirm('Opravdu resetovat kód na výchozí stav? Tvůj aktuální kód bude ztracen.')) return;
    const { section_num, lesson_num } = st.currentChallenge;
    const result = await Api.resetToStarter(section_num, lesson_num);
    if (result.content && st.editor) {
      st.editor.setValue(result.content);
      st.autosaveDirty = false;
      UI.toast('Kód resetován na výchozí stav', 'pass');
    } else {
      UI.toast(`Reset selhal: ${result.error || 'Unknown error'}`, 'fail');
    }
  }

  return { startAutosave, stopAutosave, save, resetToStarter, doAutosave, markDirty };
})();
