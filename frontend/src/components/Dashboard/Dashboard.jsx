import { useState, useEffect } from 'react'
import { Doughnut, Radar, Bar } from 'react-chartjs-2'
import { useApp } from '../../context/AppContext'
import { getDashboard } from '../../api/client'
import { formatINR, gradeColor, statusPill, fmtDate, fmtPct } from '../../utils/format'
import './Dashboard.css'

const CHART_OPTS = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { labels: { color: '#94a3b8', font: { size: 11 } } } },
}

export default function Dashboard({ onNavigate }) {
  const { activeUserId } = useApp()
  const [data, setData]     = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]   = useState(null)

  useEffect(() => {
    if (!activeUserId) return
    setLoading(true)
    setError(null)
    getDashboard(activeUserId)
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [activeUserId])

  if (!activeUserId) return <EmptySelect />
  if (loading) return <div className="spinner-wrap"><div className="spinner" /></div>
  if (error)   return <div className="empty-state"><div className="icon">⚠️</div><p>{error}</p></div>
  if (!data)   return null

  const { user, profile, health_score, goals = [], mf_holdings = [], insurance = [], life_events = [] } = data

  // ── Chart datasets ─────────────────────────────────────────────────────────
  const assetData = buildAssetChart(mf_holdings, profile)
  const radarData = buildRadarChart(health_score)
  const goalChart  = buildGoalChart(goals)

  const totalMF  = mf_holdings.reduce((s, h) => s + parseFloat(h.current_value || 0), 0)
  const totalGoalTarget = goals.reduce((s, g) => s + parseFloat(g.target_amount || 0), 0)
  const goalsOnTrack    = goals.filter((g) => g.status === 'on_track').length

  return (
    <div className="dashboard">
      {/* ── User Header ── */}
      <div className="dash-user-card card">
        <div className="duc-left">
          <div className="duc-avatar">{user?.name?.[0] || '?'}</div>
          <div>
            <h2 className="duc-name">{user?.name}</h2>
            <p className="duc-sub">{profile?.occupation} · {profile?.city} · Age {profile?.age}</p>
          </div>
        </div>
        <div className="duc-stats">
          <Stat label="Monthly Income"  value={formatINR(profile?.monthly_income)} />
          <Stat label="Monthly Savings" value={formatINR(profile?.monthly_savings)} />
          <Stat label="Net Worth"       value={formatINR(profile?.net_worth)} />
          <Stat label="Risk Profile"    value={profile?.risk_profile} highlight />
        </div>
        {health_score && (
          <div
            className="duc-grade"
            style={{ borderColor: gradeColor(health_score.grade) }}
          >
            <div className="duc-grade-score" style={{ color: gradeColor(health_score.grade) }}>
              {Math.round(health_score.overall_score)}
            </div>
            <div className="duc-grade-label">/ 100</div>
            <div className="duc-grade-letter" style={{ color: gradeColor(health_score.grade) }}>
              Grade {health_score.grade}
            </div>
          </div>
        )}
      </div>

      {/* ── KPI Row ── */}
      <div className="kpi-row">
        <KpiCard icon="📈" label="MF Portfolio"    value={formatINR(totalMF)}             color="var(--accent)" />
        <KpiCard icon="🎯" label="Goals On Track"  value={`${goalsOnTrack} / ${goals.length}`} color="var(--green)" />
        <KpiCard icon="🛡️" label="Active Policies" value={insurance.filter(i => i.policy_status === 'active').length} color="var(--pink)" />
        <KpiCard icon="⚡" label="Total Goal Target" value={formatINR(totalGoalTarget)}   color="var(--yellow)" />
      </div>

      {/* ── Charts Row ── */}
      <div className="charts-row">
        <div className="chart-card card">
          <div className="section-title">Asset Allocation</div>
          <div className="chart-wrap" style={{ height: 220 }}>
            <Doughnut data={assetData} options={{ ...CHART_OPTS, cutout: '65%' }} />
          </div>
        </div>

        <div className="chart-card card">
          <div className="section-title">Financial Health Radar</div>
          <div className="chart-wrap" style={{ height: 220 }}>
            {radarData
              ? <Radar data={radarData} options={{ ...CHART_OPTS, scales: { r: { grid: { color: '#1e2f5a' }, ticks: { color: '#64748b', font: { size: 9 } }, pointLabels: { color: '#94a3b8', font: { size: 10 } }, min: 0, max: 100 } } }} />
              : <div className="empty-state" style={{ padding: 20 }}><p>No health data</p></div>
            }
          </div>
        </div>

        <div className="chart-card card" style={{ flex: 1.5 }}>
          <div className="section-title">Goals Progress (₹L)</div>
          <div className="chart-wrap" style={{ height: 220 }}>
            {goals.length > 0
              ? <Bar data={goalChart} options={{ ...CHART_OPTS, indexAxis: 'y', scales: { x: { grid: { color: '#1e2f5a' }, ticks: { color: '#64748b', font: { size: 10 } } }, y: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 10 } } } } }} />
              : <div className="empty-state" style={{ padding: 20 }}><p>No goals data</p></div>
            }
          </div>
        </div>
      </div>

      {/* ── MF Holdings Table ── */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="section-title">Mutual Fund Holdings ({mf_holdings.length})</div>
        {mf_holdings.length > 0 ? (
          <div className="data-table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Fund Name</th><th>Category</th><th>Units</th>
                  <th>Avg NAV</th><th>Current Value</th><th>P&L</th><th>XIRR%</th>
                </tr>
              </thead>
              <tbody>
                {mf_holdings.map((h, i) => {
                  const pl = parseFloat(h.current_value) - parseFloat(h.invested_amount)
                  return (
                    <tr key={i}>
                      <td style={{ fontWeight: 500 }}>{h.fund_name}</td>
                      <td><span className="pill pill-indigo" style={{ fontSize: '0.68rem' }}>{h.fund_category}</span></td>
                      <td>{parseFloat(h.units_held).toFixed(2)}</td>
                      <td>₹{parseFloat(h.avg_nav).toFixed(2)}</td>
                      <td>{formatINR(h.current_value)}</td>
                      <td style={{ color: pl >= 0 ? 'var(--green)' : 'var(--red)' }}>
                        {pl >= 0 ? '+' : ''}{formatINR(pl)}
                      </td>
                      <td style={{ color: parseFloat(h.xirr_pct) >= 12 ? 'var(--green)' : 'var(--yellow)' }}>
                        {fmtPct(h.xirr_pct)}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        ) : <p style={{ color: 'var(--text3)', fontSize: '0.85rem' }}>No MF holdings found.</p>}
      </div>

      {/* ── Goals Table ── */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="section-title">Financial Goals ({goals.length})</div>
        {goals.length > 0 ? (
          <div className="data-table-wrap">
            <table className="data-table">
              <thead>
                <tr><th>Goal</th><th>Category</th><th>Target</th><th>Saved</th><th>Progress</th><th>Target Date</th><th>Status</th></tr>
              </thead>
              <tbody>
                {goals.map((g, i) => {
                  const pct = Math.min(100, (parseFloat(g.current_savings) / parseFloat(g.target_amount)) * 100) || 0
                  return (
                    <tr key={i}>
                      <td style={{ fontWeight: 500 }}>{g.goal_name}</td>
                      <td>{g.goal_category}</td>
                      <td>{formatINR(g.target_amount)}</td>
                      <td>{formatINR(g.current_savings)}</td>
                      <td style={{ minWidth: 100 }}>
                        <div style={{ fontSize: '0.75rem', marginBottom: 2 }}>{pct.toFixed(0)}%</div>
                        <div className="progress-bar-wrap">
                          <div className="progress-bar" style={{ width: `${pct}%` }} />
                        </div>
                      </td>
                      <td>{fmtDate(g.target_date)}</td>
                      <td><span className={`pill ${statusPill(g.status)}`}>{g.status}</span></td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        ) : <p style={{ color: 'var(--text3)', fontSize: '0.85rem' }}>No goals found.</p>}
      </div>

      {/* ── Insurance + Events Row ── */}
      <div className="two-col-row">
        <div className="card">
          <div className="section-title">Insurance Policies ({insurance.length})</div>
          <div className="data-table-wrap">
            <table className="data-table">
              <thead>
                <tr><th>Type</th><th>Provider</th><th>Coverage</th><th>Premium</th><th>Status</th></tr>
              </thead>
              <tbody>
                {insurance.map((p, i) => (
                  <tr key={i}>
                    <td>{p.insurance_type}</td>
                    <td>{p.provider_name}</td>
                    <td>{formatINR(p.coverage_amount)}</td>
                    <td>{formatINR(p.annual_premium)}/yr</td>
                    <td><span className={`pill ${statusPill(p.policy_status)}`}>{p.policy_status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card">
          <div className="section-title">Life Events ({life_events.length})</div>
          <div className="data-table-wrap">
            <table className="data-table">
              <thead>
                <tr><th>Event</th><th>Amount</th><th>Date</th><th>Status</th></tr>
              </thead>
              <tbody>
                {life_events.map((e, i) => (
                  <tr key={i}>
                    <td>{e.event_type}</td>
                    <td>{formatINR(e.estimated_cost)}</td>
                    <td>{fmtDate(e.expected_date)}</td>
                    <td><span className={`pill ${statusPill(e.planning_status)}`}>{e.planning_status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* ── Agent CTA ── */}
      <div className="card dash-cta">
        <div className="cta-text">
          <div style={{ fontSize: '1.1rem', fontWeight: 700 }}>Run AI Analysis</div>
          <div style={{ color: 'var(--text2)', fontSize: '0.85rem', marginTop: 4 }}>
            Get personalized financial insights from our 11-node LangGraph multi-agent system
          </div>
        </div>
        <button className="btn btn-primary" onClick={() => onNavigate('agent', { agent: 'full_analysis' })}>
          🤖 Full AI Analysis
        </button>
      </div>
    </div>
  )
}

function EmptySelect() {
  return (
    <div className="empty-state">
      <div className="icon">👆</div>
      <p style={{ fontWeight: 600, fontSize: '1rem' }}>Select a user from the top bar</p>
      <p style={{ marginTop: 6 }}>to view their financial dashboard</p>
    </div>
  )
}

function KpiCard({ icon, label, value, color }) {
  return (
    <div className="kpi-card card">
      <div className="kpi-icon" style={{ background: `${color}18`, color }}>{icon}</div>
      <div className="kpi-value" style={{ color }}>{value ?? '—'}</div>
      <div className="kpi-label">{label}</div>
    </div>
  )
}

function Stat({ label, value, highlight }) {
  return (
    <div className="duc-stat">
      <div className="duc-stat-label">{label}</div>
      <div className="duc-stat-value" style={highlight ? { textTransform: 'capitalize', color: 'var(--yellow)' } : {}}>
        {value ?? '—'}
      </div>
    </div>
  )
}

// ── Chart builders ────────────────────────────────────────────────────────────
function buildAssetChart(holdings, profile) {
  const mfVal = holdings.reduce((s, h) => s + parseFloat(h.current_value || 0), 0)
  const vals  = [
    mfVal,
    parseFloat(profile?.stock_value || 0),
    parseFloat(profile?.real_estate_value || 0),
    parseFloat(profile?.gold_value || 0),
    parseFloat(profile?.pf_ppf_balance || 0),
    parseFloat(profile?.fd_balance || 0),
  ]
  return {
    labels: ['Mutual Funds', 'Stocks', 'Real Estate', 'Gold', 'PF/PPF', 'FD'],
    datasets: [{
      data: vals,
      backgroundColor: ['#4f8ef7','#7c3aed','#10b981','#fbbf24','#f59e0b','#06b6d4'],
      borderColor: '#131e3f',
      borderWidth: 2,
    }],
  }
}

function buildRadarChart(hs) {
  if (!hs) return null
  return {
    labels: ['Emergency', 'Insurance', 'Investments', 'Debt Ratio', 'Tax Efficiency', 'Retirement'],
    datasets: [{
      label: 'Health Score',
      data: [
        hs.emergency_fund_score,
        hs.insurance_coverage_score,
        hs.investment_diversity_score,
        hs.debt_management_score,
        hs.tax_efficiency_score,
        hs.retirement_readiness_score,
      ],
      backgroundColor: 'rgba(79,142,247,.12)',
      borderColor: '#4f8ef7',
      pointBackgroundColor: '#4f8ef7',
      borderWidth: 2,
    }],
  }
}

function buildGoalChart(goals) {
  const top = goals.slice(0, 7)
  return {
    labels: top.map((g) => g.goal_name.length > 14 ? g.goal_name.slice(0, 14) + '…' : g.goal_name),
    datasets: [
      {
        label: 'Saved (₹L)',
        data: top.map((g) => (parseFloat(g.current_savings || 0) / 1e5).toFixed(1)),
        backgroundColor: 'rgba(16,185,129,.75)',
        borderRadius: 4,
      },
      {
        label: 'Target (₹L)',
        data: top.map((g) => (parseFloat(g.target_amount || 0) / 1e5).toFixed(1)),
        backgroundColor: 'rgba(79,142,247,.25)',
        borderRadius: 4,
      },
    ],
  }
}
