import { useState } from 'react'
import { useApp } from '../../context/AppContext'
import { AGENT_MAP } from '../../api/client'
import AgentCard, { AgentResult } from './AgentCard'
import './AgentCard.css'
import './AgentPanel.css'

const EVENT_TYPES   = ['bonus', 'marriage', 'baby', 'inheritance', 'job_change']
const RISK_PROFILES = ['conservative', 'moderate', 'aggressive']

export default function AgentPanel({ activeAgent, setActiveAgent }) {
  const { activeUserId, sessionId } = useApp()

  const [loading, setLoading] = useState(false)
  const [result,  setResult]  = useState(null)
  const [error,   setError]   = useState(null)

  // ── Agent-specific config state ──
  const [eventType,     setEventType]     = useState('bonus')
  const [eventAmount,   setEventAmount]   = useState('')
  const [partnerId,     setPartnerId]     = useState('')
  const [riskOverride,  setRiskOverride]  = useState('')

  const handleRun = async () => {
    if (!activeUserId) { setError('Please select a user first.'); return }
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const cfg  = AGENT_MAP[activeAgent]
      const body = buildBody(activeAgent, activeUserId, sessionId, {
        eventType, eventAmount, partnerId, riskOverride,
      })
      const res  = await cfg.fn(body)
      setResult(res)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const cfg = AGENT_MAP[activeAgent]

  return (
    <div className="agent-panel">
      {/* ── Agent Grid ── */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="section-title">Select Agent</div>
        <div className="agent-grid">
          {Object.keys(AGENT_MAP).map((key) => (
            <AgentCard
              key={key}
              agentKey={key}
              isSelected={activeAgent === key}
              onClick={() => { setActiveAgent(key); setResult(null); setError(null) }}
            />
          ))}
        </div>
      </div>

      {/* ── Config + Run ── */}
      <div className="card agent-config-card">
        <div className="agent-config-header">
          <span className="agent-big-icon" style={{ background: `${cfg?.color}18`, color: cfg?.color }}>
            {cfg?.icon}
          </span>
          <div>
            <div className="agent-config-title">{cfg?.label}</div>
            <div className="agent-config-sub">{agentDescription(activeAgent)}</div>
          </div>
        </div>

        {/* Agent-specific inputs */}
        {activeAgent === 'life_event' && (
          <div className="config-fields">
            <div className="form-group">
              <label>Event Type</label>
              <select className="form-control" value={eventType} onChange={e => setEventType(e.target.value)}>
                {EVENT_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label>Event Amount (₹)</label>
              <input type="number" className="form-control" placeholder="e.g. 500000"
                value={eventAmount} onChange={e => setEventAmount(e.target.value)} />
            </div>
          </div>
        )}

        {activeAgent === 'couple_planner' && (
          <div className="config-fields">
            <div className="form-group">
              <label>Partner User ID</label>
              <input type="number" className="form-control" placeholder="Partner's user ID (1–25)"
                value={partnerId} onChange={e => setPartnerId(e.target.value)} />
            </div>
          </div>
        )}

        {(activeAgent === 'fire_planner' || activeAgent === 'full_analysis') && (
          <div className="config-fields">
            <div className="form-group">
              <label>Risk Profile Override (optional)</label>
              <select className="form-control" value={riskOverride} onChange={e => setRiskOverride(e.target.value)}>
                <option value="">— Use profile default —</option>
                {RISK_PROFILES.map(r => <option key={r} value={r}>{r}</option>)}
              </select>
            </div>
          </div>
        )}

        <button
          className="btn btn-primary"
          onClick={handleRun}
          disabled={loading}
          style={{ marginTop: 8, width: '100%', justifyContent: 'center', padding: '11px' }}
        >
          {loading ? (
            <><div className="btn-spinner" /> Running Analysis...</>
          ) : (
            <>{cfg?.icon} Run {cfg?.label}</>
          )}
        </button>

        {error && (
          <div className="agent-error">
            ⚠️ {error}
          </div>
        )}
      </div>

      {/* ── Result ── */}
      {result && (
        <AgentResult result={result} agentKey={activeAgent} />
      )}
    </div>
  )
}

// ── Body builders ─────────────────────────────────────────────────────────────
function buildBody(agentKey, userId, sessionId, extras) {
  const base = { user_id: userId, session_id: sessionId || `sess_${Date.now()}` }
  switch (agentKey) {
    case 'life_event':
      return {
        ...base,
        event_type: extras.eventType,
        event_amount: extras.eventAmount ? parseFloat(extras.eventAmount) : undefined,
      }
    case 'couple_planner':
      return { ...base, partner_user_id: extras.partnerId ? parseInt(extras.partnerId) : undefined }
    case 'fire_planner':
    case 'full_analysis':
      return {
        ...base,
        risk_override: extras.riskOverride || undefined,
      }
    default:
      return base
  }
}

function agentDescription(key) {
  const desc = {
    health_score:   'Compute a 100-point financial health score across 6 dimensions',
    fire_planner:   'Calculate FIRE corpus, SIP requirements, and retirement timeline',
    tax_wizard:     'Optimize tax liability across 80C, NPS, HRA, and LTCG',
    insurance:      'Audit insurance gaps and coverage adequacy',
    life_event:     'Plan finances around major life events (bonus, marriage, baby…)',
    couple_planner: 'Joint financial optimization for two partners',
    mf_xray:        'Deep MF portfolio analysis — XIRR, overlap, expense drag',
    full_analysis:  'Comprehensive report from all 11 LangGraph agents',
  }
  return desc[key] || ''
}
