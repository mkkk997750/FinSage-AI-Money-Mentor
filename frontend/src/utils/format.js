export function formatINR(amount) {
  if (amount == null || amount === '') return '—'
  const n = parseFloat(amount)
  if (isNaN(n)) return '—'
  if (n >= 1e7) return `₹${(n / 1e7).toFixed(2)} Cr`
  if (n >= 1e5) return `₹${(n / 1e5).toFixed(1)}L`
  return `₹${n.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`
}

export function gradeColor(grade) {
  const map = { A: '#10b981', B: '#4f8ef7', C: '#f59e0b', D: '#ef4444', F: '#dc2626' }
  return map[grade] || '#94a3b8'
}

export function statusPill(status) {
  const cls = {
    active: 'pill-green', pending: 'pill-yellow', completed: 'pill-blue',
    on_track: 'pill-green', behind: 'pill-red', achieved: 'pill-blue',
  }
  return cls[status] || 'pill-gray'
}

export function fmtDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

export function fmtPct(n, digits = 1) {
  if (n == null) return '—'
  return `${parseFloat(n).toFixed(digits)}%`
}
