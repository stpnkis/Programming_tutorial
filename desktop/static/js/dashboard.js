/**
 * ProgTrain — Dashboard, progress overview, and learning guidance.
 * Integrates concept mastery, adaptive study plans, projects, and recommendations.
 */
const Dashboard = (() => {

    let _studyMode = 'guided';

    async function show() {
        UI.showView('dashboard');
        UI.setBreadcrumb('');

        const [snap, recs, concepts, plan, projects] = await Promise.all([
            Api.getSnapshot(),
            Api.getCategorizedRecs(),
            Api.getConceptMastery(),
            Api.getStudyPlan(_studyMode),
            Api.getProjects(),
        ]);

        renderStudyPlan(plan);
        renderGuidance(snap, recs);
        renderStats(snap);
        renderConcepts(concepts);
        renderProjects(projects);
        renderRecommendations(recs);
    }

    // ── Study Plan ─────────────────────────────────────────────

    function renderStudyPlan(plan) {
        const el = document.getElementById('dashboard-study-plan');
        if (!el || plan.error) { if (el) el.innerHTML = ''; return; }

        const modes = [
            { id: 'guided', emoji: '📚', name: 'Vedený' },
            { id: 'fast_track', emoji: '⚡', name: 'Zrychlený' },
            { id: 'reinforcement', emoji: '🔄', name: 'Opakování' },
            { id: 'interview', emoji: '🎯', name: 'Interview' },
        ];

        let modeHtml = modes.map(m =>
            `<button class="mode-btn ${m.id === _studyMode ? 'mode-active' : ''}"
              onclick="Dashboard.setMode('${m.id}')">${m.emoji} ${UI.escapeHtml(m.name)}</button>`
        ).join('');

        let stepsHtml = '';
        for (const step of (plan.steps || []).slice(0, 5)) {
            const catInfo = Store.CATEGORY_LABELS[step.category] || { label: '?', cls: 'new' };
            stepsHtml += `
        <div class="plan-step" onclick="Lesson.open('${step.section_num}','${step.lesson_num}')">
          <span class="rec-cat ${catInfo.cls}">${catInfo.label}</span>
          <span>${UI.escapeHtml(step.lesson_name)}</span>
          <span class="plan-step-reason">${UI.escapeHtml(step.reason)}</span>
        </div>`;
        }

        let focusHtml = '';
        if (plan.focus_concepts && plan.focus_concepts.length > 0) {
            focusHtml = `<div class="plan-focus">Zaměření: ${plan.focus_concepts.map(c => `<span class="tag">${UI.escapeHtml(c)}</span>`).join(' ')}</div>`;
        }

        let summaryBadges = '';
        if (plan.weak_concept_count > 0) summaryBadges += `<span class="guidance-badge badge-fix">${plan.weak_concept_count} slabých</span>`;
        if (plan.regressed_concept_count > 0) summaryBadges += `<span class="guidance-badge badge-fix">${plan.regressed_concept_count} regresí</span>`;
        if (plan.ready_to_learn && plan.ready_to_learn.length > 0) summaryBadges += `<span class="guidance-badge badge-new">${plan.ready_to_learn.length} připraveno</span>`;

        el.innerHTML = `
      <div class="study-plan-panel">
        <div class="plan-header">
          <h2>${plan.mode_emoji || '📚'} Co dnes dělat</h2>
          <div class="mode-selector">${modeHtml}</div>
        </div>
        <div class="plan-reasoning">${UI.escapeHtml(plan.reasoning || '')}</div>
        ${summaryBadges ? `<div class="plan-badges">${summaryBadges}</div>` : ''}
        <div class="plan-meta">
          <span>⏱ ~${plan.estimated_minutes || 0} min</span>
          <span>📊 ${plan.overall_mastery_pct || 0}% konceptů zvládnuto</span>
          ${plan.focus_area ? `<span>🎯 ${UI.escapeHtml(plan.focus_area)}</span>` : ''}
        </div>
        ${focusHtml}
        <div class="plan-steps">${stepsHtml || '<p class="muted">Žádné kroky — vše je zvládnuto! 🎉</p>'}</div>
      </div>`;
    }

    function setMode(mode) {
        _studyMode = mode;
        show();
    }

    // ── Stats ──────────────────────────────────────────────────

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

    // ── Guidance ───────────────────────────────────────────────

    function renderGuidance(snap, recs) {
        const el = document.getElementById('dashboard-guidance');
        if (!el) return;

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

        const summaryParts = [];
        if (reg.length > 0) summaryParts.push(`<span class="guidance-badge badge-fix">${reg.length} regresí</span>`);
        if (rev.length > 0) summaryParts.push(`<span class="guidance-badge badge-review">${rev.length} k opakování</span>`);
        if (cont.length > 0) summaryParts.push(`<span class="guidance-badge badge-continue">${cont.length} rozpracováno</span>`);
        if (newm.length > 0) summaryParts.push(`<span class="guidance-badge badge-new">${newm.length} nových</span>`);

        el.innerHTML = `
      <h2 style="margin-bottom:12px">🎯 Další krok</h2>
      ${primaryHtml}
      ${summaryParts.length > 0 ? `<div class="guidance-summary">${summaryParts.join(' ')}</div>` : ''}`;
    }

    // ── Concept Mastery ────────────────────────────────────────

    function renderConcepts(data) {
        const el = document.getElementById('dashboard-concepts');
        if (!el || data.error || !data.concepts) { if (el) el.innerHTML = ''; return; }

        const concepts = data.concepts;
        const weak = data.weak_concepts || [];
        const ready = data.ready_concepts || [];

        // Group by category
        const categories = {};
        for (const [cid, c] of Object.entries(concepts)) {
            const cat = c.category || 'other';
            if (!categories[cat]) categories[cat] = [];
            categories[cat].push({ id: cid, ...c });
        }

        const masteryIcons = {
            not_seen: '⬜', weak: '🔴', developing: '🟡',
            proficient: '🟢', mastered: '💎', regressed: '🔻',
        };
        const masteryLabels = {
            not_seen: 'Neviděno', weak: 'Slabé', developing: 'Rozvíjí se',
            proficient: 'Zdatný', mastered: 'Zvládnuto', regressed: 'Regrese',
        };

        // Summary bar
        const total = Object.keys(concepts).length;
        const counts = {};
        for (const c of Object.values(concepts)) {
            counts[c.mastery] = (counts[c.mastery] || 0) + 1;
        }
        const masteredPct = total > 0 ? Math.round(((counts.mastered || 0) + (counts.proficient || 0)) / total * 100) : 0;

        let html = `<div class="concepts-panel">
      <div class="concepts-header">
        <h2>🧠 Znalost konceptů</h2>
        <span class="concepts-summary">${masteredPct}% zvládnuto (${total} konceptů)</span>
      </div>
      <div class="mastery-bar">`;
        for (const level of ['mastered', 'proficient', 'developing', 'weak', 'regressed', 'not_seen']) {
            const cnt = counts[level] || 0;
            if (cnt === 0) continue;
            const pct = (cnt / total * 100).toFixed(1);
            html += `<div class="mastery-segment mastery-${level}" style="width:${pct}%" title="${masteryLabels[level]}: ${cnt}"></div>`;
        }
        html += `</div><div class="mastery-legend">`;
        for (const level of ['mastered', 'proficient', 'developing', 'weak', 'regressed', 'not_seen']) {
            const cnt = counts[level] || 0;
            if (cnt === 0) continue;
            html += `<span class="legend-item">${masteryIcons[level]} ${masteryLabels[level]}: ${cnt}</span>`;
        }
        html += `</div>`;

        // Weak concepts highlight
        if (weak.length > 0) {
            html += `<div class="concepts-weak"><h4>🔴 Slabé koncepty — procvič je</h4><div class="concept-chips">`;
            for (const cid of weak.slice(0, 8)) {
                const c = concepts[cid];
                if (!c) continue;
                html += `<span class="concept-chip chip-weak" title="${UI.escapeAttr(c.key_insight || '')}">${masteryIcons[c.mastery]} ${UI.escapeHtml(c.name)} <small>(${c.passing_challenges}/${c.total_challenges})</small></span>`;
            }
            html += `</div></div>`;
        }

        // Category grid (collapsed by default)
        const catNames = { python: '🐍 Python', oop: '🏗️ OOP', ds: '📊 Datové struktury', testing: '🧪 Testování', git: '📦 Git', debugging: '🐛 Debugging' };
        html += `<div class="concepts-categories">`;
        for (const [cat, items] of Object.entries(categories).sort()) {
            const catMastered = items.filter(c => c.mastery === 'mastered' || c.mastery === 'proficient').length;
            const catPct = Math.round(catMastered / items.length * 100);
            html += `<div class="concept-category">
        <div class="concept-cat-header" onclick="Dashboard.toggleConceptCat(this)">
          <span>${catNames[cat] || cat} (${catMastered}/${items.length})</span>
          <div class="progress-bar" style="width:80px"><div class="progress-bar-fill" style="width:${catPct}%"></div></div>
          <span class="arrow">▸</span>
        </div>
        <div class="concept-cat-items" style="display:none">`;
            for (const c of items.sort((a, b) => a.name.localeCompare(b.name))) {
                html += `<div class="concept-item mastery-${c.mastery}">
          <span>${masteryIcons[c.mastery]}</span>
          <span>${UI.escapeHtml(c.name)}</span>
          <span class="concept-score">${c.passing_challenges}/${c.total_challenges}</span>
        </div>`;
            }
            html += `</div></div>`;
        }
        html += `</div></div>`;

        el.innerHTML = html;
    }

    function toggleConceptCat(headerEl) {
        const items = headerEl.nextElementSibling;
        const arrow = headerEl.querySelector('.arrow');
        const isHidden = items.style.display === 'none';
        items.style.display = isHidden ? 'block' : 'none';
        if (arrow) arrow.textContent = isHidden ? '▾' : '▸';
    }

    // ── Projects ───────────────────────────────────────────────

    function renderProjects(projects) {
        const el = document.getElementById('dashboard-projects');
        if (!el || !Array.isArray(projects) || projects.length === 0) {
            if (el) el.innerHTML = '';
            return;
        }

        const diffIcons = { beginner: '🟢', intermediate: '🟡', advanced: '🔴' };
        let html = `<div class="projects-panel"><h2>🏗️ Projekty</h2><div class="project-grid">`;

        for (const p of projects) {
            const avail = p.available;
            html += `
        <div class="project-card ${avail ? '' : 'project-locked'}">
          <div class="project-card-header">
            <span>${diffIcons[p.difficulty] || '⚪'} ${UI.escapeHtml(p.name)}</span>
            ${avail ? '<span class="tag tag-available">Dostupný</span>' : '<span class="tag tag-locked">🔒 Zamčený</span>'}
          </div>
          <div class="project-description">${UI.escapeHtml(p.description || '')}</div>
          <div class="project-meta">
            <span>${(p.milestones || []).length} milníků</span>
            ${p.required_concepts ? `<span>${p.required_concepts.length} konceptů potřeba</span>` : ''}
          </div>
          ${avail ? '' : `<div class="project-prereqs">Potřebuješ: ${(p.required_concepts || []).slice(0, 3).map(c => `<span class="concept-chip chip-locked">${UI.escapeHtml(c)}</span>`).join(' ')}</div>`}
        </div>`;
        }
        html += `</div></div>`;
        el.innerHTML = html;
    }

    // ── Recommendations ────────────────────────────────────────

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

    return { show, setMode, toggleConceptCat };
})();
