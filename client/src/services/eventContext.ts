import { createContext, useContext } from 'react'

export interface CurrentPlanet {
  planet_id: string
  show: 'data' | 'nav'
}

export interface EventEntry {
  id: number
  time: string
  payload: unknown
}

export const EventContext = createContext<{
  events: EventEntry[]
  currentPlanet: CurrentPlanet | null
}>({ events: [], currentPlanet: null })

export const useServerEvents = () => useContext(EventContext)
