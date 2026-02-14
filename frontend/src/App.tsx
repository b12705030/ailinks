import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import LinksPage from './pages/LinksPage'
import ReportsPage from './pages/ReportsPage'
import AddLinkPage from './pages/AddLinkPage'

function App() {
  return (
    <Router
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <Layout>
        <Routes>
          <Route path="/" element={<LinksPage />} />
          <Route path="/add" element={<AddLinkPage />} />
          <Route path="/reports" element={<ReportsPage />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

