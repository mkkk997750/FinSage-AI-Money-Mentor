// All API calls use Vite's proxy (/api → http://localhost:8000)
// No need for VITE_API_URL when using proxy

const api = async (path, options = {}) => {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

// ── Users ─────────────────────────────────────────────────────────────────────
export const getUsers = () => api('/api/users-summary')

// ── Dashboard ─────────────────────────────────────────────────────────────────
export const getDashboard = (userId) => api(`/api/data/dashboard/${userId}`)

// ── Data Tables ───────────────────────────────────────────────────────────────
export const getTableData = (tableName, userId, limit = 50) => {
  const base = `/api/data/${tableName}${userId ? `?user_id=${userId}&limit=${limit}` : `?limit=${limit}`}`
  return api(base)
}

// ── Agents ────────────────────────────────────────────────────────────────────
export const runHealthScore  = (body) => api('/api/agents/health-score',   { method: 'POST', body: JSON.stringify(body) })
export const runFirePlanner  = (body) => api('/api/agents/fire-planner',   { method: 'POST', body: JSON.stringify(body) })
export const runTaxWizard    = (body) => api('/api/agents/tax-wizard',     { method: 'POST', body: JSON.stringify(body) })
export const runInsurance    = (body) => api('/api/agents/insurance-audit',{ method: 'POST', body: JSON.stringify(body) })
export const runLifeEvent    = (body) => api('/api/agents/life-event',     { method: 'POST', body: JSON.stringify(body) })
export const runCouplePlanner= (body) => api('/api/agents/couple-planner', { method: 'POST', body: JSON.stringify(body) })
export const runMfXray       = (body) => api('/api/agents/mf-xray',        { method: 'POST', body: JSON.stringify(body) })
export const runFullAnalysis = (body) => api('/api/agents/full-analysis',  { method: 'POST', body: JSON.stringify(body) })
export const getSessionHistory = (sessionId) => api(`/api/agents/sessions/${sessionId}/history`)

// ── Agent map ─────────────────────────────────────────────────────────────────
export const AGENT_MAP = {
  health_score:   { label: 'Health Score',    icon: '🏥', fn: runHealthScore,   color: '#10b981' },
  fire_planner:   { label: 'FIRE Planner',    icon: '🔥', fn: runFirePlanner,   color: '#f59e0b' },
  tax_wizard:     { label: 'Tax Wizard',       icon: '🧾', fn: runTaxWizard,     color: '#6366f1' },
  insurance:      { label: 'Insurance Audit',  icon: '🛡️', fn: runInsurance,     color: '#ec4899' },
  life_event:     { label: 'Life Event',       icon: '🎯', fn: runLifeEvent,     color: '#8b5cf6' },
  couple_planner: { label: 'Couple Planner',   icon: '💑', fn: runCouplePlanner, color: '#06b6d4' },
  mf_xray:        { label: 'MF X-Ray',         icon: '🔬', fn: runMfXray,        color: '#4f8ef7' },
  full_analysis:  { label: 'Full Analysis',    icon: '📋', fn: runFullAnalysis,  color: '#f97316' },
}
