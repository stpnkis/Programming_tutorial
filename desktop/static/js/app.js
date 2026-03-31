/**
 * ProgTrain Desktop — frontend application logic v2.
 *
 * Single-page app with:
 * - Workspace model (draft/starter/reference/compare)
 * - Persistent Python REPL
 * - PTY-backed terminal via xterm.js
 * - Challenge workflow with autosave, reset, compare
 */

// ── State ──────────────────────────────────────────────────

const state = {
  sections: [],
  currentView: 'dashboard',
  currentLesson: null,      // {section_num, lesson_num, data}
  currentChallenge: null,    // {section_num, lesson_num, index, data}
  editor: null,              // CodeMirror instance (challenge editor)
  replEditor: null,          // CodeMirror instance (REPL)
  fileContent: '',
  hintsRevealed: new Set(),
  autosaveTimer: null,
  autosaveDirty: false,
  terminal: null,            // xterm Terminal instance
  terminalPollTimer: null,
  terminalFitAddon: null,
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
  review_due: { label: 'Opakovat', cls: 'review' },
  continue_work: { label: 'Pokračovat', cls: 'continue' },
  new_material: { label: 'Nové', cls: 'new' },
  practice: { label: 'Procvičit', cls: 'continue' },
  concept_practice: { label: 'Koncept', cls: 'new' },
};

// ── API helpers ────────────────────────────────────────────

async function api(path, options = {}) {
  try {
    const resp = await fetch(path, options);
    if (!resp.ok) {
      const text = await resp.text();
      try { return JSON.parse(text); } catch { return { error: `HTTP ${resp.status}: ${text}` }; }
    }
    return resp.json();
  } catch (e) {
    return { error: `Network error: ${e.message}` };
  }
}

