import { useState, type SubmitEvent } from 'react'
import './Admin.css'
import { useServerEvents } from '../services/eventContext'

export default function Admin() {
  const { events, currentPlanet } = useServerEvents()
  const [view, setView] = useState<'speech' | 'events' | 'planet'>('speech')
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
      <nav className="admin-views" aria-label="Admin views">
        <button type="button" aria-pressed={view === 'speech'} onClick={() => setView('speech')}>Speak Text</button>
        <button type="button" aria-pressed={view === 'events'} onClick={() => setView('events')}>Event Log</button>
        <button type="button" aria-pressed={view === 'planet'} onClick={() => setView('planet')}>Current Planet</button>
      </nav>
      {view === 'events' && (
        <section aria-labelledby="event-log-heading">
          <h2 id="event-log-heading">Event Log</h2>
          <p>Latest 200 events received in this browser session, newest first.</p>
          {events.length === 0 ? <p>Waiting for events…</p> : (
            <ol className="admin-event-log">
              {events.map((event) => (
                <li key={event.id}>
                  <time dateTime={event.time}>{new Date(event.time).toLocaleTimeString()}</time>
                  <pre>{JSON.stringify(event.payload, null, 2)}</pre>
                </li>
              ))}
            </ol>
          )}
        </section>
      )}
      {view === 'planet' && (
        <section aria-labelledby="current-planet-heading">
          <h2 id="current-planet-heading">Current Planet</h2>
          {currentPlanet ? (
            <dl className="admin-planet">
              <dt>planet_id</dt><dd>{currentPlanet.planet_id}</dd>
              <dt>Screen</dt><dd>{currentPlanet.show}</dd>
            </dl>
          ) : <p>Waiting for a new_planet event…</p>}
        </section>
      )}
      <div hidden={view !== 'speech'}>
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
      </div>
    </main>
  )
}
