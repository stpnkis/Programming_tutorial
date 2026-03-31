/**
 * ProgTrain — UI utilities and shared components.
 */
const UI = (() => {

  function escapeHtml(text) {
    if (!text) return '';
    const el = document.createElement('div');
    el.textContent = text;
    return el.innerHTML;
  }

  function escapeAttr(text) {
    if (!text) return '';
    return text.replace(/&/g, '&amp;').replace(/"/g, '&quot;')
               .replace(/'/g, '&#39;').replace(/</g, '&lt;');
  }

  function renderMarkdown(text) {
    if (!text) return '';
    try { return marked.parse(text); }
    catch { return `<pre>${escapeHtml(text)}</pre>`; }
  }

  function showView(viewId) {
    const st = Store.s;
    if (st.currentView === 'challenge' && viewId !== 'challenge') {
      Workspace.stopAutosave();
    }
    if (st.currentView === 'terminal' && viewId !== 'terminal') {
      Lab.stopTerminalPolling();
    }
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    const el = document.getElementById(viewId + '-view');
    if (el) el.classList.add('active');
    st.currentView = viewId;
    // Update topbar active states
    document.querySelectorAll('.topbar-right button').forEach(b => b.classList.remove('topbar-active'));
  }

  function setBreadcrumb(html) {
    document.getElementById('breadcrumb').innerHTML = html;
  }

  /** Append text to #output-content */
  function appendOutput(text, cls) {
    const el = document.getElementById('output-content');
    if (!el) return;
    const span = document.createElement('span');
    if (cls) span.className = cls;
    span.textContent = text;
    el.appendChild(span);
    el.scrollTop = el.scrollHeight;
  }

  /** Append HTML to #output-content */
  function appendOutputHtml(html) {
    const el = document.getElementById('output-content');
    if (!el) return;
    const div = document.createElement('div');
    div.innerHTML = html;
    el.appendChild(div);
    el.scrollTop = el.scrollHeight;
  }

  function clearOutput() {
    const el = document.getElementById('output-content');
    if (el) el.innerHTML = '';
  }

  /** Toast notification */
  function toast(message, type = 'info', duration = 3000) {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      document.body.appendChild(container);
    }
    const t = document.createElement('div');
    t.className = `toast toast-${type}`;
    t.textContent = message;
    container.appendChild(t);
    requestAnimationFrame(() => t.classList.add('toast-show'));
    setTimeout(() => {
      t.classList.remove('toast-show');
      setTimeout(() => t.remove(), 300);
    }, duration);
  }

  /** Build a keyboard shortcut badge */
  function kbdBadge(keys) {
    return `<kbd class="kbd-badge">${escapeHtml(keys)}</kbd>`;
  }

  return {
    escapeHtml, escapeAttr, renderMarkdown,
    showView, setBreadcrumb,
    appendOutput, appendOutputHtml, clearOutput,
    toast, kbdBadge,
  };
})();
