import { useState, useEffect } from 'react'
import { useApp } from '../../context/AppContext'
import { getTableData } from '../../api/client'
import { formatINR, fmtDate, statusPill, fmtPct } from '../../utils/format'
import './DataTables.css'

const TABLES = [
  { key: 'users',              label: 'Users',         icon: '👤' },
  { key: 'financial-profiles', label: 'Profiles',      icon: '📂' },
  { key: 'financial-goals',    label: 'Goals',         icon: '🎯' },
  { key: 'mutual-funds',       label: 'MF Holdings',   icon: '📈' },
  { key: 'tax-profiles',       label: 'Tax Profiles',  icon: '🧾' },
  { key: 'life-events',        label: 'Life Events',   icon: '🔔' },
  { key: 'insurance',          label: 'Insurance',     icon: '🛡️' },
  { key: 'health-scores',      label: 'Health Scores', icon: '💯' },
]

export default function DataTables({ activeTable, setActiveTable }) {
  const { activeUserId } = useApp()
  const [rows,    setRows]    = useState([])
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)
  const [filterUser, setFilterUser] = useState(true)

  useEffect(() => {
    const uid = filterUser ? activeUserId : null
    setLoading(true)
    setError(null)
    getTableData(activeTable, uid)
      .then(setRows)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [activeTable, activeUserId, filterUser])

  const cols = getColumns(activeTable)

  return (
    <div className="data-tables">
      {/* Table selector */}
      <div className="card table-selector">
        {TABLES.map((t) => (
          <button
            key={t.key}
            className={`table-tab ${activeTable === t.key ? 'table-tab--active' : ''}`}
            onClick={() => { setActiveTable(t.key); setRows([]) }}
          >
            <span>{t.icon}</span> {t.label}
          </button>
        ))}
      </div>

      {/* Controls */}
      <div className="card table-controls">
        <div>
          <strong style={{ fontSize: '1rem' }}>
            {TABLES.find(t => t.key === activeTable)?.icon}{' '}
            {TABLES.find(t => t.key === activeTable)?.label}
          </strong>
          {!loading && <span className="row-count"> — {rows.length} rows</span>}
        </div>
        <label className="filter-check">
          <input
            type="checkbox"
            checked={filterUser}
            onChange={(e) => setFilterUser(e.target.checked)}
          />
          Filter by selected user
        </label>
      </div>

      {/* Table body */}
      <div className="card">
        {loading && <div className="spinner-wrap"><div className="spinner" /></div>}
        {error   && <div className="empty-state"><div className="icon">⚠️</div><p>{error}</p></div>}
        {!loading && !error && rows.length === 0 && (
          <div className="empty-state"><div className="icon">📭</div><p>No data found</p></div>
        )}
        {!loading && !error && rows.length > 0 && (
          <div className="data-table-wrap">
            <table className="data-table">
              <thead>
                <tr>{cols.map((c) => <th key={c.key}>{c.label}</th>)}</tr>
              </thead>
              <tbody>
                {rows.map((row, i) => (
                  <tr key={i}>
                    {cols.map((c) => (
                      <td key={c.key}>{c.render ? c.render(row[c.key], row) : (row[c.key] ?? '—')}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

// ── Column definitions per table ─────────────────────────────────────────────
function getColumns(table) {
  const money = (v) => formatINR(v)
  const pct   = (v) => fmtPct(v)
  const date  = (v) => fmtDate(v)
  const pill  = (v) => <span className={`pill ${statusPill(v)}`}>{v || '—'}</span>

  const defs = {
    'users': [
      { key: 'user_id',   label: 'ID' },
      { key: 'name',      label: 'Name', render: (v) => <strong>{v}</strong> },
      { key: 'email',     label: 'Email' },
      { key: 'phone',     label: 'Phone' },
      { key: 'created_at',label: 'Joined', render: date },
    ],
    'financial-profiles': [
      { key: 'user_id',        label: 'UID' },
      { key: 'age',            label: 'Age' },
      { key: 'occupation',     label: 'Occupation' },
      { key: 'city',           label: 'City' },
      { key: 'monthly_income', label: 'Income/mo', render: money },
      { key: 'monthly_savings',label: 'Savings/mo', render: money },
      { key: 'net_worth',      label: 'Net Worth', render: money },
      { key: 'risk_profile',   label: 'Risk', render: (v) => <span className="pill pill-indigo">{v}</span> },
      { key: 'dependents',     label: 'Deps' },
    ],
    'financial-goals': [
      { key: 'user_id',       label: 'UID' },
      { key: 'goal_name',     label: 'Goal', render: (v) => <strong>{v}</strong> },
      { key: 'goal_category', label: 'Category' },
      { key: 'target_amount', label: 'Target', render: money },
      { key: 'current_savings',label: 'Saved', render: money },
      { key: 'target_date',   label: 'Date', render: date },
      { key: 'status',        label: 'Status', render: pill },
      { key: 'priority',      label: 'Priority', render: (v) => <span className={`pill ${v === 'high' ? 'pill-red' : v === 'medium' ? 'pill-yellow' : 'pill-gray'}`}>{v}</span> },
    ],
    'mutual-funds': [
      { key: 'user_id',       label: 'UID' },
      { key: 'fund_name',     label: 'Fund', render: (v) => <span style={{ fontWeight: 500 }}>{v}</span> },
      { key: 'fund_category', label: 'Category', render: (v) => <span className="pill pill-indigo">{v}</span> },
      { key: 'units_held',    label: 'Units', render: (v) => parseFloat(v).toFixed(2) },
      { key: 'avg_nav',       label: 'Avg NAV', render: (v) => `₹${parseFloat(v).toFixed(2)}` },
      { key: 'invested_amount',label: 'Invested', render: money },
      { key: 'current_value', label: 'Value', render: money },
      { key: 'xirr_pct',     label: 'XIRR%', render: (v) => <span style={{ color: parseFloat(v) >= 12 ? 'var(--green)' : 'var(--yellow)' }}>{fmtPct(v)}</span> },
      { key: 'expense_ratio', label: 'Exp%', render: pct },
    ],
    'tax-profiles': [
      { key: 'user_id',          label: 'UID' },
      { key: 'financial_year',   label: 'FY' },
      { key: 'gross_income',     label: 'Gross', render: money },
      { key: 'section_80c_used', label: '80C Used', render: money },
      { key: 'nps_contribution', label: 'NPS', render: money },
      { key: 'hra_claimed',      label: 'HRA', render: money },
      { key: 'tax_paid',         label: 'Tax Paid', render: money },
      { key: 'tax_regime',       label: 'Regime', render: (v) => <span className="pill pill-blue">{v}</span> },
    ],
    'life-events': [
      { key: 'user_id',       label: 'UID' },
      { key: 'event_type',    label: 'Event', render: (v) => <strong>{v}</strong> },
      { key: 'expected_date', label: 'Expected', render: date },
      { key: 'estimated_cost',label: 'Est. Cost', render: money },
      { key: 'saved_amount',  label: 'Saved', render: money },
      { key: 'planning_status',label: 'Status', render: pill },
    ],
    'insurance': [
      { key: 'user_id',         label: 'UID' },
      { key: 'insurance_type',  label: 'Type' },
      { key: 'provider_name',   label: 'Provider' },
      { key: 'coverage_amount', label: 'Coverage', render: money },
      { key: 'annual_premium',  label: 'Premium/yr', render: money },
      { key: 'policy_start',    label: 'Start', render: date },
      { key: 'policy_end',      label: 'End', render: date },
      { key: 'policy_status',   label: 'Status', render: pill },
    ],
    'health-scores': [
      { key: 'user_id',                  label: 'UID' },
      { key: 'overall_score',            label: 'Overall', render: (v) => <strong style={{ color: 'var(--accent)' }}>{parseFloat(v).toFixed(1)}</strong> },
      { key: 'grade',                    label: 'Grade', render: (v) => <span className="pill pill-green">{v}</span> },
      { key: 'emergency_fund_score',     label: 'Emergency' },
      { key: 'insurance_coverage_score', label: 'Insurance' },
      { key: 'investment_diversity_score',label: 'Invest' },
      { key: 'debt_management_score',    label: 'Debt' },
      { key: 'tax_efficiency_score',     label: 'Tax' },
      { key: 'retirement_readiness_score',label: 'Retire' },
      { key: 'scored_at',                label: 'Date', render: date },
    ],
  }
  return defs[table] || []
}
