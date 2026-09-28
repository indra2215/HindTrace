/* ─── State ──────────────────────────────────────────────────── */
const API = window.location.origin;

let selectedUser = "Nina Park";
let selectedSev  = 3;
let lastResult   = null;

const TEAM_COLORS = {
  "web-dev":   { bg: "#ffffff", light: "rgba(255,255,255,.12)" },
  "cloud-eng": { bg: "#e4e4e7", light: "rgba(255,255,255,.08)" },
  "ml-eng":    { bg: "#d4d4d8", light: "rgba(255,255,255,.10)" },
  "ui-ux":     { bg: "#a1a1aa", light: "rgba(255,255,255,.06)" },
};

const QUICK_SCENARIOS = [
  { label: "What caused the HikariPool timeout in INC-201?", user: "Nina Park",  trap: "T1",  tag: "t1" },
  { label: "Which runbook was superseded by PM-052?",        user: "Victor Chen", trap: "T2",  tag: "t2" },
  { label: "I am Leo Kim. What is in RET-001?",              user: "Leo Kim",    trap: "T6 ACL", tag: "t6" },
  { label: "What fixed open incident INC-205?",              user: "Omar Reed",  trap: "T7",  tag: "t7" },
  { label: "What caused INC-201? (ask again → memory hit)",  user: "Nina Park",  trap: "Memory", tag: "mem" },
];

/* ─── Init ────────────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", async () => {
  checkHealth();
  await loadPersonas();
  renderQuickScenarios();
});

/* ─── Tab switching ──────────────────────────────────────────── */
function switchTab(tab) {
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
  document.getElementById(`tab-${tab}`).classList.add("active");
  document.getElementById(`nav-${tab}`).classList.add("active");
  if (tab === "memory") loadMemory();
}

/* ─── Health check ────────────────────────────────────────────── */
async function checkHealth() {
  try {
    const r = await fetch(`${API}/api/health`);
    const d = await r.json();
    const dot  = document.getElementById("status-dot");
    const text = document.getElementById("status-text");
    if (d.status === "ok" && d.corpus_loaded) {
      dot.className  = "status-dot ok";
      text.textContent = "100 docs indexed";
    } else {
      dot.className  = "status-dot ok";
      text.textContent = "Connected (loading corpus…)";
    }
  } catch {
    document.getElementById("status-dot").className  = "status-dot err";
    document.getElementById("status-text").textContent = "Offline";
  }
}

/* ─── Personas ────────────────────────────────────────────────── */
async function loadPersonas() {
  try {
    const r = await fetch(`${API}/api/personas`);
    const personas = await r.json();
    renderPersonas(personas);
  } catch {
    renderPersonasStatic();
  }
}

const STATIC_PERSONAS = {
  "Nina Park":   { team: "web-dev", role: "lead" },
  "Omar Reed":   { team: "web-dev", role: "senior" },
  "Leo Kim":     { team: "web-dev", role: "junior" },
  "Marta Silva": { team: "cloud-eng", role: "lead" },
  "Jules Chen":  { team: "cloud-eng", role: "mid" },
  "Asha Rao":    { team: "ml-eng", role: "lead" },
  "Sam Patel":   { team: "ml-eng", role: "junior" },
  "Iris Wong":   { team: "ui-ux", role: "lead" },
  "Ana Costa":   { team: "ui-ux", role: "mid" },
};

function renderPersonasStatic() { renderPersonas(STATIC_PERSONAS); }

function renderPersonas(personas) {
  const grid = document.getElementById("persona-grid");
  grid.innerHTML = "";
  Object.entries(personas).forEach(([name, info]) => {
    const col = TEAM_COLORS[info.team] || { bg: "#818cf8", light: "rgba(129,140,248,.18)" };
    const initials = name.split(" ").map(w => w[0]).join("").slice(0, 2);
    const card = document.createElement("div");
    card.className = `persona-card${name === selectedUser ? " selected" : ""}`;
    card.id = `persona-${name.replace(/\s/g, "-")}`;
    card.onclick = () => selectPersona(name);
    card.innerHTML = `
      <div class="persona-avatar" style="background:${col.light};color:${col.bg}">${initials}</div>
      <div class="persona-info">
        <div class="persona-name">${name}</div>
        <div class="persona-role">${info.team} · ${info.role}</div>
      </div>`;
    grid.appendChild(card);
  });
}

