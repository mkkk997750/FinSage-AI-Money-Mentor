import { useState, useRef, useEffect } from 'react'
import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { useApp } from '../../context/AppContext'
import { AGENT_MAP } from '../../api/client'
import './Chat.css'

const WELCOME = `**Welcome to FinSage AI Chat!** 🎯

You can ask me anything about your finances. Try:
- "What is my financial health score?"
- "How much SIP do I need for FIRE?"
- "Analyse my tax situation"
- "Review my insurance coverage"
- "Run a full analysis"

_Select a user from the top bar to get personalized insights._`

function detectAgent(text) {
  const t = text.toLowerCase()
  if (t.includes('health') || t.includes('score'))        return 'health_score'
  if (t.includes('fire') || t.includes('retire') || t.includes('sip')) return 'fire_planner'
  if (t.includes('tax') || t.includes('80c') || t.includes('nps'))     return 'tax_wizard'
  if (t.includes('insur') || t.includes('policy'))        return 'insurance'
  if (t.includes('marriage') || t.includes('baby') || t.includes('bonus') || t.includes('event')) return 'life_event'
  if (t.includes('couple') || t.includes('partner'))      return 'couple_planner'
  if (t.includes('mutual') || t.includes('mf') || t.includes('xray') || t.includes('xirr'))  return 'mf_xray'
  if (t.includes('full') || t.includes('complete') || t.includes('everything')) return 'full_analysis'
  return null
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
  const k = fields[agentKey]
  if (k && result.result && typeof result.result === 'object' && result.result[k]) return result.result[k]
  if (k && result[k]) return result[k]
  
  if (agentKey === 'full_analysis' && result.messages) {
    const reportMsg = result.messages.slice().reverse().find(m => m.node === 'report_generator' || (m.content && m.content.includes('# 📊 FinSage')))
    if (reportMsg) return reportMsg.content
  }

  if (result.messages?.length) return result.messages[result.messages.length - 1]?.content || null
  return null
}

export default function Chat() {
  const { activeUserId, sessionId } = useApp()
  const [messages, setMessages] = useState([{ role: 'assistant', content: WELCOME }])
  const [input,    setInput]    = useState('')
  const [loading,  setLoading]  = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const send = async () => {
    const text = input.trim()
    if (!text || loading) return
    setInput('')

    const userMsg = { role: 'user', content: text }
    setMessages((prev) => [...prev, userMsg])

    if (!activeUserId) {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: '⚠️ Please select a user from the top bar first!',
      }])
      return
    }

    setLoading(true)
    const agentKey = detectAgent(text)

    if (!agentKey) {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: `I can help with financial analysis! Try mentioning keywords like **health score**, **FIRE planning**, **tax**, **insurance**, **MF portfolio**, **life events**, or ask for a **full analysis**. 💡`,
      }])
      setLoading(false)
      return
    }

    try {
      const cfg  = AGENT_MAP[agentKey]
      const body = { user_id: activeUserId, session_id: sessionId || `chat_${Date.now()}` }
      const res  = await cfg.fn(body)
      const report = extractReport(res, agentKey)

      setMessages((prev) => [...prev, {
        role: 'assistant',
        agentKey,
        content: report || `Analysis completed. ${cfg.icon} **${cfg.label}** ran successfully.`,
      }])
    } catch (e) {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: `⚠️ **Error**: ${e.message}\n\nMake sure the backend is running and the database is connected.`,
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
  }

  return (
    <div className="chat">
      <div className="chat-header card">
        <div className="chat-header-left">
          <span className="chat-avatar">🤖</span>
          <div>
            <div className="chat-title">FinSage AI Chat</div>
            <div className="chat-sub">Powered by LangGraph · {Object.keys(AGENT_MAP).length} agents ready</div>
          </div>
        </div>
        <div className="chat-agents-row">
          {Object.entries(AGENT_MAP).map(([k, cfg]) => (
            <span key={k} className="chat-agent-pill" style={{ background: `${cfg.color}18`, color: cfg.color }}>
              {cfg.icon}
            </span>
          ))}
        </div>
      </div>

      <div className="chat-messages card">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`chat-msg ${msg.role === 'user' ? 'chat-msg--user' : 'chat-msg--assistant'}`}
          >
            {msg.role === 'assistant' && (
              <div className="msg-avatar">
                {msg.agentKey ? AGENT_MAP[msg.agentKey]?.icon : '🤖'}
              </div>
            )}
            <div className={`msg-bubble ${msg.role === 'user' ? 'bubble-user' : 'bubble-assistant'}`}>
              {msg.agentKey && (
                <div className="msg-agent-label">
                  {AGENT_MAP[msg.agentKey]?.icon} {AGENT_MAP[msg.agentKey]?.label}
                </div>
              )}
              <div className="md-output">
                <Markdown remarkPlugins={[remarkGfm]}>{msg.content}</Markdown>
              </div>
            </div>
            {msg.role === 'user' && (
              <div className="msg-avatar msg-avatar--user">U</div>
            )}
          </div>
        ))}

        {loading && (
          <div className="chat-msg chat-msg--assistant">
            <div className="msg-avatar">🤖</div>
            <div className="msg-bubble bubble-assistant">
              <div className="typing-indicator">
                <span /><span /><span />
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="chat-input-bar card">
        <textarea
          className="chat-input form-control"
          placeholder="Ask about your finances… (Enter to send)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          rows={2}
          disabled={loading}
        />
        <button
          className="btn btn-primary chat-send"
          onClick={send}
          disabled={loading || !input.trim()}
        >
          {loading ? <div className="btn-spinner" /> : '➤'}
        </button>
      </div>
    </div>
  )
}
