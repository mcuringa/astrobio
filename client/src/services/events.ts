export interface NewPlanetEvent {
  id: string
  show: string
}

function isNewPlanetEvent(value: unknown): value is NewPlanetEvent {
  if (typeof value !== 'object' || value === null) return false
  const event = value as Record<string, unknown>
  return typeof event.id === 'string' && event.id.trim() !== '' && typeof event.show === 'string'
}

export function listenForPlanetEvents(
  onPlanet: (event: NewPlanetEvent) => void,
  onEvent?: (event: unknown) => void,
) {
  let stopped = false
  let socket: WebSocket
  let reconnectTimer: ReturnType<typeof setTimeout> | undefined

  function connect() {
    const url = new URL('/ws', window.location.href)
    url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:'
    socket = new WebSocket(url)

    socket.onmessage = ({ data }) => {
      let message: unknown
      try {
        message = JSON.parse(data)
      } catch {
        return
      }
      onEvent?.(message)
      if (typeof message !== 'object' || message === null) return
      const envelope = message as Record<string, unknown>
      const event = envelope.type === 'new_planet' ? envelope : envelope.new_planet
      if (isNewPlanetEvent(event)) onPlanet(event)
    }

    socket.onclose = () => {
      if (!stopped) reconnectTimer = setTimeout(connect, 2000)
    }
    socket.onerror = () => socket.close()
  }

  connect()
  return () => {
    stopped = true
    clearTimeout(reconnectTimer)
    socket.onmessage = null
    socket.onerror = null
    socket.close()
  }
}