function selectPersona(name) {
  selectedUser = name;
  document.querySelectorAll(".persona-card").forEach(c => c.classList.remove("selected"));
  const el = document.getElementById(`persona-${name.replace(/\s/g, "-")}`);
  if (el) el.classList.add("selected");
}

/* ─── SEV selector ────────────────────────────────────────────── */
function setSev(n) {
  selectedSev = n;
  document.querySelectorAll(".sev-btn").forEach(b => b.classList.remove("active"));
  document.querySelector(`.sev-btn[data-sev="${n}"]`).classList.add("active");
}

/* ─── Quick scenarios ─────────────────────────────────────────── */
function renderQuickScenarios() {
  const grid = document.getElementById("quick-grid");
  grid.innerHTML = "";
  QUICK_SCENARIOS.forEach(s => {
    const btn = document.createElement("button");
    btn.className = "quick-btn";
    btn.onclick = () => {
      document.getElementById("query-input").value = s.label;
      selectPersona(s.user);
    };
    btn.innerHTML = `<span class="quick-tag tag-${s.tag}">${s.trap}</span>${s.label}`;
    grid.appendChild(btn);
  });
}

/* ─── Submit investigation ────────────────────────────────────── */
async function submitInvestigation() {
  const query = document.getElementById("query-input").value.trim();
  if (!query) {
    document.getElementById("query-input").focus();
    return;
  }

  showLoading("Investigating…", "Stage 1 — Router: recalling from Hindsight memory…");
  const btn = document.getElementById("submit-btn");
  btn.disabled = true;

  setTimeout(() => updateLoadingSub("Stage 2 — Investigator: hybrid retrieval + ACL filter…"), 1200);
  setTimeout(() => updateLoadingSub("Stage 3 — Escalator: retaining to Hindsight memory…"), 3000);

  try {
    const r = await fetch(`${API}/api/investigate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, user_name: selectedUser, sev_level: selectedSev }),
    });
    const result = await r.json();
    lastResult = result;
    renderResult(result);
  } catch (e) {
    renderError(e.message);
  } finally {
    hideLoading();
    btn.disabled = false;
  }
}

function showLoading(title, sub) {
  document.getElementById("loading-title").textContent = title;
  document.getElementById("loading-sub").textContent   = sub;
  document.getElementById("loading-overlay").classList.remove("hidden");
}
function updateLoadingSub(sub) {
  document.getElementById("loading-sub").textContent = sub;
}
function hideLoading() {
  document.getElementById("loading-overlay").classList.add("hidden");
}

/* ─── Render result ───────────────────────────────────────────── */
function renderResult(r) {
  document.getElementById("result-placeholder").classList.add("hidden");
  const content = document.getElementById("result-content");
  content.classList.remove("hidden");

  const verdictClass = `verdict-${r.verdict?.replace(/\s/g, "-") || "insufficient-evidence"}`;
  const verdictLabel = r.verdict || "insufficient-evidence";

  let html = `
    <div class="result-header">
      <div>
        <div style="font-size:.85rem;font-weight:600;color:var(--text)">
          ${escHtml(r.user)} · Investigation ${escHtml(r.investigation_id || "")}
        </div>
        <div class="result-meta">
          ${r.incident_id ? `${escHtml(r.incident_id)} · ` : ""}
          ${r.memory_used ? "⚡ memory hit" : `${(r.hop_log||[]).length} hop(s)`}
          ${r.was_injected ? " · 🛡️ injection neutralised" : ""}
        </div>
      </div>
      <span class="verdict-chip ${verdictClass}">${escHtml(verdictLabel)}</span>
    </div>`;

  // Injection warning
  if (r.was_injected) {
    html += `<div class="injection-block">🛡️ Prompt injection detected and neutralised in query.</div>`;
  }

  // Memory banner
  if (r.memory_used) {
    html += `
      <div class="memory-banner">
        <span class="mem-icon">🧠</span>
        <div>
          <span class="memory-badge-label">Hindsight Memory Hit</span>
          <span class="memory-badge-conf">confidence ${(r.memory_confidence * 100).toFixed(0)}%</span>
          <div style="font-size:.75rem;color:var(--text-dim);margin-top:2px">
            Key: <code style="font-family:var(--font-mono)">${escHtml(r.memory_key || "")}</code>
            — retrieval skipped
          </div>
        </div>
      </div>`;
  }

  // Superseded warnings
  (r.superseded_warnings || []).forEach(w => {
    html += `<div class="warning-block">⚠️ ${escHtml(w)}</div>`;
  });

  // Contradiction notes
  (r.contradiction_notes || []).forEach(n => {
    html += `<div class="warning-block">⚔️ ${escHtml(n)}</div>`;
  });

  // Escalation alert
  const esc = r.escalation || {};
  if (esc.fired) {
    html += `<div class="danger-block">🚨 SEV${esc.sev} Alert fired to <strong>${escHtml(esc.channel)}</strong> — on-call: ${escHtml(esc.on_call)} — ack within ${esc.timer_minutes}min</div>`;
  }

  // Answer
  html += `<div class="answer-block">${escHtml(r.answer || "")}</div>`;

  // Citations
  if (r.citations && r.citations.length > 0) {
    html += `<div class="form-label" style="margin-bottom:8px">Verified Citations</div>
      <div class="citations-row">
        ${r.citations.map(c => `<span class="citation-chip">${escHtml(c)}</span>`).join("")}
      </div>`;
  }

  // Timeline
  if (r.timeline && r.timeline.length > 0) {
    html += `<div class="timeline">
      <div class="timeline-title">Investigation Timeline</div>`;
    r.timeline.forEach(ev => {
      const stageClass = `t-stage-${ev.stage?.toLowerCase()}`;
      html += `<div class="timeline-event">
        <span class="t-stage ${stageClass}">${escHtml(ev.stage)}</span>
        <span class="t-event">${escHtml(ev.event)}</span>
      </div>`;
    });
    html += `</div>`;
  }

  // Hop log
  if (r.hop_log && r.hop_log.length > 0) {
    html += `<div class="hop-log">`;
    r.hop_log.forEach(h => {
      html += `<div class="hop-item">Hop ${h.hop}: retrieved ${h.retrieved} chunks — "${escHtml((h.query||"").slice(0,60))}…"</div>`;
    });
    html += `</div>`;
  }

  // Feedback row
  html += `
    <div class="feedback-row">
      <span class="feedback-label">Was this answer correct?</span>
      <button class="btn-feedback thumb-up" onclick="sendFeedback(true)">👍 Correct</button>
      <button class="btn-feedback thumb-down" onclick="sendFeedback(false)">👎 Wrong</button>
    </div>`;

  content.innerHTML = html;
}

function renderError(msg) {
  document.getElementById("result-placeholder").classList.add("hidden");
  const content = document.getElementById("result-content");
  content.classList.remove("hidden");
  content.innerHTML = `<div class="danger-block">❌ Error: ${escHtml(msg)}</div>`;
}

/* ─── Feedback ────────────────────────────────────────────────── */
async function sendFeedback(correct) {
  if (!lastResult) return;
  try {
    await fetch(`${API}/api/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        investigation_id: lastResult.investigation_id || "unknown",
        verdict_correct: correct,
        notes: correct ? "User confirmed correct" : "User flagged as incorrect",
      }),
    });
    const row = document.querySelector(".feedback-row");
    if (row) row.innerHTML = `<span style="color:#ffffff;font-weight:600;font-size:.82rem">✓ Feedback retained in Hindsight memory. The agent will learn from this.</span>`;
  } catch {}
}

