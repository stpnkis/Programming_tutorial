/**
 * ProgTrain — Lesson view and course tree navigation.
 */
const Lesson = (() => {

  async function loadCourseTree() {
    Store.s.sections = await Api.getSections();
    if (Store.s.sections.error) Store.s.sections = [];
    renderCourseTree();
  }

  function renderCourseTree() {
    const el = document.getElementById('course-tree');
    let html = '';

    for (const s of Store.s.sections) {
      const totalCh = s.lessons.reduce((sum, l) => sum + l.challenge_count, 0);
      const completed = s.lessons.reduce((sum, l) => sum + l.completed, 0);
      html += `
        <div class="section-item">
          <div class="section-header" onclick="Lesson.toggleSection(this)">
            <span class="arrow">▶</span>
            <span>${s.emoji} ${s.num}. ${UI.escapeHtml(s.name)}</span>
            <span class="lesson-progress">${completed}/${totalCh}</span>
          </div>
          <div class="section-lessons">`;
      for (const l of s.lessons) {
        const icon = l.completed === l.challenge_count && l.challenge_count > 0
          ? '💎' : l.completed > 0 ? '🔶' : '⬜';
        html += `
            <div class="lesson-item" data-lesson="${l.section_num}.${l.lesson_num}"
                 onclick="Lesson.open('${l.section_num}','${l.lesson_num}')">
              <span>${icon}</span>
              <span>${l.lesson_num}. ${UI.escapeHtml(l.name)}</span>
              <span class="lesson-progress">${l.completed}/${l.challenge_count}</span>
            </div>`;
      }
      html += `</div></div>`;
    }
    el.innerHTML = html;

    const totalChallenges = Store.s.sections.reduce(
      (s, sec) => s + sec.lessons.reduce((s2, l) => s2 + l.challenge_count, 0), 0);
    const totalCompleted = Store.s.sections.reduce(
      (s, sec) => s + sec.lessons.reduce((s2, l) => s2 + l.completed, 0), 0);
    document.getElementById('progress-summary').innerHTML = `
      ${totalCompleted}/${totalChallenges} výzev projde
      <div class="progress-bar"><div class="progress-bar-fill" style="width:${totalChallenges ? (totalCompleted/totalChallenges*100) : 0}%"></div></div>`;
  }

  function toggleSection(headerEl) {
    headerEl.classList.toggle('expanded');
    headerEl.nextElementSibling.classList.toggle('expanded');
  }

  async function open(sectionNum, lessonNum) {
    UI.showView('lesson');
    Store.s.currentLesson = { section_num: sectionNum, lesson_num: lessonNum };

    const data = await Api.getLessonDetail(sectionNum, lessonNum);
    if (data.error) {
      document.getElementById('lesson-header').innerHTML =
        `<p class="fail">Chyba: ${UI.escapeHtml(data.error)}</p>`;
      return;
    }
    Store.s.currentLesson.data = data;

    UI.setBreadcrumb(
      `<span class="text-accent" style="cursor:pointer" onclick="Dashboard.show()">Dashboard</span> › ${UI.escapeHtml(data.name)}`
    );

    // Header
    const meta = data.meta;
    let headerHtml = `
      <h1>${UI.escapeHtml(data.name)}</h1>
      <div class="lesson-meta">
        ${meta.difficulty ? '⭐'.repeat(meta.difficulty) + ' ' : ''}
        ${meta.estimated_minutes ? `⏱ ${meta.estimated_minutes} min ` : ''}
        ${(meta.tags || []).map(t => `<span class="tag">${UI.escapeHtml(t)}</span>`).join('')}
      </div>`;
    if (meta.summary) {
      headerHtml += `<p style="margin-top:8px;color:var(--text-secondary)">${UI.escapeHtml(meta.summary)}</p>`;
    }
    document.getElementById('lesson-header').innerHTML = headerHtml;

    // Theory
    let theoryHtml = '';
    if (data.why_it_matters) {
      theoryHtml += `<div class="lesson-section"><h3>🎯 Proč se to učit</h3><div class="content">${UI.renderMarkdown(data.why_it_matters)}</div></div>`;
    }
    if (data.what_you_will_learn) {
      theoryHtml += `<div class="lesson-section"><h3>🧠 Co budeš umět</h3><div class="content">${UI.renderMarkdown(data.what_you_will_learn)}</div></div>`;
    }
    if (data.key_theory) {
      theoryHtml += `<div class="lesson-section"><h3>📖 Klíčová teorie</h3><div class="content">${UI.renderMarkdown(data.key_theory)}</div></div>`;
    }
    if (data.before_you_code) {
      theoryHtml += `<div class="lesson-section before-you-code"><h3>🚀 Než začneš kódovat</h3><div class="content">${UI.renderMarkdown(data.before_you_code)}</div></div>`;
    }
    document.getElementById('lesson-theory').innerHTML = theoryHtml;

    // Lesson summary + next step (shown after challenge list)
    let footerHtml = '';
    if (data.lesson_summary) {
      footerHtml += `<div class="lesson-section lesson-summary"><h3>📋 Shrnutí lekce</h3><div class="content">${UI.renderMarkdown(data.lesson_summary)}</div></div>`;
    }
    if (data.recommended_next) {
      footerHtml += `<div class="lesson-section recommended-next"><h3>👉 Kam dál</h3><div class="content">${UI.renderMarkdown(data.recommended_next)}</div></div>`;
    }

    // Challenge list
    const totalCh = data.challenges.length;
    const passedCh = data.challenges.filter(c => ['currently_passing', 'mastered'].includes(c.state)).length;
    let chHtml = `<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
      <h3>📝 Výzvy (${passedCh}/${totalCh})</h3>
      <div class="progress-bar" style="width:150px"><div class="progress-bar-fill" style="width:${totalCh ? passedCh/totalCh*100 : 0}%"></div></div>
    </div><div class="challenge-list">`;

    for (const ch of data.challenges) {
      const icon = Store.STATE_ICONS[ch.state] || '⬜';
      const typeCfg = Store.getTypeConfig(ch.type);
      chHtml += `
        <div class="challenge-list-item" onclick="Challenge.open('${sectionNum}','${lessonNum}',${ch.index})">
          <span class="challenge-state">${icon}</span>
          <div class="challenge-title">
            <div>${ch.index}. ${UI.escapeHtml(ch.title)}</div>
            ${ch.learning_objective ? `<div style="font-size:12px;color:var(--text-muted)">${UI.escapeHtml(ch.learning_objective)}</div>` : ''}
          </div>
          <div class="challenge-meta">
            <span class="tag ${typeCfg.cls}">${typeCfg.icon} ${typeCfg.label}</span>
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
        <button class="btn-primary" onclick="Challenge.open('${sectionNum}','${lessonNum}',${target.index})" style="padding:12px 24px;font-size:15px">
          ${firstIncomplete ? '▶ Pokračovat' : '🔄 Opakovat od začátku'}
        </button>
      </div>`;
    }
    document.getElementById('lesson-challenges').innerHTML = chHtml;

    // Lesson footer — summary & next recommendation
    const footerEl = document.getElementById('lesson-footer');
    if (footerEl) footerEl.innerHTML = footerHtml;

    // Highlight active lesson in sidebar
    document.querySelectorAll('.lesson-item').forEach(el => {
      el.classList.toggle('active', el.dataset.lesson === `${sectionNum}.${lessonNum}`);
    });
  }

  return { loadCourseTree, renderCourseTree, toggleSection, open };
})();
