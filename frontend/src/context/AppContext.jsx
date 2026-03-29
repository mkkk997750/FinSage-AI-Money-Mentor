import { createContext, useContext, useState, useEffect } from 'react'
import { getUsers } from '../api/client'

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const [users, setUsers]               = useState([])
  const [activeUserId, setActiveUserId] = useState(null)
  const [sessionId, setSessionId]       = useState(null)
  const [loading, setLoading]           = useState(true)

  useEffect(() => {
    getUsers()
      .then((data) => {
        setUsers(data)
        if (data.length > 0) {
          setActiveUserId(data[0].user_id)
          setSessionId(`session_${data[0].user_id}_${Date.now()}`)
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const selectUser = (uid) => {
    setActiveUserId(uid)
    setSessionId(`session_${uid}_${Date.now()}`)
  }

  return (
    <AppContext.Provider value={{ users, activeUserId, selectUser, sessionId, loading }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)