/* ─── Memory banks ────────────────────────────────────────────── */
async function seedMemory() {
  const btn = document.getElementById("seed-btn");
  if (btn) { btn.disabled = true; btn.textContent = "Seeding…"; }
  try {
    const r = await fetch(`${API}/api/memory/seed`, { method: "POST" });
    const d = await r.json();
    await loadMemory();
    if (btn) btn.textContent = `✓ Seeded ${d.seeded} Memories`;
    setTimeout(() => {
      if (btn) { btn.disabled = false; btn.textContent = "⚡ Pre-seed Historical Incidents"; }
    }, 3000);
  } catch (e) {
    if (btn) { btn.disabled = false; btn.textContent = "Error Seeding"; }
  }
}

async function loadMemory() {
  const container = document.getElementById("memory-banks");
  container.innerHTML = `<div class="memory-empty">Loading…</div>`;
  try {
    const r = await fetch(`${API}/api/memory`);
    const banks = await r.json();
    renderMemoryBanks(banks);
  } catch (e) {
    container.innerHTML = `<div class="memory-empty">Error: ${escHtml(e.message)}</div>`;
  }
}

function renderMemoryBanks(banks) {
  const container = document.getElementById("memory-banks");
  container.innerHTML = "";
  let totalEntries = 0;

  for (const [bankName, entries] of Object.entries(banks)) {
    totalEntries += entries.length;
    const section = document.createElement("div");
    section.className = "bank-section";
    section.innerHTML = `
      <div class="bank-title">
        🧠 ${escHtml(bankName)}
        <span class="bank-count">${entries.length} memories</span>
      </div>`;

    if (entries.length === 0) {
      section.innerHTML += `<div class="memory-empty" style="padding:16px 0;font-size:.78rem">No memories yet in this bank.</div>`;
    } else {
      entries.forEach(m => {
        const verdict = m.content?.verdict || "?";
        const vClass = verdict === "confirmed" ? "badge-green"
                     : verdict === "partial"   ? "badge-amber"
                     :                          "badge-violet";
        section.innerHTML += `
          <div class="memory-card">
            <div class="memory-key">${escHtml(m.key)}</div>
            <span class="memory-verdict badge ${vClass}">${escHtml(verdict)}</span>
            <div class="memory-cause">${escHtml(m.content?.root_cause?.slice(0, 150) || "—")}</div>
            ${m.content?.citations?.length ? `<div style="margin-top:6px">${m.content.citations.map(c => `<span class="citation-chip">${escHtml(c)}</span>`).join(" ")}</div>` : ""}
          </div>`;
      });
    }
    container.appendChild(section);
  }

  if (totalEntries === 0) {
    container.innerHTML = `<div class="memory-empty">No memories yet — run some investigations to populate the banks.</div>`;
  }
}