async function apiPost(path, data) {
  return api(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

async function apiPut(path, data) {
  return api(path, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
}

// ── View switching ─────────────────────────────────────────

function showView(viewId) {
  if (state.currentView === 'challenge' && viewId !== 'challenge') {
    stopAutosave();
  }
  if (state.currentView === 'terminal' && viewId !== 'terminal') {
    stopTerminalPolling();
  }
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const el = document.getElementById(viewId + '-view');
  if (el) el.classList.add('active');
  state.currentView = viewId;
}

// ── Dashboard ──────────────────────────────────────────────

async function showDashboard() {
  showView('dashboard');
  document.getElementById('breadcrumb').textContent = '';

  const [snap, recs] = await Promise.all([
    api('/api/progress/snapshot'),
    api('/api/recommendations/categorized'),
  ]);

  const statsEl = document.getElementById('dashboard-stats');
  statsEl.innerHTML = `
    <div class="stat-card">
      <div class="stat-value">${snap.total_challenges || 0}</div>
      <div class="stat-label">Celkem výzev</div>
    </div>
    <div class="stat-card mastered">
      <div class="stat-value">${snap.mastered || 0}</div>
      <div class="stat-label">💎 Zvládnuto</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${snap.currently_passing || 0}</div>
      <div class="stat-label">✅ Projde</div>
    </div>
    <div class="stat-card regressed">
      <div class="stat-value">${snap.regressed || 0}</div>
      <div class="stat-label">🔻 Regrese</div>
    </div>
    <div class="stat-card review">
      <div class="stat-value">${snap.review_due_count || 0}</div>
      <div class="stat-label">🔄 K opakování</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${Math.round(snap.progress_pct || 0)}%</div>
      <div class="stat-label">Celkový pokrok</div>
      <div class="progress-bar"><div class="progress-bar-fill" style="width:${snap.progress_pct || 0}%"></div></div>
    </div>
  `;

  const recsEl = document.getElementById('dashboard-recs');
  let recsHtml = '<h2 style="margin-bottom:16px">📋 Doporučení</h2>';
  const categoryOrder = ['regressions', 'review', 'continue', 'new'];
  const categoryNames = {
    regressions: '🔻 Opravit regrese',
    review: '🔄 Opakování',
    continue: '📝 Pokračovat',
    new: '🆕 Nový materiál',
  };

  for (const cat of categoryOrder) {
    const items = recs[cat];
    if (!items || items.length === 0) continue;
    recsHtml += `<div class="rec-section"><h3>${categoryNames[cat]}</h3>`;
    for (const r of items.slice(0, 5)) {
      const catInfo = CATEGORY_LABELS[r.category] || { label: '?', cls: 'new' };
      recsHtml += `
        <div class="rec-card" onclick="openLesson('${r.lesson_id.split('.')[0]}','${r.lesson_id.split('.')[1]}')">
          <span class="rec-cat ${catInfo.cls}">${catInfo.label}</span>
          <span>${escapeHtml(r.lesson_name)}</span>
          <span style="color:var(--text-muted);font-size:12px;margin-left:auto">${escapeHtml(r.reason)}</span>
        </div>`;
    }
    recsHtml += '</div>';
  }

  if (Object.values(recs).every(v => !v || v.length === 0)) {
    recsHtml += '<p class="muted">Zatím žádná doporučení. Začni řešit výzvy!</p>';
  }
  recsEl.innerHTML = recsHtml;
}

// ── Course tree (sidebar) ──────────────────────────────────

async function loadCourseTree() {
  state.sections = await api('/api/sections');
  if (state.sections.error) { state.sections = []; }
  renderCourseTree();
}

function renderCourseTree() {
  const el = document.getElementById('course-tree');
  let html = '';

  for (const s of state.sections) {
    const totalCh = s.lessons.reduce((sum, l) => sum + l.challenge_count, 0);
    const completed = s.lessons.reduce((sum, l) => sum + l.completed, 0);
    html += `
      <div class="section-item">
        <div class="section-header" onclick="toggleSection(this)">
          <span class="arrow">▶</span>
          <span>${s.emoji} ${s.num}. ${escapeHtml(s.name)}</span>
          <span class="lesson-progress">${completed}/${totalCh}</span>
        </div>
        <div class="section-lessons">`;
    for (const l of s.lessons) {
      const icon = l.completed === l.challenge_count && l.challenge_count > 0
        ? '💎' : l.completed > 0 ? '🔶' : '⬜';
      html += `
          <div class="lesson-item" data-lesson="${l.section_num}.${l.lesson_num}"
               onclick="openLesson('${l.section_num}','${l.lesson_num}')">
            <span>${icon}</span>
            <span>${l.lesson_num}. ${escapeHtml(l.name)}</span>
            <span class="lesson-progress">${l.completed}/${l.challenge_count}</span>
          </div>`;
    }
    html += `</div></div>`;
  }
  el.innerHTML = html;

  const totalChallenges = state.sections.reduce(
    (s, sec) => s + sec.lessons.reduce((s2, l) => s2 + l.challenge_count, 0), 0);
  const totalCompleted = state.sections.reduce(
    (s, sec) => s + sec.lessons.reduce((s2, l) => s2 + l.completed, 0), 0);
  document.getElementById('progress-summary').innerHTML = `
    ${totalCompleted}/${totalChallenges} výzev projde
    <div class="progress-bar"><div class="progress-bar-fill" style="width:${totalChallenges ? (totalCompleted/totalChallenges*100) : 0}%"></div></div>
  `;
}

function toggleSection(headerEl) {
  headerEl.classList.toggle('expanded');
  headerEl.nextElementSibling.classList.toggle('expanded');
}

// ── Lesson detail ──────────────────────────────────────────

async function openLesson(sectionNum, lessonNum) {
  showView('lesson');
  state.currentLesson = { section_num: sectionNum, lesson_num: lessonNum };

  const data = await api(`/api/lessons/${sectionNum}/${lessonNum}`);
  if (data.error) {
    document.getElementById('lesson-header').innerHTML = `<p class="fail">Chyba: ${escapeHtml(data.error)}</p>`;
    return;
  }
  state.currentLesson.data = data;

  document.getElementById('breadcrumb').innerHTML =
    `<span class="text-accent" style="cursor:pointer" onclick="showDashboard()">Dashboard</span> › ${escapeHtml(data.name)}`;

  const meta = data.meta;
  let headerHtml = `
    <h1>${escapeHtml(data.name)}</h1>
    <div class="lesson-meta">
      ${meta.difficulty ? '⭐'.repeat(meta.difficulty) + ' ' : ''}
      ${meta.estimated_minutes ? `⏱ ${meta.estimated_minutes} min ` : ''}
      ${(meta.tags || []).map(t => `<span class="tag">${escapeHtml(t)}</span>`).join('')}
    </div>`;
  if (meta.summary) {
    headerHtml += `<p style="margin-top:8px;color:var(--text-secondary)">${escapeHtml(meta.summary)}</p>`;
  }
  document.getElementById('lesson-header').innerHTML = headerHtml;

  let theoryHtml = '';
  if (data.why_it_matters) {
    theoryHtml += `<div class="lesson-section"><h3>🎯 Proč se to učit</h3><div class="content">${renderMarkdown(data.why_it_matters)}</div></div>`;
  }
  if (data.what_you_will_learn) {
    theoryHtml += `<div class="lesson-section"><h3>🧠 Co budeš umět</h3><div class="content">${renderMarkdown(data.what_you_will_learn)}</div></div>`;
  }
  if (data.key_theory) {
    theoryHtml += `<div class="lesson-section"><h3>📖 Klíčová teorie</h3><div class="content">${renderMarkdown(data.key_theory)}</div></div>`;
  }
  document.getElementById('lesson-theory').innerHTML = theoryHtml;

  const totalCh = data.challenges.length;
  const passedCh = data.challenges.filter(c => ['currently_passing', 'mastered'].includes(c.state)).length;
  let chHtml = `<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
    <h3>📝 Výzvy (${passedCh}/${totalCh})</h3>
    <div class="progress-bar" style="width:150px"><div class="progress-bar-fill" style="width:${totalCh ? passedCh/totalCh*100 : 0}%"></div></div>
  </div><div class="challenge-list">`;

  for (const ch of data.challenges) {
    const icon = STATE_ICONS[ch.state] || '⬜';
    chHtml += `
      <div class="challenge-list-item" onclick="openChallenge('${sectionNum}','${lessonNum}',${ch.index})">
        <span class="challenge-state">${icon}</span>
        <div class="challenge-title">
          <div>${ch.index}. ${escapeHtml(ch.title)}</div>
          ${ch.learning_objective ? `<div style="font-size:12px;color:var(--text-muted)">${escapeHtml(ch.learning_objective)}</div>` : ''}
        </div>
        <div class="challenge-meta">
          <span class="tag">${ch.type}</span>
          ${ch.points} b
          ${ch.difficulty > 1 ? ' · ' + '⭐'.repeat(ch.difficulty) : ''}
        </div>
      </div>`;
  }
  chHtml += '</div>';

  if (totalCh > 0) {
    const firstIncomplete = data.challenges.find(c => !['currently_passing', 'mastered'].includes(c.state));
    const target = firstIncomplete || data.challenges[0];
    chHtml += `<div style="margin-top:16px;text-align:center">
      <button class="btn-primary" onclick="openChallenge('${sectionNum}','${lessonNum}',${target.index})" style="padding:12px 24px;font-size:15px">
        ${firstIncomplete ? '▶ Pokračovat' : '🔄 Opakovat od začátku'}
      </button>
    </div>`;
  }
  document.getElementById('lesson-challenges').innerHTML = chHtml;

  document.querySelectorAll('.lesson-item').forEach(el => {
    el.classList.toggle('active', el.dataset.lesson === `${sectionNum}.${lessonNum}`);
  });
}

// ── Challenge workspace ────────────────────────────────────

async function openChallenge(sectionNum, lessonNum, index) {
  showView('challenge');
  state.currentChallenge = { section_num: sectionNum, lesson_num: lessonNum, index };
  state.hintsRevealed.clear();
  state.autosaveDirty = false;

  const [lessonData, draftData] = await Promise.all([
    api(`/api/lessons/${sectionNum}/${lessonNum}`),
    api(`/api/workspace/${sectionNum}/${lessonNum}/draft`),
  ]);

  const ch = lessonData.challenges ? lessonData.challenges.find(c => c.index === index) : null;
  if (!ch) {
    appendOutput('❌ Výzva nenalezena.\n', 'fail');
    return;
  }
  state.currentChallenge.data = ch;
  state.currentLesson = { section_num: sectionNum, lesson_num: lessonNum, data: lessonData };

  document.getElementById('breadcrumb').innerHTML =
    `<span class="text-accent" style="cursor:pointer" onclick="showDashboard()">Dashboard</span>` +
    ` › <span class="text-accent" style="cursor:pointer" onclick="openLesson('${sectionNum}','${lessonNum}')">${escapeHtml(lessonData.name)}</span>` +
    ` › ${escapeHtml(ch.title)}`;

  // Info panel
  document.getElementById('challenge-info-panel').innerHTML = buildChallengeInfoPanel(ch, lessonData.challenges.length);

  // Editor
  document.getElementById('editor-filename').textContent = draftData.path || '';
  state.fileContent = draftData.content || '';

  if (state.editor) {
    state.editor.setValue(state.fileContent);
    state.editor.clearHistory();
  } else {
    const edContainer = document.getElementById('editor-container');
    edContainer.innerHTML = '';
    state.editor = CodeMirror(edContainer, {
      value: state.fileContent,
      mode: 'python',
      theme: 'dracula',
      lineNumbers: true,
      matchBrackets: true,
      autoCloseBrackets: true,
      indentUnit: 4,
      tabSize: 4,
      indentWithTabs: false,
      extraKeys: {
        'Ctrl-S': () => saveFile(),
        'Ctrl-Enter': () => runCurrentChallenge(),
        'Tab': (cm) => {
          if (cm.somethingSelected()) cm.indentSelection('add');
          else cm.replaceSelection('    ', 'end');
        },
      },
    });
  }

  startAutosave();
  clearOutput();
  updateNavigationButtons(lessonData.challenges, index);
}

function buildChallengeInfoPanel(ch, totalChallenges) {
  let html = `
    <div class="info-section">
      <h4>${STATE_ICONS[ch.state] || '⬜'} Výzva ${ch.index}/${totalChallenges}: ${escapeHtml(ch.title)}</h4>
      <div class="info-content">
        <span class="tag">${ch.type}</span>
        <span class="tag">${ch.points} bodů</span>
        ${ch.difficulty > 1 ? `<span class="tag">${'⭐'.repeat(ch.difficulty)}</span>` : ''}
        ${ch.practice_mode && ch.practice_mode !== 'guided' ? `<span class="tag">${ch.practice_mode}</span>` : ''}
        ${ch.attempt_count > 0 ? `<br><small>${ch.attempt_count} pokusů</small>` : ''}
      </div>
    </div>`;

  if (ch.learning_objective) {
    html += `<div class="info-section"><h4>🎯 Cíl</h4><div class="info-content">${escapeHtml(ch.learning_objective)}</div></div>`;
  }
  if (ch.why_it_matters) {
    html += `<div class="info-section"><h4>💡 Proč na tom záleží</h4><div class="info-content">${renderMarkdown(ch.why_it_matters)}</div></div>`;
  }
  if (ch.key_concept) {
    html += `<div class="info-section"><h4>🔑 Klíčový koncept</h4><div class="info-content">${renderMarkdown(ch.key_concept)}</div></div>`;
  }
  if (ch.theory) {
    html += `<div class="info-section"><h4>📖 Teorie</h4><div class="info-content">${renderMarkdown(ch.theory)}</div></div>`;
  }
  if (ch.worked_example) {
    html += `<div class="info-section"><h4>🔬 Řešený příklad</h4><div class="info-content">${renderMarkdown(ch.worked_example)}</div></div>`;
  }
  if (ch.task) {
    html += `<div class="info-section task-section"><h4>📝 Zadání</h4><div class="info-content">${renderMarkdown(ch.task)}</div></div>`;
  }
  if (ch.example) {
    html += `<div class="info-section"><h4>Příklad</h4><div class="info-content"><pre>${escapeHtml(ch.example)}</pre></div></div>`;
  }
  if (ch.hints && ch.hints.length > 0) {
    html += `<div class="info-section"><h4>💡 Nápovědy</h4>`;
    for (let i = 0; i < ch.hints.length; i++) {
      html += `<div class="hint-item" onclick="revealHint(this, ${i})" data-hint="${escapeAttr(ch.hints[i])}">Nápověda ${i + 1}</div>`;
    }
    html += `</div>`;
  }
  if (ch.common_mistakes && ch.common_mistakes.length > 0) {
    html += `<div class="info-section collapsible">
      <h4 onclick="toggleCollapsible(this)" style="cursor:pointer">⚠️ Časté chyby ▸</h4>
      <div class="info-content collapsible-content" style="display:none">`;
    for (const m of ch.common_mistakes) {
      html += `<div style="margin-bottom:4px">• ${escapeHtml(m)}</div>`;
    }
    html += `</div></div>`;
  }
  if (ch.thinking_notes) {
    html += `<div class="info-section collapsible">
      <h4 onclick="toggleCollapsible(this)" style="cursor:pointer">🧠 Jak nad tím přemýšlet ▸</h4>
      <div class="info-content collapsible-content" style="display:none">${renderMarkdown(ch.thinking_notes)}</div>
    </div>`;
  }
  return html;
}

function toggleCollapsible(h4El) {
  const content = h4El.nextElementSibling;
  const isHidden = content.style.display === 'none';
  content.style.display = isHidden ? 'block' : 'none';
  h4El.textContent = h4El.textContent.replace(isHidden ? '▸' : '▾', isHidden ? '▾' : '▸');
}

function revealHint(el, index) {
  if (state.hintsRevealed.has(index)) return;
  state.hintsRevealed.add(index);
  el.textContent = el.dataset.hint;
  el.classList.add('revealed');
}

function updateNavigationButtons(challenges, currentIndex) {
  const prevBtn = document.getElementById('btn-prev-challenge');
  const nextBtn = document.getElementById('btn-next-challenge');
  if (prevBtn) prevBtn.disabled = currentIndex <= 1;
  if (nextBtn) nextBtn.disabled = currentIndex >= challenges.length;
}

function navigateChallenge(direction) {
  if (!state.currentChallenge) return;
  const { section_num, lesson_num, index } = state.currentChallenge;
  const newIndex = index + direction;
  if (newIndex < 1) return;
  if (state.currentLesson?.data?.challenges) {
    const ch = state.currentLesson.data.challenges.find(c => c.index === newIndex);
    if (!ch) return;
  }
  openChallenge(section_num, lesson_num, newIndex);
}

// ── Autosave ───────────────────────────────────────────────

function startAutosave() {
  stopAutosave();
  if (state.editor) {
    state.editor.on('change', markDirty);
  }
  state.autosaveTimer = setInterval(doAutosave, 15000);
}

function stopAutosave() {
  if (state.autosaveTimer) {
    clearInterval(state.autosaveTimer);
    state.autosaveTimer = null;
  }
  if (state.editor) {
    state.editor.off('change', markDirty);
  }
  if (state.autosaveDirty) doAutosave();
}

function markDirty() {
  state.autosaveDirty = true;
  const indicator = document.getElementById('autosave-indicator');
  if (indicator) indicator.textContent = '● neuloženo';
}

async function doAutosave() {
  if (!state.autosaveDirty || !state.currentChallenge || !state.editor) return;
  state.autosaveDirty = false;
  const { section_num, lesson_num } = state.currentChallenge;
  const content = state.editor.getValue();
  await apiPut(`/api/workspace/${section_num}/${lesson_num}/draft`, { content });
  const indicator = document.getElementById('autosave-indicator');
  if (indicator) {
    indicator.textContent = '✓ uloženo';
    setTimeout(() => { if (indicator.textContent === '✓ uloženo') indicator.textContent = ''; }, 2000);
  }
}

// ── Editor actions ─────────────────────────────────────────

async function saveFile() {
  if (!state.currentChallenge || !state.editor) return;
  const { section_num, lesson_num } = state.currentChallenge;
  const content = state.editor.getValue();
  state.autosaveDirty = false;
  const result = await apiPut(`/api/workspace/${section_num}/${lesson_num}/draft`, { content });
  if (result.success) {
    appendOutput('💾 Soubor uložen.\n', 'pass');
    const indicator = document.getElementById('autosave-indicator');
    if (indicator) indicator.textContent = '✓ uloženo';
  } else {
    appendOutput(`❌ Chyba při ukládání: ${result.error}\n`, 'fail');
  }
}

async function resetToStarter() {
  if (!state.currentChallenge) return;
  if (!confirm('Opravdu resetovat kód na výchozí stav? Tvůj aktuální kód bude ztracen.')) return;
  const { section_num, lesson_num } = state.currentChallenge;
  const result = await apiPost(`/api/workspace/${section_num}/${lesson_num}/reset`, {});
  if (result.content && state.editor) {
    state.editor.setValue(result.content);
    state.autosaveDirty = false;
    appendOutput('🔄 Kód resetován na výchozí stav.\n', 'pass');
  } else {
    appendOutput(`❌ Reset selhal: ${result.error || 'Unknown error'}\n`, 'fail');
  }
}

async function revealReference() {
  if (!state.currentChallenge) return;
  const { section_num, lesson_num, index } = state.currentChallenge;
  const result = await api(`/api/workspace/${section_num}/${lesson_num}/reference/${index}`);
  if (result.error) {
    appendOutput(`ℹ️ ${result.error}\n`, '');
    return;
  }
  let html = '<div class="feedback-panel" style="border-left-color:var(--purple)">';
  html += '<div class="feedback-title" style="color:var(--purple)">📋 Referenční řešení</div>';
  html += `<pre style="margin-top:8px;background:var(--bg-primary);padding:12px;border-radius:4px;white-space:pre-wrap">${escapeHtml(result.reference_solution)}</pre>`;
  if (result.solution_explanation) {
    html += `<div style="margin-top:8px;color:var(--text-secondary)">${renderMarkdown(result.solution_explanation)}</div>`;
  }
  html += '</div>';
  appendOutputHtml(html);
}

async function compareWithReference() {
  if (!state.currentChallenge || !state.editor) return;
  const { section_num, lesson_num, index } = state.currentChallenge;
  const result = await api(`/api/workspace/${section_num}/${lesson_num}/reference/${index}`);
  if (result.error) {
    appendOutput(`ℹ️ ${result.error}\n`, '');
    return;
  }
  const modal = document.getElementById('compare-modal');
  const container = document.getElementById('compare-container');
  container.innerHTML = '';

  CodeMirror.MergeView(container, {
    value: state.editor.getValue(),
    origLeft: null,
    orig: result.reference_solution,
    lineNumbers: true,
    mode: 'python',
    theme: 'dracula',
    highlightDifferences: true,
    connect: 'align',
    readOnly: true,
  });
  modal.style.display = 'flex';
}

function closeCompareModal() {
  document.getElementById('compare-modal').style.display = 'none';
  document.getElementById('compare-container').innerHTML = '';
}

async function runCurrentChallenge() {
  if (!state.currentChallenge || !state.editor) return;
  const { section_num, lesson_num, index } = state.currentChallenge;
  const content = state.editor.getValue();

  state.autosaveDirty = false;
  await apiPut(`/api/workspace/${section_num}/${lesson_num}/draft`, { content });

  appendOutput(`▶ Spouštím výzvu ${index}...\n`, '');

  const result = await apiPost(`/api/challenges/${section_num}/${lesson_num}/${index}/run`, {});

  if (result.error && !result.messages) {
    appendOutput(`❌ ${result.error}\n`, 'fail');
    return;
  }

  for (const msg of (result.messages || [])) {
    const cls = msg.includes('✓') || msg.includes('✅') ? 'pass' : 'fail';
    appendOutput(`  ${msg}\n`, cls);
  }

  if (result.passed) {
    appendOutput(`\n✅ VÝZVA SPLNĚNA! +${result.points} bodů\n`, 'pass');
    const lesson = state.currentLesson?.data;
    if (lesson) {
      const nextCh = lesson.challenges.find(c => c.index === index + 1);
      if (nextCh) {
        appendOutputHtml(`<div style="margin-top:8px">
          <button class="btn-primary" onclick="openChallenge('${section_num}','${lesson_num}',${index + 1})" style="margin-top:4px">
            ▶ Další výzva: ${escapeHtml(nextCh.title)}
          </button>
        </div>`);
      } else {
        const allPassed = lesson.challenges.every(c =>
          c.index === index ? true : ['currently_passing', 'mastered'].includes(c.state)
        );
        if (allPassed) {
          appendOutputHtml(`<div class="feedback-panel" style="border-left-color:var(--green)">
            <div class="feedback-title" style="color:var(--green)">🎉 Lekce dokončena!</div>
            <div>Gratulace! Všechny výzvy této lekce jsou splněny.</div>
            <button class="btn-primary" onclick="openLesson('${section_num}','${lesson_num}')" style="margin-top:8px">
              📋 Zpět na přehled lekce
            </button>
          </div>`);
        }
      }
    }
  } else {
    appendOutput(`\n❌ Ještě ne — zkus to znovu.\n`, 'fail');
  }

  if (result.state_before !== result.state_after) {
    const icon = STATE_ICONS[result.state_after] || '';
    appendOutput(`${icon} Stav: ${result.state_before} → ${result.state_after}\n`, '');
  }

  if (result.feedback) {
    const fb = result.feedback;
    let fbHtml = `<div class="feedback-panel">`;
    fbHtml += `<div class="feedback-title">${escapeHtml(fb.title || 'Zpětná vazba')}</div>`;
    if (fb.explanation) fbHtml += `<div class="feedback-guidance">${escapeHtml(fb.explanation)}</div>`;
    if (fb.guidance && fb.guidance.length > 0) {
      fbHtml += `<div class="feedback-guidance" style="margin-top:6px">`;
      for (const g of fb.guidance) fbHtml += `• ${escapeHtml(g)}<br>`;
      fbHtml += `</div>`;
    }
    if (fb.hint) fbHtml += `<div style="margin-top:6px;color:var(--yellow)">💡 ${escapeHtml(fb.hint)}</div>`;
    if (fb.encouragement) fbHtml += `<div style="margin-top:4px">${escapeHtml(fb.encouragement)}</div>`;
    fbHtml += `</div>`;
    appendOutputHtml(fbHtml);
  }

  loadCourseTree();
}

// ── Output panel ───────────────────────────────────────────

function appendOutput(text, cls) {
  const el = document.getElementById('output-content');
  const span = document.createElement('span');
  if (cls) span.className = cls;
  span.textContent = text;
  el.appendChild(span);
  el.scrollTop = el.scrollHeight;
}

function appendOutputHtml(html) {
  const el = document.getElementById('output-content');
  const div = document.createElement('div');
  div.innerHTML = html;
  el.appendChild(div);
  el.scrollTop = el.scrollHeight;
}

function clearOutput() {
  document.getElementById('output-content').innerHTML = '';
}

// ── Search ─────────────────────────────────────────────────

function showSearch() {
  showView('search');
  document.getElementById('breadcrumb').textContent = 'Hledat';
  document.getElementById('search-input').focus();
}

let searchTimeout = null;
async function doSearch(query) {
  clearTimeout(searchTimeout);
  if (query.length < 2) {
    document.getElementById('search-results').innerHTML = '';
    return;
  }
  searchTimeout = setTimeout(async () => {
    const results = await api(`/api/search?q=${encodeURIComponent(query)}`);
    let html = '';
    if (Array.isArray(results)) {
      for (const r of results) {
        html += `
          <div class="search-result-item" onclick="openLesson('${r.section_num}','${r.lesson_num}')">
            <div><strong>${escapeHtml(r.name)}</strong></div>
            <div class="muted">${escapeHtml(r.summary || '')} ${(r.tags || []).map(t => `<span class="tag">${escapeHtml(t)}</span>`).join('')}</div>
          </div>`;
      }
      if (results.length === 0) html = '<p class="muted">Žádné výsledky.</p>';
    }
    document.getElementById('search-results').innerHTML = html;
  }, 300);
}

// ── Persistent REPL ────────────────────────────────────────

function showRepl() {
  showView('repl');
  document.getElementById('breadcrumb').textContent = 'Python REPL';

  if (!state.replEditor) {
    const container = document.getElementById('repl-editor-container');
    container.innerHTML = '';
    state.replEditor = CodeMirror(container, {
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
  if (!state.replEditor) return;
  const code = state.replEditor.getValue();
  const outEl = document.getElementById('repl-output');

  const firstLine = code.split('\n')[0];
  const more = code.split('\n').length > 1 ? ' ...' : '';
  outEl.textContent += `>>> ${firstLine}${more}\n`;

  const result = await apiPost('/api/repl/execute', { code, timeout: 10 });

  if (result.stdout) outEl.textContent += result.stdout;
  if (result.stderr) outEl.textContent += result.stderr;
  if (result.returncode !== 0 && !result.stderr && result.returncode !== undefined) {
    outEl.textContent += `(exit code: ${result.returncode})\n`;
  }
  outEl.textContent += '\n';
  outEl.scrollTop = outEl.scrollHeight;
}

async function resetRepl() {
  await apiPost('/api/repl/reset', {});
  document.getElementById('repl-output').textContent = '🔄 Python session restarted.\n\n';
}

function clearReplOutput() {
  document.getElementById('repl-output').textContent = '';
}

// ── PTY Terminal ───────────────────────────────────────────

function showTerminal() {
  showView('terminal');
  document.getElementById('breadcrumb').textContent = 'Linux Terminal';

  if (!state.terminal) {
    initTerminal();
  }
  startTerminalPolling();
}

function initTerminal() {
  const container = document.getElementById('xterm-container');
  container.innerHTML = '';

  if (typeof Terminal === 'undefined') {
    container.innerHTML = '<p class="muted" style="padding:16px">Terminal library not loaded.</p>';
    return;
  }

  state.terminal = new Terminal({
    cursorBlink: true,
    fontSize: 14,
    fontFamily: "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
    theme: {
      background: '#1e1e2e',
      foreground: '#cdd6f4',
      cursor: '#89b4fa',
      cursorAccent: '#1e1e2e',
      black: '#45475a',
      red: '#f38ba8',
      green: '#a6e3a1',
      yellow: '#f9e2af',
      blue: '#89b4fa',
      magenta: '#cba6f7',
      cyan: '#94e2d5',
      white: '#bac2de',
      brightBlack: '#585b70',
      brightRed: '#f38ba8',
      brightGreen: '#a6e3a1',
      brightYellow: '#f9e2af',
      brightBlue: '#89b4fa',
      brightMagenta: '#cba6f7',
      brightCyan: '#94e2d5',
      brightWhite: '#a6adc8',
    },
  });

  state.terminal.open(container);

  if (typeof FitAddon !== 'undefined') {
    state.terminalFitAddon = new FitAddon.FitAddon();
    state.terminal.loadAddon(state.terminalFitAddon);
    setTimeout(() => {
      state.terminalFitAddon.fit();
      apiPost('/api/terminal/resize', { cols: state.terminal.cols, rows: state.terminal.rows });
    }, 100);

    window.addEventListener('resize', () => {
      if (state.terminalFitAddon && state.currentView === 'terminal') {
        state.terminalFitAddon.fit();
        apiPost('/api/terminal/resize', { cols: state.terminal.cols, rows: state.terminal.rows });
      }
    });
  }

  state.terminal.onData(data => {
    apiPost('/api/terminal/write', { data });
  });

  updateTerminalStatus(true);
}

function startTerminalPolling() {
  stopTerminalPolling();
  state.terminalPollTimer = setInterval(pollTerminal, 100);
}

function stopTerminalPolling() {
  if (state.terminalPollTimer) {
    clearInterval(state.terminalPollTimer);
    state.terminalPollTimer = null;
  }
}

async function pollTerminal() {
  if (!state.terminal) return;
  const result = await api('/api/terminal/read');
  if (result.data) {
    state.terminal.write(result.data);
  }
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
  await apiPost('/api/terminal/reset', {});
  if (state.terminal) {
    state.terminal.clear();
  }
  updateTerminalStatus(true);
}

// ── Utilities ──────────────────────────────────────────────

function escapeHtml(text) {
  if (!text) return '';
  const el = document.createElement('div');
  el.textContent = text;
  return el.innerHTML;
}

function escapeAttr(text) {
  if (!text) return '';
  return text.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;');
}

function renderMarkdown(text) {
  if (!text) return '';
  try {
    return marked.parse(text);
  } catch {
    return `<pre>${escapeHtml(text)}</pre>`;
  }
}

// ── Keyboard shortcuts ─────────────────────────────────────

document.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault();
    if (state.currentView === 'challenge') saveFile();
  }
  if (e.key === 'Escape') {
    closeCompareModal();
  }
});

// ── Init ───────────────────────────────────────────────────

(async function init() {
  await loadCourseTree();
  await showDashboard();
})();
