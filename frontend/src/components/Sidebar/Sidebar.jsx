import { AGENT_MAP } from '../../api/client'
import './Sidebar.css'

const NAV_SECTIONS = [
  {
    title: 'Overview',
    items: [
      { id: 'dashboard', label: 'Dashboard',    icon: '📊', view: 'dashboard' },
      { id: 'chat',      label: 'AI Chat',       icon: '💬', view: 'chat' },
    ],
  },
  {
    title: 'AI Agents',
    items: Object.entries(AGENT_MAP).map(([key, cfg]) => ({
      id: key,
      label: cfg.label,
      icon: cfg.icon,
      view: 'agent',
      agent: key,
      color: cfg.color,
    })),
  },
  {
    title: 'Data Explorer',
    items: [
      { id: 'users',              label: 'Users',          icon: '👤', view: 'tables', table: 'users' },
      { id: 'financial-profiles', label: 'Profiles',       icon: '📂', view: 'tables', table: 'financial-profiles' },
      { id: 'financial-goals',    label: 'Goals',           icon: '🎯', view: 'tables', table: 'financial-goals' },
      { id: 'mutual-funds',       label: 'MF Holdings',    icon: '📈', view: 'tables', table: 'mutual-funds' },
      { id: 'tax-profiles',       label: 'Tax Profiles',   icon: '🧾', view: 'tables', table: 'tax-profiles' },
      { id: 'life-events',        label: 'Life Events',    icon: '🔔', view: 'tables', table: 'life-events' },
      { id: 'insurance',          label: 'Insurance',      icon: '🛡️', view: 'tables', table: 'insurance' },
      { id: 'health-scores',      label: 'Health Scores',  icon: '💯', view: 'tables', table: 'health-scores' },
    ],
  },
]

export default function Sidebar({ activeView, activeAgent, activeTable, onNavigate }) {
  const isActive = (item) => {
    if (item.view !== activeView) return false
    if (item.agent && item.agent !== activeAgent) return false
    if (item.table && item.table !== activeTable) return false
    return true
  }

  return (
    <aside className="sidebar">
      <nav>
        {NAV_SECTIONS.map((section) => (
          <div key={section.title} className="sidebar-section">
            <div className="sidebar-section-title">{section.title}</div>
            {section.items.map((item) => (
              <button
                key={item.id}
                className={`sidebar-item ${isActive(item) ? 'sidebar-item--active' : ''}`}
                onClick={() => onNavigate(item.view, { agent: item.agent, table: item.table })}
                style={isActive(item) && item.color
                  ? { borderLeft: `3px solid ${item.color}`, paddingLeft: 13 }
                  : undefined}
              >
                <span className="sidebar-icon">{item.icon}</span>
                <span className="sidebar-label">{item.label}</span>
                {isActive(item) && item.color && (
                  <span
                    className="active-dot"
                    style={{ background: item.color }}
                  />
                )}
              </button>
            ))}
          </div>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-footer-text">FinSage v1.0</div>
        <div className="sidebar-footer-sub">LangGraph · FastAPI · React</div>
      </div>
    </aside>
  )
}