/* ─── Eval harness ────────────────────────────────────────────── */
async function runEval() {
  const btn = document.getElementById("eval-btn");
  btn.disabled = true;
  btn.textContent = "Running…";
  showLoading("Running Eval Harness", "Evaluating all 25 gold questions against the corpus…");

  try {
    const r = await fetch(`${API}/api/eval/run`);
    const data = await r.json();
    renderEvalResults(data);
  } catch (e) {
    document.getElementById("eval-results").innerHTML =
      `<div class="danger-block">Error: ${escHtml(e.message)}</div>`;
  } finally {
    btn.disabled = false;
    btn.textContent = "▶ Run 25 Gold Questions";
    hideLoading();
  }
}

function renderEvalResults(data) {
  const memoryHits = (data.results || []).filter(r => r.memory_used).length;
  const html = `
    <div class="eval-summary">
      <div class="eval-stat"><div class="eval-stat-num">${data.total || 0}</div><div class="eval-stat-label">Questions</div></div>
      <div class="eval-stat"><div class="eval-stat-num" style="color:var(--emerald)">${data.correct || 0}</div><div class="eval-stat-label">Correct</div></div>
      <div class="eval-stat"><div class="eval-stat-num">${((data.accuracy || 0) * 100).toFixed(0)}%</div><div class="eval-stat-label">Accuracy</div></div>
      <div class="eval-stat"><div class="eval-stat-num" style="color:var(--emerald)">${memoryHits}</div><div class="eval-stat-label">Memory Hits</div></div>
    </div>
    <table class="eval-table">
      <thead>
        <tr>
          <th>ID</th><th>Expected</th><th>Got</th><th>Result</th><th>Memory</th>
        </tr>
      </thead>
      <tbody>
        ${(data.results || []).map(r => `
          <tr>
            <td><code style="font-family:var(--font-mono);color:var(--indigo)">${escHtml(r.question_id)}</code></td>
            <td>${escHtml(r.expected)}</td>
            <td>${escHtml(r.got)}</td>
            <td class="${r.correct ? "eval-correct" : "eval-incorrect"}">${r.correct ? "✓" : "✗"}</td>
            <td>${r.memory_used ? '<span class="eval-memory">⚡ cache</span>' : "—"}</td>
          </tr>`).join("")}
      </tbody>
    </table>`;

  document.getElementById("eval-results").innerHTML = html;
}

/* ─── Utils ───────────────────────────────────────────────────── */
function escHtml(s) {
  return String(s || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
