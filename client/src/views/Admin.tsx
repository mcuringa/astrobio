import { useState, type SubmitEvent } from 'react'
import './Admin.css'

export default function Admin() {
  const [text, setText] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [status, setStatus] = useState('')

  async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!text.trim() || submitting) return

    setSubmitting(true)
    setStatus('')

    try {
      const response = await fetch('http://localhost:3000/api/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text.trim() }),
      })
      if (!response.ok) throw new Error('Request failed')
      setStatus('Text sent successfully.')
    } catch {
      setStatus('Unable to send text. Check that the server is running and try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="admin">
      <h1>GM Admin</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="speak-text">Speak Text</label>
        <textarea
          id="speak-text"
          name="text"
          rows={8}
          value={text}
          onChange={(event) => setText(event.target.value)}
          onKeyDown={(event) => {
            if (event.ctrlKey && event.key === 'Enter' && !event.nativeEvent.isComposing) {
              event.preventDefault()
              if (!event.repeat) event.currentTarget.form?.requestSubmit()
            }
          }}
          aria-keyshortcuts="Control+Enter"
          required
        />
        <button type="submit" disabled={submitting || !text.trim()}>
          {submitting ? 'Sending…' : 'Speak'}
        </button>
        <p role="status">{status}</p>
      </form>
    </main>
  )
}
