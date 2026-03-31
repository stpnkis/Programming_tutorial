/**
 * ProgTrain — API client module.
 * All fetch calls to the Flask backend go through here.
 */
const Api = (() => {

    async function request(path, options = {}) {
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

    function post(path, data) {
        return request(path, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
    }

    function put(path, data) {
        return request(path, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
    }

    // ── Content
    const getSections = () => request('/api/sections');
    const getLessonDetail = (s, l) => request(`/api/lessons/${s}/${l}`);
    const search = (q) => request(`/api/search?q=${encodeURIComponent(q)}`);

    // ── Progress
    const getSnapshot = () => request('/api/progress/snapshot');
    const getChallengeProgress = (id) => request(`/api/progress/${id}`);

    // ── Recommendations
    const getRecommendations = (limit = 10) => request(`/api/recommendations?limit=${limit}`);
    const getCategorizedRecs = () => request('/api/recommendations/categorized');

    // ── Execution
    const runChallenge = (s, l, idx) => post(`/api/challenges/${s}/${l}/${idx}/run`, {});
    const executeCode = (code, t = 10) => post('/api/execute', { code, timeout: t });

    // ── Workspace
    const getWorkspaceInfo = (s, l) => request(`/api/workspace/${s}/${l}`);
    const getDraft = (s, l) => request(`/api/workspace/${s}/${l}/draft`);
    const saveDraft = (s, l, c) => put(`/api/workspace/${s}/${l}/draft`, { content: c });
    const getStarter = (s, l) => request(`/api/workspace/${s}/${l}/starter`);
    const resetToStarter = (s, l) => post(`/api/workspace/${s}/${l}/reset`, {});
    const getReference = (s, l, idx) => request(`/api/workspace/${s}/${l}/reference/${idx}`);

    // ── REPL
    const replExecute = (code, t = 10) => post('/api/repl/execute', { code, timeout: t });
    const replReset = () => post('/api/repl/reset', {});
    const replStatus = () => request('/api/repl/status');

    // ── Terminal
    const termWrite = (data) => post('/api/terminal/write', { data });
    const termRead = () => request('/api/terminal/read');
    const termResize = (cols, rows) => post('/api/terminal/resize', { cols, rows });
    const termReset = () => post('/api/terminal/reset', {});
    const termStatus = () => request('/api/terminal/status');

    // ── Concepts & Adaptive
    const getConceptMastery = () => request('/api/concepts/mastery');
    const getAdaptiveRecs = (mode = 'guided', limit = 10) =>
        request(`/api/adaptive/recommendations?mode=${mode}&limit=${limit}`);
    const getStudyPlan = (mode = 'guided', minutes = 30) =>
        request(`/api/adaptive/study-plan?mode=${mode}&minutes=${minutes}`);

    // ── Projects
    const getProjects = () => request('/api/projects');

    // ── Reflection
    const getReflection = (ctx) => post('/api/reflection', ctx);

    return {
        request, post, put,
        getSections, getLessonDetail, search,
        getSnapshot, getChallengeProgress,
        getRecommendations, getCategorizedRecs,
        runChallenge, executeCode,
        getWorkspaceInfo, getDraft, saveDraft, getStarter, resetToStarter, getReference,
        replExecute, replReset, replStatus,
        termWrite, termRead, termResize, termReset, termStatus,
        getConceptMastery, getAdaptiveRecs, getStudyPlan,
        getProjects, getReflection,
    };
})();
