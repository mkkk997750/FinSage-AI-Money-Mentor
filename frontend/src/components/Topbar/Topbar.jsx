import { useApp } from '../../context/AppContext'
import './Topbar.css'

export default function Topbar() {
  const { users, activeUserId, selectUser, loading } = useApp()

  const activeUser = users.find((u) => u.user_id === activeUserId)

  return (
    <header className="topbar">
      <div className="topbar-brand">
        <span className="brand-icon">💰</span>
        <div>
          <div className="brand-name">FinSage</div>
          <div className="brand-sub">AI Money Mentor</div>
        </div>
      </div>

      <div className="topbar-center">
        {activeUser && (
          <div className="active-user-info">
            <span className="user-avatar">{activeUser.name?.[0] || '?'}</span>
            <div>
              <div className="user-name">{activeUser.name}</div>
              <div className="user-meta">{activeUser.occupation} · {activeUser.city}</div>
            </div>
            {activeUser.grade && (
              <span
                className="grade-badge"
                style={{ background: gradeColor(activeUser.grade) }}
              >
                {activeUser.grade}
              </span>
            )}
          </div>
        )}
      </div>

      <div className="topbar-right">
        <div className="user-selector-wrap">
          <label>Select User</label>
          {loading ? (
            <div className="topbar-spinner" />
          ) : (
            <select
              value={activeUserId ?? ''}
              onChange={(e) => selectUser(Number(e.target.value))}
              className="form-control"
              style={{ width: 230 }}
            >
              {users.map((u) => (
                <option key={u.user_id} value={u.user_id}>
                  {u.name} — {u.occupation}
                  {u.overall_score ? ` [${Math.round(u.overall_score)}/100]` : ''}
                </option>
              ))}
            </select>
          )}
        </div>
        <span className="hackathon-badge">ET AI Hackathon 2026</span>
      </div>
    </header>
  )
}

function gradeColor(g) {
  return { A: '#10b981', B: '#4f8ef7', C: '#f59e0b', D: '#ef4444' }[g] || '#94a3b8'
}
