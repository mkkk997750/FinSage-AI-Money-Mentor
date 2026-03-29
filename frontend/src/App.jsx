import { useState } from 'react'
import { AppProvider } from './context/AppContext'
import Topbar from './components/Topbar/Topbar'
import Sidebar from './components/Sidebar/Sidebar'
import Dashboard from './components/Dashboard/Dashboard'
import AgentPanel from './components/AgentPanel/AgentPanel'
import DataTables from './components/DataTables/DataTables'
import Chat from './components/Chat/Chat'
import './styles/global.css'

export default function App() {
  const [activeView,  setActiveView]  = useState('dashboard')
  const [activeAgent, setActiveAgent] = useState('health_score')
  const [activeTable, setActiveTable] = useState('users')

  const navigate = (view, extra = {}) => {
    setActiveView(view)
    if (extra.agent) setActiveAgent(extra.agent)
    if (extra.table) setActiveTable(extra.table)
  }

  const renderView = () => {
    switch (activeView) {
      case 'dashboard': return <Dashboard onNavigate={navigate} />
      case 'agent':     return <AgentPanel activeAgent={activeAgent} setActiveAgent={setActiveAgent} />
      case 'tables':    return <DataTables activeTable={activeTable} setActiveTable={setActiveTable} />
      case 'chat':      return <Chat />
      default:          return <Dashboard onNavigate={navigate} />
    }
  }

  return (
    <AppProvider>
      <div className="app">
        <Topbar />
        <div className="layout">
          <Sidebar
            activeView={activeView}
            activeAgent={activeAgent}
            activeTable={activeTable}
            onNavigate={navigate}
          />
          <main className="main-content">
            {renderView()}
          </main>
        </div>
      </div>
    </AppProvider>
  )
}
