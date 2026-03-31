/**
 * ProgTrain — Application state store.
 * Single source of truth for all UI state.
 */
const Store = (() => {
  const s = {
    sections: [],
    currentView: 'dashboard',
    currentLesson: null,
    currentChallenge: null,
    editor: null,
    replEditor: null,
    fileContent: '',
    hintsRevealed: new Set(),
    autosaveTimer: null,
    autosaveDirty: false,
    terminal: null,
    terminalPollTimer: null,
    terminalFitAddon: null,
    focusZone: 'editor',        // 'editor' | 'output' | 'info' | 'terminal'
    commandPaletteOpen: false,
  };

  const STATE_ICONS = {
    not_started: '⬜',
    in_progress: '🔶',
    currently_passing: '✅',
    mastered: '💎',
    regressed: '🔻',
  };

  const CATEGORY_LABELS = {
    fix_regression: { label: 'Opravit', cls: 'fix' },
    review_due:     { label: 'Opakovat', cls: 'review' },
    continue_work:  { label: 'Pokračovat', cls: 'continue' },
    new_material:   { label: 'Nové', cls: 'new' },
    practice:       { label: 'Procvičit', cls: 'continue' },
    concept_practice:{ label: 'Koncept', cls: 'new' },
  };

  // Challenge type display config
  const TYPE_CONFIG = {
    implementation: {
      icon: '🛠️', label: 'Implementace', cls: 'type-impl',
      toolbarHint: 'Napiš kód od nuly',
      runLabel: '▶ Spustit a ověřit',
      successMsg: 'Implementace je správná!',
      failMsg: 'Zatím to ještě neprojde — zkus to upravit.',
    },
    knowledge: {
      icon: '🧠', label: 'Znalost', cls: 'type-knowledge',
      toolbarHint: 'Vrať správnou hodnotu / datovou strukturu',
      runLabel: '▶ Ověřit odpověď',
      successMsg: 'Správná odpověď!',
      failMsg: 'To ještě není správně — zkontroluj svou odpověď.',
    },
    debugging: {
      icon: '🐛', label: 'Debugging', cls: 'type-debug',
      toolbarHint: 'Najdi a oprav chybu v kódu',
      runLabel: '🐛 Ověřit opravu',
      successMsg: 'Chyba opravena!',
      failMsg: 'V kódu je stále chyba — čti chybovou hlášku pozorně.',
    },
    refactoring: {
      icon: '🔧', label: 'Refaktoring', cls: 'type-refactor',
      toolbarHint: 'Vylepši existující kód',
      runLabel: '🔧 Ověřit refaktoring',
      successMsg: 'Refaktoring úspěšný!',
      failMsg: 'Refaktoring ještě není správný — zachovej funkčnost.',
    },
    trace: {
      icon: '👁️', label: 'Trace', cls: 'type-trace',
      toolbarHint: 'Projdi kód krok po kroku a urči výstup',
      runLabel: '👁️ Ověřit trace',
      successMsg: 'Správně jsi určil výstup!',
      failMsg: 'Výstup nesedí — projdi kód znovu krok po kroku.',
    },
    open: {
      icon: '🎨', label: 'Kreativní', cls: 'type-open',
      toolbarHint: 'Navrhni vlastní řešení',
      runLabel: '▶ Spustit',
      successMsg: 'Řešení funguje!',
      failMsg: 'Ještě to neprojde — zkus jiný přístup.',
    },
  };

  function getTypeConfig(type) {
    return TYPE_CONFIG[type] || TYPE_CONFIG.implementation;
  }

  return { s, STATE_ICONS, CATEGORY_LABELS, TYPE_CONFIG, getTypeConfig };
})();
