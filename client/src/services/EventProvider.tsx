import { useEffect, useRef, useState, type ReactNode } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { listenForPlanetEvents } from './events'
import { EventContext, type CurrentPlanet, type EventEntry } from './eventContext'

export function EventProvider({ children }: { children: ReactNode }) {
  const [events, setEvents] = useState<EventEntry[]>([])
  const [currentPlanet, setCurrentPlanet] = useState<CurrentPlanet | null>(null)
  const sequence = useRef(0)
  const location = useLocation()
  const pathname = useRef(location.pathname)
  const navigate = useNavigate()

  useEffect(() => {
    pathname.current = location.pathname
  }, [location.pathname])

  useEffect(() => listenForPlanetEvents((event) => {
    const show = event.show === 'planet-data' ? 'data' : event.show
    if (show !== 'data' && show !== 'nav') return
    setCurrentPlanet({ planet_id: event.id, show })
    if (pathname.current === '/admin' || pathname.current.startsWith('/admin/')) return
    const screen = show === 'data' ? '/planet-data' : '/nav'
    navigate(`${screen}?planet_id=${encodeURIComponent(event.id)}`)
  }, (payload) => {
    const entry = { id: ++sequence.current, time: new Date().toISOString(), payload }
    setEvents((previous) => [entry, ...previous].slice(0, 200))
  }), [navigate])

  return (
    <EventContext.Provider value={{ events, currentPlanet }}>
      {children}
    </EventContext.Provider>
  )
}
