/**
 * ProgTrain Desktop — main entry point (v3).
 *
 * Module loading order (via index.html script tags):
 *   1. store.js    — state + config
 *   2. api.js      — API client
 *   3. ui.js       — shared UI utilities
 *   4. workspace.js — autosave, draft management
 *   5. lab.js      — REPL + terminal
 *   6. dashboard.js — dashboard + guidance
 *   7. lesson.js   — lesson view + course tree
 *   8. challenge.js — challenge workspace + type-specific UX
 *   9. keyboard.js — shortcuts + command palette
 *  10. app.js      — this file: init + search glue
 */

// ── Search view ──────────────────────────────────────────────

function showSearchView() {
  UI.showView('search');
  UI.setBreadcrumb('Hledat');
  document.getElementById('search-input').focus();
}

let _searchTimeout = null;
async function doSearch(query) {
  clearTimeout(_searchTimeout);
  if (query.length < 2) {
    document.getElementById('search-results').innerHTML = '';
    return;
  }
  _searchTimeout = setTimeout(async () => {
    const results = await Api.search(query);
    let html = '';
    if (Array.isArray(results)) {
      for (const r of results) {
        html += `
          <div class="search-result-item" onclick="Lesson.open('${r.section_num}','${r.lesson_num}')">
            <div><strong>${UI.escapeHtml(r.name)}</strong></div>
            <div class="muted">${UI.escapeHtml(r.summary || '')} ${(r.tags || []).map(t => `<span class="tag">${UI.escapeHtml(t)}</span>`).join('')}</div>
          </div>`;
      }
      if (results.length === 0) html = '<p class="muted">Žádné výsledky.</p>';
    }
    document.getElementById('search-results').innerHTML = html;
  }, 300);
}

// ── Init ─────────────────────────────────────────────────────

(async function init() {
  Keyboard.init();
  await Lesson.loadCourseTree();
  await Dashboard.show();
})();
