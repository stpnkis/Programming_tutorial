/**
 * ProgTrain — Challenge workspace: editor, execution, navigation.
 * Challenge-type-specific rendering and UX.
 */
const Challenge = (() => {

    // ── Open a challenge ───────────────────────────────────────

    async function open(sectionNum, lessonNum, index) {
        UI.showView('challenge');
        const st = Store.s;
        st.currentChallenge = { section_num: sectionNum, lesson_num: lessonNum, index };
        st.hintsRevealed.clear();
        st.autosaveDirty = false;

        const [lessonData, draftData] = await Promise.all([
            Api.getLessonDetail(sectionNum, lessonNum),
            Api.getDraft(sectionNum, lessonNum),
        ]);

        const ch = lessonData.challenges ? lessonData.challenges.find(c => c.index === index) : null;
        if (!ch) {
            UI.appendOutput('❌ Výzva nenalezena.\n', 'fail');
            return;
        }
        st.currentChallenge.data = ch;
        st.currentLesson = { section_num: sectionNum, lesson_num: lessonNum, data: lessonData };

        UI.setBreadcrumb(
            `<span class="text-accent" style="cursor:pointer" onclick="Dashboard.show()">Dashboard</span>` +
            ` › <span class="text-accent" style="cursor:pointer" onclick="Lesson.open('${sectionNum}','${lessonNum}')">${UI.escapeHtml(lessonData.name)}</span>` +
            ` › ${UI.escapeHtml(ch.title)}`
        );

        // Info panel — with challenge-type-specific content
        document.getElementById('challenge-info-panel').innerHTML = buildInfoPanel(ch, lessonData.challenges.length);

        // Toolbar — type-specific labels
        updateToolbar(ch);

        // Editor
        document.getElementById('editor-filename').textContent = draftData.path || '';
        st.fileContent = draftData.content || '';

        if (st.editor) {
            st.editor.setValue(st.fileContent);
            st.editor.clearHistory();
        } else {
            const edContainer = document.getElementById('editor-container');
            edContainer.innerHTML = '';
            st.editor = CodeMirror(edContainer, {
                value: st.fileContent,
                mode: 'python',
                theme: 'dracula',
                lineNumbers: true,
                matchBrackets: true,
                autoCloseBrackets: true,
                indentUnit: 4,
                tabSize: 4,
                indentWithTabs: false,
                extraKeys: {
                    'Ctrl-S': () => Workspace.save(),
                    'Ctrl-Enter': () => run(),
                    'Tab': (cm) => {
                        if (cm.somethingSelected()) cm.indentSelection('add');
                        else cm.replaceSelection('    ', 'end');
                    },
                },
            });
        }

        Workspace.startAutosave();
        UI.clearOutput();
        updateNavButtons(lessonData.challenges, index);
        st.focusZone = 'editor';
    }

    /** Open from a recommendation card (lesson_id = "01.02") */
    function openFromRec(lessonId) {
        const parts = lessonId.split('.');
        if (parts.length === 2) Lesson.open(parts[0], parts[1]);
    }

    // ── Challenge-type-specific info panel ─────────────────────

    function buildInfoPanel(ch, totalChallenges) {
        const tc = Store.getTypeConfig(ch.type);
        let html = '';

        // Header with type badge
        html += `
      <div class="info-section">
        <h4>${Store.STATE_ICONS[ch.state] || '⬜'} Výzva ${ch.index}/${totalChallenges}: ${UI.escapeHtml(ch.title)}</h4>
        <div class="info-content">
          <span class="tag ${tc.cls}">${tc.icon} ${tc.label}</span>
          <span class="tag">${ch.points} bodů</span>
          ${ch.difficulty > 1 ? `<span class="tag">${'⭐'.repeat(ch.difficulty)}</span>` : ''}
          ${ch.practice_mode && ch.practice_mode !== 'guided' ? `<span class="tag tag-practice-${ch.practice_mode}">${ch.practice_mode === 'open' ? '🎨 Samostatná úloha' : ch.practice_mode === 'creative' ? '🎨 Kreativní úloha' : ch.practice_mode}</span>` : ''}
          ${ch.attempt_count > 0 ? `<br><small>${ch.attempt_count} pokusů</small>` : ''}
        </div>
      </div>`;

        // Type-specific instruction banner
        html += `<div class="info-section type-banner ${tc.cls}">
      <div class="type-banner-text">${tc.icon} ${UI.escapeHtml(tc.toolbarHint)}</div>
    </div>`;

        // Learning objective
        if (ch.learning_objective) {
            html += `<div class="info-section"><h4>🎯 Cíl</h4><div class="info-content">${UI.escapeHtml(ch.learning_objective)}</div></div>`;
        }

        // Why it matters
        if (ch.why_it_matters) {
            html += `<div class="info-section"><h4>💡 Proč na tom záleží</h4><div class="info-content">${UI.renderMarkdown(ch.why_it_matters)}</div></div>`;
        }

        // Key concept
        if (ch.key_concept) {
            html += `<div class="info-section"><h4>🔑 Klíčový koncept</h4><div class="info-content">${UI.renderMarkdown(ch.key_concept)}</div></div>`;
        }

        // Theory
        if (ch.theory) {
            html += `<div class="info-section"><h4>📖 Teorie</h4><div class="info-content">${UI.renderMarkdown(ch.theory)}</div></div>`;
        }

        // Worked example
        if (ch.worked_example) {
            html += `<div class="info-section"><h4>🔬 Řešený příklad</h4><div class="info-content">${UI.renderMarkdown(ch.worked_example)}</div></div>`;
        }

        // Task (highlighted)
        if (ch.task) {
            html += `<div class="info-section task-section"><h4>📝 Zadání</h4><div class="info-content">${UI.renderMarkdown(ch.task)}</div></div>`;
        }

        // Example I/O
        if (ch.example) {
            html += `<div class="info-section"><h4>Příklad</h4><div class="info-content"><pre>${UI.escapeHtml(ch.example)}</pre></div></div>`;
        }

        // Hints (progressive reveal)
        if (ch.hints && ch.hints.length > 0) {
            html += `<div class="info-section"><h4>💡 Nápovědy</h4>`;
            for (let i = 0; i < ch.hints.length; i++) {
                html += `<div class="hint-item" onclick="Challenge.revealHint(this, ${i})" data-hint="${UI.escapeAttr(ch.hints[i])}">Nápověda ${i + 1} <span class="kbd-badge-inline">klikni</span></div>`;
            }
            html += `</div>`;
        }

        // Thinking notes (first-class panel, open by default for debugging/trace types)
        if (ch.thinking_notes) {
            const openByDefault = ['debugging', 'trace', 'refactoring'].includes(ch.type);
            html += `<div class="info-section thinking-panel ${openByDefault ? '' : 'collapsible'}">
        <h4 ${openByDefault ? '' : 'onclick="Challenge.toggleCollapsible(this)" style="cursor:pointer"'}>
          🧠 Jak nad tím přemýšlet ${openByDefault ? '' : '▸'}
        </h4>
        <div class="info-content thinking-content" ${openByDefault ? '' : 'style="display:none"'}>${UI.renderMarkdown(ch.thinking_notes)}</div>
      </div>`;
        }

        // Common mistakes (always collapsible)
        if (ch.common_mistakes && ch.common_mistakes.length > 0) {
            html += `<div class="info-section collapsible">
        <h4 onclick="Challenge.toggleCollapsible(this)" style="cursor:pointer">⚠️ Časté chyby ▸</h4>
        <div class="info-content collapsible-content" style="display:none">`;
            for (const m of ch.common_mistakes) {
                html += `<div style="margin-bottom:4px">• ${UI.escapeHtml(m)}</div>`;
            }
            html += `</div></div>`;
        }

        // Expected misconceptions (collapsible, pedagogically distinct from mistakes)
        if (ch.expected_misconceptions && ch.expected_misconceptions.length > 0) {
            html += `<div class="info-section collapsible">
        <h4 onclick="Challenge.toggleCollapsible(this)" style="cursor:pointer">🤔 Na co si dát pozor ▸</h4>
        <div class="info-content collapsible-content" style="display:none">`;
            for (const m of ch.expected_misconceptions) {
                html += `<div style="margin-bottom:4px">⚡ ${UI.escapeHtml(m)}</div>`;
            }
            html += `</div></div>`;
        }

        return html;
    }

    // ── Toolbar update per type ────────────────────────────────

    function updateToolbar(ch) {
        const tc = Store.getTypeConfig(ch.type);
        const runBtn = document.getElementById('btn-run-challenge');
        if (runBtn) {
            runBtn.textContent = tc.runLabel;
            // Reset type class
            runBtn.className = 'btn-primary';
            if (ch.type !== 'implementation') runBtn.classList.add(tc.cls);
        }
        const typeIndicator = document.getElementById('challenge-type-indicator');
        if (typeIndicator) {
            typeIndicator.innerHTML = `<span class="tag ${tc.cls}">${tc.icon} ${tc.label}</span>`;
        }
    }

    // ── Run challenge ──────────────────────────────────────────

    async function run() {
        const st = Store.s;
        if (!st.currentChallenge || !st.editor) return;
        const { section_num, lesson_num, index } = st.currentChallenge;
        const ch = st.currentChallenge.data;
        const tc = Store.getTypeConfig(ch?.type);
        const content = st.editor.getValue();

        st.autosaveDirty = false;
        await Api.saveDraft(section_num, lesson_num, content);
        UI.appendOutput(`${tc.runLabel.replace(/^[^\s]+\s/, '▶ ')} výzva ${index}...\n`, '');

        const result = await Api.runChallenge(section_num, lesson_num, index);

        if (result.error && !result.messages) {
            UI.appendOutput(`❌ ${result.error}\n`, 'fail');
            return;
        }

        for (const msg of (result.messages || [])) {
            const cls = msg.includes('✓') || msg.includes('✅') ? 'pass' : 'fail';
            UI.appendOutput(`  ${msg}\n`, cls);
        }

        if (result.passed) {
            UI.appendOutput(`\n✅ ${tc.successMsg} +${result.points} bodů\n`, 'pass');
            renderPostSuccess(section_num, lesson_num, index, ch);
        } else {
            UI.appendOutput(`\n❌ ${tc.failMsg}\n`, 'fail');
            renderPostFailure(ch, result);
        }

        if (result.state_before !== result.state_after) {
            const icon = Store.STATE_ICONS[result.state_after] || '';
            UI.appendOutput(`${icon} Stav: ${result.state_before} → ${result.state_after}\n`, '');
        }

        if (result.feedback) {
            renderFeedback(result.feedback);
        }

        Lesson.loadCourseTree();
    }

    function renderPostSuccess(sectionNum, lessonNum, index, ch) {
        const lesson = Store.s.currentLesson?.data;
        if (!lesson) return;

        let html = '';
        // Offer to show reference solution for comparison
        html += `<div class="post-action-bar">
      <button class="btn-small" onclick="Challenge.revealReference()">📋 Zobrazit referenční řešení</button>
      <button class="btn-small" onclick="Challenge.compareWithReference()">⚖️ Porovnat s referencí</button>`;

        const nextCh = lesson.challenges.find(c => c.index === index + 1);
        if (nextCh) {
            html += `<button class="btn-primary" onclick="Challenge.open('${sectionNum}','${lessonNum}',${index + 1})" style="margin-left:auto">
        ▶ Další: ${UI.escapeHtml(nextCh.title)}
      </button>`;
        } else {
            const allPassed = lesson.challenges.every(c =>
                c.index === index ? true : ['currently_passing', 'mastered'].includes(c.state)
            );
            if (allPassed) {
                html += `<button class="btn-primary" onclick="Lesson.open('${sectionNum}','${lessonNum}')" style="margin-left:auto">
          🎉 Lekce dokončena — zpět na přehled
        </button>`;
            }
        }
        html += '</div>';
        UI.appendOutputHtml(html);

        // Show solution explanation if available
        if (ch?.solution_explanation) {
            UI.appendOutputHtml(`<div class="feedback-panel" style="border-left-color:var(--green);margin-top:8px">
        <div class="feedback-title" style="color:var(--green)">💡 Vysvětlení řešení</div>
        <div class="feedback-guidance">${UI.renderMarkdown(ch.solution_explanation)}</div>
      </div>`);
        }

        // Fetch and show reflection prompts
        fetchReflection(sectionNum, lessonNum, index, true);
    }

    function renderPostFailure(ch, result) {
        // Type-specific failure guidance
        const tc = Store.getTypeConfig(ch?.type);
        let html = '<div class="post-action-bar">';

        if (ch?.type === 'debugging') {
            html += `<button class="btn-small" onclick="Challenge.showThinkingNotes()">🧠 Jak hledat chybu</button>`;
        } else if (ch?.type === 'trace') {
            html += `<button class="btn-small" onclick="Challenge.showThinkingNotes()">🧠 Jak trasovat kód</button>`;
        }

        // Always offer hints if available and not all revealed
        if (ch?.hints && ch.hints.length > 0) {
            const unrevealed = ch.hints.length - Store.s.hintsRevealed.size;
            if (unrevealed > 0) {
                html += `<button class="btn-small" onclick="Challenge.revealNextHint()">💡 Další nápověda (${unrevealed} zbývá)</button>`;
            }
        }

        // Common mistakes
        if (ch?.common_mistakes && ch.common_mistakes.length > 0) {
            html += `<button class="btn-small" onclick="Challenge.showCommonMistakes()">⚠️ Časté chyby</button>`;
        }

        html += '</div>';
        UI.appendOutputHtml(html);
    }

    function renderFeedback(fb) {
        let html = `<div class="feedback-panel">`;
        html += `<div class="feedback-title">${UI.escapeHtml(fb.title || 'Zpětná vazba')}</div>`;
        if (fb.explanation) html += `<div class="feedback-guidance">${UI.escapeHtml(fb.explanation)}</div>`;
        if (fb.guidance && fb.guidance.length > 0) {
            html += `<div class="feedback-guidance" style="margin-top:6px">`;
            for (const g of fb.guidance) html += `• ${UI.escapeHtml(g)}<br>`;
            html += `</div>`;
        }
        if (fb.hint) html += `<div style="margin-top:6px;color:var(--yellow)">💡 ${UI.escapeHtml(fb.hint)}</div>`;
        if (fb.encouragement) html += `<div style="margin-top:4px">${UI.escapeHtml(fb.encouragement)}</div>`;
        html += `</div>`;
        UI.appendOutputHtml(html);
    }

    // ── Reference / Compare ────────────────────────────────────

    async function revealReference() {
        const st = Store.s;
        if (!st.currentChallenge) return;
        const { section_num, lesson_num, index } = st.currentChallenge;
        const result = await Api.getReference(section_num, lesson_num, index);
        if (result.error) {
            UI.appendOutput(`ℹ️ ${result.error}\n`, '');
            return;
        }

        let html = '<div class="feedback-panel reference-panel">';
        html += '<div class="feedback-title" style="color:var(--purple)">📋 Referenční řešení</div>';
        html += `<pre class="ref-code">${UI.escapeHtml(result.reference_solution)}</pre>`;
        if (result.solution_explanation) {
            html += `<div class="ref-explanation">${UI.renderMarkdown(result.solution_explanation)}</div>`;
        }
        html += '</div>';
        UI.appendOutputHtml(html);
    }

    async function compareWithReference() {
        const st = Store.s;
        if (!st.currentChallenge || !st.editor) return;
        const { section_num, lesson_num, index } = st.currentChallenge;
        const result = await Api.getReference(section_num, lesson_num, index);
        if (result.error) {
            UI.appendOutput(`ℹ️ ${result.error}\n`, '');
            return;
        }
        const modal = document.getElementById('compare-modal');
        const container = document.getElementById('compare-container');
        container.innerHTML = '';

        // Add solution explanation above the diff
        let headerHtml = '';
        if (result.solution_explanation) {
            headerHtml = `<div class="compare-explanation">${UI.renderMarkdown(result.solution_explanation)}</div>`;
        }
        const headerDiv = document.createElement('div');
        headerDiv.innerHTML = headerHtml;
        container.appendChild(headerDiv);

        const mergeDiv = document.createElement('div');
        container.appendChild(mergeDiv);

        CodeMirror.MergeView(mergeDiv, {
            value: st.editor.getValue(),
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

    // ── Thinking notes / common mistakes in output ─────────────

    function showThinkingNotes() {
        const ch = Store.s.currentChallenge?.data;
        if (!ch?.thinking_notes) return;
        UI.appendOutputHtml(`<div class="feedback-panel thinking-panel-output">
      <div class="feedback-title" style="color:var(--purple)">🧠 Jak nad tím přemýšlet</div>
      <div class="feedback-guidance">${UI.renderMarkdown(ch.thinking_notes)}</div>
    </div>`);
    }

    function showCommonMistakes() {
        const ch = Store.s.currentChallenge?.data;
        if (!ch?.common_mistakes || ch.common_mistakes.length === 0) return;
        let html = '<div class="feedback-panel" style="border-left-color:var(--orange)"><div class="feedback-title" style="color:var(--orange)">⚠️ Časté chyby</div>';
        for (const m of ch.common_mistakes) html += `<div style="margin-bottom:4px">• ${UI.escapeHtml(m)}</div>`;
        html += '</div>';
        UI.appendOutputHtml(html);
    }

    function revealNextHint() {
        const ch = Store.s.currentChallenge?.data;
        if (!ch?.hints) return;
        for (let i = 0; i < ch.hints.length; i++) {
            if (!Store.s.hintsRevealed.has(i)) {
                Store.s.hintsRevealed.add(i);
                UI.appendOutputHtml(`<div class="feedback-panel" style="border-left-color:var(--yellow)">
          <div class="feedback-title" style="color:var(--yellow)">💡 Nápověda ${i + 1}</div>
          <div class="feedback-guidance">${UI.escapeHtml(ch.hints[i])}</div>
        </div>`);
                // Also reveal in sidebar
                const items = document.querySelectorAll('.hint-item');
                if (items[i]) { items[i].textContent = ch.hints[i]; items[i].classList.add('revealed'); }
                return;
            }
        }
        UI.toast('Všechny nápovědy už zobrazeny', 'info');
    }

    // ── Helpers ────────────────────────────────────────────────

    function revealHint(el, index) {
        if (Store.s.hintsRevealed.has(index)) return;
        Store.s.hintsRevealed.add(index);
        el.textContent = el.dataset.hint;
        el.classList.add('revealed');
    }

    function toggleCollapsible(h4El) {
        const content = h4El.nextElementSibling;
        const isHidden = content.style.display === 'none';
        content.style.display = isHidden ? 'block' : 'none';
        h4El.textContent = h4El.textContent.replace(isHidden ? '▸' : '▾', isHidden ? '▾' : '▸');
    }

    function updateNavButtons(challenges, currentIndex) {
        const prevBtn = document.getElementById('btn-prev-challenge');
        const nextBtn = document.getElementById('btn-next-challenge');
        if (prevBtn) prevBtn.disabled = currentIndex <= 1;
        if (nextBtn) nextBtn.disabled = currentIndex >= challenges.length;
    }

    function navigate(direction) {
        const st = Store.s;
        if (!st.currentChallenge) return;
        const { section_num, lesson_num, index } = st.currentChallenge;
        const newIndex = index + direction;
        if (newIndex < 1) return;
        if (st.currentLesson?.data?.challenges) {
            const ch = st.currentLesson.data.challenges.find(c => c.index === newIndex);
            if (!ch) return;
        }
        open(section_num, lesson_num, newIndex);
    }

    async function fetchReflection(sectionNum, lessonNum, index, passed) {
        const data = await Api.getReflection({
            context: 'challenge',
            section_num: sectionNum,
            lesson_num: lessonNum,
            challenge_index: index,
            passed,
        });
        if (!data || data.error || !data.prompts || data.prompts.length === 0) return;
        let html = '<div class="reflection-panel"><h4>🪞 Reflexe</h4>';
        for (const p of data.prompts) {
            html += `<div class="reflection-prompt">${UI.escapeHtml(p.question || p.prompt || '')}</div>`;
        }
        html += '</div>';
        UI.appendOutputHtml(html);
    }

    return {
        open, openFromRec, run,
        revealReference, compareWithReference, closeCompareModal,
        showThinkingNotes, showCommonMistakes, revealNextHint,
        revealHint, toggleCollapsible, navigate, fetchReflection,
    };
})();
