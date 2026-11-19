import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import Admin from './views/Admin'
import LockScreen from './views/LockScreen'
import PlanetData from './views/PlanetData'
import NavScreen from './views/NavScreen'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <main style={{ margin: 'auto', padding: '32px 24px' }}>
              <h1>Astrobio</h1>
              <p>Choose a screen to open.</p>
              <nav
                aria-label="Screen selection"
                style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 16, marginTop: 24 }}
              >
                <Link to="/admin" style={{ padding: '12px 24px', color: 'var(--accent)', border: '1px solid currentColor', borderRadius: 8 }}>
                  Admin
                </Link>
                <Link to="/lockscreen" style={{ padding: '12px 24px', color: 'var(--accent)', border: '1px solid currentColor', borderRadius: 8 }}>
                  LockScreen
                </Link>
                <Link to="/planet-data" style={{ padding: '12px 24px', color: 'var(--accent)', border: '1px solid currentColor', borderRadius: 8 }}>
                  Planet Data
                </Link>
                <Link to="/nav" style={{ padding: '12px 24px', color: 'var(--accent)', border: '1px solid currentColor', borderRadius: 8 }}>
                  Nav Screen
                </Link>
              </nav>
            </main>
          }
        />
        <Route path="/admin" element={<Admin />} />
        <Route path="/lockscreen" element={<LockScreen />} />
        <Route path="/planet-data" element={<PlanetData />} />
        <Route path="/nav" element={<NavScreen />} />
        <Route path="*" element={<LockScreen />} />
      </Routes>
    </BrowserRouter>
  )
}
