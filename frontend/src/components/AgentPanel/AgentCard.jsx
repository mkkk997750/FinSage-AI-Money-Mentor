import { useState } from 'react'
import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { useApp } from '../../context/AppContext'
import { AGENT_MAP } from '../../api/client'
import './AgentCard.css'

export default function AgentCard({ agentKey, isSelected, onClick }) {
  const cfg = AGENT_MAP[agentKey]
  if (!cfg) return null
  return (
    <button
      className={`agent-card ${isSelected ? 'agent-card--selected' : ''}`}
      style={isSelected ? { borderColor: cfg.color, boxShadow: `0 0 0 2px ${cfg.color}30` } : {}}
      onClick={onClick}
    >
      <span
        className="agent-card-icon"
        style={{ background: `${cfg.color}18`, color: cfg.color }}
      >
        {cfg.icon}
      </span>
      <span className="agent-card-label">{cfg.label}</span>
    </button>
  )
}

export function AgentResult({ result, agentKey }) {
  const [tab, setTab] = useState('report')
  if (!result) return null

  const reportText = extractReport(result, agentKey)
  const rawJson    = JSON.stringify(result, null, 2)

  return (
    <div className="agent-result">
      <div className="result-header">
        <div className="result-title">
          {AGENT_MAP[agentKey]?.icon} Analysis Complete
        </div>
        {result.session_id && (
          <span className="result-session">Session: {result.session_id}</span>
        )}
      </div>

      <div className="tabs">
        <button className={`tab-btn ${tab === 'report' ? 'active' : ''}`} onClick={() => setTab('report')}>📄 Report</button>
        <button className={`tab-btn ${tab === 'raw'    ? 'active' : ''}`} onClick={() => setTab('raw')}>🔧 Raw JSON</button>
      </div>

      {tab === 'report' && (
        <div className="md-output" style={{ background: 'var(--bg2)', borderRadius: 10, padding: '16px 20px' }}>
          {reportText
            ? <Markdown remarkPlugins={[remarkGfm]}>{reportText}</Markdown>
            : <p style={{ color: 'var(--text3)' }}>No report text found. Check Raw JSON tab.</p>
          }
        </div>
      )}
      {tab === 'raw' && (
        <div className="code-block">{rawJson}</div>
      )}
    </div>
  )
}

function extractReport(result, agentKey) {
  const fields = {
    health_score:   'health_score_report',
    fire_planner:   'fire_plan_report',
    tax_wizard:     'tax_report',
    insurance:      'insurance_report',
    life_event:     'life_event_result',
    couple_planner: 'couple_plan_result',
    mf_xray:        'mf_xray_result',
    full_analysis:  'final_report',
  }
  const key = fields[agentKey]
  
  if (key && result.result && typeof result.result === 'object' && result.result[key]) return result.result[key]
  if (key && result[key]) return result[key]
  
  if (agentKey === 'full_analysis' && result.messages) {
    const reportMsg = result.messages.slice().reverse().find(m => m.node === 'report_generator' || (m.content && m.content.includes('# 📊 FinSage')))
    if (reportMsg) return reportMsg.content
  }

  // fallback: messages
  if (result.messages?.length) {
    const last = result.messages[result.messages.length - 1]
    return last?.content || null
  }
  return null
}
