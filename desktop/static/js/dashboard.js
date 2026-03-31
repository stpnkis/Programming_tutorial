/**
 * ProgTrain — Dashboard, progress overview, and learning guidance.
 */
const Dashboard = (() => {

  async function show() {
    UI.showView('dashboard');
    UI.setBreadcrumb('');

    const [snap, recs] = await Promise.all([
      Api.getSnapshot(),
      Api.getCategorizedRecs(),
    ]);

    renderStats(snap);
    renderGuidance(snap, recs);
    renderRecommendations(recs);
  }

  function renderStats(snap) {
    const el = document.getElementById('dashboard-stats');
    const pct = Math.round(snap.progress_pct || 0);
    el.innerHTML = `
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
        <div class="stat-value">${pct}%</div>
        <div class="stat-label">Celkový pokrok</div>
        <div class="progress-bar"><div class="progress-bar-fill" style="width:${pct}%"></div></div>
      </div>`;
  }

  function renderGuidance(snap, recs) {
    const el = document.getElementById('dashboard-guidance');
    if (!el) return;

    // Determine primary action
    let primaryHtml = '';
    const reg = recs.regressions || [];
    const rev = recs.review || [];
    const cont = recs.continue || [];
    const newm = recs.new || [];

    if (reg.length > 0) {
      const r = reg[0];
      primaryHtml = `
        <div class="guidance-card guidance-urgent" onclick="Challenge.openFromRec('${r.lesson_id}')">
          <div class="guidance-icon">🔻</div>
          <div class="guidance-body">
            <div class="guidance-title">Opravit regresi</div>
            <div class="guidance-detail">${UI.escapeHtml(r.lesson_name)} — ${UI.escapeHtml(r.reason)}</div>
          </div>
          <div class="guidance-action">Opravit →</div>
        </div>`;
    } else if (rev.length > 0) {
      const r = rev[0];
      primaryHtml = `
        <div class="guidance-card guidance-review" onclick="Challenge.openFromRec('${r.lesson_id}')">
          <div class="guidance-icon">🔄</div>
          <div class="guidance-body">
            <div class="guidance-title">Čas na opakování</div>
            <div class="guidance-detail">${UI.escapeHtml(r.lesson_name)} — ${UI.escapeHtml(r.reason)}</div>
          </div>
          <div class="guidance-action">Opakovat →</div>
        </div>`;
    } else if (cont.length > 0) {
      const r = cont[0];
      primaryHtml = `
        <div class="guidance-card guidance-continue" onclick="Challenge.openFromRec('${r.lesson_id}')">
          <div class="guidance-icon">📝</div>
          <div class="guidance-body">
            <div class="guidance-title">Pokračovat v učení</div>
            <div class="guidance-detail">${UI.escapeHtml(r.lesson_name)} — ${UI.escapeHtml(r.reason)}</div>
          </div>
          <div class="guidance-action">Pokračovat →</div>
        </div>`;
    } else if (newm.length > 0) {
      const r = newm[0];
      primaryHtml = `
        <div class="guidance-card guidance-new" onclick="Challenge.openFromRec('${r.lesson_id}')">
          <div class="guidance-icon">🆕</div>
          <div class="guidance-body">
            <div class="guidance-title">Začít nový materiál</div>
            <div class="guidance-detail">${UI.escapeHtml(r.lesson_name)}</div>
          </div>
          <div class="guidance-action">Začít →</div>
        </div>`;
    } else {
      primaryHtml = `
        <div class="guidance-card guidance-empty">
          <div class="guidance-icon">🎉</div>
          <div class="guidance-body">
            <div class="guidance-title">Všechno je hotové!</div>
            <div class="guidance-detail">Gratulace — zatím žádné doporučení.</div>
          </div>
        </div>`;
    }

    // Summary line
    const summaryParts = [];
    if (reg.length > 0)  summaryParts.push(`<span class="guidance-badge badge-fix">${reg.length} regresí</span>`);
    if (rev.length > 0)  summaryParts.push(`<span class="guidance-badge badge-review">${rev.length} k opakování</span>`);
    if (cont.length > 0) summaryParts.push(`<span class="guidance-badge badge-continue">${cont.length} rozpracováno</span>`);
    if (newm.length > 0) summaryParts.push(`<span class="guidance-badge badge-new">${newm.length} nových</span>`);

    el.innerHTML = `
      <h2 style="margin-bottom:12px">🎯 Co dělat dál</h2>
      ${primaryHtml}
      ${summaryParts.length > 0 ? `<div class="guidance-summary">${summaryParts.join(' ')}</div>` : ''}`;
  }

  function renderRecommendations(recs) {
    const el = document.getElementById('dashboard-recs');
    const categoryOrder = ['regressions', 'review', 'continue', 'new'];
    const categoryNames = {
      regressions: '🔻 Opravit regrese',
      review: '🔄 Opakování',
      continue: '📝 Pokračovat',
      new: '🆕 Nový materiál',
    };

    let html = '<h2 style="margin-bottom:16px">📋 Doporučení</h2>';

    for (const cat of categoryOrder) {
      const items = recs[cat];
      if (!items || items.length === 0) continue;
      html += `<div class="rec-section"><h3>${categoryNames[cat]}</h3>`;
      for (const r of items.slice(0, 5)) {
        const catInfo = Store.CATEGORY_LABELS[r.category] || { label: '?', cls: 'new' };
        html += `
          <div class="rec-card" onclick="Lesson.open('${r.lesson_id.split('.')[0]}','${r.lesson_id.split('.')[1]}')">
            <span class="rec-cat ${catInfo.cls}">${catInfo.label}</span>
            <span>${UI.escapeHtml(r.lesson_name)}</span>
            <span style="color:var(--text-muted);font-size:12px;margin-left:auto">${UI.escapeHtml(r.reason)}</span>
          </div>`;
      }
      html += '</div>';
    }

    if (Object.values(recs).every(v => !v || v.length === 0)) {
      html += '<p class="muted">Zatím žádná doporučení. Začni řešit výzvy!</p>';
    }
    el.innerHTML = html;
  }

  return { show };
})();
